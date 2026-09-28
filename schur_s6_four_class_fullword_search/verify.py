"""Regenerate and audit the exact CNFs recorded in expected.json."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from audit import check
from one_defect import write as write_one_defect

HERE = Path(__file__).resolve().parent


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(selected):
    expected = json.loads((HERE / "expected.json").read_text(encoding="ascii"))
    assert digest(HERE / "seed537.txt") == expected["seed_sha256"]
    cases = expected["zero_defect_cases"]
    assert set(cases) == {"12", "13", "15", "16", "23", "25", "26",
                          "35", "36", "56"}
    for pair in selected:
        reference = cases[pair]
        with tempfile.TemporaryDirectory(prefix=f"schur-fourtrade-{pair}-") as tmp:
            path = Path(tmp) / "case.cnf"
            subprocess.run([sys.executable, "-B", str(HERE / "encode.py"),
                            "--fixed", pair, "--seed", str(HERE / "seed537.txt"),
                            "--cnf", str(path)], check=True, capture_output=True)
            ports = check(HERE / "seed537.txt", tuple(map(int, pair)), path)
            assert len(ports) == reference["extra_fixed_colour_options"]
            if pair == "23":
                assert ports == [tuple(x) for x in expected["pair23_port_options"]]
            assert path.stat().st_size == reference["cnf_bytes"]
            assert digest(path) == reference["cnf_sha256"]
            print(f"MATCH zero_defect_fixed={pair}", flush=True)
    relaxed = expected["at_most_one_cases"]
    assert set(relaxed) == {"12", "23", "56"}
    for pair in sorted(set(selected) & set(relaxed)):
        reference = relaxed[pair]
        with tempfile.TemporaryDirectory(prefix=f"schur-one-defect-{pair}-") as tmp:
            path = Path(tmp) / "case.cnf"
            write_one_defect(HERE / "seed537.txt", tuple(map(int, pair)), path)
            assert path.stat().st_size == reference["cnf_bytes"]
            assert digest(path) == reference["cnf_sha256"]
            print(f"MATCH at_most_one_fixed={pair}", flush=True)
    print(f"PASS selected_zero_defect_cases={len(selected)}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pairs", nargs="*", default=[])
    args = parser.parse_args()
    data = json.loads((HERE / "expected.json").read_text(encoding="ascii"))
    selected = args.pairs or list(data["zero_defect_cases"])
    assert set(selected) <= set(data["zero_defect_cases"])
    verify(selected)
