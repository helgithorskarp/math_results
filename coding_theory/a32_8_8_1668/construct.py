#!/usr/bin/env python3
"""Apply the recorded five-for-six exchange and emit the 1668-word code."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WITNESS_PATH = ROOT / "exchange.json"


def binary_from_hex(text: str) -> str:
    value = int(text, 16)
    return "".join("1" if value & (1 << index) else "0" for index in range(32))


def main() -> None:
    witness = json.loads(WITNESS_PATH.read_text(encoding="utf-8"))
    source_path = (ROOT / witness["source"]).resolve()
    source_bytes = source_path.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    if digest != witness["source_sha256"]:
        raise SystemExit(f"source hash mismatch: {digest}")

    source = [line.strip() for line in source_bytes.decode("ascii").splitlines() if line.strip()]
    if len(source) != 1667:
        raise SystemExit(f"expected 1667 source words, found {len(source)}")

    removed: set[int] = set()
    for entry in witness["removed"]:
        index = entry["zero_based_index"]
        if index in removed or not 0 <= index < len(source):
            raise SystemExit("invalid or duplicate removal index")
        if binary_from_hex(entry["hex"]) != entry["word"] or source[index] != entry["word"]:
            raise SystemExit(f"removed-word mismatch at index {index}")
        removed.add(index)

    added: list[str] = []
    for entry in witness["added"]:
        if binary_from_hex(entry["hex"]) != entry["word"]:
            raise SystemExit(f"added-word encoding mismatch for {entry['hex']}")
        added.append(entry["word"])

    result = [word for index, word in enumerate(source) if index not in removed] + added
    if len(result) != 1668 or len(set(result)) != 1668:
        raise SystemExit("exchange did not produce 1668 distinct words")
    print("\n".join(result))


if __name__ == "__main__":
    main()
