"""Literal controls for the ordinary density proof and four-tail bridge.

The ordinary proof, including equality classification, is in proof.md.
These controls are not an enumeration of all subsets of the parent universe.
"""
import hashlib
import itertools
import json
import math


def require(ok, message):
    if not ok:
        raise ValueError(message)


P = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
B = tuple(n for n in range(8, 2521) if 2520 % n == 0
          and n not in (8, 9, 10, 12, 14))
U = [y for y in range(315) if y % 9 != 0]


def stage(a21):
    phases = {n: 1 if n % 2 == 0 else 0 for n in B}
    phases.update({20: 0, 40: 36, 15: 12, 30: 22, 60: 32, 21: a21})
    return list(P) + list(phases.items())


def holes(classes, period):
    require(len({n for n, _ in classes}) == len(classes), 'Duplicate original modulus')
    require(all(8 <= n and 0 <= a < n and period % n == 0 for n, a in classes),
            'Malformed original phase inventory')
    return [x for x in range(period) if all(x % n != a for n, a in classes)]


def tail_phases(rows):
    alpha, beta = rows
    a80 = next(a for a in range(80) if a % 16 == 12 and a % 5 == alpha)
    a160 = next(a for a in range(160) if a % 32 == 28 and a % 5 == beta)
    return [(16, 4), (32, 12), (80, a80), (160, a160)]


def record():
    actualU = sorted(x % 315 for x in range(2520)
                     if x % 8 == 4 and all(x % n != a for n, a in P))
    require(actualU == U and len(U) == 280, 'Parent4 CRT universe')
    fixtures = []
    color_cells = 0
    matching_counts = 0
    for a in range(21):
        R = [(b, c) for b in range(7) for c in range(1, 9)
             if not (b == a % 7 and c % 3 == a % 3)]
        require(len(R) == (54 if a % 3 == 0 else 53), '21 deletion count')
        classes = stage(a)
        residual = holes(classes, 2520)
        actual = sorted(x % 315 for x in residual if x % 8 == 4)
        expected = [y for y in U if y % 5 in (3, 4) and y % 21 != a]
        require(actual == expected, 'Sharp BASE stage mismatch')
        require(len(actual) == 108 - 2 * (a % 3 != 0), 'Sharp count')
        require(len({y % 5 for y in actual}) == 2, 'Ordinary triple in fixture')
        for k in range(8):
            E = [(b, c) for b, c in R if (b + c - 1) % 8 == k]
            m = len(E)
            require(m in (6, 7), 'Color matching too small')
            require(len({b for b, _ in E}) == m and len({c for _, c in E}) == m,
                    'Improper cell coloring')
            # An A-labeled point appears in this many complete 5-matchings.
            incidence = math.comb(m - 1, 4) * math.factorial(4)
            total = math.comb(m, 5) * math.factorial(5)
            require(incidence * m == total, 'Exact averaging incidence')
            matching_counts += total
            color_cells += m
        require(len(residual) > len(actual), 'Fixture accidentally clears other parents')
        # BASE periods divide2520; verify all four physical lifts directly.
        lifted = holes(classes, 10080)
        require(lifted == sorted(x + 2520 * j for x in residual for j in range(4)),
                'BASE lift mismatch')
        fixtures.append({'phase21': a, 'parent4_count': len(actual),
                         'total_BASE_holes2520': len(residual),
                         'parent4_holes_sha256': hashlib.sha256(
                             json.dumps(actual, separators=(',', ':')).encode()).hexdigest()})
    missing = [(n, a) for n, a in stage(0) if n != 21]
    omitted = sorted(x % 315 for x in holes(missing, 2520) if x % 8 == 4)
    require(omitted == [y for y in U if y % 5 in (3, 4)] and len(omitted) == 112,
            'Missing21 countercontrol')
    bridge = []
    literal_points = 0
    for rows in itertools.combinations(range(5), 2):
        tail = tail_phases(rows)
        labels = [n for n, _ in tail]
        require(labels == [16, 32, 80, 160] and not any(n in B for n in labels),
                'Four-tail original ownership')
        targets = [x for x in range(10080) if x % 8 == 4 and x % 5 in rows]
        require(len(targets) == 504, 'Bridge domain size')
        require(all(any(x % n == a for n, a in tail) for x in targets),
                'Four-tail bridge failed')
        # Removing160 leaves a literal uncovered point in its second row.
        damage = next(x for x in targets if x % 32 == 28 and x % 5 == rows[1])
        require(not any(damage % n == a for n, a in tail if n != 160),
                'Missing160 countercontrol')
        literal_points += len(targets)
        bridge.append({'rows': list(rows), 'tail': [list(p) for p in tail],
                       'physical_target_count': len(targets),
                       'missing160_uncovered_control': damage})
    return {'sharp21_fixtures': fixtures, 'sharp_cases': 21,
            'matching_color_cells': color_cells,
            'exact_five_matchings_counted': matching_counts,
            'omitted21_countercontrol_count': len(omitted),
            'four_tail_bridge': bridge, 'bridge_literal_points': literal_points,
            'ordinary_equality_proof_is_unformalized': True,
            'full_cover_claimed': False}


if __name__ == '__main__':
    print(json.dumps(record(), sort_keys=True, indent=2))
