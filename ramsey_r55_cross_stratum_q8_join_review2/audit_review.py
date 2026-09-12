#!/usr/bin/env python3
"""Independent scope/guard audit for the cross-stratum q8 join.

This checker deliberately imports no module from the reviewed contribution.
It checks the public dependency pins and original-task ranges, reconstructs
the 239-leaf Boolean partition, verifies every catalog core against all node
counts, and matches the historical 956 active worker definitions literally.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


TARGET_COMMIT = "168df04f5d4f7a28a0ed068db2511a2ce950e009"
COHORT_SHA256 = "b469c44558a0d39c2a4e04171096f419b5509dcf42609ef130e60e632fae6551"
CORES_SHA256 = "ca6d60b50d01ae460941cffa4e843a81fcbe33a8e5d37ea6e1fe568e2f5c95cc"
ACTIVE_SHA256 = "8d99904405a54c3f2447ddf339e3e93bb70244338a072334e7158fa20c514392"
CORE_COUNTS = {7: 640, 8: 546356, 9: 362, 10: 4}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def route(q: int, r: int) -> str:
    if (q >= 8 and r <= 8) or (q == 7 and r in (5, 6)):
        return "Q8_PHYSICAL"
    return "ORIGINAL_PARENT"


def expected_ranges() -> list[dict]:
    rows = []
    for q in range(7, 11):
        for r in range(5, q + 1):
            count = CORE_COUNTS[q]
            rows.append(
                {
                    "q": q,
                    "r": r,
                    "first": f"bo1-q{q}-r{r}-c000000",
                    "last": f"bo1-q{q}-r{r}-c{count - 1:06d}",
                    "count": count,
                    "route": route(q, r),
                }
            )
    return rows


def audit_dependencies(repository: Path, target: Path) -> int:
    manifest = load_json(target / "DEPENDENCIES.json")
    rows = manifest["files"]
    require(len(rows) == 165, "unexpected dependency count")
    require(len({row["path"] for row in rows}) == len(rows), "duplicate dependency path")
    for row in rows:
        path = repository / row["path"]
        require(path.is_file(), f"missing dependency: {row['path']}")
        require(sha256(path) == row["sha256"], f"dependency hash mismatch: {row['path']}")
    require(manifest["q8_source_commit"] == "7e2ba1869f74410126d0fc1f2e89b92531e651c4", "q8 source pin")
    require(manifest["local19_source_commit"] == "d03ccef7effe9ec3f311b90cc3dfac32a82cf452", "local source pin")
    require(manifest["core_exchange_clauses_used"] is False, "order-5/core-exchange premise admitted")
    require(manifest["full_local19_proof_recheck_required"] is True, "local proof replay not required")
    return len(rows)


def audit_registry(repository: Path, target: Path) -> tuple[list[dict], dict]:
    wanted = expected_ranges()
    original = load_json(repository / "ramsey_r55_maximal_block_order" / "TASKS.json")
    require(original["format"] == "bo1", "registry format")
    require(original["macro_classes"] == 18 and len(original["classes"]) == 18, "registry class count")
    require(original["tasks"] == 2189178, "registry total")
    for expected, actual in zip(wanted, original["classes"]):
        observed = {
            "q": actual["q"],
            "r": actual["r"],
            "first": actual["first_task"],
            "last": actual["last_task"],
            "count": actual["core_stop"] - actual["core_start"],
            "route": route(actual["q"], actual["r"]),
        }
        require(actual["core_start"] == 0 and observed == expected, "registry range mismatch")

    cover = load_json(target / "COVER.json")
    require(cover["ranges"] == wanted, "published cover ranges differ")
    routed = sum(row["count"] for row in wanted if row["route"] == "Q8_PHYSICAL")
    parents = sum(row["count"] for row in wanted if row["route"] == "ORIGINAL_PARENT")
    payoffs = {
        str(r): sum(row["count"] for row in wanted if row["route"] == "Q8_PHYSICAL" and row["r"] == r)
        for r in range(5, 9)
    }
    require((routed, parents) == (2188168, 1010), "route totals")
    require(routed + parents == original["tasks"], "route is not a partition")
    require(payoffs == {"5": 547362, "6": 547362, "7": 546722, "8": 546722}, "conditional payoffs")
    require(cover["routed_ids"] == routed and cover["unrouted_original_parents"] == parents, "cover totals")
    require(cover["whole_r_family_conditional_payoffs"] == payoffs, "cover payoff table")
    return wanted, {"original_ids": original["tasks"], "routed_ids": routed, "retained_parents": parents, "payoffs": payoffs}


def assumptions(mask: int, value: int) -> list[int]:
    return [(802 + bit) * (1 if value >> bit & 1 else -1) for bit in range(55) if mask >> bit & 1]


def audit_tree(cohort_path: Path, core_path: Path) -> tuple[list[tuple[int, int, int]], dict]:
    require(sha256(cohort_path) == COHORT_SHA256, "cohort tree hash")
    require(sha256(core_path) == CORES_SHA256, "core stream hash")
    tree = load_json(cohort_path)
    nodes = tree["nodes"]
    require(tree["root"] == 0 and len(nodes) == 477, "tree framing")
    visited: set[int] = set()
    leaves: dict[int, tuple[int, int, int]] = {}

    def walk(index: int, mask: int, value: int) -> None:
        require(type(index) is int and 0 <= index < len(nodes), "node reference")
        require(index not in visited, "tree is cyclic or reuses a node")
        visited.add(index)
        node = nodes[index]
        require(node["id"] == index, "node id")
        require(int(node["mask"], 16) == mask and int(node["value"], 16) == value, "node cylinder")
        if "leaf" in node:
            leaf = node["leaf"]
            require(type(leaf) is int and leaf not in leaves, "leaf id")
            leaves[leaf] = (mask, value, node["count"])
            return
        bit = node["bit"]
        require(type(bit) is int and 0 <= bit < 55 and not (mask >> bit & 1), "split bit")
        walk(node["zero"], mask | (1 << bit), value)
        walk(node["one"], mask | (1 << bit), value | (1 << bit))

    walk(0, 0, 0)
    require(visited == set(range(477)), "unreachable node")
    require(sorted(leaves) == list(range(239)), "leaf range")
    ordered = [leaves[i] for i in range(239)]
    lengths: dict[int, int] = {}
    volume = 0
    for mask, value, _ in ordered:
        require(value & ~mask == 0, "leaf value outside mask")
        length = mask.bit_count()
        lengths[length] = lengths.get(length, 0) + 1
        volume += 1 << (55 - length)
    require(lengths == {7: 17, 8: 222}, "guard lengths")
    require(volume == 1 << 55, "Boolean cylinders do not cover full cube")

    raw = core_path.read_bytes()
    require(raw[:8] == b"Q8CORE1\n", "core stream magic")
    require(len(raw) == 12 + 546356 * 8, "core stream length")
    require(struct.unpack_from("<I", raw, 8)[0] == 546356, "core stream count")
    words = [word for (word,) in struct.iter_unpack("<Q", raw[12:])]
    require(all(word < 1 << 55 for word in words), "core padding")
    require(len(set(words)) == len(words), "duplicate literal core word")
    observed = [0] * len(nodes)
    core_leaf_counts = [0] * 239
    for word in words:
        index = 0
        while True:
            observed[index] += 1
            node = nodes[index]
            if "leaf" in node:
                core_leaf_counts[node["leaf"]] += 1
                break
            index = node["one"] if word >> node["bit"] & 1 else node["zero"]
    require(all(observed[i] == node["count"] for i, node in enumerate(nodes)), "node catalog counts")
    require(core_leaf_counts == [count for _, _, count in ordered], "leaf catalog counts")
    return ordered, {
        "nodes": 477,
        "leaves": 239,
        "guard_lengths": {str(k): v for k, v in lengths.items()},
        "boolean_volume": str(volume),
        "catalog_core_words": len(words),
        "smallest_leaf": min(core_leaf_counts),
        "largest_leaf": max(core_leaf_counts),
    }


def audit_active(path: Path, guards: list[tuple[int, int, int]]) -> dict:
    require(sha256(path) == ACTIVE_SHA256, "historical active queue hash")
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    require(len(rows) == 956, "active queue length")
    expected = []
    for r in range(5, 9):
        for leaf, (mask, value, core_count) in enumerate(guards):
            expected.append((r, leaf, core_count, assumptions(mask, value), [119] if r == 8 else []))
    seen = set()
    for row, (r, leaf, core_count, units, edge_cube) in zip(rows, expected):
        parent = row["parent"]
        worker = row["worker_job"]
        require((parent["r"], parent["cohort"], parent["original_tasks"]) == (r, leaf, core_count), "active parent identity")
        require(parent["assumptions"] == units, "active parent guard")
        require(parent["status"] == "PENDING_PHYSICAL43_COHORT" and parent["target_solver_calls"] == 0, "active parent status")
        require(worker == {"r": r, "core_assumptions": units, "edge_cube": edge_cube}, "worker definition")
        require(row["status"] == "UNKNOWN", "non-UNKNOWN active worker")
        seen.add((r, leaf))
    require(len(seen) == 956, "duplicate active job")
    return {"active_jobs": len(rows), "unknown_jobs": len(rows), "r8_positive_edge_jobs": 239}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    parser.add_argument("cohorts", type=Path)
    parser.add_argument("cores", type=Path)
    parser.add_argument("active_queue", type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    target = repository / "ramsey_r55_cross_stratum_q8_join"
    dependencies = audit_dependencies(repository, target)
    _, registry = audit_registry(repository, target)
    guards, tree = audit_tree(args.cohorts, args.cores)
    active = audit_active(args.active_queue, guards)
    result = {
        "status": "INDEPENDENT_Q8_CROSS_STRATUM_SCOPE_AUDIT_VERIFIED",
        "target_commit": TARGET_COMMIT,
        "dependency_files_checked": dependencies,
        **registry,
        **tree,
        **active,
        "exact_integer_arithmetic": True,
        "imports_reviewed_contribution_modules": False,
        "proof_traces_checked_by_this_script": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
