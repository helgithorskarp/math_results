"""Portable exact replay of the uniform dual and its sign certificate.

Arithmetic and finite model checks are same-author checks, not independent
mathematical review or proof-assistant formalization. Read PROOF.md for the
real-affine, orbit averaging and moment-inequality interpretation.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path
from certificate import beta, choose, parameters, quadratic, scalar, upper, witness
from poly import FIRST, SECOND, P, require


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def compositions(total, parts):
    if parts == 0:
        return [()] if total == 0 else []
    return [(head,)+tail for head in range(1, total+1)
            for tail in compositions(total-head, parts-1)]


def binomial_moment(j):
    """E[(sum of n independent Rademachers)^(2j)] as a polynomial in n."""
    n = FIRST
    if j == 0:
        return P(1)
    out = P(0)
    for k in range(1, j+1):
        falling = P(1)
        for i in range(k):
            falling *= n-i
        count = sum(Q(factorial(2*j), prod(factorial(2*h) for h in exponents))
                    for exponents in compositions(j, k))
        out += falling*count/factorial(k)
    return out


def prod(values):
    result = 1
    for value in values:
        result *= value
    return result


def symbolic():
    n, x = FIRST, SECOND
    V = n*n*(3*n-4)**2+8*(3*n-2)*x
    Z = 43*n**4+32*n*n*x-48*n*n+48*x
    Y = 24*n**5-107*n**4+136*n**3+32*n*n*x-48*n*n+48*x
    kp, e = 2*n+3, 2*n*n+6
    Xnum = kp*n*n*V-x*Z
    # Coefficient identity in Q[n,a]: Q_a = H_a(X_a-eta*a)/a+2-2/a.
    a, b, d = SECOND, n-SECOND, 2*SECOND-n
    v, y, xn = [p.substitute(n, d*d) for p in (V, Y, Xnum)]
    profile_identity = (3*n*n-8*b)*a*2*d*y-(3*n*n-8*a)*(xn-e*a*n*v)-(3*n*n-8*b)*(2*a-2)*n**3*v
    require(profile_identity == 0, 'Universal reciprocal profile identity')
    a1 = n*n*(32*n**5+16*n**4+97*n**3-571*n*n-264*n+720)
    a2 = 8*(2*n*n+3)*(4*n**3-13*n*n+11*n-30)
    # Clear n^6 V^2 in the original physical scalar integrand.
    left = (n-1)*(Xnum*Xnum+(n*n-x)*x*Y*Y)-4*(n-2)*x*Y*n**3*V-2*kp*Xnum*n*n*V+kp*kp*n**4*V*V
    right = (n-2)*kp*kp*n**4*V*V-n*n*V*x*(a1+a2*x)
    require(left == right, 'Universal scalar integrand coefficient identity')
    require(left != right+1, 'Nonzero coefficient control')

    T = SECOND
    s, q = T-n, n-2
    den = n*(n-1)
    B11 = T*n*n-9*T*n+16*T-n**3+9*n*n-8*n-16
    B12 = 2*(-T*n+4*T+2*n*n-4*n-4)
    B22 = -4*(-T*n+2*T+2*n*n-2*n-2)
    bulk0 = 2*T-2-2*n-n*(n-1)/2
    bulk1 = n*T-2*n*n
    require(B11+q*B12+2*q*n*(T-2*n)-s*den == 0, 'Universal first-row star equation')
    require((n-1)*B11+(n-1)*q*B12/2+2*q*(n-1)*bulk0-(T-2)*den == 0, 'Universal first-row center equation')
    require(B12+B22-2*bulk1 == 0, 'Universal second-row star equation')
    require(q*B12+q*B22/2-2*q*bulk0+s*den-(T-2)*den == 0, 'Universal second-row center equation')
    K0 = n*(-T*n+2*T+5*n*n-9*n+3)
    K1 = 2*q*(2*T*n-4*T+2*n**3-9*n*n+7*n+4)
    require(K0 == n*(T-1)-B11+4*n*(n-1)**2-q*B22-2*q*B12, 'Universal low zero-sector quadratic')
    require(K1 == 2*n*(n-1)*q*(2*n-3)+q*B22, 'Universal low point-sector quadratic')
    moments = [binomial_moment(j) for j in range(4)]
    require(moments == [P(1),n,3*n*n-2*n,15*n**3-30*n*n+16*n], 'Rademacher expansion independently yields four moments')
    bulk = [2*T*moment-2*n**(2*j)-2*n*(n-2)**(2*j)-n*(n-1)*(n-4)**(2*j)
            for j, moment in enumerate(moments)]
    A, B = n*n*(3*n-4)**2, 8*(3*n-2)
    low_num = e*e*K0+n**4*K1-2*kp*(2*n-1)*e*n*n+kp*kp*n**4
    # Clear n^4 A^2 in the moment upper bound, then divide its exact n factor.
    num = low_num*A*A+q*kp*kp*bulk[0]*n*n*A*A-(a1*bulk[1]+a2*bulk[2])*A+B*(a1*bulk[2]+a2*bulk[3])
    num = num.divide_first_monomial(1)
    require(all(j <= 1 for _, j in num.c), 'Upper bound affine in T')
    Pn, Qn = -num.coefficient_second(1)/2, num.coefficient_second(0)
    require(len(Pn.integers()) == 12 and len(Qn.integers()) == 16, 'Upper-bound degrees11/15')
    inequalities = {'a1':a1, 'a2':a2, 'P_minus256n11':Pn-256*n**11,
                    '384n15_minusQ':384*n**15-Qn}
    shifted = {name: p.substitute(n+16,0).integers() for name,p in inequalities.items()}
    require(all(all(v > 0 for v in coefficients) for coefficients in shifted.values()),
            'All four strict coefficient signs at n=16+u,u>=0')
    # T_17>(3/4)*17^4 and 2*n^4>(n+1)^4 for all integer n>=17.
    require(4*2**16 > 3*17**4 and 2*17**4 > 18**4, 'Exponential domination base and worst step')
    return {'domain':'Characteristic0 Q[n,x] and Q[n,T]; coefficient comparison; T=2^(n-1)',
            'universal_profile_identity':True,'universal_scalar_identity':True,'universal_low_layer_identities':6,
            'moments':[p.integers() for p in moments], 'P':Pn.integers(), 'Q':Qn.integers(),
            'positive_shift16_coefficients':shifted,
            'exponential_base':{'four_T17':4*2**16,'three_17_fourth':3*17**4,'two_17_fourth':2*17**4,'18_fourth':18**4},
            'uniform_moment_sign_domain':'All integer n>=17'}


def rref_table(n, deficits):
    """Separate rational elimination of the defining center/star equations.

    This restricted RREF uses neither the completion formulas nor the
    polynomial identities. The underlying affine model is credited9017.
    """
    r,T,s,m = parameters(n)
    pairs = [(a,b) for a in range(1,r+1) for b in range(a,r+1)
             if a+b <= n and (a <= 2 or a+b == n)]
    rows = []
    for a in range(1,r+1):
        for moment in (0,1):
            row = []
            for i,j in pairs:
                b = j if a == i else i if a == j else None
                row.append(Q(choose(n-a,b)*(b if moment else 1)) if b is not None else Q(0))
            row.append(Q((n-a)*s if moment else m-s))
            rows.append(row)
    pivots = []
    for col in range(len(pairs)):
        hit = next((i for i in range(len(pivots),len(rows)) if rows[i][col]),None)
        if hit is None:
            continue
        pos = len(pivots)
        rows[pos],rows[hit] = rows[hit],rows[pos]
        pivot = rows[pos][col]
        rows[pos] = [v/pivot for v in rows[pos]]
        for i in range(len(rows)):
            if i != pos and rows[i][col]:
                factor = rows[i][col]
                rows[i] = [v-factor*u for v,u in zip(rows[i],rows[pos])]
        pivots.append(col)
    require(not any(not any(row[:-1]) and row[-1] for row in rows), 'Consistent restricted affine model')
    free = [i for i in range(len(pairs)) if i not in pivots]
    require([pairs[i] for i in free] == [(a,n-a) for a in range(3,n//2+1)], 'All and only middle complements remain free')
    values = [Q(0)]*len(pairs)
    for i in free:
        values[i] = s-deficits.get(pairs[i],Q(0))
    for k,col in enumerate(pivots):
        values[col] = rows[k][-1]-sum(rows[k][i]*values[i] for i in free)
    table = [[Q(0)]*(r+1) for _ in range(r+1)]
    for (a,b),v in zip(pairs,values):
        table[a][b] = table[b][a] = v
    return table


def finite(n, supplied=None):
    r,T,s,m = parameters(n)
    table = beta(n)
    require(table == rref_table(n,{}), 'Independent RREF base recovery')
    p0,p1 = witness(n) if supplied is None else supplied
    require(len(p0) == len(p1) == r and all(type(v) is Q for v in p0+p1), 'Exact dual profiles')
    B0,B1 = upper(n,table)
    w = n*(n-1)
    constant = quadratic(B0,p0)+w*quadratic(B1,p1)
    require(constant == scalar(n), 'Physical matrix pairing equals closed scalar')
    checked = 0
    for a in range(3,n//2+1):
        deficits = {(a,n-a):Q(1)}
        changed = beta(n,deficits)
        require(changed == rref_table(n,deficits), 'Independent RREF complement recovery')
        U0,U1 = upper(n,changed)
        require(quadratic(U0,p0)+w*quadratic(U1,p1) == constant, 'Every affine complement coefficient vanishes')
        checked += 1
    if n >= 16:
        require(constant < 0, 'Finite exact negative dual')
    return {'n':n,'r':r,'complement_coefficients':checked,'constant':str(constant),
            'dual_profile_sha256':digest([[str(v) for v in p] for p in (p0,p1)]),'negative':constant<0}


def literal():
    n = 6
    r,T,s,m = parameters(n)
    table = beta(n,{(3,3):Q(7,3)})
    masks = [a for a in range(1,1<<n) if a.bit_count() <= r]
    C = [[Q(s*int(i == j)-1)+table[a.bit_count()][b.bit_count()]*int(not(a&b))
          for j,b in enumerate(masks)] for i,a in enumerate(masks)]
    require(len(C) == m and all(sum(row) == 0 for row in C), 'Literal centered core')
    L = [[Q(1)]*(m+1)]+[[Q(1)]+[v+1 for v in row] for row in C]
    full = [0]+masks
    N,h = m+1,T-1
    M = [[Q(L[i][j]-s*int(i == j),h) for j in range(N)] for i in range(N)]
    require(all(sum(row) == 1 for row in M), 'Original row sum1')
    require(all(M[i][j] == 0 for i,a in enumerate(full) for j,b in enumerate(full) if a&b), 'Original intersection support')
    require(M[0][0] == Q(1-s,h) and all(L[0][j] == 1 for j in range(N)), 'Actual empty loop and row retained')
    for point in range(n):
        star = [Q(int(a&(1<<point) != 0)) for a in masks]
        require(all(sum(v*x for v,x in zip(row,star)) == 0 for row in C), 'Literal forced star kernel')
    U = [[Q(h*int(i == j))-table[a.bit_count()][b.bit_count()]*int(not(a&b))
          for j,b in enumerate(masks)] for i,a in enumerate(masks)]
    v0,v1 = witness(n)
    t0 = [v0[a.bit_count()-1] for a in masks]
    t1 = [v1[a.bit_count()-1]*(int(a&1 != 0)-int(a&2 != 0)) for a in masks]
    B0,B1 = upper(n,table)
    require(quadratic(U,t0) == quadratic(B0,v0), 'Literal constant-sector metric')
    require(quadratic(U,t1) == 2*quadratic(B1,v1), 'Literal point-sector factor2')
    return {'n':n,'original_order':N,'empty_M_loop':str(M[0][0]),'full_L_sha256':digest([[str(v) for v in row] for row in L]),
            'full_original_support_rows_stars_and_two_forms':True,'PSD_not_claimed_for_this_affine_control':True}


def rejects(call, label):
    try:
        call()
    except ValueError:
        return label
    raise ValueError('Failed to reject '+label)


def result():
    sym = symbolic()
    small = literal()
    cases = [finite(n) for n in (6,7,16,17,20)]
    p0,p1 = witness(16)
    changed = list(p0)
    changed[2] += 1
    controls = [rejects(lambda: beta(16,{(3,13):0.5}),'floating coordinate'),
                rejects(lambda: beta(16,{(2,14):Q(1)}),'nonfree complement coordinate'),
                rejects(lambda: finite(16,(changed,p1)),'changed dual profile'),
                rejects(lambda: P({(1,0):0.5}),'floating symbolic coefficient')]
    return {'agent':'six-downset-2','role':'researcher','arithmetic':'CPython standard-library Fraction and coefficient arithmetic',
            'proof_scope':'No real centered capped H on D(n,n-2) with all noncomplement disjoint size>=3 couplings zero, for every integer n>=16',
            'symbolic':sym,'finite':cases,'literal_control':small,'rejected_controls':controls,
            'not_claimed':['General H/I','Center-free separation','First failing order','Independent review','Proof-assistant formalization']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true',help='Emit compact deterministic result; no fixture writes')
    args = parser.parse_args()
    observed = result()
    if args.emit:
        print(json.dumps(observed,indent=2,sort_keys=True))
    else:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        require(observed == expected,'Frozen expected record equality')
        print(json.dumps({'ok':True,'result_sha256':digest(observed),'uniform_n_at_least':16,
                          'symbolic_moment_domain':'n>=17','finite_boundary_n':16,'literal_order':57,'controls':4},sort_keys=True))
