#!/usr/bin/env python3
"""Reproduce and audit the published ACD D(10,9) cover labels."""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from exact_covers import adjacent_level_covers, compute  # noqa: E402


FILES = {
    "lattice_paths_10x9_train.jsonl": {
        "url": "https://huggingface.co/datasets/ACDRepo/partial_orders_on_lattice_paths_10x9/resolve/main/lattice_paths_10x9_train.jsonl",
        "sha256": "1faaeb935ba2dfb52e11f403199a7462f948c8b4521bff2443cb96cfa100ccc3",
    },
    "lattice_paths_10x9_test.jsonl": {
        "url": "https://huggingface.co/datasets/ACDRepo/partial_orders_on_lattice_paths_10x9/resolve/main/lattice_paths_10x9_test.jsonl",
        "sha256": "8eec0d679795b4620be3f5ce0e15a027d10db0988b17408ace71011dedc06100",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def obtain_data(scratch_dir: Path) -> list[Path]:
    scratch_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name, metadata in FILES.items():
        destination = scratch_dir / name
        if not destination.exists() or sha256(destination) != metadata["sha256"]:
            with urlopen(metadata["url"], timeout=60) as response:
                destination.write_bytes(response.read())
        actual = sha256(destination)
        if actual != metadata["sha256"]:
            raise SystemExit(f"source-data hash mismatch for {name}: {actual}")
        paths.append(destination)
    return paths


def load_published(paths: list[Path]):
    by_label = defaultdict(set)
    row_counts = defaultdict(int)
    for path in paths:
        with path.open() as stream:
            for line in stream:
                row = json.loads(line)
                label = row["Label"]
                pair = (tuple(row["Lattice path 1"]), tuple(row["Lattice path 2"]))
                by_label[label].add(pair)
                row_counts[label] += 1
    if any(row_counts[label] != len(by_label[label]) for label in by_label):
        raise SystemExit("published data contain duplicate rows within a label")
    return by_label


def audit(data_paths: list[Path]) -> dict[str, object]:
    exact = compute()
    published = load_published(data_paths)
    matching_covers = exact["matching_covers"]
    exact_lagrange_covers = exact["lagrange_covers"]

    # In the notebook D_l.items() is sorted by itemgetter(1,0,-1).
    # Item 1 is the value list [(path, float_L), ...], so the primary key is
    # the first inserted path, not L.  Distinct groups have distinct first paths.
    notebook_levels = sorted(exact["raw_lagrange_groups"].values(), key=lambda group: group[0])
    notebook_lagrange_covers = adjacent_level_covers(notebook_levels)
    notebook_common = matching_covers & notebook_lagrange_covers
    excluded_lower_paths = {lower for lower, _ in notebook_common}
    predicted_matching = {
        pair for pair in matching_covers if pair[0] not in excluded_lower_paths
    }
    predicted_lagrange = {
        pair for pair in notebook_lagrange_covers if pair[0] not in excluded_lower_paths
    }

    if published[0] != predicted_matching or published[1] != predicted_lagrange:
        raise SystemExit("independent notebook reconstruction does not reproduce published rows")

    scores = exact["lagrange_scores"]
    false_lagrange = published[1] - exact_lagrange_covers
    reverse_exact_cover = {
        pair for pair in false_lagrange if (pair[1], pair[0]) in exact_lagrange_covers
    }
    direction_correct_noncover = {
        pair for pair in false_lagrange if scores[pair[0]] < scores[pair[1]]
    }
    direction_wrong = {
        pair for pair in false_lagrange if scores[pair[0]] > scores[pair[1]]
    }

    inversions = 0
    previous = None
    for group in notebook_levels:
        score = scores[group[0]]
        if previous is not None and previous > score:
            inversions += 1
        previous = score

    exact_common = matching_covers & exact_lagrange_covers
    return {
        "notebook_lagrange_level_count": len(notebook_levels),
        "notebook_adjacent_level_inversions": inversions,
        "published_matching_rows": len(published[0]),
        "published_lagrange_rows": len(published[1]),
        "published_matching_true_matching_covers": len(published[0] & matching_covers),
        "published_matching_false_matching_covers": len(published[0] - matching_covers),
        "published_matching_also_true_lagrange_covers": len(
            published[0] & exact_lagrange_covers
        ),
        "published_lagrange_true_lagrange_covers": len(
            published[1] & exact_lagrange_covers
        ),
        "published_lagrange_false_lagrange_covers": len(false_lagrange),
        "false_lagrange_rows_wrong_direction": len(direction_wrong),
        "false_lagrange_rows_reverse_exact_cover": len(reverse_exact_cover),
        "false_lagrange_rows_correct_direction_but_noncover": len(direction_correct_noncover),
        "exact_common_covers": len(exact_common),
        "corrected_matching_only_rows": len(matching_covers - exact_common),
        "corrected_lagrange_only_rows": len(exact_lagrange_covers - exact_common),
        "all_published_rows_reproduced_from_notebook_logic": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scratch-dir",
        type=Path,
        default=Path("/scratch/acd_lagrange_cover_correction"),
    )
    args = parser.parse_args()
    actual = audit(obtain_data(args.scratch_dir))
    expected = json.loads((ROOT / "certificate.json").read_text())["published_audit"]
    if actual != expected:
        raise SystemExit(
            "audit certificate mismatch:\n"
            + json.dumps({"expected": expected, "actual": actual}, indent=2, sort_keys=True)
        )
    print(json.dumps(actual, indent=2, sort_keys=True))
    print("PUBLISHED DATA AUDIT VERIFIED")


if __name__ == "__main__":
    main()
