#!/usr/bin/env python3
"""Exact q10-r10-c0 quotient-connectivity decision formula and degree cubes."""

from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import importlib
import json
import sys


ORDER = 43
TASK = "bo1-q10-r10-c000000"
Q = 10
CORE = (40, 41, 42)
ATOMS = tuple(tuple(range(4 * i, 4 * i + 4)) for i in range(Q)) + tuple(
    (v,) for v in CORE
)
WEIGHTS = tuple(map(len, ATOMS))
COLORS = ("red", "blue")
DEGREES = tuple(range(18, 25))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load_stratifier(repository):
    package = Path(repository).resolve() / "ramsey_r55_k4_degree_stratifier"
    need(package.is_dir(), "degree-stratifier package")
    sys.path.insert(0, str(package))
    module = importlib.import_module("stratify")
    need(Path(module.__file__).resolve().parent == package, "wrong stratifier module")
    return module


def quotient_layout(base_variables):
    first = base_variables + 1
    variables = {}
    for color in COLORS:
        for pair in combinations(range(len(ATOMS)), 2):
            variables[color, pair] = first
            first += 1
    return variables, first


def fixed_color(task, edge):
    if edge in task.fixed:
        return "red" if task.fixed[edge] else "blue"
    return None


def edge_literal(task, edge, color):
    """Return signed physical literal, or Boolean for a fixed edge."""
    fixed = fixed_color(task, edge)
    if fixed is not None:
        return fixed == color
    variable = task.variables[edge]
    return variable if color == "red" else -variable


def quotient_definitions(task, quotient):
    """Define y[c,i,j] iff some c-coloured physical edge joins atoms i,j."""
    for color in COLORS:
        for i, j in combinations(range(len(ATOMS)), 2):
            y = quotient[color, (i, j)]
            literals = []
            satisfied = False
            for u in ATOMS[i]:
                for v in ATOMS[j]:
                    literal = edge_literal(task, tuple(sorted((u, v))), color)
                    if literal is True:
                        satisfied = True
                    elif literal is not False:
                        literals.append(literal)
            if satisfied:
                yield (y,)
                continue
            if not literals:
                yield (-y,)
                continue
            for literal in literals:
                yield (-literal, y)
            yield tuple([-y] + literals)


def canonical_partitions():
    """All A/B/S atom partitions, once under A/B interchange."""
    for labels in product(range(3), repeat=len(ATOMS)):
        if 1 not in labels or 2 not in labels:
            continue
        # Atoms use increasing vertex order, so this is the A/B canonical side.
        if next(label for label in labels if label) != 1:
            continue
        yield labels


def selected_cut(labels):
    """Subsumption basis for every block-respecting cut of order at most 23."""
    separator = sum(weight for weight, label in zip(WEIGHTS, labels) if label == 0)
    if separator > 23:
        return False
    if separator >= 17:
        return True
    # With only the unconditional delta>=18 bound, retain a cut precisely when
    # no atom can move from a nonsingleton component to the separator while
    # keeping the separator smaller than 18.
    for side in (1, 2):
        indices = [i for i, label in enumerate(labels) if label == side]
        if len(indices) > 1 and any(separator + WEIGHTS[i] < 18 for i in indices):
            return False
    return True


def guard_output(stratifier, states_base, color, degree):
    need(19 <= degree <= 24, "guard degree")
    _, guards, _ = stratifier.degree_layout(states_base)
    return guards[color, degree, ORDER - 1]


def cut_clauses(task, stratifier, states_base, quotient):
    """A complete subsumption basis of block-respecting connectivity cuts."""
    guards = {
        (color, degree): guard_output(stratifier, states_base, color, degree)
        for color in COLORS for degree in range(19, 25)
    }
    for labels in canonical_partitions():
        if not selected_cut(labels):
            continue
        separator = sum(weight for weight, label in zip(WEIGHTS, labels) if label == 0)
        degree = max(18, separator + 1)
        for color in COLORS:
            clause = [] if degree == 18 else [-guards[color, degree]]
            tautology = False
            for i, j in combinations(range(len(ATOMS)), 2):
                if {labels[i], labels[j]} != {1, 2}:
                    continue
                y = quotient[color, (i, j)]
                # The only fixed atom-pair quotient values are the three core
                # pairs: red false, blue true.
                if i >= Q and j >= Q:
                    if color == "blue":
                        tautology = True
                        break
                    continue
                clause.append(y)
            if not tautology:
                need(clause, "empty quotient cut")
                yield tuple(clause)


def definition_dimensions(task):
    units = binaries = long = 0
    for color in COLORS:
        for i, j in combinations(range(len(ATOMS)), 2):
            literals = []
            satisfied = False
            for u in ATOMS[i]:
                for v in ATOMS[j]:
                    literal = edge_literal(task, tuple(sorted((u, v))), color)
                    if literal is True:
                        satisfied = True
                    elif literal is not False:
                        literals.append(literal)
            if satisfied or not literals:
                units += 1
            else:
                binaries += len(literals)
                long += 1
    return {"unit": units, "binary": binaries, "long": long,
            "clauses": units + binaries + long}


def cut_dimensions(task, stratifier, states_base, quotient):
    by_color = Counter()
    by_separator = Counter()
    widths = Counter()
    count = 0
    for clause in cut_clauses(task, stratifier, states_base, quotient):
        count += 1
        color = "red" if any(
            quotient["red", pair] in clause for pair in combinations(range(len(ATOMS)), 2)
        ) else "blue"
        by_color[color] += 1
        widths[len(clause)] += 1
    # Re-enumerate separator counts directly; this remains compact and makes
    # the metadata independently useful without encoding labels into clauses.
    for labels in canonical_partitions():
        if not selected_cut(labels):
            continue
        k = sum(weight for weight, label in zip(WEIGHTS, labels) if label == 0)
        by_separator["red", k] += 1
        core_a = any(labels[i] == 1 for i in range(Q, len(ATOMS)))
        core_b = any(labels[i] == 2 for i in range(Q, len(ATOMS)))
        if not (core_a and core_b):
            by_separator["blue", k] += 1
    need(sum(by_color.values()) == count, "cut color count")
    need(count == sum(by_separator.values()), "cut separator count")
    return {
        "clauses": count,
        "by_color": dict(sorted(by_color.items())),
        "by_separator": {
            color: {str(k): by_separator[color, k] for k in range(24)
                    if by_separator[color, k]}
            for color in COLORS
        },
        "minimum_width": min(widths),
        "maximum_width": max(widths),
        "width_histogram": {str(k): widths[k] for k in sorted(widths)},
    }


def permuted_root_core(word, rows, columns):
    answer = 0
    for new_row in range(4):
        for new_column in range(3):
            old_bit = 3 * rows[new_row] + columns[new_column]
            answer |= ((word >> old_bit) & 1) << (3 * new_row + new_column)
    return answer


def admissible_root_core(word):
    # A core vertex red-complete to the root K4 would make a red K5.
    return not any(all(word >> (3 * row + column) & 1 for row in range(4))
                   for column in range(3))


def root_core_symmetry_clauses(task):
    """One canonical 4x3 matrix per S4(root rows) x S3(core columns) orbit."""
    row_actions = tuple(permutations(range(4)))
    column_actions = tuple(permutations(range(3)))
    edges = [task.variables[tuple(sorted((row, core)))]
             for row in range(4) for core in CORE]
    for word in range(1 << 12):
        if not admissible_root_core(word):
            continue
        canonical = min(permuted_root_core(word, rows, columns)
                        for rows in row_actions for columns in column_actions)
        if word != canonical:
            yield tuple(-variable if word >> bit & 1 else variable
                        for bit, variable in enumerate(edges))


def build(repository, cache):
    stratifier = load_stratifier(repository)
    task, plan, ordered, expansion, base = stratifier.build(TASK, cache, False)
    quotient, final = quotient_layout(base["variables"])
    definitions = definition_dimensions(task)
    cuts = cut_dimensions(task, stratifier, expansion["variables"], quotient)
    symmetry_clauses = sum(1 for _ in root_core_symmetry_clauses(task))
    need(symmetry_clauses == 3310, "root-core symmetry dimension")
    meta = dict(base)
    meta.update({
        "interface": "q10-weighted-quotient-rootcore-v1",
        "degree_stratified_variables": base["variables"],
        "degree_stratified_clauses": base["clauses"],
        "quotient_variables": final - 1 - base["variables"],
        "quotient_definition_clauses": definitions["clauses"],
        "quotient_definition_partition": definitions,
        "quotient_cut_clauses": cuts["clauses"],
        "quotient_cuts": cuts,
        "root_core_group_order": 144,
        "root_core_admissible_matrices": 3375,
        "root_core_orbits": 65,
        "root_core_symmetry_clauses": symmetry_clauses,
        "variables": final - 1,
        "clauses": (base["clauses"] + definitions["clauses"] + cuts["clauses"] +
                    symmetry_clauses),
    })
    return stratifier, task, plan, ordered, expansion, base, quotient, meta


def clauses(stratifier, task, plan, ordered, expansion, base, quotient):
    yield from stratifier.clauses(task, plan, ordered, expansion)
    yield from quotient_definitions(task, quotient)
    yield from cut_clauses(task, stratifier, expansion["variables"], quotient)
    yield from root_core_symmetry_clauses(task)


def write(repository, cache, path):
    built = build(repository, cache)
    *parts, meta = built
    path = Path(path)
    digest = hashlib.sha256()
    count = size = width = 0
    with path.open("xb") as stream:
        line = f"p cnf {meta['variables']} {meta['clauses']}\n".encode()
        stream.write(line); digest.update(line); size += len(line)
        for clause in clauses(*parts):
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line); digest.update(line); size += len(line)
            count += 1; width = max(width, len(clause))
    need(count == meta["clauses"], "clause count")
    return dict(meta, bytes=size, sha256=digest.hexdigest(), max_width=width)


def exact_degree_units(stratifier, states_base, red_degree, blue_degree):
    need(red_degree in DEGREES and blue_degree in DEGREES and
         red_degree + blue_degree <= 42, "degree-pair stratum")
    states, guards, _ = stratifier.degree_layout(states_base)
    answer = []
    witness = []
    for color, degree in (("red", red_degree), ("blue", blue_degree)):
        if degree == 18:
            answer.append((-guards[color, 19, ORDER - 1],))
        else:
            answer.append((guards[color, degree, ORDER - 1],))
            if degree < 24:
                answer.append((-guards[color, degree + 1, ORDER - 1],))
        if degree < 24:
            if color == "red":
                witness.append(tuple(-states[v, 42, degree + 1] for v in range(ORDER)))
            else:
                witness.append(tuple(states[v, 42, 42 - degree] for v in range(ORDER)))
    return answer + witness


def write_branch(repository, cache, base_path, red_degree, blue_degree, path):
    built = build(repository, cache)
    stratifier, task, plan, ordered, expansion, base, quotient, meta = built
    units = exact_degree_units(stratifier, expansion["variables"], red_degree, blue_degree)
    base_path = Path(base_path); path = Path(path)
    first, rest = base_path.read_bytes().split(b"\n", 1)
    need(first == f"p cnf {meta['variables']} {meta['clauses']}".encode(), "base header")
    digest = hashlib.sha256()
    with path.open("xb") as stream:
        header = f"p cnf {meta['variables']} {meta['clauses'] + len(units)}\n".encode()
        stream.write(header); digest.update(header)
        stream.write(rest); digest.update(rest)
        for clause in units:
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line); digest.update(line)
    return {
        "task": TASK, "red_minimum_degree": red_degree,
        "blue_minimum_degree": blue_degree, "variables": meta["variables"],
        "clauses": meta["clauses"] + len(units), "stratum_clauses": len(units),
        "bytes": path.stat().st_size, "sha256": digest.hexdigest(),
    }


def write_all_branches(repository, cache, base_path, output):
    built = build(repository, cache)
    stratifier, task, plan, ordered, expansion, base, quotient, meta = built
    base_path = Path(base_path); output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    first, rest = base_path.read_bytes().split(b"\n", 1)
    need(first == f"p cnf {meta['variables']} {meta['clauses']}".encode(), "base header")
    rows = []
    for red_degree in DEGREES:
        for blue_degree in DEGREES:
            if red_degree + blue_degree > 42:
                continue
            suffix = exact_degree_units(stratifier, expansion["variables"],
                                        red_degree, blue_degree)
            path = output / f"d{red_degree:02d}-{blue_degree:02d}.cnf"
            digest = hashlib.sha256()
            with path.open("xb") as stream:
                header = f"p cnf {meta['variables']} {meta['clauses'] + len(suffix)}\n".encode()
                stream.write(header); digest.update(header)
                stream.write(rest); digest.update(rest)
                for clause in suffix:
                    line = (" ".join(map(str, clause)) + " 0\n").encode()
                    stream.write(line); digest.update(line)
            rows.append({
                "red_minimum_degree": red_degree,
                "blue_minimum_degree": blue_degree,
                "variables": meta["variables"],
                "clauses": meta["clauses"] + len(suffix),
                "stratum_clauses": len(suffix),
                "bytes": path.stat().st_size,
                "sha256": digest.hexdigest(),
                "path": path.name,
            })
    need(len(rows) == 28, "degree-stratum cover")
    return {"status": "GENERATED_EXHAUSTIVE_DEGREE_STRATA", "task": TASK,
            "strata": len(rows), "rows": rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    parser.add_argument("cache", type=Path)
    sub = parser.add_subparsers(dest="action", required=True)
    generate = sub.add_parser("generate")
    generate.add_argument("cnf", type=Path)
    branch = sub.add_parser("branch")
    branch.add_argument("base", type=Path)
    branch.add_argument("red", type=int)
    branch.add_argument("blue", type=int)
    branch.add_argument("cnf", type=Path)
    all_branches = sub.add_parser("all-branches")
    all_branches.add_argument("base", type=Path)
    all_branches.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.action == "generate":
        result = write(args.repository, args.cache, args.cnf)
    elif args.action == "branch":
        result = write_branch(args.repository, args.cache, args.base,
                              args.red, args.blue, args.cnf)
    else:
        result = write_all_branches(args.repository, args.cache, args.base, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
