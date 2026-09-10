#!/usr/bin/env python3
"""Measure h4231's exact dependence on its inequality-(7) rejection.

Usage:
    python3 ablation.py /path/to/h4231/source/directory

The directory must contain tuttegen.py and sibling modules from source commit
06bce6c2c5c0c64ca19cb82b00483a4d6fafb1af.  The scan is deterministic,
single-process, and uses exact Python integers.
"""

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import types


EXPECTED_SHA256 = "9cb7ae56e49ea66eee6a837ee6bb71a040733edf7ac9e2841cbba70f4bc8c1f0"
NEEDLE = """    if (cA - iso) * max(0, rhoA - sR) > W:                          # (7)
        return False
"""
REPLACEMENT = """    # Inequality (7) ablated by the independent review.
    if False and (cA - iso) * max(0, rhoA - sR) > W:                # (7)
        return False
"""


def load_claimed(path):
    spec = importlib.util.spec_from_file_location("h4231_claimed", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot construct module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_relaxed(path, source):
    if source.count(NEEDLE) != 1:
        raise RuntimeError("expected exactly one inequality-(7) source block")
    module = types.ModuleType("h4231_relaxed")
    module.__file__ = str(path)
    exec(compile(source.replace(NEEDLE, REPLACEMENT), str(path), "exec"),
         module.__dict__)
    return module


def canonical_hash(rows):
    payload = json.dumps(rows, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: python3 ablation.py /path/to/h4231/source/directory")
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

    by_m = Counter(row[0] for row in changed)
    by_r = Counter(row[1] for row in changed)
    canonical = [list(row[:2]) + [list(row[2])] + list(row[3:]) for row in changed]
    print("target tuttegen.py sha256:", digest)
    print("configurations scanned:", len(rows))
    print("claimed closures:", claimed_closed)
    print("closures after inequality-(7) ablation:", relaxed_closed)
    print("closures lost:", len(changed))
    print("frontier lower bound after ablation:", len(rows) - relaxed_closed + 15 + 307)
    print("lost by m:", sorted(by_m.items()))
    print("lost by |R|:", sorted(by_r.items()))
    print("canonical lost-row sha256:", canonical_hash(canonical))
    print("first lost row:", changed[0])
    print("last lost row:", changed[-1])


if __name__ == "__main__":
    main(sys.argv)
