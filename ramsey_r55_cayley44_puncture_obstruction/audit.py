#!/usr/bin/env python3
"""Definition-level independent audit of the four Cayley(44) formulas/models."""
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import sys


NAMES = ("c11_c4", "c11_v4", "c11_sd_c4", "c11_sd_v4")


def coordinates(name):
    if name.endswith("v4"):
        return [(a, b, c) for c in (0, 1) for b in (0, 1) for a in range(11)]
    return [(a, b) for b in range(4) for a in range(11)]


def product(name, x, y):
    twisted = "_sd_" in name
    if len(x) == 3:
        a, b, c = x
        d, e, f = y
        return ((a + (-d if twisted and b else d)) % 11, b ^ e, c ^ f)
    a, b = x
    c, d = y
    return ((a + (-c if twisted and b % 2 else c)) % 11, (b + d) % 4)


def independently_build(name):
    elems = coordinates(name)
    number = {x: i for i, x in enumerate(elems)}
    table = [[number[product(name, x, y)] for y in elems] for x in elems]
    if any(table[0][x] != x or table[x][0] != x for x in range(44)):
        raise AssertionError("identity")
    for x, y, z in ((x, y, z) for x in range(44) for y in range(44) for z in range(44)):
        if table[table[x][y]][z] != table[x][table[y][z]]:
            raise AssertionError((name, "associativity", x, y, z))
    inv = []
    for x in range(44):
        choices = [y for y in range(44) if table[x][y] == table[y][x] == 0]
        if len(choices) != 1:
            raise AssertionError((name, "inverse", x, choices))
        inv.append(choices[0])
    unseen = set(range(1, 44))
    orbits = []
    while unseen:
        x = min(unseen)
        o = tuple(sorted({x, inv[x]}))
        orbits.append(o)
        unseen -= set(o)
    var = {x: i + 1 for i, o in enumerate(orbits) for x in o}
    clauses = set()
    for tail in combinations(range(1, 44), 4):
        vertices = (0,) + tail
        used = set()
        for u, v in combinations(vertices, 2):
            used.add(var[table[inv[u]][v]])
        ordered = tuple(sorted(used))
        clauses.add(ordered)
        clauses.add(tuple(-x for x in ordered))
    return table, inv, orbits, clauses


def parse_cnf(path):
    header = None
    clauses = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            parts = line.split()
            header = (int(parts[2]), int(parts[3]))
            continue
        row = tuple(map(int, line.split()))
        if not row or row[-1] != 0 or 0 in row[:-1]:
            raise AssertionError((path, "bad row"))
        clauses.append(row[:-1])
    if header != (header[0], len(clauses)):
        raise AssertionError((path, "header", header, len(clauses)))
    return header, clauses


def load_model(path, variables):
    status = None
    values = {}
    for line in path.read_text().splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        if line.startswith("v "):
            for lit in map(int, line[2:].split()):
                if lit:
                    values[abs(lit)] = lit > 0
    if status != "SATISFIABLE" or set(values) != set(range(1, variables + 1)):
        raise AssertionError((path, status, len(values), variables))
    return values


def verify_model(name, table, inv, orbits, model_path):
    var = {x: i + 1 for i, o in enumerate(orbits) for x in o}
    values = load_model(model_path, len(orbits))
    edges = [[False] * 44 for _ in range(44)]
    for u in range(44):
        for v in range(u + 1, 44):
            edges[u][v] = edges[v][u] = values[var[table[inv[u]][v]]]
    bad = []
    for five in combinations(range(44), 5):
        colors = {edges[u][v] for u, v in combinations(five, 2)}
        if len(colors) == 1:
            bad.append((five, int(next(iter(colors)))))
            break
    if bad:
        raise AssertionError((name, "model has monochromatic five", bad[0]))
    return sum(edges[u][v] for u in range(44) for v in range(u + 1, 44))


def main(root):
    summaries = []
    core_root = root / "cores"
    if not core_root.exists():
        core_root = root / "compact"
    for name in NAMES:
        table, inv, orbits, expected = independently_build(name)
        header, clauses = parse_cnf(root / "formulas" / f"{name}.cnf")
        actual = set(clauses)
        if len(actual) != len(clauses) or actual != expected or header[0] != len(orbits):
            raise AssertionError((name, header, len(actual), len(expected),
                                  len(actual - expected), len(expected - actual)))
        core_path = core_root / f"{name}.core.cnf"
        core_summary = None
        if core_path.exists():
            core_header, core_clauses = parse_cnf(core_path)
            physical = {frozenset(c) for c in expected}
            core_set = {frozenset(c) for c in core_clauses}
            if (core_header[0] != len(orbits) or len(core_set) != len(core_clauses)
                    or not core_set <= physical):
                raise AssertionError((name, "invalid physical core",
                                      core_header, len(core_set - physical)))
            core_summary = {
                "clauses": len(core_clauses),
                "bytes": core_path.stat().st_size,
                "sha256": sha256(core_path.read_bytes()).hexdigest(),
                "all_clauses_physical": True,
            }
        result_path = root / "run" / f"{name}.json"
        result = json.loads(result_path.read_text()) if result_path.exists() else None
        edges = None
        if result and result["outcome"] == "SAT":
            edges = verify_model(name, table, inv, orbits, root / "run" / f"{name}.stdout")
        summaries.append({
            "group": name,
            "variables": len(orbits),
            "clauses": len(actual),
            "width_histogram": {str(k): v for k, v in sorted(Counter(map(len, actual)).items())},
            "nonidentity_involutions": sum(inv[x] == x for x in range(1, 44)),
            "formula_exact": True,
            "unsat_core": core_summary,
            "sat_model_red_edges": edges,
        })
    print(json.dumps(summaries, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: audit.py ROOT")
    main(Path(sys.argv[1]))
