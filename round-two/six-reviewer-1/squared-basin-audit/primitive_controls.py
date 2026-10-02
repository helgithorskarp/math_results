"""Definition-level Gaussian controls added after the first record freeze.

No author executable is imported. These finite controls check the written
polynomial bridges; they are not a replacement for the analytic proof.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import signal

spec = importlib.util.spec_from_file_location('independent_basin', Path(__file__).with_name('check.py'))
own = importlib.util.module_from_spec(spec)
spec.loader.exec_module(own)
Z, ONE = (Q(0), Q(0)), (Q(1), Q(0))


def plus(x, y):
    return x[0]+y[0], x[1]+y[1]


def times(x, y):
    return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]


def scaled(x, c):
    return x[0]*c, x[1]*c


def norm2(x):
    return x[0]*x[0]+x[1]*x[1]


def divide(x, y):
    return scaled(times(x, (y[0], -y[1])), 1/norm2(y))


def dot(x, y):
    return x[0]*y[0]+x[1]*y[1]


def convolution(a, b):
    out = [Z]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = plus(out[i+j], times(x, y))
    return out


def elementary(q):
    e = [ONE]
    for x in q:
        e = convolution(e, [ONE, x])
    return e


def primitives(a, q):
    b, e = 1-a*a, elementary(q)
    origin = [ONE]
    polar = [ONE]
    for x in q:
        origin = convolution(origin, [ONE, scaled(x, -a)])
        polar = convolution(polar, [(a, Q(0)), scaled(x, b)])
    o = Z
    c = Z
    for k, (x, y) in enumerate(zip(origin, polar)):
        o = plus(o, scaled(x, Q(9, k+1)))
        c = plus(c, scaled(y, Q(1, k+1)))
    d = (-sum(a**k for k in [0, 2, 4, 6]), Q(0))
    for k in range(1, 9):
        d = plus(d, scaled(e[k], a**(8-k)*b**(k-1)/Q(k+1)))
    own.require(c == plus(ONE, scaled(d, b)), 'nonsingular polar elementary identity')
    if a == 1:
        own.require(d == plus(scaled(e[1], Q(1, 2)), (Q(-4), Q(0))), 'a=1 boundary D')
    else:
        own.require((norm2(c)-1)/b == 2*d[0]+b*norm2(d), 'whole normalized polar square')
    return o, c, d


def heavy_fibers():
    records = []
    for a in [Q(5, 8), Q(2, 3), Q(3, 4), Q(4, 5), Q(15, 16), Q(1)]:
        ell, b, p = 1/(1+a), 1-a*a, 9/(1+a)**8
        radii = [ell+Q(j, 200000) for j in range(1, 8)]
        units = []
        for j in range(8):
            t = Q(j-3, 10000)
            units.append(((1-t*t)/(1+t*t), 2*t/(1+t*t)))
        small = [scaled(u, r) for u, r in zip(units[1:], radii)]
        product_small2 = Q(1)
        for r in radii:
            product_small2 *= r*r
        o0, _, d0 = primitives(a, [Z]+small)
        oa, _, da = primitives(a, [units[0]]+small)
        o1, d1 = plus(oa, scaled(o0, -1)), plus(da, scaled(d0, -1))
        constant = norm2(o0)/(2*p)-own.MU/2*(2*d0[0]+b*norm2(d0))
        linear = dot(o0, o1)/p-own.MU*(d1[0]+b*dot(d0, d1))
        curvature = (norm2(o1)-product_small2)/(2*p)-own.MU*b*norm2(d1)/2
        reference = 16*ell-sum(radii)
        g = constant+linear*reference+curvature*reference*reference
        k = -linear-2*curvature*reference
        tests = []
        for delta in [Q(-10), -reference, Q(-3, 7), Q(0), Q(1, 9), Q(1), Q(4), Q(1000)]:
            radius = reference+delta
            o, c, d = primitives(a, [scaled(units[0], radius)]+small)
            literal = (norm2(o)-product_small2*radius*radius)/(2*p)-own.MU/2*(2*d[0]+b*norm2(d))
            own.require(literal == g-k*delta+curvature*delta*delta, 'whole heavy quadratic fiber')
            tests.append({'delta': delta, 'R': literal})
        own.require(curvature > Q(1, 8), 'positive controlled heavy curvature')
        records.append({'a': a, 'G': g, 'K': k, 'B': curvature, 'reference': reference,
                        'literal_quadratic_tests': tests})
    return records


def original_communications():
    records = []
    for a in [Q(5, 8), Q(4, 5), Q(1)]:
        roots = [(Q(-1), Q(0)), (Q(-1, 2), Q(0)), (Q(1, 3), Q(2, 5)),
                 (Q(1, 3), Q(-2, 5)), (Q(0), Q(1, 4)), (Q(0), Q(-1, 4)),
                 (Q(-3, 4), Q(1, 8)), (Q(-3, 4), Q(-1, 8))]
        own.require(all(norm2(z) <= 1 and z != (a, Q(0)) for z in roots), 'actual marked-simple disk domain')
        shifted = [ONE]
        prod_roots, prod_polar = ONE, ONE
        for z in roots:
            dist = plus((a, Q(0)), scaled(z, -1))
            shifted = convolution(shifted, [dist, (Q(-1), Q(0))])
            prod_roots = times(prod_roots, z)
            prod_polar = times(prod_polar, plus(ONE, scaled(z, -a)))
        e = [divide(scaled(x, (-1)**k*(k+1)), shifted[0]) for k, x in enumerate(shifted)]
        o, c, d = Z, Z, (Q(-sum(a**k for k in [0, 2, 4, 6])), Q(0))
        b = 1-a*a
        for k, x in enumerate(e):
            o = plus(o, scaled(x, Q(9, k+1)*(-a)**k))
            c = plus(c, scaled(x, a**(8-k)*b**k/Q(k+1)))
            if k:
                d = plus(d, scaled(x, a**(8-k)*b**(k-1)/Q(k+1)))
        own.require(o == times(e[8], prod_roots), 'actual polynomial origin identity')
        own.require(c == divide(prod_polar, shifted[0]), 'actual polynomial polar identity')
        own.require(c == plus(ONE, scaled(d, b)), 'actual normalized polar identity')
        own.require(norm2(o) <= norm2(e[8]), 'actual origin necessary inequality')
        if a == 1:
            own.require(e[1][0] >= 8 and d[0] >= 0, 'actual boundary trace constraint')
        else:
            own.require(norm2(c) >= 1 and 2*d[0]+b*norm2(d) >= 0, 'actual polar necessary inequality')
        records.append({'a': a, 'whole_critical_elementary_coefficients': e,
                        'O': o, 'C': c, 'D': d})
    return records


def gaussian_phase_witness():
    u = (Q(1, 2), Q(1, 3200))
    z = plus(ONE, scaled(divide(ONE, u), -1))
    own.require(norm2(z) == 1 and z != ONE, 'literal unit original phase witness')
    own.require(z == (Q(-2559999, 2560001), Q(3200, 2560001)), 'whole original witness coordinates')
    x, gap = Q(1, 1600), Q(3, 8)
    lo, hi = x-x**3/3, x
    own.require(8*lo*lo > gap/160000 and 8*hi*hi <= gap/96000,
                'atan interval strict phase enlargement')
    # Re u=1/2 gives |1-u|=|u| and zero Gauss--Lucas radial slack at a=1.
    own.require(norm2(plus(ONE, scaled(u, -1))) == norm2(u), 'phase witness exact origin equality')
    own.require(16*u[0] == 8, 'phase witness boundary trace equality')
    energy = 8*norm2(plus(u, (Q(-1, 2), Q(0))))
    original_energy = 8*norm2(plus(ONE, z))
    own.require(energy == Q(1, 1280000) and original_energy == Q(32, 2560001),
                'whole Gaussian entry witness energies')
    own.require(energy > gap/(163200*4) and energy <= gap/(97920*4),
                'strict enlarged negative-trace reciprocal-energy entry')
    own.require(original_energy > 4*gap/164000 and original_energy <= 4*gap/98400,
                'strict enlarged negative-trace original-energy entry')
    return {'small_q': u, 'other_original_root': z,
            'phase_lower': lo, 'phase_upper': hi, 'rho_squared_lower': 8*lo*lo,
            'rho_squared_upper': 8*hi*hi, 'S': 0,
            'original_reciprocal_energy': energy, 'original_root_energy': original_energy,
            'A': 0}


def entry_budgets():
    # gamma/d² <=3/32 follows from (1-a)(23-3a)>=0.
    own.require(own.mul([Q(1), Q(-1)], [Q(23), Q(-3)]) == [Q(23), Q(-26), Q(3)],
                'whole uniform gamma/d-square polynomial')
    margins = {'automatic_epsilon_squared': Q(1, 1000000)-Q(3, 32*97920),
               'phase': Q(1, 96000)-Q(51, 50*97920),
               'radial': Q(1, 52)-Q(12, 5*97920)*Q(8, 13)**2,
               'root_displacement': Q(1, 512**2)-Q(3, 8*98400),
               'original_to_reciprocal': 98400*Q(511, 512)**2-97920}
    own.require(all(v >= 0 for v in margins.values()), 'complete new original entry budgets')
    own.require(margins['automatic_epsilon_squared'] > 0 and margins['original_to_reciprocal'] > 0,
                'strict original entry geometric margins')
    return {'reciprocal_energy_denominator':97920,'original_energy_denominator':98400,
            'margins':margins,'additional_mathematical_premise':'REVIEW9339 phase51/50 and A<=0 radial12/5; defining original reciprocal matrix bridge.'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('primitive_expected.json'))
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    signal.alarm(45)
    record = own.serialize({'heavy_fibers': heavy_fibers(),
                            'actual_original_communications': original_communications(),
                            'gaussian_phase_witness': gaussian_phase_witness(),
                            'negative_trace_entry_budgets': entry_budgets()})
    content = json.dumps(record, sort_keys=True, separators=(',', ':'))+'\n'
    if args.write:
        args.write.write_text(content)
    else:
        own.same_typed(record, json.loads(args.expected.read_text()))
    print(json.dumps({'status': 'PASS', 'heavy_fibers': 6, 'whole_heavy_quadratic_controls': 48,
                      'actual_original_communications': 3, 'gaussian_phase_witness': True,
                      'record_bytes': len(content.encode()),
                      'record_sha256': hashlib.sha256(content.encode()).hexdigest()}))


if __name__ == '__main__':
    main()
