"""A complete finite grid-corona SAT encoding with Euler checks on every prefix.

This intentionally simple generator is for reduction validation, not a census.
It uses Python-SAT 1.8.dev24 only to search; check_witness uses no solver.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time

from circuit import Circuit
from topology import EIGHT, flood_counts, local_counts, topology_constraint


def normalize(cells):
    cells = set(map(tuple, cells))
    if not cells:
        raise ValueError("empty tile")
    if any(len(p) != 2 or any(type(x) is not int for x in p) for p in cells):
        raise ValueError("cells must have two integer coordinates")
    x0, y0 = min(x for x, y in cells), min(y for x, y in cells)
    return tuple(sorted((x - x0, y - y0) for x, y in cells))


def orientations(cells):
    variants = set()
    for reflect, turns in itertools.product((False, True), range(4)):
        moved = list(cells)
        if reflect:
            moved = [(-x, y) for x, y in moved]
        for _ in range(turns):
            moved = [(-y, x) for x, y in moved]
        variants.add(normalize(moved))
    return sorted(variants)


def halo(cells):
    cells = set(cells)
    return {(x + dx, y + dy) for x, y in cells for dx, dy in EIGHT} - cells


def at_most_one(circuit, xs):
    """Sinz's sequential at-most-one encoding, with no solver preprocessing."""
    xs = list(xs)
    if len(xs) < 2:
        return
    previous = circuit.new()
    circuit.clause([-xs[0], previous])
    for x in xs[1:-1]:
        current = circuit.new()
        circuit.clause([-x, current])
        circuit.clause([-previous, current])
        circuit.clause([-x, -previous])
        previous = current
    circuit.clause([-xs[-1], -previous])


def build(tile, depth, strict_disc=True, holes_last=False):
    if depth < 0:
        raise ValueError("negative depth")
    tile = normalize(tile)
    root = set(tile)
    if flood_counts(root) != (1, 0) or local_counts(root)[3]:
        raise ValueError("tile must be a topological disc")
    xmax, ymax = max(x for x, y in root), max(y for x, y in root)
    span = max(xmax + 1, ymax + 1)
    radius = depth * span
    circuit = Circuit()
    candidates = []
    # Every admissible tile through depth H lies in this proved finite box.
    for orientation in orientations(tile):
        oxmax = max(x for x, y in orientation)
        oymax = max(y for x, y in orientation)
        for tx in range(-radius, xmax + radius - oxmax + 1):
            for ty in range(-radius, ymax + radius - oymax + 1):
                cells = tuple((x + tx, y + ty) for x, y in orientation)
                if root.intersection(cells):
                    continue
                overhang = max(0, -tx, -ty, tx + oxmax - xmax, ty + oymax - ymax)
                first = max(1, (overhang + span - 1) // span)
                zs = [circuit.false] * first
                zs.extend(circuit.new() for _ in range(first, depth + 1))
                candidates.append({"cells": cells, "orientation": orientation,
                                   "translation": (tx, ty), "z": zs})
    occupancy = [{p: circuit.true for p in root} for _ in range(depth + 1)]
    covers = [{} for _ in range(depth + 1)]
    for candidate in candidates:
        zs = candidate["z"]
        for k in range(1, depth + 1):
            if zs[k] != circuit.false:
                for p in candidate["cells"]:
                    covers[k].setdefault(p, []).append(zs[k])
            if k < depth:
                circuit.clause([-zs[k], zs[k + 1]])
    for k in range(1, depth + 1):
        for p, xs in sorted(covers[k].items()):
            occupancy[k][p] = circuit.or_(xs)
    for xs in covers[depth].values():
        at_most_one(circuit, xs)
    for candidate in candidates:
        zs = candidate["z"]
        surrounding = sorted(halo(candidate["cells"]))
        for k in range(1, depth + 1):
            # On first activation, touch the previous occupied prefix.
            circuit.clause([-zs[k], zs[k - 1],
                            *(occupancy[k - 1].get(p, circuit.false) for p in surrounding)])
            if k < depth:
                for p in surrounding:
                    circuit.clause([-zs[k], occupancy[k + 1].get(p, circuit.false)])
    if depth:
        for p in sorted(halo(root)):
            circuit.clause([occupancy[1].get(p, circuit.false)])
    topology_sizes = []
    for k in range(1, depth + 1):
        if holes_last and k == depth:
            continue
        topology_sizes.append(topology_constraint(circuit, occupancy[k], strict_disc))
    return circuit, candidates, {"depth": depth, "span": span,
        "box": [-radius, xmax + radius, -radius, ymax + radius],
        "candidates": len(candidates), "variables": circuit.nv,
        "clauses": len(circuit.clauses), "topology": topology_sizes}


def check_witness(tile, depth, patch, strict_disc=True, holes_last=False):
    """Direct cell geometry, connected components and halo checks; no CNF."""
    tile = normalize(tile)
    shapes = set(orientations(tile))
    levels = [set() for _ in range(depth + 1)]
    copies = []
    for record in patch:
        k, raw = record["level"], list(map(tuple, record["cells"]))
        cells = set(raw)
        if len(raw) != len(cells):
            raise ValueError("duplicate cell in a copy")
        if type(k) is not int or not 0 <= k <= depth:
            raise ValueError("invalid level")
        if len(cells) != len(tile) or normalize(cells) not in shapes:
            raise ValueError("noncongruent tile")
        if any(cells.intersection(previous) for previous in levels):
            raise ValueError("overlapping tiles")
        levels[k].update(cells)
        copies.append((k, cells))
    if sum(k == 0 for k, cells in copies) != 1 or levels[0] != set(tile):
        raise ValueError("incorrect root")
    prefixes = [set(levels[0])]
    for k in range(1, depth + 1):
        prefixes.append(prefixes[-1] | levels[k])
    stats = []
    for k, cells in copies:
        if k and not halo(cells).intersection(prefixes[k - 1]):
            raise ValueError("tile does not touch preceding prefix")
    for k, prefix in enumerate(prefixes):
        if k < depth and not halo(prefix) <= prefixes[k + 1]:
            raise ValueError("incomplete surround")
        connected, holes = flood_counts(prefix)
        f, a, b, d = local_counts(prefix)
        if connected != 1:
            raise ValueError("disconnected prefix")
        if not (holes_last and k == depth) and (holes or (strict_disc and d)):
            raise ValueError("invalid prefix topology")
        stats.append({"level": k, "tiles": sum(lev == k for lev, _ in copies),
                      "cells": f, "holes": holes, "diagonal_pinches": d,
                      "euler": f - a + b - d})
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tile", type=Path, help="JSON containing a cells array")
    parser.add_argument("--depth", required=True, type=int)
    parser.add_argument("--allow-pinches", action="store_true")
    parser.add_argument("--holes-last", action="store_true")
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--generate-only", action="store_true")
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--proof", type=Path, help="write Glucose's UNSAT proof; check separately")
    parser.add_argument("--check-only", type=Path)
    args = parser.parse_args()
    tile = json.loads(args.tile.read_text())["cells"]
    if args.check_only:
        patch = json.loads(args.check_only.read_text())["patch"]
        print(json.dumps(check_witness(tile, args.depth, patch,
              not args.allow_pinches, args.holes_last), sort_keys=True, indent=2))
        return
    start = time.monotonic()
    circuit, candidates, stats = build(tile, args.depth, not args.allow_pinches, args.holes_last)
    stats["build_seconds"] = round(time.monotonic() - start, 3)
    if args.cnf:
        circuit.write_dimacs(args.cnf)
        stats["cnf_sha256"] = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    if args.generate_only:
        stats["result"] = "GENERATED; not solved"
        print(json.dumps(stats, sort_keys=True, indent=2))
        return
    from pysat.solvers import Solver
    from pysat import __version__
    stats["python_sat"] = __version__
    stats["solver"] = "glucose4"
    with Solver(name="glucose4", bootstrap_with=circuit.clauses,
                with_proof=bool(args.proof)) as solver:
        solve_start = time.monotonic()
        result = solver.solve()
        stats["solve_seconds"] = round(time.monotonic() - solve_start, 3)
        stats["result"] = "SAT" if result else "UNSAT (solver trust; no checked proof)"
        if not result and args.proof:
            lines = solver.get_proof()
            args.proof.write_text("\n".join(lines) + ("\n" if lines else ""))
            stats["proof_sha256"] = hashlib.sha256(args.proof.read_bytes()).hexdigest()
            stats["proof_bytes"] = args.proof.stat().st_size
        if result:
            positive = {x for x in solver.get_model() if x > 0}
            patch = [{"level": 0, "cells": normalize(tile)}]
            for candidate in candidates:
                for k, z in enumerate(candidate["z"]):
                    if z in positive:
                        patch.append({"level": k, "cells": candidate["cells"]})
                        break
            stats["checked_prefixes"] = check_witness(tile, args.depth, patch,
                not args.allow_pinches, args.holes_last)
            if args.witness:
                args.witness.write_text(json.dumps({"patch": patch}, sort_keys=True, indent=2) + "\n")
                stats["witness_sha256"] = hashlib.sha256(args.witness.read_bytes()).hexdigest()
    print(json.dumps(stats, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
