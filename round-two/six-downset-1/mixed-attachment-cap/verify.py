"""Portable complete replay: exact coefficients/identities and original witnesses."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[name]='1'
import argparse,json,signal,time,resource,sys,copy
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import prod
from certificate import generate
from check_certificate import check,check_row,decode
from analytic import scalar,constants
from original import fixed_control,actual,baseline
from sectors import parameters,check_reduced
from exact import require,psd_rank
from model import arrow
from trivariate import P

def arithmetic():
    rows=[]
    for k in range(12):
        a={ex:((-1)**(sum(ex)+k))*(2**(10+k)+prod(ex)+k+1)
           for ex in product(range(3),repeat=3) if (sum(ex)+k)%4!=0}
        b={ex:((-1)**(ex[0]+k))*(3**(7+k)+sum(ex)+1)
           for ex in product(range(2),repeat=3)}
        expected={}
        for ex,x in a.items():
            for ey,y in b.items():
                ez=tuple(x+y for x,y in zip(ex,ey));expected[ez]=expected.get(ez,0)+x*y
        expected={e:c for e,c in expected.items() if c}
        result=P(a)*P(b)
        require(result.a==expected and result.den==1,'independent FULL three-variable signed integer convolution')
        quotient=result.exact_div(P(a))
        require(quotient is not None and quotient.a==P(b).a and quotient.den==1,'exact division and all coefficient multiplication-back')
        rows.append({'control':k,'terms':len(result.a),'fingerprint':result.fingerprint()})
    return rows

def damages(certificate):
    labels=[]
    def rejection(label,change,action=check_row):
        row=copy.deepcopy(certificate['rows'][0]);change(row)
        try:action(row)
        except (ValueError,KeyError):labels.append(label);return
        raise ValueError('accepted semantic damage: '+label)
    def negative(row):row['shifted']['terms'][0][1]='-1'
    rejection('negative sign coefficient',negative)
    def zero(row):
        row['shifted']['terms']=[p for p in row['shifted']['terms'] if p[0]!=[0,0,0]]
    rejection('missing strictly positive constant',zero)
    def duplicate(row):row['shifted']['terms'].append(row['shifted']['terms'][0])
    rejection('duplicate coefficient',duplicate)
    def wrongdim(row):row['shifted']['terms'][0][0].append(0)
    rejection('wrong variable dimension',wrongdim)
    def changed_original(row):row['original']['terms'][0][1]=str(int(row['original']['terms'][0][1])+1)
    rejection('wrong original-variable polynomial',changed_original)
    def changed_matrix(row):row['cleared_matrix'][0][0]['terms'][0][1]=str(int(row['cleared_matrix'][0][0]['terms'][0][1])+1)
    rejection('wrong complete cleared matrix',changed_matrix)
    def negative_multiplier(row):row['positive_row_constants'][0]='-1'
    rejection('negative row multiplier',negative_multiplier)
    def changed_den(row):row['denominator_factors'][0]['shifted']['denominator']=2
    rejection('wrong positive denominator normalization',changed_den)
    try:check({'rows':certificate['rows'][:-1]})
    except ValueError:labels.append('missing greatest-order determinant')
    else:raise ValueError('accepted missing fourth determinant')
    try:scalar(F(8),2,2)
    except ValueError:labels.append('using r>=3 estimates on r2 boundary')
    else:raise ValueError('accepted excluded analytic boundary')
    try:scalar(F(11),3,2)
    except ValueError:labels.append('q below stated uniform domain')
    else:raise ValueError('accepted smaller q domain')
    legacy=parameters(64,3,4,'legacy')
    require(legacy['m']*legacy['cross']>legacy['N']-1,'credited exact failure of legacy mean recipe')
    try:check_reduced(64,3,4,'legacy')
    except ValueError:labels.append('legacy uncapped mean recipe')
    else:raise ValueError('accepted known legacy fixed-space failure')
    aug,_=arrow(12,3,2);damaged=[v[:] for v in aug];damaged[-1][-1]-=1
    try:psd_rank(damaged)
    except ValueError:labels.append('wrong inverse bound')
    else:raise ValueError('accepted invalid augmented inverse bound')
    require(len(labels)==13,'whole semantic damage suite')
    return labels

def compact(record):
    out={k:v for k,v in record.items() if k not in ('certificate','all_analytic_controls')}
    out['certificate']={k:v for k,v in record['certificate'].items() if k!='rows'}
    out['certificate']['rows']=[{'order':r['order'],'positive_coefficients':len(r['shifted']['terms']),
                                'fingerprint':r['fingerprint'],'original_terms':len(r['original']['terms'])}
                               for r in record['certificate']['rows']]
    out['analytic_control_coverage']={'r':list(range(3,11)),'l':list(range(2,11)),
                                    'q':'4(r+l-2),base+1/2,2base,1000000',
                                    'cases':len(record['all_analytic_controls'])}
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--record',type=Path);parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    def alarm(*_):raise TimeoutError('unchanged60s complete replay guard')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    certificate=generate();identities=check(certificate);bounds=constants()
    scalars=[]
    for r in range(3,11):
        for l in range(2,11):
            q=4*(r+l-2)
            for Q in (F(q),F(2*q+1,2),F(2*q),F(1000000)):scalars.append(scalar(Q,r,l))
    controls=[fixed_control(F(q),r,l) for r,l,q in
              ((3,2,12),(3,2,13),(4,2,16),(3,3,16),(8,10,64),
               (1000,2,4000),(3,1000,4004),(1000,1000,7992))]
    old=baseline();fixtures=[actual(4,2,2),actual(5,3,2)]
    rejects=damages(certificate);arith=arithmetic()
    counts={'positive_leading_coefficients':sum(len(r['shifted']['terms']) for r in certificate['rows']),
            'uniform_leading_minors':4,'full_degree_bounded_Gaussian_identity_points':sum(r['full_identity_points'] for r in identities),
            'full_quadrant_substitution_points':sum(r['full_shift_points'] for r in identities),
            'full_denominator_substitution_points':sum(r['full_factor_shift_points'] for r in identities),
            'exact_analytic_constant_margins':len(bounds),'analytic_control_cases':len(scalars),
            'fixed_controls':len(controls),'fixed_grouping_positions':64*len(controls),
            'Gaussian5_inverse_controls':len(controls),'triangle_update_positions':16*len(controls),
            'triangle_Schur_positions':4*len(controls),'anti_congruence_positions':4*len(controls),
            'pendant_update_positions':9*len(controls),'pendant_Schur_positions':4*len(controls),
            'symbolic_arrow_positions':9,'symbolic_augmented_positions':4,
            'actual_original_fixtures':len(fixtures),'actual_positions_per_seed_or_repair':sum(r['N']**2 for r in fixtures),
            'original_reduced_Gram_positions':sum(r['Gram_positions'] for r in fixtures),
            'original_reduced_frame_positions':sum(r['frame_positions'] for r in fixtures),
            'whole_changed_Gram_positions':sum(r['changed_Gram_positions'] for r in fixtures),
            'whole_changed_frame_positions':sum(r['changed_frame_positions'] for r in fixtures),
            'actual_untouched_high':sum(r['untouched_high'] for r in fixtures),
            'actual_untouched_low':sum(r['untouched_low'] for r in fixtures),
            'actual_forced_star_kernels':sum(r['actual_maximum_star_kernels'] for r in fixtures),
            'semantic_damages':len(rejects),'signed_arithmetic_controls':len(arith)}
    require(counts['positive_leading_coefficients']==588 and counts['full_degree_bounded_Gaussian_identity_points']==22790,'exact complete certificate coverage')
    data={'agent':'six-downset-1','role':'researcher','certificate':certificate,'identity_checks':identities,
          'analytic_constants':bounds,'all_analytic_controls':scalars,'whole_fixed_controls':controls,
          'prior9408_baseline':old,'actual_original_fixtures':fixtures,'semantic_damages':rejects,
          'signed_arithmetic_controls':arith,'counts':counts,
          'proof_status':'Exact uniform fixed signs plus ordinary unformalized analytic/complete-space/inverse/rank/repair proofs',
          'independent_review':False,'formalization':False}
    def exact_json(z):
        if isinstance(z,F):return str(z)
        raise TypeError('unexpected mathematical record type: '+type(z).__name__)
    raw=json.dumps(data,sort_keys=True,separators=(',',':'),default=exact_json).encode()
    data=json.loads(raw)
    digest=sha256(raw).hexdigest()
    record={**data,'record_sha256':digest}
    if args.check:require(json.loads(args.check.read_text())==record,'ENTIRE expected/replayed mathematical record agrees')
    expected=Path(__file__).with_name('RESULTS.json')
    if expected.exists():
        oldresult=json.loads(expected.read_text())
        require(oldresult==compact(record),'ENTIRE public compact data and regenerated full record hash agree')
    elif args.record is None:raise FileNotFoundError('RESULTS.json missing; use --record for a checked first reconstruction')
    if args.record:args.record.write_text(json.dumps(record,indent=2)+'\n')
    signal.alarm(0)
    summary={'agent':'six-downset-1','role':'researcher','status':'PASS','record_sha256':digest,'counts':counts,
             'seconds':time.monotonic()-start,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'optimized':bool(sys.flags.optimize),'whole_record_compared':bool(args.check),
             'independent_review':False,'formalization':False}
    print(json.dumps(summary,sort_keys=True))

if __name__=='__main__':main()
