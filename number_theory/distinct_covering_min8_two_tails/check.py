"""A solver-free complete exclusion for 2^a 3^b 5^c, c <= 1, minimum >= 8.

Actual author: six-covering-3, researcher. Python >= 3.10; standard library.
See proof.md for the unbounded-exponent reduction and source attribution.
"""
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
from time import monotonic
import argparse
import json

Q = 360
AXES = (8, 9, 5)
ANCHORS = (8, 9, 10, 12, 15, 18, 20)
HERE = Path(__file__).resolve().parent


class IncompleteSearch(RuntimeError):
    """Operational limits are never mathematical exclusions."""


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


def coefficients(placed=()):
    """Twice the entire infinite geometric capacity, less used resources."""
    result = {}
    for i in range(4):
        for j in range(3):
            for c in (0, 1):
                g = 2**i * 3**j * 5**c
                result[g] = (2 if i == 3 else 1) * (3 if j == 2 else 2)
    for n in (1, 2, 3, 4, 5, 6):
        result[n] -= 2
    if len(placed) != len(set(placed)) or any(n < 8 or Q % n for n in placed):
        raise ValueError('invalid placed moduli')
    for n in placed:
        result[n] -= 2
    if any(value < 0 for value in result.values()):
        raise ValueError('negative resource coefficient')
    return {g: value for g, value in sorted(result.items()) if value}


def canonical_options(modulus, seen):
    """Name each child in first-appearance order at each prime-tree node."""
    for residue in range(modulus):
        following = seen.copy()
        valid = True
        for p, powers in factor_levels(modulus):
            for power in powers:
                key = p, power, residue % power
                digit = residue // power % p
                count = seen.get(key, 0)
                if digit >= min(p, count + 1):
                    valid = False
                    break
                following[key] = max(count, digit + 1)
            if not valid:
                break
        if valid:
            yield residue, following


@lru_cache(None)
def class_mask(modulus, residue):
    if Q % modulus or not 0 <= residue < modulus:
        raise ValueError('invalid class')
    return sum(1 << x for x in range(residue, Q, modulus))


def decode_boxes(boxes):
    """Literal definition-level decoding; no stabilizer or orbit routine."""
    vector = [0] * Q
    for box in boxes:
        if len(box) != 4 or any(type(value) is not int for value in box):
            raise ValueError('box must contain four integers')
        masks, weight = box[:3], box[3]
        if weight <= 0 or any(not 0 < mask < 1 << axis for mask, axis in zip(masks, AXES)):
            raise ValueError('invalid Cartesian box')
        points = [x for x in range(Q)
                  if all(mask >> (x % axis) & 1 for mask, axis in zip(masks, AXES))]
        if not points:
            raise ValueError('empty box')
        for x in points:
            if vector[x]:
                raise ValueError('overlapping boxes')
            vector[x] = weight
    return vector


def capacity(vector, resource):
    """Exact maximum phase weight for every charged divisor of Q."""
    if len(vector) != Q or any(type(value) is not int or value < 0 for value in vector):
        raise ValueError('invalid point weights')
    maxima = {}
    for g in resource:
        if Q % g or type(resource[g]) is not int or resource[g] <= 0:
            raise ValueError('invalid resource')
        phases = [0] * g
        for x, weight in enumerate(vector):
            phases[x % g] += weight
        maxima[g] = max(phases)
    return sum(resource[g] * value for g, value in maxima.items()), maxima


def exact_certificate(vector, residues):
    placed = tuple(zip(ANCHORS, residues))
    if not 1 <= len(residues) <= len(ANCHORS):
        raise ValueError('invalid prefix length')
    if len(vector) != Q or any(type(w) is not int or w < 0 for w in vector):
        raise ValueError('invalid vector')
    if any(weight and any(x % m == a for m, a in placed)
           for x, weight in enumerate(vector)):
        raise ValueError('weight lies on an already covered point')
    demand = sum(vector)
    if demand <= 0:
        raise ValueError('positive demand required')
    resource = coefficients(ANCHORS[:len(residues)])
    total, maxima = capacity(vector, resource)
    if total > 2 * demand:
        raise ValueError('weighted inequality fails')
    if resource.get(Q, 0) <= 0 or maxima.get(Q, 0) <= 0:
        raise ValueError('positive infinite tail needed for equality exclusion')
    return demand, total, maxima


def event_bytes(tag, residues, demand, total, maxima):
    event = [tag, residues, demand, total, sorted(maxima.items())]
    return (json.dumps(event, separators=(',', ':')) + '\n').encode('ascii')


def read_certificates(path):
    data = json.loads(Path(path).read_text())
    if data['format_version'] != 1 or data['Q'] != Q or data['axes'] != list(AXES):
        raise ValueError('unexpected certificate parameters')
    result = {}
    for residues, boxes in data['certificates']:
        key = tuple(residues)
        if key in result or not 1 <= len(key) <= len(ANCHORS):
            raise ValueError('duplicate or invalid certificate prefix')
        if any(type(a) is not int or not 0 <= a < m for a, m in zip(key, ANCHORS)):
            raise ValueError('invalid phase')
        result[key] = boxes
    return result


def search(path=HERE / 'weights.json', max_nodes=10000, seconds=30):
    certificates = read_certificates(path)
    used = set()
    nodes, uniform, weighted = ([0] * (len(ANCHORS) + 1) for _ in range(3))
    equality = 0
    min_weight_gap = None
    digest, start = sha256(), monotonic()

    def visit(depth, U, seen, residues):
        nonlocal equality, min_weight_gap
        if sum(nodes) >= max_nodes or monotonic() - start > seconds:
            raise IncompleteSearch('complete verification reached a node/time limit')
        nodes[depth] += 1
        if not U:
            raise RuntimeError('an anchor prefix covers: the proposed theorem fails')
        vector = [int(bool(U >> x & 1)) for x in range(Q)]
        demand = sum(vector)
        total, maxima = capacity(vector, coefficients(ANCHORS[:depth]))
        tag = None
        if total <= 2 * demand:
            uniform[depth] += 1
            tag = 'uniform'
        elif residues in certificates:
            vector = decode_boxes(certificates[residues])
            demand, total, maxima = exact_certificate(vector, residues)
            weighted[depth] += 1
            used.add(residues)
            tag = 'weighted'
            gap = 2 * demand - total
            min_weight_gap = gap if min_weight_gap is None else min(min_weight_gap, gap)
        if tag:
            equality += total == 2 * demand
            digest.update(event_bytes(tag, residues, demand, total, maxima))
            return
        if depth == len(ANCHORS):
            raise RuntimeError(f'uncertified terminal branch: {residues}')
        m = ANCHORS[depth]
        for a, following in canonical_options(m, seen):
            visit(depth + 1, U & ~class_mask(m, a), following, residues + (a,))

    visit(0, (1 << Q) - 1, {}, ())
    if used != set(certificates):
        raise ValueError('unused certificate: proof frontier and data disagree')
    return {'agent': 'six-covering-3', 'role': 'researcher',
            'claim': 'No finite distinct covering with minimum >=8 and moduli 2^a*3^b*5^c, c<=1',
            'Q': Q, 'axes': list(AXES), 'anchors': list(ANCHORS),
            'nodes_per_depth': nodes, 'uniform_cuts_per_depth': uniform,
            'weighted_cuts_per_depth': weighted, 'nodes': sum(nodes),
            'uniform_cuts': sum(uniform), 'weighted_cuts': sum(weighted),
            'uncut_leaves': 0, 'equality_cuts': equality,
            'minimum_scaled_weighted_gap': min_weight_gap,
            'excludes_every_finite_binary_and_ternary_exponent': True,
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
          f'{result["weighted_cuts"]} weighted cuts; zero uncut leaves; '
          f'{result["equality_cuts"]} valid equality cuts.')
    print('PROVED: minimum >=8 is impossible for every finite 2^a*3^b*5^c tower with c<=1.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
