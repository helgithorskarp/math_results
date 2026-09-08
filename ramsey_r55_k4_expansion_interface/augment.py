#!/usr/bin/env python3
"""Generate a complete h3887 formula with the K4 expansion interface."""
from pathlib import Path
import argparse
import hashlib
import json
import tempfile
import interface
import locked


def build(name, cache, triangles=False):
    ordered = locked.load()["ordered"]
    task, plan, old = ordered.build(name, cache, triangles)
    extra = interface.dimensions(task.q, task.r, old["variables"])
    meta = dict(old)
    meta.update({
        "interface": "separator18-k4-expansion-v1",
        "ordered_variables": old["variables"],
        "ordered_clauses": old["clauses"],
        "expansion_variables": extra["added_variables"],
        "expansion_clauses": extra["added_clauses"],
        "variables": old["variables"] + extra["added_variables"],
        "clauses": old["clauses"] + extra["added_clauses"],
    })
    return task, plan, old, meta


def clauses(task, plan, old):
    ordered = locked.load()["ordered"]
    yield from ordered.clauses(task, plan, old)
    yield from interface.suffix(task.q, task.r, old["variables"])


def write(name, cache, path, triangles=False):
    task, plan, old, meta = build(name, cache, triangles)
    path = Path(path)
    digest = hashlib.sha256()
    size = count = width = 0
    with path.open("xb") as stream:
        line = f"p cnf {meta['variables']} {meta['clauses']}\n".encode()
        stream.write(line)
        digest.update(line)
        size += len(line)
        for clause in clauses(task, plan, old):
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line)
            digest.update(line)
            size += len(line)
            count += 1
            width = max(width, len(clause))
    if count != meta["clauses"]:
        raise ValueError("clause dimensions")
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
    if statuses != ["s SATISFIABLE"]:
        raise ValueError("exact SATISFIABLE status required")
    if set(values) != set(range(1, variables + 1)) or not values[1]:
        raise ValueError("complete exact assignment required")
    return values


def accept(name, cache, path, triangles=False):
    task, plan, old, meta = build(name, cache, triangles)
    values = assignment(path, meta["variables"])
    for clause in clauses(task, plan, old):
        if not any(values[abs(literal)] == (literal > 0) for literal in clause):
            raise ValueError("unsatisfied augmented formula")
    # Reuse the pinned full physical decoder after removing only the uniquely
    # determined interface variables.  Its exact-assignment and five-set
    # checks remain unchanged.
    ordered = locked.load()["ordered"]
    with tempfile.NamedTemporaryFile("w", prefix="k4e-base-model-", delete=True) as stream:
        stream.write("s SATISFIABLE\n")
        row = []
        for variable in range(1, old["variables"] + 1):
            row.append(str(variable if values[variable] else -variable))
            if len(row) == 20:
                stream.write("v " + " ".join(row) + " 0\n")
                row = []
        if row:
            stream.write("v " + " ".join(row) + " 0\n")
        stream.flush()
        result = ordered.accept(name, cache, stream.name, triangles)
    result.update(interface="separator18-k4-expansion-v1",
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
