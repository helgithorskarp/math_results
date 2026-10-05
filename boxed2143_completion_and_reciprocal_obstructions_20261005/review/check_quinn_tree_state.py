#!/usr/bin/env python3
"""Independent exact check of Quinn's frozen maximum-tree quotient.

Naive value-neighbor construction, ancestor walks and a heap representative
are used instead of the author's recursive shape-splitting implementation.
Finite checks do not supply the missing uniform weight or entropy bound.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time

from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def neighbors(p):
    return tuple((next((i for i in range(j - 1, -1, -1) if p[i] > x), None),
                  next((i for i in range(j + 1, len(p)) if p[i] > x), None))
                 for j, x in enumerate(p))


def naive_shape(p):
    """Build by smaller nearest-greater parent, with iterative postorder."""
    if not p:
        return ()
    links = neighbors(p)
    children = [[None, None] for _ in p]
    root = None
    for j, (left, right) in enumerate(links):
        if left is None and right is None:
            require(root is None, "Multiple roots")
            root = j
            continue
        parent = right if left is None else left if right is None else min((left, right), key=p.__getitem__)
        side = int(j > parent)
        require(children[parent][side] is None, "Multiple children on one side")
        children[parent][side] = j
    shapes = {}
    stack = [(root, False)]
    while stack:
        j, visited = stack.pop()
        if visited:
            shapes[j] = tuple(() if child is None else shapes[child] for child in children[j])
        else:
            stack.append((j, True))
            stack.extend((child, False) for child in children[j] if child is not None)
    return shapes[root]


def naive_blockers(p):
    return tuple((left, j, right) for j, (left, right) in enumerate(neighbors(p))
                 if left is not None and right is not None and p[left] < p[right])


def legal_from_values(p):
    forbidden = {gap for _, j, right in naive_blockers(p) for gap in range(j + 1, right + 1)}
    return tuple(gap for gap in range(len(p) + 1) if gap not in forbidden)


def heap_representative(tree):
    """Assign increasing ranks in postorder, read them in inorder."""
    result = []
    rank = 0

    def assign(node):
        nonlocal rank
        if not node:
            return []
        left = assign(node[0])
        right = assign(node[1])
        rank += 1
        return left + [rank] + right

    result = assign(tree)
    require(naive_shape(tuple(result)) == tree, "Heap representative has wrong shape")
    return tuple(result)


def word(tree):
    return "." if not tree else "(" + word(tree[0]) + word(tree[1]) + ")"


def file_record(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-dir", type=Path, default=Path(
        "/scratch/research-team-colloquium-sol61-20261005/workspaces/literature-researcher-3/boxed2143_quinn_20261005"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    source = args.author_dir
    manifest = json.loads((source / "TREE_STATE_MANIFEST_V1.json").read_text())
    before = {name: file_record(source / name) for name in manifest["files"]}
    require(before == manifest["files"], "Frozen tree packet changed")
    require(file_record(source / "MANIFEST.json")["sha256"] == manifest["dependencies"]["MANIFEST.json"],
            "Kernel dependency manifest changed")
    sys.path.insert(0, str(source))
    spec = importlib.util.spec_from_file_location("quinn_tree_reviewed", source / "tree_dynamics.py")
    require(spec is not None and spec.loader is not None, "Cannot load author source")
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    start = time.perf_counter()
    digest = hashlib.sha256()
    parents = children_checked = 0
    literal_fibers = []
    for n in range(8):
        fibers = defaultdict(int)
        count = 0
        for p in itertools.permutations(range(1, n + 1)):
            count += 1
            parents += 1
            shape = naive_shape(p)
            require(shape == author.cartesian_shape(p), f"Shape mismatch at {p}")
            blockers = naive_blockers(p)
            got = tuple((b.left, b.minimum, b.right) for b in author.shape_blockers(shape))
            require(got == blockers, f"Shape blocker mismatch at {p}")
            gaps = legal_from_values(p)
            require(gaps == author.shape_legal_gaps(shape), f"Legal gap mismatch at {p}")
            old = boxed_occurrences(p)
            if not old:
                fibers[shape] += 1
            for gap in range(n + 1):
                child = p[:gap] + (n + 1,) + p[gap:]
                split = (naive_shape(p[:gap]), naive_shape(p[gap:]))
                child_shape = naive_shape(child)
                require(split == child_shape == author.split(shape, gap), f"Split mismatch at {p}, {gap}")
                require(child_shape == author.insert_maximum_shape(shape, gap), "Child-state mismatch")
                if not old:
                    require((not boxed_occurrences(child)) == (gap in gaps), "Avoiding-history transition mismatch")
                children_checked += 1
            digest.update((json.dumps([p, word(shape), blockers, gaps], separators=(",", ":")) + "\n").encode())
        require(count == math.factorial(n), "Incomplete labelled enumeration")
        literal_fibers.append(dict(fibers))

    # Separate implementation of weighted transitions via value representatives.
    weights = {(): 1}
    rows = []
    expected = json.loads((source / "tree_weights_n10.json").read_text())["records"]
    for n in range(11):
        if n <= 7:
            require(weights == literal_fibers[n], f"Full weighted fiber mismatch at {n}")
        stream = hashlib.sha256()
        for tree, weight in sorted(weights.items(), key=lambda item: word(item[0])):
            stream.update((word(tree) + ":" + str(weight) + "\n").encode())
        row = {"n": n, "states": len(weights), "avoiders": sum(weights.values()),
               "max_avoiding_single_tree_fiber": max(weights.values()),
               "state_weight_stream_sha256": stream.hexdigest()}
        require(all(row[key] == expected[n][key] for key in row), f"Author table mismatch at {n}")
        rows.append(row)
        if n < 10:
            new = defaultdict(int)
            for tree, weight in weights.items():
                p = heap_representative(tree)
                for gap in legal_from_values(p):
                    child = p[:gap] + (n + 1,) + p[gap:]
                    new[naive_shape(child)] += weight
            weights = dict(new)

    # Shape equivalence is expressly not a current-avoidance decision.
    require(naive_shape((2, 1, 4, 3)) == naive_shape((3, 1, 4, 2)), "Collision shape mismatch")
    require(bool(boxed_occurrences((2, 1, 4, 3))) and not boxed_occurrences((3, 1, 4, 2)),
            "Collision occurrence mismatch")
    for gap in (-1, 3, True, 0.0):
        try:
            author.split(((), ()), gap)
        except ValueError:
            pass
        else:
            raise RuntimeError("Invalid split gap accepted")
    after = {name: file_record(source / name) for name in before}
    require(after == before, "Source changed during check")
    report = {"author": "literature-researcher-3", "checker": "literature-researcher-4",
              "decision_message_id": 410, "full_target_solved": False,
              "checked_scope": "arbitrary-size written quotient proof; finite all-shape blockers, splits, transitions and weights",
              "proof_sha256": before["TREE_STATE_LEMMA.md"]["sha256"],
              "manifest_sha256": file_record(source / "TREE_STATE_MANIFEST_V1.json")["sha256"],
              "source_files": before, "labelled_parents": parents, "maximum_insertions": children_checked,
              "state_stream_sha256": digest.hexdigest(), "weighted_rows": rows,
              "complete_fibers_definition_checked_through": 7, "python": platform.python_version(),
              "seconds": time.perf_counter() - start,
              "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key not in ("source_files", "weighted_rows")}, indent=2))


if __name__ == "__main__":
    main()
