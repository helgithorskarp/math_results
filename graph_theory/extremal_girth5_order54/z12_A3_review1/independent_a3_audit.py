#!/usr/bin/env python3
"""Clean-room certificate, profile, four-set, and frame audit for z=12, A=3."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


PROFILES = (
    (2, 0, "six1", ((6, 1, 1), (6, 2, 5), (6, 3, 8), (6, 4, 2), (7, 1, 3), (7, 2, 23))),
    (2, 0, "threefour", ((6, 2, 8), (6, 3, 5), (6, 4, 3), (7, 1, 3), (7, 2, 23))),
    (2, 0, "sev0", ((6, 2, 7), (6, 3, 7), (6, 4, 2), (7, 0, 1), (7, 1, 1), (7, 2, 24))),
    (2, 0, "sev3", ((6, 2, 7), (6, 3, 7), (6, 4, 2), (7, 1, 4), (7, 2, 21), (7, 3, 1))),
    (2, 1, "P3", ((6, 2, 7), (6, 3, 7), (6, 4, 2), (7, 1, 3), (7, 2, 23))),
    (3, 0, "3P2", ((6, 2, 5), (6, 3, 9), (6, 4, 2), (7, 1, 7), (7, 2, 19))),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def compositions(total, length):
    """Lexicographic weak compositions via a Cartesian prefix scan."""
    for prefix in product(range(total + 1), repeat=length - 1):
        last = total - sum(prefix)
        if last >= 0:
            yield prefix + (last,)


def add(rows, rhs, row, value):
    rows.append({column: coefficient for column, coefficient in row.items() if coefficient})
    rhs.append(value)


def finish_type_edges(types):
    edges = tuple(
        (i, j)
        for i, (_, ni) in enumerate(types)
        for j in range(i, len(types))
        if ni[types[j][0]] and types[j][1][types[i][0]]
    )
    return edges


def degree_model(shared):
    sizes = (16, 26, 12)
    degrees = (6, 7, 8)
    types = []
    for cls, degree in enumerate(degrees):
        for ns in compositions(degree, 3):
            if sum(d * n for d, n in zip(degrees, ns)) > 53:
                continue
            if any(ns[a] > sizes[a] - int(a == cls) for a in range(3)):
                continue
            types.append((cls, ns))
    require(len(types) == 72, "wrong uncolored type count")
    edges = finish_type_edges(types)
    require(len(edges) == 1638, "wrong uncolored edge count")
    eq, eb, ub, bb = [], [], [], []
    for cls in range(3):
        add(eq, eb, {i: int(cl == cls) for i, (cl, _) in enumerate(types)}, sizes[cls])
    for a, b in combinations(range(3), 2):
        add(eq, eb, {i: int(cl == a) * ns[b] - int(cl == b) * ns[a]
                     for i, (cl, ns) in enumerate(types)}, 0)
    for a in range(3):
        add(ub, bb, {i: ns[a] * (ns[a] - 1) + int(cl == a) * ns[a]
                     for i, (cl, ns) in enumerate(types)}, sizes[a] * (sizes[a] - 1))
    for a, b in combinations(range(3), 2):
        add(ub, bb, {i: ns[a] * ns[b] + int(cl == a) * ns[b]
                     for i, (cl, ns) in enumerate(types)}, sizes[a] * sizes[b])
    balance = {}
    ball = {}
    for i, (cls, ns) in enumerate(types):
        for a in range(3):
            balance[i, a] = len(eq)
            add(eq, eb, {i: -ns[a]}, 0)
            ball[i, a] = len(ub)
            add(ub, bb, {i: ns[a] - sizes[a] - (degrees[cls] - 1) * int(cls == a)}, 0)
    for column, (i, j) in enumerate(edges, len(types)):
        directions = ((i, j),) if i == j else ((i, j), (j, i))
        for root, neighbor in directions:
            cls, ns = types[neighbor]
            eq[balance[root, cls]][column] = 1
            for a in range(3):
                ub[ball[root, a]][column] = ns[a]
    if shared:
        for degree, c, count in PROFILES[0][3]:
            add(eq, eb, {i: 1 for i, (cls, ns) in enumerate(types)
                         if degrees[cls] == degree and ns[2] == c}, count)
        for h, count in enumerate((8, 4, 0)):
            add(eq, eb, {i: 1 for i, (cls, ns) in enumerate(types)
                         if degrees[cls] == 8 and ns[2] == h}, count)
    add(eq, eb, {i: 5 - ns[1] - 2 * ns[2]
                 for i, (cls, ns) in enumerate(types) if degrees[cls] == 8}, 3)
    if shared:
        add(ub, bb, {i: ns[2] * (5 - ns[1] - 2 * ns[2])
                     for i, (cls, ns) in enumerate(types) if degrees[cls] == 8}, 2)
        for i, (cls, ns) in enumerate(types):
            degree = degrees[cls]
            s = ns[1] + 2 * ns[2]
            if (degree == 8 and s not in (4, 5)) or (
                degree == 7 and ((ns[2] == 1 and s == 8) or (ns[2] == 2 and s == 9))
            ):
                add(ub, bb, {i: 1}, 0)
    objective = [Fraction(ns[2], 2) if not shared and degrees[cls] == 8 else Fraction(0)
                 for cls, ns in types] + [Fraction(0)] * len(edges)
    return types, edges, eq, eb, ub, bb, objective


def colored_model(p, profile, m, k):
    sizes = tuple([13 + p, 26 - p, 9, 3, 3 - p] + ([p] if p else []))
    degrees = tuple([6, 7, 8, 8, 6] + ([7] if p else []))
    nc = len(sizes)
    types = []
    profile_pairs = {(degree, c) for degree, c, _ in profile}
    for cls, degree in enumerate(degrees):
        for ns in compositions(degree, nc):
            if any(ns[a] > sizes[a] - int(a == cls) for a in range(nc)):
                continue
            weighted = sum(degrees[a] * ns[a] for a in range(nc))
            high = ns[2] + ns[3]
            endpoints = sum(ns[4:])
            if weighted > 53 or (degree == 8 and high > 2):
                continue
            if cls == 2:
                valid = weighted == 53 and endpoints == 0 and ns[3] <= 1
            elif cls == 3:
                valid = weighted == 52 and endpoints == 2 and ns[3] == 0
            elif cls >= 4:
                valid = ns[3] == 2 and ns[2] == 0 and endpoints == 0
            else:
                valid = ns[3] <= 1 and endpoints <= 1
            if not valid:
                continue
            if cls not in (2, 3):
                if (degree, high) not in profile_pairs:
                    continue
                epsilon = weighted - 6 * degree - (8 if degree == 6 else 7)
                if degree == 7 and high == 2 and epsilon == 2:
                    continue
            types.append((cls, ns))
    edges = finish_type_edges(types)
    eq, eb, ub, bb = [], [], [], []
    for cls in range(nc):
        add(eq, eb, {i: int(cl == cls) for i, (cl, _) in enumerate(types)}, sizes[cls])
    for a, b in combinations(range(nc), 2):
        add(eq, eb, {i: int(cl == a) * ns[b] - int(cl == b) * ns[a]
                     for i, (cl, ns) in enumerate(types)}, 0)
    for a in range(nc):
        add(ub, bb, {i: ns[a] * (ns[a] - 1) + int(cl == a) * ns[a]
                     for i, (cl, ns) in enumerate(types)}, sizes[a] * (sizes[a] - 1))
    for a, b in combinations(range(nc), 2):
        add(ub, bb, {i: ns[a] * ns[b] + int(cl == a) * ns[b]
                     for i, (cl, ns) in enumerate(types)}, sizes[a] * sizes[b])
    balance = {}
    ball = {}
    for i, (cls, ns) in enumerate(types):
        for a in range(nc):
            balance[i, a] = len(eq)
            add(eq, eb, {i: -ns[a]}, 0)
            missed = int(cls >= 4 and a == 3)
            row = {i: ns[a] - sizes[a] + missed - (degrees[cls] - 1) * int(cls == a)}
            exact = a in (2, 3) or (cls in (2, 3) and a < 4) or cls == 2
            rows, rhs = (eq, eb) if exact else (ub, bb)
            ball[i, a] = (rows, len(rows))
            add(rows, rhs, row, 0)
    for column, (i, j) in enumerate(edges, len(types)):
        directions = ((i, j),) if i == j else ((i, j), (j, i))
        for root, neighbor in directions:
            cls, ns = types[neighbor]
            eq[balance[root, cls]][column] = 1
            for a in range(nc):
                rows, row = ball[root, a]
                rows[row][column] = ns[a]
    for degree, c, count in profile:
        add(eq, eb, {i: 1 for i, (cls, ns) in enumerate(types)
                     if degrees[cls] == degree and ns[2] + ns[3] == c}, count)
    fours = next(count for degree, c, count in profile if (degree, c) == (6, 4))
    add(ub, bb, {i: 1 for i, (cls, ns) in enumerate(types)
                 if degrees[cls] == 7 and ns[2] + ns[3] == 1
                 and sum(ns[a] * (degrees[a] - 6) for a in range(nc)) == 8},
        0 if fours == 2 else 3)
    add(eq, eb, {i: Fraction(ns[2] + ns[3], 2)
                 for i, (cls, ns) in enumerate(types) if cls in (2, 3)}, m)
    add(eq, eb, {i: 1 for i, (cls, ns) in enumerate(types)
                 if cls in (2, 3) and ns[2] + ns[3] == 2}, k)
    return types, edges, eq, eb, ub, bb, [Fraction(0)] * (len(types) + len(edges))


def cases():
    yield "m_at_A3", degree_model(False)
    yield "shared_six_endpoint", degree_model(True)
    for p in (0, 1):
        for m, k, name, profile in PROFILES:
            yield f"cycle_p{p}_{name}", colored_model(p, profile, m, k)


def check_dual(record, built):
    name, (types, edges, eq, eb, ub, bb, objective) = built
    require(record["name"] == name, "certificate order/name mismatch")
    require(record["dimensions"] == [len(types), len(edges), len(eq), len(ub)],
            f"dimension mismatch in {name}")
    denominator = record["denominator"]
    require(type(denominator) is int and denominator > 0, "bad denominator")
    coefficients = [Fraction(0)] * (len(types) + len(edges))
    rhs = Fraction(0)
    for key, rows, bounds in (("equality_multipliers", eq, eb),
                              ("inequality_multipliers", ub, bb)):
        seen = set()
        for entry in record[key]:
            require(isinstance(entry, list) and len(entry) == 2, "bad multiplier shape")
            row, numerator = entry
            require(type(row) is type(numerator) is int, "noninteger multiplier")
            require(0 <= row < len(rows) and row not in seen, "bad row index")
            require(key == "equality_multipliers" or numerator <= 0, "bad upper-row sign")
            seen.add(row)
            multiplier = Fraction(numerator, denominator)
            rhs += multiplier * bounds[row]
            for column, value in rows[row].items():
                coefficients[column] += multiplier * value
    excess = max(Fraction(0), *(value - objective[i]
                               for i, value in enumerate(coefficients)))
    require(record["variable_budget"] == 428, "wrong variable budget")
    corrected = rhs - 428 * excess
    require(rhs == Fraction(record["uncorrected_bound"]), "wrong raw bound")
    require(excess == Fraction(record["coefficient_excess"]), "wrong excess")
    require(corrected == Fraction(record["corrected_bound"]), "wrong corrected bound")
    require(corrected > (1 if name == "m_at_A3" else 0), "nonstrict certificate")
    return len(coefficients), corrected


def profile_cover():
    found = set()
    for m, k in ((2, 0), (2, 1), (3, 0)):
        budget = 5 - m - k
        for fours in (2, 3):
            for six1, seven0, seven3 in product((0, 1), repeat=3):
                if fours + six1 + seven0 + seven3 != budget:
                    continue
                remaining6 = 16 - fours - six1
                c3_6 = 39 + 2 * m - 4 * fours - six1 - 2 * remaining6
                c2_6 = remaining6 - c3_6
                remaining7 = 26 - seven0 - seven3
                c2_7 = 57 - 4 * m - 3 * seven3 - remaining7
                c1_7 = remaining7 - c2_7
                if min(c2_6, c3_6, c1_7, c2_7) < 0:
                    continue
                rows = ((6, 1, six1), (6, 2, c2_6), (6, 3, c3_6), (6, 4, fours),
                        (7, 0, seven0), (7, 1, c1_7), (7, 2, c2_7), (7, 3, seven3))
                found.add((m, k, tuple(row for row in rows if row[2])))
    expected = {(m, k, profile) for m, k, _, profile in PROFILES}
    require(found == expected and len(found) == 6, "incomplete low-profile cover")
    return len(found)


def four_set_bound():
    universe = frozenset(range(12))
    U = frozenset(range(4))
    configs = 0
    templates = 0
    for V in (frozenset(range(4, 8)), frozenset((0, 4, 5, 6))):
        for W in map(frozenset, combinations(universe, 4)):
            if len(U & W) > 1 or len(V & W) > 1:
                continue
            blocks = (U, V, W)
            options = []
            configs += 1
            for i, j in combinations(range(3), 2):
                if blocks[i] & blocks[j]:
                    continue
                complement = universe - blocks[i] - blocks[j]
                other = 3 - i - j
                for p in complement:
                    triple = complement - {p}
                    if len(triple & blocks[other]) <= 1:
                        options.append((p, triple, frozenset((i, j))))
            union = U | V | W
            if len(union) == 11:
                options.append((next(iter(universe - union)), None, frozenset(range(3))))
            templates += len(options)
            for left, right in combinations(options, 2):
                p, triple, used = left
                q, other_triple, other_used = right
                if p != q:
                    require(triple is not None and other_triple is not None
                            and len(triple & other_triple) >= 2,
                            "distinct singleton templates can coexist")
                else:
                    require(used & other_used, "same-singleton templates lack common four-set")
            for p in {option[0] for option in options}:
                used = [option[2] for option in options if option[0] == p]
                if used:
                    common = set(range(3))
                    for indices in used:
                        common &= indices
                    require(common, "A1 templates lack a common far four-set")
    require((configs, templates) == (294, 349), "wrong three-four-set census")
    require(max(min(2 + a, 5 - a) for a in range(4)) == 3, "wrong A1 capacity")
    return configs, templates


def two_four_incompatibility():
    T = frozenset(range(12))
    U = frozenset(range(4))
    V = frozenset(range(4, 8))
    K = T - U - V
    p = 8
    triple = K - {p}
    one_far = 0
    for pair in map(frozenset, combinations(T - U, 2)):
        if len(pair & V) > 1:
            continue
        small = tuple(frozenset(s) for size in range(4)
                      for s in combinations(T - pair, size))
        for left in small:
            if len(left & V) > 1:
                continue
            for right in small:
                if len(right & V) <= 1 and U | pair | left | right == T:
                    one_far += 1
    two_far = 0
    for pair in map(frozenset, combinations(K, 2)):
        if len(pair & triple) > 1:
            continue
        for size in range(4):
            for last in map(frozenset, combinations(T - pair, size)):
                if U | V | pair | last != T:
                    continue
                valid = not (pair & triple) if last == triple else len(last & triple) <= 1
                two_far += int(valid)
    require(one_far == two_far == 0, "type-(2,1) survives with an A1 vertex")


def canonical_partitions():
    result = set()
    for word in product(range(3), repeat=3):
        renaming = {}
        next_label = 0
        canonical = []
        for value in word:
            if value not in renaming:
                renaming[value] = next_label
                next_label += 1
            canonical.append(renaming[value])
        result.add(tuple(canonical))
    return tuple(sorted(result))


def frame_cover():
    frame_count = 0
    degree_count = 0
    bounded_count = 0
    survivors = Counter()
    for deficit in ((3,), (2, 1), (1, 1, 1)):
        owners = tuple(i for i, amount in enumerate(deficit) for _ in range(amount))
        r = len(deficit)
        for labels in canonical_partitions():
            far = tuple(frozenset(labels[j] for j, owner in enumerate(owners) if owner == i)
                        for i in range(r))
            if any(len(far[i]) != deficit[i] for i in range(r)):
                continue
            nx = max(labels) + 1
            choices = tuple((i, x) for i in range(r) for x in range(nx) if x not in far[i])
            for selected in product((0, 1), repeat=len(choices)):
                neighbors = [set() for _ in range(nx)]
                for bit, (i, x) in zip(selected, choices):
                    if bit:
                        neighbors[x].add(i)
                if any(sum(i in neighbors[x] for x in far[j])
                       != sum(j in neighbors[x] for x in far[i])
                       for i, j in combinations(range(r), 2)):
                    continue
                if any(len(neighbors[x] & neighbors[y]) > 1
                       for x, y in combinations(range(nx), 2)):
                    continue
                frame_count += 1
                forced_nonedge = {
                    (i, j)
                    for i, j in combinations(range(r), 2)
                    if any({i, j} <= neighbors[x] for x in range(nx))
                    or any(j in neighbors[x] for x in far[i])
                    or any(i in neighbors[x] for x in far[j])
                }
                independent = len(forced_nonedge) == r * (r - 1) // 2
                far_multiplicity = tuple(sum(x in row for row in far) for x in range(nx))
                for endpoint_degrees in product((6, 7), repeat=nx):
                    degree_count += 1
                    inventory = sum(
                        ((len(neighbors[x]) - 3) * (len(neighbors[x]) - 2) // 2
                         if endpoint_degrees[x] == 6 else
                         (len(neighbors[x]) - 1) * (len(neighbors[x]) - 2) // 2)
                        for x in range(nx)
                    )
                    p7 = sum(far_multiplicity[x] for x in range(nx)
                             if endpoint_degrees[x] == 7)
                    high_gap = sum(a * (a + 4) for a in deficit)
                    low_gap = sum((2 - len(neighbors[x])) ** 2 for x in range(nx)
                                  if endpoint_degrees[x] == 6)
                    positive = sum((len(neighbors[x]) - 3) * (len(neighbors[x]) - 2)
                                   for x in range(nx) if endpoint_degrees[x] == 6)
                    for m, k in ((2, 0), (2, 1), (3, 0)):
                        for fours in (2, 3):
                            bounded_count += 1
                            if fours + inventory > 5 - m - k:
                                continue
                            q_upper = 28 - high_gap - 4 * p7
                            if q_upper < low_gap:
                                continue
                            rho_upper = m if deficit == (1, 1, 1) and independent else 3 + k
                            b1_upper = 0 if fours == 2 else 3
                            charge_lower = 21 - 2 * m - rho_upper + p7 + positive
                            charge_upper = 7 + q_upper + b1_upper
                            if charge_lower > charge_upper:
                                continue
                            sizes = sorted(map(len, neighbors))
                            if (deficit == (1, 1, 1) and nx == 2
                                    and sizes == [1, 2] and endpoint_degrees == (6, 6)):
                                require((m, k, fours) == (2, 0, 2), "bad shared survivor")
                                shared = next(x for x in range(nx)
                                              if sum(x in row for row in far) == 2)
                                lone = 1 - shared
                                shared_owners = {i for i, row in enumerate(far) if shared in row}
                                lone_owner = next(i for i, row in enumerate(far) if lone in row)
                                require(neighbors[shared] == {lone_owner}
                                        and neighbors[lone] == shared_owners,
                                        "wrong shared-endpoint incidence")
                                survivors["shared"] += 1
                            elif deficit == (1, 1, 1) and nx == 3 and sizes == [2, 2, 2]:
                                require(independent and p7 in (0, 1), "bad cycle survivor")
                                for owner, row in enumerate(far):
                                    endpoint = next(iter(row))
                                    require(neighbors[endpoint] == set(range(3)) - {owner},
                                            "wrong six-cycle incidence")
                                survivors[f"cycle_p{p7}"] += 1
                            else:
                                raise RuntimeError("unclassified incidence-frame survivor")
    require((frame_count, degree_count, bounded_count) == (21, 130, 780),
            "wrong frame census")
    require(survivors == Counter({"cycle_p1": 12, "cycle_p0": 4, "shared": 3}),
            "wrong residual frame cover")
    return frame_count, degree_count, bounded_count, sum(survivors.values())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificates", type=Path)
    args = parser.parse_args()
    records = json.loads(args.certificates.read_text(encoding="ascii"))
    built = tuple(cases())
    require(len(records) == len(built) == 14, "wrong certificate count")
    checked = [check_dual(record, case) for record, case in zip(records, built)]
    total_columns = sum(columns for columns, _ in checked)
    m_bound = checked[0][1]
    min_margin = min(bound for _, bound in checked[1:])
    profiles = profile_cover()
    configs, templates = four_set_bound()
    two_four_incompatibility()
    frames = frame_cover()
    print("cleanroom_z12_A3_audit=PASS")
    print(f"certificate_cases={len(checked)} total_columns={total_columns} m_lower_bound={m_bound}")
    print(f"infeasibility_cases=13 minimum_exact_margin={min_margin} variable_budget=428")
    print(f"low_profiles={profiles} three_four_configurations={configs} A1_templates={templates}")
    print("two_four_A1_A2_coexistence_cases=0")
    print(f"incidence_frames={frames[0]} degree_assignments={frames[1]} bounded_cases={frames[2]} survivors={frames[3]}")
    print("survivor_forms=shared:3,cycle_p0:4,cycle_p1:12")
    print("colored_model_cases=12 high_partition=S9,R3 endpoint_degrees=p0_or_p1")
    print("conclusion=z12_A3_impossible; combined_A_at_most_2")


if __name__ == "__main__":
    main()
