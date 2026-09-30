"""Alternate full replay using original labels, CRT inversion and sets.

Author: six-covering-3, researcher. This self-audit is not external review.
The main replay does not use the production canonical generator, decoder,
resource coefficients, capacity counter, bitset state or period lift.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import gcd, lcm, prod
from pathlib import Path
from time import monotonic
import json
import random
import check as production

ANCHORS = (8, 9, 10, 12, 15, 18, 20, 24, 25, 30)
AXES = {360: (8, 9, 5), 1800: (8, 9, 25)}
HERE = Path(__file__).resolve().parent


def base_period(depth):
    return 360 if depth < 9 else 1800


@lru_cache(None)
def prime_powers(n):
    result = []
    for p in range(2, n + 1):
        if n % p:
            continue
        maximal = 1
        while n % p == 0:
            maximal *= p
            n //= p
        result.append((p, maximal))
        if n == 1:
            break
    return tuple(result)


def normalize(previous):
    names, answer = {}, []
    for modulus, residue in previous:
        coordinates = []
        for p, maximal in prime_powers(modulus):
            encoded, power = 0, 1
            while power < maximal:
                key = p, power, residue % power
                children = names.setdefault(key, {})
                child = residue // power % p
                if child not in children:
                    children[child] = len(children)
                encoded += power * children[child]
                power *= p
            coordinates.append((maximal, encoded))
        image = next(r for r in range(modulus)
                     if all(r % axis == value for axis, value in coordinates))
        answer.append((modulus, image))
    return tuple(answer)


def options(modulus, previous):
    for residue in range(modulus):
        enlarged = previous + ((modulus, residue),)
        if normalize(enlarged) == enlarged:
            yield residue


def resources(Q, placed=(), minimum=8):
    five_power = AXES[Q][2]
    result = {}
    for g in range(1, Q + 1):
        if Q % g:
            continue
        value = Fraction(1)
        if g % 8 == 0:
            value /= 1 - Fraction(1, 2)
        if g % five_power == 0:
            value /= 1 - Fraction(1, 5)
        if g < minimum:
            value -= 1
        if g in placed:
            value -= 1
        scaled = 4 * value
        if scaled.denominator != 1 or scaled < 0:
            raise RuntimeError('invalid independently derived resource')
        if scaled:
            result[g] = int(scaled)
    return result


def decode(Q, boxes):
    result = {}
    axes = AXES[Q]
    for box in boxes:
        if len(box) != 4 or any(type(v) is not int for v in box) or box[3] <= 0:
            raise ValueError('bad box')
        coordinates = []
        for mask, axis in zip(box[:3], axes):
            if not 0 < mask < 2**axis:
                raise ValueError('bad mask')
            coordinates.append(tuple(a for a in range(axis) if mask & 2**a))
        for point in product(*coordinates):
            x = sum(a * (Q // axis) * pow(Q // axis, -1, axis)
                    for a, axis in zip(point, axes)) % Q
            if x in result:
                raise ValueError('overlapping rectangles')
            result[x] = box[3]
    return result


def maxima_of(Q, weights, moduli):
    return {g: max(sum(weights.get(x, 0) for x in range(a, Q, g))
                   for a in range(g)) for g in moduli}


def literal_replay(path=HERE / 'weights.json', max_nodes=10000, seconds=30):
    data = json.loads(Path(path).read_text())
    if data['format_version'] != 1 or data['axes_by_period'] != {
            str(Q): list(axes) for Q, axes in AXES.items()}:
        raise ValueError('bad header')
    certificates = {}
    for residues, Q, boxes in data['certificates']:
        key = tuple(residues)
        if key in certificates or not 1 <= len(key) <= len(ANCHORS) or Q != base_period(len(key)):
            raise ValueError('invalid certificate prefix')
        if any(type(a) is not int or not 0 <= a < m for a, m in zip(key, ANCHORS)):
            raise ValueError('invalid phase')
        certificates[key] = Q, boxes
    used = set()
    nodes, uniform, weighted = ([0] * (len(ANCHORS) + 1) for _ in range(3))
    equality, min_gap = 0, None
    digest, start = sha256(), monotonic()
    equality_fixtures = []

    def visit(previous):
        nonlocal equality, min_gap
        depth = len(previous)
        Q = base_period(depth)
        residues = tuple(a for m, a in previous)
        if sum(nodes) >= max_nodes or monotonic() - start > seconds:
            raise production.IncompleteSearch('alternate complete audit limit')
        nodes[depth] += 1
        # Recompute from the original congruences, including after Q changes.
        active = {x for x in range(Q) if all(x % m != a for m, a in previous)}
        if not active:
            raise RuntimeError('anchor cover invalidates theorem')
        resource = resources(Q, tuple(m for m, a in previous))
        weights = {x: 1 for x in active}
        demand = len(weights)
        maxima = maxima_of(Q, weights, resource)
        total = sum(resource[g] * maxima[g] for g in resource)
        tag = None
        if total <= 4 * demand:
            uniform[depth] += 1
            tag = 'uniform'
        elif residues in certificates:
            certificate_period, boxes = certificates[residues]
            if certificate_period != Q:
                raise ValueError('period mismatch')
            weights = decode(Q, boxes)
            if not weights or not set(weights) <= active:
                raise ValueError('weight outside the literal uncovered set')
            demand = sum(weights.values())
            maxima = maxima_of(Q, weights, resource)
            total = sum(resource[g] * maxima[g] for g in resource)
            if total > 4 * demand:
                raise ValueError('literal weighted inequality fails')
            weighted[depth] += 1
            used.add(residues)
            tag = 'weighted'
            gap = 4 * demand - total
            min_gap = gap if min_gap is None else min(min_gap, gap)
        if tag:
            if resource.get(Q, 0) <= 0 or maxima.get(Q, 0) <= 0:
                raise ValueError('missing positive omitted-tail witness')
            if total == 4 * demand:
                equality += 1
                equality_fixtures.append((Q, previous, weights))
            event = [tag, Q, residues, demand, total, sorted(maxima.items())]
            digest.update((json.dumps(event, separators=(',', ':')) + '\n').encode('ascii'))
            return
        if depth == len(ANCHORS):
            raise RuntimeError('literal terminal branch remains open')
        modulus = ANCHORS[depth]
        for residue in options(modulus, previous):
            visit(previous + ((modulus, residue),))

    visit(())
    if used != set(certificates):
        raise ValueError('alternate replay has unused certificates')
    result = {'agent': 'six-covering-3', 'role': 'researcher',
              'claim': 'No finite distinct covering with minimum>=8 and moduli 2^a*3^b*5^c, b<=2',
              'unrestricted_exponents': ['a', 'c'], 'anchors': list(ANCHORS),
              'period_by_depth': [base_period(d) for d in range(len(ANCHORS) + 1)],
              'axes_by_period': {str(Q): list(a) for Q, a in AXES.items()},
              'nodes_per_depth': nodes, 'uniform_cuts_per_depth': uniform,
              'weighted_cuts_per_depth': weighted, 'nodes': sum(nodes),
              'uniform_cuts': sum(uniform), 'weighted_cuts': sum(weighted),
              'equality_cuts': equality, 'minimum_scaled_weighted_gap': min_gap,
              'uncut_leaves': 0, 'excludes_every_finite_binary_and_five_exponent': True,
              'proof_events_sha256': digest.hexdigest(),
              'weights_file_sha256': sha256(Path(path).read_bytes()).hexdigest()}
    return result, equality_fixtures


def finite_controls(fixtures):
    checked = 0
    for Q, axes in AXES.items():
        h = 1 if Q == 360 else 2
        for A, C in product(range(3, 6), range(h, h + 3)):
            actual = defaultdict(Fraction)
            for a, b, c in product(range(A + 1), range(3), range(C + 1)):
                n = 2**a * 3**b * 5**c
                if n >= 8:
                    actual[gcd(Q, n)] += Fraction(gcd(Q, n), n)
            for g in range(1, Q + 1):
                if Q % g:
                    continue
                binary = sum(Fraction(1, 2**k) for k in range(A - 2)) if g % 8 == 0 else 1
                five = sum(Fraction(1, 5**k) for k in range(C - h + 1)) if g % axes[2] == 0 else 1
                expected = binary * five - int(g < 8)
                if actual[g] != expected or 4 * actual[g] > resources(Q).get(g, 0):
                    raise RuntimeError('finite geometric coefficient control failed')
                checked += 1
    rng = random.Random(20260929)
    samples = []
    for Q in AXES:
        samples.extend([(Q, (), {}), (Q, (), {x: rng.randrange(8) for x in range(Q)}),
                        (Q, (), {0: 1, Q - 1: 7})])
    samples += fixtures
    individual, grouped, strict = 0, 0, 0
    for Q, previous, weights in samples:
        h = 1 if Q == 360 else 2
        placed = tuple(m for m, a in previous)
        phase_maxima = maxima_of(Q, weights, (g for g in range(1, Q + 1) if Q % g == 0))
        for A, C in ((3, h), (4, h), (3, h + 1), (4, h + 1)):
            L = 2**A * 9 * 5**C
            literal_total = 0
            grouped_weights = defaultdict(Fraction)
            for n in range(8, L + 1):
                if L % n or n in placed:
                    continue
                g = gcd(Q, n)
                literal = max(sum(weights.get(y % Q, 0) for y in range(a, L, n))
                              for a in range(n))
                if literal != L // lcm(Q, n) * phase_maxima[g]:
                    raise RuntimeError('weighted CRT capacity control failed')
                literal_total += literal
                grouped_weights[g] += Fraction(g, n)
                individual += 1
            finite = sum(value * phase_maxima[g] for g, value in grouped_weights.items())
            if Fraction(L, Q) * finite != literal_total:
                raise RuntimeError('finite grouping control failed')
            infinite = Fraction(sum(value * phase_maxima[g]
                                    for g, value in resources(Q, placed).items()), 4)
            if finite > infinite:
                raise RuntimeError('infinite upper bound is too small')
            grouped += 1
            if (Q, previous, weights) in fixtures:
                if not literal_total < L // Q * sum(weights.values()):
                    raise RuntimeError('infinite equality failed to exclude a finite box')
                strict += 1
    return {'finite_coefficient_checks': checked, 'literal_individual_CRT_checks': individual,
            'literal_grouped_capacity_checks': grouped, 'strict_finite_equality_checks': strict}


def transport_controls():
    transported, phase_checks = 0, 0
    for residues, Q, boxes in json.loads((HERE / 'weights.json').read_text())['certificates']:
        if Q != 360:
            continue
        old = decode(Q, boxes)
        new = {x: old[x % Q] for x in range(1800) if x % Q in old}
        moduli = tuple(g for g in range(1, 1801) if 1800 % g == 0)
        old_maxima = maxima_of(360, old, (g for g in range(1, 361) if 360 % g == 0))
        new_maxima = maxima_of(1800, new, moduli)
        for g in moduli:
            if new_maxima[g] != 1800 // lcm(360, g) * old_maxima[gcd(360, g)]:
                raise RuntimeError('periodic phase transport failed')
            phase_checks += 1
        placed = ANCHORS[:len(residues)]
        old_total = sum(v * old_maxima[g] for g, v in resources(360, placed).items())
        new_total = sum(v * new_maxima[g] for g, v in resources(1800, placed).items())
        if sum(new.values()) != 5 * sum(old.values()) or new_total != 5 * old_total:
            raise RuntimeError('periodic demand or full-tail capacity changed')
        transported += 1
    return {'periodic_certificate_lifts': transported, 'periodic_phase_capacity_checks': phase_checks}


def controls():
    symmetry = []
    for moduli in ((8, 9, 10, 12), (5, 10, 25), (8, 15, 25), (8, 10, 25, 30)):
        literal = {normalize(tuple(zip(moduli, phases)))
                   for phases in product(*(range(m) for m in moduli))}
        generated = set()
        def walk(depth, seen, previous):
            if depth == len(moduli):
                generated.add(previous)
                return
            m = moduli[depth]
            for a, following in production.canonical_options(m, seen):
                walk(depth + 1, following, previous + ((m, a),))
        walk(0, {}, ())
        if literal != generated:
            raise RuntimeError('complete small symmetry sets disagree')
        alternate = set()
        def literal_walk(depth, previous):
            if depth == len(moduli):
                alternate.add(previous)
                return
            m = moduli[depth]
            for a in options(m, previous):
                literal_walk(depth + 1, previous + ((m, a),))
        literal_walk(0, ())
        if literal != alternate:
            raise RuntimeError('alternate canonical generator misses a normalized tuple')
        symmetry.append({'moduli': list(moduli), 'raw_tuples': prod(moduli),
                         'canonical_tuples': len(literal)})
    witness = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11))
    Q = 360
    active = set(range(Q))
    positive = 0
    for depth, (m, a) in enumerate(witness, 1):
        active = {x for x in active if x % m != a}
        weights = {x: 1 + x % 7 for x in active}
        resource = resources(Q, tuple(n for n, r in witness[:depth]), minimum=2)
        total = sum(resource[g] * cap for g, cap in maxima_of(Q, weights, resource).items())
        if active and total <= 4 * sum(weights.values()):
            raise RuntimeError('a genuine covering prefix was falsely excluded')
        positive += 1
    if active:
        raise RuntimeError('positive fixture does not cover')
    rejections = 0
    for runner in (production.search, literal_replay):
        try:
            runner(max_nodes=1)
        except production.IncompleteSearch:
            rejections += 1
        else:
            raise RuntimeError('partial search was reported complete')
    for boxes in ([[1, 1, 1, 1], [1, 1, 1, 2]], [[256, 1, 1, 1]], [[1, 1, 1, 0]]):
        try:
            production.decode_boxes(360, boxes)
        except ValueError:
            rejections += 1
        else:
            raise RuntimeError('malformed boxes were accepted')
    for x in (None, 0, 1):
        vector = [0] * 360
        if x is not None:
            vector[x] = 1
        try:
            production.exact_certificate(360, vector, (0,))
        except ValueError:
            rejections += 1
        else:
            raise RuntimeError('zero, covered or insufficient weights were accepted')
    return {'complete_symmetry_controls': symmetry, 'positive_cover_prefixes': positive,
            'malformed_certificate_and_limit_rejections': rejections}


def main():
    start = monotonic()
    result, equalities = literal_replay()
    expected = json.loads((HERE / 'expected.json').read_text())
    if result != expected:
        raise RuntimeError('alternate full manifest and proof-event digest differ')
    print('Full literal replay: every manifest field and ordered proof event agrees.', flush=True)
    report = controls()
    report.update(finite_controls(equalities))
    report.update(transport_controls())
    print(json.dumps(report, indent=2))
    print('FULL AUDIT PASSED: complete canonical coverage, two periods, all finite tails.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
