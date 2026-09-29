#!/usr/bin/env python3
"""Reject corrupted proofs at the exact trust boundaries used by the theorem."""

import copy
import json
from pathlib import Path

from verify import verify


def main():
    data = json.loads(Path(__file__).with_name("certificate.json").read_text())
    if not verify(data)["verified"]:
        raise ValueError("Positive control failed")
    bad = []
    truncated = copy.deepcopy(data)
    truncated["records"].pop()
    bad.append(("incomplete_coverage", truncated))
    overlapping = copy.deepcopy(data)
    if len(overlapping["records"][0][1]) != data["radius"]:
        raise ValueError("First record must be an initial packing")
    overlapping["records"][0][1][1] = overlapping["records"][0][1][0]
    bad.append(("overlapping_petals", overlapping))
    invalid = copy.deepcopy(data)
    invalid["records"][0][1][0][0] = -1
    bad.append(("invalid_progression", invalid))
    missing_color = copy.deepcopy(data)
    missing_color["extension_obstructions"].pop()
    bad.append(("unblocked_endpoint_color", missing_color))
    exaggerated = copy.deepcopy(data)
    exaggerated["radius"] += 1
    bad.append(("unsupported_radius", exaggerated))
    duplicate = copy.deepcopy(data)
    duplicate["records"].insert(1, duplicate["records"][0])
    bad.append(("duplicate_elimination", duplicate))
    for label, certificate in bad:
        try:
            verify(certificate)
        except ValueError:
            continue
        raise ValueError(f"Corrupted proof accepted: {label}")
    print(json.dumps({"positive_control": True, "rejected_corruptions": [label for label, _ in bad]}, sort_keys=True))


if __name__ == "__main__":
    main()
