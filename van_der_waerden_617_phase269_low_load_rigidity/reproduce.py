"""Frozen exact replay by default; optional bounded fresh LP generation."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def run(args):
    subprocess.run([sys.executable]+[str(a) for a in args], cwd=HERE, check=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--regenerate", action="store_true")
    p.add_argument("--work", type=Path, default=HERE / "build")
    args = p.parse_args()
    run(["verify.py", "certificate.json", "--base", "base/phase-269.json", "--base-checker", "base/verify.py", "--expected", "expected.json"])
    run(["controls.py"])
    if args.regenerate:
        work = args.work.resolve()
        work.mkdir(parents=True, exist_ok=True)
        run(["generate.py", "--output", work / "fresh.json", "--summary", work / "guidance.json"])
        run(["verify.py", work / "fresh.json", "--base", "base/phase-269.json", "--base-checker", "base/verify.py", "--output", work / "checked.json"])
        fresh = json.loads((work / "checked.json").read_text())
        frozen = json.loads((HERE / "expected.json").read_text())
        for key in ("forbidden_low_load_edit_positions_color0", "forbidden_low_load_edit_positions_color1"):
            if fresh[key] != frozen[key]:
                raise ValueError("Fresh coordinate restriction differs")


if __name__ == "__main__":
    main()
