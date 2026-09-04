#!/usr/bin/env python3
"""Independent closed-form reconstruction of the h=19 certificate."""

from hashlib import sha256
from itertools import combinations_with_replacement
from math import comb


def colour_cap(edges):
    c = 1
    while comb(c + 1, 2) <= edges:
        c += 1
    return c


def reconstruct():
    h = 19
    low = 34
    floor = 8
    forced = 26 * low - 713
    assert forced == 171

    four = []
    for overlap in range(4):
        components = 4 - overlap
        excess = low + overlap - 4 * floor
        cap = 3 * comb(floor, 2) + comb(floor + excess, 2) + comb(components, 2)
        four.append(cap)
    assert four == [135, 142, 151, 162]
    assert max(four) < forced
    assert 5 * floor - 4 == 36 > low

    connector_values = {0: range(4), 1: range(2), 2: (0,)}
    summary = []
    exceptions = []
    all_rows = []
    for overlap in range(3):
        rows = []
        for sizes in combinations_with_replacement(range(floor, 27), 3):
            if sum(sizes) != low + overlap:
                continue
            if overlap == 1 and sizes[0] + sizes[1] > 28:
                continue
            if overlap == 2 and not any(
                all(sizes[mid] + sizes[end] <= 28 for end in range(3) if end != mid)
                for mid in range(3)
            ):
                continue
            base = sum(comb(x, 2) for x in sizes)
            for extra in connector_values[overlap]:
                e_low = base + extra
                if e_low < forced:
                    continue
                e_high = e_low - forced
                cap = colour_cap(e_high)
                row = (sizes, overlap, extra, e_low, e_high, cap, max(sizes) + cap)
                rows.append(row)
                all_rows.append(row)
                if row[-1] > 26:
                    exceptions.append(row)
        summary.append((overlap, len(rows), max(row[-1] for row in rows)))
    assert summary == [(0, 56, 27), (1, 32, 30), (2, 19, 32)]
    assert len(exceptions) == 14

    # The unique largest block is the sole possible non-strict list
    # component.  It is isolated precisely in these four exact rows.
    residual = (
        ((8, 8, 18), 0, 0, 38, 9),
        ((8, 8, 18), 0, 1, 39, 9),
        ((8, 8, 19), 1, 0, 56, 11),
        ((8, 9, 18), 1, 0, 46, 10),
    )
    for sizes, overlap, extra, e_high, cap in residual:
        assert e_high == sum(comb(x, 2) for x in sizes) + extra - forced
        assert cap == colour_cap(e_high)
        big = max(sizes)
        small = sorted(sizes)[:2]
        assert 26 - cap > max(small) - 1
        assert 27 - big <= cap

    two = []
    identity_checks = 0
    for p in range(19):
        q = 18 - p
        a, b = floor + p, floor + q
        if a > b or b >= 27:
            continue
        deficit = comb(h, 2) - 713 + 26 * low - comb(a, 2) - comb(b, 2)
        if deficit < 0:
            continue
        two.append((a, b, p, q, deficit))
        assert p >= 1
        for side, other, support, opposite_support in (
            (a, b, p, q),
            (b, a, q, p),
        ):
            assert side - support - 1 == other - opposite_support - 1 == 7
            assert side - support == other - opposite_support == 8
            assert support + opposite_support + 1 == h
            assert other + support + 1 == 27
            assert other - (25 - (support + 1)) == 2
            assert other - (25 - (floor + support + 1)) == 10
            assert other - (25 - (floor + support + 2)) == 11
            identity_checks += 8
    assert [row[-1] for row in two] == [6, 21, 34, 45, 54, 61, 66, 69, 70]
    assert len(two) == 9

    contraction_pairs = comb(comb(h, 2), 2)
    assert contraction_pairs == 14535
    return tuple(four), tuple(summary), tuple(all_rows), tuple(exceptions), residual, tuple(two), identity_checks, contraction_pairs


def main():
    four, summary, rows, exceptions, residual, two, identities, contractions = reconstruct()
    record = (
        f"four={four};summary={summary};rows={rows};exceptions={exceptions};"
        f"residual={residual};two={two};identities={identities};"
        f"contractions={contractions}"
    )
    print("PASS independent Albertson h=19 reconstruction")
    print(f"four_block_caps={four}; three_block_summary={summary}")
    print(f"palette_exceptions={len(exceptions)}; residual={residual}")
    print(f"two_clique_profiles={two}")
    print(f"terminal_identities={identities}; unordered_contractions={contractions}")
    print(f"independent_sha256={sha256(record.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
