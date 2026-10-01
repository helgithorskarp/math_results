"""Exact prime-lift resource counting. Python 3.11+, standard library."""
import argparse
import copy
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def integer(x):
    return type(x) is int


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def rows(data, period, minimum):
    require(data['schema'] == 1 and data['period'] == period, 'row header')
    answer = []
    for row in data['congruences']:
        require(type(row) is list and len(row) == 2, 'row shape')
        a, m = row
        require(integer(a) and integer(m), 'row integer')
        require(m >= minimum and period % m == 0 and 0 <= a < m, 'row domain')
        answer.append((a, m))
    require(len({m for a, m in answer}) == len(answer), 'duplicate modulus')
    return answer


def residual(period, prescriptions):
    covered = bytearray(period)
    for a, m in prescriptions:
        for x in range(a, period, m):
            covered[x] = 1
    return [x for x in range(period) if not covered[x]]


def analyze(Q, p, R, E):
    require(p >= 2 and all(p % d for d in range(2, math.isqrt(p) + 1)), 'prime')
    T = Q
    while T % p == 0:
        T //= p
    h = Q // T
    require(h > 1, 'positive prime exponent')
    require(len(set(E)) == len(E) and all(T % d == 0 for d in E), 'top resources')
    groups = {}
    for r in range(h):
        S = [x for x in R if x % h == r]
        if S:
            g = T
            for x in S:
                g = math.gcd(g, x - S[0])
            groups[r] = {'points': S, 'gcd': g, 'neighbors': [d for d in E if g % d == 0]}
    keys = sorted(groups)
    hall = []
    for bits in range(1 << len(keys)):
        chosen = [r for i, r in enumerate(keys) if bits >> i & 1]
        union = set().union(*(set(groups[r]['neighbors']) for r in chosen))
        deficit = p * len(chosen) - len(union)
        hall.append((deficit, chosen, sorted(union)))
    deficit, chosen, union = max(hall, key=lambda x: (x[0], -len(x[1]), x[1]))
    clones = [(r, j) for r in keys for j in range(p)]
    matched = {}

    def augment(i, seen):
        r, j = clones[i]
        for d in groups[r]['neighbors']:
            if d in seen:
                continue
            seen.add(d)
            if d not in matched or augment(matched[d], seen):
                matched[d] = i
                return True
        return False

    for i in range(len(clones)):
        augment(i, set())
    matching = [[d, *clones[i]] for d, i in sorted(matched.items())]
    require(len(matching) == len(clones) - deficit, 'matching/Hall discrepancy')
    return {'h': h, 'T': T, 'groups': groups, 'matching': matching,
            'hall': chosen, 'neighbors': union, 'deficit': deficit,
            'lower': len(clones) + deficit}


def validate(core_data, near_data, cert):
    require(cert['schema'] == 1 and cert['prime'] == 3 and
            cert['core_period'] == 5040 and cert['period'] == 15120, 'certificate header')
    Q, N, p = 5040, 15120, 3
    core = rows(core_data, Q, 8)
    near = rows(near_data, N, 8)
    require({m for a, m in core} == {m for m in divisors(Q) if m >= 8}, 'completed core')
    require({m for a, m in near} == {m for m in divisors(N) if m >= 8}, 'completed near-cover')
    require(dict((m, a) for a, m in core) == dict((m, a) for a, m in near if Q % m == 0), 'core correspondence')
    require(min(m for a, m in core) == 8 and math.lcm(*(m for a, m in core)) == Q, 'core minimum/lcm')
    R = residual(Q, core)
    E = [d for d in divisors(560) if 27 * d >= 8]
    info = analyze(Q, p, R, E)
    witnesses = cert['point_witnesses']
    require(all(type(row) is list and len(row) == 2 for row in witnesses), 'witness shape')
    seen = set()
    sample = {}
    for r, points in witnesses:
        require(integer(r) and r in info['groups'] and r not in seen, 'witness fiber')
        require(type(points) is list and points and all(integer(x) for x in points), 'witness points')
        require(len(set(points)) == len(points) and all(x in R and x % 9 == r for x in points), 'uncovered witness')
        sample[r] = points
        seen.add(r)
    require(seen == set(info['groups']), 'witness fiber coverage')
    H = cert['hall_fibers']
    require(type(H) is list and len(set(H)) == len(H) and all(r in sample for r in H), 'Hall subset')
    sample_union = set()
    for r in H:
        g = 560
        for x in sample[r]:
            g = math.gcd(g, x - sample[r][0])
        sample_union.update(d for d in E if g % d == 0)
    require(sorted(sample_union) == cert['neighbor_resources'], 'Hall neighborhood')
    lower = p * len(sample) + p * len(H) - len(sample_union)
    require(lower == cert['resource_lower_bound'] == info['lower'] and lower > len(E), 'strict resource bound')
    full_R = sorted(x + j * Q for x in R for j in range(p))
    capacities = [[27 * d, max(Counter(x % (27 * d) for x in full_R).values())] for d in E]
    near_holes = residual(N, near)
    summary = {'core_classes': len(core), 'core_residual': len(R),
               'residual_fibers': [[r, len(g['points']), g['gcd']] for r, g in info['groups'].items()],
               'lifted_fibers': p * len(info['groups']), 'top_resources': len(E),
               'maximum_singleton_matching': len(info['matching']),
               'hall_fibers': H, 'hall_neighbors': sorted(sample_union),
               'resource_lower_bound': lower, 'resource_shortfall': lower - len(E),
               'ordinary_uniform_demand': len(full_R), 'ordinary_uniform_capacity': sum(c for m, c in capacities),
               'capacities': capacities, 'near_cover_holes': len(near_holes),
               'near_holes_sha256': hashlib.sha256(','.join(map(str, near_holes)).encode()).hexdigest(),
               'matching': info['matching'], 'witness_core_points': sum(map(len, sample.values()))}
    return summary


def controls(core, near, cert):
    damaged = []
    c = copy.deepcopy(core); c['congruences'].append(c['congruences'][0]); damaged.append((c, near, cert))
    c = copy.deepcopy(core); c['congruences'][0][0] = True; damaged.append((c, near, cert))
    c = copy.deepcopy(core); c['congruences'][0][0] = c['congruences'][0][1]; damaged.append((c, near, cert))
    c = copy.deepcopy(core); c['congruences'].pop(); damaged.append((c, near, cert))
    n = copy.deepcopy(near); n['congruences'][0][0] = 4; damaged.append((core, n, cert))
    for key, value in [('prime', 2), ('period', 15121), ('resource_lower_bound', 20), ('neighbor_resources', [1])]:
        c = copy.deepcopy(cert); c[key] = value; damaged.append((core, near, c))
    c = copy.deepcopy(cert); c['point_witnesses'][0][1][0] = 5; damaged.append((core, near, c))
    c = copy.deepcopy(cert); c['hall_fibers'].append(c['hall_fibers'][0]); damaged.append((core, near, c))
    rejected = 0
    for args in damaged:
        try:
            validate(*args)
        except (ValueError, KeyError, TypeError):
            rejected += 1
    require(rejected == len(damaged), 'damaged control accepted')
    # Exhaustive physical completions for small prime lifts; their failure
    # is a control only. The theorem's completeness is the written argument.
    tested = 0
    covering = 0
    for p, Q in [(2, 6), (2, 10), (3, 6), (3, 18), (5, 10)]:
        T = Q
        while T % p == 0:
            T //= p
        h = Q // T
        E = divisors(T)
        top = [p * h * d for d in E]
        prefixes = [[], [(0, p)], [(0, Q)], [(a, Q) for a in range(Q) if a != 1]]
        if Q == 6 and p == 2:
            prefixes.append([(0, 2), (0, 3), (5, 6)])
        for prefix in prefixes:
            info = analyze(Q, p, residual(Q, prefix), E)
            for phases in itertools.product(*(range(m) for m in top)):
                tested += 1
                complete = prefix + list(zip(phases, top))
                physical = all(any(x % m == a for a, m in complete) for x in range(p * Q))
                if physical:
                    covering += 1
                    require(info['lower'] <= len(E), 'resource bound rejected genuine cover')
                if info['lower'] > len(E):
                    require(not physical, 'strict bound has a covering control')
    require(covering > 0, 'no positive completion controls')
    return {'malformed_controls_rejected': rejected, 'physical_assignments_checked': tested,
            'physical_covering_controls': covering}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--write-expected', action='store_true')
    args = ap.parse_args()
    core = json.loads((HERE / 'core.json').read_text())
    near = json.loads((HERE / 'near.json').read_text())
    cert = json.loads((HERE / 'certificate.json').read_text())
    summary = validate(core, near, cert)
    if args.controls:
        summary.update(controls(core, near, cert))
    if args.write_expected:
        (HERE / 'expected.json').write_text(json.dumps(summary, indent=2) + '\n')
    else:
        expected = json.loads((HERE / 'expected.json').read_text())
        require(all(expected.get(k) == v for k, v in summary.items()), 'expected output mismatch')
    print(json.dumps(summary, sort_keys=True))


if __name__ == '__main__':
    main()
