"""Check a uniform 50-edit obstruction for the 537-unit orbit of a 536-colouring.

No SAT library or certificate generator is imported.  The two residual cases
are refuted by unit propagation on clauses built from the Schur definition.
"""

from __future__ import annotations

import json
import lzma
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLOURS = range(1, 7)
UNITS = [m for m in range(1, 537) if gcd(m, 537) == 1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def triples_ok(colour: list[int]) -> None:
    for x in range(1, 537):
        for y in range(x, 537 - x):
            require(colour[x] != colour[y] or colour[x] != colour[x + y],
                    f"bad 536-colouring at {(x, y, x + y)}")


def groups_for(colour: list[int], m: int, data: dict) -> tuple[dict, dict]:
    pairs = {c: [(x, 537 - x) for x in range(1, 269)
                 if colour[x] == colour[537 - x] == c] for c in COLOURS}
    require([len(pairs[c]) for c in COLOURS] == [64, 43, 55, 38, 32, 35],
            f"wrong complement-pair counts for {m}")
    require(set(data) == {"2", "4", "5", "6"}, f"wrong colour cases for {m}")
    groups = {}
    for c in (2, 4, 5, 6):
        selected = data[str(c)]
        require(isinstance(selected, list), f"invalid selection for {m},{c}")
        seen_pairs = set()
        used_support = set()
        groups[c] = [list(pair) for pair in pairs[c]]
        for entry in selected:
            require(isinstance(entry, list) and len(entry) == 2,
                    f"malformed pair entry for {m},{c}")
            x, coordinates = entry
            pair = (x, 537 - x)
            require(pair in pairs[c] and pair not in seen_pairs,
                    f"invalid or duplicate pair for {m},{c}: {pair}")
            seen_pairs.add(pair)
            require(isinstance(coordinates, list) and len(coordinates) == 20,
                    f"incomplete witnesses for {m},{c}: {pair}")
            support = set()
            index = 0
            for v in pair:
                for d in COLOURS:
                    if d == c:
                        continue
                    a, b = coordinates[index:index + 2]
                    index += 2
                    require(isinstance(a, int) and isinstance(b, int) and
                            1 <= a <= b and a + b <= 536,
                            f"invalid witness coordinates for {m},{c}")
                    witness = {a, b, a + b}
                    require(v in witness, f"missing endpoint for {m},{c}")
                    others = witness - {v}
                    require(others and all(colour[u] == d for u in others),
                            f"wrong support colour for {m},{c}")
                    support.update(others)
            require(not support & used_support,
                    f"overlapping supports for {m},{c}")
            used_support.update(support)
            groups[c].append(sorted(support))
        pair_vertices = {v for pair in pairs[c] for v in pair}
        require(not pair_vertices & used_support,
                f"pair/support overlap for {m},{c}")
        flat = [v for group in groups[c] for v in group]
        require(len(flat) == len(set(flat)), f"overlapping groups for {m},{c}")
    return pairs, groups


def unit_refutes_49(colour: list[int], groups: list[list[int]]) -> tuple[bool, int, int, int]:
    """Assume <=49 edits, 537 in colour 5; derive an empty clause."""
    require(len(groups) == 49, "the saturation case needs 49 groups")
    free = {v for group in groups for v in group}
    require(all(1 <= v <= 536 for v in free), "bad group member")
    extended = colour + [5]

    def var(v: int, d: int) -> int:
        return 6 * (v - 1) + d

    clauses: list[tuple[int, ...]] = []
    for v in sorted(free):
        clauses.append(tuple(var(v, d) for d in COLOURS))
        for d in COLOURS:
            for e in range(1, d):
                clauses.append((-var(v, d), -var(v, e)))
    for group in groups:
        clauses.append(tuple(-var(v, colour[v]) for v in group))
        for i, v in enumerate(group):
            for w in group[:i]:
                clauses.append((var(v, colour[v]), var(w, colour[w])))

    for x in range(1, 538):
        for y in range(x, 538 - x):  # includes x=y
            vertices = {x, y, x + y}
            fixed = vertices - free
            for d in COLOURS:
                if any(extended[v] != d for v in fixed):
                    continue
                clause = tuple(-var(v, d) for v in sorted(vertices & free))
                require(clause, f"fixed monochromatic triple {(x, y, x + y)}")
                clauses.append(clause)

    values: dict[int, bool] = {}
    rounds = 0
    while True:
        rounds += 1
        changes = 0
        for clause in clauses:
            unset = []
            for literal in clause:
                value = values.get(abs(literal))
                if value is None:
                    unset.append(literal)
                elif value == (literal > 0):
                    break
            else:
                if not unset:
                    return True, len(clauses), rounds, len(values)
                if len(unset) == 1:
                    literal = unset[0]
                    values[abs(literal)] = literal > 0
                    changes += 1
        if changes == 0:
            return False, len(clauses), rounds, len(values)


def main() -> None:
    encoded = (HERE / "baseline.txt").read_text(encoding="ascii").strip()
    require(len(encoded) == 536 and set(encoded) == set("123456"), "bad baseline")
    baseline = [0] + [int(d) for d in encoded]
    with lzma.open(HERE / "certificates.json.xz", "rt", encoding="utf-8") as stream:
        certificates = json.load(stream)
    require(set(certificates) == set(map(str, UNITS)), "missing or extra multipliers")
    exceptions = []
    worst = 537
    for m in UNITS:
        inverse = pow(m, -1, 537)
        colour = [0] + [baseline[(inverse * x) % 537] for x in range(1, 537)]
        triples_ok(colour)
        pairs, groups = groups_for(colour, m, certificates[str(m)])
        bounds = {c: len(groups[c]) for c in (2, 4, 5, 6)}
        bounds[1], bounds[3] = len(pairs[1]), len(pairs[3])
        if min(bounds.values()) < 50:
            require(min(bounds.values()) == 49 and bounds[5] == 49,
                    f"unsupported low bound for {m}")
            refuted, clauses, rounds, assigned = unit_refutes_49(colour, groups[5])
            require(refuted, f"49-edit case not refuted for {m}")
            exceptions.append((m, clauses, rounds, assigned))
            bounds[5] = 50
        require(min(bounds.values()) >= 50, f"weak bound for {m}")
        worst = min(worst, min(bounds.values()))
    print(f"PASS units={len(UNITS)} minimum_distance={worst} "
          f"unit_refutations={len(exceptions)}")
    for m, clauses, rounds, assigned in exceptions:
        print(f"multiplier={m} colour=5 clauses={clauses} "
              f"unit_rounds={rounds} assigned={assigned} UNSAT")


if __name__ == "__main__":
    main()
