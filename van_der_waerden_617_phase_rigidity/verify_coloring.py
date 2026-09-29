#!/usr/bin/env python3
"""Definition-level bit intersection checker for a supplied binary word."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def first_bad(word, k=7):
    n = len(word)
    ones = sum((b == "1") << i for i, b in enumerate(word))
    full = (1 << n) - 1
    for d in range(1, (n - 1) // (k - 1) + 1):
        for color, positions in enumerate((ones ^ full, ones)):
            starts = positions
            for j in range(1, k):
                starts &= positions >> (j * d)
            if starts:
                a = (starts & -starts).bit_length() - 1
                return a, d, color
    return None


def controls():
    # Different representation: explicit point tuples, complete small domain.
    for n in range(1, 10):
        for bits in itertools.product("01", repeat=n):
            word = "".join(bits)
            direct = any(len({word[a + j * d] for j in range(3)}) == 1
                         for d in range(1, (n - 1) // 2 + 1)
                         for a in range(n - 2 * d))
            assert (first_bad(word, 3) is not None) == direct
    assert first_bad("0" * 6) is None
    assert first_bad("0" * 7) == (0, 1, 0)
    assert first_bad("1" * 7) == (0, 1, 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()
    if args.controls:
        controls()
    data = args.path.read_bytes()
    word = data.decode("ascii").removesuffix("\n")
    if not word or set(word) - {"0", "1"}:
        raise SystemExit("Malformed coloring: expected one nonempty binary line")
    bad = first_bad(word)
    if bad is not None:
        a, d, color = bad
        print(json.dumps({"valid": False, "progression_one_based":
                          [a + 1 + j * d for j in range(7)], "color": color}))
        raise SystemExit(1)
    n = len(word)
    dmax = (n - 1) // 6
    print(json.dumps({"valid": True, "points": n,
                      "progressions_checked": dmax * n - 3 * dmax * (dmax + 1),
                      "file_sha256": hashlib.sha256(data).hexdigest()},
                     indent=2, sort_keys=True))
