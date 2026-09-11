#!/usr/bin/env python3
"""Definition-level audit through radius three for the A(32,8,8) incumbent."""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from itertools import combinations
from pathlib import Path

CODE_SHA256 = "161367ae8fafd7c8595b891437a95670968a8a65c0feac77000d0b1c3cfe40a7"
LOW3_SHA256 = "0b2bc13d80e514df8e6937f8b271eb5da4decd67c9ec71f8de53a2f1f9fb35e3"
LOW4_SHA256 = "6dd9393d0e1cf5768161bd074ea0eb1410f03f7419c448b92b43f69613d73138"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_code(path: Path) -> list[int]:
    words = []
    for line_number, line in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        if len(line) != 32 or set(line) - {"0", "1"}:
            raise AssertionError(f"malformed code line {line_number}")
        word = sum((character == "1") << index for index, character in enumerate(line))
        if word.bit_count() != 8:
            raise AssertionError(f"wrong weight on code line {line_number}")
        words.append(word)
    if len(words) != 1667 or len(set(words)) != 1667:
        raise AssertionError("expected 1667 distinct incumbent words")
    minimum_distance = min((left ^ right).bit_count() for left, right in combinations(words, 2))
    if minimum_distance != 8:
        raise AssertionError(f"unexpected minimum distance {minimum_distance}")
    return words


def load_candidates(path: Path, maximum_blockers: int) -> list[tuple[int, tuple[int, ...]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "word_hex\tblocker_count\tblockers_zero_based":
        raise AssertionError("unexpected candidate header")
    records = []
    for line in lines[1:]:
        word_text, count_text, blocker_text = line.split("\t")
        blockers = tuple(map(int, blocker_text.split(",")))
        record = (int(word_text, 16), blockers)
        if len(blockers) != int(count_text) or not 1 <= len(blockers) <= maximum_blockers:
            raise AssertionError("bad blocker record")
        records.append(record)
    if records != sorted(records) or len({word for word, _ in records}) != len(records):
        raise AssertionError("candidate list is not unique and canonically ordered")
    return records


def compatible(left: int, right: int) -> bool:
    return (left & right).bit_count() <= 4


def verify_candidate_records(code: list[int], records: list[tuple[int, tuple[int, ...]]]) -> None:
    code_set = set(code)
    for word, claimed in records:
        if word.bit_count() != 8 or word in code_set:
            raise AssertionError(f"invalid outsider {word:08x}")
        actual = tuple(index for index, incumbent in enumerate(code) if (word & incumbent).bit_count() >= 5)
        if actual != claimed:
            raise AssertionError(f"blocker mismatch for {word:08x}")


def verify_radii_one_and_two(records: list[tuple[int, tuple[int, ...]]]) -> tuple[int, int, int]:
    singleton: dict[int, list[int]] = defaultdict(list)
    pairs: dict[tuple[int, int], list[int]] = defaultdict(list)
    for word, blockers in records:
        if len(blockers) == 1:
            singleton[blockers[0]].append(word)
        elif len(blockers) == 2:
            pairs[blockers].append(word)
    one_pairs = 0
    for words in singleton.values():
        for left, right in combinations(words, 2):
            one_pairs += 1
            if compatible(left, right):
                raise AssertionError("one-removal improvement exists")
    nontrivial = triples_tested = 0
    for first in range(1667):
        for second in range(first + 1, 1667):
            pool = [*singleton.get(first, ()), *singleton.get(second, ()), *pairs.get((first, second), ())]
            if len(pool) < 3:
                continue
            nontrivial += 1
            for triple in combinations(pool, 3):
                triples_tested += 1
                if all(compatible(left, right) for left, right in combinations(triple, 2)):
                    raise AssertionError("two-removal improvement exists")
    return one_pairs, nontrivial, triples_tested


def verify_radius_three(records: list[tuple[int, tuple[int, ...]]]) -> tuple[int, int, int, int]:
    buckets: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for word, blockers in records:
        buckets[blockers].append(word)
    supports = sorted(buckets)
    removals: set[tuple[int, int, int]] = set()
    for first_index, first in enumerate(supports):
        first_set = set(first)
        for second in supports[first_index:]:
            union = first_set | set(second)
            if len(union) == 3:
                removals.add(tuple(sorted(union)))

    nontrivial = all_quadruples = 0
    maximum_pool = 0
    for removed in sorted(removals):
        pool = []
        for size in range(1, 4):
            for support in combinations(removed, size):
                pool.extend(buckets.get(support, ()))
        maximum_pool = max(maximum_pool, len(pool))
        if len(pool) < 4:
            continue
        nontrivial += 1
        for quadruple in combinations(pool, 4):
            all_quadruples += 1
            if all(compatible(left, right) for left, right in combinations(quadruple, 2)):
                raise AssertionError("three-removal improvement exists")
    return len(removals), nontrivial, all_quadruples, maximum_pool


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("code", type=Path)
    parser.add_argument("low3", type=Path)
    parser.add_argument("low4", type=Path)
    args = parser.parse_args()
    if (digest(args.code), digest(args.low3), digest(args.low4)) != (
        CODE_SHA256,
        LOW3_SHA256,
        LOW4_SHA256,
    ):
        raise AssertionError("input hash mismatch")

    code = load_code(args.code)
    low3 = load_candidates(args.low3, 3)
    low4 = load_candidates(args.low4, 4)
    if low3 != [record for record in low4 if len(record[1]) <= 3]:
        raise AssertionError("threshold-three list is not the exact low4 restriction")
    if tuple(sum(len(blockers) == count for _, blockers in low4) for count in range(1, 5)) != (
        158,
        636,
        1562,
        3695,
    ):
        raise AssertionError("unexpected low-blocker histogram")
    verify_candidate_records(code, low4)
    radius12 = verify_radii_one_and_two(low3)
    radius3 = verify_radius_three(low3)
    if radius12 != (76, 17_965, 107_820):
        raise AssertionError(f"unexpected radius-one/two counts {radius12}")
    if radius3 != (64_651, 19_020, 722_417, 18):
        raise AssertionError(f"unexpected radius-three counts {radius3}")

    print("incumbent_size=1667")
    print("incumbent_minimum_distance=8")
    print("low4_blocker_histogram=1:158,2:636,3:1562,4:3695")
    print("radius_one_add_pairs=76")
    print("radius_two_nontrivial_pools=17965")
    print("radius_two_add_triples=107820")
    print("radius_three_removal_sets=64651")
    print("radius_three_nontrivial_pools=19020")
    print("radius_three_all_add_quadruples=722417")
    print("radius_three_maximum_pool=18")
    print("conclusion_through_radius_three=PASS")


if __name__ == "__main__":
    main()
