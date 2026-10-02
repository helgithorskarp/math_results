"""Independent certificate/physical-sector audit of lemma9147.

Author seed/dual rational data are credited INPUT files. No author program is
imported. Center-first completion, explicit quotient metrics, reconstructed LDL
congruences and literal original-mask actions are independent implementations.
"""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import re
import sys


def need(x, why):
    if not x:
        raise ValueError(why)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def rational(x):
    need(type(x) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', x), 'exact rational string')
    return F(x)


def zero(n, m=None):
    return [[F() for _ in range(n if m is None else m)] for _ in range(n)]


def transpose(a):
    return [list(v) for v in zip(*a)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum((x*y for x,y in zip(row,col)), F()) for col in bt] for row in a]


def symmetric(a):
    need(all(len(row) == len(a) for row in a), 'square matrix')
    need(a == transpose(a), 'physical matrix symmetry')


def matrix_hash(a):
    return hashlib.sha256(json.dumps([[str(x) for x in row] for row in a],
                         separators=(',',':')).encode()).hexdigest()


def ldl(a):
    """PSD congruence with symmetric pivoting; independently reconstruct P A P^T."""
    symmetric(a)
    n = len(a); work = [row[:] for row in a]; perm = list(range(n))
    lower = zero(n)
    for i in range(n):
        lower[i][i] = F(1)
    diagonal = []; rank = 0
    for k in range(n):
        need(all(work[i][i] >= 0 for i in range(k,n)), 'negative quadratic direction')
        pivot = next((i for i in range(k,n) if work[i][i] > 0), None)
        if pivot is None:
            need(all(work[i][j] == 0 for i in range(k,n) for j in range(k,n)), 'nonzero zero-diagonal residual')
            break
        if pivot != k:
            work[k], work[pivot] = work[pivot], work[k]
            for row in work:
                row[k], row[pivot] = row[pivot], row[k]
            perm[k], perm[pivot] = perm[pivot], perm[k]
            for j in range(k):
                lower[k][j], lower[pivot][j] = lower[pivot][j], lower[k][j]
        d = work[k][k]; diagonal.append(d); rank += 1
        for i in range(k+1,n):
            lower[i][k] = work[i][k]/d
        for i in range(k+1,n):
            for j in range(i,n):
                value = work[i][j] - lower[i][k]*d*lower[j][k]
                work[i][j] = work[j][i] = value
    for i in range(n):
        for j in range(n):
            actual = sum((lower[i][k]*diagonal[k]*lower[j][k] for k in range(rank)),F())
            need(actual == a[perm[i]][perm[j]], 'whole LDL congruence reconstruction')
    return {'rank':rank,'nullity':n-rank,'matrix_sha256':matrix_hash(a),
            'pivot_product':str(product_value(diagonal))}


def product_value(xs):
    result = F(1)
    for x in xs:
        result *= x
    return result


def rref(a):
    rows = [row[:] for row in a]; pivots = []; rank = 0
    for col in range(len(rows[0])):
        at = next((i for i in range(rank,len(rows)) if rows[i][col]),None)
        if at is None:
            continue
        rows[rank], rows[at] = rows[at], rows[rank]
        scale = rows[rank][col]; rows[rank] = [x/scale for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                scale = rows[i][col]
                rows[i] = [x-scale*y for x,y in zip(rows[i],rows[rank])]
        pivots.append(col); rank += 1
        if rank == len(rows):
            break
    return rows, pivots


def counts(n):
    N = (1 << n)-n-1; s = (1 << (n-1))-n
    return N,s,N-s


def free_pairs(n):
    return [(a,b) for a in range(3,n-1) for b in range(a,n-1) if a+b<=n]


def completion(n, free):
    """Center-first two-equation solve, with the last row fixed by centering."""
    need(type(n) is int and n>=5, 'near-cube order parameter')
    allowed = free_pairs(n)
    need(all(p in allowed and type(x) in (int,F) for p,x in free.items()), 'free exact coordinate domain')
    N,s,h = counts(n); R = N-1-s; beta = zero(n-1)
    for (a,b),value in free.items():
        beta[a][b] = beta[b][a] = F(value)
    for a in list(range(3,n-1))+[2]:
        q = n-a
        row = R-sum((beta[a][b]*choose(q,b) for b in range(3,n-1)),F())
        moment = q*s-sum((b*beta[a][b]*choose(q,b) for b in range(3,n-1)),F())
        beta[a][2] = (moment-row)/choose(q,2)
        beta[a][1] = (2*row-moment)/q
        beta[2][a] = beta[a][2]; beta[1][a] = beta[a][1]
    beta[1][1] = (R-sum((beta[1][b]*choose(n-1,b) for b in range(2,n-1)),F()))/(n-1)
    need(beta == transpose(beta), 'entire symmetric affine completion')
    for a in range(1,n-1):
        need(sum((beta[a][b]*choose(n-a,b) for b in range(1,n-1)),F()) == R, 'all centering equations')
        need(sum((b*beta[a][b]*choose(n-a,b) for b in range(1,n-1)),F()) == (n-a)*s, 'all first-moment equations')
    for pair in allowed:
        need(beta[pair[0]][pair[1]] == free.get(pair,F()), 'all free coordinates retained')
    return beta


def affine_audit():
    n=17; allpairs=[(a,b) for a in range(1,16) for b in range(a,16) if a+b<=n]
    equations=[]
    for a in range(1,16):
        for moment in [False,True]:
            row=[]
            for i,j in allpairs:
                b=j if a==i else i if a==j else None
                row.append(F(0 if b is None else choose(n-a,b)*(b if moment else 1)))
            equations.append(row)
    _,pivots=rref(equations)
    need(len(allpairs)==71 and len(pivots)==29 and len(free_pairs(n))==42,'whole real affine dimension')
    completion(n,{})
    for pair in free_pairs(n):
        completion(n,{pair:F(1)})
    return {'supported_coordinates':71,'equation_rows':30,'rank':29,'free_dimension':42,
            'whole_affine_basis_checks':43,'determined_by':'Centering and first moments; final beta11 fixed by centering, not the author star-row decoder.'}


def physical_blocks(n,beta):
    N,s,h=counts(n); out=[]
    for j in range(n//2+1):
        layers=list(range(max(j,1),min(n-j,n-2)+1))
        metric=[F(choose(n-2*j,a-j)) for a in layers]
        lower=zero(len(layers));upper=zero(len(layers))
        for i,a in enumerate(layers):
            for k,b in enumerate(layers):
                count=(-1)**j*choose(n-a-j,b-j)
                K=s*int(a==b)-(choose(n,b) if j==0 else 0)+beta[a][b]*count
                U=N*int(a==b)-(choose(n,b) if j==0 else 0)-K
                lower[i][k]=metric[i]*K;upper[i][k]=metric[i]*U
        symmetric(lower);symmetric(upper)
        out.append({'j':j,'layers':layers,'metric':metric,'lower':lower,'upper':upper,
                    'multiplicity':choose(n,j)-choose(n,j-1)})
    need(sum(len(z['layers'])*z['multiplicity'] for z in out)==N-1,'complete harmonic dimension')
    return out


def quotient(a,g,kernels):
    """A kills each kernel; choose full G-orthogonal coordinate complement."""
    n=len(a)
    for v in kernels:
        need(all(sum((x*y for x,y in zip(row,v)),F())==0 for row in a),'literal prescribed kernel')
    if kernels:
        equations=[[v[i]*g[i] for i in range(n)] for v in kernels]
        rr,pivots=rref(equations)
        need(len(pivots)==len(kernels),'independent prescribed kernels')
        columns=[]
        for f in range(n):
            if f in pivots:
                continue
            v=[F() for _ in range(n)];v[f]=F(1)
            for i,p in enumerate(pivots):
                v[p]=-rr[i][f]
            columns.append(v)
        W=transpose(columns)
        need(all(sum((row[i]*column[i] for i in range(n)),F())==0
                 for row in equations for column in columns),'entire orthogonal quotient basis')
    else:
        W=[[F(int(i==k)) for k in range(n)] for i in range(n)]
    G=[[g[i]*int(i==k) for k in range(n)] for i in range(n)]
    return multiply(transpose(W),multiply(a,W)),multiply(transpose(W),multiply(G,W))


def floor_matrix(a,g,delta):
    return [[a[i][k]-delta*g[i][k] for k in range(len(a))] for i in range(len(a))]


def dual_check(data):
    n=17;N,s,h=counts(n);pairs=free_pairs(n)
    permitted=[p for p in pairs if min(p)<=3 or sum(p)==n]
    need(type(data['n']) is int and data['n']==n and data['degrees']==[0]
         and data['matrix_roles']==[[0,'lower'],[0,'upper']],'two-sided degree-zero dual scope')
    need(data['allowed_free_pairs']==[list(p) for p in permitted],'all17 permitted real coordinates')
    Y=[[[rational(x) for x in row] for row in a] for a in data['Y']]
    need(len(Y)==2 and all(len(a)==15 for a in Y),'two15x15 duals')
    eps=F(1,200000000)
    need(rational(data['positive_definite_floor'])==eps,'dual exact floor')
    identity=[[F(int(i==k)) for k in range(15)] for i in range(15)]
    dual_psd=[]
    for a in Y:
        need(ldl(a)['rank']==15,'strict positive dual')
        z=ldl(floor_matrix(a,identity,eps));need(z['rank']==15,'strict positive dual floor');dual_psd.append(z)
    need(sum(Y[k][i][i] for k in range(2) for i in range(15))==1,'combined dual trace1')
    scales=[isqrt(choose(n,a)) for a in range(1,16)]
    need(data['scales']==[scales,scales],'actual physical dual scales')
    def phi(free):
        z=physical_blocks(n,completion(n,free))[0]
        return sum((Y[r][i][k]*z[key][i][k]/(s*scales[i]*scales[k])
                   for r,key in enumerate(['lower','upper']) for i in range(15) for k in range(15)),F())
    base={p:F(s) for p in pairs if sum(p)==n};constant=phi(base)
    need(constant==rational(data['dual_constant']) and constant < -F(1,10000),'negative whole-affine constant')
    coefficients={}
    for p in pairs:
        moved=dict(base);moved[p]=moved.get(p,F())+1;coefficient=phi(moved)-constant
        if p in permitted:
            need(coefficient==0,'all17 exact real free-coordinate cancellations')
        else:
            coefficients[p]=coefficient
    need(len(coefficients)==25 and sum(abs(c) for c in coefficients.values())>0,'whole unrestricted layer>=4 coefficient inventory')
    infinity=(-constant)/(h*sum(abs(c) for c in coefficients.values()))
    orbit_counts={p:choose(n,p[0])*choose(n-p[0],p[1])//(2 if p[0]==p[1] else 1) for p in coefficients}
    weighted_max=max(abs(c)/orbit_counts[p] for p,c in coefficients.items())
    l1=(-constant)/(h*weighted_max)
    need(infinity>F(1,1<<27) and l1>F(1,3),'simple strict original-coordinate coupling bounds')
    return {'dual_PSD_floors':dual_psd,'constant':str(constant),'cancelled_real_coordinates':17,
            'all_outside_coefficients':[{'pair':list(p),'coefficient':str(c),'unordered_orbit_size':orbit_counts[p]} for p,c in coefficients.items()],
            'original_M_entry_infinity_lower_bound':str(infinity),'original_M_unordered_L1_lower_bound':str(l1),
            'simple_strict_entry_bound':'1/134217728','simple_strict_unordered_L1_bound':'1/3',
            'meaning':'Every real centered capped H has some proper-disjoint min-size>=4 |M_AB| at least the infinity bound; total absolute unordered entries in those orbits is at least L1. Symmetry is unnecessary by averaging.'}


def seed_check(data):
    n=17;N,s,h=counts(n);pairs=free_pairs(n)
    need(all(type(data[k]) is int for k in ['n','r','N','s'])
         and data['n']==n and data['r']==15 and data['N']==N and data['s']==s,'seed domain')
    need(rational(data['seed_projected_lower_floor'])==F(1,2)
         and rational(data['seed_upper_floor'])==F(1,4)
         and rational(data['repair_upper_floor'])==F(1,8),'original seed/repair floor scope')
    need(data['free_pairs']==[list(p) for p in pairs] and len(data['free_values'])==42,'whole seed coordinates')
    free={p:rational(v) for p,v in zip(pairs,data['free_values'])}
    need(all(free[p]==0 for p in pairs if min(p)>=5 and sum(p)<n),'exact S4 seed support')
    active=[p for p in pairs if free[p] and sum(p)<n]
    need(len(active)==20 and free[(4,4)]==F(56609,1000000),'exact active layer4')
    beta=completion(n,free);star_tau={(1,1):F(210),(1,2):F(-14),(2,2):F(1)}
    endpoint=F(1,27720);need(rational(data['repair_endpoint'])==endpoint,'original real repair endpoint')
    repaired=[row[:] for row in beta]
    for (a,b),v in star_tau.items():
        repaired[a][b]+=endpoint*v
        if a!=b:
            repaired[b][a]+=endpoint*v
    output=[]
    extra_floor=F(1,1<<20)
    for label,matrix,upper_floor in [('seed',beta,F(1,4)),('endpoint',repaired,F(1,8))]:
        blocks=physical_blocks(n,matrix);nullity=0;items=[]
        for z in blocks:
            j=z['j'];layers=z['layers'];g=z['metric'];d=len(layers)
            kernels=([[F(1)]*d,[F(a) for a in layers]] if label=='seed' else [[F(a) for a in layers]]) if j==0 else [[F(1)]*d] if j==1 else []
            B,G=quotient(z['lower'],g,kernels)
            lo=ldl(z['lower']);q=ldl(B)
            need(lo['rank']==d-len(kernels) and q['rank']==len(B),'complete lower kernel/rank')
            delta=F(1,2) if label=='seed' else extra_floor
            floor=ldl(floor_matrix(B,G,delta))
            metric=[[g[i]*int(i==k) for k in range(d)] for i in range(d)]
            up=ldl(floor_matrix(z['upper'],metric,upper_floor))
            need(up['rank']==d,'whole strict upper floor')
            nullity+=len(kernels)*z['multiplicity']
            items.append({'j':j,'layers':layers,'multiplicity':z['multiplicity'],'lower':lo,
                          'quotient_lower_floor':str(delta),'quotient_floor':floor,'upper_floor':str(upper_floor),'upper_floor_certificate':up})
        need(nullity==(18 if label=='seed' else 17),'all-sector weighted core nullity')
        output.append({'parameter':label,'full_lower_rank':N-nullity,'full_upper_rank':N-1,'core_nullity':nullity,'blocks':items})
    increments={a:sum((star_tau.get((min(a,b),max(a,b)),F())*choose(n-a,b) for b in range(1,16)),F()) for a in range(1,16)}
    need(increments=={a:F(1680 if a==1 else -105 if a==2 else 0) for a in range(1,16)},'all repaired actual row increments')
    for a in range(1,16):
        need(sum((star_tau.get((min(a,b),max(a,b)),F())*choose(n-a-1,b-1) for b in range(1,16)),F())==0,'whole exact trade-star actions')
    empty=sum((choose(n,a)*increments[a] for a in range(1,16)),F());need(empty==14280,'actual empty diagonal increment')
    return {'active_noncomplement_middle_orbits':[list(p) for p in active],'least_attained_layer':4,
            'seed_and_endpoint':output,'real_interval':['0','1/27720'],
            'new_full_lower_gap':'27720*t/1048576 on the complement of the17 forced-star kernel directions, for every real0<t<=1/27720.',
            'new_full_upper_gap':'1/4-3465*t on1_N perp, for every real0<=t<=1/27720.',
            'actual_empty_increment':str(empty),'actual_empty_loop':'(1+14280*t-s)/h',
            'actual_empty_nonempty_entries':['1-1680*t atsingletons','1+105*t attwo-sets','1 otherwise'],
            'centering':'Seed iscentered; every positive t isNOT centered.'}


def harmonic_value(mask,j):
    result=1
    for k in range(j):
        result*=((mask>>(2*k))&1)-((mask>>(2*k+1))&1)
    return result


def validate_original(n,masks,L):
    N,s,h=counts(n)
    symmetric(L)
    need(all(L[i][k]==s*int(i==k) for i,A in enumerate(masks) for k,B in enumerate(masks) if A&B),
         'entire original intersecting support')
    need(all(sum(row)==N for row in L),'entire original full rows')
    for point in range(n):
        columns=[k for k,B in enumerate(masks) if B>>point&1]
        need(all(sum((row[k] for k in columns),F())==s for row in L),
             'entire original stars includingempty')


def original_control(n):
    N,s,h=counts(n);pairs=free_pairs(n)
    free={p:F(s-3) if sum(p)==n else F((p[0]+p[1])%5-2,7) for p in pairs}
    need(any(v and sum(p)<n and min(p)>=3 for p,v in free.items()),'noncomplement three-set control')
    beta=completion(n,free);masks=[a for a in range(1<<n) if a.bit_count()<=n-2]
    need(len(masks)==N and N<=247,'bounded original domain')
    nonempty=masks[1:];sizes=[a.bit_count() for a in nonempty];m=N-1
    C=[[F(s*int(i==k)-1)+(beta[a.bit_count()][b.bit_count()] if not a&b else F()) for k,b in enumerate(nonempty)] for i,a in enumerate(nonempty)]
    need(all(sum(row)==0 for row in C),'original centered rows')
    stars=[[int(a>>i&1) for a in nonempty] for i in range(n)]
    for row in C:
        for v in stars:
            need(sum((c*x for c,x in zip(row,v)),F())==0,'all original star actions')
    need(F(1-s,h)<0,'actual original empty loop retained')
    need(all(C[i][k]==s*int(i==k)-1 for i,a in enumerate(nonempty) for k,b in enumerate(nonempty) if a&b),'all intersecting original M entries zero')
    blocks=physical_blocks(n,beta);actions=0;bilinears=0
    for z in blocks:
        j=z['j'];layers=z['layers'];metric=z['metric']
        vectors={b:[harmonic_value(A,j)*int(a==b) for A,a in zip(nonempty,sizes)] for b in layers}
        for b,v in vectors.items():
            support=[k for k,x in enumerate(v) if x];sumv=sum(v)
            act=[sum((C[i][k]*v[k] for k in support),F()) for i in range(m)]
            upper=[N*v[i]-sumv-act[i] for i in range(m)]
            for i,(A,a) in enumerate(zip(nonempty,sizes)):
                if a in layers:
                    p=layers.index(a);q=layers.index(b)
                    need(act[i]==z['lower'][p][q]/metric[p]*harmonic_value(A,j),'literal full lower harmonic action')
                    need(upper[i]==z['upper'][p][q]/metric[p]*harmonic_value(A,j),'literal full upper harmonic action')
                else:
                    need(act[i]==upper[i]==0,'literal outside harmonic support')
                actions+=2
            for a,w in vectors.items():
                p=layers.index(a);q=layers.index(b)
                need(sum(x*x for x in w)==2**j*metric[p],'literal all physical Gram normalizations')
                need(sum((x*y for x,y in zip(w,act)),F())==2**j*z['lower'][p][q],'literal all physical lower entries')
                need(sum((x*y for x,y in zip(w,upper)),F())==2**j*z['upper'][p][q],'literal all physical upper entries')
                bilinears+=2
    # Same original indices with a positive trade parameter; controls assert
    # support/row/star/empty identities only, not PSD feasibility.
    t=F(1,997);tau={(1,1):F((n-2)*(n-3)),(1,2):F(-(n-3)),(2,2):F(1)}
    R=[[C[i][k]+t*tau.get((min(a.bit_count(),b.bit_count()),max(a.bit_count(),b.bit_count())),F())*int(not a&b) for k,b in enumerate(nonempty)] for i,a in enumerate(nonempty)]
    rows=[sum(row) for row in R];empty=1+sum(rows)
    L=[[F(0) for _ in masks] for _ in masks];L[0][0]=empty
    for i in range(m):
        L[0][i+1]=L[i+1][0]=1-rows[i]
        for k in range(m):
            L[i+1][k+1]=1+R[i][k]
    validate_original(n,masks,L)
    need(empty!=1 and any(x!=1 for x in L[0][1:]),'repaired genuine noncentering')
    rejected=[]
    for label in ['changed actual empty loop','row-preserving intersecting diagonal','row/support-preserving broken star']:
        damaged=[row[:] for row in L]
        if label=='changed actual empty loop':
            damaged[0][0]+=1
        elif label=='row-preserving intersecting diagonal':
            damaged[1][1]+=1;damaged[1][0]-=1;damaged[0][1]-=1;damaged[0][0]+=1
        else:
            i=masks.index(1);k=masks.index(2)
            damaged[i][k]+=1;damaged[k][i]+=1
            damaged[i][0]-=1;damaged[0][i]-=1;damaged[k][0]-=1;damaged[0][k]-=1
            damaged[0][0]+=2
        try:
            validate_original(n,masks,damaged)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('original semantic damage accepted')
    return {'n':n,'N':N,'all_harmonic_degrees':[z['j'] for z in blocks],'literal_action_entries':actions,
            'literal_physical_bilinear_entries':bilinears,'full_star_and_row_checks':True,
            'centered_empty_loop':str(F(1-s,h)),'repaired_empty_loop':str((empty-s)/h),
            'full_repaired_matrix_sha256':matrix_hash(L),'PSD_witness':False,
            'rejected_original_damages':rejected}


def arithmetic_controls():
    count=0;failed=0
    for values in product(range(-1,2),repeat=6):
        a,b,c,d,e,f=values;A=[[F(a),F(b),F(c)],[F(b),F(d),F(e)],[F(c),F(e),F(f)]]
        determinant=a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b
        expected=(a>=0 and d>=0 and f>=0 and a*d>=b*b and a*f>=c*c and d*f>=e*e and determinant>=0)
        try:
            ldl(A);actual=True
        except ValueError:
            actual=False;failed+=1
        need(actual==expected,'complete ternary3x3 versus principal minors');count+=1
    return {'whole_ternary3x3_cases':count,'PSD_rejections':failed}


def record():
    folder=Path(__file__).parent
    seed=json.loads((folder/'INPUT-seed.json').read_text());dual=json.loads((folder/'INPUT-dual.json').read_text())
    value={'agent':'six-reviewer-2','role':'independent mathematical reviewer',
            'target':'9147 / bafkreidz633ymu7x25p25vtmk7bmoakjatwaxjjxpbj23sikx64ddo2x2a',
            'affine':affine_audit(),'dual':dual_check(dual),'positive':seed_check(seed),
            'original_controls':[original_control(n) for n in [7,8]],'arithmetic':arithmetic_controls(),
            'trust':'Credited original rational certificates, independent exact checker and ordinary real-affine/harmonic/lift/convexity bridge; no author executable imports or131054-square allocation.'}
    value['rejected_input_damages']=input_damages(seed,dual)
    value['rejected_record_damages']=record_damages(value)
    return value


def exact_record(a,b):
    need(type(a) is type(b),'exact record types')
    if type(a) is dict:
        need(a.keys()==b.keys(),'exact record fields')
        for k in a:
            exact_record(a[k],b[k])
    elif type(a) is list:
        need(len(a)==len(b),'exact record list coverage')
        for x,y in zip(a,b):
            exact_record(x,y)
    else:
        need(a==b,'exact record values')


def record_damages(value):
    labels=['missing outside coefficient','wrong endpoint nullity','float LDL rank']
    for label in labels:
        damaged=json.loads(json.dumps(value))
        if label=='missing outside coefficient':
            damaged['dual']['all_outside_coefficients'].pop()
        elif label=='wrong endpoint nullity':
            damaged['positive']['seed_and_endpoint'][1]['core_nullity']=18
        else:
            damaged['positive']['seed_and_endpoint'][0]['blocks'][0]['lower']['rank']=13.0
        try:
            exact_record(value,damaged)
        except ValueError:
            continue
        raise ValueError('record damage accepted')
    return labels


def input_damages(seed,dual):
    actions=[('negative pivot',lambda:ldl([[F(-1)]])),
             ('zero-diagonal offdiagonal residual',lambda:ldl([[F(0),F(1)],[F(1),F(0)]])),
             ('asymmetric physical form',lambda:ldl([[F(1),F(0)],[F(1),F(1)]])),
             ('unsupported free coordinate',lambda:completion(17,{(4,14):F(1)})),
             ('float rational input',lambda:rational(0.5))]
    for label in ['omitted seed coordinate','forbidden size-five seed coupling','changed seed floor',
                  'changed dual metric','changed dual matrix','omitted real free coordinate','changed dual constant']:
        obj=json.loads(json.dumps(seed if 'seed' in label else dual))
        if label=='omitted seed coordinate':
            obj['free_values'].pop()
        elif label=='forbidden size-five seed coupling':
            obj['free_values'][obj['free_pairs'].index([5,5])]='1/1000000'
        elif label=='changed seed floor':
            obj['seed_projected_lower_floor']='1/3'
        elif label=='changed dual metric':
            obj['scales'][0][0]=5
        elif label=='changed dual matrix':
            obj['Y'][0][0][0]=str(rational(obj['Y'][0][0][0])+F(1,100000000))
        elif label=='omitted real free coordinate':
            obj['allowed_free_pairs'].pop()
        else:
            obj['dual_constant']='-1/10000'
        action=seed_check if 'seed' in label else dual_check
        actions.append((label,lambda obj=obj,action=action:action(obj)))
    rejected=[]
    for label,action in actions:
        try:
            action()
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('input damage accepted '+label)
    return rejected


if __name__=='__main__':
    value=record()
    if '--record' in sys.argv:
        print(json.dumps(value,indent=2,sort_keys=True))
    else:
        expected=json.loads(Path(__file__).with_name('expected.json').read_text())
        exact_record(value,expected)
        print(json.dumps({'status':'PASS','canonical_record_sha256':hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                          'all_harmonic_blocks':18,'affine_dimension':42,'cancelled_real_coordinates':17,
                          'layer4_coefficients':25,'original_orders':[120,247]},sort_keys=True))
