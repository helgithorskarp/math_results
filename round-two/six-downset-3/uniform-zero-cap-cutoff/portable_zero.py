"""Portable whole-polynomial zero-limit identities and domain signs.

No CAS import. Exact degree-bounded determinant equalities are polynomial
proofs; finite original-member comparisons are a different obligation.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
import coefficient as c
p = c.r.poly
require = c.require
Q, K = p.Q, p.K
C = p.constant
A, M, S = p.add, p.mul, p.scale


def product(*xs):
    out = C(1)
    for x in xs:
        out = M(out, x)
    return out


def clearing():
    qm1, qm2, qm3, ff = A(Q,C(-1)), A(Q,C(-2)), A(Q,C(-3)), A(S(Q,3),C(5))
    D = product(Q,qm1,qm2,qm3,ff)
    Dq = product(qm1,qm2,qm3,ff)
    tab={}
    def put(x,y,value):tab[tuple(sorted((x,y)))]=value
    o,pp,a,b,cc,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    put(o,o,A(S(product(qm2,qm3,ff),6),product(A(S(Q,-1),C(-4),K),Q,qm2,qm3,ff)))
    put(o,pp,product(Q,Q,qm3,qm3,ff))
    put(pp,pp,A(S(product(qm1,ff),12),S(product(Q,Q,ff),4),
                S(product(Q,qm1,ff,A(S(Q,-3),C(-4),S(product(Q,qm1),F(1,2)),K)),2),
                S(product(K,A(Q,C(1))),-12)))
    for leaf,alpha,beta,gamma in (
        (o,A(D,S(Dq,-1)),A(D,Dq),A(D,S(Dq,6))),
        (pp,A(D,S(product(K,qm2,qm3),2)),
            A(D,S(product(qm1,qm1,qm3,ff),2),S(product(K,Q,qm3),2)),
            A(D,S(Dq,6),S(product(K,A(Q,C(1)),qm2,qm3),-6)))):
        for core,value in ((a,alpha),(cc,alpha),(b,beta),(d,beta),(e,gamma)):put(leaf,core,value)
    for x,y,value in ((a,a,C(0)),(a,b,C(0)),(b,b,C(0)),(a,cc,S(D,2)),
                      (a,d,M(A(S(Q,3),C(2)),Dq)),(b,cc,M(A(S(Q,3),C(2)),Dq)),
                      (b,d,product(A(S(M(Q,Q),3),Q,C(-2)),qm2,qm3,ff))):
        put(x,y,value)
    return D,tab


def choose(n,r):
    return C(1) if r==0 else n if r==1 else S(M(n,A(n,C(-1))),F(1,2))


def cleared_grams():
    D,tab=clearing()
    types=((0,1),(0,2),(1,1),(1,1),(2,0),(3,0),(2,1),(2,1))
    groups=((0,),(0,),(1,),(2,4),(6,),(7,),(3,5),(6,))
    mass=[S(choose(Q,t[1]),len(gs)) for gs,t in zip(groups,types)]
    even=[]
    for i,t in enumerate(types):
        row=[]
        for j,tt in enumerate(types):
            count=sum(not(x&y) for x in groups[i] for y in groups[j])
            val=M(D,A(S(M(A(S(Q,3),C(4)),mass[i]),int(i==j)),S(M(mass[i],mass[j]),-1)))
            if count:
                val=A(val,S(product(choose(Q,t[1]),choose(A(Q,C(-t[1])),tt[1]),tab[tuple(sorted((t,tt)))]),count))
            row.append(S(val,4))
        even.append(row)
    standard=[]
    for i,t in enumerate(c.TYPES):
        row=[]
        for j,tt in enumerate(c.TYPES):
            val=C(0)
            if i==j:
                norm=S(A(Q,C(-2)),2) if t[1]==2 else C(2)
                val=product(D,A(S(Q,3),C(4)),S(norm,len(c.GROUPS[i])))
            count=sum(not(x&y) for x in c.GROUPS[i] for y in c.GROUPS[j])
            if count:
                outside=C(-2) if t[1]==tt[1]==1 else S(product(A(Q,C(-2)),A(Q,C(-3))),-2) if t[1]==tt[1]==2 else S(A(Q,C(-2)),-2)
                val=A(val,S(M(outside,tab[tuple(sorted((t,tt)))]),count))
            row.append(S(val,4))
        standard.append(row)
    for G in (even,standard):
        require(all(G[i][j]==G[j][i] for i in range(len(G)) for j in range(len(G))),
                'EVERY independently cleared Gram reciprocity coefficient')
        require(all(v.denominator==1 for row in G for poly in row for v in poly.values()),
                'complete4D polynomial clearing integral')
    return S(D,4),tab,even,standard


def evaluate_matrix(G,q,kap=0):
    out=[[p.evaluate(poly,q,kap) for poly in row] for row in G]
    require(all(v.denominator==1 for row in out for v in row), 'entire cleared evaluation integral')
    return [[int(v) for v in row] for row in out]


def det_integer(A):
    n=len(A)
    if n==1:return A[0][0]
    W=[list(row) for row in A];previous=1;sign=1
    for j in range(n-1):
        pivot=next((i for i in range(j,n) if W[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:W[j],W[pivot]=W[pivot],W[j];sign=-sign
        cur=W[j][j]
        for i in range(j+1,n):
            for k in range(j+1,n):
                val,rem=divmod(cur*W[i][k]-W[i][j]*W[j][k],previous)
                require(rem==0,'every exact integer Bareiss division')
                W[i][k]=val
        previous=cur
    return sign*W[-1][-1]


def degree_det(G):
    # Zero entries contribute no monomials. Sum of row maxima is a
    # proved bound on every determinant term, independent of cancellation.
    return sum(max((i for poly in row for (i,j),v in poly.items() if j==0),default=0) for row in G)


def dense(poly):
    values=[F(v) for v in poly]
    return {(i,0):v for i,v in enumerate(values) if v}


def polynomial_matrix_record(G):
    """Lossless JSON record of every sparse rational coefficient."""
    return [[[[list(power), str(value)] for power, value in sorted(poly.items())]
             for poly in row] for row in G]


def det_fraction(A):
    """Distinct exact elimination control; no fraction-free divisions."""
    W = [[F(value) for value in row] for row in A]
    out = F(1)
    for j in range(len(W)):
        pivot = next((i for i in range(j, len(W)) if W[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            W[j], W[pivot] = W[pivot], W[j]
            out = -out
        value = W[j][j]
        out *= value
        for i in range(j+1, len(W)):
            ratio = W[i][j]/value
            for k in range(j+1, len(W)):
                W[i][k] -= ratio*W[j][k]
    return out


def shift4(poly):
    return [sum(F(poly[j])*comb(j,i)*4**(j-i) for j in range(i,len(poly))) for i in range(len(poly))]


EVEN_TYPES = ((0,1),(0,2),(1,1),(1,1),(2,0),(3,0),(2,1),(2,1))
EVEN_GROUPS = ((0,),(0,),(1,),(2,4),(6,),(7,),(3,5),(6,))


def original_binding(q, even, standard):
    """Every ordered original pair; no orbit-count Gram construction."""
    members = c.r.domain(q, 0)[1:]
    tab = c.r.table(q)
    frames = []
    for member in members:
        core, outside = member & 7, (member >> 3).bit_count()
        value = int(bool(member & (1 << 3)))-int(bool(member & (1 << 4)))
        i = next((i for i,(gs,t) in enumerate(zip(EVEN_GROUPS,EVEN_TYPES))
                  if core in gs and outside == t[1]), None)
        j = next((i for i,(gs,t) in enumerate(zip(c.GROUPS,c.TYPES))
                  if core in gs and outside == t[1]), None) if value else None
        frames.append((member,i,j,value))
    pairs = [([[F(0)]*8 for _ in range(8)], [[F(0)]*8 for _ in range(8)]),
             ([[F(0)]*6 for _ in range(6)], [[F(0)]*6 for _ in range(6)])]
    for aa,i,j,value in frames:
        for bb,ii,jj,other in frames:
            base,der,*_ = c.r.entry(q,3*q+4,tab,aa,bb)
            if i is not None and ii is not None:
                pairs[0][0][i][ii] += base
                pairs[0][1][i][ii] += der
            if j is not None and jj is not None:
                pairs[1][0][j][jj] += value*other*base
                pairs[1][1][j][jj] += value*other*der
    D,*_ = cleared_grams()
    for source,(base,der) in zip((even,standard),pairs):
        for kap in (F(0),F(1,4096),F(1,8)):
            actual = [[base[i][j]+kap*der[i][j] for j in range(len(base))] for i in range(len(base))]
            cleared = [[p.evaluate(v,q,kap) for v in row] for row in source]
            factor = p.evaluate(D,q,kap)
            require(cleared == [[factor*v for v in row] for row in actual],
                    'EVERY original member pair binds both literal affine Grams')
    return {'q':q, 'original_members':len(members), 'all_ordered_original_pairs':len(members)**2,
            'both_complete_affine_Gram_coefficients_checked':True,
            'actual_pair_sum_sha256':c.r.exact.digest(c.r.encode(pairs))}


def verify(raw=None):
    D,tab,even,standard=cleared_grams()
    if raw is None:
        raw=json.loads(Path(__file__).with_name('CLOSED-ZERO.json').read_text())
    require([entry['name'] for entry in raw['rows']]==['nu0','tau0'],
            'ENTIRE closed coefficient certificate has both ordered targets')
    # Full q,kappa polynomial binding for the readable six-to-two reduction.
    s = A(S(Q,3),C(4))
    Dw = S(product(A(M(Q,Q),S(Q,F(1,3)),C(F(-2,3))),
                   A(Q,C(-2)),A(Q,C(-3)),A(S(Q,3),C(5))),12)
    norms = (2,4,4,2)
    for i in range(4):
        for j in range(4):
            expected = S(M(D,s),norms[i]) if i==j else S(Dw,-norms[i]) if (i,j) in ((0,3),(3,0),(1,2),(2,1)) else C(0)
            require(standard[i+2][j+2]==expected,
                    'EVERY full q,kappa cleared two-core-pair coefficient')
    for i in range(2):
        for j, multiple in enumerate((1,2,2,1)):
            require(standard[i][j+2]==S(standard[i][5],multiple),
                    'EVERY full q,kappa outside-to-core rank-one coefficient')
    rows=[]
    for entry in raw['rows']:
        name=entry['name'];num,den=dense(entry['numerator']),dense(entry['denominator'])
        for side in ('numerator','denominator'):
            shifted=shift4(entry[side])
            require(shifted[0]>0 and all(v>=0 for v in shifted), 'ALL complete closed-zero numerator/denominator domain coefficients')
        G=[row[1:] for row in even[1:]] if name=='tau0' else standard
        minor=[row[:-1] for row in G[:-1]]
        # tau0=det(G)/(q D det(minor)); nu0=det(G)/(2 D det(minor)).
        prefactor=M(Q,D) if name=='tau0' else S(D,2)
        bound=max(degree_det(G)+max(i for i,j in den),
                  degree_det(minor)+max(i for i,j in num)+max(i for i,j in prefactor))
        points=[]
        for q in range(4,5+bound):
            whole_value, minor_value = evaluate_matrix(G,q), evaluate_matrix(minor,q)
            big,small=det_integer(whole_value),det_integer(minor_value)
            require(big == det_fraction(whole_value) and small == det_fraction(minor_value),
                    'every identity point: Bareiss and independent fractional determinant')
            lhs=big*p.evaluate(den,q,0)
            rhs=small*p.evaluate(prefactor,q,0)*p.evaluate(num,q,0)
            require(lhs==rhs, 'EVERY complete degree-bounded original determinant identity')
            points.append([q,str(big),str(small)])
        rows.append({'name':name,'entire_two_side_q_degree_bound':bound,'exact_identity_points':len(points),
                     'all_point_values_sha256':c.r.exact.digest(points),
                     'closed_num_coefficients':entry['numerator'],'closed_den_coefficients':entry['denominator'],
                     'shifted_numerator':shift4(entry['numerator']), 'shifted_denominator':shift4(entry['denominator']),
                     'every_point_two_distinct_exact_determinant_algorithms': True,
                     'no_CAS_import_or_interpolation_input':True})
    # Entire sharp univariate improvement over the old closed dual.
    A4=dense([6,-24,16,3,3]);B7=dense([-56,364,-176,-996,66,783,279,108]);oldD=dense([-12,12,57,36])
    P=product(A(S(Q,3),C(2)),A(S(Q,3),C(4)),A(S(M(Q,Q),3),S(Q,3),C(-2)))
    tau_entry=raw['rows'][1]
    require(dense(tau_entry['numerator'])==S(M(P,A4),2) and
            dense(tau_entry['denominator'])==M(Q,B7),
            'EVERY coefficient of displayed factored tau0 rational formula')
    difference=A(M(A4,oldD),S(B7,-1))
    expected=S(product(A(Q,C(-1)),A(Q,C(-1)),A(S(Q,3),C(2)),A(S(Q,3),C(4))),-2)
    require(difference==expected, 'EVERY coefficient of strict tau0 versus old2c improvement')
    bindings = [original_binding(q,even,standard) for q in (4,9,12)]
    return {'actual_agent':'six-downset-3','role':'researcher','domain':'ALL integerq>=4; exact zero-limit coefficient identities',
            'rows':rows,'strict_old_dual_difference_factor': '-2(q-1)^2(3q+2)(3q+4)',
            'original_member_bindings':bindings,
            'all_general_kappa_standard_pair_and_cross_coefficients_verified':True,
            'displayed_tau0_factored_formula_entirely_verified':True,
            'full_original_cleared_even_sha256':c.r.exact.digest(polynomial_matrix_record(even)),
            'full_original_cleared_standard_sha256':c.r.exact.digest(polynomial_matrix_record(standard)),
            'ordinary_symmetry_kernel_and_limit_bridges_unformalized':True}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=verify()
    args.out.write_text(json.dumps(c.r.encode(value),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'closed_zero_whole_polynomial_checks':[{k:x[k] for k in ('name','entire_two_side_q_degree_bound','exact_identity_points')} for x in value['rows']]}))
