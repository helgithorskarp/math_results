#!/usr/bin/env python3
"""Small negative controls for the separating-basis verifier."""

import json
import tempfile
from pathlib import Path

import verify


def rejected(certificate):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "certificate.json"
        path.write_text(json.dumps(certificate) + "\n")
        try:
            verify.verify(path)
        except (ValueError, KeyError, TypeError):
            return True
    return False


def main():
    source = json.loads((verify.HERE / "certificate.json").read_text())
    bad = json.loads(json.dumps(source))
    bad["schema"] = "wrong"
    assert rejected(bad)
    bad = json.loads(json.dumps(source))
    bad["heptagon_moser"]["colourings"] = ["0" * 143]
    assert rejected(bad)
    bad = json.loads(json.dumps(source))
    bad["golomb_rotation"]["cases"] = bad["golomb_rotation"]["cases"][:-1]
    assert rejected(bad)
    bad = json.loads(json.dumps(source))
    bad["golomb_rotation"]["cases"][0]["colourings"][0] = "x" * 100
    assert rejected(bad)
    print(json.dumps({"malformed_controls_rejected": 4, "status": "PASS"}, sort_keys=True))


if __name__ == "__main__":
    main()
