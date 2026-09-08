#!/usr/bin/env python3
"""Independent formula and theorem audit for Discovery Net h3925.

This checker imports no code from the reviewed degree-stratifier or its h3899
baseline.  It compares the complete baseline clause stream to the augmented
prefix, reconstructs the complete added suffix from the literal conventions,
and rechecks the combinatorial and primitive-gate claims from definitions.
"""

import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path


ORDER = 43
Q = R = 7
CORE_START = 28
BASE_VARIABLES = 10868
BASE_CLAUSES = 923269
ORDERED_VARIABLES = 6332
TARGET_VARIABLES = 43622
TARGET_CLAUSES = 1051035
BASE_SHA256 = "755dbcd5677bbc57a0865637dbce19fa72084c4846b3996b8697bf1485070178"
TARGET_SHA256 = "73745bbae36bb9959fa5dc5ae2495a13598ed202a2db61186dfa144d6dded0bf"
TARGET_MANIFEST_SHA256 = "d031ea7032146cb1cdc0eab7308b539702701d42995e10a2d7698ae4963cb02b"
BASE_MANIFEST_SHA256 = "18273dc7ca8a1a7e693a05a98a31df0c3c4b0b250efcf172f87bf97a61e1b78c"

CATALOGS = {
    3: ("r44_3.g6", 4, 3, "1d237c0da1c599bbd8f4cffdf1fd13171099276e9ca335a1e0c819e4be9b2bea"),
    7: ("r44_7.g6", 362, 6, "6a3da7f0687c392420f190db0643b5c5b7ecb1a3c5ed098c7d96200185a5f010"),
    11: ("r44_11.g6", 546356, 12, "39e10a1bb2d6b36d556e646e12f0181b2bc3bd45b334ad7f495b8900d7680433"),
    15: ("r44_15.g6", 640, 20, "53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1"),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            value.update(chunk)
    return value.hexdigest()


def parse_header(raw):
    fields = raw.decode("ascii").split()
    need(len(fields) == 4 and fields[:2] == ["p", "cnf"], "DIMACS header")
    return int(fields[2]), int(fields[3])


def parse_clause(raw, variables):
    fields = raw.decode("ascii").split()
    need(fields and fields[-1] == "0", "DIMACS clause terminator")
    clause = tuple(map(int, fields[:-1]))
    need(clause and all(literal and abs(literal) <= variables for literal in clause),
         "DIMACS literal range")
    absolute = [abs(literal) for literal in clause]
    need(len(absolute) == len(set(absolute)), "repeated clause variable")
    need(not any(-literal in clause for literal in clause), "tautological clause")
    return clause


def graph6(line, order):
    need(line.endswith(b"\n"), "graph6 newline")
    data = line[:-1]
    edge_count = order * (order - 1) // 2
    need(len(data) == 1 + (edge_count + 5) // 6 and data[0] == order + 63,
         "graph6 order or length")
    need(all(63 <= byte <= 126 for byte in data), "graph6 byte range")
    bits = "".join(f"{byte - 63:06b}" for byte in data[1:])
    need(set(bits[edge_count:]) <= {"0"}, "graph6 padding")
    edges = set()
    k = 0
    for high in range(1, order):
        for low in range(high):
            if bits[k] == "1":
                edges.add((low, high))
            k += 1
    return edges


def catalog_check(cache):
    counts = {}
    first_core = None
    for order, (name, count, line_bytes, wanted) in CATALOGS.items():
        path = Path(cache) / name
        raw = path.read_bytes()
        need(digest(path) == wanted, "catalog identity " + name)
        lines = raw.splitlines(keepends=True)
        need(len(lines) == count and all(len(line) == line_bytes for line in lines),
             "catalog shape " + name)
        counts[order] = len(lines)
        if order == 15:
            first_core = graph6(lines[0], order)
    need(first_core is not None, "missing order-15 core")
    all_edges = set(combinations(range(15), 2))
    complement = all_edges - first_core
    need(not any(set(combinations(vertices, 2)) <= first_core
                 for vertices in combinations(range(15), 4)), "red core K4")
    need(not any(set(combinations(vertices, 2)) <= complement
                 for vertices in combinations(range(15), 4)), "blue core K4")
    macro_classes = sum(q - 4 for q in range(7, 11))
    tasks = sum((q - 4) * counts[43 - 4 * q] for q in range(7, 11))
    need(macro_classes == 18 and tasks == 2189178, "family count")
    return first_core, counts, macro_classes, tasks


def counter_keys(inputs, level):
    return [(i, j) for i in range(1, inputs + 1)
            for j in range(1, min(i, level) + 1)]


def physical_task(core_edges):
    fixed = {}
    for block in range(Q):
        for edge in combinations(range(4 * block, 4 * block + 4), 2):
            fixed[edge] = True
    for low, high in combinations(range(15), 2):
        fixed[CORE_START + low, CORE_START + high] = (low, high) in core_edges
    variables = {}
    next_variable = 2
    for edge in combinations(range(ORDER), 2):
        if edge not in fixed:
            variables[edge] = next_variable
            next_variable += 1
    need(next_variable - 2 == 756, "physical variable count")
    return fixed, variables


def allocate_degree_variables():
    next_variable = BASE_VARIABLES + 1
    states = {}
    for vertex in range(ORDER):
        for i, j in counter_keys(42, 25):
            states[vertex, i, j] = next_variable
            next_variable += 1
    guards = {}
    for color in ("red", "blue"):
        for degree in range(19, 25):
            for step in range(1, ORDER):
                guards[color, degree, step] = next_variable
                next_variable += 1
    need(next_variable == TARGET_VARIABLES + 1, "degree layout endpoint")
    return states, guards


def threshold_clauses(inputs, state, level):
    yield (-state[1, 1], inputs[0])
    yield (state[1, 1], -inputs[0])
    for i in range(2, len(inputs) + 1):
        literal = inputs[i - 1]
        previous, out = state[i - 1, 1], state[i, 1]
        yield (-previous, out)
        yield (-literal, out)
        yield (-out, previous, literal)
        for j in range(2, min(i, level) + 1):
            diagonal, out = state[i - 1, j - 1], state[i, j]
            if i == j:
                yield (-out, diagonal)
                yield (-out, literal)
                yield (out, -diagonal, -literal)
            else:
                previous = state[i - 1, j]
                yield (-previous, out)
                yield (-diagonal, -literal, out)
                yield (-out, previous, diagonal)
                yield (-out, previous, literal)


def contact_state(block, i, j):
    first = ORDERED_VARIABLES + block * 648 + 1 + 39
    for key in counter_keys(39, 21):
        if key == (i, j):
            return first
        first += 1
    raise ValueError("missing contact state")


def expected_suffix(core_edges):
    fixed, variables = physical_task(core_edges)
    states, guards = allocate_degree_variables()
    for vertex in range(ORDER):
        inputs = []
        for other in range(ORDER):
            if vertex == other:
                continue
            edge = tuple(sorted((vertex, other)))
            inputs.append((1 if fixed[edge] else -1) if edge in fixed
                          else variables[edge])
        need(len(inputs) == 42, "degree arity")
        local = {(i, j): states[vertex, i, j] for i, j in counter_keys(42, 25)}
        yield from threshold_clauses(inputs, local, 25)
        yield (states[vertex, 42, 18],)
        yield (-states[vertex, 42, 25],)
    outputs = {}
    for color in ("red", "blue"):
        for degree in range(19, 25):
            literals = ([states[v, 42, degree] for v in range(ORDER)]
                        if color == "red" else
                        [-states[v, 42, ORDER - degree] for v in range(ORDER)])
            previous = literals[0]
            for step, literal in enumerate(literals[1:], 1):
                out = guards[color, degree, step]
                yield (-out, previous)
                yield (-out, literal)
                yield (out, -previous, -literal)
                previous = out
            outputs[color, degree] = previous
    for block in range(Q):
        color = "red" if block < R else "blue"
        yield (-contact_state(block, 39, 18),)
        for degree in range(19, 25):
            yield (-outputs[color, degree],
                   -contact_state(block, 39, 54 - 2 * degree))


def formula_check(baseline, target, core_edges):
    need(digest(baseline) == BASE_SHA256, "baseline formula hash")
    need(digest(target) == TARGET_SHA256, "target formula hash")
    prefix_digest = hashlib.sha256()
    suffix_digest = hashlib.sha256()
    maximum_width = 0
    with Path(baseline).open("rb") as old, Path(target).open("rb") as new:
        need(parse_header(old.readline()) == (BASE_VARIABLES, BASE_CLAUSES),
             "baseline formula header")
        need(parse_header(new.readline()) == (TARGET_VARIABLES, TARGET_CLAUSES),
             "target formula header")
        for _ in range(BASE_CLAUSES):
            old_raw, new_raw = old.readline(), new.readline()
            need(old_raw and old_raw == new_raw, "target prefix differs")
            clause = parse_clause(old_raw, BASE_VARIABLES)
            maximum_width = max(maximum_width, len(clause))
            prefix_digest.update(old_raw)
        need(old.read(1) == b"", "baseline trailing data")
        suffix_count = 0
        for wanted in expected_suffix(core_edges):
            raw = new.readline()
            need(raw, "truncated target suffix")
            got = parse_clause(raw, TARGET_VARIABLES)
            need(got == wanted, "independent suffix mismatch")
            maximum_width = max(maximum_width, len(got))
            suffix_digest.update(raw)
            suffix_count += 1
        need(new.read(1) == b"", "target trailing data")
    need(suffix_count == TARGET_CLAUSES - BASE_CLAUSES == 127766,
         "target suffix count")
    need(maximum_width == 8, "formula maximum width")
    return prefix_digest.hexdigest(), suffix_digest.hexdigest(), maximum_width


def satisfies(clauses, values):
    return all(any(values[abs(literal)] == (literal > 0) for literal in clause)
               for clause in clauses)


def primitive_truth_tables():
    checked = 0
    families = [
        ((1, 2), [(-2, 1), (2, -1)], lambda row: row[1] == row[0]),
        ((1, 2, 3), [(-1, 3), (-2, 3), (-3, 1, 2)],
         lambda row: row[2] == (row[0] or row[1])),
        ((1, 2, 3), [(-3, 1), (-3, 2), (3, -1, -2)],
         lambda row: row[2] == (row[0] and row[1])),
        ((1, 2, 3, 4), [(-1, 4), (-2, -3, 4), (-4, 1, 2), (-4, 1, 3)],
         lambda row: row[3] == (row[0] or (row[1] and row[2]))),
    ]
    for variables, clauses, meaning in families:
        for row in product((False, True), repeat=len(variables)):
            values = dict(zip(variables, row))
            need(satisfies(clauses, values) == meaning(row), "primitive gate semantics")
            checked += 1
    need(checked == 36, "primitive truth-table count")
    for red_degree in range(43):
        for degree in range(18, 25):
            need((42 - red_degree >= degree) == (not (red_degree >= 43 - degree)),
                 "blue-degree signed literal")
        need(((red_degree >= 18) and not (red_degree >= 25)) ==
             (18 <= red_degree <= 24), "degree window semantics")
    return checked


def unit_propagate(clauses, initial):
    values = dict(initial)
    while True:
        changed = False
        for clause in clauses:
            if any(abs(literal) in values and
                   values[abs(literal)] == (literal > 0) for literal in clause):
                continue
            open_literals = [literal for literal in clause
                             if abs(literal) not in values]
            if not open_literals:
                return None
            if len(open_literals) == 1:
                literal = open_literals[0]
                variable, value = abs(literal), literal > 0
                if variable in values and values[variable] != value:
                    return None
                if variable not in values:
                    values[variable] = value
                    changed = True
        if not changed:
            return values


def local_counter(n, level):
    inputs = list(range(1, n + 1))
    next_variable = n + 1
    states = {}
    for key in counter_keys(n, level):
        states[key] = next_variable
        next_variable += 1
    return inputs, states, list(threshold_clauses(inputs, states, level))


def propagation_controls():
    small_assignments = 0
    for n in range(2, 10):
        for bound in range(1, n):
            inputs, states, clauses = local_counter(n, bound + 1)
            clauses.append((-states[n, bound + 1],))
            for row in product((False, True), repeat=n):
                values = dict(zip(inputs, row))
                for i, j in states:
                    values[states[i, j]] = sum(row[:i]) >= j
                need(satisfies(clauses, values) == (sum(row) <= bound),
                     "small exact counter semantics")
                small_assignments += 1
    need(small_assignments == 7172, "small counter assignment count")

    boundary_cases = 0
    for bound in (17, 15, 13, 11, 9, 7, 5):
        inputs, states, clauses = local_counter(39, bound + 1)
        clauses.append((-states[39, bound + 1],))
        patterns = set()
        for step in (1, 2, 5):
            for offset in range(39):
                patterns.add(tuple(sorted((offset + step * i) % 39
                                          for i in range(bound))))
        for selected in patterns:
            initial = {inputs[index]: True for index in selected}
            forced = unit_propagate(clauses, initial)
            need(forced is not None and
                 all(forced.get(inputs[index]) is False
                     for index in range(39) if index not in selected),
                 "contact boundary propagation")
            extra = next(index for index in range(39) if index not in selected)
            need(unit_propagate(clauses,
                                {**initial, inputs[extra]: True}) is None,
                 "contact excess propagation")
            boundary_cases += 1
    return small_assignments, boundary_cases


def signature_theorem():
    rows = []
    for degree in range(18, 25):
        feasible = []
        for n0 in range(40):
            for n1 in range(40 - n0):
                for n2 in range(40 - n0 - n1):
                    n3 = 39 - n0 - n1 - n2
                    if n3 <= 16 and n1 + 2 * n2 + 3 * n3 >= 4 * (degree - 3):
                        feasible.append((n0, n1, n2, n3))
        maximum = max(row[0] for row in feasible)
        extrema = [list(row) for row in feasible if row[0] == maximum]
        need(maximum == 53 - 2 * degree, "signature contact bound")
        need(extrema == [[53 - 2 * degree, 0, 2 * degree - 30, 16]],
             "signature extremal aggregate")
        rows.append({"minimum_color_degree": degree,
                     "feasible_populations": len(feasible),
                     "maximum_noncontacts": maximum,
                     "minimum_contacts": 39 - maximum,
                     "extremal_population": extrema[0]})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reviewed_source", type=Path)
    parser.add_argument("cache", type=Path)
    parser.add_argument("baseline_cnf", type=Path)
    parser.add_argument("target_cnf", type=Path)
    args = parser.parse_args()
    need(digest(args.reviewed_source / "ramsey_r55_k4_degree_stratifier" / "SHA256SUMS") ==
         TARGET_MANIFEST_SHA256, "target package manifest")
    need(digest(args.reviewed_source / "ramsey_r55_k4_expansion_interface" / "SHA256SUMS") ==
         BASE_MANIFEST_SHA256, "baseline package manifest")
    core, counts, macro_classes, tasks = catalog_check(args.cache)
    prefix_hash, suffix_hash, width = formula_check(
        args.baseline_cnf, args.target_cnf, core
    )
    theorem = signature_theorem()
    truth_rows = primitive_truth_tables()
    small_controls, boundary_controls = propagation_controls()
    result = {
        "status": "INDEPENDENT_K4_DEGREE_STRATIFIER_VERIFIED_H3925",
        "reviewed_source_commit": "68ce2ce13db7885be3c5f225a1108baf102cd3f4",
        "target_manifest_sha256": TARGET_MANIFEST_SHA256,
        "baseline_manifest_sha256": BASE_MANIFEST_SHA256,
        "catalog_counts": counts,
        "catalog_completeness_imported": True,
        "macro_classes": macro_classes,
        "physical_tasks": tasks,
        "baseline_formula_sha256": BASE_SHA256,
        "target_formula_sha256": TARGET_SHA256,
        "prefix_clauses_equal": BASE_CLAUSES,
        "prefix_clause_stream_sha256": prefix_hash,
        "independently_reconstructed_suffix_clauses": TARGET_CLAUSES - BASE_CLAUSES,
        "suffix_clause_stream_sha256": suffix_hash,
        "target_variables": TARGET_VARIABLES,
        "target_clauses": TARGET_CLAUSES,
        "target_maximum_width": width,
        "primitive_truth_assignments": truth_rows,
        "exhaustive_small_counter_assignments": small_controls,
        "full_size_contact_boundary_placements": boundary_controls,
        "minimum_contact_floors": [row["minimum_contacts"] for row in theorem],
        "signature_rows": theorem,
        "solver_calls": 0,
        "tasks_decided": 0,
        "good43_found": False,
        "ramsey_lower_bound_improved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
