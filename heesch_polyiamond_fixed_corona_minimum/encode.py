"""Exact necessary CNF for the fixed-corona positive-angle-surplus family.

The 354-cell halo and 131 poses come from the sibling hexapillar reproduction.
The formula relaxes global topology. See proof.md for the implication from
admissible five-corona shapes to satisfying assignments.
"""
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

import sys
PUBLIC = Path(__file__).resolve().parents[1]/"heesch_polyiamond_hexapillar"
sys.path.insert(0, str(PUBLIC))


def move(t, p):
    a, b, c, d = p["matrix"]; x, y = p["translation"]
    return tuple(sorted((a*u+b*v+x, c*u+d*v+y) for u, v in t))

from check import cell, mesh, star, DIRECTIONS


def wedges(v):
    x, y = v
    return [tuple(sorted((v, (x+DIRECTIONS[j][0], y+DIRECTIONS[j][1]),
                          (x+DIRECTIONS[(j+1)%6][0], y+DIRECTIONS[(j+1)%6][1]))))
            for j in range(6)]


def link_clauses(local, tip, pocket):
    """All local occupancy patterns, with exact angle indicators."""
    result = []; active = [j for j, v in enumerate(local) if v is not None]
    for assignment in itertools.product((False, True), repeat=len(active)):
        bits = [False]*6
        for j, value in zip(active, assignment):
            bits[j] = value
        opposite = [-local[j] if bits[j] else local[j] for j in active]
        transitions = sum(bits[j] != bits[(j+1)%6] for j in range(6))
        if transitions > 2:
            result.append(opposite)
            continue
        count = sum(bits)
        result.append([*opposite, tip if count == 1 else -tip])
        result.append([*opposite, pocket if count == 5 else -pocket])
    return result


def build(limit):
    original = {cell(t) for t in json.loads((PUBLIC/'tile.json').read_text())['triangles']}
    placements = json.loads((PUBLIC/'coronas.json').read_text())['placements']
    _, vertices, _ = mesh(original)
    cells = sorted(original | {t for v in vertices for t in star(v)})
    variables = {t: j for j, t in enumerate(cells, 1)}
    clauses = set()
    def clause(raw):
        q = frozenset(raw)
        if not any(-v in q for v in q):
            clauses.add(tuple(sorted(q, key=lambda v: (abs(v), v < 0))))
    incidences = defaultdict(list)
    for j, p in enumerate(placements):
        for t, v in variables.items():
            incidences[move(t, p)].append((j, v))
    for occurrences in incidences.values():
        for j, (_, a) in enumerate(occurrences):
            for _, b in occurrences[j+1:]:
                clause([-a, -b])
    for p in placements:
        level = p['level']
        if level == 5:
            continue
        for t, v in variables.items():
            neighbors = {u for point in t for u in star(point)} - {t}
            for u in neighbors:
                filling = {x for j, x in incidences.get(move(u, p), ())
                           if placements[j]['level'] <= level+1}
                clause([-v, *filling])
    all_vertices = sorted({v for t in cells for v in t})
    sixty = {}; three_hundred = {}; top = len(cells)
    for point in all_vertices:
        ws = wedges(point); assert set(ws) == star(point)
        local = [variables.get(t) for t in ws]
        top += 1; sixty[point] = top
        top += 1; three_hundred[point] = top
        for raw in link_clauses(local, sixty[point], three_hundred[point]):
            clause(raw)
    from pysat.card import CardEnc, EncType
    cardinality = CardEnc.atmost(lits=list(variables.values()), bound=limit,
                                 top_id=top, encoding=EncType.totalizer)
    surplus = CardEnc.atleast(lits=[*three_hundred.values(), *(-v for v in sixty.values())],
                              bound=len(sixty)+1, top_id=cardinality.nv,
                              encoding=EncType.cardnetwrk)
    frozen = sorted(clauses)+cardinality.clauses+surplus.clauses
    return cells, original, placements, sixty, three_hundred, frozen, surplus.nv
