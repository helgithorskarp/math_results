"""CNF for lifting a quotient, with a proved three-hole affine normalization."""
from functools import lru_cache
from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool

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
    lines, planes = geometry()
    formula, pool = CNF(), IDPool(start_from=126)
    for line in lines:
        formula.append([-v for v in line])
    for plane in planes:
        formula.extend(CardEnc.atmost(lits=list(plane), bound=16, vpool=pool,
                                     encoding=EncType.seqcounter).clauses)
    return formula


def generate(word):
    if len(word) != 25 or any(c not in "01234" for c in word):
        raise ValueError("invalid fiber weights")
    weights = tuple(map(int, word))
    base = base_formula()
    formula = CNF(from_clauses=base.clauses)
    pool = IDPool(start_from=base.nv+1)
    for i, n in enumerate(weights):
        formula.extend(CardEnc.equals(lits=list(range(5*i+1, 5*i+6)), bound=n,
                                     vpool=pool, encoding=EncType.seqcounter).clauses)
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
