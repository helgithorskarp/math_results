#!/usr/bin/env python3
"""Finite falsification controls of Theo's new arbitrary-inflation packet.

Uniform proofs are separate and await Lyra's check. No finite observations
here decide the boxed2143 growth target. Standard-library exact arithmetic.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import time

from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def standardize(word):
    ranks = {value: rank for rank, value in enumerate(sorted(word), 1)}
    return tuple(ranks[value] for value in word)


@lru_cache(maxsize=20000)
def occurrences(p):
    return boxed_occurrences(p)


def inflate(p, blocks):
    require(len(p) == len(blocks) and all(blocks), 'Nonempty blocks required')
    result = []
    starts = []
    lows = []
    for i, value in enumerate(p):
        starts.append(len(result))
        low = sum(len(blocks[j]) for j in range(len(p)) if p[j] < value)
        lows.append(low)
        result.extend(low + x for x in blocks[i])
    require(sorted(result) == list(range(1, len(result) + 1)), 'Invalid inflation')
    return tuple(result), tuple(starts), tuple(lows)


def canonical_lifts(p, blocks, starts):
    return tuple(sorted((starts[a] + len(blocks[a]) - 1,
                         starts[b] + blocks[b].index(max(blocks[b])),
                         starts[c] + blocks[c].index(min(blocks[c])),
                         starts[d]) for a, b, c, d in occurrences(p)))


@lru_cache(maxsize=None)
def short_boxes(p, pattern):
    result = []
    for selected in itertools.combinations(range(len(p)), len(pattern)):
        values = tuple(p[i] for i in selected)
        if standardize(values) != pattern:
            continue
        low, high = min(values), max(values)
        if not any(low < p[j] < high for j in range(selected[0] + 1, selected[-1]) if j not in selected):
            result.append(selected)
    return tuple(result)


def boundary_statistics(block):
    right = sum(all(x > y for y in block[j + 1:]) and any(y > x for y in block[:j])
                for j, x in enumerate(block))
    left = sum(all(x < y for y in block[:j]) and any(y < x for y in block[j + 1:])
               for j, x in enumerate(block))
    return right, left


def composition_count(p, blocks):
    stats = tuple(boundary_statistics(q) for q in blocks)
    return (len(occurrences(p)) + sum(len(occurrences(q)) for q in blocks)
            + sum(stats[i][0] for i, j, k in short_boxes(p, (1, 3, 2)))
            + sum(stats[k][1] for i, j, k in short_boxes(p, (2, 1, 3)))
            + sum(stats[i][0] * stats[j][1] for i, j in short_boxes(p, (1, 2))))


def proper_intervals(p):
    return tuple((lo, hi) for length in range(2, len(p))
                 for lo in range(len(p) - length + 1) for hi in (lo + length,)
                 if max(p[lo:hi]) - min(p[lo:hi]) + 1 == length)


def simple(p):
    return bool(p) and not proper_intervals(p)


def graft(tree, leaf_index, replacement):
    counter = -1

    def visit(node):
        nonlocal counter
        if node is None:
            counter += 1
            return replacement if counter == leaf_index else None
        label, children = node
        return label, tuple(visit(child) for child in children)

    result = visit(tree)
    require(counter >= leaf_index, 'Leaf index outside tree')
    return result


def encode(p):
    require(bool(p), 'Encoding uses positive lengths')
    if len(p) == 1:
        return None
    intervals = proper_intervals(p)
    if not intervals:
        return p, (None,) * len(p)
    lo, hi = intervals[0]  # already minimum length, then position
    block = standardize(p[lo:hi])
    require(simple(block), 'Minimum interval is not simple')
    quotient = standardize(p[:lo] + (min(p[lo:hi]),) + p[hi:])
    return graft(encode(quotient), lo, (block, (None,) * len(block)))


def evaluate(tree):
    if tree is None:
        return (1,)
    label, children = tree
    return inflate(label, tuple(evaluate(child) for child in children))[0]


def tree_statistics(tree):
    if tree is None:
        return 1, 1, (), 0
    label, children = tree
    stats = tuple(tree_statistics(child) for child in children)
    return (1 + sum(r[0] for r in stats), sum(r[1] for r in stats),
            (label,) + tuple(q for r in stats for q in r[2]),
            len(label) + sum(r[3] for r in stats))


def inflation_control(p, blocks, digest):
    output, starts, _ = inflate(p, blocks)
    actual = occurrences(output)
    lifted = canonical_lifts(p, blocks, starts)
    require(set(lifted) <= set(actual), 'Existing occurrence was removed')
    require(len(set(lifted)) == len(occurrences(p)), 'Lift is not injective')
    expected = composition_count(p, blocks)
    require(len(actual) == expected, f'Full composition formula mismatch: {p}, {blocks}')
    if all(q[0] == 1 and q[-1] == len(q) for q in blocks):
        internal = tuple(tuple(start + i for i in occ) for start, q in zip(starts, blocks) for occ in occurrences(q))
        require(actual == tuple(sorted(lifted + internal)), 'Anchored exact occurrence-set mismatch')
    digest.update((json.dumps([p, blocks, output, actual, expected], separators=(',', ':')) + '\n').encode())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    began = time.perf_counter()
    arbitrary_blocks = tuple(q for k in range(1, 4) for q in itertools.permutations(range(1, k + 1)))
    arbitrary_digest = hashlib.sha256()
    arbitrary_cases = 0
    for m in range(1, 4):
        for p in itertools.permutations(range(1, m + 1)):
            for blocks in itertools.product(arbitrary_blocks, repeat=m):
                inflation_control(p, blocks, arbitrary_digest)
                arbitrary_cases += 1
    # Include nonzero parent occurrences and arbitrary size-four single blocks.
    single_cases = 0
    for m in range(1, 5):
        for p in itertools.permutations(range(1, m + 1)):
            for position in range(m):
                for k in range(1, 5):
                    for block in itertools.permutations(range(1, k + 1)):
                        blocks = [(1,)] * m
                        blocks[position] = block
                        inflation_control(p, tuple(blocks), arbitrary_digest)
                        single_cases += 1

    anchored_blocks = ((1,), (1, 2), (1, 3, 2, 4), (1, 3, 2, 5, 4, 6))
    anchored_digest = hashlib.sha256()
    anchored_cases = 0
    for m in range(1, 4):
        for p in itertools.permutations(range(1, m + 1)):
            for blocks in itertools.product(anchored_blocks, repeat=m):
                inflation_control(p, blocks, anchored_digest)
                anchored_cases += 1
    for p in ((2, 1, 4, 3), (3, 1, 2, 5, 6, 4)):
        inflation_control(p, (anchored_blocks[-1],) * len(p), anchored_digest)
        anchored_cases += 1

    safe_rows = []
    unsafe_contexts = 0
    for k in range(1, 7):
        safe_count = tested = 0
        for block in itertools.permutations(range(1, k + 1)):
            tested += 1
            right, left = boundary_statistics(block)
            require((right == 0) == (block[-1] == k), 'Right boundary equivalence failed')
            require((left == 0) == (block[0] == 1), 'Left boundary equivalence failed')
            safe = not occurrences(block) and left == right == 0
            safe_count += safe
            if not safe:
                if occurrences(block):
                    context = block
                elif block[0] != 1:
                    context = inflate((2, 1, 3), ((1,), (1,), block))[0]
                else:
                    context = inflate((1, 3, 2), (block, (1,), (1,)))[0]
                require(bool(occurrences(context)), 'Unsafe block lost its explicit counterexample')
                unsafe_contexts += 1
        require(tested == math.factorial(k), 'Incomplete block enumeration')
        expected = 1 if k == 1 else sum(not occurrences(q) for q in itertools.permutations(range(1, k - 1)))
        require(safe_count == expected, 'Safe-block counting shift failed')
        safe_rows.append({'size': k, 'blocks_tested': tested, 'safe_blocks': safe_count})

    tree_digest = hashlib.sha256()
    tree_cases = 0
    simple_rows = []
    for n in range(1, 8):
        an = sn = count = 0
        for p in itertools.permutations(range(1, n + 1)):
            count += 1
            tree_cases += 1
            tree = encode(p)
            require(evaluate(tree) == p, 'Substitution encoding does not decode')
            vertices, leaves, labels, degrees = tree_statistics(tree)
            require(leaves == n and vertices <= 2 * n - 1 and degrees == vertices - 1,
                    'Substitution tree counting invariant failed')
            require(all(len(q) >= 2 and simple(q) for q in labels), 'Nonsimple internal label')
            avoids = not occurrences(p)
            if avoids:
                require(all(not occurrences(q) for q in labels), 'Avoidance failed under contraction')
                an += 1
                sn += simple(p)
            tree_digest.update((json.dumps([p, tree], separators=(',', ':')) + '\n').encode())
        require(count == math.factorial(n), 'Incomplete tree enumeration')
        simple_rows.append({'n': n, 'avoiders': an, 'simple_avoiders': sn})
    bad = (5, 3, 1, 6, 4, 2)
    require(simple(bad) and (1, 2, 3, 4) in occurrences(bad), 'Simple nonavoidance witness failed')
    proof = Path(__file__).with_name('ARBITRARY_INFLATION_BOUNDARIES_V1.md')
    report = {'author': 'literature-researcher-4', 'checker': None, 'decision_message_id': 410,
              'full_target_solved': False, 'claim_status': 'finite controls of new uniform author proof awaiting independent review',
              'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
              'arbitrary_all_block_cases': arbitrary_cases, 'single_block_cases': single_cases,
              'arbitrary_stream_sha256': arbitrary_digest.hexdigest(),
              'anchored_cases': anchored_cases, 'anchored_stream_sha256': anchored_digest.hexdigest(),
              'safe_block_rows': safe_rows, 'explicit_unsafe_contexts': unsafe_contexts,
              'substitution_tree_cases': tree_cases, 'substitution_stream_sha256': tree_digest.hexdigest(),
              'simple_rows': simple_rows, 'simple_nonavoider_fixture': bad,
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
