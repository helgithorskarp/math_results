"""Inclusion-exclusion checker, independent of the target-degree transfer DP."""
from functools import lru_cache
from math import comb
from itertools import product
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

@lru_cache(None)
def unrestricted(n):
    # Coefficients of (4+4X+4Y+3XY)^n.
    if n == 0:
        return {(0, 0): 1}
    out = {}
    for (x, y), v in unrestricted(n-1).items():
        for dx, dy, multiplicity in ((0,0,4), (1,0,4), (0,1,4), (1,1,3)):
            key = x+dx, y+dy
            out[key] = out.get(key, 0) + multiplicity*v
    return out

@lru_cache(None)
def excluded_sum(n, x, y, a, b):
    total = 0
    for i in range(min(a, y)+1):
        for j in range(min(b, x, n-i)+1):
            if a <= b:
                ways = comb(a, i)*comb(b-i, j) if j <= b-i else 0
            else:
                ways = comb(b, j)*comb(a-j, i) if i <= a-j else 0
            total += (-1)**(i+j)*ways*unrestricted(n-i-j).get((x-j, y-i), 0)
    need(total >= 0, 'negative inclusion-exclusion coefficient')
    return total

def count(degrees, blue):
    n = len(degrees)
    answer = 0
    for x in range(n+1):
        a = sum(d < (n-1-x if blue else x) for d in degrees)
        for y in range(n+1):
            b = sum(d < (n-1-y if blue else y) for d in degrees)
            answer += excluded_sum(n, x, y, a, b)
    return answer

def literal(degrees, blue, rows=2):
    n = len(degrees)
    answer = 0
    for columns in product(range(15), repeat=n):
        D = [sum((c >> w) & 1 for c in columns) for w in range(rows)]
        answer += all(c != (15 ^ (1 << w)) or
                      not (degrees[v] < (n-1-D[w] if blue else D[w]))
                      for v, c in enumerate(columns) for w in range(rows))
    return answer

def verify(keys, counts):
    need(len(keys) == len(counts), 'row count')
    for i, (key, row) in enumerate(zip(keys, counts)):
        need(row[0] == i, 'row identity')
        d = key['degrees']
        need(key['n'] == len(d) and d == sorted(d), 'degree key')
        for blue in (False, True):
            need(count(tuple(d), blue) == row[1+blue], 'independent count mismatch')
            need(0 <= row[1+blue] <= 15**len(d), 'count bound')
    direct = 0
    # All degree multisets on up to three vertices, including non-graphical ones.
    from itertools import combinations_with_replacement
    for n in range(1, 4):
        for d in combinations_with_replacement(range(n), n):
            for blue in (False, True):
                need(count(d, blue) == literal(d, blue), 'literal count mismatch')
                direct += 15**n
    return dict(status='INCLUSION_EXCLUSION_AND_LITERAL_VERIFIED', keys=len(keys),
                exact_counts=2*len(keys), literal_indexed_assignments=direct,
                trust='Same author; different combinatorial decomposition, not an external review')

if __name__ == '__main__':
    import argparse
    from pathlib import Path
    p = argparse.ArgumentParser(); p.add_argument('keys'); p.add_argument('counts'); p.add_argument('out')
    a = p.parse_args()
    result = verify(json.loads(Path(a.keys).read_text()),
                    [list(map(int, s.split())) for s in Path(a.counts).read_text().splitlines()])
    Path(a.out).write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps(result, sort_keys=True))
