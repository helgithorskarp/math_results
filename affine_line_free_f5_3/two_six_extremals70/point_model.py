"""Direct 125-variable CNF with explicit clauses for every fiber cardinality."""
from functools import lru_cache
from itertools import combinations, product

from pysat.formula import CNF

POINTS = tuple(product(range(5), repeat=3))


@lru_cache(None)
def geometry():
    index = {p: i+1 for i, p in enumerate(POINTS)}
    normals = [p for p in POINTS if any(p) and next(c for c in p if c) == 1]
    lines = sorted({tuple(sorted(index[tuple((a+t*b) % 5 for a, b in zip(p, v))]
                                for t in range(5)))
                    for p in POINTS for v in normals})
    planes = [tuple(i+1 for i, p in enumerate(POINTS)
                    if sum(a*b for a, b in zip(p, v)) % 5 == t)
              for v in normals for t in range(5)]
    if len(lines) != 775 or len(planes) != 155:
        raise RuntimeError("incorrect affine geometry")
    return lines, planes


@lru_cache(None)
def base_formula():
    lines, _ = geometry()
    formula = CNF()
    for line in lines:
        formula.append([-v for v in line])
    return formula


def fiber_clauses(fiber, n):
    """Exactly n of five variables, expressed by forbidden subsets."""
    if len(fiber) != 5 or n not in range(5):
        raise ValueError("invalid five-point fiber cardinality")
    return ([[-v for v in selected] for selected in combinations(fiber, n+1)]
            + [list(absent) for absent in combinations(fiber, 6-n)])


def generate(word):
    if len(word) != 25 or any(c not in "01234" for c in word):
        raise ValueError("invalid fiber weights")
    weights = tuple(map(int, word))
    base = base_formula()
    formula = CNF(from_clauses=base.clauses)
    for i, n in enumerate(weights):
        fiber = list(range(5*i+1, 5*i+6))
        formula.extend(fiber_clauses(fiber, n))
    full = [i for i, n in enumerate(weights) if n == 4]
    gauge = next((abc for abc in combinations(full, 3)
                  if ((abc[1]//5-abc[0]//5)*(abc[2] % 5-abc[0] % 5)
                      -(abc[2]//5-abc[0]//5)*(abc[1] % 5-abc[0] % 5)) % 5), None)
    if gauge is None:
        raise ValueError("no noncollinear triple of four-point fibers")
    for i in gauge:
        formula.append([-(5*i+1)])
    return formula, gauge


def decode_and_check(word, model):
    selected = {v for v in model if 0 < v <= 125}
    lines, planes = geometry()
    if any(set(line) <= selected for line in lines):
        raise ValueError("decoded set contains an affine line")
    if any(sum(v in selected for v in plane) > 16 for plane in planes):
        raise ValueError("decoded set violates the plane cap")
    if any(sum(v in selected for v in range(5*i+1, 5*i+6)) != int(n)
           for i, n in enumerate(word)):
        raise ValueError("decoded fiber weights disagree")
    return sorted(v-1 for v in selected)
