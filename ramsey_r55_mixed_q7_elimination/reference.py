"""Definition-level grounder, independent of encode.py.

Grounds all four/five vertex subsets of the 19-vertex graph, substitutes
fixed edges, then forbids every disjoint pair of possible red fours.
"""
from itertools import combinations


def literal_formula(record):
    n = record[0]-63
    red = set()
    position = 0
    for j in range(n):
        for i in range(j):
            if ((record[1+position//6]-63) >> (5-position%6)) & 1:
                red.add((i+4,j+4))
            position += 1
    red.update(combinations(range(4),2))
    free = {(w,4+v):1+n*w+v for w in range(4) for v in range(n)}
    def guard(S, color):
        result = set()
        for uv in combinations(S,2):
            if uv in free:
                result.add(free[uv] if color else -free[uv])
            elif int(uv in red) != color:
                return None
        return result
    clauses = set()
    for size,color in ((5,1),(4,0)):
        for vertices in combinations(range(n+4),size):
            g = guard(vertices,color)
            if g is not None:
                clauses.add(tuple(sorted(-x for x in g)))
    possible = []
    for vertices in combinations(range(n+4),4):
        g = guard(vertices,1)
        if g is not None:
            possible.append((frozenset(vertices),g))
    for (s,g),(t,h) in combinations(possible,2):
        if s.isdisjoint(t):
            clauses.add(tuple(sorted(-x for x in g|h)))
    return sorted(clauses,key=lambda c:(len(c),c))
