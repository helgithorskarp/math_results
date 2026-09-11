#!/usr/bin/env python3
"""Definition-level checker for the A(32,8,8) local-exchange certificate."""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from itertools import combinations
from pathlib import Path

EXPECTED_CODE_SHA256 = "161367ae8fafd7c8595b891437a95670968a8a65c0feac77000d0b1c3cfe40a7"
EXPECTED_LOW_SHA256 = "cf73bef6e8d9f0645fbf47e18fd764e4deebb30c09ad1538c67ea60f883091ea"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_code(path: Path) -> list[int]:
    words: list[int] = []
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if len(line) != 32 or set(line) - {"0", "1"}:
            raise AssertionError(f"malformed incumbent line {line_number}")
        # Match the upstream C representation: textual coordinate i is bit i.
        word = sum((character == "1") << i for i, character in enumerate(line))
        if word.bit_count() != 8:
            raise AssertionError(f"incumbent line {line_number} has weight != 8")
        words.append(word)
    if len(words) != 1667 or len(set(words)) != 1667:
        raise AssertionError("incumbent must contain 1667 distinct words")
    minimum_distance = min((left ^ right).bit_count() for left, right in combinations(words, 2))
    if minimum_distance != 8:
        raise AssertionError(f"expected incumbent minimum distance 8, found {minimum_distance}")
    return words


def load_low_candidates(path: Path) -> list[tuple[int, tuple[int, ...]]]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or lines[0] != "word_hex\tblocker_count\tblockers_zero_based":
        raise AssertionError("unexpected low-candidate header")
    records: list[tuple[int, tuple[int, ...]]] = []
    for line_number, line in enumerate(lines[1:], 2):
        fields = line.split("\t")
        if len(fields) != 3:
            raise AssertionError(f"malformed low-candidate line {line_number}")
        word = int(fields[0], 16)
        blocker_count = int(fields[1])
        blockers = tuple(int(value) for value in fields[2].split(",") if value)
        if blocker_count != len(blockers) or blocker_count not in (1, 2):
            raise AssertionError(f"bad blocker count on line {line_number}")
        if tuple(sorted(blockers)) != blockers or len(set(blockers)) != len(blockers):
            raise AssertionError(f"noncanonical blocker set on line {line_number}")
        records.append((word, blockers))
    if len(records) != 794 or len({word for word, _ in records}) != 794:
        raise AssertionError("expected 794 distinct low candidates")
    if records != sorted(records):
        raise AssertionError("low candidates are not canonically sorted")
    return records


def compatible(left: int, right: int) -> bool:
    return (left & right).bit_count() <= 4


def verify_records(code: list[int], records: list[tuple[int, tuple[int, ...]]]) -> None:
    code_set = set(code)
    for word, claimed_blockers in records:
        if word < 0 or word >= 1 << 32 or word.bit_count() != 8 or word in code_set:
            raise AssertionError(f"invalid outsider word {word:08x}")
        actual_blockers = tuple(
            index for index, incumbent in enumerate(code) if (word & incumbent).bit_count() >= 5
        )
        if actual_blockers != claimed_blockers:
            raise AssertionError(
                f"blocker mismatch for {word:08x}: claimed {claimed_blockers}, actual {actual_blockers}"
            )


def verify_exchanges(
    code: list[int], records: list[tuple[int, tuple[int, ...]]]
) -> tuple[int, int, int, int]:
    singleton: dict[int, list[int]] = defaultdict(list)
    pair_bucket: dict[tuple[int, int], list[int]] = defaultdict(list)
    for word, blockers in records:
        if len(blockers) == 1:
            singleton[blockers[0]].append(word)
        else:
            pair_bucket[blockers].append(word)

    one_removal_pairs = 0
    for removed in range(len(code)):
        for left, right in combinations(singleton.get(removed, ()), 2):
            one_removal_pairs += 1
            if compatible(left, right):
                raise AssertionError(f"improving one-removal exchange at incumbent {removed}")

    removal_pairs = 0
    nontrivial_pools = 0
    add_triples = 0
    for first_removed in range(len(code)):
        for second_removed in range(first_removed + 1, len(code)):
            removal_pairs += 1
            pool = [
                *singleton.get(first_removed, ()),
                *singleton.get(second_removed, ()),
                *pair_bucket.get((first_removed, second_removed), ()),
            ]
            if len(pool) < 3:
                continue
            nontrivial_pools += 1
            for left, middle, right in combinations(pool, 3):
                add_triples += 1
                if compatible(left, middle) and compatible(left, right) and compatible(middle, right):
                    raise AssertionError(
                        f"improving two-removal exchange at incumbents {first_removed},{second_removed}"
                    )
    return one_removal_pairs, removal_pairs, nontrivial_pools, add_triples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("code", type=Path)
    parser.add_argument("low_candidates", type=Path)
    args = parser.parse_args()

    code_sha = file_sha256(args.code)
    low_sha = file_sha256(args.low_candidates)
    if code_sha != EXPECTED_CODE_SHA256:
        raise AssertionError(f"unexpected incumbent SHA-256: {code_sha}")
    if low_sha != EXPECTED_LOW_SHA256:
        raise AssertionError(f"unexpected low-candidate SHA-256: {low_sha}")

    code = load_code(args.code)
    records = load_low_candidates(args.low_candidates)
    verify_records(code, records)
    singleton_count = sum(len(blockers) == 1 for _, blockers in records)
    double_count = sum(len(blockers) == 2 for _, blockers in records)
    if (singleton_count, double_count) != (158, 636):
        raise AssertionError("unexpected blocker-count split")
    counts = verify_exchanges(code, records)
    if counts != (76, 1_388_611, 17_965, 107_820):
        raise AssertionError(f"unexpected exchange enumeration counts: {counts}")

    print("incumbent_size=1667")
    print("incumbent_minimum_distance=8")
    print("low_candidate_count=794")
    print("low_candidate_blocker_counts=1:158,2:636")
    print("one_removal_add_pairs_tested=76")
    print("two_removal_pairs_tested=1388611")
    print("two_removal_pools_with_at_least_three_candidates=17965")
    print("two_removal_add_triples_tested=107820")
    print("conclusion=incumbent_is_2_exchange_maximal")
    print("verification=PASS")


if __name__ == "__main__":
    main()
