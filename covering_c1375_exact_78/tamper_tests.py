#!/usr/bin/env python3
"""Check that the end-to-end verifier rejects representative corruptions."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(checker, paths):
    return subprocess.run(
        [sys.executable, str(checker), *(str(path) for path in paths)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode


def write_json(path, document):
    path.write_text(json.dumps(document, sort_keys=True) + "\n", encoding="ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_link", type=Path)
    parser.add_argument("prior_witness", type=Path)
    parser.add_argument("prior_certificates", type=Path)
    parser.add_argument("hard_e1_certificate", type=Path)
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()
    checker = Path(__file__).with_name("independent_bitmask_check.py")
    baseline = [
        args.source_link,
        args.prior_witness,
        args.prior_certificates,
        args.hard_e1_certificate,
        args.certificates,
    ]
    if run(checker, baseline) != 0:
        raise AssertionError("baseline end-to-end check failed")

    new = json.loads(args.certificates.read_text(encoding="ascii"))
    prior = json.loads(args.prior_certificates.read_text(encoding="ascii"))
    hard = json.loads(args.hard_e1_certificate.read_text(encoding="ascii"))
    tests = []
    with tempfile.TemporaryDirectory(prefix="c1375-tamper-") as raw:
        temporary = Path(raw)

        changed = copy.deepcopy(new)
        changed["profile_cases"][0]["gap"] += 1
        path = temporary / "new-gap.json"
        write_json(path, changed)
        tests.append(("new-gap", baseline[:4] + [path]))

        changed = copy.deepcopy(new)
        changed["profile_cases"].pop()
        path = temporary / "new-case-deleted.json"
        write_json(path, changed)
        tests.append(("new-case-deleted", baseline[:4] + [path]))

        changed = copy.deepcopy(new)
        multipliers = changed["profile_cases"][0]["multipliers"]
        multipliers[1][0] = multipliers[0][0]
        path = temporary / "new-duplicate-row.json"
        write_json(path, changed)
        tests.append(("new-duplicate-row", baseline[:4] + [path]))

        changed = copy.deepcopy(prior)
        changed["cases"][11]["gap"] += 1
        path = temporary / "prior-gap.json"
        write_json(path, changed)
        tests.append(("prior-gap", [baseline[0], baseline[1], path, baseline[3], baseline[4]]))

        changed = copy.deepcopy(hard)
        changed["arithmetic"]["strict_gap"] += 1
        path = temporary / "hard-arithmetic.json"
        write_json(path, changed)
        tests.append(("hard-arithmetic", [baseline[0], baseline[1], baseline[2], path, baseline[4]]))

        rejected = []
        for label, paths in tests:
            if run(checker, paths) == 0:
                raise AssertionError(f"checker accepted corruption: {label}")
            rejected.append(label)

    print("baseline_end_to_end_check=PASS")
    print(f"tamper_rejections={len(rejected)}/{len(tests)} labels=" + ",".join(rejected))


if __name__ == "__main__":
    main()
