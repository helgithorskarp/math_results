#!/usr/bin/env python3
"""Add exact degree strata and their K4 contact consequences to h3899."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import tempfile
import source

ORDER = 43
DEGREE_INPUTS = 42
DEGREE_COUNTER_LEVEL = 25
MIN_DEGREE = 18
MAX_DEGREE = 24
STRATIFIED_DEGREES = tuple(range(19, 25))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def counter_keys(n, level):
    return [(i, j) for i in range(1, n + 1)
            for j in range(1, min(i, level) + 1)]


def degree_layout(base_variables):
    first = base_variables + 1
    states = {}
    for vertex in range(ORDER):
        for key in counter_keys(DEGREE_INPUTS, DEGREE_COUNTER_LEVEL):
            states[vertex, *key] = first
            first += 1
    guards = {}
    for color in ("red", "blue"):
        for degree in STRATIFIED_DEGREES:
            for step in range(1, ORDER):
                guards[color, degree, step] = first
                first += 1
    return states, guards, first


def threshold_clauses(inputs, state):
    """Define state[i,j] iff at least j of the first i signed literals hold."""
    yield (-state[1, 1], inputs[0])
    yield (state[1, 1], -inputs[0])
    for i in range(2, len(inputs) + 1):
        literal = inputs[i - 1]
        out = state[i, 1]
        previous = state[i - 1, 1]
        yield (-previous, out)
        yield (-literal, out)
        yield (-out, previous, literal)
        for j in range(2, min(i, DEGREE_COUNTER_LEVEL) + 1):
            out = state[i, j]
            diagonal = state[i - 1, j - 1]
            if j == i:
                yield (-out, diagonal)
                yield (-out, literal)
                yield (out, -diagonal, -literal)
            else:
                previous = state[i - 1, j]
                yield (-previous, out)
                yield (-diagonal, -literal, out)
                yield (-out, previous, diagonal)
                yield (-out, previous, literal)


def and_gate(out, left, right):
    """Define out iff the two signed input literals both hold."""
    yield (-out, left)
    yield (-out, right)
    yield (out, -left, -right)


def red_degree_inputs(task, vertex):
    answer = []
    for other in range(ORDER):
        if other == vertex:
            continue
        edge = tuple(sorted((vertex, other)))
        if edge in task.fixed:
            answer.append(1 if task.fixed[edge] else -1)
        else:
            answer.append(task.variables[edge])
    require(len(answer) == DEGREE_INPUTS, "degree input count")
    return answer


def color_degree_literals(states, color, degree):
    if color == "red":
        return [states[v, DEGREE_INPUTS, degree] for v in range(ORDER)]
    # blue degree >= d iff red degree <= 42-d iff red degree is not >=43-d.
    return [-states[v, DEGREE_INPUTS, ORDER - degree] for v in range(ORDER)]


def guard_clauses(literals, color, degree, guards):
    previous = literals[0]
    for step, literal in enumerate(literals[1:], 1):
        out = guards[color, degree, step]
        yield from and_gate(out, previous, literal)
        previous = out


def suffix(task, ordered_variables, k4_variables):
    modules = source.load()
    interface = modules["interface"]
    states, guards, final = degree_layout(k4_variables)
    for vertex in range(ORDER):
        local = {(i, j): states[vertex, i, j]
                 for i, j in counter_keys(DEGREE_INPUTS, DEGREE_COUNTER_LEVEL)}
        yield from threshold_clauses(red_degree_inputs(task, vertex), local)
        yield (states[vertex, DEGREE_INPUTS, MIN_DEGREE],)
        yield (-states[vertex, DEGREE_INPUTS, MAX_DEGREE + 1],)
    guard_outputs = {}
    for color in ("red", "blue"):
        for degree in STRATIFIED_DEGREES:
            literals = color_degree_literals(states, color, degree)
            yield from guard_clauses(literals, color, degree, guards)
            guard_outputs[color, degree] = guards[color, degree, ORDER - 1]
    for block in range(task.q):
        color = "red" if block < task.r else "blue"
        _, contact_states, _ = interface.block_layout(block, ordered_variables)
        # d=18 is unconditional: n_0 <= 53-2d = 17.
        yield (-contact_states[39, 18],)
        for degree in STRATIFIED_DEGREES:
            maximum_noncontacts = 53 - 2 * degree
            yield (-guard_outputs[color, degree],
                   -contact_states[39, maximum_noncontacts + 1])
    require(final - 1 == k4_variables + added_variables(), "layout dimension")


def degree_counter_dimensions():
    variables = len(counter_keys(DEGREE_INPUTS, DEGREE_COUNTER_LEVEL))
    clauses = 2
    for i in range(2, DEGREE_INPUTS + 1):
        clauses += 3
        for j in range(2, min(i, DEGREE_COUNTER_LEVEL) + 1):
            clauses += 3 if j == i else 4
    return variables, clauses


def added_variables():
    degree_variables, _ = degree_counter_dimensions()
    return ORDER * degree_variables + 2 * len(STRATIFIED_DEGREES) * (ORDER - 1)


def added_clauses(q):
    _, degree_clauses = degree_counter_dimensions()
    degree_windows = 2 * ORDER
    guard_definitions = 2 * len(STRATIFIED_DEGREES) * (ORDER - 1) * 3
    contact_consequences = q * (1 + len(STRATIFIED_DEGREES))
    return (ORDER * degree_clauses + degree_windows + guard_definitions +
            contact_consequences)


def build(name, cache, triangles=False):
    expansion = source.load()["expansion"]
    task, plan, ordered, base = expansion.build(name, cache, triangles)
    meta = dict(base)
    meta.update({
        "interface": "k4-signature-degree-strata-v1",
        "k4_expansion_variables": base["variables"],
        "k4_expansion_clauses": base["clauses"],
        "degree_counter_variables": ORDER * degree_counter_dimensions()[0],
        "degree_counter_clauses": ORDER * degree_counter_dimensions()[1],
        "degree_window_clauses": 2 * ORDER,
        "degree_guard_variables": 2 * len(STRATIFIED_DEGREES) * (ORDER - 1),
        "degree_guard_clauses": 2 * len(STRATIFIED_DEGREES) * (ORDER - 1) * 3,
        "contact_stratum_clauses": task.q * (1 + len(STRATIFIED_DEGREES)),
        "variables": base["variables"] + added_variables(),
        "clauses": base["clauses"] + added_clauses(task.q),
    })
    return task, plan, ordered, base, meta


def clauses(task, plan, ordered, base):
    expansion = source.load()["expansion"]
    yield from expansion.clauses(task, plan, ordered)
    yield from suffix(task, ordered["variables"], base["variables"])


def write(name, cache, path, triangles=False):
    task, plan, ordered, base, meta = build(name, cache, triangles)
    path = Path(path)
    digest = hashlib.sha256()
    size = count = width = 0
    with path.open("xb") as stream:
        line = f"p cnf {meta['variables']} {meta['clauses']}\n".encode()
        stream.write(line)
        digest.update(line)
        size += len(line)
        for clause in clauses(task, plan, ordered, base):
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line)
            digest.update(line)
            size += len(line)
            count += 1
            width = max(width, len(clause))
    require(count == meta["clauses"], "clause count")
    return dict(meta, bytes=size, sha256=digest.hexdigest(), max_width=width)


def assignment(path, variables):
    values = {}
    statuses = []
    for line in Path(path).read_text().splitlines():
        if line.startswith("s "):
            statuses.append(line)
        elif line.startswith("v "):
            for item in line[2:].split():
                literal = int(item)
                if literal == 0:
                    continue
                variable, value = abs(literal), literal > 0
                if variable in values and values[variable] != value:
                    raise ValueError("conflicting assignment")
                values[variable] = value
    require(statuses == ["s SATISFIABLE"], "exact SAT status")
    require(set(values) == set(range(1, variables + 1)) and values[1],
            "complete exact assignment")
    return values


def accept(name, cache, path, triangles=False):
    task, plan, ordered, base, meta = build(name, cache, triangles)
    values = assignment(path, meta["variables"])
    for clause in clauses(task, plan, ordered, base):
        require(any(values[abs(lit)] == (lit > 0) for lit in clause),
                "unsatisfied stratified formula")
    expansion = source.load()["expansion"]
    with tempfile.NamedTemporaryFile("w", prefix="degree-strata-base-", delete=True) as stream:
        stream.write("s SATISFIABLE\n")
        row = []
        for variable in range(1, base["variables"] + 1):
            row.append(str(variable if values[variable] else -variable))
            if len(row) == 20:
                stream.write("v " + " ".join(row) + " 0\n")
                row = []
        if row:
            stream.write("v " + " ".join(row) + " 0\n")
        stream.flush()
        result = expansion.accept(name, cache, stream.name, triangles)
    result.update(interface="k4-signature-degree-strata-v1",
                  augmented_variables=meta["variables"],
                  augmented_clauses=meta["clauses"])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cache")
    parser.add_argument("--task", required=True)
    parser.add_argument("--triangles", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--cnf")
    group.add_argument("--sat")
    args = parser.parse_args()
    result = (write(args.task, args.cache, args.cnf, args.triangles)
              if args.cnf else accept(args.task, args.cache, args.sat, args.triangles))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
