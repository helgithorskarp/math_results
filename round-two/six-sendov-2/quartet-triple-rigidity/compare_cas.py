#!/usr/bin/env python3
"""Optional same-author dense SymPy 1.14 whole-record comparison.

No native arithmetic/checker is imported. This is corroboration, not review.
Bernstein vectors are reconstructed by exact interpolation in a dense basis.
"""
from pathlib import Path
from itertools import combinations
import hashlib
import json
import sympy as s


def require(ok, label):
    if not ok:
        raise ValueError(label)


def equal(a, b, label):
    require(s.cancel(a - b) == 0, label)


def rec(expr, names):
    vs = s.symbols(' '.join(names), seq=True)
    terms = {}
    for term in s.Add.make_args(s.expand(expr)):
        if not term:
            continue
        powers = term.as_powers_dict()
        ee = tuple(int(powers.get(v, 0)) for v in vs)
        c = s.cancel(term / s.prod(v ** k for v, k in zip(vs, ee)))
        require(c.is_Rational is True, 'QQ Laurent coefficient')
        terms[ee] = terms.get(ee, s.Rational(0)) + c
    return {'variables': list(names),
            'whole_QQ_Laurent_terms': [[list(e), str(c)]
                                      for e, c in sorted(terms.items(), reverse=True) if c]}


def closed_bernstein(poly, x):
    degree = s.Poly(poly, x, domain=s.QQ).degree()
    if degree == 0:
        return [s.Rational(poly)]
    # Independent dense interpolation: evaluations at all natural-degree nodes.
    nodes = [s.Rational(i, degree) for i in range(degree + 1)]
    matrix = s.Matrix([[s.binomial(degree, j) * t ** j * (1-t) ** (degree-j)
                        for j in range(degree + 1)] for t in nodes])
    values = s.Matrix([s.expand(poly).subs(x, t/4) for t in nodes])
    return list(matrix.inv() * values)


def oriented_parts(expr, x):
    numerator, denominator = s.fraction(s.cancel(expr))
    if denominator.subs(x, 0) < 0:
        numerator, denominator = -numerator, -denominator
    require(denominator.subs(x, 0) > 0, 'positive rational orientation at zero')
    return s.expand(numerator), s.expand(denominator)


def corner(k):
    x = s.Symbol('x')
    a = 1 - x / s.Integer(k)
    ds = s.cancel((k - k * a ** 3 - x ** 3) / (6 * a))
    fifth = s.cancel(k * a ** 5 + 20 * a ** 3 * ds + 10 * a * ds ** 2 + x ** 5)
    equal(k*a+x, k, 'exact whole first moment')
    equal(k*a**3+6*a*ds+x**3, k, 'exact whole third moment')
    numerator, denominator = oriented_parts(ds, x)
    gap_n, gap_d = oriented_parts(a*a-ds, x)
    gain_n, gain_d = oriented_parts(fifth-k, x)
    derivative = s.diff(fifth, x).subs(x, 0)
    require(derivative == 5, 'exact boundary fifth gain')
    pp = {'delta_numerator_over_x': s.cancel(numerator/x), 'delta_denominator': denominator,
          'old_positive_gap_numerator': gap_n, 'old_positive_gap_denominator': gap_d,
          'fifth_gain_numerator_over_x': s.cancel(gain_n/x), 'fifth_gain_denominator': gain_d}
    certs = {}
    for name, p in pp.items():
        bb = closed_bernstein(p, x)
        require(all(b > 0 for b in bb), 'whole interpolated positive Bernstein vector')
        certs[name] = {'polynomial': rec(p, ['x']),
                       'all_Bernstein_coefficients_on_0_to_1_over_4': list(map(str, bb))}
    return {'positive_support': k, 'mean': rec(a, ['x']),
            'pair_split_square': {'numerator': rec(numerator, ['x']), 'denominator': rec(denominator, ['x'])},
            'old_positive_gap': {'numerator': rec(gap_n, ['x']), 'denominator': rec(gap_d, ['x'])},
            'fifth_gain': {'numerator': rec(gain_n, ['x']), 'denominator': rec(gain_d, ['x'])},
            'right_fifth_gain_derivative': str(derivative), 'all_positive_certificates': certs}


def extension_record(expr):
    expr = s.expand(expr)
    b = expr.coeff(s.sqrt(57))
    a = s.expand(expr - b * s.sqrt(57))
    require(a.is_Rational is True and b.is_Rational is True, 'exact quadratic field coefficients')
    return [str(a), str(b)]


def control():
    a = (47-3*s.sqrt(57))/32
    b = (-29+9*s.sqrt(57))/32
    left = [s.Integer(1)]*3+[s.Rational(1,2)]
    right = [a]*3+[b]
    return {'field_relation': 'r^2=57', 'positive_embedding_bounds': ['15/2', '38/5'],
            'left': list(map(extension_record, left)), 'right': list(map(extension_record, right)),
            'first_third_fifth_differences': {str(j): extension_record(sum(v**j for v in left)-sum(v**j for v in right))
                                            for j in (1,3,5)}}


def fiber_control():
    z = s.Symbol('z')
    base = s.prod(z-i for i in range(1,5))
    q = z*z-10*z+30
    controls = []
    for eps in (-s.Rational(1,1000),s.Rational(1,1000)):
        g = base + eps*q
        # Derive all three odd moments directly from this monic quartic's coefficients.
        p = s.Poly(g,z,domain=s.QQ)
        ee = [-p.nth(3),p.nth(2),-p.nth(1),p.nth(0)]
        ps = [s.Integer(4)]
        for j in range(1,6):
            value = sum((-1)**(i-1)*ee[i-1]*ps[j-i] for i in range(1,min(j,4)+1))
            if j<=4:
                value += (-1)**j*(4-j)*ee[j-1]
            ps.append(s.expand(value))
        require([ps[i] for i in (1,3,5)] == [10,100,1300], 'literal matched odd moments')
        brackets = []
        for i in range(1,5):
            l,r = s.Rational(i)-s.Rational(1,100),s.Rational(i)+s.Rational(1,100)
            aa,bb = s.expand(g).subs(z,l),s.expand(g).subs(z,r)
            require(l>0 and aa*bb<0, 'all four exact positive root brackets')
            brackets.append({'interval':[str(l),str(r)],'entire_endpoint_values':[str(aa),str(bb)]})
        controls.append({'A':str(35+eps),'whole_quartic':rec(g,['z']),'four_root_brackets':brackets})
    return {'S':'10','K':'100','L':'1300','T':'-300','U':'-1026','R':'12600',
            'quadratic':rec(q,['z']),'distinct_actual_quartets':controls}


def build():
    z,t,b = s.symbols('z t b')
    names = ['z','t','b']
    lam,mu = s.Rational(5,3)*(t*t+b*b),-5*t*t*b*b
    multiplier = 5*z**4-3*lam*z*z-mu
    equal(multiplier,5*(z*z-t*t)*(z*z-b*b),'whole multiplier factor')
    lower,upper = s.diff(multiplier,z).subs(z,t),s.diff(multiplier,z).subs(z,b)
    S0,K0 = 3*t+b,3*t**3+b**3
    universal = dict(zip(['multiplier','lower_Hessian','upper_Hessian','cube_min_gap','cube_max_gap',
                          'support3_cube_gap','regular_zero_opening_fifth_derivative'],
                         [rec(p,names) for p in [multiplier,lower,upper,16*K0-S0**3,S0**3-K0,S0**3-9*K0,-mu]]))
    z,S,T,U,A,d = s.symbols('z S T U A d')
    names = ['z','S','T','U','A','d']
    q = z*z-S*z-T/S
    e3,e4 = S*A+T,U-T*A/S
    g = z**4-S*z**3+A*z*z-e3*z+e4
    R = -T*T-S*S*U
    p3 = S**3-3*S*A+3*e3
    p5 = S**5-5*S**3*A+5*S*S*e3+5*S*A*A-5*A*e3-5*S*e4
    equal(S*A*e3-e3*e3-S*S*e4,R,'Hurwitz pencil invariant')
    cross = q*g.subs(z,-z)-g*q.subs(z,-z)
    abar = S*S/2-s.Rational(1,4)
    bar = g.subs(A,abar)
    f = s.Poly(s.expand((bar+d*q)*(bar.subs(z,-z)-d*q.subs(z,-z))),z)
    vv = s.symbols('v0:4')
    ss = sum(vv)
    aa = sum(s.prod(c) for c in combinations(vv,2))
    bb = sum(s.prod(c) for c in combinations(vv,3))
    cc = s.prod(vv)
    hurwitz = ss*aa*bb-bb*bb-ss*ss*cc
    equal(hurwitz,s.prod(vv[i]+vv[j] for i,j in combinations(range(4),2)), 'whole classical pair product')
    hn,hd = z*q*q,S-2*z
    derivative_numerator = s.diff(hn,z)*hd-hn*s.diff(hd,z)
    N = S*q-2*z*(S-2*z)**2
    critical = R*(S-2*z)-2*S*S*z*q*q
    equal(s.diff(g,z)*q-g*s.diff(q,z),-critical/S**2,'whole independent double-root equation')
    return {'schema':'six-sendov-2.quartet-rigidity.v1',
            'exact_domains':['QQ sparse polynomials','QQ[S,S^-1,T,U,A,d,z]','QQ[r]/(r^2-57)'],
            'universal_quartet_maps':universal,'all_equal_support_zero_openings':[corner(k) for k in (2,3)],
            'essential_fifth_moment_control':control(),
            'pencil':{'quartic':rec(g,names),'quadratic':rec(q,names),'third_power':rec(p3,names),
                       'fifth_power':rec(p5,names),'Hurwitz_invariant':rec(R,names),
                       'full_Hurwitz_pair_product':rec(hurwitz,['v0','v1','v2','v3']),
                       'quotient_decomposition':rec(q*(z*z+A+T/S)-R/S**2,names),
                       'whole_odd_cross_part':rec(cross,names),'normalized_Abar':rec(abar,names),
                       'all_nine_normalized_octic_coefficients_ascending':[rec(f.nth(j),names) for j in range(9)],
                       'J':rec(d*R/(4*S),names)},
            'fiber_interval_bridges':{'H_numerator':rec(hn,names),'H_denominator':rec(hd,names),
                       'H_derivative_numerator':rec(derivative_numerator,names),'critical_cubic_N':rec(N,names),
                       'critical_cubic_derivative':rec(s.diff(N,z),names),'N_at_zero':rec(N.subs(z,0),names),
                       'N_at_quarter_sum':rec(N.subs(z,S/4),names),'N_at_half_sum':rec(N.subs(z,S/2),names),
                       'direction_discriminant':rec(S*S+4*T/S,names),'entire_double_root_equation':rec(critical,names)},
            'literal_nonsingleton_positive_fiber':fiber_control()}


def main():
    require(s.__version__ == '1.14.0', 'documented optional SymPy version')
    record = build()
    expected_path = Path(__file__).with_name('expected.json')
    raw = (json.dumps(record,sort_keys=True,indent=2,allow_nan=False)+'\n').encode('utf-8')
    expected = expected_path.read_bytes()
    require(record == json.loads(expected), 'complete dense CAS parsed record')
    require(raw == expected, 'complete dense CAS canonical bytes')
    print(json.dumps({'status':'PASS','sympy':s.__version__,'entire_record_bytes':len(raw),
                      'sha256':hashlib.sha256(raw).hexdigest(),
                      'Bernstein_method':'dense exact interpolation',
                      'all_normalized_octic_coefficients':9,'same_author_not_independent_review':True}))


if __name__ == '__main__':
    main()
