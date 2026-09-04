#!/usr/bin/env python3
"""Clean-room exact audit of the Albertson r=27 Gallai-block reduction."""

from hashlib import sha256
from itertools import product
from json import dumps
from math import comb


K = 27
ROWS = (
    (53, 713, 8),
    (53, 714, 8),
    (53, 715, 9),
    (54, 726, 10),
)
EXPECTED_BOUNDARIES = {
    (53, 713): [(22, 23, 0, 1), (22, 23, 1, 0)],
    (53, 714): [(22, 23, 0, 0)],
    (53, 715): [
        (21, 23, 0, 2),
        (21, 23, 1, 1),
        (22, 22, 0, 3),
        (22, 22, 1, 2),
    ],
    (54, 726): [
        (21, 23, 0, 0),
        (22, 22, 0, 1),
        (22, 22, 1, 0),
    ],
}


def connected(mask: tuple[int, int, int, int]) -> bool:
    """Whether y_i and y_j connect in the two pair classes.

    The four possible cross-colour edges are, in order,
    y_i-y_j, y_i-x_j, x_i-y_j, x_i-x_j.
    """

    edges = ((0, 2), (0, 3), (1, 2), (1, 3))
    adjacency = [set() for _ in range(4)]
    for present, (u, v) in zip(mask, edges, strict=True):
        if present:
            adjacency[u].add(v)
            adjacency[v].add(u)
    reached = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u] - reached:
            reached.add(v)
            stack.append(v)
    return 2 in reached


def check_pair_masks() -> list[str]:
    admissible = []
    for mask in product((0, 1), repeat=4):
        if connected(mask):
            admissible.append("".join(map(str, mask)))
            if mask[0] == 0:
                # With y_i-y_j absent, the only possible connection is
                # y_i-x_j-x_i-y_j, so all other edges are forced.
                assert mask == (0, 1, 1, 1)
    assert len(admissible) == 9
    assert sum(mask[0] == "1" for mask in admissible) == 8
    return admissible


def minimum_fully_low_pairs(n: int, h: int) -> int:
    if n == 2 * K - 1:
        # G-v consists of K-1 pair classes.  Each high vertex spoils at
        # most one pair.
        return K - 1 - h
    if n == 2 * K:
        # G-v consists of K-2 pairs and one triple.  The worst case for
        # the pair count puts no high vertex in the triple.
        return K - 2 - h
    raise ValueError(n)


def structural_preconditions(n: int, h: int) -> tuple[int, int]:
    low = n - h
    full_pairs = minimum_fully_low_pairs(n, h)
    block_floor = full_pairs + 1
    assert full_pairs >= 3
    # A degree-(K-1) vertex cannot be the cut vertex of two such blocks.
    assert 2 * (block_floor - 1) > K - 1
    # At least two blocks are needed, while three do not fit.
    assert low > K - 1
    assert 3 * block_floor > low
    return low, block_floor


def profiles(n: int, m: int, h: int) -> list[tuple[int, int, int, int]]:
    """Enumerate every (a,b,t,r) compatible with the proved structure.

    Here t is the number of low-clique bridges and r is the number of
    missing edges in G[Q].  This computes the total edge count directly,
    rather than importing the target's excess-cap formula.
    """

    low, block_floor = structural_preconditions(n, h)
    answer = []
    for a in range(block_floor, K):
        b = low - a
        if not (a <= b < K and b >= block_floor):
            continue
        for t in (0, 1):
            low_edges = comb(a, 2) + comb(b, 2) + t
            low_high_edges = (K - 1) * low - 2 * low_edges
            if not 0 <= low_high_edges <= low * h:
                continue
            for r in range(comb(h, 2) + 1):
                high_edges = comb(h, 2) - r
                if low_edges + low_high_edges + high_edges == m:
                    answer.append((a, b, t, r))
    return answer


def check_rows() -> dict[str, list[list[int]]]:
    boundary_data = {}
    for n, m, first_h in ROWS:
        assert 2 * m - (K - 1) * n > 0
        for h in range(1, first_h):
            assert profiles(n, m, h) == []
        boundary = profiles(n, m, first_h)
        assert boundary == EXPECTED_BOUNDARIES[(n, m)]
        boundary_data[f"{n},{m}"] = [list(item) for item in boundary]
    return boundary_data


def main() -> None:
    masks = check_pair_masks()
    boundaries = check_rows()
    certificate = {"pair_masks": masks, "boundary_profiles": boundaries}
    digest = sha256(dumps(certificate, sort_keys=True).encode()).hexdigest()
    print("PASS independent Gallai-block audit")
    print(f"admissible pair-pair Kempe masks: {len(masks)}")
    for n, m, first_h in ROWS:
        print(f"(n,m)=({n},{m}): h>={first_h}; boundary={profiles(n,m,first_h)}")
    print(f"certificate_sha256={digest}")


if __name__ == "__main__":
    main()
