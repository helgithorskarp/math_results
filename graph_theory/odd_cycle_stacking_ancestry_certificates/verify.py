#!/usr/bin/env python3
"""Verify residue-compressed ancestry certificates for odd-cycle stacking.

Vertices of C_(2k+1) are 0,...,2k.  The tested configuration is

    (5*2**(k-1)-6) e_0 + e_k + e_(k+2).

The program constructs a lower-bound table for binary pebbling ancestry trees,
checks every local Bellman inequality, and then checks every possible common
root of an ancestry forest.  All arithmetic is exact Python integer arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from heapq import heappop, heappush

INF = None


def improve(table, heap, vertex, special_mask, residue, value):
    old = table[vertex][special_mask][residue]
    if old is None or value < old:
        table[vertex][special_mask][residue] = value
        heappush(heap, (value, vertex, special_mask, residue))


def construct_tree_table(k):
    """Return candidate lower bounds D[v][S][r] for one ancestry tree.

    D[v][S][r] is the least number found of main-pile leaves in a tree
    rooted at v, using singleton set S, with the pile count congruent to r
    modulo 3.  Masks 1 and 2 denote the singleton leaves at k and k+2.

    This is Knuth/Dijkstra relaxation for the finite weighted tree grammar.
    The later Bellman check, rather than the search procedure, certifies the
    lower-bound direction used by the theorem.
    """
    if k < 3:
        raise ValueError("k must be at least 3")
    order = 2 * k + 1
    table = [[[INF] * 3 for _ in range(4)] for _ in range(order)]
    heap = []

    # The three possible one-leaf ancestry trees.
    improve(table, heap, 0, 0, 1, 1)
    improve(table, heap, k, 1, 0, 0)
    improve(table, heap, k + 2, 2, 0, 0)

    while heap:
        value, source, mask, residue = heappop(heap)
        if table[source][mask][residue] != value:
            continue
        for other_mask in range(4):
            if mask & other_mask:
                continue
            for other_residue in range(3):
                other_value = table[source][other_mask][other_residue]
                if other_value is None:
                    continue
                parent_mask = mask | other_mask
                parent_residue = (residue + other_residue) % 3
                parent_value = value + other_value
                improve(
                    table,
                    heap,
                    (source - 1) % order,
                    parent_mask,
                    parent_residue,
                    parent_value,
                )
                improve(
                    table,
                    heap,
                    (source + 1) % order,
                    parent_mask,
                    parent_residue,
                    parent_value,
                )
    return table


def verify_tree_lower_bound_certificate(k, table):
    """Check the base and local inequalities that prove D is a lower bound."""
    order = 2 * k + 1
    if len(table) != order:
        raise AssertionError("wrong vertex count")
    for vertex, rows in enumerate(table):
        if len(rows) != 4 or any(len(row) != 3 for row in rows):
            raise AssertionError(f"malformed table at vertex {vertex}")
        for mask, row in enumerate(rows):
            for residue, value in enumerate(row):
                if not isinstance(value, int) or value < 0:
                    raise AssertionError(
                        f"non-finite/nonnegative entry {(vertex, mask, residue)}"
                    )
                if value % 3 != residue:
                    raise AssertionError(
                        f"residue mismatch at {(vertex, mask, residue)}: {value}"
                    )

    # Every possible leaf tree has cost at least its table entry.
    if table[0][0][1] > 1:
        raise AssertionError("main-pile leaf base inequality fails")
    if table[k][1][0] > 0 or table[k + 2][2][0] > 0:
        raise AssertionError("singleton leaf base inequality fails")

    # An internal ancestry node is one move: its two children are rooted at
    # the same neighboring source and use disjoint singleton sets.
    for source in range(order):
        for left_mask in range(4):
            for right_mask in range(4):
                if left_mask & right_mask:
                    continue
                parent_mask = left_mask | right_mask
                for left_residue in range(3):
                    for right_residue in range(3):
                        parent_residue = (left_residue + right_residue) % 3
                        children = (
                            table[source][left_mask][left_residue]
                            + table[source][right_mask][right_residue]
                        )
                        for parent in (
                            (source - 1) % order,
                            (source + 1) % order,
                        ):
                            if table[parent][parent_mask][parent_residue] > children:
                                raise AssertionError(
                                    "Bellman inequality fails: "
                                    f"parent={(parent, parent_mask, parent_residue)} "
                                    f"source={source} children="
                                    f"{(left_mask, left_residue, right_mask, right_residue)}"
                                )


def minplus_convolution(left, right):
    result = [None] * 3
    for left_residue in range(3):
        for right_residue in range(3):
            residue = (left_residue + right_residue) % 3
            candidate = left[left_residue] + right[right_residue]
            if result[residue] is None or candidate < result[residue]:
                result[residue] = candidate
    return result


def empty_forest_star(empty_tree):
    """Minimum certificate weight for any number of no-singleton roots.

    On the three residue states, a cheapest walk has at most two edges: a
    repeated prefix residue would give a nonnegative cycle that can be removed.
    """
    result = [0, None, None]
    one = empty_tree
    two = minplus_convolution(empty_tree, empty_tree)
    for residue in range(3):
        candidates = [one[residue], two[residue]]
        if result[residue] is not None:
            candidates.append(result[residue])
        result[residue] = min(candidates)
    return result


def two_singleton_forest_bound(root_rows):
    """Return lower bounds by total pile residue for forests at one root."""
    separate = minplus_convolution(root_rows[1], root_rows[2])
    special_roots = [
        min(root_rows[3][residue], separate[residue]) for residue in range(3)
    ]
    return minplus_convolution(special_roots, empty_forest_star(root_rows[0]))


def expected_root_bound(k, vertex):
    threshold = 5 * 2 ** (k - 1) - 3
    if k - 2 <= vertex <= k + 3:
        return threshold
    return threshold + 3


def verify_k(k, digest=None):
    table = construct_tree_table(k)
    verify_tree_lower_bound_certificate(k, table)

    pile = 5 * 2 ** (k - 1) - 6
    residue = pile % 3
    root_bounds = []
    for vertex, rows in enumerate(table):
        forest = two_singleton_forest_bound(rows)
        bound = forest[residue]
        expected = expected_root_bound(k, vertex)
        if bound != expected:
            raise AssertionError(
                f"unexpected root bound k={k} v={vertex}: {bound} != {expected}"
            )
        if pile >= bound:
            raise AssertionError(
                f"nonstackability certificate fails k={k} v={vertex}: "
                f"pile={pile} bound={bound}"
            )
        root_bounds.append(bound)

    if digest is not None:
        for vertex, mask, residue_index in itertools.product(
            range(2 * k + 1), range(4), range(3)
        ):
            digest.update(
                f"D,{k},{vertex},{mask},{residue_index},"
                f"{table[vertex][mask][residue_index]}\n".encode("ascii")
            )
        for vertex, bound in enumerate(root_bounds):
            digest.update(f"F,{k},{vertex},{residue},{bound}\n".encode("ascii"))
    return root_bounds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=1000)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error("--max-k must be at least 3")

    digest = hashlib.sha256()
    for k in range(3, args.max_k + 1):
        verify_k(k, digest)

    cases = args.max_k - 2
    targets = args.max_k**2 + 2 * args.max_k - 8
    final_bound = 5 * 2 ** (args.max_k - 1) - 3
    print(
        f"VERIFIED k=3..{args.max_k} cases={cases} targets={targets} "
        f"local_states={12 * targets}"
    )
    print(
        "root_profile=threshold_on_[k-2,k+3],threshold_plus_3_elsewhere"
    )
    print(f"last_lower_bound={final_bound}")
    print(f"certificate_sha256={digest.hexdigest()}")


if __name__ == "__main__":
    main()
