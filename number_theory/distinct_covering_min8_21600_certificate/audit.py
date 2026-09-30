"""Full-period audit with original labels, CRT inversion and literal classes.

Author: six-covering-3, researcher. This self-audit is not external review.
Every visited prefix is checked on all 21600 integers. Resource coefficients,
bitsets, the canonical generator and decoder of check.py are not used in this
replay. check.py is imported only for comparison and validation controls.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import gcd, lcm, prod
from pathlib import Path
from time import monotonic
import argparse
import json
import random
import check as production

N, SCALE = 21600, 30
ANCHORS = (8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30)
AXES = {720: (16, 9, 5), 3600: (16, 9, 25)}
DIVISORS = tuple(n for n in range(8, N + 1) if N % n == 0)
HERE = Path(__file__).resolve().parent


class IncompleteAudit(RuntimeError):
    """A truncated audit never proves an exclusion."""


def base_period(depth):
    return 720 if depth < 10 else 3600


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


@lru_cache(None)
def resources(Q, placed=(), minimum=8):
    result = defaultdict(Fraction)
    for n in range(minimum, N + 1):
        if N % n == 0 and n not in placed:
            g = gcd(Q, n)
            result[g] += Fraction(g, n)
    scaled = {g: SCALE * value for g, value in sorted(result.items())}
    if any(value.denominator != 1 for value in scaled.values()):
        raise ValueError('nonintegral finite divisor grouping')
    return {g: int(value) for g, value in scaled.items()}


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


def progression_maximum(values, modulus, largest=None):
    """Literal phase scan; early exit only at the exact pointwise upper bound."""
    if len(values) % modulus:
        raise ValueError('modulus does not divide period')
    if largest is None:
        largest = max(values)
    upper = len(values) // modulus * largest
    if modulus == len(values) or not largest:
        return largest
    best = 0
    for a in range(modulus):
        best = max(best, sum(values[a::modulus]))
        if best == upper:
            break
    return best


def literal_capacity(Q, weights, placed, minimum=8):
    """Compute every actual n-class maximum directly on period N."""
    base = [weights.get(x, 0) for x in range(Q)]
    values = [weights.get(x % Q, 0) for x in range(N)]
    largest = max(values)
    individual = {}
    eligible = DIVISORS if minimum == 8 else tuple(n for n in range(minimum, N+1) if N % n == 0)
    for n in eligible:
        if n not in placed:
            individual[n] = progression_maximum(values, n, largest)
    resource = resources(Q, placed, minimum)
    maxima = {g: max(sum(base[a::g]) for a in range(g)) for g in resource}
    for n, value in individual.items():
        if value != N // lcm(Q, n) * maxima[gcd(Q, n)]:
            raise RuntimeError('individual full-period capacity and CRT grouping disagree')
    total = sum(individual.values())
    scaled = sum(resource[g] * maxima[g] for g in resource)
    if Fraction(N, Q * SCALE) * scaled != total:
        raise RuntimeError('full-period total and exact rational grouping disagree')
    return sum(values), total, sum(base), scaled, maxima, individual


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
    minimum_gap = None
    digest, full_digest, start = sha256(), sha256(), monotonic()
    individual_checks = 0

    def visit(previous):
        nonlocal minimum_gap, individual_checks
        if sum(nodes) >= max_nodes or monotonic() - start > seconds:
            raise IncompleteAudit(f'INCOMPLETE after {sum(nodes)} nodes in {monotonic()-start:.3f}s')
        depth = len(previous)
        Q = base_period(depth)
        residues = tuple(a for m, a in previous)
        nodes[depth] += 1
        active = {x for x in range(Q) if all(x % m != a for m, a in previous)}
        if not active:
            raise RuntimeError('anchors alone cover: claimed exclusion fails')
        placed = tuple(m for m, a in previous)
        weights = {x: 1 for x in active}
        D, T, demand, total, maxima, individual = literal_capacity(Q, weights, placed)
        individual_checks += len(individual)
        full_event = ['uniform-check', residues, D, T, sorted(individual.items())]
        full_digest.update((json.dumps(full_event, separators=(',', ':'))+'\n').encode('ascii'))
        tag = None
        if T < D:
            uniform[depth] += 1
            tag = 'uniform'
        elif residues in certificates:
            certificate_period, boxes = certificates[residues]
            if certificate_period != Q:
                raise ValueError('period mismatch')
            weights = decode(Q, boxes)
            if not weights or not set(weights) <= active:
                raise ValueError('weight outside the literal uncovered set')
            D, T, demand, total, maxima, individual = literal_capacity(Q, weights, placed)
            individual_checks += len(individual)
            if T >= D:
                raise ValueError('literal strict weighted inequality fails')
            weighted[depth] += 1
            used.add(residues)
            tag = 'weighted'
            gap = SCALE * demand - total
            minimum_gap = gap if minimum_gap is None else min(minimum_gap, gap)
            full_event = ['weighted-check', residues, D, T, sorted(individual.items())]
            full_digest.update((json.dumps(full_event, separators=(',', ':'))+'\n').encode('ascii'))
        if tag:
            event = [tag, Q, residues, demand, total, sorted(maxima.items())]
            digest.update((json.dumps(event, separators=(',', ':'))+'\n').encode('ascii'))
            return
        if depth == len(ANCHORS):
            raise RuntimeError('literal terminal branch remains open')
        for residue in options(ANCHORS[depth], previous):
            visit(previous + ((ANCHORS[depth], residue),))

    visit(())
    if used != set(certificates):
        raise ValueError('alternate replay has unused certificates')
    result = {'agent': 'six-covering-3', 'role': 'researcher',
              'claim': 'No distinct covering with minimum>=8 and every modulus dividing 21600',
              'N': N, 'maximum_exponents': [5, 3, 2], 'denominator': SCALE,
              'anchors': list(ANCHORS),
              'period_by_depth': [base_period(d) for d in range(len(ANCHORS) + 1)],
              'axes_by_period': {str(Q): list(a) for Q, a in AXES.items()},
              'nodes_per_depth': nodes, 'uniform_cuts_per_depth': uniform,
              'weighted_cuts_per_depth': weighted, 'nodes': sum(nodes),
              'uniform_cuts': sum(uniform), 'weighted_cuts': sum(weighted),
              'equality_cuts': 0, 'minimum_scaled_weighted_gap': minimum_gap,
              'uncut_leaves': 0, 'all_unused_divisors_charged': True,
              'proof_events_sha256': digest.hexdigest(),
              'weights_file_sha256': sha256(Path(path).read_bytes()).hexdigest()}
    details = {'literal_period': N, 'eligible_divisors': len(DIVISORS),
               'literal_individual_capacity_checks': individual_checks,
               'all_visited_nodes_and_cuts_sha256': full_digest.hexdigest()}
    return result, details


def controls():
    symmetry = []
    for moduli in ((8, 9, 10, 12), (5, 10, 25), (8, 15, 25),
                   (8, 10, 25, 30), (8, 16, 24), (9, 18, 36)):
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
            for a in options(moduli[depth], previous):
                literal_walk(depth + 1, previous + ((moduli[depth], a),))
        literal_walk(0, ())
        if literal != alternate:
            raise RuntimeError('alternate generator misses a normalized tuple')
        symmetry.append({'moduli': list(moduli), 'raw_tuples': prod(moduli),
                         'canonical_tuples': len(literal)})
    coefficient_checks = 0
    for d in range(len(ANCHORS) + 1):
        Q = base_period(d)
        if resources(Q, ANCHORS[:d]) != production.coefficients(Q, ANCHORS[:d]):
            raise RuntimeError('literal finite coefficients disagree with closed formula')
        coefficient_checks += len(resources(Q, ANCHORS[:d]))
    witness = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11))
    active, positive = set(range(720)), 0
    for depth, (m, a) in enumerate(witness, 1):
        active = {x for x in active if x % m != a}
        weights = {x: 1 + x % 7 for x in active}
        D, T, *_ = literal_capacity(720, weights, tuple(n for n, a in witness[:depth]), minimum=2)
        if active and T < D:
            raise RuntimeError('genuine covering prefix falsely excluded')
        positive += 1
    if active:
        raise RuntimeError('positive fixture does not cover')
    rejected = 0
    for runner, exception in ((production.search, production.IncompleteSearch),
                              (literal_replay, IncompleteAudit)):
        try:
            runner(max_nodes=1)
        except exception:
            rejected += 1
        else:
            raise RuntimeError('partial search reported complete')
    for decoder in (production.decode_boxes, decode):
        for boxes in ([[1, 1, 1, 1], [1, 1, 1, 2]], [[65536, 1, 1, 1]], [[1, 1, 1, 0]]):
            try:
                decoder(720, boxes)
            except ValueError:
                rejected += 1
            else:
                raise RuntimeError('malformed boxes accepted')
    for x in (None, 0, 1):
        vector = [0] * 720
        if x is not None:
            vector[x] = 1
        try:
            production.exact_certificate(720, vector, (0,))
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('zero, covered or insufficient weights accepted')
    rng = random.Random(20260930)
    bounds = 0
    for length in (12, 60, 120):
        for values in ([0]*length, [1]*length, [rng.randrange(8) for _ in range(length)]):
            for n in range(1, length + 1):
                if length % n == 0:
                    expected = max(sum(values[a::n]) for a in range(n))
                    if progression_maximum(values, n) != expected:
                        raise RuntimeError('exact upper-bound early exit changes a maximum')
                    bounds += 1
    return {'complete_symmetry_controls': symmetry, 'finite_coefficient_checks': coefficient_checks,
            'positive_cover_prefixes': positive, 'malformed_certificate_and_limit_rejections': rejected,
            'literal_maximum_early_exit_controls': bounds}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile-nodes', type=int)
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    start = monotonic()
    if args.profile_nodes is not None:
        try:
            literal_replay(max_nodes=args.profile_nodes)
        except IncompleteAudit as exc:
            print(exc)
            print('Profiling only: no exclusion asserted.')
            return
        raise RuntimeError('profile exceeded complete domain')
    result, details = literal_replay()
    expected = json.loads((HERE / 'expected.json').read_text())
    if result != expected:
        raise RuntimeError('alternate full manifest and proof-event digest differ')
    print('Full period 21600 replay: every manifest field and ordered cut agrees.', flush=True)
    details.update(controls())
    if args.check is not None and details != json.loads(args.check.read_text()):
        raise RuntimeError('full-period audit details differ')
    if args.write is not None:
        args.write.write_text(json.dumps(details, indent=2)+'\n')
    print(json.dumps(details, indent=2))
    print('FULL AUDIT PASSED: all root branches and every actual unused divisor.')
    print(f'Elapsed seconds: {monotonic()-start:.3f}')


if __name__ == '__main__':
    main()
