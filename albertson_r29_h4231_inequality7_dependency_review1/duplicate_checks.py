#!/usr/bin/env python3
"""Correct h4231's two repeated-block aliases and measure their effect."""

import hashlib
from pathlib import Path
import sys
import types


EXPECTED_SHA256 = "9cb7ae56e49ea66eee6a837ee6bb71a040733edf7ac9e2841cbba70f4bc8c1f0"

OLD_CAP = """                                lb = (max(0, qi - a) * min(rh, u)
                                      + sum(q * min(max(0, q + RSZ - 29), u)
                                            for q in mult if q != qi))
"""
NEW_CAP = """                                lb = (sum(q * min(max(0, q + RSZ - 29), u)
                                          for q in mult)
                                      - a * min(rh, u))
"""

OLD_REM = """    need, red, take_of = 3 * k, [], {}
    for rho, q, av in cells:
        take = min(need, k, av)
        red.append((rho, q - take))
        take_of[(rho, q)] = take
        need -= take
    if need > 0:
        return True                      # k disjoint triangles unavailable
    cells = red
    rem = [take_of.get((max(0, q + RSZ - 29), q), 0) for q in mult]
"""
NEW_REM = """    need, red, take_of = 3 * k, [], {}
    for rho, q, av in cells:
        take = min(need, k, av)
        red.append((rho, q - take))
        take_of.setdefault((rho, q), []).append(take)
        need -= take
    if need > 0:
        return True                      # k disjoint triangles unavailable
    cells = red
    remaining_take = {key: list(values) for key, values in take_of.items()}
    rem = []
    for q in mult:
        key = (max(0, q + RSZ - 29), q)
        rem.append(remaining_take[key].pop())
"""


def load(name, path, source):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


def replace_once(source, old, new, label):
    if source.count(old) != 1:
        raise RuntimeError(f"expected exactly one {label} source block")
    return source.replace(old, new)


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: duplicate_checks.py /path/to/source/directory")
    directory = Path(argv[1]).resolve()
    path = directory / "tuttegen.py"
    payload = path.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("unexpected tuttegen.py SHA-256: " + digest)
    source = payload.decode("utf-8")
    sys.path.insert(0, str(directory))

    claimed = load("h4231_claimed_duplicates", path, source)
    cap_fixed = load("h4231_cap_fixed", path,
                     replace_once(source, OLD_CAP, NEW_CAP, "cap"))
    rem_fixed = load("h4231_rem_fixed", path,
                     replace_once(source, OLD_REM, NEW_REM, "rem"))
    both_source = replace_once(source, OLD_CAP, NEW_CAP, "cap")
    both_source = replace_once(both_source, OLD_REM, NEW_REM, "rem")
    both_fixed = load("h4231_both_fixed", path, both_source)

    rows = claimed.configurations()
    candidates = [row for row in rows if len(set(row[2])) < len(row[2])]
    partition_candidates = [
        row for row in candidates if sum(row[2]) == claimed.N58 - row[1]
    ]
    changed_cap = []
    changed_rem = []
    changed_both = []
    claimed_closed = 0
    for row in candidates:
        m, r_size, mult, e_hr = row
        excess = 2 * m - claimed.N58 * claimed.DEG
        old = claimed.route_closed(r_size, list(mult), e_hr, excess)
        if not old[0]:
            continue
        claimed_closed += 1
        cap = cap_fixed.route_closed(r_size, list(mult), e_hr, excess)
        rem = rem_fixed.route_closed(r_size, list(mult), e_hr, excess)
        both = both_fixed.route_closed(r_size, list(mult), e_hr, excess)
        if not cap[0]:
            changed_cap.append((row, old, cap))
        if not rem[0]:
            changed_rem.append((row, old, rem))
        if not both[0]:
            changed_both.append((row, old, both))

    print("target tuttegen.py sha256:", digest)
    print("all configurations:", len(rows))
    print("repeated-block candidates:", len(candidates))
    print("partition candidates with repeated blocks:", len(partition_candidates))
    print("claimed closures among candidates:", claimed_closed)
    print("closures lost with exact repeated-block cap:", len(changed_cap))
    print("closures lost with indexed triangle removals:", len(changed_rem))
    print("closures lost with both corrections:", len(changed_both))


if __name__ == "__main__":
    main(sys.argv)
