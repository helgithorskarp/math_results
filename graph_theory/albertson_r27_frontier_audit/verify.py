#!/usr/bin/env python3
"""Independent exact audit of the r=27 frontier in arXiv:2609.01682v1.

This program was written from the displayed inequalities in the paper.  It
does not import, invoke, or parse the authors' supplementary verifier.
"""

from fractions import Fraction as Q


R = 27


def ceil_q(x: Q) -> int:
    return -((-x.numerator) // x.denominator)


def z(r: int) -> int:
    return (
        (r // 2)
        * ((r - 1) // 2)
        * ((r - 2) // 2)
        * ((r - 3) // 2)
        // 4
    )


def sampled_crossing_lower_bound(n: int, m: int, k: int) -> Q:
    """Lemma 2.2, evaluated exactly."""
    assert 4 <= k <= n
    return (
        Q(5 * m * (n - 2) * (n - 3), (k - 2) * (k - 3))
        - Q(
            203 * n * (n - 1) * (n - 2) * (n - 3),
            9 * k * (k - 1) * (k - 3),
        )
    )


def best_sample(n: int, m: int) -> tuple[Q, int]:
    """Best bound among every allowed sample size, with smallest k on ties."""
    bound, negative_k = max(
        ((sampled_crossing_lower_bound(n, m, k), -k) for k in range(4, n + 1))
    )
    return bound, -negative_k


def ky_twice_edges(r: int, n: int) -> Q:
    return Q((r + 1) * (r - 2) * n - r * (r - 3), r - 1)


def barat_toth_twice_edges(r: int, n: int) -> int:
    return (r - 1) * n + 2 * r - 6


def gallai_twice_edges(r: int, n: int) -> int:
    assert r + 2 <= n <= 2 * r - 2
    return (r - 1) * n + (n - r) * (2 * r - n) - 2


def ordinary_edge_floor(r: int, n: int) -> int:
    twice_bounds = [ky_twice_edges(r, n), Q(barat_toth_twice_edges(r, n))]
    if r + 2 <= n <= 2 * r - 2:
        twice_bounds.append(Q(gallai_twice_edges(r, n)))
    return ceil_q(max(twice_bounds) / 2)


def singleton_join_floor(r: int, n: int) -> int:
    """First quantity in Proposition 3.2."""
    return (n - 1) + ceil_q(Q((r - 2) * (n - 1) + 2 * r - 8, 2))


def nonsingleton_join_floor(r: int) -> int:
    """Second quantity in Proposition 3.2."""
    return r * r + 3 * r - 19


def proposition_floor(r: int, n: int) -> int:
    return min(singleton_join_floor(r, n), nonsingleton_join_floor(r))


def relaxed_gallai_profiles(r: int, n: int):
    """Enumerate a superset of the component profiles in Gallai's theorem.

    A block is (chromatic number, order).  Blocks are nondecreasing, so each
    multiset occurs once.  We enforce k=1 iff order=1, exclude k=2, and impose
    order >= 2k-1 for k>=3.  We deliberately do not require odd order at k=3;
    hence this is a relaxation, and a lower bound valid for every emitted
    profile is certainly valid for every realizable profile.
    """

    def visit(rem_r: int, rem_n: int, last: tuple[int, int], blocks: tuple):
        if rem_r == 0 or rem_n == 0:
            if rem_r == rem_n == 0 and len(blocks) >= 2:
                yield blocks
            return

        min_k = last[0] if blocks else 1
        for k in range(min_k, rem_r + 1):
            if k == 2:
                continue
            if k == 1:
                orders = (1,)
            else:
                orders = range(2 * k - 1, rem_n + 1)
            for order in orders:
                block = (k, order)
                if blocks and block < last:
                    continue
                if order > rem_n:
                    continue
                yield from visit(rem_r - k, rem_n - order, block, blocks + (block,))

    yield from visit(r, n, (0, 0), ())


def component_edge_floor(k: int, n: int) -> int:
    if k == 1:
        assert n == 1
        return 0
    if k == 3:
        # A realizable 3-critical block is an odd cycle, with n edges.  The
        # same lower bound is harmless on the deliberately relaxed even n.
        return n
    assert k >= 4 and n >= 2 * k - 1
    return ceil_q(ky_twice_edges(k, n) / 2)


def profile_edge_floor(r: int, n: int, blocks: tuple[tuple[int, int], ...]) -> int:
    direct = sum(component_edge_floor(k, order) for k, order in blocks)
    direct += sum(
        blocks[i][1] * blocks[j][1]
        for i in range(len(blocks))
        for j in range(i + 1, len(blocks))
    )
    if any(k == 1 for k, _ in blocks):
        # Removing one universal vertex and applying Barát--Tóth to the
        # remaining (r-1)-critical graph gives this independent lower bound.
        direct = max(direct, singleton_join_floor(r, n))
    return direct


def audit_profiles(r: int, n: int) -> tuple[int, int, tuple]:
    count = 0
    minimum = None
    witness = None
    for blocks in relaxed_gallai_profiles(r, n):
        count += 1
        bound = profile_edge_floor(r, n, blocks)
        if minimum is None or bound < minimum:
            minimum, witness = bound, blocks
    assert count and minimum is not None
    return count, minimum, witness


def main() -> None:
    assert z(R) == 6084

    basic = {}
    for n in range(32, 97):
        m = ordinary_edge_floor(R, n)
        basic[n] = (m, *best_sample(n, m))
    basic_survivors = [n for n, (_, bound, _) in basic.items() if bound < z(R)]
    assert basic_survivors == [52, 53, 54]

    excluded = [entry for n, entry in basic.items() if n not in basic_survivors]
    weakest_bound, weakest_neg_k = min((bound, -k) for _, bound, k in excluded)
    weakest_k = -weakest_neg_k
    weakest_orders = [
        n
        for n, (_, bound, k) in basic.items()
        if n not in basic_survivors and bound == weakest_bound and k == weakest_k
    ]
    # Optimizing k separately at every order strengthens the paper's grouped
    # table at n=55: k=25 is better there than the row's common choice k=26.
    assert weakest_bound == Q(15530749, 2530)
    assert weakest_orders == [55] and weakest_k == 25

    disconnected = {}
    for n in basic_survivors:
        m = proposition_floor(R, n)
        disconnected[n] = (m, *best_sample(n, m))
        assert disconnected[n][1] > z(R)
    assert {n: data[0] for n, data in disconnected.items()} == {
        52: 712,
        53: 725,
        54: 739,
    }

    profile_results = {n: audit_profiles(R, n) for n in basic_survivors}
    for n, (_, minimum, _) in profile_results.items():
        assert minimum >= proposition_floor(R, n)

    thresholds = {}
    for n in (53, 54):
        floor = ordinary_edge_floor(R, n)
        threshold = next(m for m in range(floor, floor + 100) if best_sample(n, m)[0] >= z(R))
        thresholds[n] = (floor, threshold)
    assert thresholds == {53: (713, 716), 54: (726, 727)}

    # Gallai forces disconnected complement through n=2r-2=52.  Since every
    # disconnected case above is excluded, only n=53,54 with connected
    # complement remain.
    assert 52 == 2 * R - 2
    final_survivors = [53, 54]

    print("PASS independent exact audit of arXiv:2609.01682v1, Theorem 1.3")
    print(f"Z(27)={z(R)}")
    print(f"ordinary bounds leave orders {basic_survivors}")
    print(
        "weakest excluded ordinary case: "
        f"n={weakest_orders[0]}, k={weakest_k}, bound={weakest_bound}"
    )
    print(
        "disconnected-complement edge floors: "
        + ", ".join(f"n={n}:m>={data[0]}" for n, data in disconnected.items())
    )
    for n, (count, minimum, witness) in profile_results.items():
        print(
            f"relaxed Gallai profiles n={n}: count={count}, "
            f"minimum direct floor={minimum}, witness={witness}"
        )
    print(f"ordinary edge-floor/closure thresholds: {thresholds}")
    print(f"final frontier: orders {final_survivors}, connected complement")


if __name__ == "__main__":
    main()
