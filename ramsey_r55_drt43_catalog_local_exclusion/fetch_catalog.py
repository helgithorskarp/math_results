#!/usr/bin/env python3
"""Fetch the pinned McKay DRT(43) partial catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    metadata = json.loads((Path(__file__).parent / "PROVENANCE.json").read_text())
    data = urllib.request.urlopen(metadata["catalog_url"], timeout=60).read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != metadata["catalog_sha256"]:
        raise RuntimeError(f"catalog SHA-256 mismatch: {digest}")
    args.output.write_bytes(data)
    print(f"FETCHED {len(data)} bytes sha256 {digest}")


if __name__ == "__main__":
    main()
