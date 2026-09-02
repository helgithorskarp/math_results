#!/usr/bin/env python3
"""Small exact tests for the reduction, verifier, and certificate rejection."""

from __future__ import annotations

from generate_cnf import cyclic_distance
from verify_witnesses import distances, load_witnesses, total_graph, verify_witness


def test_distance_reduction() -> None:
    for n in range(3, 31):
        metric = distances(total_graph(n))
        for a in range(2 * n):
            for b in range(2 * n):
                expected = (cyclic_distance(a, b, 2 * n) + 1) // 2
                assert metric[a][b] == expected, (n, a, b, metric[a][b], expected)


def test_all_witnesses() -> None:
    for raw_n, item in load_witnesses().items():
        verify_witness(int(raw_n), int(item["claimed_chi"]), list(map(int, item["word"])))


def test_corruption_rejected() -> None:
    item = load_witnesses()["14"]
    word = list(map(int, item["word"]))
    word[1] = word[0]
    try:
        verify_witness(14, int(item["claimed_chi"]), word)
    except AssertionError:
        return
    raise AssertionError("corrupted adjacent repeat was accepted")


def main() -> None:
    tests = [test_distance_reduction, test_all_witnesses, test_corruption_rejected]
    for test in tests:
        test()
    print(f"all {len(tests)} tests passed")


if __name__ == "__main__":
    main()
