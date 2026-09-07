#!/usr/bin/env python3
"""Definition-level verifier for a claimed 43-vertex Ramsey graph."""

from itertools import combinations
import json
from pathlib import Path
import re
import sys


def main() -> None:
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if set(data) != {"n", "red_hex"} or data["n"] != 43:
        raise ValueError("expected exactly n=43 and red_hex")
    raw = data["red_hex"]
    if not isinstance(raw, str) or re.fullmatch(r"[0-9a-f]{226}", raw) is None:
        raise ValueError("red_hex must contain exactly 226 lowercase hex digits")
    bits = int(raw, 16)
    pairs = list(combinations(range(43), 2))
    if bits >= 1 << len(pairs):
        raise ValueError("bits outside the 903 physical edges")
    index = {edge: i for i, edge in enumerate(pairs)}
    checked = 0
    for vertices in combinations(range(43), 5):
        colors = [bool((bits >> index[edge]) & 1)
                  for edge in combinations(vertices, 2)]
        if all(colors) or not any(colors):
            raise ValueError(f"monochromatic five-set: {vertices}")
        checked += 1
    print(json.dumps({"status": "VERIFIED_GOOD43", "five_sets": checked},
                     sort_keys=True))


if __name__ == "__main__":
    main()
