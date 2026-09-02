#!/usr/bin/env python3
"""Small definition-level and arithmetic boundary tests."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def valid_cycle_word(word: str) -> bool:
    entries = tuple(map(int, word))
    length = len(entries)
    for first in range(length):
        for second in range(first + 1, length):
            if entries[first] != entries[second]:
                continue
            separation = min(second - first, length - (second - first))
            if separation <= 2 * entries[first]:
                return False
    return True


def representable(n: int) -> bool:
    return any(n == 27 * a + 53 * b for a in range(n // 27 + 1) for b in range(n // 53 + 1))


def main() -> None:
    certificate = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))
    generators = certificate["common_base_cycle_words"]
    assert valid_cycle_word(generators["54"])
    assert valid_cycle_word(generators["106"])
    assert valid_cycle_word(generators["107"])
    # Concatenation is justified by closure at a common transfer state; check
    # representative even combinations directly from the cyclic definition.
    assert valid_cycle_word(generators["54"] + generators["106"])
    assert valid_cycle_word(generators["106"] * 2)

    assert not any(representable(n) for n in range(14, 27))
    assert [n for n in range(27, 108) if representable(n)] == [
        27,
        53,
        54,
        80,
        81,
        106,
        107,
    ]
    gaps = [n for n in range(1, 1352) if not representable(n)]
    assert len(gaps) == 676
    assert gaps[-1] == 1351
    assert all(representable(n) for n in range(1352, 2000))
    print("all boundary, concatenation, genus, and conductor tests passed")


if __name__ == "__main__":
    main()
