#!/usr/bin/env python3
"""Independent domain-propagation audit of the 52-edit S(6) obstruction."""

import hashlib
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parent.parent / "schur_s6_fredricksen_sweet_distance"
ALL = (1 << 6) - 1


class Contradiction(Exception):
    """A logically forced empty domain or monochromatic constraint."""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def bit(colour):
    return 1 << (colour - 1)


def groups_for(base, rows, colour):
    pairs = [(x, 537 - x) for x in range(1, 269)
             if base[x] == base[537 - x] == colour]
    pair_set = set(pairs)
    used = {x for pair in pairs for x in pair}
    supports = []
    selected = set()
    witnesses = 0
    for row in rows:
        pair = tuple(row["pair"])
        require(pair in pair_set and pair not in selected,
                "selected pair missing or repeated")
        selected.add(pair)
        coverage = set()
        support = set()
        for witness in row["witnesses"]:
            v, d = witness["endpoint"], witness["new_color"]
            x, y, z = witness["triple"]
            require(v in pair and d in range(1, 7) and d != colour and
                    (v, d) not in coverage and 1 <= x <= y and x + y == z <= 536 and
                    v in (x, y, z), "invalid witness")
            others = {x, y, z} - {v}
            require(others and all(base[u] == d for u in others),
                    "witness does not force a support edit")
            coverage.add((v, d))
            support.update(others)
            witnesses += 1
        require(coverage == {(v, d) for v in pair
                             for d in range(1, 7) if d != colour},
                "incomplete endpoint/colour coverage")
        require(not support & used, "mandatory edit groups overlap")
        used.update(support)
        supports.append(tuple(sorted(support)))
    groups = [tuple(pair) for pair in pairs] + supports
    require(len(used) == sum(map(len, groups)), "groups are not disjoint")
    return groups, used, witnesses


def schur_edges():
    # Distinct supports handle x=y as a two-vertex edge.
    edges = []
    for x in range(1, 269):
        for y in range(x, 538 - x):
            edges.append(tuple(sorted({x, y, x + y})))
    require(len(edges) == 72092, "Schur triple count changed")
    return edges


def propagate(base, colour, groups, free, edges):
    domains = [0] + [ALL if v in free else bit(base[v]) for v in range(1, 537)]
    domains.append(bit(colour))
    rounds = deductions = 0

    def narrow(v, allowed):
        nonlocal deductions
        new = domains[v] & allowed
        if not new:
            raise Contradiction(f"empty colour domain at {v}")
        if new != domains[v]:
            domains[v] = new
            deductions += 1
            return True
        return False

    try:
        while True:
            rounds += 1
            start = deductions
            for group in groups:
                edited = [v for v in group if not domains[v] & bit(base[v])]
                unchanged = [v for v in group if domains[v] == bit(base[v])]
                if len(edited) > 1 or len(unchanged) == len(group):
                    raise Contradiction("mandatory group contradiction")
                if edited:
                    for v in group:
                        if v != edited[0]:
                            narrow(v, bit(base[v]))
                elif len(unchanged) == len(group) - 1:
                    remaining = next(v for v in group if v not in unchanged)
                    narrow(remaining, ALL ^ bit(base[remaining]))
            for edge in edges:
                for c in range(1, 7):
                    mask = bit(c)
                    if any(not domains[v] & mask for v in edge):
                        continue
                    uncertain = [v for v in edge if domains[v] != mask]
                    if not uncertain:
                        raise Contradiction(f"monochromatic Schur edge {edge}")
                    if len(uncertain) == 1:
                        narrow(uncertain[0], ALL ^ mask)
            if deductions == start:
                return False, rounds, deductions, "fixed point"
    except Contradiction as exc:
        return True, rounds, deductions, str(exc)


def main():
    raw = (SOURCE / "baseline.txt").read_bytes()
    digits = raw.decode("ascii").strip()
    require(len(digits) == 536 and set(digits) == set("123456"),
            "invalid baseline")
    base = [0] + list(map(int, digits))
    for x in range(1, 269):
        for y in range(x, 537 - x):
            require(not (base[x] == base[y] == base[x + y]),
                    "baseline is not sum-free")
    data = json.loads((SOURCE / "certificate.json").read_text())
    require(data["target"] == 537, "wrong certificate target")
    edges = schur_edges()
    counts = []
    total_witnesses = 0
    for colour in range(1, 7):
        groups, free, witnesses = groups_for(
            base, data["selected_by_color"][str(colour)], colour)
        counts.append(len(groups))
        total_witnesses += witnesses
        if colour in (1, 3):
            require(len(groups) > 51, "counting exclusion lost")
            continue
        require(len(groups) == 51, "wrong saturation case")
        refuted, rounds, deductions, reason = propagate(
            base, colour, groups, free, edges)
        require(refuted, f"case {colour} was not refuted")
        print(f"colour={colour} groups={len(groups)} free={len(free)} "
              f"rounds={rounds} domain_reductions={deductions} {reason}")
    require(counts == [64, 51, 55, 51, 51, 51] and total_witnesses == 560,
            "first-stage certificate mismatch")
    print("PASS independent_distance_at_least=52", "baseline_sha256=" +
          hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
