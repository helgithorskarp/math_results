#!/usr/bin/env python3
"""Independent literal audit for suffixes and complete augmented formulas."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import locked

ORDER = 43
OUTSIDE = 39
LEVEL = 21


def edge_variables(q):
    core = 4 * q
    omitted = set(combinations(range(core, ORDER), 2))
    for block in range(q):
        omitted.update(combinations(range(4 * block, 4 * block + 4), 2))
    table = {}
    number = 2
    for edge in combinations(range(ORDER), 2):
        if edge not in omitted:
            table[edge] = number
            number += 1
    return table


def state_shape():
    return [(i, j) for i in range(1, OUTSIDE + 1)
            for j in range(1, min(i, LEVEL) + 1)]


def independent_suffix(q, r, base):
    physical = edge_variables(q)
    shape = state_shape()
    stride = OUTSIDE + len(shape)
    for block in range(q):
        start = base + block * stride + 1
        z = list(range(start, start + OUTSIDE))
        s = dict(zip(shape, range(start + OUTSIDE, start + stride)))
        vertices = list(range(4 * block, 4 * block + 4))
        external = sorted(set(range(ORDER)) - set(vertices))
        color = 1 if block < r else -1
        for v, indicator in zip(external, z):
            literals = [color * physical[tuple(sorted((u, v)))] for u in vertices]
            for literal in literals:
                yield (-indicator, -literal)
            yield tuple([indicator] + literals)
        yield (-s[1, 1], z[0])
        yield (s[1, 1], -z[0])
        for i in range(2, OUTSIDE + 1):
            x = z[i - 1]
            old, new = s[i - 1, 1], s[i, 1]
            yield (-old, new)
            yield (-x, new)
            yield (-new, old, x)
            for j in range(2, min(i, LEVEL) + 1):
                diagonal, new = s[i - 1, j - 1], s[i, j]
                if i == j:
                    yield (-new, diagonal)
                    yield (-new, x)
                    yield (new, -diagonal, -x)
                else:
                    old = s[i - 1, j]
                    yield (-old, new)
                    yield (-diagonal, -x, new)
                    yield (-new, old, diagonal)
                    yield (-new, old, x)
        yield (-s[OUTSIDE, LEVEL],)


def suffix_dimensions(q, base):
    stride = OUTSIDE + len(state_shape())
    return base + q * stride, q * 2572


def consume(stream, clauses, digest, counters):
    for expected in clauses:
        line = stream.readline()
        digest.update(line)
        counters["bytes"] += len(line)
        counters["clauses"] += 1
        counters["width"] = max(counters["width"], len(expected))
        if tuple(map(int, line.split())) != expected + (0,):
            raise ValueError(("literal mismatch", counters["clauses"]))


def audit_suffix(q, r, base, path):
    expected_variables, expected_clauses = suffix_dimensions(q, base)
    digest = hashlib.sha256()
    counters = {"bytes": 0, "clauses": 0, "width": 0}
    with Path(path).open("rb") as stream:
        line = stream.readline()
        digest.update(line)
        counters["bytes"] += len(line)
        header = line.decode().split()
        if header != ["p", "cnf", str(expected_variables), str(expected_clauses)]:
            raise ValueError("suffix header")
        consume(stream, independent_suffix(q, r, base), digest, counters)
        if stream.read(1):
            raise ValueError("suffix trailing data")
    if counters["clauses"] != expected_clauses or counters["width"] != 5:
        raise ValueError("suffix dimensions")
    return {"q": q, "r": r, "base_variables": base,
            "variables": expected_variables, "clauses": expected_clauses,
            "bytes": counters["bytes"], "max_width": counters["width"],
            "sha256": digest.hexdigest(), "status": "AUDITED_EXPANSION_SUFFIX"}


def base_stream(name, cache, triangles):
    check_order = locked.load()["check_order"]
    modules = check_order.dependencies.load()
    old_name = "mp1" + name[3:]
    if triangles:
        backend = modules["triangle_audit"]
        data = backend.physical(old_name, cache)
        plan = backend.independent_plan(data)
        initial = max(plan["variables"].values())
        clauses = (clause for _, clause in backend.independent_clauses(data, plan))
        q, r, variables = data["q"], data["r"], data["variables"]
    else:
        backend = modules["physical_audit"]
        q, r, _, fixed, variables = backend.physical(old_name, cache)
        initial = len(variables) + 1
        clauses = backend.clauses(q, r, fixed, variables)
    order_clauses = check_order.independent_suffix(q, r, variables, initial)
    comparisons = sum(1 for block in range(1, q - 1) if block != r - 1)
    ordered_variables = initial + 15 * comparisons
    return q, r, ordered_variables, clauses, order_clauses


def audit_full(name, cache, path, triangles=False):
    q, r, ordered_variables, physical_clauses, order_clauses = base_stream(
        name, cache, triangles)
    expected_variables, added_clauses = suffix_dimensions(q, ordered_variables)
    digest = hashlib.sha256()
    counters = {"bytes": 0, "clauses": 0, "width": 0}
    with Path(path).open("rb") as stream:
        line = stream.readline()
        digest.update(line)
        counters["bytes"] += len(line)
        header = line.decode().split()
        if header[:2] != ["p", "cnf"] or len(header) != 4:
            raise ValueError("full header shape")
        if int(header[2]) != expected_variables:
            raise ValueError("full variable count")
        consume(stream, physical_clauses, digest, counters)
        consume(stream, order_clauses, digest, counters)
        ordered_clauses = counters["clauses"]
        consume(stream, independent_suffix(q, r, ordered_variables), digest, counters)
        if stream.read(1) or counters["clauses"] != int(header[3]):
            raise ValueError("full length")
    if counters["clauses"] - ordered_clauses != added_clauses:
        raise ValueError("interface count")
    return {"status": "AUDITED_COMPLETE_EXPANSION_FORMULA", "task": name,
            "triangles": triangles, "variables": expected_variables,
            "ordered_variables": ordered_variables,
            "clauses": counters["clauses"], "ordered_clauses": ordered_clauses,
            "expansion_variables": expected_variables - ordered_variables,
            "expansion_clauses": added_clauses, "bytes": counters["bytes"],
            "max_width": counters["width"], "sha256": digest.hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int)
    parser.add_argument("--r", type=int)
    parser.add_argument("--base-variables", type=int)
    parser.add_argument("--task")
    parser.add_argument("--cache")
    parser.add_argument("--triangles", action="store_true")
    parser.add_argument("--cnf", required=True)
    args = parser.parse_args()
    if args.task:
        answer = audit_full(args.task, args.cache, args.cnf, args.triangles)
    else:
        answer = audit_suffix(args.q, args.r, args.base_variables, args.cnf)
    print(json.dumps(answer, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
