#!/usr/bin/env python3
"""Check public source lengths/digests only; this is not a proof checker."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text())
    assert manifest["manifest_bytes_excluded"] is True
    assert manifest["full_target_solved"] is False
    for row in manifest["files"]:
        relative = Path(row["path"])
        assert not relative.is_absolute() and ".." not in relative.parts
        data = (root / relative).read_bytes()
        assert len(data) == row["bytes"], row["path"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
    assert len(manifest["files"]) == manifest["total_named_files"]
    assert sum(row["bytes"] for row in manifest["files"]) == manifest["total_named_bytes"]
    print(f"PASS: {len(manifest['files'])} named source files match the manifest.")


if __name__ == "__main__":
    main()
