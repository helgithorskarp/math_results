"""Independent exact validation of every geometric premise in the W4 CNF.

No producer code or SAT library is imported. The source is reconstructed from
five literal intervals and a direct middle-coordinate adjacency predicate.
"""
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from check_rup import read_cnf

INTERVALS = [(1, 2), (2, 10), (4, 14), (8, 16), (16, 17)]
VERTICES = [(a, b) for a in range(1, 18) for b in range(a+1, 18)
            if any(l <= a < b <= r for l, r in INTERVALS)]
N = len(VERTICES)


def source_edge(a, b):
    if type(a) is not int or type(b) is not int or not 0 <= a < N or not 0 <= b < N:
        raise ValueError('invalid source endpoints')
    return VERTICES[a][1] == VERTICES[b][0] or VERTICES[b][1] == VERTICES[a][0]


def eq(a, b, n=N):
    if type(a) is not int or type(b) is not int or not 0 <= a < n or not 0 <= b < n or a == b:
        raise ValueError('invalid equality endpoints')
    a, b = min(a, b), max(a, b)
    return a*(2*n-a-1)//2 + b-a


def canonical(clause):
    return tuple(sorted(set(clause)))


def geometric(record, n=N, edge=source_edge):
    """Translate a witnessed necessary plane lemma into one Boolean clause."""
    kind = record['kind']
    if kind == 'wheel':
        center, rim = record['center'], record['cycle']
        labels = [center] + rim
        if len(rim) < 3 or len(rim) % 2 != 1 or len(set(labels)) != len(labels):
            raise ValueError('invalid odd wheel')
        expected = {tuple(sorted((center, x))) for x in rim}
        expected |= {tuple(sorted((rim[i], rim[(i+1) % len(rim)]))) for i in range(len(rim))}
        clause = []
    elif kind == 'k23':
        left, right = record['left'], record['right']
        labels = left + right
        if len(left) != 2 or len(right) != 3 or len(set(labels)) != 5:
            raise ValueError('invalid K23')
        expected = {tuple(sorted((a, b))) for a in left for b in right}
        clause = [eq(*left, n)] + [eq(a, b, n) for a, b in combinations(right, 2)]
    else:
        raise ValueError('unknown geometric lemma')
    if any(type(x) is not int or not 0 <= x < n for x in labels):
        raise ValueError('invalid quotient label')
    found = set()
    for c, d, a, b in record['witnesses']:
        if any(type(x) is not int or not 0 <= x < n for x in (c, d, a, b)):
            raise ValueError('invalid witness label')
        if c >= d or (c, d) not in expected or (c, d) in found:
            raise ValueError('invalid witnessed quotient edge')
        found.add((c, d))
        if not edge(a, b):
            raise ValueError('witness is not a source edge')
        for x, y in ((c, a), (d, b)):
            if x != y:
                clause.append(-eq(x, y, n))
    if found != expected:
        raise ValueError('incomplete edge witnesses')
    return canonical(clause)


def verify(work):
    work = Path(work)
    nvars, actual = read_cnf(work/'instance.cnf')
    if nvars != N*(N-1)//2:
        raise ValueError('wrong variable set')
    data = json.loads((work/'geometric.json').read_text())
    position = 0

    def accept(clause):
        nonlocal position
        if position >= len(actual) or canonical(clause) != canonical(actual[position]):
            raise ValueError(f'CNF differs from validated premise at clause {position+1}')
        position += 1

    for a, b, c in combinations(range(N), 3):
        x, y, z = eq(a, b), eq(a, c), eq(b, c)
        for clause in ((-x, -y, z), (-x, -z, y), (-y, -z, x)):
            accept(clause)
    edges = [(a, b) for a, b in combinations(range(N), 2) if source_edge(a, b)]
    for a, b in edges:
        accept((-eq(a, b),))
    neighbors = [{j for j in range(N) if source_edge(i, j)} for i in range(N)]
    original = []
    for a, b in combinations(range(N), 2):
        for c, d, e in combinations(sorted(neighbors[a] & neighbors[b]), 3):
            accept((eq(a, b), eq(c, d), eq(c, e), eq(d, e)))
            original.append([a, b, c, d, e])
    if original != data['original_k23']:
        raise ValueError('original K23 manifest mismatch')
    counts = {'k23': 0, 'wheel': 0}
    for record in data['learned']:
        accept(geometric(record))
        counts[record['kind']] += 1
    if position != len(actual):
        raise ValueError('unjustified additional clauses')
    source = json.dumps({'vertices': VERTICES, 'edges': edges}, separators=(',', ':')).encode()
    return {'status': 'ALL_GEOMETRIC_PREMISES_VERIFIED', 'source_vertices': N,
            'source_edges': len(edges), 'source_sha256': hashlib.sha256(source).hexdigest(),
            'variables': nvars, 'clauses': position, 'original_k23': len(original),
            'learned': counts, 'cnf_sha256': hashlib.sha256((work/'instance.cnf').read_bytes()).hexdigest(),
            'witness_sha256': hashlib.sha256((work/'geometric.json').read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('work', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.work), sort_keys=True))
