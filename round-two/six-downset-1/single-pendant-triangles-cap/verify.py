"""Whole portable replay of single-pendant certificates and both actual small cases."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):os.environ[name]='1'
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import prod
import argparse,copy,json,signal,time,resource,sys
from certificate import generate
from check_certificate import check as certificate_check,check_row
from original import fixed_control,control,baseline
from sharp import repaired,pair_data
from sectors import parameters,check_reduced
from model import forms
from builder import build
from exact import require,psd_rank,check as matrix_check,lift
from bivariate import P

def uniform_point(q,r):
    require(type(r) is int and r>=2 and q>=4*r,'exact uniform single-pendant domain')
    return forms(q,r,1)

def damages(cert):
    labels=[]
    def reject(name,action):
        try:action()
        except (ValueError,KeyError):labels.append(name);return
        raise ValueError('accepted semantic damage: '+name)
    def alter(name,change):
        def run():
            row=copy.deepcopy(cert['rows'][0]);change(row);check_row(row)
        reject(name,run)
    alter('negative positivity coefficient',lambda a:a['shifted']['terms'][0].__setitem__(1,'-1'))
    alter('missing positive constant',lambda a:a['shifted'].__setitem__('terms',[t for t in a['shifted']['terms'] if t[0]!=[0,0]]))
    alter('duplicate coefficient',lambda a:a['shifted']['terms'].append(a['shifted']['terms'][0]))
    alter('wrong exponent dimension',lambda a:a['shifted']['terms'][0][0].append(0))
    alter('wrong original numerator',lambda a:a['original']['terms'][0].__setitem__(1,str(int(a['original']['terms'][0][1])+1)))
    alter('wrong complete cleared binding',lambda a:a['cleared_original_matrix'][0][0]['terms'][0].__setitem__(1,str(int(a['cleared_original_matrix'][0][0]['terms'][0][1])+1)))
    alter('negative row multiplier',lambda a:a['positive_row_constants'].__setitem__(0,'-1'))
    alter('changed positive factor orientation',lambda a:a['denominator_factors'][0]['original']['terms'][0].__setitem__(1,str(int(a['denominator_factors'][0]['original']['terms'][0][1])+1)))
    alter('zero denominator exponent',lambda a:a['denominator_factors'][0].__setitem__('power',0))
    reject('missing last inverse minor',lambda:certificate_check({'rows':cert['rows'][:-1]}))
    changed=copy.deepcopy(cert);changed['rows'][0]['group']='fake'
    reject('wrong whole obligation catalogue',lambda:certificate_check(changed))
    reject('r1 excluded uniform domain',lambda:uniform_point(F(8),1))
    reject('small actual q4 is no uniform-domain point',lambda:uniform_point(F(4),2))
    reject('small actual q8r3 is no uniform-domain point',lambda:uniform_point(F(8),3))
    # The coarse final test fails, while complete original caps pass below the domain.
    reject('false sufficient inverse cap at actual small q4',lambda:psd_rank(forms(4,2,1)['final']))
    family,C,W,p,*_=build(3,2,1,mean_recipe='cap-harmonic')
    small=repaired(3,2);delta=F(small['sharp_delta']);private=[2*p['q']-1+2*i for i in range(p['m'])]
    cp=[v[:] for v in C]
    for i in range(3):cp[private[i]][private[-1]]+=delta;cp[private[-1]][private[i]]+=delta
    seed=lift(C,p['s']);changed=lift(cp,p['s'])
    for i in range(p['N']):changed[0][i]=seed[0][i];changed[i][0]=seed[i][0]
    reject('retaining old empty row and loop after sharp repair',lambda:matrix_check(family,changed,p['s']))
    def missing_empty():
        u,v=pair_data(p['N'],private,private[-1]);u[0]=0
        require(sum(u)==0 and sum(x*x for x in u)==12,'actual whole pair Gram')
    reject('omitted empty coordinate in norm',missing_empty)
    return labels

def arithmetic():
    rows=[]
    for k in range(12):
        a={e:(-1)**(sum(e)+k)*(2**(12+k)+sum(e)+k) for e in product(range(4),repeat=2) if (sum(e)+k)%3}
        b={e:(-1)**(e[0]+k)*(3**(8+k)+prod(e)+1) for e in product(range(3),repeat=2)}
        expected={}
        for x,c in a.items():
            for y,d in b.items():
                e=tuple(v+w for v,w in zip(x,y));expected[e]=expected.get(e,0)+c*d
        expected={e:c for e,c in expected.items() if c};actual=P(a)*P(b)
        require(actual.a==expected and actual.den==1,'independent every-coefficient signed convolution')
        quotient=actual.exact_div(P(a));require(quotient==P(b),'every coefficient exact division multiplication-back')
        rows.append({'control':k,'terms':len(actual.a),'fingerprint':actual.fingerprint()})
    return rows

def compact(record):
    out={k:v for k,v in record.items() if k not in ('certificate','all_scalar_controls')}
    out['certificate']={k:v for k,v in record['certificate'].items() if k!='rows'}
    out['certificate']['rows']=[{'group':r['group'],'order':r['order'],'positive_coefficients':len(r['shifted']['terms']),'fingerprint':r['fingerprint']} for r in record['certificate']['rows']]
    out['scalar_control_coverage']={'r':list(range(2,11)),'q':'4r,4r+1/2,8r,1000000','cases':len(record['all_scalar_controls'])}
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',type=Path);parser.add_argument('--check',type=Path);args=parser.parse_args()
    signal.alarm(60);start=time.monotonic();cert=generate();identities=certificate_check(cert)
    controls=[fixed_control(F(q),r,1) for r,q in ((2,8),(3,12),(4,16),(2,F(17,2)),(8,32),(1000,4000),(20,1000000),(4,20))]
    scalars=[]
    for r in range(2,11):
        for q in (F(4*r),F(8*r+1,2),F(8*r),F(1000000)):
            f=uniform_point(q,r);p=f['p']
            require(all(p[k]>0 for k in ('mu','alpha','beta','etaP','nuT','C')),'all exact scalar uniform controls')
            require(all(psd_rank(f[k])==len(f[k]) for k in ('anti','triangle','augmented','final')),'every sufficient scalar form positive')
            scalars.append({'r':r,'q':str(q),'norms':{k:str(p[k]) for k in ('mu','alpha','beta','etaP','nuT','C')}})
    fixtures=[repaired(n,r) for n,r in ((3,2),(4,3),(4,2),(5,3),(5,4))]
    old=baseline();rejects=damages(cert);arith=arithmetic()
    counts={'positive_coefficients':sum(len(r['shifted']['terms']) for r in cert['rows']),'uniform_obligations':15,
            'full_identity_points':sum(r['full_identity_points'] for r in identities),'full_numerator_shift_points':sum(r['full_shift_points'] for r in identities),
            'full_denominator_shift_points':sum(r['full_factor_shift_points'] for r in identities),'full_clearing_factor_shift_points':sum(r['full_clearing_factor_shift_points'] for r in identities),
            'symbolic_arrow_positions':9,'symbolic_augmented_positions':4,'symbolic_residual_identities':6,
            'fixed_controls':len(controls),'grouped_frame_positions':64*len(controls),'triangle_update_positions':16*len(controls),
            'triangle_Schur_positions':4*len(controls),'anti_congruence_positions':4*len(controls),'Gaussian5_inverse_controls':len(controls),
            'scalar_controls':len(scalars),'actual_fixtures':len(fixtures),'all_original_positions_per_seed_or_repair':sum(r['N']**2 for r in fixtures),
            'all_sharp_repair_identity_positions':sum(r['whole_repair_identity_positions'] for r in fixtures),'all_sharp_cap_positions':sum(r['whole_cap_positions'] for r in fixtures),
            'original_reduced_Gram_positions':sum(r['old_complete_correspondence']['Gram_positions'] for r in fixtures),'original_reduced_frame_positions':sum(r['old_complete_correspondence']['frame_positions'] for r in fixtures),
            'original_changed_Gram_positions':sum(r['old_complete_correspondence']['changed_Gram_positions'] for r in fixtures),'original_changed_frame_positions':sum(r['old_complete_correspondence']['changed_frame_positions'] for r in fixtures),
            'actual_untouched_high':sum(r['old_complete_correspondence']['untouched_high'] for r in fixtures),'actual_untouched_low':sum(r['old_complete_correspondence']['untouched_low'] for r in fixtures),
            'actual_star_kernels':sum(r['actual_star_kernels'] for r in fixtures),'semantic_damages':len(rejects),'signed_arithmetic_controls':len(arith)}
    require(counts['positive_coefficients']==1573 and counts['full_identity_points']==5060,'entire exact uniform certificate counts')
    data={'agent':'six-downset-1','role':'researcher','certificate':cert,'identity_checks':identities,'fixed_controls':controls,'all_scalar_controls':scalars,
          'actual_fixtures':fixtures,'prior9408_baseline':old,'semantic_damages':rejects,'arithmetic_controls':arith,'counts':counts,
          'proof_status':'Exact uniform sign identities plus ordinary unformalized complete-space/inverse/coverage/repair/all-real rank bridges',
          'independent_review':False,'formalization':False,'sharp_norm_credit':'9723;new l1 seed not reviewed there'}
    def exact_json(z):
        if isinstance(z,F):return str(z)
        raise TypeError(type(z).__name__)
    raw=json.dumps(data,sort_keys=True,separators=(',',':'),default=exact_json).encode();data=json.loads(raw);digest=sha256(raw).hexdigest();record={**data,'record_sha256':digest}
    if args.check:require(json.loads(args.check.read_text())==record,'ENTIRE regenerated full mathematical record agrees')
    expected=Path(__file__).with_name('RESULTS.json')
    if expected.exists():require(json.loads(expected.read_text())==compact(record),'ENTIRE compact data and full regenerated hash agree')
    elif not args.record:raise FileNotFoundError('RESULTS.json missing; use --record for first checked reconstruction')
    if args.record:args.record.write_text(json.dumps(record,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({'agent':'six-downset-1','role':'researcher','status':'PASS','record_sha256':digest,'counts':counts,'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'optimized':bool(sys.flags.optimize),'whole_record_compared':bool(args.check),'independent_review':False,'formalization':False},sort_keys=True))

if __name__=='__main__':main()
