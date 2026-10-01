"""Observed timing for the same literal input; timings are not proof premises."""

import argparse
import json
from pathlib import Path
import resource
from statistics import median
import sys
from time import monotonic

from check_orbits import run
from application import prepare
from budget import require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--optimizer", type=Path, required=True)
    args = parser.parse_args()
    fixture_path = Path(__file__).resolve().parent.parent / "mixed-outside-groups" / "input.json"
    fixture = json.loads(fixture_path.read_text())
    B, _, _, _, _, fixed, _, _, u, v = prepare(fixture, 48)
    samples = {"full": [], "quotient": []}
    exe = args.optimizer.resolve()
    for i in range(3):
        for quotient in ((False, True) if i % 2 == 0 else (True, False)):
            before = resource.getrusage(resource.RUSAGE_CHILDREN)
            started = monotonic()
            result = run(exe, B, 48, u, v, fixed, quotient)
            seconds = monotonic() - started
            after = resource.getrusage(resource.RUSAGE_CHILDREN)
            require(result["value"] == 174 and result["cofactor_tuples"] == (25 if quotient else 1225),
                    "benchmark changes the exact budget")
            samples["quotient" if quotient else "full"].append({
                "seconds": round(seconds, 6),
                "child_cpu_seconds": round(after.ru_utime + after.ru_stime -
                                           before.ru_utime - before.ru_stime, 6)})
    output = {"fixture": str(fixture_path.name), "period": 10080, "exact_value": 174,
              "full_tuples": 1225, "quotient_tuples": 25,
              "full_local_visits": 141120000, "quotient_local_visits": 2880000,
              "samples": samples, "child_peak_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              "python": sys.version.split()[0], "scope": "same-workload observations, not a speed guarantee"}
    for key, values in samples.items():
        output[key + "_median_seconds"] = round(median(x["seconds"] for x in values), 6)
        output[key + "_median_child_cpu_seconds"] = round(median(x["child_cpu_seconds"] for x in values), 6)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
