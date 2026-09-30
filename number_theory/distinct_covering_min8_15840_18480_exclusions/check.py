"""Standard-library exact checker for a compact complete exclusion tree.

Branch equivalence uses first-appearance normalization of original prime
digits. The independent SQLite audit instead checks complete coordinate
permutations. Solver output and the Cartesian orbit constructor are unused.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import gcd, lcm, prod
from pathlib import Path
from time import monotonic


@lru_cache(None)
def powers(n):
    result = []
    p = 2
    while p * p <= n:
        if n % p == 0:
            q = 1
            while n % p == 0:
                n //= p
                q *= p
            result.append((p, q))
        p += 1
    if n > 1:
        result.append((n, n))
    return tuple(result)


@lru_cache(None)
def normalize(A):
    names, answer = {}, []
    for m, a in A:
        coordinates = []
        for p, P in powers(m):
            power, encoded = 1, 0
            while power < P:
                labels = names.setdefault((p, power, a % power), {})
                digit = a // power % p
                if digit not in labels:
                    labels[digit] = len(labels)
                encoded += labels[digit] * power
                power *= p
            coordinates.append((P, encoded))
        value = sum(v * (m // P) * pow(m // P, -1, P)
                    for P, v in coordinates) % m
        answer.append((m, value))
    return tuple(answer)


def decode(L, boxes):
    periods = tuple(P for p, P in powers(L))
    coefficients = tuple(L // P * pow(L // P, -1, P) for P in periods)
    if prod(periods) != L:
        raise ValueError('Invalid factorization')
    weights = [0] * L
    for box in boxes:
        if len(box) != len(periods) + 1 or type(box[-1]) is not int or box[-1] <= 0:
            raise ValueError('Invalid positive weight box')
        axes = []
        for mask, P in zip(box[:-1], periods):
            if type(mask) is not int or not 0 < mask < 1 << P:
                raise ValueError('Invalid literal coordinate mask')
            axes.append([a for a in range(P) if mask >> a & 1])
        for coordinates in product(*axes):
            x = sum(a * c for a, c in zip(coordinates, coefficients)) % L
            if weights[x]:
                raise ValueError('Overlapping weight boxes')
            weights[x] = box[-1]
    return weights


def population(W, m):
    values = [0] * m
    for x, w in enumerate(W):
        if w:
            values[x % m] += w
    return values


def pair_capacity(W, m, n):
    left, right, meet = population(W, m), population(W, n), population(W, lcm(m, n))
    ell, g = lcm(m, n), gcd(m, n)
    q = n // g
    inverse = pow(m // g, -1, q)
    largest, digest = 0, sha256()
    for a in range(m):
        for b in range(n):
            overlap = meet[(a + m * ((b - a) // g * inverse % q)) % ell] if (b - a) % g == 0 else 0
            value = left[a] + right[b] - overlap
            largest = max(largest, value)
            digest.update((str(value) + ',').encode('ascii'))
    return largest, digest.hexdigest()


def prove(certificate, target=15840):
    if certificate['schema'] != 2 or certificate['L'] != target or certificate['minimum'] != 8:
        raise ValueError('Wrong certificate theorem')
    if certificate['root_anchors'] != [[8, 0]]:
        raise ValueError('A global exactly-eight proof must start at (8,0)')
    L = target
    permitted = [m for m in range(8, L + 1) if L % m == 0]
    vectors, nodes = certificate['vectors'], certificate['nodes']
    if not nodes:
        raise ValueError('Empty proof')
    visited, used_vectors, events, pair_events = set(), set(), [], []
    counts = Counter()
    branch_phases, support_points, boxes, pair_phases = 0, 0, 0, 0

    def visit(i, A, U):
        nonlocal branch_phases, support_points, boxes, pair_phases
        if type(i) is not int or not 0 <= i < len(nodes) or i in visited:
            raise ValueError('Missing, cyclic or shared proof node')
        visited.add(i)
        node = nodes[i]
        if not node or type(node[0]) is not int or node[0] not in (0, 1, 2):
            raise ValueError('Open or invalid proof node')
        if not U:
            raise ValueError('Covering prefix cannot be excluded')
        B = [m for m in permitted if m not in dict(A)]
        if node[0] == 2:
            if len(node) != 3:
                raise ValueError('Invalid branch record')
            _, m, children = node
            if type(m) is not int or m not in B or not children:
                raise ValueError('Invalid branch modulus or empty children')
            phases = []
            for child in children:
                if len(child) != 2 or type(child[0]) is not int or not 0 <= child[0] < m:
                    raise ValueError('Invalid child phase')
                phases.append(child[0])
            if len(set(phases)) != len(phases):
                raise ValueError('Duplicate child phase')
            gains = population([int(x in U) for x in range(L)], m)
            normalized = {normalize(A + ((m, a),)) for a in phases}
            if any(not gains[a] for a in phases):
                raise ValueError('Zero-gain child')
            for a in range(m):
                branch_phases += 1
                if gains[a] and normalize(A + ((m, a),)) not in normalized:
                    raise ValueError('Unrepresented positive-gain phase')
            counts['expanded'] += 1
            events.append([i, 'expanded', m, phases])
            for a, j in children:
                visit(j, A + ((m, a),), {x for x in U if x % m != a})
            return
        if node[0] == 0:
            if len(node) != 3:
                raise ValueError('Invalid uniform record')
            D = len(U)
            W = [int(x in U) for x in range(L)]
            C = sum(max(population(W, m)) for m in B)
            stored = tuple(node[1:])
            counts['uniform'] += 1
        else:
            if len(node) != 5:
                raise ValueError('Invalid weighted record')
            _, vi, stored_D, stored_C, pairs = node
            if type(vi) is not int or not 0 <= vi < len(vectors):
                raise ValueError('Invalid weight vector reference')
            used_vectors.add(vi)
            W = decode(L, vectors[vi])
            if any(w and x not in U for x, w in enumerate(W)):
                raise ValueError('Covered weight support')
            D = sum(W)
            support_points += sum(bool(w) for w in W)
            boxes += len(vectors[vi])
            used = set()
            for pair in pairs:
                if len(pair) != 2 or any(type(m) is not int or m not in B or m in used for m in pair) or pair[0] == pair[1]:
                    raise ValueError('Invalid resource partition')
                used.update(pair)
            C = sum(max(population(W, m)) for m in B if m not in used)
            for m, n in pairs:
                cap, digest = pair_capacity(W, m, n)
                C += cap
                pair_phases += m * n
                pair_events.append([i, m, n, digest])
            stored = (stored_D, stored_C)
            counts['weighted'] += 1
            counts['grouped_weighted'] += bool(pairs)
        if any(type(v) is not int for v in stored) or (D, C) != stored or D <= C:
            raise ValueError('False exact strict cut')
        events.append([i, 'uniform' if node[0] == 0 else 'weighted', D, C])

    visit(0, ((8, 0),), {x for x in range(L) if x % 8})
    if visited != set(range(len(nodes))) or used_vectors != set(range(len(vectors))):
        raise ValueError('Unused proof material')
    return {'agent': 'six-covering-2', 'role': 'researcher', 'status': 'COMPLETE GLOBAL LCM EXCLUSION',
            'L': L, 'minimum': 8, 'root_anchors': [[8, 0]], 'nodes': len(nodes),
            'node_counts': dict(sorted(counts.items())), 'vectors': len(vectors),
            'boxes_checked': boxes, 'positive_weight_points_checked': support_points,
            'literal_branch_phases_checked': branch_phases, 'pair_phase_tuples_checked': pair_phases,
            'events_sha256': sha256(json.dumps(sorted(events), separators=(',', ':')).encode('ascii')).hexdigest(),
            'pair_events_sha256': sha256(json.dumps(sorted(pair_events), separators=(',', ':')).encode('ascii')).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path, nargs='?')
    parser.add_argument('--target', type=int, choices=(15840,18480), default=15840)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--write', type=Path)
    args = parser.parse_args()
    args.certificate = args.certificate or Path(__file__).with_name(f'certificate-{args.target}.json')
    args.expected = args.expected or Path(__file__).with_name(f'expected-{args.target}.json')
    start = monotonic()
    result = prove(json.loads(args.certificate.read_text()), args.target)
    if not args.write and result != json.loads(args.expected.read_text()):
        raise ValueError('Manifest mismatch')
    if args.write:
        args.write.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    print(f'Elapsed seconds: {monotonic() - start:.3f}')
