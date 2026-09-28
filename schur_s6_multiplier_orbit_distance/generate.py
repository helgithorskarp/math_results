"""Regenerate the compact orbit certificate by deterministic randomized search.

This program finds witnesses; check.py independently validates their proof.
"""

from __future__ import annotations

import argparse
import json
import lzma
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def trial(task: tuple[int, str, str]) -> tuple[int, dict]:
    m, encoded, directory = task
    root = Path(directory) / str(m)
    root.mkdir()
    (root / "search.py").write_bytes((HERE / "search.py").read_bytes())
    inverse = pow(m, -1, 537)
    baseline = [0] + [int(d) for d in encoded]
    transformed = "".join(str(baseline[(inverse * x) % 537])
                          for x in range(1, 537))
    (root / "baseline.txt").write_text(transformed + "\n", encoding="ascii")
    output = root / "certificate.json"
    for trials in (100, 500, 3000):
        subprocess.run([sys.executable, str(root / "search.py"),
                        "--trials", str(trials), "--output", str(output)],
                       check=True, capture_output=True, text=True)
        raw = json.loads(output.read_text(encoding="utf-8"))["selected_by_color"]
        if len(raw["5"]) >= 18:
            break
    lengths = tuple(len(raw[str(c)]) for c in (2, 4, 5, 6))
    if not (lengths[0] >= 8 and lengths[1] >= 13 and lengths[2] >= 17
            and lengths[3] >= 16):
        raise RuntimeError(f"weak witness search for multiplier {m}: {lengths}")
    packed = {str(c): [[entry["pair"][0],
                        [a for witness in entry["witnesses"]
                         for a in witness["triple"][:2]]]
                       for entry in raw[str(c)]]
              for c in (2, 4, 5, 6)}
    return m, packed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--multipliers", help="comma-separated unit subset for a sample")
    args = parser.parse_args()
    if not 1 <= args.workers <= 16:
        parser.error("workers must be between 1 and 16")
    encoded = (HERE / "baseline.txt").read_text(encoding="ascii").strip()
    if len(encoded) != 536 or set(encoded) != set("123456"):
        raise ValueError("bad baseline")
    units = [m for m in range(1, 537) if gcd(m, 537) == 1]
    if args.multipliers:
        selected = [int(word) for word in args.multipliers.split(",")]
        if len(set(selected)) != len(selected) or any(m not in units for m in selected):
            parser.error("multipliers must be distinct units modulo 537")
        units = selected
    with tempfile.TemporaryDirectory(prefix="schur-orbit-distance-") as directory:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            results = dict(pool.map(trial, [(m, encoded, directory) for m in units]))
    if len(units) == 356:
        weak = {m for m in units if len(results[m]["5"]) == 17}
        if weak != {83, 454}:
            raise RuntimeError(f"unexpected 49-group cases: {weak}")
    data = {str(m): results[m] for m in sorted(units)}
    args.output.write_bytes(lzma.compress(
        json.dumps(data, separators=(",", ":")).encode("utf-8"), preset=6))
    print(f"generated={len(units)} bytes={args.output.stat().st_size} "
          f"weak_49={sum(len(results[m]['5']) == 17 for m in units)}")


if __name__ == "__main__":
    main()
