#!/usr/bin/env python3
"""Exact audits of the ray relabelling theorem; standard library only.

The Gaussian analytic theorem is an external written prerequisite. This
program checks geometry and equality of endpoint measures, not quadrature.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rank(rows):
    a = [[Q(x) for x in row] for row in rows]
    p = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(p, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[p], a[pivot] = a[pivot], a[p]
        scale = a[p][j]
        a[p] = [x/scale for x in a[p]]
        for i in range(len(a)):
            if i != p:
                factor = a[i][j]
                a[i] = [x-factor*y for x, y in zip(a[i], a[p])]
        p += 1
        if p == len(a):
            break
    return p


def descriptors():
    return [(i, j, s, t) for i, j in combinations(range(3), 2)
            for s, t in product((-1, 1), repeat=2)]


def point(label, radius=1):
    i, j, s, t = label
    x = [0, 0, 0]
    x[i], x[j] = radius*s, radius*t
    return tuple(x)


def original(x):
    """Recover the map from coordinates, independently of sign labels."""
    if not any(x):
        return (0, 0, 0)
    active = [i for i, a in enumerate(x) if a]
    require(len(active) == 2, 'Not a ray point')
    i, j = active
    radius = abs(x[i])
    require(abs(x[j]) == radius, 'Unequal active coordinate magnitudes')
    y = [0, 0, 0]
    y[3-i-j] = Q(x[i]*x[j], radius)
    return tuple(y)


def alternative(x):
    if not any(x):
        return (0, 0, 0)
    active = [i for i, a in enumerate(x) if a]
    require(len(active) == 2, 'Not a ray point')
    i, j = active
    require(abs(x[i]) == abs(x[j]), 'Unequal active coordinate magnitudes')
    y = [0, 0, 0]
    y[3-i-j] = x[i]
    return tuple(y)


def pushforward(atoms, mapping):
    result = defaultdict(Q)
    for x, mass in atoms:
        result[mapping(x)] += mass
    return {x: m for x, m in result.items() if m}


def encode_measure(measure):
    return [[list(map(str, x)), str(m)] for x, m in sorted(measure.items())]


def canonical_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(raw).hexdigest()


def verify():
    labels = descriptors()
    xs = list(map(point, labels))
    maps = {'S': original, 'R': alternative}
    polynomial_counts = {}
    for name, mapping in maps.items():
        counts = Counter()
        for a, b in product(labels, repeat=2):
            x, z = point(a), point(b)
            y, w = mapping(x), mapping(z)
            # Independent coordinate expansion of the coefficient triple
            # of |r*x-u*z|^2 - |r*y-u*w|^2.
            coefficients = (dot(x, x)-dot(y, y),
                            -2*(dot(x, z)-dot(y, w)),
                            dot(z, z)-dot(w, w))
            i, j, s, t = a
            h, k, sp, tp = b
            if (i, j) == (h, k):
                middle = -2*t*tp if name == 'R' else -2*(s*sp+t*tp-s*sp*t*tp)
            else:
                common = next(iter({i, j} & {h, k}))
                middle = -2*x[common]*z[common]
            require(coefficients == (1, middle, 1), 'Polynomial identity failed')
            require(middle >= -2, 'No nonnegative (r-u)^2+c*r*u decomposition')
            counts[int(middle)] += 1
        polynomial_counts[name] = dict(sorted(counts.items()))

    affine_ranks = {}
    for name, mapping in maps.items():
        rows = [(1,)+x+mapping(x) for x in xs]
        affine_ranks[name] = rank(rows)-1
    require(affine_ranks == {'S': 6, 'R': 5}, 'Unexpected paired affine rank')
    require(all(x[0] == alternative(x)[1]+alternative(x)[2] for x in xs),
            'The paired hyperplane relation failed')
    require(original((0, 0, 0)) == alternative((0, 0, 0)) == (0, 0, 0),
            'The maps must fix zero')

    uniform_s = pushforward([(x, Q(1, 12)) for x in xs], original)
    uniform_r = pushforward([(x, Q(1, 12)) for x in xs], alternative)
    require(uniform_s == uniform_r, 'Uniform endpoints differ')
    require(len(uniform_s) == 6 and set(uniform_s.values()) == {Q(1, 6)},
            'The image is not the uniform six-axis law')

    # Independent signed incidence matrices of the pushforward difference.
    output = sorted(uniform_s)
    incidence = []
    for y in output:
        incidence.append([int(original(x) == y)-int(alternative(x) == y) for x in xs])
    require(rank(incidence) == 3, 'Expected three independent balance equations')
    for row in incidence:
        nonzero = [(labels[j], coefficient) for j, coefficient in enumerate(row) if coefficient]
        require(len(nonzero) == 2, 'Unexpected output-law difference')
        (a, ca), (b, cb) = nonzero
        require(a[:2] == b[:2] and a[3] == b[3] == -1 and ca == -cb,
                'Difference is not the claimed negative-branch balance')

    # Three distinct radii, unequal plane masses, biased positive branches.
    radii = (Q(1, 3), Q(1), Q(5, 2))
    atoms = [((0, 0, 0), Q(7))]
    for plane, (i, j) in enumerate(combinations(range(3), 2), 1):
        for index, radius in enumerate(radii, 1):
            for s, t in product((-1, 1), repeat=2):
                if t == -1:
                    mass = plane*index+2
                elif s == 1:
                    mass = plane+2*index+1
                else:
                    mass = 2*plane+index+3
                atoms.append((point((i, j, s, t), radius), Q(mass)))
    total = sum(m for _, m in atoms)
    atoms = [(x, m/total) for x, m in atoms]
    image = pushforward(atoms, original)
    require(image == pushforward(atoms, alternative), 'Balanced radial laws differ')
    require(sum(image.values()) == 1, 'Probability mass is not preserved')

    # An independent pairwise exact-distance check at unequal rational radii.
    rational_pair_checks = 0
    for (x, _), (z, _) in combinations(atoms, 2):
        dx = sum((a-b)**2 for a, b in zip(x, z))
        for mapping in maps.values():
            dy = sum((a-b)**2 for a, b in zip(mapping(x), mapping(z)))
            require(dx >= dy, 'A rational-distance check failed')
            rational_pair_checks += 1

    unbalanced = list(atoms)
    unbalanced.append((point((0, 1, 1, -1)), Q(1, 101)))
    require(pushforward(unbalanced, original) != pushforward(unbalanced, alternative),
            'An unbalanced control was incorrectly accepted')
    equal_mass_only = [(point((0, 1, 1, -1), 1), Q(1, 2)),
                       (point((0, 1, -1, -1), 2), Q(1, 2))]
    require(pushforward(equal_mass_only, original) != pushforward(equal_mass_only, alternative),
            'Equal total ray masses were confused with equal radial measures')

    # Match the twelve non-anchor points of the classical fixture directly.
    tetrahedron = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    classical = {}
    for i, j in product(range(4), repeat=2):
        if i != j:
            x = tuple(b-a for a, b in zip(tetrahedron[i], tetrahedron[j]))
            y = tuple(a+b for a, b in zip(tetrahedron[i], tetrahedron[j]))
            require(original(x) == y, 'Not the classical depth-one flap map')
            classical[x] = y
    require(set(classical) == {point(label, 2) for label in labels}, 'Flap sites differ')
    require(all(x[0] != x[1]+x[2] for x in tetrahedron),
            'An anchor unexpectedly satisfies the alternative fixed-image relation')

    table = [[list(x), list(map(int, original(x))), list(alternative(x))] for x in xs]
    return dict(status='RAY_RELABELLING_CHECKS_PASS',
                ray_count=len(labels), exact_polynomial_checks=2*len(labels)**2,
                middle_coefficient_counts=polynomial_counts,
                paired_affine_ranks=affine_ranks, pushforward_difference_rank=rank(incidence),
                balanced_example_atoms=len(atoms), balanced_example_output_atoms=len(image),
                rational_pair_checks=rational_pair_checks,
                rejected_output_equality_controls=2, classical_flap_matches=len(classical),
                unit_ray_table_sha256=canonical_hash(table),
                balanced_output_sha256=canonical_hash(encode_measure(image)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = verify()
    if args.check:
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        # JSON converts integer dictionary keys to strings.
        require(json.loads(json.dumps(result)) == expected, 'EXPECTED.json differs')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
