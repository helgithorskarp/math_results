#!/usr/bin/env python3
"""Independent definition-level audit for the oriented order-15 theorem.

This standard-library checker imports no target module and uses no SAT solver.
It exhausts all oriented graphs through order five at every root, comparing an
augmenting-path matching algorithm with direct Hall-subset enumeration.  It
also checks the elementary reductions used before the order-15 SAT instances
and audits the published twelve-case manifest.
"""
from __future__ import annotations

from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "strong_seymour_oriented_order15"


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def decode_oriented_graph(order: int, code: int) -> list[int]:
    """Decode base-three pair states: absent, low-to-high, high-to-low."""
    rows = [0] * order
    for low, high in combinations(range(order), 2):
        code, state = divmod(code, 3)
        if state == 1:
            rows[low] |= 1 << high
        elif state == 2:
            rows[high] |= 1 << low
    need(code == 0, "graph code overflow")
    return rows


def exact_second(rows: list[int], root: int) -> int:
    first = rows[root]
    reached = 0
    bits = first
    while bits:
        edge = bits & -bits
        reached |= rows[edge.bit_length() - 1]
        bits ^= edge
    universe = (1 << len(rows)) - 1
    return reached & ~first & ~(1 << root) & universe


def matching_rank(rows: list[int], root: int) -> int:
    """Maximum matching by repeated augmenting paths, not subset-state DP."""
    left = rows[root]
    right = exact_second(rows, root)
    match: dict[int, int] = {}

    def augment(source: int, seen: set[int]) -> bool:
        choices = rows[source] & right
        while choices:
            edge = choices & -choices
            target = edge.bit_length() - 1
            choices ^= edge
            if target in seen:
                continue
            seen.add(target)
            if target not in match or augment(match[target], seen):
                match[target] = source
                return True
        return False

    rank = 0
    bits = left
    while bits:
        edge = bits & -bits
        rank += augment(edge.bit_length() - 1, set())
        bits ^= edge
    return rank


def hall_data(rows: list[int], root: int) -> tuple[int, list[tuple[int, int]]]:
    """Return maximum Hall deficiency and all inclusion-minimal witnesses."""
    first = rows[root]
    right = exact_second(rows, root)
    deficient: dict[int, int] = {}
    source = first
    while source:
        reached = 0
        bits = source
        while bits:
            edge = bits & -bits
            reached |= rows[edge.bit_length() - 1]
            bits ^= edge
        target = reached & right
        if source.bit_count() > target.bit_count():
            deficient[source] = target
        source = (source - 1) & first

    minimal: list[tuple[int, int]] = []
    for source, target in deficient.items():
        proper = (source - 1) & source
        is_minimal = True
        while proper:
            if proper in deficient:
                is_minimal = False
                break
            proper = (proper - 1) & source
        if is_minimal:
            minimal.append((source, target))
    maximum = max(
        (source.bit_count() - target.bit_count()
         for source, target in deficient.items()),
        default=0,
    )
    return maximum, minimal


def check_minimal_witness(rows: list[int], source: int, target: int) -> None:
    need(target.bit_count() == source.bit_count() - 1,
         "minimal Hall witness does not have deficiency one")
    bits = target
    while bits:
        edge = bits & -bits
        vertex = edge.bit_length() - 1
        predecessors = sum(
            bool((source >> u) & 1 and (rows[u] >> vertex) & 1)
            for u in range(len(rows))
        )
        need(predecessors >= 2, "minimal Hall target lacks double coverage")
        bits ^= edge


def check_dominating_extension(rows: list[int]) -> None:
    order = len(rows)
    extended = rows[:] + [(1 << order) - 1]
    for root in range(order):
        need(rows[root] == extended[root], "old first neighborhood changed")
        need(exact_second(rows, root) == exact_second(extended, root),
             "old second neighborhood changed")
    new_root = order
    need(extended[new_root].bit_count() == order, "new vertex is not dominating")
    need(exact_second(extended, new_root) == 0,
         "dominating extension acquired an exact second neighbor")


def check_arc_deletion_monotonicity(rows: list[int]) -> int:
    """Deleting u->v can only make the tail u newly strong."""
    checks = 0
    for tail, row in enumerate(rows):
        heads = row
        while heads:
            edge = heads & -heads
            head = edge.bit_length() - 1
            heads ^= edge
            deleted = rows[:]
            deleted[tail] &= ~edge
            for root in range(len(rows)):
                if root == tail:
                    continue
                need(deleted[root] == rows[root],
                     "non-tail first neighborhood changed under deletion")
                need(exact_second(deleted, root) & ~exact_second(rows, root) == 0,
                     "non-tail second neighborhood grew under deletion")
                checks += 1
    return checks


def check_small_graphs() -> dict[str, int | str]:
    graphs = roots = strong_roots = minimal_witnesses = deletion_checks = 0
    digest = sha256()
    for order in range(2, 6):
        graph_total = 3 ** (order * (order - 1) // 2)
        for code in range(graph_total):
            rows = decode_oriented_graph(order, code)
            check_dominating_extension(rows)
            deletion_checks += check_arc_deletion_monotonicity(rows)
            for root in range(order):
                rank = matching_rank(rows, root)
                deficiency, minimal = hall_data(rows, root)
                degree = rows[root].bit_count()
                need(deficiency == degree - rank,
                     "matching rank and direct Hall deficiency disagree")
                for source, target in minimal:
                    check_minimal_witness(rows, source, target)
                strong_roots += rank == degree
                minimal_witnesses += len(minimal)
                roots += 1
                digest.update(bytes((order, root, degree, rank, deficiency, len(minimal))))
            graphs += 1
    return {
        "oriented_graphs": graphs,
        "root_checks": roots,
        "strong_root_checks": strong_roots,
        "minimal_hall_witnesses": minimal_witnesses,
        "arc_deletion_subset_checks": deletion_checks,
        "entry_digest": digest.hexdigest(),
    }


def check_case_partition() -> list[str]:
    cases: list[str] = []
    for source_size in range(3, 7):
        if source_size < 6:
            cases.append(f"s{source_size}")
            continue
        for maximum in range(1, 6):
            if maximum <= 3:
                cases.append(f"s6-m{maximum}")
            else:
                cases.extend(f"s6-m{maximum}-p{degree}" for degree in range(6, 9))
    need(len(cases) == 12 and len(set(cases)) == 12,
         "the structural partition is not twelve disjoint labels")
    return cases


def check_ternary_columns() -> int:
    checked = 0
    for source_size in range(3, 7):
        for digits in product(range(3), repeat=source_size):
            code = sum(digit * 3 ** index for index, digit in enumerate(digits))
            recovered = tuple((code // 3 ** index) % 3 for index in range(source_size))
            need(recovered == digits, "ternary target-column code is not injective")
            checked += 1
    return checked


def check_manifest(cases: list[str]) -> dict[str, int | str]:
    data = (TARGET / "manifest.json").read_bytes()
    manifest = json.loads(data)
    records = manifest["cases"]
    need([record["case"] for record in records] == cases,
         "manifest case order or coverage differs from the reduction")
    need(all(record["proof_verified"] is True for record in records),
         "manifest contains an unchecked proof")
    need(all(len(record["cnf_sha256"]) == 64 and len(record["drat_sha256"]) == 64
             for record in records), "manifest contains a malformed digest")
    return {
        "manifest_sha256": sha256(data).hexdigest(),
        "manifest_cases": len(records),
        "manifest_variables_min": min(record["variables"] for record in records),
        "manifest_variables_max": max(record["variables"] for record in records),
        "manifest_clauses_min": min(record["clauses"] for record in records),
        "manifest_clauses_max": max(record["clauses"] for record in records),
        "manifest_drat_bytes": sum(record["drat_bytes"] for record in records),
    }


def main() -> None:
    # With 15 vertices there are at most C(15,2)=105 arcs.  Minimum
    # out-degree seven already contributes 105, forcing a 7-regular tournament.
    need(15 * 7 == 15 * 14 // 2, "degree-seven reduction arithmetic failed")
    # Arc-minimality gives d-1 <= 15-d, hence d <= 8.
    need(max(d for d in range(15) if d - 1 <= 15 - d) == 8,
         "arc-minimal degree upper bound failed")

    cases = check_case_partition()
    result = {
        "status": "INDEPENDENT STRUCTURAL AUDIT PASSED",
        "case_labels": cases,
        "degree_seven_forces_regular_tournament": True,
        "arc_minimal_maximum_degree": 8,
        "ternary_columns_checked": check_ternary_columns(),
        **check_small_graphs(),
        **check_manifest(cases),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
