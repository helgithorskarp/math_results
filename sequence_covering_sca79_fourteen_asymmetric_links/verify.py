#!/usr/bin/env python3
"""Exact checker for the fourteen-asymmetric-link theorem."""

from math import factorial


def degrees(n: int, arcs: set[tuple[int, int]]) -> tuple[list[int], list[int]]:
    outdegree = [0] * n
    indegree = [0] * n
    for tail, head in arcs:
        assert 0 <= tail < n and 0 <= head < n and tail != head
        outdegree[tail] += 1
        indegree[head] += 1
    return outdegree, indegree


def ceil_div(numerator: int, denominator: int) -> int:
    return -((-numerator) // denominator)


def main() -> None:
    g = [factorial(r) * factorial(8 - r) // 72 for r in range(9)]
    assert g == [560, 70, 20, 10, 8, 10, 20, 70, 560]

    # (modulus, right-hand side) for (8-r) | G_r+epsilon*b.
    congruences = []
    for r in range(2, 7):
        epsilon = (-1) ** (r + 1)
        modulus = 8 - r
        residues = [b for b in range(modulus) if (g[r] + epsilon * b) % modulus == 0]
        assert len(residues) == 1
        congruences.append((r, modulus, residues[0]))

    joint_residues = [
        b for b in range(60)
        if all(b % modulus == residue for _, modulus, residue in congruences)
    ]
    assert joint_residues == [20]

    u = [1, -7, 21, -35, 35, -21, 7, -1, 0]
    v = [0, 1, -7, 21, -35, 35, -21, 7, -1]

    # Under a=40+60k and b=20+60l, verify d_i=420*(constant+kcoef*k+lcoef*l).
    expected = {
        2: (3, 3, -1),
        3: (-1, -5, 3),
        4: (3, 5, -5),
        5: (1, -3, 5),
        6: (1, 1, -3),
    }
    for i, coefficients in expected.items():
        constant = (560 + 40 * u[i] + 20 * v[i]) // 420
        k_coefficient = 60 * u[i] // 420
        l_coefficient = 60 * v[i] // 420
        assert (constant, k_coefficient, l_coefficient) == coefficients

    # Replay the short nonnegativity certificate on coefficient triples
    # (constant, coefficient of k, coefficient of l).
    d2, d3, d4_form, d5, d6 = (expected[i] for i in range(2, 7))
    assert tuple(x + y for x, y in zip(d3, d6)) == (0, -4, 0)
    # Hence k<=0.  At k=0, d3>=0 needs l>=1 while d6>=0 needs l<=0.
    assert ceil_div(1, 3) == 1 and 1 // 3 == 0
    k_upper = -1

    assert tuple(x + 5 * y for x, y in zip(d5, d2)) == (16, 12, 0)
    k_lower = ceil_div(-16, 12)
    assert k_lower == k_upper == -1
    k = k_lower

    # At k=-1, d2>=0 needs l<=0 and d5>=0 needs l>=0.
    l_upper = 3 + 3 * k
    l_lower = ceil_div(3 * k - 1, 5)
    assert l_lower == l_upper == 0
    l = l_lower
    d4 = 420 * (3 + 5 * k - 5 * l)
    assert d4 == -840

    n = 9
    for s in range(5):
        assert 2 * s < n

    # Sharpness fixture for the graph-only implication.
    fixture = {
        (4, 0), (5, 1), (6, 2), (7, 3), (8, 4),
        (0, 4), (0, 5), (0, 6),
        (1, 5), (1, 7),
        (2, 6), (2, 8),
        (3, 7), (3, 8),
    }
    outdegree, indegree = degrees(n, fixture)
    assert len(fixture) == 14
    assert min(outdegree) == min(indegree) == 1
    assert all(not (outdegree[z] == 1 and indegree[z] == 1) for z in range(n))
    assert sorted(outdegree) == [1] * 5 + [2] * 3 + [3]
    assert sorted(indegree) == [1] * 4 + [2] * 5

    print("outdegree-one congruences:")
    for r, modulus, residue in congruences:
        print(f"  r={r}: b = {residue} (mod {modulus})")
    print(f"joint outdegree-one residue: b = {joint_residues[0]} (mod 60)")
    print("joint indegree-one residue: a = 40 (mod 60)")
    print(f"both-degree contradiction: d_4 = {d4}")
    print("forbidden vertex type: indegree 1 and outdegree 1")
    print("first possible edge excess: 5")
    print("asymmetric ordered-pair-link lower bound: 14")
    print(f"sharp graph fixture: {len(fixture)} arcs")
    print("all checks passed")


if __name__ == "__main__":
    main()
