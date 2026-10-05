"""Lyra's independent definition-level check of Theo's new A--E packet.

No author rectangle/composition/tree routine is used. Enumerate valid local
descending pairs to predict COMPLETE occurrence sets. Construct tree by an
iterative contraction log and decode by lexicographic rank paths, rather than
recursive author graft/inflation evaluation. Infinite arguments are reviewed
separately; finite controls cannot decide full target410.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from definition_checker import occurrences as literal_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(maxsize=None)
def occ(p):
    return tuple(literal_occurrences(p))


def rank_word(word):
    return tuple(1 + sum(y < x for y in word) for x in word)


@lru_cache(maxsize=None)
def short_boxes(p, pattern):
    rows = []
    for indices in itertools.combinations(range(len(p)), len(pattern)):
        selected = tuple(p[i] for i in indices)
        if rank_word(selected) == pattern and all(
                j in indices or not min(selected) < p[j] < max(selected)
                for j in range(indices[0] + 1, indices[-1])):
            rows.append(indices)
    return tuple(rows)


def expand(p, blocks):
    # Assign each position its (parent value, within-block value) key and
    # standardize the full lexicographic ordering, avoiding author's offsets.
    keys = tuple((p[i], x) for i, block in enumerate(blocks) for x in block)
    ordered = {key: j for j, key in enumerate(sorted(keys), 1)}
    output = tuple(ordered[key] for key in keys)
    starts = tuple(sum(len(b) for b in blocks[:i]) for i in range(len(p)))
    return output, starts


@lru_cache(maxsize=None)
def boundary_pairs(block):
    # Full local pair geometry, independent of the author's record predicates.
    right = tuple((a, b) for a in range(len(block)) for b in range(a + 1, len(block))
                  if block[a] > block[b] and all(j == b or block[j] < block[b]
                                               for j in range(a + 1, len(block))))
    left = tuple((c, d) for c in range(len(block)) for d in range(c + 1, len(block))
                 if block[c] > block[d] and all(j == c or block[j] > block[c]
                                              for j in range(d)))
    require(len({b for a, b in right}) == len(right), "Right local pair is not unique per bottom")
    require(len({c for c, d in left}) == len(left), "Left local pair is not unique per top")
    right_records = {j for j, x in enumerate(block)
                     if x == max(block[j:]) and any(y > x for y in block[:j])}
    left_records = {j for j, x in enumerate(block)
                    if x == min(block[:j + 1]) and any(y < x for y in block[j + 1:])}
    require({b for a, b in right} == right_records and {c for c, d in left} == left_records,
            "Local pairs disagree with R/L record definitions")
    return right, left


def check_expansion(p, blocks, digest):
    output, starts = expand(p, blocks)
    actual = occ(output)
    categories = []
    lifted = tuple((starts[a] + len(blocks[a]) - 1,
                    starts[b] + blocks[b].index(len(blocks[b])),
                    starts[c] + blocks[c].index(1), starts[d])
                   for a, b, c, d in occ(p))
    require(len(set(lifted)) == len(occ(p)), "Canonical lifts collide")
    categories.extend(lifted)
    categories.extend(tuple(start + j for j in row)
                      for start, block in zip(starts, blocks) for row in occ(block))
    pairs = tuple(boundary_pairs(block) for block in blocks)
    for i, j, k in short_boxes(p, (1, 3, 2)):
        for a, b in pairs[i][0]:
            categories.append((starts[i] + a, starts[i] + b,
                               starts[j] + blocks[j].index(1), starts[k]))
    for i, j, k in short_boxes(p, (2, 1, 3)):
        for c, d in pairs[k][1]:
            categories.append((starts[i] + len(blocks[i]) - 1,
                               starts[j] + blocks[j].index(len(blocks[j])),
                               starts[k] + c, starts[k] + d))
    for i, j in short_boxes(p, (1, 2)):
        for a, b in pairs[i][0]:
            for c, d in pairs[j][1]:
                categories.append((starts[i] + a, starts[i] + b,
                                   starts[j] + c, starts[j] + d))
    require(len(set(categories)) == len(categories), "Predicted category selections collide")
    require(tuple(sorted(categories)) == actual,
            f"Full arbitrary-inflation occurrence SET mismatch: {p}, {blocks}")
    if all(block[0] == 1 and block[-1] == len(block) for block in blocks):
        require(all(not r and not l for r, l in pairs), "Anchor has a boundary pair")
        require(len(actual) == len(occ(p)) + sum(len(occ(b)) for b in blocks), "Anchored addition fails")
    digest.update((json.dumps([p, blocks, output, actual, len(categories)],
                             separators=(",", ":")) + "\n").encode())


def minimum_interval(p):
    intervals = [(end - first, first, end) for first in range(len(p))
                 for end in range(first + 2, len(p) + 1)
                 if end - first < len(p) and set(p[first:end]) ==
                 set(range(min(p[first:end]), max(p[first:end]) + 1))]
    return min(intervals) if intervals else None


def simple(p):
    return bool(p) and minimum_interval(p) is None


def leaf_paths(tree):
    stack = [(tree, ())]
    output = []
    while stack:
        node, path = stack.pop()
        if node is None:
            output.append(path)
        else:
            for i in reversed(range(len(node[1]))):
                stack.append((node[1][i], path + (i,)))
    return output


def replace_path(tree, path, replacement):
    ancestors = []
    node = tree
    for child in path:
        ancestors.append((node, child))
        node = node[1][child]
    require(node is None, "Reconstruction path is not a leaf")
    for ancestor, child in reversed(ancestors):
        children = list(ancestor[1])
        children[child] = replacement
        replacement = ancestor[0], tuple(children)
    return replacement


def encode_iteratively(p):
    current = p
    log = []
    parent_avoids = not occ(p)
    while (interval := minimum_interval(current)) is not None:
        length, first, end = interval
        block = rank_word(current[first:end])
        quotient = rank_word(current[:first] + (min(current[first:end]),) + current[end:])
        require(simple(block), "Minimum contracted interval is nonsimple")
        if parent_avoids:
            require(not occ(block) and not occ(quotient), "An avoiding word has a nonavoiding contraction/child")
        log.append((first, block))
        current = quotient
    tree = None if len(current) == 1 else (current, (None,) * len(current))
    for first, block in reversed(log):
        tree = replace_path(tree, leaf_paths(tree)[first], (block, (None,) * len(block)))
    return tree


def decode_and_statistics(tree):
    leaves = []
    stack = [(tree, ())]
    vertices = degrees = 0
    labels = []
    while stack:
        node, rank_path = stack.pop()
        vertices += 1
        if node is None:
            leaves.append(rank_path)
            continue
        label, children = node
        labels.append(label)
        require(len(label) == len(children) >= 2 and simple(label), "Invalid simple node label")
        degrees += len(children)
        for i in reversed(range(len(children))):
            stack.append((children[i], rank_path + (label[i],)))
    ordered = {path: rank for rank, path in enumerate(sorted(leaves), 1)}
    decoded = tuple(ordered[path] for path in leaves)
    return decoded, vertices, degrees, tuple(labels)


def run():
    began = time.monotonic()
    arbitrary_digest = hashlib.sha256()
    arbitrary_count = single_count = 0
    blocks = tuple(q for r in range(1, 4) for q in itertools.permutations(range(1, r + 1)))
    for m in range(1, 4):
        for p in itertools.permutations(range(1, m + 1)):
            for choices in itertools.product(blocks, repeat=m):
                check_expansion(p, choices, arbitrary_digest)
                arbitrary_count += 1
    for m in range(1, 5):
        for p in itertools.permutations(range(1, m + 1)):
            for position in range(m):
                for r in range(1, 5):
                    for block in itertools.permutations(range(1, r + 1)):
                        choices = tuple(block if i == position else (1,) for i in range(m))
                        check_expansion(p, choices, arbitrary_digest)
                        single_count += 1

    anchors = ((1,), (1, 2), (1, 3, 2, 4), (1, 3, 2, 5, 4, 6))
    anchored_digest = hashlib.sha256()
    anchored_count = 0
    for m in range(1, 4):
        for p in itertools.permutations(range(1, m + 1)):
            for choices in itertools.product(anchors, repeat=m):
                check_expansion(p, choices, anchored_digest)
                anchored_count += 1
    for p in ((2, 1, 4, 3), (3, 1, 2, 5, 6, 4)):
        check_expansion(p, (anchors[-1],) * len(p), anchored_digest)
        anchored_count += 1

    safe_rows = []
    unsafe_count = 0
    for r in range(1, 7):
        safe_count = tested = 0
        for block in itertools.permutations(range(1, r + 1)):
            tested += 1
            right, left = boundary_pairs(block)
            require((not right) == (block[-1] == r) and (not left) == (block[0] == 1),
                    "Vanishing statistic does not match anchor")
            safe = not occ(block) and not left and not right
            safe_count += safe
            if not safe:
                if occ(block):
                    context = block
                elif block[0] != 1:
                    context = expand((2, 1, 3), ((1,), (1,), block))[0]
                else:
                    context = expand((1, 3, 2), (block, (1,), (1,)))[0]
                require(bool(occ(context)), "Unsafe context is avoiding")
                unsafe_count += 1
        shifted_count = 1 if r == 1 else sum(not occ(q)
                        for q in itertools.permutations(range(1, r - 1)))
        require(safe_count == shifted_count, "Safe count is not a_(r-2)")
        safe_rows.append({"size": r, "blocks_tested": tested, "safe_blocks": safe_count})

    tree_digest = hashlib.sha256()
    tree_count = 0
    simple_rows = []
    for n in range(1, 8):
        avoiding_count = simple_count = 0
        for p in itertools.permutations(range(1, n + 1)):
            tree = encode_iteratively(p)
            decoded, vertices, degrees, labels = decode_and_statistics(tree)
            require(decoded == p and vertices <= 2 * n - 1 and degrees == vertices - 1,
                    "Rank-path decode or tree-size invariant failed")
            if not occ(p):
                require(all(not occ(label) for label in labels), "Avoiding word encoded a nonavoiding label")
                avoiding_count += 1
                simple_count += simple(p)
            tree_count += 1
            tree_digest.update((json.dumps([p, tree], separators=(",", ":")) + "\n").encode())
        simple_rows.append({"n": n, "avoiders": avoiding_count, "simple_avoiders": simple_count})
    bad = (5, 3, 1, 6, 4, 2)
    require(simple(bad) and (1, 2, 3, 4) in occ(bad), "Simple nonavoidance fixture failed")
    root = Path(__file__).parent
    frozen = root
    author = json.loads((frozen / "arbitrary-inflation-controls-v1.json").read_text())
    replay = {"arbitrary_all_block_cases": arbitrary_count, "single_block_cases": single_count,
              "arbitrary_stream_sha256": arbitrary_digest.hexdigest(), "anchored_cases": anchored_count,
              "anchored_stream_sha256": anchored_digest.hexdigest(), "safe_block_rows": safe_rows,
              "explicit_unsafe_contexts": unsafe_count, "substitution_tree_cases": tree_count,
              "substitution_stream_sha256": tree_digest.hexdigest(), "simple_rows": simple_rows,
              "simple_nonavoider_fixture": bad}
    for key, value in replay.items():
        require(json.dumps(value) == json.dumps(author[key]), f"Author stream/control mismatch: {key}")
    return {"checker": "literature-researcher-2", "author": "literature-researcher-4",
            "decision_message_id": 410, "full_target_solved": False,
            "checked_scope": "All uniform A--E arguments separately reviewed; complete occurrence-set, unsafe-context and contraction/rank-path controls below",
            "proof_sha256": hashlib.sha256((frozen / "ARBITRARY_INFLATION_BOUNDARIES_V1.md").read_bytes()).hexdigest(),
            "manifest_sha256": hashlib.sha256((frozen / "MANIFEST.json").read_bytes()).hexdigest(),
            **replay, "all_author_deterministic_fields_match": True,
            "checker_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "literal_checker_sha256": hashlib.sha256((root / "definition_checker.py").read_bytes()).hexdigest(),
            "python": platform.python_version(), "elapsed_seconds": time.monotonic() - began,
            "peak_rss_kib_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
