"""Hash-locked loader for the ordered family and separator theorem."""
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib
import json
import sys

HERE = Path(__file__).resolve().parent


def verify_package(row):
    path = HERE.parent / row["directory"]
    manifest = path / "SHA256SUMS"
    raw = manifest.read_bytes()
    if hashlib.sha256(raw).hexdigest() != row["manifest_sha256"]:
        raise ValueError("dependency manifest " + row["directory"])
    lines = raw.decode().splitlines()
    if len(lines) != row["manifest_entries"]:
        raise ValueError("dependency entry count " + row["directory"])
    for line in lines:
        digest, name = line.split("  ", 1)
        if hashlib.sha256((path / name).read_bytes()).hexdigest() != digest:
            raise ValueError("changed dependency " + row["directory"] + "/" + name)
    return path


@lru_cache(maxsize=None)
def load():
    rows = json.loads((HERE / "DEPENDENCIES.json").read_text())
    paths = {row["directory"]: verify_package(row) for row in rows}
    ordered_path = paths["ramsey_r55_maximal_block_order"]
    sys.path.insert(0, str(ordered_path))
    ordered = importlib.import_module("ordered")
    check_order = importlib.import_module("check_order")
    if Path(ordered.__file__).resolve().parent != ordered_path.resolve():
        raise ValueError("wrong ordered module")
    if Path(check_order.__file__).resolve().parent != ordered_path.resolve():
        raise ValueError("wrong ordered audit module")
    return {"ordered": ordered, "check_order": check_order, "paths": paths}
