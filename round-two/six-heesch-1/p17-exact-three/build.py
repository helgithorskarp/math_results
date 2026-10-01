"""Complete necessary third-prefix CNF and compact local-cover compiler.

The written proof supplies interior integrality and the unique second prefix.
The 115 retained integral types are an allowed relaxation, not an E1 census.
"""
from collections import defaultdict
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent/'finite-contact-types'))
sys.path.insert(0, str(HERE.parent/'p17-interior-integrality'))
from contact import Tile, halo, require
from local import candidates, compile_cnf, dimacs
from compact import compile_subset, audit_subset
from rup import RupChecker


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def contact_domain(tile, pairs):
    forbidden = set(map(tuple, pairs['forbidden_poses']))
    require(tuple(sorted(map(tuple, pairs['tile']))) == tile.orientations[tile.root[0]],
            'old pair tile changed')
    integer = {t for t in tile.universe() if not (t[1] % 2 or t[2] % 2)}

    def bad(t):
        return (t[0], t[1]//2, t[2]//2) in forbidden

    allowed = {t for t in integer if not bad(t) and
               not bad(tile.relative_type(tile.pose(t), tile.root))}
    return forbidden, integer, allowed


def third_formula(tile, data, pairs, dependency_root=ROOT):
    Circuit = load(dependency_root/'heesch_polyomino_euler_cnf/circuit.py',
                   'p17_prior_circuit').Circuit
    fixed = [tuple(p) for p in data['second_prefix']]
    fixed = [tile.root]+[p for p in fixed if p != tile.root]
    forbidden, integer, allowed = contact_domain(tile, pairs)
    pool, cnf, nv = compile_cnf(tile, fixed, 1, allowed)
    require(len(pool) <= 1500 and len(cnf) <= 200000, 'formula guard: incomplete')
    # Circuit reserves variable 1 for true, so shift the whole prior CNF.
    circuit = Circuit(nv=nv+1)
    circuit.clauses.extend([[x+1 if x > 0 else x-1 for x in row] for row in cnf])
    owners = defaultdict(list)
    for i, (pose, pixels) in enumerate(pool, 2):
        for q in pixels:
            owners[q].append(i)
    old = set().union(*(tile.pixels(p, 1) for p in fixed))
    occupancy = {q: circuit.true for q in sorted(old)}
    for q, xs in sorted(owners.items()):
        occupancy[q] = circuit.or_(xs)
    vertices = {(x-dx, y-dy) for x, y in occupancy
                for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1))}
    # These necessary no-pinch clauses do not impose hole-freeness.
    for x, y in sorted(vertices):
        a, b, c, d = [occupancy.get(q, circuit.false)
                      for q in ((x, y), (x+1, y), (x, y+1), (x+1, y+1))]
        circuit.clause([-a, b, c, -d])
        circuit.clause([a, -b, -c, d])
    motif = set(map(tuple, data['forbidden_three_copy_support']))
    block = [i for i, (pose, pixels) in enumerate(pool, 2) if pose in motif]
    require(len(block) == len(motif) == 3, 'motif is not three candidate copies')
    formula = circuit.clauses+[[-i for i in block]]
    require(len(formula) <= 200000 and circuit.nv <= 60000,
            'topology formula guard: incomplete')
    metadata = dict(candidates=len(pool), variables=circuit.nv,
                    clauses=len(formula), blocked_literals=block,
                    retained_integral_types=len(allowed),
                    prior_forbidden_types=len(forbidden))
    return fixed, pool, formula, circuit.nv, metadata
