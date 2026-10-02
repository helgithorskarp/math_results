#!/usr/bin/env python3
"""Serial exact replay. Python3 standard library only; -O checks stay active."""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_name]='1'
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse,itertools,json,random,resource,signal,time,ast
from exact import require,psd_rank,check,lift,matvec,dot,vecadd,scale,fingerprint
from bivariate import P,R,atom,LIMIT,value
from polynomial import identity,clear_rows
from certificate import component_certificate,fixed_certificate
from original import original,original_low_rank,build,forms
from model import reduced,fixed
import baseline9408

def packed(data):return json.dumps(data,sort_keys=True,separators=(',',':')).encode()

def alarm(*_):raise TimeoutError('unchanged exact stage60s guard')

def stage(function,*args):
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
    try:return function(*args)
    finally:signal.alarm(0)

def direct_product(a,b):
    out={}
    for i,x in a.a.items():
        for j,y in b.a.items():
            ex=(i[0]+j[0],i[1]+j[1])
            out[ex]=out.get(ex,F(0))+F(x,a.den)*F(y,b.den)
    return P.fractions(out)

def arithmetic_controls():
    rng=random.Random(610102);rows=[]
    for trial in range(8):
        width=2 if trial<2 else 5
        a=P.fractions({ex:F(rng.choice((-7,-3,-1,1,2,5)),rng.randrange(1,6))
                       for ex in itertools.product(range(width),repeat=2)})
        b=P.fractions({ex:F(rng.choice((-5,-2,-1,1,3,7)),rng.randrange(1,6))
                       for ex in itertools.product(range(width),repeat=2)})
        product=a*b;require(product==direct_product(a,b),'ALL direct/packed product coefficients')
        quotient=product.exact_div(a)
        require(quotient==b and direct_product(a,quotient)==product,'exact quotient and separate multiplication back')
        rows.append({'trial':trial,'packed_branch':len(a.a)*len(b.a)>256,
                     'product_fingerprint':product.fingerprint(),'quotient_fingerprint':quotient.fingerprint()})
    return rows

def baseline():
    family,s,C,W,_=baseline9408.build(3);N=len(family)
    require(N==16 and s==7 and psd_rank(W)==3,'credited9408 baseline residual')
    M=lift(C,s);result=check(family,M,s)
    Q=[[(N-s)*M[i][j]+s*int(i==j)-1 for j in range(N)] for i in range(N)]
    gap=[[(N-1)*(int(i==j)-F(1,N))-Q[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(gap)==N-1,'complete credited9408 balanced-seed cap')
    return {'source_commit':'f8255e1d617237421c32b3d1e13dd865bffd50c4','n':3,'N':N,
            'core_positions':225,'residual_positions':16,'core_sha256':fingerprint(C),
            'residual_sha256':fingerprint(W),'seed':result,
            'status':'prior validation; one-pendant mean/internal coupling is different'}

def rejections():
    rows=[]
    def reject(label,fn):
        try:fn()
        except ValueError as error:rows.append({'label':label,'reason':str(error)})
        else:raise ValueError('invalid semantic input accepted: '+label)
    reject('negative PSD pivot',lambda:psd_rank([[-1]]))
    reject('singular PSD residual coupling',lambda:psd_rank([[0,1],[1,0]]))
    reject('nonsymmetric PSD matrix',lambda:psd_rank([[1,1],[0,1]]))
    reject('zero polynomial at quadrant boundary',lambda:require(P({(1,0):1}).positive(),'strict constant required'))
    reject('negative quadrant coefficient',lambda:require(P({(0,0):3,(1,0):-1}).positive(),'coefficient sign required'))
    reject('false determinant polynomial',lambda:identity([[P(1)]],P(2)))
    key,unused=atom(P({(1,0):1}))
    reject('denominator vanishes at quadrant boundary',lambda:clear_rows([[R(1,{key:1})]]))
    reject('unchanged512 term guard',lambda:P({(j,0):1 for j in range(LIMIT+1)}))
    family,C,W,p,*rest=build(3,2);N=len(family);s=p['s'];seed=lift(C,s)
    reject('unrepaired seed called greatest rank',lambda:require(check(family,seed,s)['lower_rank']==N-1,'greatest rank requires repair'))
    broken=[row[:] for row in seed];broken[1][1]=1
    reject('mandatory nonempty entry changed',lambda:check(family,broken,s))
    broken=[row[:] for row in seed];broken[0][0]+=1
    reject('actual empty row sum changed',lambda:check(family,broken,s))
    reject('actual empty vertex removed',lambda:check(family[1:],[row[1:] for row in seed[1:]],s))
    badlabels=family[:];badlabels[-1]=badlabels[-2]
    reject('actual private labels collide',lambda:check(badlabels,seed,s))
    reject('excluded l1 orthogonal means imported',lambda:build(3,1))
    reject('too many distinct marks',lambda:build(3,3))
    sectors,parameters=reduced(4,2);G,S=sectors['fixed']
    K=[F(1),F(2,3),F(1),F(1,3),F(0),F(1),F(0),F(0)]
    image=matvec(G,K)
    omitted=[[S[i][j]-image[i]*image[j]/6 for j in range(8)] for i in range(8)]
    reject('empty update omitted from grouped fixed frame',lambda:require(omitted==S,'entire fixed frame required'))
    S3,S2,parameters,info=fixed(4,2)
    rho=F(3,5);goodcross=[F(1,3)+rho/2,1-rho,rho-1]
    badcross=goodcross[:];badcross[2]=1-rho
    reject('arrow congruence last cross sign reversed',lambda:require(badcross==goodcross,'exact inverse-bound congruence required'))
    kappa=9*F(1,2)/p['nuL']+3/(2*p['cross']);excessive=7/kappa
    badW=[row[:] for row in W]
    for i in range(3):badW[i][-1]+=excessive;badW[-1][i]+=excessive
    require(6*excessive-kappa*excessive**2<0,'excessive repair scalar Schur negative')
    reject('excessive disjoint-entry repair',lambda:psd_rank(badW))
    return rows

def run():
    start=time.monotonic()
    component=stage(component_certificate);fixed_record=stage(fixed_certificate)
    arithmetic=stage(arithmetic_controls);old=stage(baseline)
    fixed_controls=[stage(original_low_rank,q,l) for q,l in
                    ((4,2),(5,2),(8,3),(9,3),(16,4),(32,5),(100,10),(1000,100))]
    fixtures=[stage(original,n,l) for n,l in ((3,2),(4,2),(4,3),(5,4),(6,2),(6,5))]
    invalid=stage(rejections)
    small=[minor for row in component['cap_component_certificates'] for minor in row['minors']]
    fixed_minors=[minor for row in fixed_record['certificate'] for minor in row['minors']]
    counts={'positive_norm_coefficients':sum(row['terms'] for row in component['norms']),
            'uniform_leading_minors':len(small)+len(fixed_minors),
            'uniform_leading_minor_coefficients':sum(row['terms'] for row in small+fixed_minors),
            'full_degree_bounded_identity_points':sum(row['full_grid_points'] for row in small)+sum(row['identity_grid_points'] for row in fixed_minors),
            'exact_symbolic_arrow_congruence_positions':fixed_record['exact_arrow_congruence_identity_positions'],
            'rational_scalar_component_positions':component['scalar_identity_controls']+fixed_record['numeric_identity_positions'],
            'direct_arithmetic_controls':len(arithmetic),'fixed_frame_controls':len(fixed_controls),
            'independent_Gaussian5_inverse_controls':len(fixed_controls),
            'fixed_frame_grouping_positions':sum(row['fixed_positions'] for row in fixed_controls),
            'actual_original_fixtures':len(fixtures),
            'actual_positions_per_seed_or_repair':sum(row['full_original_positions'] for row in fixtures),
            'original_reduced_Gram_positions':sum(row['reduced_Gram_positions'] for row in fixtures),
            'original_reduced_frame_positions':sum(row['reduced_frame_positions'] for row in fixtures),
            'complete_changed_Gram_positions':sum(row['changed_Gram_positions'] for row in fixtures),
            'complete_changed_frame_positions':sum(row['changed_frame_positions'] for row in fixtures),
            'untouched_high_directions':sum(row['untouched_high'] for row in fixtures),
            'untouched_low_directions':sum(row['untouched_low'] for row in fixtures),
            'semantic_damages_rejected':len(invalid)}
    data={'agent':'six-downset-1','role':'researcher','domain':'every integer n>=3 and2<=l<=n-1; distinct old triangle and pendant marks; all private points distinct',
          'conclusion':'explicit rational capped H, lowerN-1 greatest among all real ordinary H, upperN-1, scaled gap>=3/4',
          'proof_status':'author-checked exact uniform polynomial certificate plus ordinary unformalized complete-space, inverse and rank bridges; independently unreviewed',
          'component':component,'fixed':fixed_record,'arithmetic_controls':arithmetic,'credited_baseline':old,
          'fixed_original_controls':fixed_controls,'actual_fixtures':fixtures,'semantic_rejections':invalid,'counts':counts,
          'resource_guards':{'native_threads':1,'serial_CPU_jobs':1,'stage_seconds':60,'literal_n_max':6,'literal_N_max':80,'bivariate_terms':512,'packing_bytes':32*1024*1024}}
    data=json.loads(packed(data));return {**data,'record_sha256':sha256(packed(data)).hexdigest()},time.monotonic()-start

def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group()
    group.add_argument('--record',type=Path);group.add_argument('--check',type=Path);args=parser.parse_args()
    record,seconds=run()
    if args.record:args.record.write_bytes(packed(record)+b'\n')
    if args.check:require(json.loads(args.check.read_text())==record,'ENTIRE frozen mathematical record differs')
    print(json.dumps({'status':'PASS','record_sha256':record['record_sha256'],'entire_record_compared':bool(args.check),
                      'seconds':seconds,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'counts':record['counts']},sort_keys=True))

if __name__=='__main__':main()
