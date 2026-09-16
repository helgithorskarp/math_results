#!/usr/bin/env python3
"""Certificate corruption controls for the UD9-3 closure checker."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile

from verify import CERTIFICATE, verify


def rejected(certificate, label):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "bad.json"
        path.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
        try:
            verify(path, check_expected=False)
        except (ValueError, KeyError, TypeError, ZeroDivisionError):
            return
        raise AssertionError(f"corruption accepted: {label}")


def main():
    valid = json.loads(CERTIFICATE.read_text())
    verify(CERTIFICATE, check_expected=True)

    bad = copy.deepcopy(valid)
    bad["schema"] = "wrong"
    rejected(bad, "schema")

    bad = copy.deepcopy(valid)
    bad["midpoint_numerators"].pop()
    rejected(bad, "midpoint dimension")

    bad = copy.deepcopy(valid)
    bad["four_colour_word"] = "9" + bad["four_colour_word"][1:]
    rejected(bad, "colour alphabet")

    print(json.dumps({
        "all_controls_passed": True,
        "valid_certificate_replayed": True,
        "corruptions_rejected": 3,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
