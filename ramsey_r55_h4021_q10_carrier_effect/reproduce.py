#!/usr/bin/env python3
"""Fresh-output normal/-O replay with independent and corruption checks."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def invoke(flags, script, *args, check=True):
    return subprocess.run([sys.executable, *flags, "-B", str(HERE / script),
                           *map(str, args)], check=check, capture_output=True)


def reproduce(destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((HERE / "MANIFEST.json").read_text())
    for name, expected in manifest.items():
        actual = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        need(actual == expected, "source identity: " + name)
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    receipts = {}
    for label, flags in (("normal", []), ("optimized", ["-O"])):
        result_path = destination / f"{label}-result.json"
        produced = invoke(flags, "analyze.py")
        result_path.write_bytes(produced.stdout)
        need(json.loads(produced.stdout) == expected, "frozen expected result")
        independent = invoke(flags, "independent_check.py", result_path)
        controls = invoke(flags, "controls.py")
        corruptions = 0
        for field in ("eligible", "closure", "maximum"):
            bad = json.loads(produced.stdout)
            if field == "eligible":
                bad["carrier"]["eligible_root_color_pairs"] = 1
            elif field == "closure":
                bad["carrier"]["new_task_closures"] = 1
            else:
                bad["carrier"]["maximum_fixed_red_degree"] = 18
            path = destination / f"{label}-bad-{field}.json"
            path.write_text(json.dumps(bad) + "\n")
            rejected = invoke(flags, "independent_check.py", path, check=False)
            need(rejected.returncode != 0, "corruption was accepted: " + field)
            corruptions += 1
        receipts[label] = {
            "independent": json.loads(independent.stdout),
            "controls": json.loads(controls.stdout),
            "deliberate_result_corruptions_rejected": corruptions,
        }
    answer = {"status": "REPRODUCED_H4021_Q10_ZERO_DIRECT_CARRIER_EFFECT",
              "normal_and_optimized": True, "solver_calls": 0,
              "receipts": receipts, "python": sys.version}
    (destination / "RECEIPT.json").write_text(
        json.dumps(answer, indent=2, sort_keys=True) + "\n")
    return answer


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: reproduce.py FRESH_OUTPUT_DIRECTORY")
    print(json.dumps(reproduce(sys.argv[1]), sort_keys=True))
