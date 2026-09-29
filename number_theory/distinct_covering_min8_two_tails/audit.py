"""Full alternate audit: original-child names, CRT boxes, progression sums.

Authored by six-covering-3, researcher; this is not an external review.
No production symmetry, box decoder, resource generator or counter is used.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import gcd, lcm
from pathlib import Path
from time import monotonic
import json
import random
import check as production

Q, AXES, ANCHORS = 360, (8, 9, 5), (8, 9, 10, 12, 15, 18, 20)
HERE = Path(__file__).resolve().parent


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
    # Scan actual candidate phases; normalize the whole original tuple.
    # Prefix canonicality makes the test independent of any count-state map.
    for residue in range(modulus):
        enlarged = previous + ((modulus, residue),)
        if normalize(enlarged) == enlarged:
            yield residue


def resources(placed=(), minimum=8):
    result = {}
    for g in range(1, Q + 1):
        if Q % g:
            continue
        value = Fraction(1)
        if g % 8 == 0:
            value /= 1 - Fraction(1, 2)
        if g % 9 == 0:
            value /= 1 - Fraction(1, 3)
        if g < minimum:
            value -= 1
        if g in placed:
            value -= 1
        scaled = 2 * value
        if scaled.denominator != 1 or scaled < 0:
            raise RuntimeError('invalid alternate resource')
        if scaled:
            result[g] = int(scaled)
    return result


def decode(boxes):
    result = {}
    for box in boxes:
        if len(box) != 4 or any(type(v) is not int for v in box) or box[3] <= 0:
            raise ValueError('bad box')
        coordinates = []
        for mask, axis in zip(box[:3], AXES):
            if not 0 < mask < 2**axis:
                raise ValueError('bad mask')
            coordinates.append(tuple(a for a in range(axis) if mask & 2**a))
        for point in product(*coordinates):
            # Independent Cartesian enumeration and explicit CRT inversion.
            x = sum(a * (Q // axis) * pow(Q // axis, -1, axis)
                    for a, axis in zip(point, AXES)) % Q
            if x in result:
                raise ValueError('overlapping rectangles')
            result[x] = box[3]
    return result


def maxima_of(weights, moduli):
    return {g: max(sum(weights.get(x, 0) for x in range(a, Q, g))
                   for a in range(g)) for g in moduli}


def literal_replay(path=HERE / 'weights.json', max_nodes=10000, seconds=30):
    data = json.loads(Path(path).read_text())
    if data['format_version'] != 1 or data['Q'] != Q or data['axes'] != list(AXES):
        raise ValueError('bad header')
    certificates = {tuple(residues): boxes for residues, boxes in data['certificates']}
    if len(certificates) != len(data['certificates']):
        raise ValueError('duplicate prefixes')
    used = set()
    nodes, uniform, weighted = ([0] * (len(ANCHORS) + 1) for _ in range(3))
    equality, min_gap = 0, None
    digest, start = sha256(), monotonic()
    equality_fixtures = []

    def visit(previous, active):
        nonlocal equality, min_gap
        depth = len(previous)
        residues = tuple(a for m, a in previous)
        if sum(nodes) >= max_nodes or monotonic() - start > seconds:
            raise production.IncompleteSearch('alternate complete audit limit')
        nodes[depth] += 1
        if not active:
            raise RuntimeError('anchor cover invalidates theorem')
        resource = resources(tuple(m for m, a in previous))
        weights = {x: 1 for x in active}
        demand = len(weights)
        maxima = maxima_of(weights, resource)
        total = sum(resource[g] * maxima[g] for g in resource)
        tag = None
        if total <= 2 * demand:
            uniform[depth] += 1
            tag = 'uniform'
        elif residues in certificates:
            weights = decode(certificates[residues])
            if not weights or not set(weights) <= active:
                raise ValueError('weight outside the literal uncovered set')
            demand = sum(weights.values())
            maxima = maxima_of(weights, resource)
            total = sum(resource[g] * maxima[g] for g in resource)
            if total > 2 * demand or maxima.get(Q, 0) <= 0:
                raise ValueError('literal weighted inequality fails')
            weighted[depth] += 1
            used.add(residues)
            tag = 'weighted'
            gap = 2 * demand - total
            min_gap = gap if min_gap is None else min(min_gap, gap)
        if tag:
            if total == 2 * demand:
                equality += 1
                equality_fixtures.append((previous, weights))
            event = [tag, residues, demand, total, sorted(maxima.items())]
            digest.update((json.dumps(event, separators=(',', ':')) + '\n').encode('ascii'))
            return
        if depth == len(ANCHORS):
            raise RuntimeError('literal terminal branch remains open')
        modulus = ANCHORS[depth]
        for residue in options(modulus, previous):
            following = {x for x in active if x % modulus != residue}
            visit(previous + ((modulus, residue),), following)

    visit((), set(range(Q)))
    if used != set(certificates):
        raise ValueError('alternate replay has unused certificates')
    result = {'agent': 'six-covering-3', 'role': 'researcher',
              'claim': 'No finite distinct covering with minimum >=8 and moduli 2^a*3^b*5^c, c<=1',
              'Q': Q, 'axes': list(AXES), 'anchors': list(ANCHORS),
              'nodes_per_depth': nodes, 'uniform_cuts_per_depth': uniform,
              'weighted_cuts_per_depth': weighted, 'nodes': sum(nodes),
              'uniform_cuts': sum(uniform), 'weighted_cuts': sum(weighted),
              'uncut_leaves': 0, 'equality_cuts': equality,
              'minimum_scaled_weighted_gap': min_gap,
              'excludes_every_finite_binary_and_ternary_exponent': True,
              'proof_events_sha256': digest.hexdigest(),
              'weights_file_sha256': sha256(Path(path).read_bytes()).hexdigest()}
    return result, equality_fixtures


def finite_controls(fixtures):
    checked = 0
    for A, B in product(range(3, 6), range(2, 5)):
        actual = defaultdict(Fraction)
        for a, b, c in product(range(A + 1), range(B + 1), (0, 1)):
            n = 2**a * 3**b * 5**c
            if n >= 8:
                actual[gcd(Q, n)] += Fraction(gcd(Q, n), n)
        for g in range(1, Q + 1):
            if Q % g:
                continue
            binary = sum(Fraction(1, 2**k) for k in range(A - 2)) if g % 8 == 0 else 1
            ternary = sum(Fraction(1, 3**k) for k in range(B - 1)) if g % 9 == 0 else 1
            expected = binary * ternary - int(g < 8)
            if actual[g] != expected or 2 * actual[g] > resources().get(g, 0):
                raise RuntimeError('finite geometric coefficient control failed')
            checked += 1
    rng = random.Random(20260929)
    samples = [((), {}), ((), {x: rng.randrange(8) for x in range(Q)}),
               ((), {0: 1, Q - 1: 7})] + fixtures
    individual, grouped, strict = 0, 0, 0
    for previous, weights in samples:
        placed = tuple(m for m, a in previous)
        for A, B in ((3, 2), (4, 2), (3, 3), (4, 3)):
            L = 2**A * 3**B * 5
            literal_total = 0
            grouped_weights = defaultdict(Fraction)
            for n in range(8, L + 1):
                if L % n or n in placed:
                    continue
                g = gcd(Q, n)
                literal = max(sum(weights.get(y % Q, 0) for y in range(a, L, n))
                              for a in range(n))
                phase = max(sum(weights.get(x, 0) for x in range(a, Q, g))
                            for a in range(g))
                if literal != L // lcm(Q, n) * phase:
                    raise RuntimeError('weighted CRT capacity control failed')
                literal_total += literal
                grouped_weights[g] += Fraction(g, n)
                individual += 1
            finite = sum(value * maxima_of(weights, (g,))[g]
                         for g, value in grouped_weights.items())
            if Fraction(L, Q) * finite != literal_total:
                raise RuntimeError('finite grouping control failed')
            infinite = Fraction(sum(value * maxima_of(weights, (g,))[g]
                                    for g, value in resources(placed).items()), 2)
            if finite > infinite:
                raise RuntimeError('infinite upper bound is too small')
            grouped += 1
            if (previous, weights) in fixtures:
                if not literal_total < L // Q * sum(weights.values()):
                    raise RuntimeError('an infinite equality failed to exclude a finite box')
                strict += 1
    return {'finite_coefficient_checks': checked, 'literal_individual_CRT_checks': individual,
            'literal_grouped_capacity_checks': grouped, 'strict_finite_equality_checks': strict}


def controls():
    symmetry = []
    for moduli in ((2, 3, 4), (4, 6, 8), (8, 9, 10, 12), (9, 10, 12)):
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
        symmetry.append({'moduli': list(moduli), 'canonical_tuples': len(literal)})
    witness = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11))
    active = set(range(Q))
    positive = 0
    for depth, (m, a) in enumerate(witness, 1):
        active = {x for x in active if x % m != a}
        weights = {x: 1 + x % 7 for x in active}
        resource = resources(tuple(n for n, r in witness[:depth]), minimum=2)
        total = sum(resource[g] * h for g, h in maxima_of(weights, resource).items())
        if active and total <= 2 * sum(weights.values()):
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
            raise RuntimeError('a partial search was reported complete')
    for boxes in ([[[1, 1, 1, 1], [1, 1, 1, 2]]], [[[256, 1, 1, 1]]], [[[1, 1, 1, 0]]]):
        try:
            production.decode_boxes(boxes[0])
        except ValueError:
            rejections += 1
        else:
            raise RuntimeError('malformed boxes were accepted')
    for x in (None, 0, 1):
        vector = [0] * Q
        if x is not None:
            vector[x] = 1
        try:
            production.exact_certificate(vector, (0,))
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
    print(json.dumps(report, indent=2))
    print('FULL AUDIT PASSED: complete canonical coverage, CRT decoding, weighted finite tails.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
