#!/usr/bin/env python3
"""One serial exact replay of the uniform theorem and its bounded controls.

No solver, floating-point eigensolver, external packages or private inputs.
Every mathematical requirement remains active under python -O.
"""
import os
for _variable in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                  'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[_variable]='1'

from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse, itertools, json, random, resource, signal, time
from exact import require, psd_rank, check, lift, matvec, dot, vecadd, fingerprint
from bivariate import P, R, atom, rational_value, DIM, LIMIT
from sector import reduced
from original import build, form, original
from uniform import certificate, identity, clear_rows

def alarm(signum, frame):
    raise TimeoutError('fixed mathematical stage60s guard')

def stage(function, *arguments):
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(60)
    try:
        return function(*arguments)
    finally:
        signal.alarm(0)

def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',',':')).encode()

def direct_product(a,b):
    """Independent Fraction convolution, with neither packing nor P multiplication."""
    out={}
    for i,x in a.a.items():
        for j,y in b.a.items():
            ex=(i[0]+j[0],i[1]+j[1])
            out[ex]=out.get(ex,F(0))+F(x,a.den)*F(y,b.den)
    return P.fractions(out)

def arithmetic_controls():
    rng=random.Random(610102)
    records=[]
    for trial in range(8):
        width=2 if trial<2 else 5
        a=P.fractions({ex:F(rng.choice((-7,-3,-1,1,2,5)),rng.randrange(1,6))
                       for ex in itertools.product(range(width),repeat=2)})
        b=P.fractions({ex:F(rng.choice((-5,-2,-1,1,3,7)),rng.randrange(1,6))
                       for ex in itertools.product(range(width),repeat=2)})
        product=a*b
        require(product==direct_product(a,b),'every direct/packed coefficient')
        quotient=product.exact_div(a)
        require(quotient==b and direct_product(a,quotient)==product,
                'exact quotient and separate multiplication-back identity')
        records.append({'trial':trial,'terms_a':len(a.a),'terms_b':len(b.a),
                        'packed_branch':len(a.a)*len(b.a)>256,
                        'product_fingerprint':product.fingerprint(),
                        'quotient_fingerprint':quotient.fingerprint()})
    return records

def scalar_controls():
    r=R(P({(1,0):1}));t=R(P({(0,1):1}))
    k=r+2;q=4*k-4+t
    symbolic=reduced(q,k,fraction=lambda a,b=1:R(a)/b)
    # The two exceptional points check formula identities, not quadrant signs.
    inputs=[(4,2),(4,3),(8,3),(8,4),(16,5),(32,2),
            (31,7),(100,20),(2**99,100)]
    records=[]
    for q0,k0 in inputs:
        point=(k0-2,q0-4*k0+4)
        ordinary=reduced(q0,k0)
        count=0;data={}
        for label in ('anti','fixed','standard'):
            data[label]=[]
            for matrix,expected in zip(symbolic[label],ordinary[label]):
                actual=[[rational_value(z,point) for z in row] for row in matrix]
                require(actual==expected,'ALL rational/scalar Gram/frame/cap entries')
                count+=len(matrix)**2
                data[label].append([[str(z) for z in row] for row in actual])
        residual=[[rational_value(z,point) for z in row] for row in symbolic['residual']]
        require(residual==ordinary['residual'],'ALL rational/scalar residual entries')
        parameters={name:rational_value(z,point) for name,z in symbolic['parameters'].items()}
        require(parameters==ordinary['parameters'],'ALL rational/scalar parameters')
        data['residual']=[[str(z) for z in row] for row in residual]
        data['parameters']={name:str(z) for name,z in parameters.items()}
        records.append({'q':str(q0),'k':k0,'quadrant_point':list(point),
                        'Gram_frame_cap_positions':count,
                        'residual_positions':len(residual)**2,
                        'parameter_positions':len(parameters),
                        'entire_data_sha256':sha256(packed(data)).hexdigest()})
    return records

def damages():
    rejected=[]
    def reject(label, function):
        try:
            function()
        except ValueError as error:
            rejected.append({'label':label,'reason':str(error)})
        else:
            raise ValueError('invalid semantic input accepted: '+label)
    reject('negative PSD pivot',lambda:psd_rank([[-1]]))
    reject('singular residual coupling',lambda:psd_rank([[0,1],[1,0]]))
    reject('nonsymmetric PSD input',lambda:psd_rank([[1,1],[0,1]]))
    reject('zero polynomial at quadrant boundary',
           lambda:require(P({(1,0):1}).positive(),'strict constant required'))
    reject('negative polynomial coefficient',
           lambda:require(P({(0,0):3,(1,0):-1}).positive(),'nonnegative coefficients required'))
    reject('false determinant identity',lambda:identity([[P(1)]],P(2)))
    key,unused=atom(P({(1,0):1}))
    reject('row denominator zero on quadrant boundary',
           lambda:clear_rows([[R(1,{key:1})]]))
    reject('polynomial guard unchanged',lambda:P({(j,0):1 for j in range(LIMIT+1)}))

    family,s,C,W,private,sectors,changed,parameters=build(3,2)
    prediction=reduced(parameters['q'],parameters['k'])
    wrong=sectors['standard'][:]
    # The actual full residual equals the internal full vector plus its mean.
    wrong[-1]=vecadd(wrong[-1],wrong[-2])
    reject('group mean omitted from internal full extraction',
           lambda:require(form(C,wrong)==prediction['standard'][:2],
                          'literal standard Gram/frame must match'))
    images=[matvec(C,v) for v in sectors['fixed']]
    omitted=[[dot(u,v) for v in images] for u in images]
    reject('actual empty frame contribution omitted',
           lambda:require(omitted==prediction['fixed'][1],'complete actual frame required'))
    seed=lift(C,s);N=len(family);k=parameters['k']
    bad=[row[:] for row in seed];bad[1][1]=F(1)
    def support():
        for i,A in enumerate(family):
            for j,B in enumerate(family):
                if A&B:require(bad[i][j]==0,'mandatory intersecting entry')
    reject('nonempty support corrupted',support)
    badrow=[row[:] for row in seed];badrow[0][0]+=1
    reject('actual empty row regularity corrupted',lambda:check(family,badrow,s))
    reject('actual empty member removed',
           lambda:check(family[1:],[row[1:] for row in seed[1:]],s))
    collision=family[:];collision[-1]=collision[-2]
    reject('private labels collide',lambda:check(collision,seed,s))
    reject('unrepaired seed falsely called greatest rank',
           lambda:require(check(family,seed,s)['lower_rank']==N-k,'greatest lower rank required'))
    p=prediction['parameters']
    nu=k*p['mean_norm']/(k-1);kappa=2/nu+4/p['full_norm']
    excessive=F(7)/kappa
    badW=[row[:] for row in W]
    for j in range(3):
        badW[j][-1]+=excessive;badW[-1][j]+=excessive
    require(6*excessive-kappa*excessive**2<0,'damaged repair has negative exact Schur')
    reject('excessive free-entry repair',lambda:psd_rank(badW))
    reject('excluded n2 candidate imported',lambda:build(2,2))
    reject('more distinct marks than old points',lambda:build(3,4))
    return rejected

def run():
    start=time.monotonic()
    uniform=stage(certificate)
    uniform.pop('seconds');uniform.pop('peak_kib')
    arithmetic=stage(arithmetic_controls)
    scalars=stage(scalar_controls)
    fixtures=[stage(original,n,k) for n,k in
              ((3,2),(3,3),(4,3),(4,4),(5,5),(6,2))]
    invalid=stage(damages)
    minors=[minor for record in uniform['records'] for minor in record['minors']]
    counts={'uniform_leading_minors':len(minors),
            'uniform_leading_minor_coefficients':sum(row['terms'] for row in minors),
            'positive_residual_numerator_coefficients':sum(row['terms'] for row in uniform['direct_positive_residual_numerator_factors']),
            'independent_degree_bounded_determinant_grid_points':sum(row['full_grid_identity_points'] for row in minors),
            'standard_rank_two_identity_positions':uniform['standard4_two_update_identity_positions'],
            'direct_convolution_exact_quotient_controls':len(arithmetic),
            'scalar_controls':len(scalars),
            'scalar_Gram_frame_cap_positions':sum(row['Gram_frame_cap_positions'] for row in scalars),
            'original_fixtures':len(fixtures),
            'original_actual_positions_per_seed_or_repair':sum(row['full_original_positions'] for row in fixtures),
            'original_reduced_Gram_positions':sum(row['reduced_Gram_positions'] for row in fixtures),
            'original_reduced_frame_positions':sum(row['reduced_frame_positions'] for row in fixtures),
            'original_changed_Gram_positions':sum(row['changed_Gram_positions'] for row in fixtures),
            'original_changed_frame_positions':sum(row['changed_frame_positions'] for row in fixtures),
            'untouched_high_directions':sum(row['untouched_high_count'] for row in fixtures),
            'untouched_low_directions':sum(row['untouched_low_count'] for row in fixtures),
            'semantic_damages_rejected':len(invalid)}
    mathematical={'agent':'six-downset-1','role':'researcher',
                  'theorem_domain':'every integer n>=3 and2<=k<=n; all distinct old marks and2k distinct private points',
                  'conclusion':'rational capped H, greatest all-real ordinary lower rankN-k, upperrankN-1, scaled gap>=3/4',
                  'status':'author-checked exact certificate plus ordinary unformalized complete-space proof; independently unreviewed',
                  'uniform':uniform,'arithmetic_controls':arithmetic,'scalar_controls':scalars,
                  'original_fixtures':fixtures,'semantic_rejections':invalid,'counts':counts,
                  'resource_guards':{'native_threads':1,'serial_CPU_jobs':1,'stage_seconds':60,
                                     'literal_n_max':6,'literal_N_max':80,
                                     'bivariate_term_limit':512,'packing_bytes':32*1024*1024}}
    # Canonical JSON types are also the in-memory comparison types.
    # Nested factor exponents are tuples internally but lists in JSON.
    mathematical=json.loads(packed(mathematical))
    digest=sha256(packed(mathematical)).hexdigest()
    return {**mathematical,'record_sha256':digest},time.monotonic()-start

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--record',type=Path)
    group.add_argument('--check',type=Path)
    arguments=parser.parse_args()
    mathematical,seconds=run()
    if arguments.record:
        arguments.record.write_bytes(packed(mathematical)+b'\n')
    if arguments.check:
        require(json.loads(arguments.check.read_text())==mathematical,'entire frozen mathematical record differs')
    print(json.dumps({'status':'PASS','record_sha256':mathematical['record_sha256'],
                      'entire_frozen_record_compared':bool(arguments.check),
                      'seconds':seconds,'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      'counts':mathematical['counts']},sort_keys=True))

if __name__=='__main__':
    main()
