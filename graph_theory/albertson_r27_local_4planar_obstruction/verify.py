#!/usr/bin/env python3
"""Exact arithmetic audit for the 24-vertex Albertson obstruction.

The mathematical meanings of the variables and the imported inequalities are
given in README.md.  This program checks only their finite integer
consequences and the subsequent induced-subgraph sampling arithmetic.
"""

from fractions import Fraction as Q
from math import comb


N = 24
S = N - 2
M = 132
ASSUMED_CROSSINGS = 164


def ceil_div(a: int, b: int) -> int:
    assert b > 0
    return -((-a) // b)


def enumerate_profiles() -> list[tuple[int, ...]]:
    """Enumerate every integer profile allowed by the cited inequalities.

    A returned tuple is
      (a,b,c,d,Delta,m0,p,h,t,e2,x2,total),
    using the notation of README.md.
    """
    profiles = []
    five_s = 5 * S

    # The first deletion phase removes exactly M-5S=22 edges.
    for a in range(M - five_s + 1):
        for b in range(M - five_s - a + 1):
            c = M - five_s - a - b

            # D_2 has 5S-2c-d edges, so this is an absolute bound on d.
            for d in range(five_s - 2 * c + 1):
                e2 = five_s - 2 * c - d

                # Delta is at most the 2S faces of a plane triangulation.
                for Delta in range(2 * S + 1):
                    x2 = ceil_div(7 * e2 - 25 * S + 2 * Delta, 3)
                    total = 5 * a + 4 * b + 9 * c + 3 * d + x2
                    if total > ASSUMED_CROSSINGS:
                        continue

                    # Combining the configuration lower bound with the
                    # triangulation identity gives 3m0+h <= 3d, hence m0<=d.
                    for m0 in range(d + 1):
                        for p in range((2 * S - 4 * c) // 3 + 1):
                            for h in range((2 * S - 4 * c - 3 * p) // 4 + 1):
                                t = 2 * S - 4 * c - 3 * p - 4 * h
                                assert t >= 0

                                # Büngener--Kaufmann, Proposition 11.
                                if 3 * (p + h) < 2 * S - 4 * c - 3 * d + 3 * m0:
                                    continue

                                # Büngener--Kaufmann, Proposition 12.
                                if b > c + h + 4 * m0 + 2 * t:
                                    continue

                                profiles.append(
                                    (a, b, c, d, Delta, m0, p, h, t, e2, x2, total)
                                )
    return profiles


def conditional_sampling_bound() -> Q:
    """Order-54 sampled bound if cr(24,132)>=165 is available."""
    return Q(
        5 * 726 * comb(52, 22) - 495 * comb(54, 24),
        comb(50, 20),
    )


def main() -> None:
    # Arithmetic in the three ranges used to derive cr >= 5e-495 from the
    # single local target.  The e>132 range additionally imports the
    # 4-planar density/deletion argument described in README.md.
    for e in range(132):
        assert ceil_div(37 * e - 155 * S, 9) >= 5 * e - 495
    assert 165 == 5 * 132 - 495
    for e in range(133, comb(N, 2) + 1):
        assert 165 + 5 * (e - 132) == 5 * e - 495

    profiles = enumerate_profiles()
    expected = [
        (0, 20, 2, 3, 0, 0, 9, 0, 9, 103, 57, 164),
        (0, 22, 0, 4, 0, 0, 11, 0, 11, 106, 64, 164),
    ]
    assert profiles == expected

    # In an equality remainder the Pach--Radoicic--Tardos--Toth induction
    # gives only K_2 and C_5 components in the edge-crossing graph.  Reducing
    # each C_5 to the terminal 1-planar equality case gives this count.
    crossing_components = []
    for profile in profiles:
        e2, x2, p_full = profile[9], profile[10], profile[6]
        c5 = (2 * e2 - 8 * S) // 3
        assert 3 * c5 == 2 * e2 - 8 * S
        k2 = x2 - 5 * c5
        free_edges = e2 - 5 * c5 - 2 * k2
        assert (c5, k2, free_edges, c5 - p_full) in (
            (10, 7, 39, 1),
            (12, 4, 38, 1),
        )
        crossing_components.append((c5, k2, free_edges, c5 - p_full))

    bound = conditional_sampling_bound()
    assert bound == Q(1965795, 322)
    assert bound > 6084
    assert ceil_div(bound.numerator, bound.denominator) == 6105

    print("PASS exact 24-vertex obstruction audit")
    for profile, components in zip(profiles, crossing_components):
        print(f"profile={profile}")
        print(
            "  D2 crossing graph: "
            f"C5={components[0]}, K2={components[1]}, "
            f"free_edges={components[2]}, non_full_C5={components[3]}"
        )
    print(
        "conditional order-54 bound from cr(24,132)>=165: "
        f"{bound} = {float(bound):.12f}, hence cr(G)>=6105>6084"
    )


if __name__ == "__main__":
    main()
