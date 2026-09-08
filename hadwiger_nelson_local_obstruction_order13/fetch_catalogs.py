#!/usr/bin/env python3
"""Fetch and hash-check the external edge-5-critical graph catalogs."""
import argparse
import gzip
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE / "catalog_manifest.json").read_text())
    report = {}
    for order, row in manifest["catalogs"].items():
        target = args.output / row["download_name"]
        if not target.exists():
            temporary = target.with_suffix(target.suffix + ".tmp")
            require(not temporary.exists(), f"refusing stale temporary file {temporary}")
            try:
                with urllib.request.urlopen(row["url"], timeout=120) as response, temporary.open("wb") as out:
                    shutil.copyfileobj(response, out)
                temporary.replace(target)
            finally:
                temporary.unlink(missing_ok=True)
        require(target.stat().st_size == row["bytes"], f"size mismatch for {target.name}")
        require(digest(target) == row["sha256"], f"hash mismatch for {target.name}")
        plain = target
        if "uncompressed_name" in row:
            plain = args.output / row["uncompressed_name"]
            if not plain.exists():
                temporary = plain.with_suffix(plain.suffix + ".tmp")
                require(not temporary.exists(), f"refusing stale temporary file {temporary}")
                try:
                    with gzip.open(target, "rb") as source, temporary.open("wb") as out:
                        shutil.copyfileobj(source, out)
                    temporary.replace(plain)
                finally:
                    temporary.unlink(missing_ok=True)
            require(plain.stat().st_size == row["uncompressed_bytes"], "uncompressed size mismatch")
            require(digest(plain) == row["uncompressed_sha256"], "uncompressed hash mismatch")
        with plain.open("rb") as source:
            records = sum(1 for line in source if line.rstrip(b"\r\n"))
        require(records == row["records"], f"record-count mismatch for order {order}")
        report[order] = {"download": target.name, "records": records, "verified": True}
    print(json.dumps({"catalogs": report, "all_checks": True}, sort_keys=True))


if __name__ == "__main__":
    main()
