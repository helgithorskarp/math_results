"""Standard-library checker for a 52-edit obstruction at S(6).

The earlier certificate supplies 51 disjoint mandatory edit groups. At a
putative distance of at most 51, each group has exactly one edit and all other
positions are fixed. Unit propagation refutes each remaining colour of 537.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLORS = range(1, 7)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def certificate_groups() -> tuple[list[int], dict[int, list[tuple[int, int]]],
                                  dict[int, list[list[int]]]]:
    encoded = (HERE / "baseline.txt").read_text(encoding="ascii").strip()
    require(len(encoded) == 536 and set(encoded) == set("123456"), "bad baseline")
    baseline = [0] + [int(d) for d in encoded]
    for x in range(1, 537):
        for y in range(x, 537 - x):
            require(len({baseline[x], baseline[y], baseline[x + y]}) > 1,
                    f"invalid baseline triple {(x, y, x + y)}")

    data = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))
    require(data["target"] == 537, "wrong certificate target")
    require(set(data["selected_by_color"]) == {str(c) for c in COLORS},
            "missing colour case")
    pairs = {c: [(x, 537 - x) for x in range(1, 269)
                 if baseline[x] == baseline[537 - x] == c] for c in COLORS}
    supports: dict[int, list[list[int]]] = {}
    for c in COLORS:
        seen_pairs: set[tuple[int, int]] = set()
        seen_support: set[int] = set()
        supports[c] = []
        for entry in data["selected_by_color"][str(c)]:
            pair = tuple(entry["pair"])
            require(pair in pairs[c] and pair not in seen_pairs,
                    f"invalid selected pair for colour {c}")
            seen_pairs.add(pair)
            covered: set[tuple[int, int]] = set()
            support: set[int] = set()
            for witness in entry["witnesses"]:
                v, d = witness["endpoint"], witness["new_color"]
                x, y, z = witness["triple"]
                require(v in pair and d in COLORS and d != c and
                        (v, d) not in covered and 1 <= x <= y and
                        x + y == z <= 536 and v in (x, y, z),
                        f"invalid witness for colour {c}")
                covered.add((v, d))
                other = {x, y, z} - {v}
                require(other and all(baseline[s] == d for s in other),
                        f"invalid witness support for colour {c}")
                support.update(other)
            require(covered == {(v, d) for v in pair for d in COLORS if d != c},
                    f"incomplete witnesses for colour {c}")
            require(not support & seen_support, "overlapping support groups")
            seen_support.update(support)
            supports[c].append(sorted(support))
        pair_vertices = {v for pair in pairs[c] for v in pair}
        require(not pair_vertices & seen_support, "pair/support overlap")
    return baseline, pairs, supports


def reduced_clauses(baseline: list[int], c: int,
                    pairs: list[tuple[int, int]],
                    supports: list[list[int]]) -> tuple[list[list[int]], int]:
    # Each pair and support group needs an edit. With 51 edits available,
    # every group has exactly one and every position outside them is fixed.
    groups = [list(pair) for pair in pairs] + supports
    require(len(groups) == 51, f"colour {c} has no 51-group certificate")
    free = {v for group in groups for v in group}
    require(sum(map(len, groups)) == len(free), "mandatory groups overlap")
    colour = baseline + [c]  # fixed colour of 537

    def variable(v: int, d: int) -> int:
        return (v - 1) * 6 + d

    clauses: list[list[int]] = []
    for v in sorted(free):
        clauses.append([variable(v, d) for d in COLORS])
        for d in COLORS:
            for e in range(1, d):
                clauses.append([-variable(v, d), -variable(v, e)])
    for group in groups:
        clauses.append([-variable(v, baseline[v]) for v in group])
        for i, v in enumerate(group):
            for w in group[:i]:
                clauses.append([variable(v, baseline[v]),
                                variable(w, baseline[w])])

    # Substitute fixed colours directly into the definition-level clauses.
    # A repeated summand has just two distinct positions in its clause.
    for x in range(1, 538):
        for y in range(x, 538 - x):
            vertices = {x, y, x + y}
            fixed = vertices - free
            for d in COLORS:
                if any(colour[v] != d for v in fixed):
                    continue
                clause = sorted(-variable(v, d) for v in vertices & free)
                require(clause, f"fixed monochromatic triple {(x, y, x + y)}")
                clauses.append(clause)
    return clauses, len(free)


def unit_refutes(clauses: list[list[int]]) -> tuple[bool, int, int]:
    """Repeated full scans implement unit propagation without a SAT library."""
    assignment: dict[int, bool] = {}
    rounds = 0
    while True:
        rounds += 1
        changes = 0
        for clause in clauses:
            unassigned: list[int] = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    unassigned.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unassigned:
                return True, rounds, len(assignment)
            if len(unassigned) == 1:
                literal = unassigned[0]
                assignment[abs(literal)] = literal > 0
                changes += 1
        if changes == 0:
            return False, rounds, len(assignment)


def main() -> None:
    baseline, pairs, supports = certificate_groups()
    bounds = {c: len(pairs[c]) + len(supports[c]) for c in COLORS}
    require(bounds == {1: 64, 2: 51, 3: 55, 4: 51, 5: 51, 6: 51},
            "unexpected first-stage distance bounds")
    for c in (2, 4, 5, 6):
        clauses, free = reduced_clauses(baseline, c, pairs[c], supports[c])
        refuted, rounds, assigned = unit_refutes(clauses)
        require(refuted, f"unit propagation did not refute colour {c}")
        print(f"colour={c} groups=51 free={free} clauses={len(clauses)} "
              f"unit_rounds={rounds} assigned={assigned} UNSAT")
    print("PASS distance_at_least=52")


if __name__ == "__main__":
    main()
