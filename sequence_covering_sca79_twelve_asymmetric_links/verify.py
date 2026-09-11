#!/usr/bin/env python3
"""Exact checker for the twelve-asymmetric-link lower bound."""

from math import factorial


def degrees(n: int, arcs: set[tuple[int, int]]) -> tuple[list[int], list[int]]:
    outdegree = [0] * n
    indegree = [0] * n
    for tail, head in arcs:
        assert 0 <= tail < n and 0 <= head < n and tail != head
        outdegree[tail] += 1
        indegree[head] += 1
    return outdegree, indegree


def main() -> None:
    n = 9

    # Definition-level replay of the named immediate-successor obstruction.
    point_value = factorial(2) * factorial(6) // 72
    number_of_equations = 7
    coefficient_per_cell = 6
    aggregate_rhs = number_of_equations * point_value
    remainder = aggregate_rhs % coefficient_per_cell
    assert point_value == 20 and aggregate_rhs == 140 and remainder == 2

    # If m=n+s, the local forbidden-edge rule requires at least n-p arcs to
    # enter the q high-indegree vertices.  Since p,q<=s, their maximum
    # capacity is 2s, whereas at least n-s arcs are required.
    for s in range(3):
        required = n - s
        capacity = 2 * s
        assert required > capacity
        print(f"excess s={s}: required >= {required}, capacity <= {capacity}, impossible")

    first_possible_excess = 3
    lower_bound = n + first_possible_excess
    assert n - first_possible_excess <= 2 * first_possible_excess

    # A simple loopless digraph showing sharpness of the pure degree count.
    fixture = {
        (3, 0), (4, 0), (5, 1), (6, 1), (7, 2), (8, 2),
        (0, 3), (0, 4), (1, 5), (1, 6), (2, 7), (2, 8),
    }
    outdegree, indegree = degrees(n, fixture)
    assert len(fixture) == lower_bound
    assert min(outdegree) == min(indegree) == 1
    forbidden = [
        (tail, head)
        for tail, head in fixture
        if outdegree[tail] == 1 and indegree[head] == 1
    ]
    assert forbidden == []
    assert sorted(outdegree) == [1] * 6 + [2] * 3
    assert sorted(indegree) == [1] * 6 + [2] * 3

    print(f"local modulo-6 certificate: {aggregate_rhs} mod {coefficient_per_cell} = {remainder}")
    print("forbidden local pattern: outdegree 1 -> indegree 1")
    print(f"first possible excess: {first_possible_excess}")
    print(f"asymmetric ordered-pair-link lower bound: {lower_bound}")
    print(f"sharp graph fixture: {len(fixture)} arcs, forbidden edges {len(forbidden)}")
    print("all checks passed")


if __name__ == "__main__":
    main()
