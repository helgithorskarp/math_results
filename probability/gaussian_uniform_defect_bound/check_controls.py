#!/usr/bin/env python3
"""Damage the envelope premises separately; every case must be rejected."""

from copy import deepcopy
import json
from pathlib import Path
from verify import InvalidCertificate, audit, require


def main():
    original = json.loads(Path(__file__).with_name("CERTIFICATE.json").read_text())
    audit(original)
    controls = []

    data = deepcopy(original)
    data["error"] = "6/50"
    controls.append(("incorrect infinite-end error", data, "envelope parameters"))

    data = deepcopy(original)
    data["critical_bracket"] = ["4/5", "81/100"]
    controls.append(("missed critical point", data, "critical root isolation"))

    # This nearby shift has a genuinely positive critical maximum.
    data = deepcopy(original)
    data["shift"] = "1/3"
    data["critical_bracket"] = ["84375/100000", "84376/100000"]
    data["claims"]["d_zero"] = ["-7/50", "0"]
    data["claims"]["critical_value"] = ["-1", "1"]
    controls.append(("nearby false global upper envelope", data,
                     "positive-side upper envelope"))

    data = deepcopy(original)
    data["claims"]["d_zero"] = ["-1/10", "0"]
    controls.append(("incorrect finite-end enclosure", data, "d(0) enclosure claim"))

    for name, data, expected in controls:
        try:
            audit(data)
        except InvalidCertificate as exc:
            require(str(exc) == expected, name + ": wrong rejection boundary")
        else:
            raise InvalidCertificate(name + ": false certificate accepted")
    print(json.dumps({"status": "ENVELOPE_DAMAGE_CONTROLS_PASS",
                      "rejected": [row[0] for row in controls]}, indent=2))


if __name__ == "__main__":
    main()
