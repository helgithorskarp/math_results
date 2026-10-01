"""Separate census and literal certificate checker; author six-books-3, researcher.

The default command imports no generator or rational matrix code.
--compare additionally compares complete state sets and every matrix entry.
"""
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
EDGES = list(combinations(range(8), 2))


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def adjacency(mask):
    return [{j for j in range(8) if j != i and
             mask & (1 << EDGES.index(tuple(sorted((i, j)))))} for i in range(8)]


def binary_domain():
    """Decide all 28 edge bits, using remaining degree/future-edge bounds."""
    degrees = [2, 2] + [3] * 6
    future = [[0] * 8 for _ in range(29)]
    for k in range(27, -1, -1):
        future[k] = future[k + 1][:]
        i, j = EDGES[k]
        if (i, j) != (0, 1):
            future[k][i] += 1
            future[k][j] += 1
    out = set()

    def visit(k, mask):
        if any(d < 0 or d > f for d, f in zip(degrees, future[k])):
            return
        if k == 28:
            rows = adjacency(mask)
            if any(rows[i] & rows[j] for i, j in EDGES if j in rows[i]):
                return
            check(mask not in out, 'duplicate binary core')
            out.add(mask)
            return
        visit(k + 1, mask)
        i, j = EDGES[k]
        if (i, j) != (0, 1) and degrees[i] and degrees[j]:
            degrees[i] -= 1
            degrees[j] -= 1
            visit(k + 1, mask | (1 << k))
            degrees[i] += 1
            degrees[j] += 1

    visit(0, 0)
    return out


def orbit_cover(domain, records):
    covered = set()
    for record in records:
        mask = record['F_mask']
        check(type(mask) is int and 0 <= mask < 1 << 28 and mask in domain, 'invalid core representative')
        images = set()
        for tail in permutations(range(2, 8)):
            point = (0, 1) + tail
            inverse = {point[i]: i for i in range(8)}
            bits = [int(bool(mask & (1 << EDGES.index(tuple(sorted((inverse[i], inverse[j])))))))
                    for i, j in EDGES]
            images.add(sum(bit << k for k, bit in enumerate(bits)))
        check(images <= domain and not (images & covered), 'core coverage gap or overlap')
        check(min(images) == mask and len(images) == record['orbit_size'], 'incorrect orbit record')
        covered |= images
    check(covered == domain, 'incomplete core cover')


def full_matrix(mask):
    """Reconstruct the nine retained entries by degree class and F intersections."""
    rows = adjacency(mask)
    check(list(map(len, rows)) == [2, 2] + [3] * 6, 'core degree decoding')
    out = [[0] * 9 for _ in range(9)]
    out[0][0] = 4
    for i in range(8):
        out[i + 1][i + 1] = 5
        out[0][i + 1] = out[i + 1][0] = 0 if i < 2 else 3 - len(rows[i] & {0, 1})
    for i, j in EDGES:
        common = len(rows[i] & rows[j]) + int(i == 0 and j == 1)
        value = (1 if j in rows[i] else 4) - common
        out[i + 1][j + 1] = out[j + 1][i + 1] = value
    return out


def edge_weights(target, capacities):
    """Decide each integer edge weight, including zero, independently."""
    pairs = [(i, j) for i, j in combinations(range(9), 2)
             if target[i] and target[j] and capacities[i][j] > 0]
    future = [[0] * 9 for _ in range(len(pairs) + 1)]
    for k in range(len(pairs) - 1, -1, -1):
        future[k] = future[k + 1][:]
        i, j = pairs[k]
        limit = min(target[i], target[j], capacities[i][j])
        future[k][i] += limit
        future[k][j] += limit
    remaining = target[:]
    chosen = []
    out = []

    def visit(k):
        if any(d < 0 or d > f for d, f in zip(remaining, future[k])):
            return
        if k == len(pairs):
            out.append(tuple(chosen))
            return
        i, j = pairs[k]
        for weight in range(min(remaining[i], remaining[j], capacities[i][j]) + 1):
            remaining[i] -= weight
            remaining[j] -= weight
            if weight:
                chosen.append((i, j, weight))
            visit(k + 1)
            if weight:
                chosen.pop()
            remaining[i] += weight
            remaining[j] += weight

    visit(0)
    check(len(out) == len(set(out)), 'duplicate weighted-edge state')
    return sorted(out)


def matrix_for(capacities, slack, group):
    weights = {(i, j): weight for i, j, weight in slack}
    blocks = [{1 + i for i in group}, {1 + i for i in range(8) if i not in group}]
    return [[capacities[i][j] - (weights.get(tuple(sorted((i, j))), 0) if i != j else 0)
             - sum(int(i in block and j in block) for block in blocks)
             for j in range(9)] for i in range(9)]


def certificate_check(expected, certificates, compare=None):
    check(sha256(encode(certificates)).hexdigest() == expected['negative_vectors_sha256'], 'vector hash')
    domain = binary_domain()
    check(len(domain) == expected['labeled_marked_F'], 'core domain size')
    check(sha256(encode(sorted(domain))).hexdigest() == expected['F_domain_sha256'], 'core domain hash')
    orbit_cover(domain, expected['core_records'])
    check(len(expected['core_records']) == 4 and len(expected['cases']) == 8, 'record coverage')
    pools = {}
    for record in certificates:
        key = (record['F_mask'], record['case'])
        check(key not in pools and record['vectors'], 'duplicate or empty vector pool')
        for vector in record['vectors']:
            check(len(vector) == 9 and all(type(x) is int for x in vector) and any(vector), 'invalid vector')
        pools[key] = record['vectors']
    check(set(pools) == {(r['F_mask'], k) for r in expected['core_records']
                        for k in ['five_five', 'six_four']}, 'incomplete certificate coverage')
    if compare is not None:
        check(compare.core_domain() == domain, 'entry-level core-domain mismatch')
    summaries = []
    for core in expected['core_records']:
        mask = core['F_mask']
        capacities = full_matrix(mask)
        for kind in ['five_five', 'six_four']:
            pool = pools[(mask, kind)]
            # Start with all four-subsets, and quotient interchange only afterwards.
            parts = list(combinations(range(8), 4 if kind == 'five_five' else 5))
            parts = [group for group in parts if kind != 'five_five' or 0 in group]
            digest = sha256()
            count = negative_entries = 0
            cache = {}
            for group in parts:
                target = [2]
                for i in range(8):
                    excess = 1 if kind == 'five_five' else 2 * int(i in group)
                    target.append(2 + int(i in {0, 1}) - excess)
                key = tuple(target)
                if key not in cache:
                    cache[key] = edge_weights(target, capacities)
                slacks = cache[key]
                if compare is not None:
                    check(slacks == compare.weighted_stars(target, capacities), 'entry-level slack-domain mismatch')
                for slack in slacks:
                    actual = [sum(w for a, b, w in slack if i in (a, b)) for i in range(9)]
                    check(actual == target, 'literal slack degrees')
                    matrix = matrix_for(capacities, slack, group)
                    check(all(matrix[i][i] == 4 and sum(matrix[i]) == 16 for i in range(9)), 'Gram sums')
                    if compare is not None:
                        check(matrix == compare.residual(compare.base(mask), slack, group), 'entry-level Gram mismatch')
                    check(any(sum(matrix[i][j] * v[i] * v[j] for i in range(9) for j in range(9)) < 0
                              for v in pool), 'missing negative integer form')
                    digest.update(encode([mask, kind, group, slack, matrix]))
                    count += 1
                    negative_entries += int(any(x < 0 for row in matrix for x in row))
            summaries.append({'F_mask': mask, 'case': kind, 'groups': len(parts), 'states': count,
                              'negative_entry_states': negative_entries, 'state_stream_sha256': digest.hexdigest(),
                              'vectors': len(pool)})
    check(summaries == expected['cases'], 'state summaries or streamed matrices differ')
    check(sum(x['states'] for x in summaries) == expected['states'] == expected['negative_forms'], 'state total')
    check(sum(x['states'] * r['orbit_size'] for r in expected['core_records']
              for x in summaries if x['F_mask'] == r['F_mask']) == expected['labeled_marked_states'], 'multiplicities')
    check(sum(len(pool) for pool in pools.values()) == expected['vectors'], 'vector count')
    check(max(abs(x) for pool in pools.values() for v in pool for x in v) == expected['max_absolute_vector_entry'], 'vector bound')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--compare', action='store_true', help='add full entry-level comparison to the generator')
    args = parser.parse_args()
    compare = None
    if args.compare:
        import generate as compare
    expected = json.loads((HERE / 'expected.json').read_bytes())
    certificates = json.loads((HERE / 'negative_vectors.json').read_bytes())
    certificate_check(expected, certificates, compare)
    print(encode(expected).decode(), end='')
