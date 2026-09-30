#!/usr/bin/env python3
"""Independent exact evidence for two-family boundary stability.

Standard-library CPython 3.11. No author checker, root solver, floating
point, external data or sampling inference. Analytic bridges are in README.
"""
import hashlib
import json
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import comb


def indices(dim, degree):
    if dim == 1:
        yield (degree,)
    else:
        for first in range(degree + 1):
            for rest in indices(dim - 1, degree - first):
                yield (first,) + rest


def difference(function, alpha):
    value = F(0)
    for point in product(*(range(a + 1) for a in alpha)):
        weight = 1
        for a, coordinate in zip(alpha, point):
            weight *= (-1)**(a - coordinate) * comb(a, coordinate)
        value += weight * function(point)
    return value


def identity(function, dim, degree):
    count = 0
    for total in range(degree + 1):
        for alpha in indices(dim, total):
            assert difference(function, alpha) == 0, alpha
            count += 1
    assert count == comb(dim + degree, degree)
    return count


def elementary(values, order):
    return sum((multiply(xs) for xs in combinations(values, order)), F(0))


def multiply(values):
    answer = F(1)
    for value in values:
        answer *= value
    return answer


def collapsed_energy(point):
    alphas, ts = point[:8], point[8:]
    real_u = [F(1, 2) + a for a in alphas]
    re_e2_u = sum((real_u[i]*real_u[j] - ts[i]*ts[j]
                   for i, j in combinations(range(8), 2)), F(0))
    A, B = sum(alphas), sum(ts)
    # e2(q)=3e2(u), so (2/3) Re e2(q)=2 Re e2(u).
    return (sum(t*t for t in ts) + 14 + 7*A + A*A
            - sum(a*a for a in alphas) - B*B - 2*re_e2_u)


def shifted_relation(point):
    r = [F(x) + F(1, 2) for x in point]
    left = elementary(point, 3) - elementary(point, 2)
    right = (elementary(r, 3) - 4*elementary(r, 2)
             + 56 + F(35, 4)*(sum(r) - 8))
    return left - right


def convolution(left, right):
    out = [F(0)]*(len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i+j] += x*y
    return out


def power(poly, exponent):
    out = [F(1)]
    for _ in range(exponent):
        out = convolution(out, poly)
    return out


def derivative(poly):
    return [i*poly[i] for i in range(1, len(poly))]


def evaluate(poly, value):
    out = F(0)
    for coefficient in reversed(poly):
        out = coefficient + value*out
    return out


def trim(poly):
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def remainder(left, right):
    out = trim([F(x) for x in left])
    right = trim([F(x) for x in right])
    assert right
    while out and len(out) >= len(right):
        offset = len(out) - len(right)
        scale = out[-1]/right[-1]
        for i, coefficient in enumerate(right):
            out[offset+i] -= scale*coefficient
        trim(out)
    return out


def velocity_gcds():
    unity = [F(-1)] + [F(0)]*8 + [F(1)]
    # 28 times the first u-derivative of P_u at u=0.
    disk = [F(153)] + [F(0)]*6 + [F(36), F(-189)]
    circle = [F(0)]*4 + [F(-1), F(1)]
    for perturbation in (disk,circle):
        a, b = unity[:], perturbation[:]
        while b:
            a, b = b, remainder(a,b)
        assert [coefficient/a[-1] for coefficient in a] == [F(-1), F(1)]
    return 2


def family_checks():
    checks = 0
    # Difference has bidegree at most (8,4). A 9 by 5 grid proves it zero.
    for v in range(5):
        base = [F(1), 2*(1-F(v)), F(1)]
        h = convolution([-1, 1], power(base, 4))
        rhs = convolution(power(base, 3), [-7+8*v, 2-10*v, 9])
        for z in range(9):
            assert evaluate(derivative(h), z) == evaluate(rhs, z)
            checks += 1
    # The regular disk derivative difference has bidegree at most (8,2).
    for u in range(3):
        p = [F(0)]*10
        p[9], p[8], p[7] = F(1), F(-27, 4)*u, F(9, 7)*(u+9*u*u)
        p[0] = -sum(p[1:])
        rhs = [F(0)]*6 + [9*(9*u*u+u), -54*u, 9]
        for z in range(9):
            assert evaluate(derivative(p), z) == evaluate(rhs, z)
            checks += 1
        assert evaluate(p, 1) == 0
    # Unit-circle derivative difference is degree <=8 in z and <=1 in t.
    for t in range(2):
        p = [F(-1), 0, 0, 0, -t, t, 0, 0, 0, 1]
        rhs = [0, 0, 0, -4*t, 5*t, 0, 0, 0, 9]
        assert rhs[7] == rhs[6] == 0  # Newton sums S1=S2=0.
        for z in range(9):
            assert evaluate(derivative(p), z) == evaluate(rhs, z)
            checks += 1

    intervals = [(F(-19, 10), F(-18, 10)), (F(-11, 10), F(-9, 10)),
                 (F(3, 10), F(4, 10)), (F(15, 10), F(16, 10))]
    endpoints = []
    for left, right in intervals:
        pair = []
        for x in (left, right):
            q = x**4 + x**3 - 3*x*x - 2*x + 1
            pair.append([q, q+F(1, 1000)])
        assert -2 < left < right < 2
        assert pair[0][0]*pair[0][1] > 0
        assert pair[1][0]*pair[1][1] > 0
        assert pair[0][0]*pair[1][0] < 0
        endpoints.append([[str(y) for y in xs] for xs in pair])
    return checks, endpoints


def second_order_jet():
    # Pull back the exact binomial Taylor coefficients through w=-2x+x²+y².
    w = {(1, 0): F(-2), (2, 0): F(1), (0, 2): F(1)}
    out = {(0, 0): F(1)}
    for monomial, coefficient in w.items():
        out[monomial] = out.get(monomial, F(0)) - coefficient/2
    for a, ca in w.items():
        for b, cb in w.items():
            m = (a[0]+b[0], a[1]+b[1])
            if sum(m) <= 2:
                out[m] = out.get(m, F(0)) + F(3, 8)*ca*cb
    expected = {(0, 0): F(1), (1, 0): F(1), (2, 0): F(1), (0, 2): F(-1, 2)}
    out = {m: x for m, x in out.items() if x}
    assert out == expected
    return {str(m): str(x) for m, x in sorted(out.items())}


def rational_checks():
    tau0, large_tau, delta0 = F(1, 10**10), F(1, 100), F(2, 100000)
    tests = {
        'cauchy reciprocal sum': sum((F(comb(8, k), (k+1)*7**k) for k in range(1, 9)), F(0)) < 1,
        'symmetric phase defect': 24192+12600+4*560+70 == 39102 < 40000,
        'Newton defect throughout larger range': (7+14*large_tau)*40000 < 300000,
        'regular variance': 75000+7+7*large_tau < 76000,
        'quadratic transfer': 76000+2+large_tau < 77000,
        'quadratic input domain': 77000*tau0 < delta0,
        'critical energy transfer': 9*77000 == 693000,
        'coefficient paired sum': 126+F(84,32)+F(36,32**2)+F(9,32**3) < 129,
        'high-index constant': F(9,4)*129*27 == F(31347,4),
        'collapsed energy': 32*tau0+160+F(2,3)*50000+F(56,3) < 34000,
        'collapsed roots': 16*34000 < 800**2,
        'collapsed scalar matching': (100008**2+100000**2)*tau0 < 3,
        'collapsed critical matching': 16*(2*80+2*3) == 2656 < 52**2,
        'regular radius collapse': 77000 < 278**2 and 2500*77000**2*278*F(1,10**15) < 5,
        'regular linear constant': 2400+5 < 2500,
        'refined quadratic root scale': 9*delta0 < F(1,32)**2,
        'refined radius bound': 1200*delta0+2500*delta0**2*F(1,200) < F(1,40),
        'refined sqrt bound': delta0 < F(1,200)**2,
        'refined Rouche tail': sum((F(comb(9,k))*F(1,40)**(k-1) for k in range(2,10)),F(0)) < 1,
        'refined coefficient norm factor': F(41,40)**8+1 < F(9,4),
        'refined radial dominance': F(9,4)*1024 < 8*300,
        'refined critical dominance': F(9,4)*F(31347,4) < 8*2500,
        'refined disjoint disks': F(1,20) < F(4,9),
        'collapsed finite sharpness derivative': F(3,32)**2 < F(1,10)**2*F(199,200)**3,
        'collapsed negative root sign': -7+8*F(1,100) < 0,
        'collapsed positive root sign': 4-2*F(1,100) > 0,
    }
    for name, passed in tests.items():
        assert passed, name
    assert [F(18), F(-7), F(4)] != [F(-18), F(-7), F(4)]
    return len(tests)


def mutations():
    bad_energy = lambda p: collapsed_energy(p) + sum(p[:8])
    assert difference(bad_energy, (1,)+(0,)*15) != 0
    v, z = F(1), F(0)
    base = [1, 2*(1-v), 1]
    bad = convolution(power(base,3),[-7-8*v,2-10*v,9])
    assert evaluate(derivative(convolution([-1,1],power(base,4))),z) != evaluate(bad,z)
    # The larger circle invalidates the very binomial lower bound used.
    assert sum((F(comb(9,k))*F(1,20)**(k-1) for k in range(2,10)),F(0)) > 1
    return 3


def main():
    energy = identity(collapsed_energy,16,2)
    shift = identity(shifted_relation,8,3)
    grid, signs = family_checks()
    jet = second_order_jet()
    bounds = rational_checks()
    gcds = velocity_gcds()
    rejected = mutations()
    evidence = {
        'method': 'complete polynomial-basis mixed differences; exact bidegree interpolation grids; independent binomial pullback jet; rational analytic endpoint comparisons',
        'collapsed_energy_basis_checks': energy,
        'shift_basis_checks': shift,
        'sharp_family_grid_checks': grid,
        'first_power_second_order_jet': jet,
        'rational_bounds': bounds,
        'regular_velocity_gcd_checks': gcds,
        'regular_velocity_gcd': 'z-1 for both perturbations against z^9-1; every nonmarked ninth root has nonzero first velocity',
        'quartic_endpoint_values': signs,
        'mutations_rejected': rejected,
        'proved_interpolation_domain': '0<=delta2<=2/100000, boundary disk roots, no first-power smallness assumption',
        'matching_bound': '300*D+2500*delta2^(5/2)',
        'collapsed_sharpness_control': '3*v/32<=tau(v)<=v/10 for 0<v<=1/100',
        'trust_boundary': 'exact finite algebra only; README and REFINEMENT supply universal analytic bridges'
    }
    encoded = (json.dumps(evidence,indent=2,sort_keys=True)+'\n').encode()
    if sys.argv[1:] == ['--json']:
        sys.stdout.buffer.write(encoded)
    else:
        assert not sys.argv[1:]
        print(f'PASS: {energy+shift} complete basis checks; {grid} sharp-family grid checks; {gcds} velocity gcds; first-power jet; {bounds} exact bounds; {rejected} mutations rejected.')
        print('certificate SHA256:',hashlib.sha256(encoded).hexdigest())


if __name__ == '__main__':
    main()
