#!/usr/bin/env python3
"""Serial exact replay; Python3 standard library; checks remain active under -O."""
import os
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
              'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_name]='1'
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse,itertools,json,random,resource,signal,time
from exact import require,psd_rank,check,lift,matvec,dot,scale
from bivariate import P,R,atom,LIMIT
from polynomial import identity,clear_rows
from certificate import sign_certificate
from links import links_certificate
from original import fixed_control,actual
from verify_original import baseline
from builder import build
from sectors import reduced
from model import fixed,parameters


def packed(data):return json.dumps(data,sort_keys=True,separators=(',',':')).encode()


def compact(data):
    """Keep the hash of ALL coefficients; regenerate coefficients at replay.

    The reader-facing record retains every other mathematical field. No
    external corpus or precomputed polynomial is needed for validation.
    """
    if isinstance(data,dict):return {k:compact(v) for k,v in data.items() if k!='polynomial'}
    if isinstance(data,list):return [compact(v) for v in data]
    return data


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
    family,C,W,p,*_=build(4,2,2,mean_recipe='cap-harmonic');N=p['N'];s=p['s'];seed=lift(C,s)
    reject('unrepaired seed called greatest rank',lambda:require(check(family,seed,s)['lower_rank']==N-2,'greatest rank requires repair'))
    broken=[row[:] for row in seed];broken[1][1]=1
    reject('mandatory nonempty entry changed',lambda:check(family,broken,s))
    broken=[row[:] for row in seed];broken[0][0]+=1
    reject('actual empty row sum changed',lambda:check(family,broken,s))
    reject('actual empty vertex removed',lambda:check(family[1:],[row[1:] for row in seed[1:]],s))
    badlabels=family[:];badlabels[-1]=badlabels[-2]
    reject('actual private labels collide',lambda:check(badlabels,seed,s))
    reject('excluded l1 domain',lambda:parameters(8,1))
    reject('too many distinct marks',lambda:build(4,2,3,mean_recipe='cap-harmonic'))
    reject('unchanged literalN80 guard',lambda:build(6,2,3,mean_recipe='cap-harmonic'))
    sectors,_=reduced(8,2,2,'cap-harmonic');G,S=sectors['fixed']
    K=[F(1),F(5,3),F(1),F(1,3),F(0),F(1),F(0),F(0)];image=matvec(G,K)
    omitted=[[S[i][j]-image[i]*image[j]/81 for j in range(8)] for i in range(8)]
    reject('empty update omitted from grouped fixed frame',lambda:require(omitted==S,'entire fixed frame required'))
    aug,tail,_,_=fixed(8,2,upper_bounds=True)
    bad=[row[:] for row in aug];bad[2][3]=-bad[2][3];bad[3][2]=-bad[3][2]
    reject('arrow congruence last cross sign reversed',lambda:require(bad==aug,'exact inverse-bound congruence required'))
    values=parameters(8,2);kappa=F(1,2)/values['nuT']+F(9,2)/values['nuL']+F(3,4)/values['C']
    excessive=7/kappa;badW=[row[:] for row in W]
    for i in range(3):badW[i][-1]+=excessive;badW[-1][i]+=excessive
    require(6*excessive-kappa*excessive**2<0,'excessive repair scalar Schur negative')
    reject('excessive disjoint-entry repair',lambda:psd_rank(badW))
    return rows


def run():
    start=time.monotonic()
    signs=[stage(sign_certificate,label) for label in ('norms','anti','pendant','triangle','augmented','final')]
    links=stage(links_certificate);arithmetic=stage(arithmetic_controls);old=stage(baseline)
    controls=[stage(fixed_control,q,l) for q,l in
              ((8,2),(9,2),(12,3),(16,3),(16,4),(32,5),(100,10),(100000,100))]
    fixtures=[stage(actual,n,l) for n,l in ((4,2),(5,2),(5,3),(6,2))]
    invalid=stage(rejections)
    norms=signs[0]['rows'];minors=[row for test in signs[1:] for row in test['rows']]
    counts={'positive_residual_and_floor_coefficients':sum(row['terms'] for row in norms),
            'uniform_leading_minors':len(minors),'positive_leading_minor_coefficients':sum(row['terms'] for row in minors),
            'full_degree_bounded_identity_points':sum(row['full_grid_points'] for row in minors),
            'symbolic_arrow_positions':links['symbolic_arrow_positions'],
            'symbolic_augmented_positions':links['symbolic_augmented_positions'],
            'rational_scalar_sign_positions':sum(row['scalar_checks'] for row in signs),
            'direct_arithmetic_controls':len(arithmetic),'fixed_frame_controls':len(controls),
            'independent_Gaussian5_inverse_controls':len(controls),
            'fixed_frame_grouping_positions':sum(row['fixed_positions'] for row in controls),
            'triangle_diagonal_update_positions':sum(row['triangle_update_positions'] for row in controls),
            'triangle_Schur_positions':sum(row['triangle_schur_positions'] for row in controls),
            'actual_original_fixtures':len(fixtures),
            'actual_positions_per_seed_or_repair':sum(row['full_original_positions_per_seed_or_repair'] for row in fixtures),
            'original_reduced_Gram_positions':sum(row['Gram_positions'] for row in fixtures),
            'original_reduced_frame_positions':sum(row['frame_positions'] for row in fixtures),
            'complete_changed_Gram_positions':sum(row['changed_Gram_positions'] for row in fixtures),
            'complete_changed_frame_positions':sum(row['changed_frame_positions'] for row in fixtures),
            'untouched_high_directions':sum(row['untouched_high'] for row in fixtures),
            'untouched_low_directions':sum(row['untouched_low'] for row in fixtures),
            'actual_maximum_star_kernel_vectors':2*len(fixtures),'semantic_damages_rejected':len(invalid)}
    data={'agent':'six-downset-1','role':'researcher',
          'domain':'every integer n>=4,2<=l<=n-2; two triangle and l pendant marks mutually distinct; all private points distinct',
          'conclusion':'explicit rational capped H, lowerN-2 greatest among all real ordinary H, upperN-1, scaled gap>=3/4',
          'proof_status':'author-checked exact uniform signs and ordinary unformalized complete-space/inverse/rank/repair proofs; independently unreviewed',
          'sign_certificates':signs,'symbolic_links':links,'arithmetic_controls':arithmetic,
          'credited_baseline':old,'fixed_original_controls':controls,'actual_fixtures':fixtures,
          'semantic_rejections':invalid,'counts':counts,
          'resource_guards':{'native_threads':1,'serial_CPU_jobs':1,'stage_seconds':60,'literal_n_max':6,
                             'literal_N_max':80,'bivariate_terms':512,'packing_bytes':32*1024*1024}}
    data=json.loads(packed(data))
    return {**data,'record_sha256':sha256(packed(data)).hexdigest()},time.monotonic()-start


def main():
    parser=argparse.ArgumentParser(description=__doc__);group=parser.add_mutually_exclusive_group()
    group.add_argument('--record',type=Path);group.add_argument('--check',type=Path);args=parser.parse_args()
    record,seconds=run()
    if args.record:args.record.write_bytes(packed(record)+b'\n')
    target=args.check
    if target is None and args.record is None:target=Path(__file__).with_name('RESULTS.json')
    if target:
        expected=json.loads(target.read_text())
        if expected.get('coefficient_storage')=='regenerated; full-record hash retained':
            got={**compact(record),'coefficient_storage':expected['coefficient_storage']}
        else:got=record
        require(expected==got,'ENTIRE mathematical record or compact/hash-bound record differs')
    print(json.dumps({'status':'PASS','record_sha256':record['record_sha256'],'entire_record_compared':bool(target),
                      'seconds':seconds,'peak_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'counts':record['counts']},sort_keys=True))


if __name__=='__main__':main()
