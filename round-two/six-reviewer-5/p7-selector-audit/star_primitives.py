"""Explicit reuse of this reviewer's previously audited fixture/row primitives.

Only these seven pure functions are extracted from reviewer source5da38609,
three-hub-budget-audit/audit.py. No old inventory routine or author engine
is imported. The generic23 census remains an explicit mathematical import.
"""
from collections import Counter
from itertools import combinations, permutations
import hashlib
import json

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(value):
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()).hexdigest()

def canonical(n, edges):
    return min(tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in edges))
               for p in permutations(range(n)))

def positive_compositions(total, length):
    if length == 1:
        if total > 0:
            yield (total,)
    elif length > 1:
        for first in range(1, total-length+2):
            for tail in positive_compositions(total-first, length-1):
                yield (first,)+tail

def unit_types(fixtures):
    require(len(fixtures) == 23, 'complete credited generic fixture input')
    records, classes, seen = [], set(), set()
    for index, quads in enumerate(fixtures):
        require(len(quads) == 20 and all(len(q) == len(set(q)) == 4 and
                all(type(p) is int and 0 <= p < 17 for p in q) for q in quads), 'literal quadruple domain')
        key = tuple(sorted(tuple(sorted(q)) for q in quads))
        require(key not in seen, 'duplicate fixture'); seen.add(key)
        pairs = Counter(p for q in quads for p in combinations(sorted(q), 2))
        degrees = Counter(p for q in quads for p in q)
        require(len(pairs) == 120 and max(pairs.values()) == 1, 'repeated fixture pair')
        high = sorted(p for p in range(17) if degrees[p] < 5)
        require(all(degrees[p] <= 5 for p in range(17)), 'fixture point cap')
        require(not any(degrees[a] == degrees[b] == 5 and (a, b) not in pairs
                        for a, b in combinations(range(17), 2)), 'low-low fixture leave')
        if sorted(5-degrees[p] for p in high) != [1]*5:
            continue
        edges = tuple((a, b) for a, b in combinations(range(5), 2)
                      if tuple(sorted((high[a], high[b]))) not in pairs)
        require(len(edges) == 4, 'unit high-leave count')
        form = canonical(5, edges); classes.add(form)
        records.append({'fixture': index, 'high': high, 'edges': edges, 'canonical': form})
    require([r['fixture'] for r in records] == [11, 15, 16, 17, 19, 20, 21, 22]
            and len(classes) == 4, 'complete eight unit fixtures/four graph classes')
    check_charge(classes)
    return classes, records

def check_charge(classes):
    for edges in classes:
        for marks in combinations(range(5), 2):
            require(sum(bool(set(e)&set(marks)) for e in edges) >= 2,
                    'unit two-hub charge below two')

def flags(delta, edges, marks):
    degree = Counter(v for e in edges for v in e)
    h = len(delta)
    return tuple(int(v >= 0 and degree[v] == 0 and
                     (h == 5 and delta[v] == 1 or h == 4 and delta[v] == 2)) for v in marks)
