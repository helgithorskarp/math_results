"""Exclude minimum >=8 on 2^a*3^b*5^c with a<=4, b,c unrestricted.

Author: six-covering-3, researcher. Python >=3.10, standard library.
The marked-prefix framework and weighted criterion build on the sources
attributed in proof.md. Verification imports no orbit code or solver.
"""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from time import monotonic
import argparse
import json

ANCHORS = (8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40, 45)
AXES = {720: (16, 9, 5), 3600: (16, 9, 25)}
HERE = Path(__file__).resolve().parent


class IncompleteSearch(RuntimeError):
    """An operational cutoff never establishes an exclusion."""


def period(depth):
    if not 0 <= depth <= len(ANCHORS):
        raise ValueError('invalid depth')
    return 720 if depth <= 9 else 3600


def coefficients(Q, placed=()):
    """Eight times the remaining infinite ternary/five capacity."""
    if Q not in AXES:
        raise ValueError('unexpected base period')
    h = 1 if Q == 720 else 2
    result = {2**i * 3**j * 5**k:
              (3 if j == 2 else 2) * (5 if k == h else 4)
              for i in range(5) for j in range(3) for k in range(h + 1)}
    for n in (1, 2, 3, 4, 5, 6):
        result[n] -= 8
    if len(placed) != len(set(placed)) or any(n < 8 or Q % n for n in placed):
        raise ValueError('invalid placed moduli')
    for n in placed:
        result[n] -= 8
    if any(value < 0 for value in result.values()):
        raise ValueError('negative resource coefficient')
    return {g: value for g, value in sorted(result.items()) if value}


@lru_cache(None)
def factor_levels(n):
    result = []
    for p in (2, 3, 5):
        powers, power = [], 1
        while n % p == 0:
            powers.append(power)
            power *= p
            n //= p
        if powers:
            result.append((p, tuple(powers)))
    if n != 1:
        raise ValueError('unexpected prime')
    return tuple(result)


def canonical_options(modulus, seen):
    """Prime-tree first-appearance naming, extending to every future depth."""
    for residue in range(modulus):
        following, valid = seen.copy(), True
        for p, powers in factor_levels(modulus):
            for power in powers:
                key = p, power, residue % power
                child = residue // power % p
                count = seen.get(key, 0)
                if child >= min(p, count + 1):
                    valid = False
                    break
                following[key] = max(count, child + 1)
            if not valid:
                break
        if valid:
            yield residue, following


@lru_cache(None)
def class_mask(Q, modulus, residue):
    if Q % modulus or not 0 <= residue < modulus:
        raise ValueError('invalid class')
    return sum(1 << x for x in range(residue, Q, modulus))


def lift(U, Q, R):
    if R % Q or U < 0 or U >> Q:
        raise ValueError('invalid periodic lift')
    return sum(U << offset for offset in range(0, R, Q))


@lru_cache(None)
def coordinate_mask(Q, axis, mask):
    """Literal remainders, with no CRT or orbit declaration."""
    return sum(1 << x for x in range(Q) if mask >> (x % axis) & 1)


def decode_boxes(Q, boxes):
    if Q not in AXES:
        raise ValueError('unexpected period')
    axes = AXES[Q]
    vector = [0] * Q
    for box in boxes:
        if len(box) != 4 or any(type(v) is not int for v in box):
            raise ValueError('four integer box entries required')
        masks, weight = box[:3], box[3]
        if weight <= 0 or any(not 0 < mask < 1 << axis for mask, axis in zip(masks, axes)):
            raise ValueError('invalid Cartesian box')
        active = (1 << Q) - 1
        for axis, mask in zip(axes, masks):
            active &= coordinate_mask(Q, axis, mask)
        while active:
            bit = active & -active
            x = bit.bit_length() - 1
            if vector[x]:
                raise ValueError('overlapping boxes')
            vector[x] = weight
            active ^= bit
    return vector


def capacity(Q, vector, resource):
    if len(vector) != Q or any(type(w) is not int or w < 0 for w in vector):
        raise ValueError('invalid point weights')
    maxima = {}
    points = [(x, weight) for x, weight in enumerate(vector) if weight]
    for g in resource:
        if Q % g or type(resource[g]) is not int or resource[g] <= 0:
            raise ValueError('invalid resource')
        phases = [0] * g
        for x, weight in points:
            phases[x % g] += weight
        maxima[g] = max(phases)
    return sum(resource[g] * value for g, value in maxima.items()), maxima


def exact_certificate(Q, vector, residues):
    if not 1 <= len(residues) <= len(ANCHORS) or Q != period(len(residues)):
        raise ValueError('invalid certificate period or prefix')
    if len(vector) != Q or any(type(w) is not int or w < 0 for w in vector):
        raise ValueError('invalid vector')
    pairs = tuple(zip(ANCHORS, residues))
    if any(weight and any(x % m == a for m, a in pairs)
           for x, weight in enumerate(vector)):
        raise ValueError('weight on an already covered point')
    demand = sum(vector)
    if demand <= 0:
        raise ValueError('positive demand required')
    resource = coefficients(Q, ANCHORS[:len(residues)])
    total, maxima = capacity(Q, vector, resource)
    if total > 8 * demand:
        raise ValueError('exact weighted inequality fails')
    if resource.get(Q, 0) <= 0 or maxima.get(Q, 0) <= 0:
        raise ValueError('a positive omitted tail is required for equality')
    return demand, total, maxima


def event_bytes(tag, Q, residues, demand, total, maxima):
    row = [tag, Q, residues, demand, total, sorted(maxima.items())]
    return (json.dumps(row, separators=(',', ':')) + '\n').encode('ascii')


def read_certificates(path):
    data = json.loads(Path(path).read_text())
    if data['format_version'] != 1 or data['axes_by_period'] != {str(Q): list(a) for Q, a in AXES.items()}:
        raise ValueError('unexpected certificate parameters')
    result = {}
    for residues, Q, boxes in data['certificates']:
        key = tuple(residues)
        if key in result or not 1 <= len(key) <= len(ANCHORS) or Q != period(len(key)):
            raise ValueError('duplicate or invalid prefix')
        if any(type(a) is not int or not 0 <= a < m for a, m in zip(key, ANCHORS)):
            raise ValueError('invalid phase')
        result[key] = Q, boxes
    return result


def search(path=HERE / 'weights.json', max_nodes=10000, seconds=30):
    certificates = read_certificates(path)
    used = set()
    nodes, uniform, weighted = ([0] * (len(ANCHORS) + 1) for _ in range(3))
    equalities, minimum_gap = 0, None
    digest, start = sha256(), monotonic()

    def visit(depth, U, seen, residues):
        nonlocal equalities, minimum_gap
        if sum(nodes) >= max_nodes or monotonic() - start > seconds:
            raise IncompleteSearch('complete verification node/time cap')
        nodes[depth] += 1
        Q = period(depth)
        if not U or U >> Q:
            raise RuntimeError('empty or invalid residual state')
        vector = [int(bool(U >> x & 1)) for x in range(Q)]
        demand = sum(vector)
        total, maxima = capacity(Q, vector, coefficients(Q, ANCHORS[:depth]))
        tag = None
        if total <= 8 * demand:
            uniform[depth] += 1
            tag = 'uniform'
        elif residues in certificates:
            certificate_period, boxes = certificates[residues]
            if certificate_period != Q:
                raise ValueError('certificate base changed')
            demand, total, maxima = exact_certificate(Q, decode_boxes(Q, boxes), residues)
            weighted[depth] += 1
            used.add(residues)
            tag = 'weighted'
            gap = 8 * demand - total
            minimum_gap = gap if minimum_gap is None else min(minimum_gap, gap)
        if tag:
            equalities += total == 8 * demand
            digest.update(event_bytes(tag, Q, residues, demand, total, maxima))
            return
        if depth == len(ANCHORS):
            raise RuntimeError(f'uncertified terminal prefix: {residues}')
        following_period = period(depth + 1)
        base = U if Q == following_period else lift(U, Q, following_period)
        modulus = ANCHORS[depth]
        for residue, following in canonical_options(modulus, seen):
            visit(depth + 1, base & ~class_mask(following_period, modulus, residue),
                  following, residues + (residue,))

    visit(0, (1 << period(0)) - 1, {}, ())
    if used != set(certificates):
        raise ValueError('unused certificates: stored and verified frontier disagree')
    return {'agent': 'six-covering-3', 'role': 'researcher',
            'claim': 'No finite distinct covering with minimum>=8 and moduli 2^a*3^b*5^c, a<=4',
            'unrestricted_exponents': ['b', 'c'], 'anchors': list(ANCHORS),
            'period_by_depth': [period(d) for d in range(len(ANCHORS) + 1)],
            'axes_by_period': {str(Q): list(a) for Q, a in AXES.items()},
            'nodes_per_depth': nodes, 'uniform_cuts_per_depth': uniform,
            'weighted_cuts_per_depth': weighted, 'nodes': sum(nodes),
            'uniform_cuts': sum(uniform), 'weighted_cuts': sum(weighted),
            'equality_cuts': equalities, 'minimum_scaled_weighted_gap': minimum_gap,
            'uncut_leaves': 0, 'excludes_every_finite_ternary_and_five_exponent': True,
            'proof_events_sha256': digest.hexdigest(),
            'weights_file_sha256': sha256(Path(path).read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--weights', type=Path, default=HERE / 'weights.json')
    parser.add_argument('--check', type=Path)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    start = monotonic()
    result = search(args.weights)
    if args.check is not None and result != json.loads(args.check.read_text()):
        raise RuntimeError('complete output differs from expected manifest')
    if args.write is not None:
        args.write.write_text(json.dumps(result, indent=2) + '\n')
    print(f'{result["nodes"]} nodes; {result["uniform_cuts"]} uniform and '
          f'{result["weighted_cuts"]} weighted cuts; zero open leaves; '
          f'{result["equality_cuts"]} valid equality cuts.')
    print('PROVED: minimum >=8 is impossible on 2^a*3^b*5^c with a<=4, for all finite b,c.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
