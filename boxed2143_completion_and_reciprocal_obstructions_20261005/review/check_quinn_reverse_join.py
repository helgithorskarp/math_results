#!/usr/bin/env python3
"""Theo's separate exact check of Quinn's reverse merges and join certificate.

No author executable is imported. State transitions use a postorder heap
representative, direct nearest-greater value scans and a monotone-stack tree
builder, instead of the author's recursive tree split/ancestor gap rule.
The all-size counting proof and its accepted quotient dependency are reviewed
in QUINN_REVERSE_JOIN_REVIEW.md. Finite data does not solve target410.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def record(path):
    data = path.read_bytes()
    return {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def shape(values):
    """Cartesian tree from an increasing-index monotone value stack."""
    if not values:
        return ()
    left = [-1] * len(values)
    right = [-1] * len(values)
    stack = []
    for j, value in enumerate(values):
        removed = -1
        while stack and values[stack[-1]] < value:
            removed = stack.pop()
        if stack:
            right[stack[-1]] = j
        left[j] = removed
        stack.append(j)
    root = stack[0]
    built = {-1: ()}
    pending = [(root, False)]
    while pending:
        j, visited = pending.pop()
        if visited:
            built[j] = built[left[j]], built[right[j]]
        else:
            pending.append((j, True))
            for child in (left[j], right[j]):
                if child != -1:
                    pending.append((child, False))
    return built[root]


@lru_cache(maxsize=None)
def word(tree):
    return "." if not tree else "(" + word(tree[0]) + word(tree[1]) + ")"


@lru_cache(maxsize=None)
def representative(tree):
    """Ranks assigned in postorder, output in inorder; arbitrary heap label."""
    if not tree:
        return ()
    left = representative(tree[0])
    right = representative(tree[1])
    return left + (len(left) + len(right) + 1,) + tuple(x + len(left) for x in right)


def value_legal_gaps(values):
    """Only new-maximum blockers, computed directly from value neighbors."""
    n = len(values)
    forbidden = set()
    for j, value in enumerate(values):
        previous = next((i for i in range(j - 1, -1, -1) if values[i] > value), None)
        following = next((i for i in range(j + 1, n) if values[i] > value), None)
        if previous is not None and following is not None and values[previous] < values[following]:
            forbidden.update(range(j + 1, following + 1))
    return tuple(g for g in range(n + 1) if g not in forbidden)


@lru_cache(maxsize=None)
def transitions(tree):
    values = representative(tree)
    require(shape(values) == tree, "Representative lost its tree")
    return {gap: shape(values[:gap] + (len(values) + 1,) + values[gap:])
            for gap in value_legal_gaps(values)}


def clear_geometry():
    transitions.cache_clear()
    representative.cache_clear()
    word.cache_clear()


def spine_merges(left, right):
    """Enumerate shuffle positions, reconstruct the parent from bottom up."""
    l_off, r_off = [], []
    node = left
    while node:
        l_off.append(node[0])
        node = node[1]
    node = right
    while node:
        r_off.append(node[1])
        node = node[0]
    for selected in itertools.combinations(range(len(l_off) + len(r_off)), len(l_off)):
        selected = set(selected)
        letters = "".join("L" if j in selected else "R" for j in range(len(l_off) + len(r_off)))
        a, b = len(l_off), len(r_off)
        tree = ()
        for letter in reversed(letters):
            if letter == "L":
                a -= 1
                tree = l_off[a], tree
            else:
                b -= 1
                tree = tree, r_off[b]
        yield letters, tree


def admissible(letters):
    first_r = letters.find("R")
    return first_r < 0 or "LL" not in letters[first_r:]


def perfect(height):
    tree = ()
    for _ in range(height):
        tree = tree, tree
    return tree


def check_reverse(source):
    expected = json.loads((source / "reverse_merges_check.json").read_text())
    weights = {(): 1}
    prior = {}
    stream = hashlib.sha256()
    merges = 0
    rows = []
    for n in range(11):
        for child, child_weight in weights.items():
            if not child:
                continue
            cut = len(representative(child[0]))
            parents = set()
            incoming = 0
            for letters, parent in spine_merges(*child):
                require(parent not in parents, "Merge-word collision")
                parents.add(parent)
                values = representative(parent)
                require((shape(values[:cut]), shape(values[cut:])) == child, "Wrong parent restriction")
                legal = cut in value_legal_gaps(values)
                require(legal == admissible(letters), "Grammar/value disagreement")
                if legal:
                    incoming += prior[parent]
                stream.update((word(child) + ":" + letters + ":" + str(legal) + "\n").encode())
                merges += 1
            require(incoming == child_weight, "Incoming/outgoing weight mismatch")
        row = {"n": n, "states_compared": len(weights), "avoiders": sum(weights.values())}
        require(row == expected["rows"][n], "Forward table mismatch")
        rows.append(row)
        if n < 10:
            new = defaultdict(int)
            for parent, weight in weights.items():
                for child in transitions(parent).values():
                    new[child] += weight
            prior, weights = weights, dict(new)
            clear_geometry()
    require(merges == expected["all_merge_candidates_checked"], "Wrong complete merge count")
    require(stream.hexdigest() == expected["merge_stream_sha256"], "Full merge stream mismatch")
    clear_geometry()
    processed = 0

    @lru_cache(maxsize=None)
    def reverse_weight(tree):
        nonlocal processed
        if not tree:
            return 1
        cut = len(representative(tree[0]))
        total = 0
        for letters, parent in spine_merges(*tree):
            # Use independent value geometry in the count, not just the grammar.
            if cut in value_legal_gaps(representative(parent)):
                require(admissible(letters), "Unexpected accepted word")
                total += reverse_weight(parent)
                processed += 1
        return total

    balanced = [reverse_weight(perfect(h)) for h in range(1, 5)]
    require(balanced == [row["avoiding_fiber"] for row in expected["perfect_tree_controls"]],
            "Balanced reverse counts disagree")
    states = reverse_weight.cache_info().currsize
    clear_geometry()
    return {"merges_checked": merges, "merge_stream_sha256": stream.hexdigest(),
            "rows": rows, "perfect_fibers": balanced, "reverse_states": states,
            "reverse_legal_transitions": processed}


def fixed_pair(alpha, beta, keep_streams=True):
    """Direct value-state implementation of the reviewed rank-history recurrence."""
    m = len(alpha)
    require(len(beta) == m, "Unequal join halves")
    # Restrict each word by rank, then obtain the new rank's actual position.
    gaps_a = tuple(tuple(x for x in alpha if x <= rank).index(rank) for rank in range(1, m + 1))
    gaps_b = tuple(tuple(x for x in beta if x <= rank).index(rank) for rank in range(1, m + 1))
    current = {(0, ()): 1}
    rows = []
    legal_count = 0
    maximum = 1
    for total in range(2 * m):
        new = defaultdict(int)
        for (i, tree), weight in current.items():
            j = total - i
            edges = transitions(tree)
            if i < m and gaps_a[i] in edges:
                new[(i + 1, edges[gaps_a[i]])] += weight
                legal_count += 1
            if j < m and i + gaps_b[j] in edges:
                new[(i, edges[i + gaps_b[j]])] += weight
                legal_count += 1
        current = dict(new)
        maximum = max(maximum, len(current))
        if keep_streams:
            digest = hashlib.sha256()
            for (i, tree), weight in sorted(current.items(), key=lambda pair: (pair[0][0], word(pair[0][1]))):
                digest.update((str(i) + ":" + word(tree) + ":" + str(weight) + "\n").encode())
            rows.append({"ranks_inserted": total + 1, "states": len(current),
                         "state_weight_stream_sha256": digest.hexdigest()})
            clear_geometry()
        require(len(current) <= 50000, "Independent state cap: incomplete")
    count = sum(weight for (i, tree), weight in current.items() if i == m and m in transitions(tree))
    return {"valid_rank_partitions": count, "states_per_level": rows,
            "peak_level_states": maximum, "legal_transitions": legal_count}


def literal_join(alpha, beta):
    m = len(alpha)
    count = 0
    for selected in itertools.combinations(range(1, 2 * m + 1), m):
        complement = tuple(x for x in range(1, 2 * m + 1) if x not in selected)
        permutation = tuple(selected[x - 1] for x in alpha) + (2 * m + 1,) + tuple(complement[x - 1] for x in beta)
        count += not boxed_occurrences(permutation)
    return count


def seed(height):
    if height == 1:
        return (1,)
    if height == 2:
        return (1, 3, 2)
    small = seed(height - 1)
    d = len(small)
    return tuple(x + d for x in small) + (2 * d + 1,) + small


def check_joins(source):
    native = json.loads((source / "balanced_join_cpp_h3.json").read_text())
    # Reconstruct the complete fiber from the boxed definition, not the input file.
    tree = perfect(3)
    fiber = tuple(p for p in itertools.permutations(range(1, 8)) if shape(p) == tree and not boxed_occurrences(p))
    tokens = (source / "balanced_fiber_h3.txt").read_text().split()
    received = tuple(tuple(map(int, tokens[2 + 7 * k:2 + 7 * (k + 1)])) for k in range(int(tokens[1])))
    require(fiber == received and len(fiber) == 43, "Incomplete/wrong literal input fiber")
    pair_counts = [fixed_pair(a, b, False)["valid_rank_partitions"] for a in fiber for b in fiber]
    require(pair_counts == native["pair_counts_in_input_order"], "Complete m7 join table mismatch")
    require(sum(pair_counts) == 790086 and min(pair_counts) == 37, "Wrong complete join statistics")
    clear_geometry()
    baseline = json.loads((source / "balanced_join_reference.json").read_text())
    literals = 0
    for row in baseline["rows"]:
        for pair in row["pair_counts"]:
            a, b = tuple(pair["alpha"]), tuple(pair["beta"])
            count = literal_join(a, b)
            require(count == pair["valid_rank_partitions"] == fixed_pair(a, b)["valid_rank_partitions"],
                    "Literal small-pair baseline mismatch")
            literals += 1
    selected = {(0, 0), (0, 42), (42, 0), (42, 42),
                (fiber.index(tuple(native["first_minimizing_alpha"])),
                 fiber.index(tuple(native["first_minimizing_beta"])))}
    for ai, bi in sorted(selected):
        require(literal_join(fiber[ai], fiber[bi]) == pair_counts[ai * 43 + bi], "Literal m7 baseline mismatch")
        literals += 1
    clear_geometry()
    expected = json.loads((source / "fixed_pair_join_counts_v3.json").read_text())
    family = []
    for row in expected["family"]:
        h, m = row["height"], row["m"]
        if h == 1:
            a = b = (1,)
        else:
            small = seed(h - 1)
            d = len(small)
            a = tuple(x + d for x in small) + (2 * d + 1,) + small
            # Rank-to-band map expressed directly rather than an offset table.
            b = tuple(1 if x == 1 else d + x for x in small) + (2 * d + 1,) + tuple(x + 1 for x in small)
        require(a == tuple(row["alpha"]) and b == tuple(row["beta"]), "Family reconstruction mismatch")
        require(not boxed_occurrences(a) and not boxed_occurrences(b), "H domain avoidance fails")
        require(shape(a) == shape(b) == perfect(h), "H domain tree fails")
        got = fixed_pair(a, b)
        for key, value in got.items():
            require(value == row[key], "Family state/count mismatch at " + str(h) + ":" + key)
        family.append({"height": h, "m": m, "alpha": a, "beta": b, **got,
                       "bound": 1 << ((m - 1) // 2), "domain_checked": True})
        clear_geometry()
        print(json.dumps({"height": h, "m": m, "N": got["valid_rank_partitions"],
                          "full_state_streams_matched": True}), flush=True)
    require(family[-1]["valid_rank_partitions"] == 25635 < family[-1]["bound"] == 32768,
            "Claimed valid H failure not reproduced")
    bad = (1, 3, 2, 7, 4, 6, 5)
    require((1, 2, 3, 4) in boxed_occurrences(bad), "Preserved invalid family's boxed subword missing")
    return {"definition_reconstructed_fiber_size": len(fiber), "m7_all_pairs_checked": len(pair_counts),
            "m7_pair_counts_sha256": hashlib.sha256(json.dumps(pair_counts, separators=(",", ":")).encode()).hexdigest(),
            "m7_minimum_N": min(pair_counts), "m7_sum_N": sum(pair_counts),
            "literal_pairs_checked": literals, "family": family,
            "unchecked_v1_domain_failure_confirmed": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author-dir", type=Path, default=Path(__file__).resolve().parent / "received/quinn_reverse_join_v1")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.author_dir
    manifest = json.loads((source / "REVERSE_JOIN_MANIFEST_V1.json").read_text())
    before = {name: record(source / name) for name in manifest["files"]}
    require(before == manifest["files"], "Frozen author source changed")
    for name, digest in manifest["dependencies"].items():
        require(record(source / name)["sha256"] == digest, "Frozen dependency changed")
    start = time.perf_counter()
    reverse = check_reverse(source)
    joins = check_joins(source)
    require(before == {name: record(source / name) for name in before}, "Source changed during check")
    result = {"author": "literature-researcher-3", "checker": "literature-researcher-4",
              "decision_message_id": 410, "full_target_solved": False,
              "proof_sha256": before["REVERSE_MERGE_AND_JOIN_BOUND.md"]["sha256"],
              "manifest_sha256": record(source / "REVERSE_JOIN_MANIFEST_V1.json")["sha256"],
              "source_files": before, "reverse": reverse, "joins": joins,
              "python": platform.python_version(), "seconds": time.perf_counter() - start,
              "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              "processes": 1, "native_threads": 1,
              "trust_boundary": "written all-size counting proof and separately accepted maximum-tree quotient467"}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("source_files", "reverse", "joins")}, indent=2))


if __name__ == "__main__":
    main()
