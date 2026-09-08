#!/usr/bin/env python3
"""Independent audit of the global greedy good43 carrier refinement.

The checker imports no submitted Python module.  It independently parses the
catalogs, uses a forward exact-cover DP for ordered triple partitions,
reconstructs all Cartesian carrier factors, and emits all new physical closure
clauses directly from block atoms.  With --cnf-dir it also checks the exact
new-clause suffix of every regenerated representative formula.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import combinations
from math import comb, prod
from pathlib import Path


TARGET_MANIFEST_SHA256 = (
    "5d1e479ae9d8e9d33a013029096ea73409607923e96a703033b9ea2feb8b1a8c"
)
PARENT_MANIFEST_SHA256 = (
    "1e3cafb437e30478f3961200529cb0a7bb4d5065495f8bf47f0da7589457172e"
)
CATALOG_HASHES = {
    6: "e93e46f7100d26157f7a63106f9b32a05480f6fa0c70fd41a940bd124b2b6ec6",
    9: "3246c40dc444a248ae9199625abe16a984f630cf3d5f1ff1528e4409ff0c80cb",
    12: "322e7a54e67f4201bd37998ab420afb3eee41b1dcd6b277b7f055bda152da95e",
}
CATALOG_ORDERS = {6: 32, 9: 290, 12: 12}
LAST_TYPES = ("B3", "E3", "P3", "R3")
LAST_MASKS = (0, 1, 3, 7)
FULL_BRANCHES = ([5, 1, 0], [5, 4, 3], [6, 2, 1], [6, 3, 2],
                 [7, 1, 2], [7, 4, 0], [5, 1, 2])


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def object_sha256(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256_bytes(raw)


def read_json(path: Path):
    return json.loads(path.read_text())


def verify_manifest(directory: Path, expected_manifest_hash: str) -> int:
    manifest = directory / "SHA256SUMS"
    require(file_sha256(manifest) == expected_manifest_hash,
            f"manifest identity mismatch in {directory.name}")
    count = 0
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(file_sha256(directory / name) == digest,
                f"manifest mismatch in {directory.name}/{name}")
        count += 1
    require(count == 29, f"unexpected manifest length {count}")
    return count


def parse_graph6(line: str) -> list[int]:
    """Parse small graph6 records by consuming their bit stream directly."""
    require(type(line) is str and line, "empty graph6 record")
    values = [ord(character) - 63 for character in line]
    require(all(0 <= value < 64 for value in values), "graph6 alphabet")
    order = values[0]
    require(order in CATALOG_ORDERS, f"unexpected graph order {order}")
    needed = comb(order, 2)
    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    require(len(bits) == 6 * ((needed + 5) // 6), "graph6 payload length")
    require(not any(bits[needed:]), "nonzero graph6 padding")
    adjacency = [0] * order
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return adjacency


def is_clique(vertices, adjacency) -> bool:
    return all((adjacency[left] >> right) & 1
               for left, right in combinations(vertices, 2))


def is_independent(vertices, adjacency) -> bool:
    return all(not ((adjacency[left] >> right) & 1)
               for left, right in combinations(vertices, 2))


def mask_vertices(mask: int) -> list[int]:
    return [vertex for vertex in range(mask.bit_length()) if (mask >> vertex) & 1]


def mask_edge_count(mask: int, adjacency: list[int]) -> int:
    vertices = mask_vertices(mask)
    return sum((adjacency[left] >> right) & 1
               for left, right in combinations(vertices, 2))


def forward_partition_counts(adjacency: list[int]) -> list[int]:
    """Count named independent bins using a forward used-mask transfer DP."""
    order = len(adjacency)
    independent_triples = []
    for triple in combinations(range(order), 3):
        if is_independent(triple, adjacency):
            independent_triples.append(sum(1 << vertex for vertex in triple))
    independent_triples.sort()
    named_independent_bins = order // 3 - 1
    states = {0: 1}
    for _ in range(named_independent_bins):
        next_states = defaultdict(int)
        for used, multiplicity in states.items():
            for triple in independent_triples:
                if not (used & triple):
                    next_states[used | triple] += multiplicity
        states = next_states
    full = (1 << order) - 1
    counts = [0, 0, 0, 0]
    for used, multiplicity in states.items():
        remaining = full ^ used
        require(remaining.bit_count() == 3, "partition leaves wrong remainder")
        counts[mask_edge_count(remaining, adjacency)] += multiplicity
    return counts


def audit_catalogs(package: Path):
    published = read_json(package / "TAIL_COVERS.json")
    published_by_order = {record["n"]: record
                          for record in published["catalogs"]}
    totals_by_order = {}
    graphs_checked = 0
    ordered_partitions = 0
    per_entry_hashes = {}
    for order in (6, 9, 12):
        path = package / f"r35_{order}.g6"
        require(file_sha256(path) == CATALOG_HASHES[order],
                f"catalog {order} identity mismatch")
        lines = path.read_text().splitlines()
        require(len(lines) == CATALOG_ORDERS[order],
                f"catalog {order} cardinality mismatch")
        records = published_by_order[order]["entries"]
        require(len(records) == len(lines), "published entry count mismatch")
        cover_totals = [0, 0, 0, 0]
        compact_entries = []
        for index, (line, record) in enumerate(zip(lines, records)):
            adjacency = parse_graph6(line)
            require(not any(is_clique(triple, adjacency)
                            for triple in combinations(range(order), 3)),
                    f"red triangle in catalog {order}, entry {index}")
            require(not any(is_independent(five, adjacency)
                            for five in combinations(range(order), 5)),
                    f"blue K5 in catalog {order}, entry {index}")
            counts = forward_partition_counts(adjacency)
            require(record["index"] == index and record["graph6"] == line,
                    "published catalog entry ordering mismatch")
            require(record["partitions_by_last_red_edges"] == counts,
                    f"partition count mismatch at {order}:{index}")
            factor = 6 ** (order // 3 - 1)
            covers = [counts[edges] * factor * (6 if edges in (0, 3) else 2)
                      for edges in range(4)]
            require(record["embedding_covers_by_last_red_edges"] == covers,
                    f"embedding count mismatch at {order}:{index}")
            for edges in range(4):
                cover_totals[edges] += covers[edges]
            graphs_checked += 1
            ordered_partitions += sum(counts)
            compact_entries.append([index, counts, covers])
        require(published_by_order[order]["embedding_cover_totals"] ==
                cover_totals, f"catalog total mismatch at order {order}")
        totals_by_order[order] = cover_totals
        per_entry_hashes[str(order)] = object_sha256(compact_entries)
    require(graphs_checked == 334, "wrong total catalog size")
    require(ordered_partitions == 167046, "wrong ordered-partition total")
    expected_totals = {
        6: [2376, 732, 492, 0],
        9: [3220560, 1323504, 788976, 0],
        12: [56422656, 22584096, 11583648, 0],
    }
    require(totals_by_order == expected_totals,
            f"unexpected embedding totals {totals_by_order}")
    return totals_by_order, graphs_checked, ordered_partitions, per_entry_hashes


def branch_types(branch):
    red_fours, red_triples, last_type = branch
    return (["R4"] * red_fours + ["B4"] * (7 - red_fours)
            + ["R3"] * red_triples + ["B3"] * (4 - red_triples)
            + [LAST_TYPES[last_type]])


def allowed_branch(branch) -> bool:
    red_fours, red_triples, last_type = branch
    return (red_fours in (5, 6, 7) and red_triples in (1, 2, 3, 4)
            and last_type in (0, 1, 2, 3)
            and (red_triples == 4 or last_type < 3))


def reconstruct_global_counts(package: Path, parent: Path, tail_totals):
    domain_rows = read_json(parent / "DOMAINS.json")
    pair_counts = {(row["left"], row["right"]): row["count"]
                   for row in domain_rows}
    root_counts = {row["child"]: row["count"]
                   for row in read_json(parent / "ROOT_DOMAINS.json")}
    parent_counts = read_json(parent / "COUNTS.json")
    parent_rows = {tuple(row["branch"]): row
                   for row in parent_counts["branches"]}
    require(len(parent_rows) == 60, "parent does not have 60 branches")
    published = read_json(package / "GLOBAL_COUNTS.json")
    published_rows = {tuple(row["branch"]): row
                      for row in published["branches"]}
    require(len(published_rows) == 39, "published branch count mismatch")

    parent_total = 0
    carrier_total = 0
    reconstructed_rows = []
    removed = []
    for red_fours in (5, 6, 7):
        for red_triples in range(5):
            for last_type in range(4):
                branch = [red_fours, red_triples, last_type]
                kinds = branch_types(branch)
                factors = {}
                for left, right in combinations(range(12), 2):
                    factors[left, right] = (root_counts[kinds[right]]
                                            if left == 0 else
                                            pair_counts[kinds[left], kinds[right]])
                parent_count = prod(factors.values())
                require(parent_rows[tuple(branch)]["count"] == parent_count,
                        f"parent branch count mismatch {branch}")
                parent_total += parent_count
                if not allowed_branch(branch):
                    removed.append(branch)
                    continue

                residual_blocks = list(range(7 + red_triples, 12))
                residual_pairs = list(combinations(residual_blocks, 2))
                residual_pair_count = prod(factors[pair]
                                           for pair in residual_pairs)
                outside_count = prod(value for pair, value in factors.items()
                                     if pair not in set(residual_pairs))
                residual_order = 15 - 3 * red_triples
                if red_triples < 4:
                    embedding_count = tail_totals[residual_order][last_type]
                    carrier_count = min(residual_pair_count, embedding_count)
                    carrier_mode = ("catalog_embedding"
                                    if embedding_count < residual_pair_count
                                    else "original_pair_matrices")
                else:
                    embedding_count = carrier_count = 1
                    carrier_mode = "fixed_triple"
                whole_count = outside_count * carrier_count
                expected_row = {
                    "branch": branch,
                    "task_id": f"r{red_fours}-s{red_triples}-t{last_type}",
                    "residual_vertices": residual_order,
                    "residual_blocks": residual_blocks,
                    "residual_pairs": [list(pair) for pair in residual_pairs],
                    "parent_count": parent_count,
                    "parent_tail_pair_count": residual_pair_count,
                    "catalog_embedding_cover": embedding_count,
                    "carrier_mode": carrier_mode,
                    "tail_carrier_count": carrier_count,
                    "other_matrix_count": outside_count,
                    "whole_graph_cover_count": whole_count,
                    "red_four_free_union_size": (43 - 4 * red_fours
                                                 if red_fours < 7 else None),
                    "red_triangle_free_union_size": (residual_order
                                                     if red_triples < 4
                                                     else None),
                }
                require(published_rows[tuple(branch)] == expected_row,
                        f"published carrier row mismatch {branch}")
                reconstructed_rows.append(expected_row)
                carrier_total += whole_count

    require(parent_total == parent_counts["retained_rooted_family"],
            "parent total mismatch")
    require(parent_total == published["parent_physical_count"],
            "published parent total mismatch")
    require(carrier_total == published["whole_graph_representation_count"],
            "published carrier total mismatch")
    ratio = Fraction(parent_total, carrier_total)
    require(published["reduction_factor"] == {
        "numerator": ratio.numerator, "denominator": ratio.denominator},
        "published reduction fraction mismatch")
    require(6 * carrier_total < parent_total,
            "claimed sixfold reduction does not hold")
    require(carrier_total < 2 ** 785, "claimed power bound does not hold")
    require(published["strict_power_two_upper_bound"] ==
            carrier_total.bit_length(), "published power bound mismatch")
    require(published["removed_normal_form_branches"] == removed,
            "removed branch list mismatch")
    return (reconstructed_rows, removed, parent_total, carrier_total, ratio,
            parent_rows)


def physical_atoms(branch):
    red_fours, red_triples, last_type = branch
    blocks = [list(range(4 * index, 4 * index + 4)) for index in range(7)]
    blocks += [list(range(28 + 3 * index, 31 + 3 * index))
               for index in range(5)]
    fixed = {}
    owner = {}
    for block_index, block in enumerate(blocks):
        for vertex in block:
            owner[vertex] = block_index
        if block_index < 7:
            colour = int(block_index < red_fours)
            for edge in combinations(block, 2):
                fixed[edge] = colour
        elif block_index < 11:
            colour = int(block_index < 7 + red_triples)
            for edge in combinations(block, 2):
                fixed[edge] = colour
        else:
            for bit, edge in enumerate(combinations(block, 2)):
                fixed[edge] = (LAST_MASKS[last_type] >> bit) & 1
    require(len(fixed) == 57 and len(owner) == 43,
            "physical atom construction mismatch")
    variables = {}
    next_variable = 2
    for edge in combinations(range(43), 2):
        if edge not in fixed:
            variables[edge] = next_variable
            next_variable += 1
    require(next_variable == 848 and len(variables) == 846,
            "physical variable construction mismatch")
    return blocks, fixed, owner, variables


def closure_clauses(branch):
    red_fours, red_triples, _ = branch
    _, fixed, owner, variables = physical_atoms(branch)
    constraints = []
    if red_fours < 7:
        constraints.append((4, list(range(4 * red_fours, 43))))
    if red_triples < 4:
        constraints.append((3, list(range(28 + 3 * red_triples, 43))))
    clauses = []
    stats = {3: {"subsets": 0, "clauses": 0,
                 "across_three_or_more_blocks": 0},
             4: {"subsets": 0, "clauses": 0,
                 "across_three_or_more_blocks": 0}}
    for size, vertices in constraints:
        for chosen in combinations(vertices, size):
            stats[size]["subsets"] += 1
            edges = list(combinations(chosen, 2))
            if any(edge in fixed and fixed[edge] == 0 for edge in edges):
                continue
            clause = tuple(-variables[edge] for edge in edges
                           if edge in variables)
            require(clause, f"fixed red clique in normalized branch {branch}")
            clauses.append(clause)
            stats[size]["clauses"] += 1
            if len({owner[vertex] for vertex in chosen}) >= 3:
                stats[size]["across_three_or_more_blocks"] += 1
    return clauses, stats


def audit_closures_and_registry(package: Path, rows, parent_rows,
                                carrier_total):
    interface = read_json(package / "INTERFACE_AUDIT.json")
    interface_stats = {tuple(row["branch"]): row
                       for row in interface["formula_stats"]}
    closure_records = []
    clause_total = 0
    multiblock_total = 0
    by_branch = {}
    for row in rows:
        branch = row["branch"]
        clauses, stats = closure_clauses(branch)
        normalized_stats = {str(size): values for size, values in stats.items()}
        published = interface_stats[tuple(branch)]
        parent_clause_count = parent_rows[tuple(branch)]["cnf_clauses"]
        require(published == {
            "task_id": row["task_id"],
            "branch": branch,
            "variables": 847,
            "parent_clauses": parent_clause_count,
            "extra_clauses": len(clauses),
            "clauses": parent_clause_count + len(clauses),
            "extra_statistics": normalized_stats,
        }, f"interface statistics mismatch {branch}")
        multiblock = sum(values["across_three_or_more_blocks"]
                         for values in stats.values())
        record = {
            "branch": branch,
            "clauses": len(clauses),
            "multiblock_clauses": multiblock,
            "clause_sequence_sha256": object_sha256(
                [list(clause) for clause in clauses]),
        }
        closure_records.append(record)
        by_branch[tuple(branch)] = (clauses, normalized_stats,
                                    parent_clause_count)
        clause_total += len(clauses)
        multiblock_total += multiblock
    require(clause_total == interface["all_extra_clauses_compared"] == 106263,
            "global closure-clause total mismatch")
    require(multiblock_total ==
            interface["extra_clauses_meeting_at_least_three_blocks"] == 103941,
            "global multiblock clause total mismatch")

    registry = read_json(package / "TASKS.json")
    require(registry["task_count"] == len(registry["tasks"]) == 39,
            "task registry cardinality mismatch")
    require(registry["all_tasks_undecided"] is True
            and registry["code_is_physical_graph_bijection"] is False,
            "task registry scope mismatch")
    offset = 0
    for task, row in zip(registry["tasks"], rows):
        clauses, extra_stats, parent_clause_count = by_branch[tuple(row["branch"])]
        red_fours, red_triples, _ = row["branch"]
        expected = {
            "task_id": "gc1-" + row["task_id"],
            "parent_task_id": row["task_id"],
            "branch": row["branch"],
            "variables": 847,
            "clauses": parent_clause_count + len(clauses),
            "extra_clauses": len(clauses),
            "extra_statistics": extra_stats,
            "carrier_mode": row["carrier_mode"],
            "tail_carrier_count": row["tail_carrier_count"],
            "catalog_order": (row["residual_vertices"]
                              if row["carrier_mode"] == "catalog_embedding"
                              else None),
            "whole_graph_cover_count": row["whole_graph_cover_count"],
            "global_start": offset,
            "global_stop": offset + row["whole_graph_cover_count"],
            "red_four_free_union_size": (43 - 4 * red_fours
                                         if red_fours < 7 else None),
            "red_triangle_free_union_size": (15 - 3 * red_triples
                                             if red_triples < 4 else None),
            "decision": "UNDECIDED",
        }
        require(task == expected, f"task record mismatch {row['branch']}")
        offset = expected["global_stop"]
    require(offset == registry["whole_graph_representation_count"]
            == carrier_total, "registry intervals do not cover the carrier")
    least = min(rows, key=lambda row: row["whole_graph_cover_count"])
    require(registry["least_carrier_task"] == "gc1-" + least["task_id"],
            "least-carrier task mismatch")
    return closure_records, clause_total, multiblock_total, by_branch


def parse_clause(line: bytes):
    fields = line.decode().split()
    require(fields and fields[-1] == "0", "malformed DIMACS clause")
    return tuple(map(int, fields[:-1]))


def audit_full_formula_suffixes(package: Path, cnf_dir: Path, by_branch):
    full_audit = read_json(package / "FULL_AUDIT.json")
    published = {tuple(record["producer"]["branch"]): record
                 for record in full_audit["records"]}
    require(set(published) == {tuple(branch) for branch in FULL_BRANCHES},
            "representative full-formula branch set mismatch")
    results = []
    for branch in FULL_BRANCHES:
        key = tuple(branch)
        record = published[key]["producer"]
        path = cnf_dir / ("branch-" + "-".join(map(str, branch)) + ".cnf")
        require(path.is_file(), f"missing regenerated CNF {path.name}")
        require(path.stat().st_size == record["bytes"],
                f"CNF byte-size mismatch {branch}")
        require(file_sha256(path) == record["sha256"],
                f"CNF SHA-256 mismatch {branch}")
        clauses, _, parent_clause_count = by_branch[key]
        require(parent_clause_count == record["parent_clauses"]
                and len(clauses) == record["extra_clauses"],
                f"CNF layer count mismatch {branch}")
        with path.open("rb") as stream:
            header = stream.readline().decode().split()
            require(header == ["p", "cnf", "847", str(record["clauses"])],
                    f"CNF header mismatch {branch}")
            for _ in range(parent_clause_count):
                require(stream.readline(), f"truncated parent prefix {branch}")
            for index, expected in enumerate(clauses):
                require(parse_clause(stream.readline()) == expected,
                        f"new-clause suffix mismatch {branch} at {index}")
            require(stream.read() == b"", f"trailing CNF data {branch}")
        results.append({
            "branch": branch,
            "clauses": record["clauses"],
            "extra_clauses": len(clauses),
            "bytes": record["bytes"],
            "sha256": record["sha256"],
            "independent_extra_suffix_verified": True,
        })
    require(sum(row["clauses"] for row in results) == 9858581,
            "representative formula clause total mismatch")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    parser.add_argument("--cnf-dir", type=Path)
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    package = source_root / "ramsey_r55_global_greedy_closure"
    parent = source_root / "ramsey_r55_global_clique_packing"
    require(package.is_dir() and parent.is_dir(),
            "source root lacks the target or pinned parent package")
    target_manifest_entries = verify_manifest(package, TARGET_MANIFEST_SHA256)
    parent_manifest_entries = verify_manifest(parent, PARENT_MANIFEST_SHA256)

    (tail_totals, graphs_checked, ordered_partitions,
     catalog_entry_hashes) = audit_catalogs(package)
    (rows, removed, parent_total, carrier_total, ratio,
     parent_rows) = reconstruct_global_counts(package, parent, tail_totals)
    (closure_records, closure_clause_total, multiblock_total,
     by_branch) = audit_closures_and_registry(
        package, rows, parent_rows, carrier_total)
    formula_results = (audit_full_formula_suffixes(
        package, args.cnf_dir.resolve(), by_branch) if args.cnf_dir else [])

    getcontext().prec = 30
    result = {
        "status": "VERIFIED_INDEPENDENT_GLOBAL_GREEDY_CLOSURE",
        "target_manifest_entries": target_manifest_entries,
        "parent_manifest_entries": parent_manifest_entries,
        "catalog_completeness": "imported from McKay author catalog",
        "catalog_graphs_checked": graphs_checked,
        "ordered_partitions_checked": ordered_partitions,
        "catalog_entry_census_sha256": catalog_entry_hashes,
        "catalog_embedding_totals": {
            str(order): totals for order, totals in tail_totals.items()},
        "refined_branches": len(rows),
        "normalized_away_parent_labels": len(removed),
        "parent_representation_count": parent_total,
        "new_representation_count": carrier_total,
        "reduction_factor_numerator": ratio.numerator,
        "reduction_factor_denominator": ratio.denominator,
        "reduction_factor_decimal": str(Decimal(ratio.numerator)
                                        / Decimal(ratio.denominator)),
        "strict_sixfold_reduction": 6 * carrier_total < parent_total,
        "strict_upper_bound_2_pow_785": carrier_total < 2 ** 785,
        "closure_clauses": closure_clause_total,
        "closure_clauses_meeting_at_least_three_blocks": multiblock_total,
        "closure_branch_records_sha256": object_sha256(closure_records),
        "task_intervals_verified": len(rows),
        "least_carrier_task": "gc1-r5-s1-t2",
        "full_formula_results": formula_results,
        "full_formula_suffixes_verified": len(formula_results),
        "target_found": False,
        "branch_excluded": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
