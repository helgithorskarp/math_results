#!/usr/bin/env python3
"""Independent exact audit of the two six-point repair exclusions.

No target Python module is imported.  Original Parts coordinates come from
the integer field table, completion points are parsed as Fractions, and every
unit edge and stored coloring is checked from those data.  The hitting-set
CNFs are then regenerated, and the prefix-counter semantics are exhaustively
tested on all small assignments used by the source validation.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import lcm
from pathlib import Path
import json


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_parts509_two_triple_budgets"
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
PRIMES = (3, 5, 11)
EXPECTED = {
    (374, 375, 383): (930, 3234,
        "e4baa3fc9947c31a065fecd6a49fc4377a1281759f576e46f684692f4e8768f8"),
    (396, 412, 479): (485, 2789,
        "fedf92e241f9434222c015d18e603d6e778490edbccf02601526980f87d0ac0d"),
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def field_multiply(left, right):
    """Multiply in the ordered basis for Q(sqrt(3),sqrt(5),sqrt(11))."""
    answer = [0]*8
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            if not a or not b:
                continue
            repeated = i & j
            coefficient = a*b
            for bit, prime in enumerate(PRIMES):
                if repeated & (1 << bit):
                    coefficient *= prime
            answer[i ^ j] += coefficient
    return tuple(answer)


def field_add(left, right):
    return tuple(a+b for a, b in zip(left, right))


def field_subtract(left, right):
    return tuple(a-b for a, b in zip(left, right))


def squared_distance(first, second):
    dx = field_subtract(first[0], second[0])
    dy = field_subtract(first[1], second[1])
    return field_add(field_multiply(dx, dx), field_multiply(dy, dy))


def read_integer_points(path):
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        require(len(values) == 16, ("integer point width", len(points)))
        points.append((values[:8], values[8:]))
    require(len(points) == 509, ("integer point count", len(points)))
    return points


def read_all_points():
    """Combine scale-96 Parts data with independently parsed completion data."""
    originals = read_integer_points(
        REPOSITORY/"hadwiger_nelson_parts509_completion_census_degree9"/"points.tsv"
    )
    raw = json.loads((
        REPOSITORY/"hadwiger_nelson_parts509_swap_closure"/"completion_points.json"
    ).read_text())
    require(len(raw["points"]) == 1158, "completion point count")
    completions = []
    denominator = 96
    for point in raw["points"]:
        x = tuple(Fraction(value) for value in point["x"])
        y = tuple(Fraction(value) for value in point["y"])
        require(len(x) == len(y) == 8, "completion point width")
        for value in x+y:
            denominator = lcm(denominator, value.denominator)
        completions.append((x, y))

    scaled = [
        (tuple((denominator//96)*x for x in point[0]),
         tuple((denominator//96)*y for y in point[1]))
        for point in originals
    ]
    scaled.extend(
        (tuple(int(denominator*x) for x in point[0]),
         tuple(int(denominator*y) for y in point[1]))
        for point in completions
    )
    return denominator, tuple(scaled)


def unit_edges(points, indices, denominator):
    target = (denominator*denominator,)+(0,)*7
    return tuple(
        (first, second)
        for first, second in combinations(indices, 2)
        if squared_distance(points[first], points[second]) == target
    )


def edge_digest(edges):
    body = "".join(f"{a},{b}\n" for a, b in edges).encode("ascii")
    return sha256(body).hexdigest()


def validate_coloring_families(edges, vertices):
    certificate = json.loads((TARGET/"colourings.json").read_text())
    require(tuple(tuple(record["R"]) for record in certificate) == tuple(EXPECTED),
            "unexpected deletion triples")
    interface = json.loads((
        REPOSITORY/"hadwiger_nelson_parts509_interface_lemma"/"interface_L.json"
    ).read_text())
    left_rows = tuple(record["witness_colouring_L"] for record in interface["classes"])
    require(len(left_rows) == 20 and all(len(row) == 374 for row in left_rows),
            "left interface witness dimensions")

    pool_data = json.loads((
        REPOSITORY/"hadwiger_nelson_parts509_s_replacement_budget"/"pool_S.json"
    ).read_text())
    universe = tuple(sorted(pool_data["W_S"]))
    fixed_pool = tuple(v for v in universe if v < 509)
    additions = tuple(v for v in universe if v >= 509)
    require(fixed_pool == tuple(range(374, 509)), "S vertex range")
    require(additions == tuple(sorted(pool_data["Q5"])) and len(additions) == 168,
            "Q5 does not equal the completion portion of W_S")
    require(vertices == tuple(range(374))+universe, "geometry vertex order")

    families = {}
    used_interfaces = set()
    coloring_total = 0
    for record in certificate:
        removed = set(record["R"])
        require(len(removed) == 3 and removed <= set(fixed_pool), "bad deletion triple")
        family = []
        for witness in record["witnesses"]:
            interface_index = witness["p"]
            encoded = witness["c"]
            require(type(interface_index) is int and 0 <= interface_index < len(left_rows),
                    "bad interface index")
            require(len(encoded) == len(universe) and set(encoded) <= set(".0123"),
                    "bad encoded coloring")
            deleted = {v for v, color in zip(universe, encoded) if color == "."}
            require(deleted & set(fixed_pool) == removed, "wrong deleted S vertices")
            require(deleted <= set(universe), "deletion outside universe")
            excluded_additions = tuple(sorted(deleted-removed))
            require(excluded_additions and set(excluded_additions) <= set(additions),
                    "empty or invalid excluded-addition set")

            left = left_rows[interface_index]
            colors = {v: int(left[v]) for v in range(374)}
            colors.update({v: int(color) for v, color in zip(universe, encoded)
                           if color != "."})
            require(set(colors) == set(vertices)-deleted, "colored vertex set mismatch")
            require(all(0 <= color < 4 for color in colors.values()), "color range")
            require(all(a not in colors or b not in colors or colors[a] != colors[b]
                        for a, b in edges),
                    ("improper stored coloring", tuple(record["R"]), coloring_total))
            used_interfaces.add(interface_index)
            family.append(excluded_additions)
            coloring_total += 1
        require(len(family) == len(set(family)), "duplicate excluded-addition set")
        families[tuple(record["R"])] = tuple(family)
    return additions, families, len(used_interfaces), coloring_total


def prefix_counter(input_variables, bound):
    """Independently construct the forward at-least-prefix counter."""
    next_variable = max(input_variables)
    rows = []
    meanings = {}
    clauses = []
    for prefix_length, input_variable in enumerate(input_variables, 1):
        row = []
        for threshold in range(1, min(prefix_length, bound+1)+1):
            next_variable += 1
            row.append(next_variable)
            meanings[next_variable] = (prefix_length, threshold)
        clauses.append((-input_variable, row[0]))
        if rows:
            previous = rows[-1]
            for offset, previous_variable in enumerate(previous):
                clauses.append((-previous_variable, row[offset]))
                if offset+1 < len(row):
                    clauses.append((-input_variable, -previous_variable, row[offset+1]))
        rows.append(tuple(row))
    clauses.append((-rows[-1][bound],))
    return next_variable, tuple(clauses), meanings


def clause_true(clause, assignment):
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


def propagation_conflict(clauses, assignment):
    assignment = dict(assignment)
    while True:
        changed = False
        for clause in clauses:
            if any(abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
                   for lit in clause):
                continue
            unknown = [lit for lit in clause if abs(lit) not in assignment]
            if not unknown:
                return True
            if len(unknown) == 1:
                literal = unknown[0]
                variable, value = abs(literal), literal > 0
                if variable in assignment and assignment[variable] != value:
                    return True
                assignment[variable] = value
                changed = True
        if not changed:
            return False


def check_small_counters():
    cases = 0
    for length in range(1, 9):
        inputs = tuple(range(1, length+1))
        for bound in range(length):
            _, clauses, meanings = prefix_counter(inputs, bound)
            for bits in product((False, True), repeat=length):
                cases += 1
                input_assignment = dict(zip(inputs, bits))
                if sum(bits) <= bound:
                    assignment = dict(input_assignment)
                    for variable, (prefix_length, threshold) in meanings.items():
                        assignment[variable] = sum(bits[:prefix_length]) >= threshold
                    require(all(clause_true(clause, assignment) for clause in clauses),
                            ("intended counter extension fails", length, bound, bits))
                else:
                    require(propagation_conflict(clauses, input_assignment),
                            ("counter fails to refute", length, bound, bits))
    require(cases == 3586, ("small counter case count", cases))
    return cases


def cnf_bytes(additions, family):
    identifiers = {vertex: index+1 for index, vertex in enumerate(additions)}
    variable_count, counter_clauses, _ = prefix_counter(tuple(identifiers.values()), 6)
    clauses = tuple(tuple(identifiers[v] for v in excluded) for excluded in family)
    clauses += counter_clauses
    text = f"p cnf {variable_count} {len(clauses)}\n"
    text += "".join(" ".join(map(str, clause))+" 0\n" for clause in clauses)
    return variable_count, clauses, text.encode("ascii")


def main():
    denominator, points = read_all_points()
    pool_data = json.loads((
        REPOSITORY/"hadwiger_nelson_parts509_s_replacement_budget"/"pool_S.json"
    ).read_text())
    universe = tuple(sorted(pool_data["W_S"]))
    vertices = tuple(range(374))+universe
    require(len(vertices) == 677 and len(set(vertices)) == 677, "vertex universe")
    require(len({points[v] for v in vertices}) == 677, "coincident selected points")
    edges = unit_edges(points, vertices, denominator)
    require(len(edges) == 3400, ("unit edge count", len(edges)))

    additions, families, used_interfaces, coloring_total = validate_coloring_families(
        edges, vertices
    )
    require(coloring_total == 1415, ("coloring total", coloring_total))
    counter_cases = check_small_counters()

    family_summaries = []
    for triple, family in families.items():
        expected_witnesses, expected_clauses, expected_hash = EXPECTED[triple]
        variable_count, clauses, encoded = cnf_bytes(additions, family)
        digest = sha256(encoded).hexdigest()
        require(len(family) == expected_witnesses, ("family size", triple))
        require(variable_count == 1323 and len(clauses) == expected_clauses,
                ("CNF dimensions", triple, variable_count, len(clauses)))
        require(digest == expected_hash, ("CNF digest", triple, digest))
        set_sizes = tuple(map(len, family))
        family_summaries.append((triple, len(family), min(set_sizes), max(set_sizes), digest))

    print(f"PASS exact field reconstruction: {len(vertices)} distinct points, denominator={denominator}")
    print(f"PASS direct all-pairs geometry: {len(edges)} unit edges, sha256={edge_digest(edges)}")
    print(f"PASS all {coloring_total} explicit proper colorings; used L interfaces={used_interfaces}")
    for triple, count, smallest, largest, digest in family_summaries:
        label = ",".join(map(str, triple))
        print(f"PASS R={label}: witnesses={count} E-size-range={smallest}..{largest} CNF={digest}")
    print(f"PASS prefix-counter semantics: {counter_cases} assignment/bound cases")
    print("PASS independently regenerated CNFs: variables=1323 clauses=3234,2789")
    print("SCOPE coloring-cover plus hitting-set reduction only; unfinished a=6 search remains open")


if __name__ == "__main__":
    main()
