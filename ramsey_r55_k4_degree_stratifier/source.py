"""Hash-locked access to the physical K4 formula and structural sources."""
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib
import json
import sys

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def verify(row):
    path = HERE.parent / row["directory"]
    raw = (path / "SHA256SUMS").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == row["manifest_sha256"],
            "dependency manifest " + row["directory"])
    lines = raw.decode().splitlines()
    require(len(lines) == row["manifest_entries"],
            "dependency cardinality " + row["directory"])
    for line in lines:
        wanted, name = line.split("  ", 1)
        require(hashlib.sha256((path / name).read_bytes()).hexdigest() == wanted,
                "changed dependency " + row["directory"] + "/" + name)
    return path


@lru_cache(maxsize=None)
def load():
    rows = json.loads((HERE / "DEPENDENCIES.json").read_text())
    paths = {row["directory"]: verify(row) for row in rows}
    package = paths["ramsey_r55_k4_expansion_interface"]
    sys.path.insert(0, str(package))
    expansion = importlib.import_module("augment")
    interface = importlib.import_module("interface")
    require(Path(expansion.__file__).resolve().parent == package.resolve(),
            "wrong K4 expansion module")
    require(Path(interface.__file__).resolve().parent == package.resolve(),
            "wrong K4 interface module")
    return {"expansion": expansion, "interface": interface, "paths": paths}
