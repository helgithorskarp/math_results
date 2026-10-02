"""Exact bivariate quadrant certificates with unchanged512-term guard.

No resource escalation. Any failure concerns this computation/candidate,
not mathematical H nonexistence. The complete full-space bridge is proved separately in PROOF.md.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json, signal, time, resource, itertools, random
from math import gcd,lcm
from bivariate import P,R,atom,ATOMS,PROBES,DEN_CACHE,denominator,value,DIM
from sector import reduced

def require(condition,message):
    if not condition:raise ValueError(message)

def alarm(signum,frame):
    raise TimeoutError('bivariate stage60s guard')

def clear_rows(matrix):
    out=[];domains=[];removals=[];constants=[]
    for row in matrix:
        powers={}
        for z in row:
            for a,e in z.den.items():powers[a]=max(powers.get(a,0),e)
        require(all(ATOMS[a].positive() for a in powers),'strictly positive clearing factors on quadrant')
        cleared=[z.num*denominator({a:e-z.den.get(a,0) for a,e in powers.items() if e>z.den.get(a,0)}) for z in row]
        require(any(bool(z) for z in cleared),'nonzero cleared row')
        removed={}
        # Exact division by known strictly positive common row factors
        # reduces intermediate expansion without changing the512-term guard.
        for a in tuple(ATOMS):
            if not ATOMS[a].positive():continue
            while True:
                quotients=[z.exact_div(ATOMS[a]) for z in cleared]
                if any(z is None for z in quotients):break
                cleared=quotients;removed[a]=removed.get(a,0)+1
        common_den=1
        for z in cleared:common_den=lcm(common_den,z.den)
        content=0
        for z in cleared:
            for value0 in z.a.values():content=gcd(content,abs(value0*(common_den//z.den)))
        require(content>0,'positive primitive row content')
        cleared=[P({ex:value0*(common_den//z.den)//content for ex,value0 in z.a.items()}) for z in cleared]
        out.append(cleared);removals.append(removed);constants.append(str(F(common_den,content)))
        domains.append(powers)
    return out,domains,removals,constants

def bareiss_minors(matrix):
    a=[row[:] for row in matrix];prior=P(1);out=[]
    for k in range(len(a)):
        pivot=a[k][k];require(bool(pivot),'nonzero symbolic leading minor')
        out.append(pivot)
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                top=pivot*a[i][j]-a[i][k]*a[k][j]
                answer=top.exact_div(prior)
                require(answer is not None,'exact multivariate Bareiss division')
                a[i][j]=answer
        prior=pivot
    return out

def scalar_determinant(matrix):
    a=[[F(x) for x in row] for row in matrix];out=F(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return F(0)
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];out=-out
        out*=a[k][k]
        for i in range(k+1,len(a)):
            factor=a[i][k]/a[k][k]
            for j in range(k+1,len(a)):a[i][j]-=factor*a[k][j]
    return out

def identity(matrix,minor):
    bounds=[sum(max((max((ex[d] for ex in p.a),default=0) for p in row),default=0) for row in matrix) for d in range(DIM)]
    require(all(max((ex[d] for ex in minor.a),default=0)<=bounds[d] for d in range(DIM)),'separate determinant degree bounds')
    count=0
    for point in itertools.product(*(range(d+1) for d in bounds)):
        require(scalar_determinant([[value(z,point) for z in row] for row in matrix])==value(minor,point),'independent full-grid polynomial identity')
        count+=1
    return bounds,count

def certificate():
    ATOMS.clear();PROBES.clear();DEN_CACHE.clear()
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60)
    start=time.monotonic()
    r=R(P({(1,0):1}));t=R(P({(0,1):1}));k=r+2;q=4*k-4+t
    for z in [k-1,k,q,q+3,3*k+1,q-k]:atom(z.num)
    models=reduced(q,k,fraction=lambda a,b=1:R(a)/b)
    residual_factors=[]
    # These numerators have their own direct positive-coefficient proof.
    # Dividing the corresponding common positive row factor removes
    # artificial determinant degree before fraction-free elimination.
    for name in ['mean_norm','anti_norm','full_norm']:
        expression=models['parameters'][name]
        require(expression.num.positive() and all(ATOMS[a].positive() for a in expression.den),'strict residual rational norm on whole quadrant')
        key,unit=atom(expression.num)
        require(unit>0 and ATOMS[key].positive(),'positive normalized residual factor')
        residual_factors.append({'name':name,'terms':len(expression.num.a),
                                'positive_constant':str(value(expression.num,(0,0))),
                                'fingerprint':expression.num.fingerprint(),
                                'polynomial':[[list(ex),str(z)] for ex,z in sorted(expression.num.a.items())],
                                'coefficient_denominator':expression.num.den})
    # The standard4-space has positive diagonal base minus only TWO
    # private update columns. Its rational2x2 Schur complement is an
    # equivalent PD test, avoiding the blocked4x4 polynomial expansion.
    p=models['parameters'];s=p['s'];N=p['N']
    nu=k*p['mean_norm']/(k-1);full=p['full_norm']
    positive_diagonal=[6*q*(q+6*k-7),12*s*(q+6*k-4),2*nu*(N-1),2*full*(N-1)]
    leaf=[p['a']*k*q/(k-1),p['c']*s,nu,-full/2]
    whole=[p['d']*k*q/(k-1),2*p['c']*s/(k-1),nu,full]
    expected=[[((positive_diagonal[i] if i==j else R(0))-4*leaf[i]*leaf[j]-2*whole[i]*whole[j]) for j in range(4)] for i in range(4)]
    require(expected==models['standard'][2],'every standard4 diagonal/two-update identity')
    columns=[leaf,whole]
    Schur=[[R(F(1,4) if i==0 else F(1,2))*(i==j)-sum(columns[i][a]*columns[j][a]/positive_diagonal[a] for a in range(4)) for j in range(2)] for i in range(2)]
    rows=[]
    matrices=[('residual',models['residual'])]+[('cap-'+label,models[label][2]) for label in ['anti','fixed']]+[('cap-standard-Schur',Schur)]
    for label,M in matrices:
        signal.alarm(60)
        require(all(M[i][j]==M[j][i] for i in range(len(M)) for j in range(len(M))), 'sector symmetry')
        A,domains,removals,constants=clear_rows(M)
        minors=bareiss_minors(A);data=[]
        for j,minor in enumerate(minors,1):
            require(minor.positive(),'positive quadrant coefficients '+label+'/'+str(j))
            bounds,points=identity([row[:j] for row in A[:j]],minor)
            data.append({'order':j,'total_degree':minor.degree(),'terms':len(minor.a),
                         'strictly_positive_stored_coefficients':all(z>0 for z in minor.a.values()),
                         'constant':str(value(minor,(0,0))),'fingerprint':minor.fingerprint(),
                         'separate_degree_bounds':bounds,'full_grid_identity_points':points,
                         'polynomial':[[list(ex),str(z)] for ex,z in sorted(minor.a.items())],
                         'coefficient_denominator':minor.den})
        record={'label':label,'dimension':len(M),'minors':data,
                'positive_row_factors':[[{'factor':list(map(list,a)),'power':e} for a,e in sorted(d.items())] for d in domains],
                'removed_positive_row_factors':[[{'factor':list(map(list,a)),'power':e} for a,e in sorted(d.items())] for d in removals],
                'positive_primitive_row_multipliers':constants}
        rows.append(record)
    mathematical={'agent':'six-downset-1','role':'researcher','domain':'k=2+r,q=4k-4+t,r>=0,t>=0',
                  'records':rows,'direct_positive_residual_numerator_factors':residual_factors,
                  'standard4_two_update_identity_positions':16,
                  'standard4_equivalent_Schur_dimension':2,
                  'standard_positive_base':['6q(q+6k-7)','12(q+3)(q+6k-4)','2nu(N-1)','2full(N-1)'],
                  'term_guard':512,'packing_guard_bytes':32*1024*1024,
                  'status':'exact uniform reduced signs; original-space implication proved separately in PROOF.md'}
    packed=json.dumps(mathematical,sort_keys=True,separators=(',',':')).encode()
    out={**mathematical,'record_sha256':sha256(packed).hexdigest(),'seconds':time.monotonic()-start,
         'peak_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    signal.alarm(0)
    return out
