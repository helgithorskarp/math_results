#!/usr/bin/env python3
"""Independent bounded-cost enumeration of odd-cycle ancestry trees.

Unlike verify.py's min-plus optimization, this checker retains every attainable
pile-leaf count through the claimed root bound as a Python-integer bitset.
It is intended for small cases and shares no production routines.
"""

from __future__ import annotations

import argparse


def bit_values(bits, limit):
    return [value for value in range(limit + 1) if (bits >> value) & 1]


def attainable_tree_costs(k, limit):
    order = 2 * k + 1
    costs = [[0] * 4 for _ in range(order)]
    costs[0][0] = 1 << 1
    costs[k][1] = 1
    costs[k + 2][2] = 1
    cutoff = (1 << (limit + 1)) - 1

    changed = True
    while changed:
        changed = False
        previous = [row[:] for row in costs]
        for source in range(order):
            for left_mask in range(4):
                left = previous[source][left_mask]
                if not left:
                    continue
                for right_mask in range(4):
                    if left_mask & right_mask:
                        continue
                    right = previous[source][right_mask]
                    if not right:
                        continue
                    sums = 0
                    remaining = left
                    while remaining:
                        lowest = remaining & -remaining
                        shift = lowest.bit_length() - 1
                        sums |= right << shift
                        remaining ^= lowest
                    sums &= cutoff
                    parent_mask = left_mask | right_mask
                    for parent in ((source - 1) % order, (source + 1) % order):
                        enlarged = costs[parent][parent_mask] | sums
                        if enlarged != costs[parent][parent_mask]:
                            costs[parent][parent_mask] = enlarged
                            changed = True
    return costs


def additive_closure(coins, limit):
    reachable = 1
    coin_values = [value for value in range(1, limit + 1) if (coins >> value) & 1]
    for total in range(limit + 1):
        if not ((reachable >> total) & 1):
            continue
        for coin in coin_values:
            if total + coin <= limit:
                reachable |= 1 << (total + coin)
    return reachable


def forest_costs_at_root(root_costs, limit):
    cutoff = (1 << (limit + 1)) - 1
    no_singletons = additive_closure(root_costs[0], limit)
    special = root_costs[3]
    for left in bit_values(root_costs[1], limit):
        special |= root_costs[2] << left
    special &= cutoff
    all_forests = 0
    for cost in bit_values(special, limit):
        all_forests |= no_singletons << cost
    return all_forests & cutoff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=9)
    args = parser.parse_args()
    if not 3 <= args.max_k <= 12:
        parser.error("this bounded-cost checker requires 3 <= --max-k <= 12")

    checked_targets = 0
    for k in range(3, args.max_k + 1):
        pile = 5 * 2 ** (k - 1) - 6
        threshold = pile + 3
        limit = threshold + 3
        residue = pile % 3
        tree_costs = attainable_tree_costs(k, limit)
        for vertex, root_costs in enumerate(tree_costs):
            forests = forest_costs_at_root(root_costs, limit)
            if (forests >> pile) & 1:
                raise AssertionError(f"witness stacks at k={k}, root={vertex}")
            same_residue = [
                value
                for value in bit_values(forests, limit)
                if value % 3 == residue
            ]
            expected = threshold if k - 2 <= vertex <= k + 3 else threshold + 3
            if not same_residue or same_residue[0] != expected:
                raise AssertionError(
                    f"root profile mismatch k={k}, root={vertex}: "
                    f"{same_residue[:1]} != {[expected]}"
                )
            checked_targets += 1
    print(
        f"INDEPENDENTLY VERIFIED k=3..{args.max_k} "
        f"targets={checked_targets} representation=bounded_cost_bitsets"
    )


if __name__ == "__main__":
    main()
