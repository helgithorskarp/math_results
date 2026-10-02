"""Produce the three star identities and all 27 annulus seam certificates.

Actual author six-tammes-1, researcher. Geometry and scope: PROOF.md.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
from poly import Rat, bernstein

LO, HI = F(9, 20), F(1)
ONE, C, H = Rat([1]), Rat([0, 1]), Rat([1, 2])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def signed(p, sign):
    values = bernstein(p, LO, HI)
    require(all(sign * x > 0 for x in values), 'strict closed-band sign')
    return [str(x) for x in values]


def stars():
    # B_t = A*b, S = A*s, A^2 = H. Cotangent addition generates b.
    rows, b = [], ONE
    for t in (1, 2, 3):
        divisor = ONE + C * b
        s = (ONE - C * C) / (H * divisor)
        p = ONE - H * s
        delta = H * s * s - Rat([4]) * p
        require((p - C * C - C * H * s * b).n == [], 'second endpoint star')
        rows.append({'t': t, 'B_over_A': b.encode(), 'S_over_A': s.encode(),
                     'P': p.encode(), 'Delta': delta.encode(),
                     'solver_divisor_over_A': divisor.encode(),
                     'solver_divisor_numerator_Bernstein': signed(divisor.n, 1),
                     'solver_divisor_denominator_Bernstein': signed(divisor.d, 1),
                     'Delta_numerator_Bernstein': signed(delta.n, -1),
                     'Delta_denominator_Bernstein': signed(delta.d, 1)})
        b = (H * b - ONE) / (H * (b + ONE))
    return rows


def name(v):
    return str(v[0]) + ':' + str(v[1])


def ring(sides, ports):
    # All identifications are disjoint pairs; no union-find in this producer.
    vertices = [(i, j) for i, q in enumerate(sides) for j in range(q)]
    pairs = []
    for i, k in enumerate(ports):
        nxt = (i + 1) % 3
        pairs += [sorted(((i, k), (nxt, 1))), sorted(((i, k + 1), (nxt, 0)))]
    paired = [v for pair in pairs for v in pair]
    require(len(set(paired)) == len(paired), 'disjoint seam endpoints')
    classes = sorted(pairs + [[v] for v in vertices if v not in set(paired)])
    representative = {v: group[0] for group in classes for v in group}

    def track(order, first):
        walk = []
        for i in order:
            local = range(1, ports[i] + 1) if first else list(range(ports[i] + 1, sides[i])) + [0]
            for j in local:
                v = representative[i, j]
                if not walk or v != walk[-1]:
                    walk.append(v)
        require(walk[0] == walk[-1], 'track closes')
        walk.pop()
        require(len(walk) == len(set(walk)), 'track is simple')
        smallest = walk.index(min(walk))
        return walk[smallest:] + walk[:smallest]

    cycles = sorted((track((0, 1, 2), True), track((0, 2, 1), False)))
    arcs = sorted((cycle[j], cycle[(j + 1) % len(cycle)])
                  for cycle in cycles for j in range(len(cycle)))
    membership = {v: index for index, cycle in enumerate(cycles) for v in cycle}
    require(set(membership) == set(representative.values()), 'whole boundary coverage')
    seams = []
    for i, k in enumerate(ports):
        endpoints = [representative[i, k], representative[i, k + 1]]
        require(membership[endpoints[0]] != membership[endpoints[1]], 'seam splits boundaries')
        seams.append({'face': i, 'endpoints': [name(v) for v in endpoints]})
    mixed = [sum(len(classes_for(v, classes)) == 2 for v in cycle) for cycle in cycles]
    require(mixed == [3, 3], 'three mixed corners per boundary')
    require(len(classes) == sum(sides) - 6, 'quotient count')
    return {'sides': list(sides), 'ports': list(ports),
            'classes': [[name(v) for v in group] for group in classes],
            'boundary_arcs': [[name(a), name(b)] for a, b in arcs],
            'boundary_cycles': [[name(v) for v in cycle] for cycle in cycles],
            'seams': seams, 'mixed_corners_per_boundary': mixed}


def classes_for(v, classes):
    return next(group for group in classes if group[0] == v)


def prism():
    labels = [layer + str(i) for layer in ('U', 'V') for i in range(3)]
    gram = []
    for a in range(6):
        row = []
        for b in range(6):
            horizontal = F(4, 7) if a % 3 == b % 3 else F(-2, 7)
            vertical = F(3, 7) if a // 3 == b // 3 else F(-3, 7)
            row.append(str(horizontal + vertical))
        gram.append(row)
    return {'c': '1/7', 'labels': labels, 'Gram': gram,
            'contact_pairs': [[labels[a], labels[b]] for a in range(6) for b in range(a + 1, 6)
                              if F(gram[a][b]) == F(1, 7)],
            'faces': [['U0', 'U1', 'U2'], ['V0', 'V2', 'V1'],
                      ['U0', 'V0', 'V1', 'U1'], ['U1', 'V1', 'V2', 'U2'],
                      ['U2', 'V2', 'V0', 'U0']]}


def certificate():
    rings = [ring(q, k) for q in product((4, 5), repeat=3)
             for k in product(*(range(2, size - 1) for size in q))]
    require(len(rings) == 27, 'complete labeled port domain')
    return {'format': 1, 'actual_agent': 'six-tammes-1', 'role': 'researcher',
            'algebraic_closed_band': ['9/20', '1'], 'physical_upper_endpoint_excluded': True,
            'application_closed_band': ['1/2', '3/5'], 'A_squared': ['1', '2'],
            'star_cases': stars(), 'rings': rings, 'prism_calibration': prism(),
            'adjacent_angle_factorization': {'left': ['-1', '0', '3', '2'],
                                             'right_factors': [['-1', '2'], ['1', '1'], ['1', '1']]}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', type=Path)
    args = parser.parse_args()
    data = certificate()
    raw = json.dumps(data, sort_keys=True, separators=(',', ':')) + '\n'
    if args.emit:
        args.emit.write_text(raw)
    else:
        require(Path(__file__).with_name('CERTIFICATE.json').read_text() == raw, 'entire certificate regeneration')
    print(json.dumps({'star_cases': 3, 'strict_negative_discriminants': 3,
                      'annulus_port_cases': 27, 'seams_joining_distinct_boundaries': 81,
                      'calibration': 'six-point triangular prism at c=1/7',
                      'certificate_sha256': hashlib.sha256(raw.encode()).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
