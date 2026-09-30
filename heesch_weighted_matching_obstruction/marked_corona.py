"""Exact signed-edge corona synthesis and checking; no record claim.

Cell/topology CNF uses six-heesch-1's published Circuit and topology modules.
This adapter retains all D4 maps and introduces one signed state per grid edge.
The witness checker uses flood fills and direct incidences, never the CNF.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import resource
import sys
import time

FOUR = ((1, 0), (-1, 0), (0, 1), (0, -1))
EIGHT = tuple((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y)
DEPENDENCY_SHA256 = {
    "circuit.py": "be6a80950052bb3b5b09874b3ecd16a22fb5caa1cec55b0734891e591a00c975",
    "topology.py": "65f914feed3f60a63304b36651e3b5fc99c35847ffa4a5ccc27bdec7bc361f54",
}


def check_encoding_dependencies(directory):
    for name, expected in DEPENDENCY_SHA256.items():
        if hashlib.sha256((Path(directory) / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"{name} differs from the pinned six-heesch-1 dependency")


def boundary(cells):
    """Original boundary ports in counterclockwise cycle order."""
    cells = set(map(tuple, cells))
    directed = []
    for x, y in cells:
        sides = [((x, y), (x + 1, y), (x, y - 1)),
                 ((x + 1, y), (x + 1, y + 1), (x + 1, y)),
                 ((x + 1, y + 1), (x, y + 1), (x, y + 1)),
                 ((x, y + 1), (x, y), (x - 1, y))]
        directed.extend((a, b) for a, b, neighbor in sides if neighbor not in cells)
    outgoing = {}
    for a, b in directed:
        if a in outgoing:
            raise ValueError("pinched or multiply connected base boundary")
        outgoing[a] = b
    start = min(outgoing)
    result, v = [], start
    while True:
        w = outgoing[v]
        result.append((v, w))
        v = w
        if v == start:
            break
        if len(result) >= len(directed):
            raise ValueError("noncyclic boundary")
    if len(result) != len(directed):
        raise ValueError("more than one boundary component")
    return result


def transform(p, reflect, turns):
    x, y = p
    if reflect:
        x = -x
    for _ in range(turns):
        x, y = -y, x
    return x, y


def oriented(tile, reflect, turns):
    """Transform square vertices, not cell indices, then normalize."""
    raw = []
    for x, y in tile:
        corners = [transform(p, reflect, turns) for p in
                   ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1))]
        raw.append((min(a for a, b in corners), min(b for a, b in corners)))
    ox, oy = min(x for x, y in raw), min(y for x, y in raw)
    cells = tuple(sorted((x - ox, y - oy) for x, y in raw))
    ports = []
    for a, b in boundary(tile):
        ends = [transform(p, reflect, turns) for p in (a, b)]
        ends = tuple(sorted((x - ox, y - oy) for x, y in ends))
        (x, y), (u, v) = ends
        # On a horizontal edge side 0 is above; on a vertical edge it is right.
        side = 0 if (x, y) in cells else 1
        ports.append((ends, side))
    return cells, ports


def halo(cells):
    cells = set(cells)
    return {(x + dx, y + dy) for x, y in cells for dx, dy in EIGHT} - cells


def at_most_one(circuit, xs):
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


def positive_charge_constraint(circuit, signs):
    """Exact p>q>0 comparator; sign legality is the caller's constraint."""
    plus_bits = circuit.count([x for x, y in signs])
    minus_bits = circuit.count([y for x, y in signs])
    length = max(len(plus_bits), len(minus_bits))
    plus_bits += [circuit.false] * (length - len(plus_bits))
    minus_bits += [circuit.false] * (length - len(minus_bits))
    equal, greater = circuit.true, []
    for a, b in zip(reversed(plus_bits), reversed(minus_bits)):
        greater.append(circuit.and_([equal, a, -b]))
        equal = circuit.and_([equal, -circuit.xor(a, b)])
    circuit.clause([circuit.or_(greater)])
    circuit.clause([y for x, y in signs])


def edge_state_constraints(circuit, signs, incidences):
    """One shared signed state per global edge, complemented on side 1."""
    edge_states = {}
    for active, edges in incidences:
        for index, (edge, side) in enumerate(edges):
            if edge not in edge_states:
                edge_states[edge] = circuit.new(), circuit.new()
                a, b = edge_states[edge]
                circuit.clause([-a, -b])
            a, b = edge_states[edge]
            targets = (a, b) if side == 0 else (b, a)
            for source, target in zip(signs[index], targets):
                circuit.clause([-active, -source, target])
                circuit.clause([-active, source, -target])
    return edge_states


def build(tile, depth, p, q, Circuit, topology_constraint, fixed=None, domain=None,
          allow_reflections=True, require_charge=True):
    boundary_fn = boundary if domain is None else domain.boundary
    oriented_fn = oriented if domain is None else domain.oriented
    halo_fn = halo if domain is None else domain.halo
    turns_count = 4 if domain is None else domain.turns_count
    root = set(tile)
    ports = boundary_fn(tile)
    if not (type(depth) is int and depth >= 1 and
            ((p is None and q is None) or
             (type(p) is int and type(q) is int and 0 < q < p <= len(ports) and p + q <= len(ports)))):
        raise ValueError("positive depth and 0<q<p, p+q<=perimeter are required")
    circuit = Circuit()
    if fixed is not None:
        if len(fixed) != len(ports) or any(type(x) is not int or x not in (-1, 0, 1) for x in fixed):
            raise ValueError("bad fixed signed pattern")
        signs = [(circuit.true if s == 1 else circuit.false,
                  circuit.true if s == -1 else circuit.false) for s in fixed]
    else:
        signs = [(circuit.new(), circuit.new()) for _ in ports]
    for plus, minus in signs:
        circuit.clause([-plus, -minus])
    if p is None and require_charge:
        positive_charge_constraint(circuit, signs)
    elif p is not None:
        circuit.equal_count([x for x, y in signs], p)
        circuit.equal_count([y for x, y in signs], q)
    xmax, ymax = max(x for x, y in tile), max(y for x, y in tile)
    span = max(xmax + 1, ymax + 1) if domain is None else domain.span(tile)
    radius = depth * span
    candidates = []
    reflections = (False, True) if allow_reflections else (False,)
    for reflect, turns in itertools.product(reflections, range(turns_count)):
        cells, edges = oriented_fn(tile, reflect, turns)
        oxmax, oymax = max(x for x, y in cells), max(y for x, y in cells)
        for tx in range(-radius, xmax + radius - oxmax + 1):
            for ty in range(-radius, ymax + radius - oymax + 1):
                moved = tuple((x + tx, y + ty) for x, y in cells)
                if root.intersection(moved):
                    continue
                overhang = max(0, -tx, -ty, tx + oxmax - xmax, ty + oymax - ymax)
                if domain is not None:
                    overhang = max(overhang, domain.extra_overhang(moved, tile))
                    if overhang > radius:
                        continue
                first = max(1, (overhang + span - 1) // span)
                zs = [circuit.false] * first
                zs.extend(circuit.new() for _ in range(first, depth + 1))
                candidates.append({"cells": moved, "translation": (tx, ty),
                                   "reflect": reflect, "turns": turns, "z": zs,
                                   "ports": [(tuple((x + tx, y + ty) for x, y in ends), side)
                                             for ends, side in edges]})
    occupancy = [{cell: circuit.true for cell in root} for _ in range(depth + 1)]
    covers = [{} for _ in range(depth + 1)]
    for candidate in candidates:
        zs = candidate["z"]
        for k in range(1, depth + 1):
            if zs[k] != circuit.false:
                for cell in candidate["cells"]:
                    covers[k].setdefault(cell, []).append(zs[k])
            if k < depth:
                circuit.clause([-zs[k], zs[k + 1]])
    for k in range(1, depth + 1):
        for cell, xs in sorted(covers[k].items()):
            occupancy[k][cell] = circuit.or_(xs)
    for xs in covers[depth].values():
        at_most_one(circuit, xs)
    for candidate in candidates:
        zs = candidate["z"]
        surrounding = sorted(halo_fn(candidate["cells"]))
        for k in range(1, depth + 1):
            circuit.clause([-zs[k], zs[k - 1],
                            *(occupancy[k - 1].get(cell, circuit.false) for cell in surrounding)])
            if k < depth:
                for cell in surrounding:
                    circuit.clause([-zs[k], occupancy[k + 1].get(cell, circuit.false)])
    for cell in sorted(halo_fn(root)):
        circuit.clause([occupancy[1].get(cell, circuit.false)])
    topology_sizes = [topology_constraint(circuit, occupancy[k], True)
                      for k in range(1, depth + 1)]
    incidences = itertools.chain([(circuit.true, oriented_fn(tile, False, 0)[1])],
                                 ((c["z"][depth], c["ports"]) for c in candidates))
    edge_states = edge_state_constraints(circuit, signs, incidences)
    counts = [p, q, len(ports) - p - q] if p is not None else (
        "any p>q>0" if require_charge else "no charge constraint")
    return circuit, candidates, signs, {"depth": depth, "counts": counts,
        "box": [-radius, xmax + radius, -radius, ymax + radius], "orientations": len(reflections) * turns_count,
        "candidates": len(candidates), "variables": circuit.nv,
        "clauses": len(circuit.clauses), "grid_edges": len(edge_states), "topology": topology_sizes}


def component_count(cells, directions):
    remaining = set(cells)
    count = 0
    while remaining:
        count += 1
        queue = deque([remaining.pop()])
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                v = x + dx, y + dy
                if v in remaining:
                    remaining.remove(v)
                    queue.append(v)
    return count


def check_witness(witness):
    """Direct definition-level checker, independent of CNF and imported modules."""
    if witness.get("grid", "square") == "hex":
        from hex_domain import check_witness as check_hex
        return check_hex(witness)
    if witness.get("grid", "square") != "square":
        raise ValueError("unknown grid")
    tile = tuple(map(tuple, witness["tile"]))
    if not tile or len(set(tile)) != len(tile) or any(len(v) != 2 or any(type(x) is not int for x in v) for v in tile):
        raise ValueError("empty or duplicate base cells")
    if min(x for x, y in tile) or min(y for x, y in tile):
        raise ValueError("base cells must be normalized")
    signs, depth = witness["signs"], witness["depth"]
    if type(depth) is not int or depth < 0:
        raise ValueError("invalid depth")
    if len(signs) != len(boundary(tile)) or any(type(x) is not int or x not in (-1, 0, 1) for x in signs):
        raise ValueError("invalid signs")
    original_ports = {tuple(sorted(port)): i for i, port in enumerate(boundary(tile))}
    levels = [set() for _ in range(depth + 1)]
    copies, edges = [], {}
    roots = 0
    for record in witness["patch"]:
        k, reflect, turns = record["level"], record["reflect"], record["turns"]
        if type(k) is not int or not 0 <= k <= depth or type(reflect) is not bool or type(turns) is not int or not 0 <= turns < 4:
            raise ValueError("invalid placement or level")
        tx, ty = record["translation"]
        if type(tx) is not int or type(ty) is not int:
            raise ValueError("invalid translation")
        def forward(p):
            a, b = p
            if reflect:
                a = -a
            for _ in range(turns):
                a, b = -b, a
            return a, b

        vertex_images = [forward((x + dx, y + dy)) for x, y in tile
                         for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1))]
        x0, y0 = min(x for x, y in vertex_images), min(y for x, y in vertex_images)
        cells = set()
        for x, y in tile:
            corners = [forward((x + dx, y + dy)) for dx, dy in ((0, 0), (1, 0), (1, 1), (0, 1))]
            cells.add((min(a for a, b in corners) - x0 + tx,
                       min(b for a, b in corners) - y0 + ty))

        def inverse(p):
            a, b = p[0] + x0 - tx, p[1] + y0 - ty
            for _ in range(turns):
                a, b = b, -a
            if reflect:
                a = -a
            return a, b
        if any(cells & previous for previous in levels):
            raise ValueError("overlap")
        if k == 0:
            roots += 1
            if reflect or turns or tx or ty or cells != set(tile):
                raise ValueError("incorrect central copy")
        levels[k].update(cells)
        copies.append((k, cells))
        for ends in boundary(cells):
            edge = tuple(sorted(ends))
            original_edge = tuple(sorted(inverse(v) for v in ends))
            index = original_ports[original_edge]
            side = 0 if edge[0] in cells else 1
            incident = edges.setdefault(edge, [])
            if incident:
                if len(incident) != 1 or incident[0][0] == side or incident[0][1] != -signs[index]:
                    raise ValueError("noncomplementary boundary edge")
            incident.append((side, signs[index]))
    if roots != 1:
        raise ValueError("expected one central copy")
    prefixes = [set(levels[0])]
    for k in range(1, depth + 1):
        prefixes.append(prefixes[-1] | levels[k])
    for k, cells in copies:
        if k and not halo(cells) & prefixes[k - 1]:
            raise ValueError("copy fails to touch preceding prefix")
    stats = []
    for k, cells in enumerate(prefixes):
        if k < depth and not halo(cells) <= prefixes[k + 1]:
            raise ValueError("incomplete corona")
        if component_count(cells, EIGHT) != 1:
            raise ValueError("disconnected prefix")
        lo_x, hi_x = min(x for x, y in cells) - 1, max(x for x, y in cells) + 1
        lo_y, hi_y = min(y for x, y in cells) - 1, max(y for x, y in cells) + 1
        background = {(x, y) for x in range(lo_x, hi_x + 1)
                      for y in range(lo_y, hi_y + 1)} - cells
        if component_count(background, FOUR) != 1:
            raise ValueError("hole in prefix")
        for x in range(lo_x, hi_x + 1):
            for y in range(lo_y, hi_y + 1):
                bits = [(x, y) in cells, (x + 1, y) in cells,
                        (x, y + 1) in cells, (x + 1, y + 1) in cells]
                if bits in ([True, False, False, True], [False, True, True, False]):
                    raise ValueError("diagonal pinch")
        stats.append({"level": k, "tiles": sum(lev == k for lev, _ in copies),
                      "cells": len(cells), "holes": 0, "diagonal_pinches": 0})
    p, q = signs.count(1), signs.count(-1)
    return {"signed_counts": [p, q, signs.count(0)], "finite_charge": p != q,
            "prefixes": stats}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int, default=1)
    parser.add_argument("--grid", choices=("square", "hex"))
    parser.add_argument("--tile", type=Path, help="JSON with cells and optional grid; normalized disc base")
    parser.add_argument("--depth", type=int)
    parser.add_argument("--plus", type=int)
    parser.add_argument("--minus", type=int)
    parser.add_argument("--unmarked-source", type=Path, default=Path(__file__).resolve().parent.parent / "heesch_polyomino_euler_cnf")
    parser.add_argument("--conflicts", type=int, default=20000)
    parser.add_argument("--fixed", type=Path)
    parser.add_argument("--witness", type=Path)
    parser.add_argument("--check-only", type=Path)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--generate-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        print(json.dumps(check_witness(json.loads(args.check_only.read_text())), sort_keys=True, indent=2))
        return
    if args.depth is None or args.conflicts < 1 or (args.tile is None and
            (args.width is None or args.width < 1 or args.height < 1)):
        parser.error("positive dimensions, depth, and conflict budget required")
    if args.tile:
        raw = json.loads(args.tile.read_text())
        tile = tuple(map(tuple, raw["cells"]))
        file_grid = raw.get("grid")
        if file_grid is not None and args.grid is not None and file_grid != args.grid:
            parser.error("tile grid conflicts with --grid")
        args.grid = args.grid or file_grid or "square"
    else:
        tile = tuple((x, y) for x in range(args.width) for y in range(args.height))
        args.grid = args.grid or "square"
    if args.grid not in ("square", "hex"):
        parser.error("unknown tile grid")
    check_encoding_dependencies(args.unmarked_source)
    sys.path.insert(0, str(args.unmarked_source))
    from circuit import Circuit
    from topology import topology_constraint
    domain = None
    if args.grid == "hex":
        import hex_domain as domain
        topology_constraint = domain.topology_constraint
    boundary_fn = boundary if domain is None else domain.boundary
    check_witness({"grid": args.grid, "tile": tile, "signs": [0] * len(boundary_fn(tile)),
                   "depth": 0, "patch": [{"level": 0, "reflect": False, "turns": 0,
                                          "translation": [0, 0]}]})
    fixed = json.loads(args.fixed.read_text())["signs"] if args.fixed else None
    started = time.monotonic()
    circuit, candidates, signs, stats = build(tile, args.depth, args.plus, args.minus,
                                             Circuit, topology_constraint, fixed, domain)
    stats["grid"] = args.grid
    stats["build_seconds"] = round(time.monotonic() - started, 3)
    if args.cnf:
        circuit.write_dimacs(args.cnf)
        stats["cnf_sha256"] = hashlib.sha256(args.cnf.read_bytes()).hexdigest()
    print(json.dumps({"generated": stats}), flush=True)
    if args.generate_only:
        stats["result"] = "GENERATED; not solved"
        print(json.dumps(stats, indent=2, sort_keys=True), flush=True)
        return
    from pysat.solvers import Solver
    from pysat import __version__
    stats["python_sat"] = __version__
    stats["solver"] = "glucose4"
    stats["conflict_budget"] = args.conflicts
    with Solver(name="glucose4", bootstrap_with=circuit.clauses,
                with_proof=bool(args.proof)) as solver:
        solver.conf_budget(args.conflicts)
        started = time.monotonic()
        result = solver.solve_limited()
        stats["solve_seconds"] = round(time.monotonic() - started, 3)
        stats["result"] = "SAT; direct witness checks passed" if result else (
            "UNSAT; solver trust until proof is checked" if result is False else "UNKNOWN; conflict budget exhausted")
        stats["solver_stats"] = solver.accum_stats()
        if result is False and args.proof:
            lines = solver.get_proof()
            args.proof.write_text("\n".join(lines) + ("\n" if lines else ""))
            stats["proof_bytes"] = args.proof.stat().st_size
        if result:
            positive = {x for x in solver.get_model() if x > 0}
            decoded = [1 if p in positive else -1 if q in positive else 0 for p, q in signs]
            patch = [{"level": 0, "reflect": False, "turns": 0, "translation": [0, 0]}]
            for candidate in candidates:
                for k, z in enumerate(candidate["z"]):
                    if z in positive:
                        patch.append({"level": k, "reflect": candidate["reflect"],
                                      "turns": candidate["turns"], "translation": candidate["translation"]})
                        break
            witness = {"grid": args.grid, "tile": tile, "signs": decoded, "depth": args.depth, "patch": patch}
            stats["witness_checks"] = check_witness(witness)
            if args.witness:
                args.witness.write_text(json.dumps(witness, indent=2, sort_keys=True) + "\n")
                stats["witness_sha256"] = hashlib.sha256(args.witness.read_bytes()).hexdigest()
    stats["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(json.dumps(stats, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
