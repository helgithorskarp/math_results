#!/usr/bin/env python3
"""Generate the compact exact certificate."""

import argparse
import json
from pathlib import Path

from model import build_certificate


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    if a.out.exists():
        raise ValueError("output path already exists")
    cert = build_certificate()
    a.out.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(a.out), "status": cert["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
