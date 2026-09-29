#!/usr/bin/env python3
"""Independent rational algebra for README.md. No target code is imported.

This checks identities and bounds, not universal root containment or compactness.
Python 3.11+, standard library; Gaussian rationals are exact pairs of Fractions.
"""
from fractions import Fraction as F
from math import comb
import json


COUNT = 0


def require(ok, name):
    global COUNT
    if not ok:
        raise AssertionError(name)
    COUNT += 1


def g(x=0, y=0):
    return F(x), F(y)


def ga(z, w):
    return z[0] + w[0], z[1] + w[1]


def gm(z, w):
    return z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0]


def gs(z, c):
    return z[0]*c, z[1]*c


def gd(z, w):
    n = w[0]*w[0] + w[1]*w[1]
    return gs(gm(z, (w[0], -w[1])), 1/n)


def product(zs):
    r = g(1)
    for z in zs:
        r = gm(r, z)
    return r


def pm(p, q):
    out = [g()] * (len(p) + len(q) - 1)
    for i, z in enumerate(p):
        for j, w in enumerate(q):
            out[i+j] = ga(out[i+j], gm(z, w))
    return out


def pe(p, z):
    r = g()
    for c in reversed(p):
        r = ga(gm(r, z), c)
    return r


def shift_scale(p, c, h):
    """Coefficient substitution p(c+h*t), via Horner multiplication."""
    r = [g()]
    for z in reversed(p):
        r = pm(r, [c, h])
        r[0] = ga(r[0], z)
    return r


def real_multiply(p, q):
    out = [F(0)] * (len(p)+len(q)-1)
    for i, c in enumerate(p):
        for j, d in enumerate(q):
            out[i+j] += c*d
    return out


def tail_and_bounds():
    h = [F(comb(2*k, k), 4**k) for k in range(33)]
    for k in range(33):
        require(sum(h[j]*h[k-j] for j in range(k+1)) == 1,
                'binomial convolution ' + str(k))
    cap = F(1, 100)
    inva = F(4, 3)
    tail = inva**4 / (1-inva*cap)
    require(tail == F(3200, 999) and tail < 4, 'uniform series tail')
    require(h[2] == F(3, 8) and h[1]**2 == F(1, 4), 'quadratic terms')
    weights = [F(9*comb(8, k), 8*(9-k)) for k in range(3, 9)]
    coefficient_tail = sum(weights[k]*cap**k for k in range(6))
    require(coefficient_tail < 13, 'integrated coefficient tail / TQ')
    for k in range(2, 9):
        require(F(comb(6, k-2)*7, 2*comb(k, 2)) == F(comb(8, k), 8),
                'pair multiplicity ' + str(k))
    require(inva**3/2 + 4*cap < 4 and inva**2 < 2, 'failure estimate')
    require(2+4*cap < 3, 'eta / T')
    require(F(9, 8)*cap**5 < 2, 'linear coefficient / TQ')
    require(27+168*cap < 29, 'Z replacement: s')
    require(21+13 == 34, 'Z replacement: Q')
    require(F(243, 8)+216*cap < 33, 'a9 replacement: s')
    require(27*(1+13*cap) < 31, 'a9 replacement: Q')
    require(2*(29+33)+F(72, 7) < 135, 'constant term: s')
    require(2*(34+31) == 130, 'constant term: Q')
    schur_s = 8*F(135, 18)
    schur_q = F(8*130+2, 18)
    require(schur_s == 60 and schur_q < 58, 'Schur error propagation')
    a = F(3, 4)
    require((1+a)/a**2 < 4 and (1+a+a*a)/a**3 < 8, 'inverse-power errors')
    require(60+4*3 == 72 and 58+8*3+4 == 86, 'final error propagation')
    require(1-F(4, 7) == F(3, 7) and F(-1, 2)+F(4, 7) == F(1, 14),
            'quadratic positivity')
    t = F(1, 1250)
    margins = F(1, 16)-72*t, F(1, 14)-86*t
    require(margins == (F(49, 10000), F(23, 8750)), 'refined threshold margins')
    require(F(1, 14*86) < F(1, 16*72), 'open range is T < 1/1204')
    require(not tail < 3, 'mutation: tail constant three rejected')
    require(F(1, 14)-86*F(1, 1100) < 0, 'mutation: excessive threshold rejected')
    return dict(tail_bound=str(tail),threshold=str(t),margins=list(map(str,margins)),
                open_threshold='1/1204')


def polar_identity_controls():
    # Compare the root product with exact integration of the translated p'.
    # No numerical critical-point computation is involved.
    grid = [g(F(x,5),F(y,5)) for x in range(-4,5) for y in range(-4,5)
            if x*x+y*y <= 25]
    for case in range(16):
        a = F(case % 4 + 1, 5)
        available = [z for z in grid if z != g(a)]
        other = [available[(case*7+j*11) % len(available)] for j in range(8)]
        require(all(x*x+y*y <= 1 and (x,y) != g(a) for x,y in other),
                'polar root hypotheses')
        p = [g(1)]
        for z in [g(a)]+other:
            p = pm(p, [gs(z,-1),g(1)])
        dp = [gs(p[k],k) for k in range(1,len(p))]
        denom = pe(dp,g(a))
        require(denom != g(), 'simple distinguished polar root')
        b = 1-a*a
        integrand = shift_scale(dp,g(a),g(b/a))
        integrated = gs(sum_gaussian([gs(c,F(1,k+1))
                                     for k,c in enumerate(integrand)]),a**8)
        rhs = gd(integrated,denom)
        lhs = product([gd(ga(g(1),gs(z,-a)),ga(g(a),gs(z,-1))) for z in other])
        require(lhs == rhs, 'polar product = integral')
    return 16


def sum_gaussian(zs):
    out = g()
    for z in zs:
        out = ga(out,z)
    return out


def product_modulus_controls():
    # Recover the product's degree-two delta expansion by squaring every
    # modulus, multiplying, and taking a formal square root. This differs
    # from summing individual norm expansions in the written proof.
    cases = 0
    for sample in range(20):
        qs = [g(F((sample+3*j) % 13-3,5),F((2*sample+j) % 9-4,7))
              for j in range(8)]
        u = sum(z[0] for z in qs)
        vx = sum(z[0]**2 for z in qs)
        vy = sum(z[1]**2 for z in qs)
        for t in [F(0),F(1,4),F(1,2),F(1)] :
            squared = [F(1)]
            for x,y in qs:
                real = [F(1), 2*t*x-1, -t*x]
                imag = [F(0), 2*t*y, -t*y]
                rr,ii = real_multiply(real,real),real_multiply(imag,imag)
                squared = real_multiply(squared,[r+i for r,i in zip(rr,ii)])
            recovered = squared[1]/2, squared[2]/2-squared[1]**2/8
            predicted = 2*t*u-8, 2*t*t*(u*u-vx+vy)-15*t*u+28
            require(recovered == predicted, 'direct product-modulus expansion')
            cases += 1
    # Boundary moments U=8, Vx=8(1+v), Vy=0, integrated exactly.
    for v in [F(0),F(1),F(7,4)]:
        integral_second = F(2,3)*(64-8*(1+v))-F(15,2)*8+28
        require(integral_second == F(16,3)*(1-v), 'boundary variance coefficient')
    require(F(16,3)*(1-F(7,4)) < 0, 'collapsed equality family excluded')
    require(F(16,3)*(1-F(7,4)) != F(16,3)*(1+F(7,4)),
            'mutation: variance sign rejected')
    return cases


def boundary_coefficient_controls():
    for m in range(3,13):
        for variant in range(3):
            # Arbitrary even/odd T with symmetric imaginary roots.
            tpoly = [g()]* (m%2) + [g(1)]
            for j in range(m//2):
                c = F(j+variant+1,7)
                tpoly = pm(tpoly,[g(c*c),g(),g(1)])
            u = shift_scale(tpoly,g(F(-1,2)),g(1))
            # (m+1)U - S U', then translate S = X+1/2.
            q = [gs(c,m+1-k) for k,c in enumerate(u)]
            translated = shift_scale(q,g(F(1,2)),g(1))
            A = tpoly[m-2][0]
            require(translated[m:m+1] == [g(1)], 'monic reciprocal transform')
            require(translated[m-1] == g(F(-m,2)), 'first shifted coefficient')
            require(translated[m-2] == g(3*A), 'second shifted coefficient')
            require(translated[m-3] == g(-F(m-2,2)*A), 'third shifted coefficient')
    for n in range(4,13):
        m=n-1
        qs=[F(1,2)]*(m-1)+[F(n,2)]
        require(sum(qs)==m, 'collapsed family first-power equality')
        v=sum((q-1)**2 for q in qs)/m
        require(v==F(n-2,4), 'collapsed family variance')
    require(F(9-2,4)==F(7,4)>1, 'degree-nine exclusion')
    return 30


def main():
    summary = dict(agent='six-reviewer-3',role='reviewer',arithmetic='exact rational',
                   bounds=tail_and_bounds(),polar_identity_controls=polar_identity_controls(),
                   product_modulus_controls=product_modulus_controls(),
                   boundary_parity_controls=boundary_coefficient_controls(),
                   mutations_rejected=3)
    summary['checks']=COUNT
    print(json.dumps(summary,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
