#!/usr/bin/env python3
"""Reviewer-owned exhaustive audit for the six-quotient classification.

This checker imports no target module.  It binds the reviewed source by hash,
compiles a separate canonical-augmentation audit, and checks the two minimum
blow-ups directly from the definition of a strong Seymour vertex.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "strong_seymour_six_oriented_quotients"
SOURCE_COMMIT = "c4a7893cf346a8a761d05f3195b06b542249b94c"

TARGET_HASHES = {
    ".gitignore": "a7d3ec2efb2be8ee8da74403ec1b1bc0ab32cbe92efabe5aca57aa5b2c7613b4",
    "EXPECTED_INDEPENDENT.json": "d0dad08f12f3fc249a7a7fd5222362c911a7d83929b2318f7b96192595875bf4",
    "EXPECTED_PRIMARY.json": "2fd8a49b3e48b0fe0676b03cae4564f28febaecb546834d120f6e6d2c8f33f77",
    "PROOF.md": "5318ce7be5da6c98a5fa74fa25a9b07153a7ca12cf4721391bb9cc0987ac548f",
    "README.md": "28f44a097188b64a9b922613504dd7a0a5aaf9cafb03e28e62fe0960cf8d41f8",
    "SHA256SUMS": "3fe0d088ca7eadea4f4cb1267c4753a059abedc808352c1999fa4442e141f42c",
    "SOURCES.md": "a3173a93406a908383e300a0954b940a669b01283db44c89c91c177641d80ca4",
    "certificate.json": "3e93c4998c6f85c69c0fdeeebfb1045bef8399c200151af9eb65cd605d421fcc",
    "construction.py": "910c04e5848fefab233ad39242229f88615e697b545d7530352c2635ca7a9b6f",
    "independent_check.py": "f596259383c0aa7fcff00d29d57abae4a738690276209ec20ea6c24c6d8e3845",
    "orbit_audit.cpp": "328b39e7c057d00f297660b6835e83e318f558e9b52f9600aa9e7d8003c58f09",
    "oriented51.txt": "0e9d97df51533eeafe98070f841adf2e1fa57d0a946051d17ecc743e197fddfc",
    "requirements-independent.txt": "9cd18f59b731510e819dea6d1f0a74e4d7a1283561f43548cbc16d9e57710d91",
    "verify.py": "33909bea162b23bb681a5a44316ed25a62eae68b5cec2cd3afd35cc3ce17fdc4",
}

QUOTIENTS = {
    "tournament": ((1, 2, 3), (2, 3, 4), (3, 5), (4, 5), (0, 2), (0, 1, 4)),
    "missing_arc": ((2, 3), (4, 5), (1, 3, 4), (1, 5), (0, 3, 5), (0, 2)),
}
WEIGHTS = {
    "tournament": (7, 3, 9, 3, 3, 11),
    "missing_arc": (3, 8, 16, 3, 7, 14),
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind_target() -> str:
    actual_names = {path.name for path in TARGET.iterdir() if path.is_file()}
    need(actual_names == set(TARGET_HASHES), "reviewed target file set changed")
    for name, expected in TARGET_HASHES.items():
        need(sha256(TARGET / name) == expected, f"reviewed target hash changed: {name}")
    digest = hashlib.sha256()
    for name in sorted(TARGET_HASHES):
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update((TARGET / name).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def run_native(sanitize: bool) -> dict:
    with tempfile.TemporaryDirectory(prefix="six-quotient-review-") as temporary:
        binary = Path(temporary) / "review-audit"
        flags = (
            ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
            if sanitize else ["-O3"]
        )
        subprocess.run(
            [
                "g++", "-std=c++20", *flags, "-Wall", "-Wextra", "-Wconversion",
                "-Wshadow", "-pedantic", str(HERE / "review_audit.cpp"), "-o", str(binary),
            ],
            check=True,
        )
        completed = subprocess.run([binary], check=True, capture_output=True, text=True)
    result = json.loads(completed.stdout)
    need(result["status"] == "REVIEWER EXHAUSTIVE CLASSIFICATION VERIFIED", "native status")
    return result


def deficiencies(quotient: tuple[tuple[int, ...], ...], weights: tuple[int, ...]) -> list[int]:
    result = []
    for root, out_neighbors in enumerate(quotient):
        best = 0
        for mask in range(1 << len(out_neighbors)):
            source = {out_neighbors[index] for index in range(len(out_neighbors)) if mask >> index & 1}
            reached = set().union(*(quotient[vertex] for vertex in source)) if source else set()
            target = reached - set(out_neighbors) - {root}
            best = max(best, sum(weights[v] for v in source) - sum(weights[v] for v in target))
        result.append(best)
    return result


def construct(
    quotient: tuple[tuple[int, ...], ...], weights: tuple[int, ...], transitive: bool
) -> list[set[int]]:
    labels = [part for part, size in enumerate(weights) for _ in range(size)]
    return [
        {
            j
            for j, other in enumerate(labels)
            if (part == other and i < j and transitive)
            or (part != other and other in quotient[part])
        }
        for i, part in enumerate(labels)
    ]


def matching_size(graph: list[set[int]], vertex: int) -> int:
    left = sorted(graph[vertex])
    right = set().union(*(graph[source] for source in left)) - graph[vertex] - {vertex}
    mates: dict[int, int] = {}

    def augment(source: int, seen: set[int]) -> bool:
        for target in sorted(graph[source] & right):
            if target in seen:
                continue
            seen.add(target)
            if target not in mates or augment(mates[target], seen):
                mates[target] = source
                return True
        return False

    return sum(augment(source, set()) for source in left)


def expanded_checks() -> list[dict]:
    results = []
    for family in ("tournament", "missing_arc"):
        quotient, weights = QUOTIENTS[family], WEIGHTS[family]
        for transitive in (False, True):
            graph = construct(quotient, weights, transitive)
            profile = [[len(graph[v]), matching_size(graph, v)] for v in range(len(graph))]
            need(all(out_degree > matching for out_degree, matching in profile), "strong vertex found")
            if family == "missing_arc" and transitive:
                literal = (TARGET / "oriented51.txt").read_text().splitlines()
                encoded = ["".join("1" if j in graph[i] else "0" for j in range(len(graph)))
                           for i in range(len(graph))]
                need(encoded == literal, "literal 51-vertex graph mismatch")
            results.append(
                {
                    "family": family,
                    "transitive": transitive,
                    "order": len(graph),
                    "minimum_out_degree": min(map(len, graph)),
                    "profile_sha256": hashlib.sha256(
                        json.dumps(profile, separators=(",", ":")).encode()
                    ).hexdigest(),
                }
            )
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sanitize", action="store_true")
    arguments = parser.parse_args()
    output = {
        "status": "INDEPENDENT REVIEW OF SIX-QUOTIENT CLASSIFICATION VERIFIED",
        "source_commit": SOURCE_COMMIT,
        "target_files_bound": len(TARGET_HASHES),
        "target_tree_sha256": bind_target(),
        "native_audit": run_native(arguments.sanitize),
        "minimum_weight_deficiencies": {
            family: deficiencies(QUOTIENTS[family], WEIGHTS[family])
            for family in ("tournament", "missing_arc")
        },
        "expanded_checks": expanded_checks(),
    }
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
