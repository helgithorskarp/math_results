"""Exact geometry in Q(t)[q]; no numerical roots or floating input.

Actual author six-tammes-2, researcher. Geometric completeness is explained
in PROOF.md; the certificate is not a substitute for that reduction.
"""
from itertools import permutations
import math,time
import sympy as sp
from sympy.polys.rings import ring

def derive_geometry():
    started = time.monotonic()
    t = sp.Symbol('t')
    K = sp.QQ.frac_field(t)
    R, q = ring('q', K)
    T = K.from_sympy(t)
    zero, one = (R.zero, R.one)

    def ground(a):
        return R.ground_new(K.convert(a))
    H = [[one if i == j else ground(T) for j in range(3)] for i in range(3)]
    HI = [[ground((1 / (1 - T) if i == j else 0) - T / ((1 - T) * (1 + 2 * T))) for j in range(3)] for i in range(3)]
    D = (1 - T) ** 2 * (1 + 2 * T)
    r = 2 * T / (1 + T)
    k = T * (9 * T * T - 2 * T - 3) / (1 + T) ** 2
    gamma = k / (1 + k)
    mu = (T - 1) * (T + 1) * (2 * T + 1) * (3 * T - 1) / (9 * T ** 3 - T * T - T + 1)

    def dot(a, b):
        return sum((a[i] * H[i][j] * b[j] for i in range(3) for j in range(3)), zero)

    def mv(A, x):
        return [sum((a * b for a, b in zip(row, x)), zero) for row in A]

    def cross(x, y):
        return [x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0]]

    def det(M):
        result = zero
        for p in permutations(range(len(M))):
            n = sum((p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))))
            term = ground((-1) ** n)
            for i, j in enumerate(p):
                term *= M[i][j]
            result += term
        return result

    def need(ok, message):
        if not ok:
            raise ValueError(message)

    def encode(c):
        n, d = sp.fraction(K.to_sympy(c))
        nl = list(reversed(sp.Poly(n, t, domain=sp.QQ).all_coeffs()))
        dl = list(reversed(sp.Poly(d, t, domain=sp.QQ).all_coeffs()))
        scale = sp.ilcm(*[a.q for a in nl + dl])
        return {'n': [int(a * scale) for a in nl], 'd': [int(a * scale) for a in dl]}

    def encode_poly(P):
        return [encode(P.get((i,), K.zero)) for i in range(P.degree() + 1)]

    def cleared(P):
        den = K.field.ring.one
        for c in P.values():
            den = den.lcm(c.denom)
        coeff = []
        for i in range(P.degree() + 1):
            c = P.get((i,), K.zero)
            v = c.numer * den.exquo(c.denom)
            coeff.append(sp.Poly(v.as_expr(), t, domain=sp.QQ))
        common = sp.ilcm(*[a.q for p in coeff for a in p.all_coeffs()])
        content = 0
        table = []
        for p in coeff:
            row = [int(a * common) for a in reversed(p.all_coeffs())]
            for a in row:
                content = math.gcd(content, abs(a))
            table.append(row)
        table = [[a // content for a in row] for row in table]
        return table
    B = {i: [one if j == s else zero for j in range(3)] for s, i in enumerate((1, 2, 4))}
    for n, i, j, o in ((8, 2, 4, 1), (10, 1, 2, 4), (12, 1, 10, 2), (13, 2, 8, 4)):
        B[n] = [ground(r) * (a + b) - c for a, b, c in zip(B[i], B[j], B[o])]
    for x in B.values():
        need(dot(x, x) == one, 'all B unit identities')
    need(dot(B[10], B[12]) == ground(T), 'B10-B12 retained contact')
    need(ground(mu * mu * (1 + k) ** 2) == ground(D * (1 + 2 * k)), 'equilateral orientation identity')
    d = mv(HI, cross(B[8], B[2]))
    need(dot(d, d) == ground((1 - T * T) / D), 'circle normal metric identity')
    L = ground(D) + q * q
    un = [ground(T) * a * L + (ground(D) - q * q) * (b - ground(T) * a) + ground(2 * D) * q * c for a, b, c in zip(B[8], B[2], d)]
    need(dot(un, un) == L * L, 'projective circle unit identity')
    need(dot(un, B[8]) == ground(T) * L, 'projective circle cross contact')
    certificate = {'format': 1, 'coefficient_domain': 'Q(t)[q]', 'deleted_edge': [9, 13], 'circle_denominator': encode_poly(L), 'circle_numerator': [encode_poly(a) for a in un], 'orientation_polynomials': {}, 'gram_pivots': {}, 'cleared_orientation_polynomials': {}, 'endpoint_residuals': {}}
    for sign in (-1, 1):
        cn = [ground(gamma) * a * L + ground(sign * mu) * b for a, b in zip(B[12], mv(HI, cross(B[12], un)))]
        vectors = (un, B[10], cn)
        gram = [[dot(a, b) for b in vectors] for a in vectors]
        rhs = (ground(k) * L, ground(T), ground(T) * L - ground(gamma) * dot(un, B[12]))
        M = [row + [rhs[i]] for i, row in enumerate(gram)] + [list(rhs) + [one]]
        P = det(M)
        pivot = det(gram)
        certificate['orientation_polynomials'][str(sign)] = encode_poly(P)
        certificate['gram_pivots'][str(sign)] = encode_poly(pivot)
        table = cleared(P)
        certificate['cleared_orientation_polynomials'][str(sign)] = table
        need(P.degree() <= 8, 'degree-eight projective orientation bound')
        endpoint = [ground(2 * T) * a - b for a, b in zip(B[8], B[2])]
        ce = [ground(gamma) * a + ground(sign * mu) * b for a, b in zip(B[12], mv(HI, cross(B[12], endpoint)))]
        evectors = (endpoint, B[10], ce)
        eg = [[dot(a, b) for b in evectors] for a in evectors]
        erhs = (ground(k), ground(T), ground(T) - ground(gamma) * dot(endpoint, B[12]))
        ep = det([row + [erhs[i]] for i, row in enumerate(eg)] + [list(erhs) + [one]])
        need(ep.degree() == 0, 'endpoint residual independent of q')
        certificate['endpoint_residuals'][str(sign)] = encode(ep.get((0,), K.zero))
    return certificate


def derive_loci(geometry):
    """Recompute all exceptional loci and exact real-root counts."""
    t,q=sp.symbols('t q');K=sp.QQ.frac_field(t)
    lo,hi=sp.Rational(14,25),sp.Rational(593,1000)
    def require(ok,message):
        if not ok:raise ValueError(message)
    def decode(c):
        return sum(sp.Integer(a)*t**i for i,a in enumerate(c['n']))/sum(sp.Integer(a)*t**i for i,a in enumerate(c['d']))
    def clear(expr):return sp.fraction(sp.cancel(expr))
    def table(expr):
        p=sp.Poly(expr,q,t,domain=sp.QQ)
        require(all(a.q==1 for a in p.coeffs()),'integer factor table')
        return [[int(p.coeff_monomial(q**i*t**j)) for j in range(p.degree(t)+1)] for i in range(p.degree(q)+1)]
    def locus(expr):
        num,den=clear(expr);result=[]
        for kind,poly in [('numerator',num),('denominator',den)]:
            require(poly!=0,'nonzero exceptional-locus polynomial')
            constant,factors=sp.factor_list(poly,t)
            rows=[]
            for f,m in factors:
                p=sp.Poly(f,t,domain=sp.QQ)
                require(p.eval(lo)!=0 and p.eval(hi)!=0,'closed endpoint nonvanishing')
                count=int(p.count_roots(lo,hi))
                require(count==0,'no exceptional parameter on the whole I')
                rows.append({'coefficients':[int(a) for a in reversed(p.all_coeffs())],
                             'multiplicity':m,'roots_on_I':count})
            result.append({'kind':kind,'constant':str(constant),'factors':rows})
        return result
    result={}
    for sign in (-1,1):
        residual=sum(decode(c)*q**i for i,c in enumerate(geometry['orientation_polynomials'][str(sign)]))
        num,den=clear(residual)
        require(sp.degree(den,q)==0,'orientation clearing denominator has no q')
        denominator_locus=locus(den)
        constant,all_factors=sp.factor_list(num,t,q)
        require(constant!=0,'nonzero orientation factorization constant')
        factors=sorted([x for x,m in all_factors if sp.degree(x,q)>0],
                       key=lambda a:(sp.degree(a,q),sp.degree(a,t),str(a)))
        require(all(m==1 for a,m in all_factors if sp.degree(a,q)>0),'simple factor multiplicity')
        for a,m in all_factors:
            if sp.degree(a,q)==0:locus(a)
        expected_degrees=[4,4] if sign==-1 else [1,3,4]
        require([sp.degree(a,q) for a in factors]==expected_degrees,'complete literal orientation factors')
        pivot=sum(decode(c)*q**i for i,c in enumerate(geometry['gram_pivots'][str(sign)]))
        pnum,pden=clear(pivot)
        require(sp.degree(pden,q)==0,'Gram clearing denominator has no q')
        pivot_denominator_locus=locus(pden)
        pconstant,pf=sp.factor_list(pnum,t,q)
        require(pconstant!=0,'nonzero Gram factorization constant')
        for a,m in pf:
            if sp.degree(a,q)==0:locus(a)
        nonconstant_pivots=[x for x,m in pf if sp.degree(x,q)>0]
        target={'factors':[],
                'gram_numerator_factors':[[table(a),int(m)] for a,m in pf if sp.degree(a,q)>0],
                'orientation_denominator_locus':denominator_locus,
                'gram_denominator_locus':pivot_denominator_locus}
        for a in factors:
            p=sp.Poly(a,q,domain=K)
            item={'degree':int(p.degree()),'table':table(a),
                  'leading_coefficient_locus':locus(p.LC()),
                  'discriminant_locus':locus(p.discriminant().as_expr()),
                  'gram_resultant_loci':[locus(sp.resultant(a,pivot_factor,q)) for pivot_factor in nonconstant_pivots],
                  'real_roots_at_lo':int(sp.Poly(a.subs(t,lo),q).count_roots(-sp.oo,sp.oo))}
            target['factors'].append(item)
        expected_counts=[2,2] if sign==-1 else [1,1,2]
        require([a['real_roots_at_lo'] for a in target['factors']]==expected_counts,'four real roots per orientation')
        result[str(sign)]=target
    return result

def derive_certificate():
    geometry=derive_geometry()
    result={'format':1,'interval':['14/25','593/1000'],
            'authoring_agent':'six-tammes-2','role':'researcher',
            'deleted_edge':[9,13],'geometry':geometry,'loci':derive_loci(geometry)}
    def ordinary(value):
        if isinstance(value,sp.Integer):return int(value)
        if isinstance(value,dict):return {k:ordinary(v) for k,v in value.items()}
        if isinstance(value,(list,tuple)):return [ordinary(v) for v in value]
        return value
    return ordinary(result)
