"""Run a token-deficit catalogue enumeration and exhaustive affine audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "upper_bound71"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    executable = out / "catalogue_orbit_check"
    catalogue = out / "catalogue.txt"
    subprocess.run(
        [
            "g++", "-O3", "-std=c++20", "-Wall", "-Wextra", "-Wconversion",
            str(HERE / "catalogue_orbit_check.cpp"), "-o", str(executable),
        ],
        check=True,
    )
    result = json.loads(
        subprocess.check_output(
            [str(executable), str(TARGET / "orbits.json"), str(catalogue)],
            text=True,
        )
    )
    result["catalogue_sha256"] = hashlib.sha256(catalogue.read_bytes()).hexdigest()
    expected = {
        "status": "INDEPENDENT_TOKEN_CATALOGUE_AND_FULL_AFFINE_AUDIT_VERIFIED",
        "typed_quotients": 16192,
        "labeled_counts_AA_AB_BB": [4442, 5428, 6322],
        "representatives": 4332,
        "canonical_counts_AA_AB_BB": [164, 1252, 2916],
        "affine_maps_per_representative": 12000,
        "normalized_images": 16192,
        "overlaps": 0,
        "published_orbit_sizes_match": True,
        "catalogue_sha256": "7ad44f1b9e1244da30d0ac28d29eb9f84e441323285b62cd21454827579fcb7f",
    }
    if result != expected:
        raise RuntimeError(f"independent catalogue/orbit audit disagrees: {result}")
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
