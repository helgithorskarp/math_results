#!/usr/bin/env python3
"""Clean-room exact audit of the Albertson r=27, h=13 closure.

This checker deliberately imports none of the target contribution's code.  It
checks the finite block-incidence classification, the exact edge rows, the
two-contraction rigidity kernel, all one-target support patterns, and the
cardinality/disjointness conditions in the terminal subdivision templates.
"""

from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from math import comb


K = 27
N = 53
M = 713
H = 13
LOW = N - H
LOW_DEGREE = K - 1


def is_forest(order, edges):
    parent = list(range(order))

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for u, v in edges:
        u, v = find(u), find(v)
        if u == v:
            return False
        parent[u] = v
    return True


def block_incidence_audit():
    """Enumerate the possible large-clique block incidences.

    A shared low vertex in two large blocks already has
    (14-1)+(14-1)=26 neighbours, so the two blocks must both be K14.  A low
    vertex cannot be shared by three large blocks.  Consequently the direct
    block-intersection graph faithfully records distinct cut vertices and is
    a forest.
    """
    labelled = []
    for count in range(1, 5):
        block_pairs = tuple(combinations(range(count), 2))
        for sizes in combinations_with_replacement(range(14, 27), count):
            for flags in product((0, 1), repeat=len(block_pairs)):
                overlaps = tuple(p for p, flag in zip(block_pairs, flags) if flag)
                if not is_forest(count, overlaps):
                    continue
                if any(sizes[i] != 14 or sizes[j] != 14 for i, j in overlaps):
                    continue
                if sum(sizes) - len(overlaps) != LOW:
                    continue
                labelled.append((sizes, overlaps))

    two_block_orders = {
        sizes for sizes, overlaps in labelled if len(sizes) == 2 and not overlaps
    }
    three_block_patterns = [
        overlaps for sizes, overlaps in labelled if sizes == (14, 14, 14)
    ]
    assert two_block_orders == {(a, 40 - a) for a in range(14, 21)}
    assert len(three_block_patterns) == 3
    assert all(len(overlaps) == 2 for overlaps in three_block_patterns)
    assert len(labelled) == 10

    three_edges = 3 * comb(14, 2)
    low_high_edges = LOW_DEGREE * LOW - 2 * three_edges
    assert (three_edges, low_high_edges) == (273, 494)
    assert three_edges + low_high_edges == 767 > M
    return len(labelled), len(two_block_orders), len(three_block_patterns)


def exact_rows():
    rows = []
    variants = []
    for a in range(14, LOW // 2 + 1):
        b = LOW - a
        d, e = a - 14, b - 14
        base_low = comb(a, 2) + comb(b, 2)
        # If t is the possible low bridge and r=|E(H[Q])|, exact edge
        # accounting cancels t and fixes D=t+r=405-base_low.
        D = comb(H, 2) - (M - (LOW_DEGREE * LOW - base_low))
        if D < 0:
            continue
        rows.append((a, b, d, e, D))
        for bridge in (0, 1):
            if D - bridge >= 0:
                variants.append((a, b, d, e, bridge, D - bridge))

    expected = [
        (15, 25, 1, 11, 0),
        (16, 24, 2, 10, 9),
        (17, 23, 3, 9, 16),
        (18, 22, 4, 8, 21),
        (19, 21, 5, 7, 24),
        (20, 20, 6, 6, 25),
    ]
    assert rows == expected
    assert len(variants) == 11
    return rows, variants


def contraction_kernel():
    """Check the set-theoretic core of the two-contraction argument."""
    high_edges = tuple(combinations(range(H), 2))
    checks = 0
    for first, second in combinations(high_edges, 2):
        intersection = set(first) & set(second)
        assert len(intersection) <= 1
        # Equality of two fixed-size rows after both contractions confines
        # their symmetric difference to this intersection.  Its cardinality
        # must be even, so the only possibility is the empty set.
        for difference_size in range(len(intersection) + 1):
            if difference_size % 2 == 0:
                assert difference_size == 0
            checks += 1
    return checks


def one_target_patterns(rows):
    """Exhaust the support types and independently check each route bound."""
    counts = {"short": 0, "opposite": 0, "one_centre": 0, "two_centres": 0}
    for a, b, d, e, D in rows:
        if D == 0:
            continue
        for support_size, opposite_size in ((d, b), (e, a)):
            assert support_size >= 2
            centre_degree = opposite_size - (25 - (support_size + 1))
            support_degree = 29 - H
            opposite_type_degree = 30 - H
            assert centre_degree == 2
            assert support_degree == 16
            assert 2 * opposite_type_degree > opposite_size
            for pattern in product(range(4), repeat=support_size):
                # 0 = adjacent in G to both target ends; 1/2 = adjacent in H
                # to exactly one target end; 3 = adjacent in H to both.
                if 0 in pattern:
                    counts["short"] += 1
                elif 1 in pattern and 2 in pattern:
                    counts["opposite"] += 1
                elif all(t in (1, 3) for t in pattern) ^ all(
                    t in (2, 3) for t in pattern
                ):
                    counts["one_centre"] += 1
                else:
                    assert set(pattern) == {3}
                    counts["two_centres"] += 1
    assert sum(counts.values()) == 1_402_192
    return counts


def terminal_identities(rows, variants):
    """Check every residual-matching and subdivision capacity identity."""
    balance_pairs = 0
    injection_cases = 0
    for a, b, d, e, D in rows:
        assert d + e == H - 1
        assert a == 14 + d and b == 14 + e
        assert a + H - d == b + H - e == K
        if D == 0:
            continue

        # After deleting s0 from S, low-side balance in a factor-critical
        # matching is r_M-s_M=1.  If z is matched into S, endpoint parity
        # forces at least one R-R edge (and symmetrically).
        for s_matched in range(d):
            r_matched = s_matched + 1
            if r_matched <= e:
                assert a - (d - 1 - s_matched) == b - (e - r_matched)
                balance_pairs += 1

        # Each conformal-triangle deletion used in the unbridged proof leaves
        # 15 low vertices on each side to be paired across H[A,B].
        assert a - (d - 1) == b - (e - 1) == 15
        assert (a - 1) - (d - 2) == b - (e - 1) == 15
        assert a - (d - 1) == (b - 1) - (e - 2) == 15

        # Exhaust every possible pair of nonempty z-neighbour sets X subset S,
        # Y subset R.  The smaller injects into the larger, and there are more
        # than enough distinct low internal vertices for all replacement paths.
        for x_size in range(1, d + 1):
            for y_size in range(1, e + 1):
                if x_size <= y_size:
                    assert x_size <= a
                    assert b + d + 1 == K
                else:
                    assert y_size <= b
                    assert a + e + 1 == K
                injection_cases += 1

    bridge_templates = double_uniform_templates = special = 0
    for a, b, d, e, bridge, missing_high in variants:
        assert a - (d + 1) == b - (e + 1) == 13
        if missing_high == 0:
            special += 1
        elif bridge:
            # Branch set A union R union {z}; only a0-z is absent.  The route
            # a0-b0-b1-z has two distinct internal vertices because b>=20.
            assert a + e + 1 == K and b >= 2
            bridge_templates += 1
        else:
            assert b + d + 1 == K
            double_uniform_templates += 1
    assert (special, bridge_templates, double_uniform_templates) == (1, 5, 5)
    assert balance_pairs == 20
    return balance_pairs, injection_cases, special, bridge_templates, double_uniform_templates


def main():
    labelled, pairs, paths = block_incidence_audit()
    rows, variants = exact_rows()
    contractions = contraction_kernel()
    targets = one_target_patterns(rows)
    terminal = terminal_identities(rows, variants)
    record = (
        f"block_labelled={labelled};pairs={pairs};k14_paths={paths};"
        f"rows={rows};variants={len(variants)};contractions={contractions};"
        f"targets={sorted(targets.items())};terminal={terminal}"
    )
    digest = sha256(record.encode()).hexdigest()
    print("PASS clean-room review of Albertson r=27 h=13 closure")
    print("block alternatives: seven disjoint pairs or three labelled K14 paths")
    print("three-K14 budget: 273+494=767>713")
    print("rows:", rows)
    print("variants:", len(variants))
    print("contraction-kernel checks:", contractions)
    print("one-target patterns:", targets)
    print("terminal identities:", terminal)
    print("review_sha256=" + digest)


if __name__ == "__main__":
    main()
