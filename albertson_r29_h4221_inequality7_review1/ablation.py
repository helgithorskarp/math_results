#!/usr/bin/env python3
"""Ablate only inequality (7) in the h4221 source and compare closures.

Usage:
    python3 ablation.py /path/to/h4221/source/directory

The directory must contain tuttegen.py and its sibling modules from source
commit 686a21d81a670928d51ccc61e3d64e7d54661e6f.  The run is deterministic and
uses exact Python integers.  It can take several minutes.
"""

import hashlib
import importlib.util
from pathlib import Path
import sys
import types


EXPECTED_SHA256 = "3b453e61b414549bae75fb95fec91a60ec5a16dde55183b87c6dbd7798630a4a"
NEEDLE = """    if (cA - iso) * max(0, rhoA - sR) > W:                          # (7)
        return False
"""
REPLACEMENT = """    # Inequality (7) ablated by the independent review.
    if False and (cA - iso) * max(0, rhoA - sR) > W:                # (7)
        return False
"""


def load_claimed(path):
    spec = importlib.util.spec_from_file_location("h4221_claimed", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot construct module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_relaxed(path, source):
    if source.count(NEEDLE) != 1:
        raise RuntimeError("expected exactly one inequality-(7) source block")
    module = types.ModuleType("h4221_relaxed")
    module.__file__ = str(path)
    exec(compile(source.replace(NEEDLE, REPLACEMENT), str(path), "exec"), module.__dict__)
    return module


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: python3 ablation.py /path/to/h4221/source/directory")
    directory = Path(argv[1]).resolve()
    path = directory / "tuttegen.py"
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("unexpected tuttegen.py SHA-256: " + digest)
    source = payload.decode("utf-8")
    sys.path.insert(0, str(directory))
    claimed = load_claimed(path)
    relaxed = load_relaxed(path, source)

    rows = claimed.configurations()
    claimed_closed = 0
    relaxed_closed = 0
    changed = []
    for m, r_size, mult, e_hr in rows:
        excess = 2 * m - claimed.N58 * claimed.DEG
        old_closed, old_reason = claimed.route_closed(r_size, list(mult), e_hr, excess)
        if not old_closed:
            continue
        claimed_closed += 1
        new_closed, new_reason = relaxed.route_closed(r_size, list(mult), e_hr, excess)
        if new_closed:
            relaxed_closed += 1
        else:
            changed.append((m, r_size, mult, e_hr, old_reason, new_reason))

    print("target tuttegen.py sha256:", digest)
    print("configurations scanned:", len(rows))
    print("claimed closures:", claimed_closed)
    print("closures after ablation:", relaxed_closed)
    print("closures lost:", len(changed))
    for row in changed:
        print(row)


if __name__ == "__main__":
    main(sys.argv)
