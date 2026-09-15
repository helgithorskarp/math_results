#!/usr/bin/env python3
"""Small rejection controls for the G15 lens certificate."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import verify

HERE = Path(__file__).resolve().parent


def rejected(cert):
    try:
        verify.verify_certificate(cert)
    except ValueError:
        return True
    return False


def main():
    cert = json.loads((HERE / "certificate.json").read_text())
    cases = []
    bad = copy.deepcopy(cert); bad["point_stream_sha256"] = "0" * 64; cases.append(bad)
    bad = copy.deepcopy(cert); bad["edge_stream_sha256"] = "0" * 64; cases.append(bad)
    bad = copy.deepcopy(cert); bad["collision_classes"] = []; cases.append(bad)
    bad = copy.deepcopy(cert); bad["four_colouring"] = "0" * cert["physical_vertices"]; cases.append(bad)
    if not all(rejected(case) for case in cases):
        raise ValueError("a malformed certificate was accepted")
    print(json.dumps({"controls": "PASS", "malformed_certificates_rejected": len(cases)}, sort_keys=True))


if __name__ == "__main__":
    main()
