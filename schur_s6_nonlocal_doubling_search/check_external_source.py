"""Verify and normalize the attributed public six-class two-defect seed."""
import argparse
import hashlib
from pathlib import Path

from check_best3 import N, defects

HERE = Path(__file__).resolve().parent
RAW_SHA256 = "ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="upstream near_537_two_violations.col")
    args = parser.parse_args()
    data = args.source.read_bytes()
    assert hashlib.sha256(data).hexdigest() == RAW_SHA256
    classes = data.decode("ascii").splitlines()
    assert len(classes) == 6
    colours = [0] * (N + 1)
    for colour, line in enumerate(classes, start=1):
        values = [int(token) for token in line.split()]
        assert values
        for value in values:
            assert 1 <= value <= N and colours[value] == 0
            colours[value] = colour
    assert all(colours[1:])
    word = "".join(str(c) for c in colours[1:])
    assert word == (HERE / "external_two.txt").read_text(encoding="ascii").strip()
    assert defects(colours) == [(12, 12, 24, 4), (12, 24, 36, 4)]
    print("PASS upstream_sha256_match=yes exact_partition=yes "
          "normalized_word_match=yes seed_defects=2")


if __name__ == "__main__":
    main()
