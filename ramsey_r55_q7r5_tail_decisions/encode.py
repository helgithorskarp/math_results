"""Exact 23-vertex residual formulas for the 640 complete q7,r5 tasks."""
import argparse
import hashlib
from itertools import combinations
from pathlib import Path

CATALOG_SHA256 = '53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1'
PAIRS = list(combinations(range(23), 2))
FREE = [p for p in PAIRS if not (p[1] < 15 or 15 <= p[0] < p[1] < 19 or 19 <= p[0] < p[1])]
VARIABLE = {p: i + 1 for i, p in enumerate(FREE)}

def catalog(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise ValueError('Catalog SHA-256 mismatch')
    lines = raw.decode('ascii').splitlines()
    if len(lines) != 640 or any(len(x) != 19 for x in lines):
        raise ValueError('Catalog dimensions')
    return lines

def decode(line):
    vals = [ord(c) - 63 for c in line]
    if len(vals) != 19 or vals[0] != 15 or any(not 0 <= v < 64 for v in vals):
        raise ValueError('Expected a graph6 graph of order 15')
    bits = [(v >> k) & 1 for v in vals[1:] for k in range(5, -1, -1)]
    if any(bits[105:]):
        raise ValueError('Nonzero graph6 padding')
    return {(i, j): bits[j * (j - 1) // 2 + i] for j in range(1, 15) for i in range(j)}

def fixed(core):
    ans = dict(core)
    for block in (range(15, 19), range(19, 23)):
        for pair in combinations(block, 2):
            ans[pair] = 0
    return ans

def physical_clauses(core):
    known = fixed(core)
    for size, color in ((4, 1), (5, 0)):
        for vertices in combinations(range(23), size):
            pairs = list(combinations(vertices, 2))
            if any(p in known and known[p] != color for p in pairs):
                continue
            yield [(-1 if color else 1) * VARIABLE[p] for p in pairs if p not in known]

def lex_leq(left, right, first):
    if not left or len(left) != len(right):
        raise ValueError('Comparator word lengths')
    rows = []
    prev = None
    nextvar = first
    for i, (x, y) in enumerate(zip(left, right)):
        rows.append(([] if prev is None else [-prev]) + [-x, y])
        if i + 1 == len(left):
            break
        z = nextvar
        nextvar += 1
        if prev is not None:
            rows.append([-z, prev])
        rows.extend([[-z, -x, y], [-z, x, -y]])
        rows.extend([([] if prev is None else [-prev]) + [-x, -y, z],
                     ([] if prev is None else [-prev]) + [x, y, z]])
        prev = z
    return nextvar, rows

def comparisons():
    ans = []
    for block in (range(15, 19), range(19, 23)):
        for u, v in zip(block, list(block)[1:]):
            ans.append(([VARIABLE[i, u] for i in range(14, -1, -1)],
                        [VARIABLE[i, v] for i in range(14, -1, -1)]))
    ans.append(([VARIABLE[i, u] for u in range(18, 14, -1) for i in range(14, -1, -1)],
                [VARIABLE[i, u] for u in range(22, 18, -1) for i in range(14, -1, -1)]))
    return ans

def ordering():
    rows = []
    first = 137
    for left, right in comparisons():
        first, extra = lex_leq(left, right, first)
        rows.extend(extra)
    if first != 280 or len(rows) != 858:
        raise ValueError('Ordering dimensions')
    return rows

def formula(core):
    return list(physical_clauses(core)) + ordering()

def dimacs(core):
    rows = formula(core)
    return (f'p cnf 279 {len(rows)}\n' + ''.join(' '.join(map(str, row)) + ' 0\n' for row in rows)).encode('ascii')

def graph(core, word):
    if not isinstance(word, str) or len(word) != 136 or set(word) - {'0', '1'}:
        raise ValueError('Expected exactly 136 physical edge bits')
    ans = fixed(core)
    ans.update({p: int(word[i]) for i, p in enumerate(FREE)})
    return ans

def normalize(g):
    def signature(v):
        return sum(g[tuple(sorted((i, v)))] << i for i in range(15))
    blocks = [sorted(block, key=signature) for block in (range(15, 19), range(19, 23))]
    blocks.sort(key=lambda block: sum(signature(v) << (15 * j) for j, v in enumerate(block)))
    permutation = list(range(15)) + blocks[0] + blocks[1]
    out = {(i, j): g[tuple(sorted((permutation[i], permutation[j])))] for i, j in PAIRS}
    return out, permutation

def assignment(g):
    ans = {v: g[p] for p, v in VARIABLE.items()}
    first = 137
    for left, right in comparisons():
        equal = True
        for x, y in zip(left[:-1], right[:-1]):
            equal = equal and ans[x] == ans[y]
            ans[first] = int(equal)
            first += 1
    return ans

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--catalog', required=True)
    p.add_argument('--index', type=int, required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    if not 0 <= a.index < 640:
        raise ValueError('Core index')
    raw = dimacs(decode(catalog(a.catalog)[a.index]))
    with Path(a.output).open('xb') as f:
        f.write(raw)
    print(hashlib.sha256(raw).hexdigest())
