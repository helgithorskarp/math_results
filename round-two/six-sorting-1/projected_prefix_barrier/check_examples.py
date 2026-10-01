#!/usr/bin/env python3
"""Replay fixed invalid research vectors and their necessary anchor bounds."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--profile-dir", type=Path, default=ROOT.parents[1] / "six-sorting-2" / "semantic-pruning")
    args = p.parse_args()
    for name, pin in [("profile.py", "dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719"),
                      ("anchors.py", "0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902")]:
        if hashlib.sha256((args.profile_dir / name).read_bytes()).hexdigest() != pin:
            raise ValueError("dependency differs: "+name)
    spec = importlib.util.spec_from_file_location("semantic_anchors", args.profile_dir / "anchors.py")
    anchors = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anchors)
    doc = json.loads((ROOT / "construction-examples.json").read_text())
    for case in doc["cases"]:
        if case["n"] != 13 or case["size"] != 44 or len(case["gates"]) != 44:
            raise ValueError("invalid fixture scope")
        anchors.semantic.validate(13, case["gates"])
        bad = []
        for mask in range(8192):
            values = [(mask >> i) & 1 for i in range(13)]
            for a, b in case["gates"]:
                if values[a] > values[b]:
                    values[a], values[b] = values[b], values[a]
            if values != sorted(values):
                bad.append(mask)
        if not bad or bad != case["failed_inputs"]:
            raise ValueError("complete failure list differs")
        data = anchors.both(13, anchors.semantic.analyze(13, case["gates"]))
        units = {side: item["normalized_mass"] for side, item in data.items()}
        if units != case["anchor_units"] or max(units.values()) > 512:
            raise ValueError("anchor-bound fixture differs")
        print(case["name"], "failed_inputs", len(bad), "anchor_units", units)


if __name__ == "__main__":
    main()
