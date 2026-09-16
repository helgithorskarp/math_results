#!/usr/bin/env python3
"""Reject representative corruptions of the compact certificate."""

import copy
import json
from pathlib import Path

from verify import audit


HERE = Path(__file__).resolve().parent


def rejected(certificate):
    try:
        audit(certificate)
    except (ValueError, KeyError):
        return True
    return False


def main():
    good = json.loads((HERE / "certificate.json").read_text())
    tests = []

    bad = copy.deepcopy(good)
    bad["threshold"] = 3
    tests.append(bad)

    bad = copy.deepcopy(good)
    bad["supports"][2]["edges"] += 1
    tests.append(bad)

    bad = copy.deepcopy(good)
    word = list(bad["source_input_decision"]["surviving_full_word"])
    word[0] = word[1]
    bad["source_input_decision"]["surviving_full_word"] = "".join(word)
    tests.append(bad)

    bad = copy.deepcopy(good)
    bad["mixed_depth_audit"]["a2_points_beyond_full_s2"] = 0
    tests.append(bad)

    if not all(rejected(test) for test in tests):
        raise RuntimeError("a corrupted certificate was accepted")
    print("CONTROLS_OK", len(tests))


if __name__ == "__main__":
    main()
