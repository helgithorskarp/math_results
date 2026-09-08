#!/usr/bin/env python3
"""Independent review of the h3873 maximal-K4 global carrier.

This checker intentionally imports no module from the reviewed package.  It
uses only Python's standard library and the pinned source/data files supplied
on the command line.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path


TARGET_MANIFEST_SHA256 = "4b5eef01603081a0777d5d3cd060b4ba59f48922e101221024b7e7dd29417f2b"
PARENT_MANIFEST_SHA256 = "1e3cafb437e30478f3961200529cb0a7bb4d5065495f8bf47f0da7589457172e"
COMPARISON_COUNTS_SHA256 = "c8b825da0d59a4192d81f322f1541c705ca4098983886d8c7546e36a0c7a4158"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text())


def verify_manifest(directory: Path, wanted_hash: str, wanted_count: int) -> None:
    manifest = directory / "SHA256SUMS"
    require(sha256(manifest.read_bytes()) == wanted_hash, f"manifest identity: {directory.name}")
    lines = manifest.read_text().splitlines()
    require(len(lines) == wanted_count, f"manifest cardinality: {directory.name}")
    seen = set()
    for line in lines:
        parts = line.split("  ", 1)
        require(len(parts) == 2, "manifest syntax")
        digest, name = parts
        require(name not in seen and name and not Path(name).is_absolute(), "manifest path")
        seen.add(name)
        path = directory / name
        require(path.is_file() and sha256(path.read_bytes()) == digest, f"manifest entry: {name}")


def graph6_decode(line: bytes, n: int) -> list[int]:
    """Decode the small graph6 form directly, bit by bit."""
    require(line.endswith(b"\n"), "catalog newline")
    data = line[:-1]
    edge_slots = comb(n, 2)
    require(len(data) == 1 + (edge_slots + 5) // 6, "graph6 length")
    require(data[0] == n + 63 and all(63 <= byte <= 126 for byte in data), "graph6 alphabet")

    def bit(position: int) -> int:
        return ((data[1 + position // 6] - 63) >> (5 - position % 6)) & 1

    require(not any(bit(k) for k in range(edge_slots, 6 * (len(data) - 1))), "graph6 padding")
    adjacency = [0] * n
    k = 0
    for high in range(1, n):
        for low in range(high):
            if bit(k):
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            k += 1
    return adjacency


def triangle_count(adjacency: list[int]) -> int:
    total = 0
    for u in range(len(adjacency)):
        later = adjacency[u] & ~((1 << (u + 1)) - 1)
        while later:
            bit = later & -later
            later -= bit
            v = bit.bit_length() - 1
            total += (adjacency[u] & adjacency[v]).bit_count()
    require(total % 3 == 0, "triangle divisibility")
    return total // 3


def has_k4(adjacency: list[int]) -> bool:
    """Detect K4 through edges in common-neighbour subgraphs."""
    for u in range(len(adjacency)):
        later = adjacency[u] & ~((1 << (u + 1)) - 1)
        while later:
            bit = later & -later
            later -= bit
            v = bit.bit_length() - 1
            common = adjacency[u] & adjacency[v]
            scan = common
            while scan:
                w_bit = scan & -scan
                scan -= w_bit
                w = w_bit.bit_length() - 1
                if adjacency[w] & common:
                    return True
    return False


def graph_statistics(adjacency: list[int]) -> tuple[int, int, int]:
    n = len(adjacency)
    full = (1 << n) - 1
    complement = [full ^ (1 << u) ^ adjacency[u] for u in range(n)]
    require(not has_k4(adjacency), "red K4 in catalog")
    require(not has_k4(complement), "blue K4 in catalog")
    edges = sum(row.bit_count() for row in adjacency) // 2
    return edges, triangle_count(adjacency), triangle_count(complement)


def edge_word(adjacency: list[int]) -> int:
    word = 0
    for k, (u, v) in enumerate(combinations(range(len(adjacency)), 2)):
        word |= ((adjacency[u] >> v) & 1) << k
    return word


def catalog_audit(package: Path, cache: Path) -> tuple[dict[int, list[bytes]], list[dict]]:
    specs = read_json(package / "INPUTS.json")
    frozen = read_json(package / "CATALOG_CENSUS.json")
    records_by_n: dict[int, list[bytes]] = {}
    results = []
    all_rows = hashlib.sha256()
    total_row_bytes = 0
    total_records = 0
    for spec in specs:
        raw = (cache / spec["name"]).read_bytes()
        require(len(raw) == spec["bytes"] and sha256(raw) == spec["sha256"], "catalog file identity")
        records = raw.splitlines(keepends=True)
        require(len(records) == spec["count"] and len(set(records)) == spec["count"], "catalog count/uniqueness")
        require(all(len(line) == spec["line_bytes"] for line in records), "catalog record width")
        records_by_n[spec["n"]] = records
        histogram: Counter[tuple[int, int, int]] = Counter()
        local_rows = hashlib.sha256()
        for index, line in enumerate(records):
            adjacency = graph6_decode(line, spec["n"])
            edges, red_triangles, blue_triangles = graph_statistics(adjacency)
            histogram[edges, red_triangles, blue_triangles] += 1
            word = edge_word(adjacency)
            row = (
                f"{spec['n']} {index} {edges} {red_triangles} {blue_triangles} "
                f"{word & ((1 << 64) - 1)} {word >> 64}\n"
            ).encode()
            local_rows.update(row)
            all_rows.update(row)
            total_row_bytes += len(row)
            total_records += 1
        result = {
            "n": spec["n"],
            "count": len(records),
            "records_sha256": local_rows.hexdigest(),
            "histogram": [list(key) + [value] for key, value in sorted(histogram.items())],
        }
        results.append(result)
    require(results == frozen, "independent catalog census differs from frozen census")
    require(total_records == 547362, "total catalog records")
    require(total_row_bytes == 21122259, "total canonical row bytes")
    require(
        all_rows.hexdigest() == "2a33b4b9f308ffd056d5bcc92d2cff1596555c062090f62708fac428c57b72e3",
        "aggregate catalog row hash",
    )
    return records_by_n, results


def forbidden_cross_constraints(child_red: bool) -> list[tuple[int, int]]:
    """Return (cross-edge mask, forbidden colour) for every relevant 5-set."""
    constraints = set()
    for vertices in combinations(range(8), 5):
        fixed_colours = set()
        mask = 0
        for u, v in combinations(vertices, 2):
            if v < 4:
                fixed_colours.add(1)
            elif u >= 4:
                fixed_colours.add(int(child_red))
            else:
                mask |= 1 << (4 * u + (v - 4))
        if len(fixed_colours) == 1:
            constraints.add((mask, next(iter(fixed_colours))))
    return sorted(constraints)


def cross_allowed(word: int, constraints: list[tuple[int, int]]) -> bool:
    for mask, colour in constraints:
        if colour and word & mask == mask:
            return False
        if not colour and word & mask == 0:
            return False
    return True


def root_ordered(word: int) -> bool:
    columns = [sum(((word >> (4 * row + col)) & 1) << row for row in range(4)) for col in range(4)]
    return columns == sorted(columns, reverse=True)


def domain_audit(parent: Path) -> dict[str, int]:
    domains = read_json(parent / "DOMAINS.json")
    roots = read_json(parent / "ROOT_DOMAINS.json")
    masks = {}
    root_masks = {}
    for child, child_red in (("R4", True), ("B4", False)):
        constraints = forbidden_cross_constraints(child_red)
        semantic = 0
        ordered = 0
        for word in range(1 << 16):
            if cross_allowed(word, constraints):
                semantic |= 1 << word
                if root_ordered(word):
                    ordered |= 1 << word
        masks[child] = semantic
        root_masks[child] = ordered
    ordinary_red = next(row for row in domains if row.get("left") == "R4" and row.get("right") == "R4")
    ordinary_blue = next(row for row in domains if row.get("left") == "R4" and row.get("right") == "B4")
    root_red = next(row for row in roots if row.get("child") == "R4")
    root_blue = next(row for row in roots if row.get("child") == "B4")
    for row, wanted in (
        (ordinary_red, masks["R4"]),
        (ordinary_blue, masks["B4"]),
        (root_red, root_masks["R4"]),
        (root_blue, root_masks["B4"]),
    ):
        require(int(row["allowed_bitmap_hex"], 16) == wanted, "semantic matrix domain bitmap")
        require(row["count"] == wanted.bit_count(), "semantic matrix domain count")
    return {
        "root_red": root_masks["R4"].bit_count(),
        "root_blue": root_masks["B4"].bit_count(),
        "ordinary_same_colour": masks["R4"].bit_count(),
        "ordinary_opposite_colour": masks["B4"].bit_count(),
        "star": 15,
    }


def family_audit(package: Path, comparison: Path, census: list[dict]) -> dict:
    specs = read_json(package / "INPUTS.json")
    actual = read_json(package / "TASKS.json")
    target_comparison = read_json(package / "COMPARISON.json")
    comparison_file = comparison / "GLOBAL_COUNTS.json"
    require(sha256(comparison_file.read_bytes()) == COMPARISON_COUNTS_SHA256, "comparison count identity")
    old = read_json(comparison_file)
    offset = 0
    tasks = 0
    wanted_classes = []
    for q in range(7, 11):
        n = 43 - 4 * q
        spec = next(row for row in specs if row["n"] == n)
        census_row = next(row for row in census if row["n"] == n)
        require(sum(row[3] for row in census_row["histogram"]) == spec["count"], "census count transport")
        for r in range(5, q + 1):
            red_nonroot = r - 1
            blue = q - r
            per_task = (
                1998**red_nonroot
                * 1931**blue
                * 37823 ** (comb(red_nonroot, 2) + comb(blue, 2))
                * 35714 ** (red_nonroot * blue)
                * 15 ** (q * n)
            )
            stop = offset + spec["count"] * per_task
            wanted_classes.append(
                {
                    "q": q,
                    "r": r,
                    "n": n,
                    "core_start": 0,
                    "core_stop": spec["count"],
                    "first_task": f"mp1-q{q}-r{r}-c000000",
                    "last_task": f"mp1-q{q}-r{r}-c{spec['count'] - 1:06d}",
                    "per_task": per_task,
                    "code_start": offset,
                    "code_stop": stop,
                    "physical_variables": 903 - 6 * q - comb(n, 2),
                    "input_sha256": spec["sha256"],
                }
            )
            offset = stop
            tasks += spec["count"]
    require(actual["format"] == "mp1" and actual["classes"] == wanted_classes, "18-class registry")
    require(actual["macro_classes"] == 18 and actual["tasks"] == tasks == 2189178, "task count")
    require(actual["carrier_count"] == offset, "carrier total")
    H = old["whole_graph_representation_count"]
    require(target_comparison["H"] == H and target_comparison["N"] == offset, "comparison transport")
    require(18767 * offset < H < 18768 * offset, "strict factor interval")
    require(4096 * offset < H and offset < 2**770, "declared reduction gates")
    return {"macro_classes": 18, "tasks": tasks, "N": offset, "H": H}


def task_parameters(name: str) -> tuple[int, int, int]:
    pieces = name.split("-")
    require(len(pieces) == 4 and pieces[0] == "mp1", "task syntax")
    q, r, index = int(pieces[1][1:]), int(pieces[2][1:]), int(pieces[3][1:])
    require(7 <= q <= 10 and 5 <= r <= q, "task range")
    return q, r, index


def physical_task(name: str, records_by_n: dict[int, list[bytes]]) -> tuple[int, int, dict, dict]:
    q, r, index = task_parameters(name)
    n = 43 - 4 * q
    require(0 <= index < len(records_by_n[n]), "task catalog index")
    core = graph6_decode(records_by_n[n][index], n)
    fixed = {}
    for block in range(q):
        for u, v in combinations(range(4 * block, 4 * block + 4), 2):
            fixed[u, v] = int(block < r)
    for u, v in combinations(range(n), 2):
        fixed[4 * q + u, 4 * q + v] = (core[u] >> v) & 1
    variables = {}
    next_variable = 2
    for edge in combinations(range(43), 2):
        if edge not in fixed:
            variables[edge] = next_variable
            next_variable += 1
    return q, r, fixed, variables


def expected_clauses(q: int, r: int, fixed: dict, variables: dict):
    yield (1,)
    for block in range(1, q):
        for column in range(3):
            for low, high in combinations(range(16), 2):
                clause = []
                for vertex, word in ((4 * block + column, low), (4 * block + column + 1, high)):
                    for root_vertex in range(4):
                        variable = variables[root_vertex, vertex]
                        clause.append(-variable if (word >> root_vertex) & 1 else variable)
                yield tuple(clause)
    for vertices in combinations(range(43), 5):
        edges = tuple(combinations(vertices, 2))
        for colour in (1, 0):
            if any(fixed[edge] != colour for edge in edges if edge in fixed):
                continue
            yield tuple((-variables[edge] if colour else variables[edge]) for edge in edges if edge in variables)
    for vertices in combinations(range(4 * r, 43), 4):
        edges = tuple(combinations(vertices, 2))
        if any(fixed[edge] != 1 for edge in edges if edge in fixed):
            continue
        yield tuple(-variables[edge] for edge in edges if edge in variables)


def formula_audit(package: Path, cnf_directory: Path, records_by_n: dict[int, list[bytes]]) -> dict:
    frozen = read_json(package / "FORMULA_AUDIT.json")
    total_clauses = 0
    total_bytes = 0
    for receipt in frozen:
        name = receipt["task"]
        q, r, fixed, variables = physical_task(name, records_by_n)
        path = cnf_directory / f"{name}.cnf"
        digest = hashlib.sha256()
        byte_count = 0
        clause_count = 0
        histogram = Counter()
        with path.open("rb") as handle:
            header = handle.readline()
            digest.update(header)
            byte_count += len(header)
            words = header.split()
            require(len(words) == 4 and words[:2] == [b"p", b"cnf"], "DIMACS header")
            require(int(words[2]) == len(variables) + 1, "DIMACS variable count")
            for wanted in expected_clauses(q, r, fixed, variables):
                line = handle.readline()
                require(line, "truncated DIMACS")
                digest.update(line)
                byte_count += len(line)
                got = tuple(map(int, line.split()))
                require(got == wanted + (0,), f"clause mismatch: {name}:{clause_count + 1}")
                clause_count += 1
                histogram[len(wanted)] += 1
            require(not handle.read(1), "trailing DIMACS clause")
            require(clause_count == int(words[3]), "DIMACS clause count")
        result = {
            "task": name,
            "variables": len(variables) + 1,
            "clauses": clause_count,
            "sha256": digest.hexdigest(),
            "bytes": byte_count,
            "clause_lengths": {str(length): count for length, count in histogram.items()},
        }
        require(result == receipt, f"formula receipt: {name}")
        total_clauses += clause_count
        total_bytes += byte_count
    require(total_clauses == 21530292 and total_bytes == 947947181, "aggregate formula totals")
    return {"formulas": len(frozen), "clauses": total_clauses, "bytes": total_bytes}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--cache", required=True, type=Path)
    parser.add_argument("--cnfs", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    package = source / "ramsey_r55_global_maximal_packing"
    parent = source / "ramsey_r55_global_clique_packing"
    comparison = source / "ramsey_r55_global_greedy_closure"
    verify_manifest(package, TARGET_MANIFEST_SHA256, 20)
    verify_manifest(parent, PARENT_MANIFEST_SHA256, 29)
    domains = domain_audit(parent)
    records_by_n, census = catalog_audit(package, args.cache.resolve())
    family = family_audit(package, comparison, census)
    formulas = formula_audit(package, args.cnfs.resolve(), records_by_n)
    result = {
        "status": "INDEPENDENT_GLOBAL_CARRIER_VERIFIED_NO_TARGET",
        "source_commit": "1884881efbf52a54bd3a30b1445c211da7caec27",
        "catalog_completeness": "IMPORTED_FROM_MCKAY",
        "catalog_records_physically_checked": sum(row["count"] for row in census),
        "catalog_rows_sha256": "2a33b4b9f308ffd056d5bcc92d2cff1596555c062090f62708fac428c57b72e3",
        "domains": domains,
        **family,
        **formulas,
        "strict_ratio_interval": [18767, 18768],
        "gate_4096": True,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
