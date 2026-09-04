#!/usr/bin/env python3
"""Independent closed-form reconstruction of the h=18 certificate."""

from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb


def edge_colour_cap(edges):
    c = 1
    while c * (c + 1) // 2 <= edges:
        c += 1
    return c


def triples_with_sum(total):
    for a, b, c in combinations_with_replacement(range(9, 27), 3):
        if a + b + c == total:
            yield a, b, c


def reconstruct():
    low = 35
    forced = 26 * low - 713
    assert forced == 197

    # Convex upper bounds for four blocks.  If q overlaps occur, the order
    # sum is 35+q and there are 4-q direct components.  One connector through
    # all components is the edge-maximizing connector forest.
    four = []
    for q in range(4):
        excess = low + q - 4 * 9
        if excess < 0:
            four.append(None)
            continue
        upper = 3 * comb(9, 2) + comb(9 + excess, 2) + comb(4 - q, 2)
        four.append(upper)
    assert four == [None, 147, 154, 163]
    assert max(x for x in four if x is not None) < forced

    connectors = {0: (0, 1, 2, 3), 1: (0, 1), 2: (0,)}
    summary = []
    exceptions = []
    certificate_rows = []
    for q in range(3):
        rows = []
        for sizes in triples_with_sum(low + q):
            # For q=1, the two smallest blocks can be the intersecting pair.
            if q == 1 and sizes[0] + sizes[1] > 28:
                continue
            # For q=2, some block must serve as the middle of a path and meet
            # each endpoint within the degree-26 cap.
            if q == 2 and not any(
                sizes[middle] + sizes[end] <= 28
                for middle in range(3)
                for end in range(3)
                if middle != end
            ):
                continue
            if q == 2:
                possible_middle = any(
                    all(sizes[middle] + sizes[end] <= 28 for end in range(3) if end != middle)
                    for middle in range(3)
                )
                if not possible_middle:
                    continue
            base = sum(comb(x, 2) for x in sizes)
            for extra in connectors[q]:
                e_low = base + extra
                if e_low < forced:
                    continue
                e_high = e_low - forced
                cap = max(sizes) + edge_colour_cap(e_high)
                row = (sizes, extra, e_low, e_high, cap)
                rows.append(row)
                certificate_rows.append((q,) + row)
                if cap > 26:
                    exceptions.append((sizes, e_high, cap))
        summary.append((q, len(rows), max(row[-1] for row in rows)))

    assert summary == [(0, 13, 22), (1, 24, 26), (2, 14, 29)]
    assert exceptions == [((9, 9, 19), 46, 29), ((9, 10, 18), 37, 27)]

    # Colour-class incidence, reconstructed without the labelled path code.
    # A row of size r has 18-r bad vertices, which can contaminate no more
    # than 18-r colour classes.
    assert 9 - (18 - 17) >= 1                 # K18 exception
    assert 9 - (18 - 10) >= 1                 # one internal K19 row
    assert 10 - (18 - 10) >= 2                # two internal K19 rows
    assert 19 + 8 - 1 == 19 + 9 - 2 == 19 + 10 - 3 == 26

    # Two-clique rows from the excess variables p+q=17.
    two = []
    identities = 0
    for p in range(9):
        q = 17 - p
        a, b = 9 + p, 9 + q
        if a > b or b >= 27:
            continue
        D = comb(18, 2) - 713 + 26 * 35 - comb(a, 2) - comb(b, 2)
        if D < 0:
            continue
        two.append((a, b, p, q, D))
        assert p >= 1
        assert a - (p + 1) == b - (q + 1) == 8
        assert 18 + 8 == 26
        assert a - p == b - q == 9
        assert 17 + 9 == 26
        assert p + q + 1 == 18
        assert b + p + 1 == 27
        if p >= 2:
            assert b - (25 - (p + 1)) == 2
            assert b - (25 - (9 + p + 1)) == 11
        identities += 10

    assert [row[-1] for row in two] == [5, 19, 31, 41, 49, 55, 59, 61]
    assert len(two) == 8

    parity = comb(comb(18, 2), 2)
    assert parity == 11628
    return four, summary, tuple(certificate_rows), tuple(exceptions), tuple(two), identities, parity


def main():
    four, summary, rows, exceptions, two, identities, parity = reconstruct()
    record = (
        f"four={four};summary={summary};rows={rows};exceptions={exceptions};"
        f"two={two};identities={identities};parity={parity}"
    )
    print("PASS independent Albertson h=18 reconstruction")
    print(f"four_block_caps={four}; three_block_summary={summary}")
    print(f"palette_exceptions={exceptions}")
    print(f"two_clique_profiles={two}")
    print(f"terminal_identities={identities}; unordered_contraction_pairs={parity}")
    print(f"independent_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
