"""Exact generation. Author six-books-3, researcher; Python 3.11 stdlib."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
from math import gcd, lcm
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
PAIRS = list(combinations(range(8), 2))
INDEX = {edge: k for k, edge in enumerate(PAIRS)}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def decode(mask):
    rows = [set() for _ in range(8)]
    for k, (i, j) in enumerate(PAIRS):
        if mask >> k & 1:
            rows[i].add(j)
            rows[j].add(i)
    return rows


def core_domain():
    """Fix each vertex's entire later neighbor set, with prescribed degrees."""
    remaining = [2, 2] + [3] * 6
    rows = [set() for _ in range(8)]
    out = set()

    def visit(i, mask):
        if i == 8:
            require(not any(remaining), 'nonzero terminal degree')
            require(mask not in out, 'duplicate core')
            out.add(mask)
            return
        choices = [j for j in range(i + 1, 8)
                   if remaining[j] and (i, j) != (0, 1) and not (rows[i] & rows[j])]
        if remaining[i] > len(choices):
            return
        for neighbors in combinations(choices, remaining[i]):
            # A triangle wholly within this newly chosen star is also forbidden.
            if any(j in rows[k] for j, k in combinations(neighbors, 2)):
                continue
            amount = remaining[i]
            remaining[i] = 0
            new_mask = mask
            for j in neighbors:
                remaining[j] -= 1
                rows[i].add(j)
                rows[j].add(i)
                new_mask |= 1 << INDEX[(i, j)]
            if all(remaining[j] <= 7 - i - int(j > i) for j in range(i + 1, 8)):
                visit(i + 1, new_mask)
            for j in neighbors:
                rows[i].remove(j)
                rows[j].remove(i)
                remaining[j] += 1
            remaining[i] = amount

    visit(0, 0)
    for mask in out:
        rows = decode(mask)
        require(list(map(len, rows)) == [2, 2] + [3] * 6, 'core degrees')
        require(1 not in rows[0], 'marked edge')
        require(all(not (rows[i] & rows[j]) for i, j in PAIRS if j in rows[i]),
                'core triangle')
    return out


def orbit(mask):
    edges = [edge for k, edge in enumerate(PAIRS) if mask >> k & 1]
    return {sum(1 << INDEX[tuple(sorted((point[i], point[j])))] for i, j in edges)
            for tail in permutations(range(2, 8)) for point in [(0, 1) + tail]}


def core_records(domain):
    todo = set(domain)
    records = []
    while todo:
        mask = min(todo)
        covered = orbit(mask)
        require(covered <= todo and mask == min(covered), 'orbit overlap or missing core')
        records.append({'F_mask': mask, 'orbit_size': len(covered)})
        todo -= covered
    return records


def base(mask):
    f = decode(mask)
    local = [set(), {2, 3}] + [{2 + j for j in row} for row in f]
    local[2].add(1)
    local[3].add(1)
    h = list(map(len, local))
    require(h == [0, 2] + [3] * 8, 'local degrees')
    return [[h[i] + 2 if i == j else
             h[i] + h[j] - (5 if j in local[i] else 2) - len(local[i] & local[j])
             for j in range(10)] for i in range(10)]


def weighted_stars(degrees, capacities):
    remaining = list(degrees)
    edges = []

    def visit():
        i = next((i for i, d in enumerate(remaining) if d), None)
        if i is None:
            yield tuple(edges)
            return
        amount = remaining[i]
        neighbors = [j for j in range(i + 1, 9) if remaining[j] and capacities[i][j] > 0]
        if sum(min(remaining[j], capacities[i][j]) for j in neighbors) < amount:
            return
        remaining[i] = 0

        def distribute(k, left):
            if k == len(neighbors):
                if left == 0:
                    yield from visit()
                return
            j = neighbors[k]
            future = sum(min(remaining[v], capacities[i][v]) for v in neighbors[k + 1:])
            for weight in range(max(0, left - future), min(left, remaining[j], capacities[i][j]) + 1):
                remaining[j] -= weight
                if weight:
                    edges.append((i, j, weight))
                yield from distribute(k + 1, left - weight)
                if weight:
                    edges.pop()
                remaining[j] += weight

        yield from distribute(0, amount)
        remaining[i] = amount

    out = list(visit())
    require(len(out) == len(set(out)), 'duplicate slack graph')
    return sorted(out)


def groups(kind):
    if kind == 'five_five':
        return [(0,) + tail for tail in combinations(range(1, 8), 3)]
    return list(combinations(range(8), 5))


def degrees(kind, group):
    return [2] + [int(i < 2) + (1 if kind == 'five_five' else 0 if i in group else 2)
                  for i in range(8)]


def residual(full, edges, group):
    matrix = [row[1:] for row in full[1:]]
    for i, j, weight in edges:
        matrix[i][j] -= weight
        matrix[j][i] -= weight
    for i in range(8):
        for j in range(8):
            if (i in group) == (j in group):
                matrix[i + 1][j + 1] -= 1
    require(all(matrix[i][i] == 4 and sum(matrix[i]) == 16 for i in range(9)),
            'residual diagonal or row sum')
    return matrix


def quadratic(matrix, vector):
    return sum(matrix[i][j] * vector[i] * vector[j] for i in range(9) for j in range(9))


def primitive(vector):
    scale = lcm(*(x.denominator for x in vector))
    out = [int(x * scale) for x in vector]
    divisor = gcd(*out)
    require(divisor > 0, 'zero vector')
    out = [x // divisor for x in out]
    if next(x for x in out if x) < 0:
        out = [-x for x in out]
    return out


def negative_vector(original):
    """Fraction congruence constructs a witness; literal integers certify it."""
    a = [[Fraction(x) for x in row] for row in original]
    columns = [[Fraction(i == j) for i in range(9)] for j in range(9)]
    for k in range(9):
        pivot = a[k][k]
        if pivot < 0:
            out = primitive(columns[k])
            require(quadratic(original, out) < 0, 'invalid negative pivot witness')
            return out
        if pivot == 0:
            j = next((j for j in range(k + 1, 9) if a[k][j]), None)
            if j is not None:
                cross = a[k][j]
                multiple = -(1 if cross > 0 else -1) * (int(abs(a[j][j]) / (2 * abs(cross))) + 1)
                out = primitive([multiple * x + y for x, y in zip(columns[k], columns[j])])
                require(quadratic(original, out) < 0, 'invalid zero pivot witness')
                return out
            continue
        multipliers = {j: a[k][j] / pivot for j in range(k + 1, 9)}
        for j, multiplier in multipliers.items():
            columns[j] = [x - multiplier * y for x, y in zip(columns[j], columns[k])]
        for i in range(k + 1, 9):
            for j in range(i, 9):
                a[i][j] -= a[k][i] * multipliers[j]
                a[j][i] = a[i][j]
    raise RuntimeError('unexpected positive semidefinite survivor')


def run():
    domain = core_domain()
    records = core_records(domain)
    expected = {'agent': 'six-books-3', 'role': 'researcher',
                'labeled_marked_F': len(domain), 'F_domain_sha256': sha256(encode(sorted(domain))).hexdigest(),
                'core_records': records, 'cases': []}
    certificates = []
    for record in records:
        full = base(record['F_mask'])
        capacities = [row[1:] for row in full[1:]]
        require(all(x >= 0 for row in capacities for x in row), 'negative full capacity')
        for kind in ['five_five', 'six_four']:
            digest = sha256()
            count = negative_entries = 0
            pool = []
            for group in groups(kind):
                target = degrees(kind, group)
                for edges in weighted_stars(target, capacities):
                    actual = [0] * 9
                    for i, j, weight in edges:
                        actual[i] += weight
                        actual[j] += weight
                    require(actual == target, 'slack degrees')
                    matrix = residual(full, edges, group)
                    digest.update(encode([record['F_mask'], kind, group, edges, matrix]))
                    count += 1
                    negative_entries += int(any(x < 0 for row in matrix for x in row))
                    if not any(quadratic(matrix, vector) < 0 for vector in pool):
                        pool.append(negative_vector(matrix))
            expected['cases'].append({'F_mask': record['F_mask'], 'case': kind, 'groups': len(groups(kind)),
                                      'states': count, 'negative_entry_states': negative_entries,
                                      'state_stream_sha256': digest.hexdigest(), 'vectors': len(pool)})
            certificates.append({'F_mask': record['F_mask'], 'case': kind, 'vectors': pool})
    expected['states'] = sum(x['states'] for x in expected['cases'])
    expected['labeled_marked_states'] = sum(x['states'] * record['orbit_size']
                                           for record in records for x in expected['cases']
                                           if x['F_mask'] == record['F_mask'])
    expected['negative_forms'] = expected['states']
    expected['vectors'] = sum(len(x['vectors']) for x in certificates)
    expected['max_absolute_vector_entry'] = max(abs(z) for x in certificates for v in x['vectors'] for z in v)
    certificate_bytes = encode(certificates)
    expected['negative_vectors_sha256'] = sha256(certificate_bytes).hexdigest()
    return encode(expected), certificate_bytes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='regenerate the two compact evidence files')
    args = parser.parse_args()
    expected, vectors = run()
    for name, data in [('expected.json', expected), ('negative_vectors.json', vectors)]:
        if args.write:
            (HERE / name).write_bytes(data)
        else:
            require((HERE / name).read_bytes() == data, 'regeneration mismatch: ' + name)
    print(expected.decode(), end='')
