#!/usr/bin/env python3
"""Independent literal audit of the degree-stratified K4 formula."""
from pathlib import Path
import argparse
import hashlib
import json
import source

ORDER = 43
INPUTS = 42
LEVEL = 25
DEGREES = tuple(range(19, 25))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def keys(n, level):
    return [(i, j) for i in range(1, n + 1)
            for j in range(1, min(i, level) + 1)]


def allocate(base):
    nxt = base + 1
    states = {}
    for vertex in range(ORDER):
        for i, j in keys(INPUTS, LEVEL):
            states[vertex, i, j] = nxt
            nxt += 1
    guards = {}
    for color in ("red", "blue"):
        for degree in DEGREES:
            for step in range(1, ORDER):
                guards[color, degree, step] = nxt
                nxt += 1
    return states, guards, nxt


def edge_inputs(task, vertex):
    result = []
    for other in range(ORDER):
        if other == vertex:
            continue
        edge = tuple(sorted((vertex, other)))
        if edge in task.fixed:
            result.append(1 if task.fixed[edge] else -1)
        else:
            result.append(task.variables[edge])
    need(len(result) == INPUTS, "physical degree arity")
    return result


def counter(inputs, state):
    x = inputs[0]
    yield (-state[1, 1], x)
    yield (state[1, 1], -x)
    for i, x in enumerate(inputs[1:], 2):
        before, out = state[i - 1, 1], state[i, 1]
        yield (-before, out)
        yield (-x, out)
        yield (-out, before, x)
        for j in range(2, min(i, LEVEL) + 1):
            diagonal, out = state[i - 1, j - 1], state[i, j]
            if i == j:
                yield (-out, diagonal)
                yield (-out, x)
                yield (out, -diagonal, -x)
            else:
                before = state[i - 1, j]
                yield (-before, out)
                yield (-diagonal, -x, out)
                yield (-out, before, diagonal)
                yield (-out, before, x)


def guard_inputs(states, color, degree):
    if color == "red":
        return [states[v, INPUTS, degree] for v in range(ORDER)]
    return [-states[v, INPUTS, ORDER - degree] for v in range(ORDER)]


def guard(literals, color, degree, guards):
    previous = literals[0]
    for step in range(1, ORDER):
        literal = literals[step]
        out = guards[color, degree, step]
        yield (-out, previous)
        yield (-out, literal)
        yield (out, -previous, -literal)
        previous = out


def expected_suffix(task, ordered_variables, base_variables):
    modules = source.load()
    interface = modules["interface"]
    states, guards, final = allocate(base_variables)
    for vertex in range(ORDER):
        local = {(i, j): states[vertex, i, j] for i, j in keys(INPUTS, LEVEL)}
        yield from counter(edge_inputs(task, vertex), local)
        yield (states[vertex, INPUTS, 18],)
        yield (-states[vertex, INPUTS, 25],)
    outputs = {}
    for color in ("red", "blue"):
        for degree in DEGREES:
            literals = guard_inputs(states, color, degree)
            yield from guard(literals, color, degree, guards)
            outputs[color, degree] = guards[color, degree, ORDER - 1]
    for block in range(task.q):
        color = "red" if block < task.r else "blue"
        _, contact, _ = interface.block_layout(block, ordered_variables)
        yield (-contact[39, 18],)
        for degree in DEGREES:
            threshold = 54 - 2 * degree
            yield (-outputs[color, degree], -contact[39, threshold])
    need(final - 1 == base_variables + 32754, "final variable")


def read(path):
    stream = Path(path).open("rb")
    header = stream.readline().decode().split()
    need(len(header) == 4 and header[:2] == ["p", "cnf"], "DIMACS header")
    variables, clauses = map(int, header[2:])

    def records():
        for number, raw in enumerate(stream, 2):
            words = raw.decode().split()
            need(words and words[-1] == "0", f"terminator line {number}")
            literals = tuple(map(int, words[:-1]))
            need(all(lit and abs(lit) <= variables for lit in literals),
                 f"literal range line {number}")
            need(len({abs(lit) for lit in literals}) == len(literals),
                 f"repeated variable line {number}")
            need(not any(-lit in literals for lit in literals),
                 f"tautology line {number}")
            yield literals
        stream.close()
    return variables, clauses, records()


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def run(cache, task_name, path, triangles):
    modules = source.load()
    expansion = modules["expansion"]
    task, plan, ordered, base = expansion.build(task_name, cache, triangles)
    variables, declared, actual = read(path)
    expected_count = 0
    width = 0
    for clause in expansion.clauses(task, plan, ordered):
        got = next(actual, None)
        need(got == tuple(clause), "changed h3899 prefix clause")
        expected_count += 1
        width = max(width, len(got))
    prefix_clauses = expected_count
    for clause in expected_suffix(task, ordered["variables"], base["variables"]):
        got = next(actual, None)
        need(got == tuple(clause), "degree-stratifier suffix clause")
        expected_count += 1
        width = max(width, len(got))
    need(next(actual, None) is None, "trailing clause")
    need(declared == expected_count == base["clauses"] + 127717 + 7 * task.q,
         "clause count")
    need(variables == base["variables"] + 32754, "variable count")
    return {
        "status": "AUDITED_K4_DEGREE_STRATIFIED_FORMULA",
        "task": task_name,
        "triangles": triangles,
        "physical_variables": base["physical_variables"],
        "k4_expansion_variables": base["variables"],
        "k4_expansion_clauses": base["clauses"],
        "degree_counter_variables": 32250,
        "degree_counter_clauses": 126119,
        "degree_window_clauses": 86,
        "degree_guard_variables": 504,
        "degree_guard_clauses": 1512,
        "contact_stratum_clauses": 7 * task.q,
        "variables": variables,
        "clauses": declared,
        "prefix_clauses_checked": prefix_clauses,
        "max_width": width,
        "bytes": Path(path).stat().st_size,
        "sha256": digest(path),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--cnf", required=True)
    parser.add_argument("--triangles", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.cache, args.task, args.cnf, args.triangles),
                     indent=2, sort_keys=True))
