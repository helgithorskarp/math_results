"""Generate a universal physical five-set cover for the declared Cayley group.

The complete enumeration and DPLL construction are producer logic only.
The independent checker verifies the emitted literal cover without them.
"""
from collections import Counter
from itertools import combinations
import json


def multiply(u, v):
    i, j, k, l = u % 5, u//5, v % 5, v//5
    return (i+pow(2, j, 5)*k) % 5+5*((j+l) % 8)


def inverse(u):
    i, j = u % 5, u//5
    return (-pow(pow(2, j, 5), -1, 5)*i) % 5+5*((-j) % 8)


def model():
    parts = sorted({tuple(sorted({u, inverse(u)})) for u in range(1, 40)})
    if len(parts) != 20:
        raise ValueError('twenty inverse classes required')
    index = {u: k for k, part in enumerate(parts) for u in part}
    edges = [[None if u == v else index[multiply(inverse(u), v)]
              for v in range(40)] for u in range(40)]
    return parts, edges


def build():
    parts, edges = model()
    witnesses = {}
    for rest in combinations(range(1, 40), 4):
        q = (0, *rest)
        support = 0
        for u, v in combinations(q, 2):
            support |= 1 << edges[u][v]
        witnesses.setdefault(support, q)
    minimal = []
    for support in sorted(witnesses, key=lambda m: (m.bit_count(), m)):
        if not any(t & support == t for t in minimal):
            minimal.append(support)
    selected = set()

    def search(clauses):
        for mask, color, original in clauses:
            if mask == 0:
                selected.add(witnesses[original])
                return
        scores = Counter()
        for mask, color, original in clauses:
            weight = 1 << (10-mask.bit_count())
            while mask:
                bit = mask & -mask
                mask ^= bit
                scores[bit.bit_length()-1] += weight
        if not scores:
            raise ValueError('a Ramsey core survived')
        var = max(scores, key=lambda v: (scores[v], -v))
        bit = 1 << var
        for value in (0, 1):
            child = []
            for mask, color, original in clauses:
                if mask & bit:
                    if color != value:
                        continue
                    mask ^= bit
                child.append((mask, color, original))
            search(child)

    search([(m, c, m) for m in minimal for c in (0, 1)])
    return {'schema': 1, 'five_sets': sorted(selected)}


if __name__ == '__main__':
    print(json.dumps(build(), separators=(',', ':')))
