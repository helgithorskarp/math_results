#!/usr/bin/env python3
"""Reconstruct the host and verify its complete order-508 closure."""

import argparse
import hashlib
import json
from pathlib import Path

import geometry
import verify


HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    certificate_data = (HERE / "certificate.json").read_bytes()
    certificate = json.loads(certificate_data)
    geometry_result, edges = geometry.generate(args.output, certificate)
    result = verify.verify(certificate, edges)
    result["geometry"] = geometry_result
    result["certificate_sha256"] = hashlib.sha256(certificate_data).hexdigest()
    expected = json.loads((HERE / "expected.json").read_text())
    for key, value in expected.items():
        observed = result[key] if key in result else geometry_result[key]
        verify.require(observed == value, "expected result mismatch: " + key)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "verification.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
