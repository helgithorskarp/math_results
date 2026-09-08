#!/usr/bin/env python3
"""Positive replay and three certificate-rejection controls."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent


def run(path: Path) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, "-B", str(HERE / "verify.py"), str(path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    original = json.loads((HERE / "certificate.json").read_text())
    positive = run(HERE / "certificate.json")
    need(positive.returncode == 0, "uncorrupted certificate was rejected")

    controls = []
    with tempfile.TemporaryDirectory(prefix="royle80-controls-") as temp_name:
        temp = Path(temp_name)

        bad_lcf = json.loads(json.dumps(original))
        bad_lcf["lcf"]["rows"]["0"][2] = 31
        controls.append(("altered_lcf_entry", bad_lcf))

        bad_colouring = json.loads(json.dumps(original))
        bad_colouring["five_colouring"][1] = bad_colouring["five_colouring"][0]
        controls.append(("improper_colouring", bad_colouring))

        bad_orbits = json.loads(json.dumps(original))
        bad_orbits["required_edge_orbits"].pop()
        controls.append(("missing_proof_orbit", bad_orbits))

        rejected = []
        for index, (name, data) in enumerate(controls):
            path = temp / f"bad-{index}.json"
            path.write_text(json.dumps(data))
            result = run(path)
            need(result.returncode != 0, f"control {name} was accepted")
            rejected.append(name)

    receipt = {
        "status": "VERIFIED_POSITIVE_REPLAY_AND_REJECTION_CONTROLS",
        "positive_replays": 1,
        "negative_controls_rejected": rejected,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
