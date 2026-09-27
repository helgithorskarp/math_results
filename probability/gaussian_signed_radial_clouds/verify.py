"""Exact ancillary controls for the written signed-radial cloud theorem.

No Gaussian quadrature or floating-point sign is used. Polynomial identities
are checked coefficient by coefficient. Finite controls do not establish
the written universal analytic proof or its imported Gaussian endpoint.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ArithmeticError(message)


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError('Exact integer or rational string required')
    return F(value)


def schedule(m, epsilon):
    if isinstance(m, bool) or not isinstance(m, int) or m < 1:
        raise ValueError('m must be a positive integer')
    e = rational(epsilon)
    if not 0 < e <= 1:
        raise ValueError('epsilon must lie in (0,1]')
    target = 32 * (m + 1) / e
    n = -(-target.numerator // target.denominator)
    exponent = 2 * m + 4 * n
    # Keep the cutoff compressed; no integer of size 2**exponent is built.
    return {'m': m, 'epsilon': str(e), 'cloud_relative_width': str(e / 8),
            'N': n, 'E': exponent, 'eta_coefficient': str(e / 48),
            'eta_negative_binary_exponent': exponent,
            'variance_over_R_squared_coefficient': str(2112 / e),
            'variance_over_R_squared_binary_exponent': exponent}


def check_schedule(record):
    m = record['m']; e = F(record['epsilon']); n = record['N']
    need(type(m) is int and m >= 1 and 0 < e <= 1, 'schedule domain')
    need(type(n) is int and n - 1 < 32 * (m + 1) / e <= n, 'ceiling')
    need(F(record['cloud_relative_width']) == e / 8, 'cloud width')
    exponent = 2 * m + 4 * n
    need(record['E'] == exponent == record['eta_negative_binary_exponent']
         == record['variance_over_R_squared_binary_exponent'], 'exponents')
    need(F(record['eta_coefficient']) == e / 48, 'gap coefficient')
    cutoff = F(record['variance_over_R_squared_coefficient'])
    need(cutoff * F(record['eta_coefficient']) == 44, 'Gaussian endpoint constant')
    need(cutoff > 8 and exponent > 0, 'endpoint regime')
    large_bound = 3 * e * n / 64 - e * m / 4 - m - F(1, 2)
    need(large_bound >= 1 + F(m, 4), 'large-parameter margin')
    need(F(1, 2) <= n, 'parameter windows join')
    return large_bound


def add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else F(0))
            + (b[i] if i < len(b) else F(0)) for i in range(n)]


def scale(c, p):
    return [F(c) * x for x in p]


def multiply(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def same(a, b, message):
    difference = add(a, scale(-1, b))
    need(all(x == 0 for x in difference), message)


def polynomial_controls():
    one = [F(1)]; variable = [F(0), F(1)]
    kappa = [F(1), -F(1, 4)]
    target = [F(1), -F(3, 4)]
    gap = add(multiply(kappa, kappa), scale(-1, multiply(target, target)))
    same(gap, [0, 1, -F(1, 2)], 'squared radial loss')
    # After subtracting epsilon/2, the remainder is epsilon(1-epsilon)/2.
    same(add(gap, [0, -F(1, 2)]),
         multiply(scale(F(1, 2), variable), [1, -1]), 'loss nonnegative remainder')
    same(add(multiply(kappa, kappa), [-1, F(1, 2)]),
         [0, 0, F(1, 16)], 'hexagon dilation slack')
    # Clear the positive denominator 1+t in the two axial barycentres.
    same(add(one, scale(-1, multiply(variable, variable))),
         multiply([1, 1], [1, -1]), 'axial barycentre x')
    same(add(scale(-1, variable), variable), [0], 'axial barycentre y')
    same(add([1, -F(1, 2)], [0, -F(1, 2)]), [1, -1], 'diagonal barycentre')
    # At z=32(m+1)/epsilon, J lower bound is 1+(1/2-epsilon/4)m.
    same(add([F(1, 2), -F(1, 4)], [-F(1, 4)]),
         [F(1, 4), -F(1, 4)], 'large-parameter remainder')
    need(44 * 48 == 2112, 'cutoff product')
    return 7


def barycentres(ell, r):
    need(0 <= ell < r, 'cloud means domain')
    vertices = [(r, -ell), (-ell, r), (r, -r), (-r, r)]
    rows = [(r / (r + ell), ell / (r + ell), 0, 0),
            (ell / (r + ell), r / (r + ell), 0, 0),
            (0, 0, 1 - ell / (2 * r), ell / (2 * r))]
    targets = [(r - ell, 0), (0, r - ell), (r - ell, ell - r)]
    for weights, target in zip(rows, targets):
        need(sum(weights) == 1 and min(weights) >= 0, 'barycentric masses')
        for j in (0, 1):
            need(sum(w * v[j] for w, v in zip(weights, vertices)) == target[j],
                 'hexagon inclusion')
    return 6  # Three displayed vertices and their negatives.


def rank(rows):
    rows = [list(map(F, r)) for r in rows]; k = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(k, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[k], rows[pivot] = rows[pivot], rows[k]
        lead = rows[k][j]; rows[k] = [x / lead for x in rows[k]]
        for i in range(k + 1, len(rows)):
            factor = rows[i][j]
            rows[i] = [x - factor * y for x, y in zip(rows[i], rows[k])]
        k += 1
    return k


def fold(a):
    if a < 0:
        return -fold(-a)
    return a if a <= 1 else 2 - a


def finite_control():
    radii = list(map(F, ['0', '1/8', '1', '2', '15/4', '4']))
    weights = list(map(F, ['1/8', '1/8', '1/4', '1/8', '1/8', '1/4']))
    directions = [(F(1), F(0), F(0)), (F(3, 5), F(4, 5), F(0)),
                  (F(1, 3), F(2, 3), F(2, 3))]
    need(sum(weights) == 1 and all(w > 0 for w in weights), 'radial weights')
    need(all(sum(x*x for x in u) == 1 for u in directions), 'unit directions')
    low = sum(p for a, p in zip(radii, weights) if a <= F(1, 4))
    high = sum(p for a, p in zip(radii, weights) if a >= F(15, 4))
    need(low == F(1, 4) and high == F(3, 8), 'cloud masses')
    need(abs(fold(F(4))) == F(2), 'outer fold guard')
    pairs = sorted(set((tuple(a*x for x in u), tuple(fold(a)*x for x in u))
                       for a in radii for u in directions))
    strict = tight = 0; losses = []
    for i, (x, y) in enumerate(pairs):
        for a, b in pairs[:i]:
            loss = sum((p-q)**2 for p,q in zip(x,a))-sum((p-q)**2 for p,q in zip(y,b))
            need(loss >= 0, 'finite contraction')
            strict += loss > 0; tight += loss == 0
            if loss:
                losses.append(loss)
    joined = [x+y for x,y in pairs]
    paired_rank = rank([[a-b for a,b in zip(p,joined[0])] for p in joined[1:]])
    need(paired_rank == 6, 'paired affine rank')
    return {'sites': len(pairs), 'strict_pairs': strict, 'tight_pairs': tight,
            'minimum_strict_loss': str(min(losses)), 'paired_rank': paired_rank,
            'low_cloud_mass': str(low), 'high_cloud_mass': str(high),
            'profile_lipschitz_constant': '1', 'radial_schedule': schedule(2, '1/2')}


def run():
    identities = polynomial_controls()
    bary_count = sum(barycentres(F(j, 20), F(r)) for r in (1, 2, 4) for j in range(20))
    schedules = [schedule(m, e) for m in (1, 2, 4, 12, 100, 10**100)
                 for e in ('1', '1/2', '1/10', '1/1000', '1/1000000000000')]
    for row in schedules:
        check_schedule(row)
    damaged = 0
    for key, value in [('N', 1), ('E', 1), ('eta_coefficient', '1/47'),
                       ('variance_over_R_squared_coefficient', '44'),
                       ('cloud_relative_width', '1/7')]:
        bad = schedule(2, '1/2'); bad[key] = value
        try:
            check_schedule(bad)
        except ArithmeticError:
            damaged += 1
    for m, e in [(0, '1/2'), (True, '1/2'), (1, '0'), (1, '2'), (1, 0.5)]:
        try:
            schedule(m, e)
        except (ValueError, TypeError):
            damaged += 1
    need(damaged == 10, 'damaged schedule accepted')
    fixture = finite_control()
    diffuse = schedule(4, '1/2')
    need(diffuse['N'] == 320 and diffuse['E'] == 1288, 'uniform radial example')
    out = {'status': 'SIGNED_RADIAL_CLOUD_EVENTUAL_EXACT_CONTROLS_PASS',
           'universal_polynomial_identities': identities,
           'finite_barycentric_vertex_checks': bary_count,
           'exact_schedule_controls': len(schedules), 'damaged_inputs_rejected': damaged,
           'finite_input_control': fixture, 'uniform_radial_example': diffuse,
           'gaussian_integration_performed': False,
           'trust': 'Exact algebra and finite controls; universal theorem is the written proof.'}
    out['record_sha256'] = hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--schedule', nargs=2, metavar=('M', 'EPSILON'))
    args = parser.parse_args()
    if args.schedule:
        row = schedule(int(args.schedule[0]), args.schedule[1]); check_schedule(row)
        print(json.dumps(row, indent=2)); return
    out = run()
    if not args.emit:
        expected = json.loads((HERE/'EXPECTED.json').read_text())
        need(out == expected, 'expected record mismatch')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
