#!/usr/bin/env python3
"""Audit the pinned input and committed full-run transcript."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    if args.catalog is None:
        temporary = tempfile.TemporaryDirectory(prefix="drt43-catalog-")
        catalog = Path(temporary.name) / "drtourn43some.txt"
        subprocess.run(["python3", "-B", str(package / "fetch_catalog.py"), str(catalog)], check=True)
    else:
        temporary = None
        catalog = args.catalog
    subprocess.run(
        ["python3", "-B", str(package / "audit.py"), "--catalog", str(catalog),
         "--result", str(package / "RESULT.tsv")],
        check=True,
    )
    if temporary is not None:
        temporary.cleanup()
    print("REPRODUCED_DRT43_PARTIAL_CATALOG_LOCAL_EXCLUSION_AUDIT")


if __name__ == "__main__":
    main()
