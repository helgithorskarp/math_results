"""Exact finite rooted square-grid covering relaxation for corona upper bounds.

UNSAT excludes the requested corona depth. SAT certifies only cell coverage,
not corona ranks or prefix topology. Solver traces need a separate proof check.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

from circuit import Circuit
from corona import at_most_one, normalize, orientations
from topology import flood_counts, local_counts


def dilation(cells, radius):
    if type(radius) is not int or radius < 0:
        raise ValueError("radius must be a nonnegative integer")
    return {(x + dx, y + dy) for x, y in cells
            for dx in range(-radius, radius + 1)
            for dy in range(-radius, radius + 1)}


def build_cover(tile, radius):
    tile = normalize(tile)
    root = set(tile)
    if flood_counts(root) != (1, 0) or local_counts(root)[3]:
        raise ValueError("tile must be a topological disc")
    target = dilation(root, radius)
    xmin, xmax = min(x for x, y in target), max(x for x, y in target)
    ymin, ymax = min(y for x, y in target), max(y for x, y in target)
    circuit = Circuit()
    candidates = []
    covers = {}
    for orientation in orientations(tile):
        width = max(x for x, y in orientation)
        height = max(y for x, y in orientation)
        for tx in range(xmin - width, xmax + 1):
            for ty in range(ymin - height, ymax + 1):
                cells = tuple((x + tx, y + ty) for x, y in orientation)
                if root.intersection(cells) or not target.intersection(cells):
                    continue
                z = circuit.new()
                candidates.append({"cells": cells, "variable": z})
                for p in cells:
                    covers.setdefault(p, []).append(z)
    for p in sorted(target - root):
        circuit.clause(covers.get(p, []))
    # Outside-target overlaps must also be forbidden.
    for p in sorted(covers):
        at_most_one(circuit, covers[p])
    stats = {"radius": radius, "target_cells": len(target),
             "candidates": len(candidates), "footprint_cells": len(root | set(covers)),
             "variables": circuit.nv, "clauses": len(circuit.clauses)}
    return circuit, candidates, stats


def check_cover(tile, radius, patch):
    """Check raw congruent copies, disjointness and metric coverage, without CNF."""
    tile = normalize(tile)
    if type(radius) is not int or radius < 0:
        raise ValueError("radius must be a nonnegative integer")
    variants = set(orientations(tile))
    occupied = set()
    roots = 0
    for raw in patch:
        cells = set(map(tuple, raw))
        if len(cells) != len(raw) or len(cells) != len(tile):
            raise ValueError("invalid copy area or repeated cell")
        if normalize(cells) not in variants:
            raise ValueError("noncongruent copy")
        if cells & occupied:
            raise ValueError("overlapping copies")
        roots += cells == set(tile)
        occupied.update(cells)
    if roots != 1:
        raise ValueError("prescribed root missing")
    # The checker uses distance to P, rather than the generator's Minkowski sum.
    target = {(x, y)
              for x in range(-radius, max(x for x, y in tile) + radius + 1)
              for y in range(-radius, max(y for x, y in tile) + radius + 1)
              if min(max(abs(x - a), abs(y - b)) for a, b in tile) <= radius}
    if not target <= occupied:
        raise ValueError("uncovered target cells")
    return {"copies": len(patch), "occupied_cells": len(occupied),
            "target_cells": len(target), "checked": "rooted covering only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tile", type=Path)
    parser.add_argument("--radius", type=int, required=True)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--generate-only", action="store_true")
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--check-only", type=Path)
    args = parser.parse_args()
    tile = json.loads(args.tile.read_text())["cells"]
    if args.check_only:
        patch = json.loads(args.check_only.read_text())["patch"]
        print(json.dumps(check_cover(tile, args.radius, patch), sort_keys=True))
        return
    started = time.monotonic()
    circuit, candidates, stats = build_cover(tile, args.radius)
    stats["build_seconds"] = round(time.monotonic() - started, 3)
    if args.cnf:
        circuit.write_dimacs(args.cnf)
        stats["cnf_sha256"] = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    if args.generate_only:
        stats["result"] = "GENERATED; not solved"
    else:
        from pysat.solvers import Solver
        from pysat import __version__
        stats.update({"solver": "glucose4", "python_sat": __version__})
        with Solver(name="glucose4", bootstrap_with=circuit.clauses,
                    with_proof=bool(args.proof)) as solver:
            started = time.monotonic()
            sat = solver.solve()
            stats["solve_seconds"] = round(time.monotonic() - started, 3)
            stats["result"] = "SAT covering only" if sat else "UNSAT (proof not checked)"
            if sat:
                positive = {x for x in solver.get_model() if x > 0}
                patch = [normalize(tile)] + [q["cells"] for q in candidates
                                            if q["variable"] in positive]
                stats["cover"] = check_cover(tile, args.radius, patch)
                if args.witness:
                    args.witness.write_text(json.dumps({"patch": patch}, sort_keys=True,
                                                       indent=2) + "\n")
                    stats["witness_sha256"] = hashlib.sha256(args.witness.read_bytes()).hexdigest()
            elif args.proof:
                lines = solver.get_proof() or ["0"]
                args.proof.write_text("\n".join(lines) + ("\n" if lines else ""))
                stats["proof_bytes"] = args.proof.stat().st_size
                stats["proof_sha256"] = hashlib.sha256(args.proof.read_bytes()).hexdigest()
    print(json.dumps(stats, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
