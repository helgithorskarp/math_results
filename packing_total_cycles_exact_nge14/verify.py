#!/usr/bin/env python3
"""Definition-level checker for the exact n >= 14 cycle formula."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_certificate() -> dict[str, object]:
    data = json.loads((HERE / "certificate.json").read_text())
    if not isinstance(data, dict):
        raise AssertionError("certificate must be a JSON object")
    return data


def verify_cyclic_word(n: int, word: list[int]) -> None:
    """Check the cyclic gap definition for C_(2n)^2 directly."""
    if len(word) != 2 * n:
        raise AssertionError(f"order {n}: word has length {len(word)}, not {2*n}")
    if not word or min(word) < 1 or max(word) > 9:
        raise AssertionError(f"order {n}: colors must lie in 1,...,9")
    for color in range(1, 10):
        positions = [position for position, value in enumerate(word) if value == color]
        if not positions:
            continue
        cyclic_positions = positions + [positions[0] + len(word)]
        gaps = [right - left for left, right in zip(cyclic_positions, cyclic_positions[1:])]
        if min(gaps) < 2 * color + 1:
            raise AssertionError(f"order {n}: color {color} has gaps {gaps}")


def step(state: tuple[int, ...], color: int, caps: tuple[int, ...]) -> tuple[int, ...]:
    chosen = color - 1
    if state[chosen] != caps[chosen]:
        raise AssertionError(f"color {color} unavailable in state {state}")
    return tuple(
        0 if index == chosen else min(value + 1, caps[index])
        for index, value in enumerate(state)
    )


def verify_common_return(
    word: list[int], base: tuple[int, ...], caps: tuple[int, ...]
) -> None:
    state = base
    for color in word:
        state = step(state, color, caps)
    if state != base:
        raise AssertionError(f"word ends at {state}, not common base {base}")


def common_word(n: int, words: dict[int, list[int]]) -> list[int]:
    """Construct a common-base word for every n >= 23 by subtracting 17."""
    if n < 23:
        raise ValueError("common induction begins at order 23")
    pieces: list[list[int]] = []
    while n >= 40:
        pieces.append(words[17])
        n -= 17
    if n not in range(23, 40):
        raise AssertionError(f"induction ended outside base interval: {n}")
    pieces.append(words[n])
    return [color for piece in pieces for color in piece]


def main() -> None:
    data = load_certificate()
    caps = tuple(map(int, data["caps"]))
    base = tuple(map(int, data["base_ages"]))
    if caps != tuple(range(2, 19, 2)) or len(base) != 9:
        raise AssertionError("unexpected transfer parameters")

    common = {
        int(n): list(map(int, word))
        for n, word in data["common_base_words"].items()
    }
    standalone = {
        int(n): list(map(int, word))
        for n, word in data["standalone_words"].items()
    }
    if set(common) != {17, *range(23, 40)}:
        raise AssertionError(f"wrong common-base orders: {sorted(common)}")
    if set(standalone) != set(range(18, 23)):
        raise AssertionError(f"wrong standalone orders: {sorted(standalone)}")

    for n, word in sorted(common.items()):
        verify_cyclic_word(n, word)
        verify_common_return(word, base, caps)
    for n, word in sorted(standalone.items()):
        verify_cyclic_word(n, word)
    print(f"verified {len(common)} common-base loops and {len(standalone)} standalone words")

    for n in range(23, 2001):
        word = common_word(n, common)
        verify_cyclic_word(n, word)
        verify_common_return(word, base, caps)
    print("verified the common-base induction for every order 23 through 2000")
    print("therefore every C_n with n >= 17 has a 9-color packing total coloring")
    print("combined with the cited exact lower bounds: the n >= 14 formula follows")


if __name__ == "__main__":
    main()
