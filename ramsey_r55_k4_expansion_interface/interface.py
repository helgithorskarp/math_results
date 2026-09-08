#!/usr/bin/env python3
"""Compact CNF interface for the separator-18 K4 expansion consequence."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

ORDER = 43
BLOCK_SIZE = 4
OUTSIDE = ORDER - BLOCK_SIZE
MAX_NONCONTACTS = 20
COUNTER_LEVEL = MAX_NONCONTACTS + 1


def require(ok, message):
    if not ok:
        raise ValueError(message)


def validate(q, r, base_variables):
    require(type(q) is int and 7 <= q <= 10, "q range")
    require(type(r) is int and 5 <= r <= q, "r range")
    require(type(base_variables) is int and base_variables >= 1, "base variable range")


def physical_map(q):
    """The h3873/h3887 physical edge numbering, independent of core colors."""
    core_start = 4 * q
    fixed = set()
    for block in range(q):
        fixed.update(combinations(range(4 * block, 4 * block + 4), 2))
    fixed.update(combinations(range(core_start, ORDER), 2))
    return {edge: variable for variable, edge in enumerate(
        (edge for edge in combinations(range(ORDER), 2) if edge not in fixed), 2)}


def counter_keys():
    return [(i, j) for i in range(1, OUTSIDE + 1)
            for j in range(1, min(i, COUNTER_LEVEL) + 1)]


def dimensions(q, r, base_variables):
    validate(q, r, base_variables)
    indicators_per_block = OUTSIDE
    counters_per_block = len(counter_keys())
    variables_per_block = indicators_per_block + counters_per_block
    # 5 clauses define each noncontact indicator.  The exact recurrence has
    # 2 clauses at i=1, 2374 over i=2..39, and one final exclusion unit.
    clauses_per_block = 5 * OUTSIDE + 2377
    return {
        "q": q,
        "r": r,
        "base_variables": base_variables,
        "blocks": q,
        "outside_vertices_per_block": OUTSIDE,
        "max_noncontacts": MAX_NONCONTACTS,
        "contact_indicators_per_block": indicators_per_block,
        "counter_variables_per_block": counters_per_block,
        "variables_per_block": variables_per_block,
        "clauses_per_block": clauses_per_block,
        "added_variables": q * variables_per_block,
        "added_clauses": q * clauses_per_block,
        "variables": base_variables + q * variables_per_block,
        "clauses": q * clauses_per_block,
        "max_width": 5,
    }


def block_layout(block, base_variables):
    require(type(block) is int and block >= 0, "block index")
    per_block = OUTSIDE + len(counter_keys())
    first = base_variables + block * per_block + 1
    indicators = list(range(first, first + OUTSIDE))
    first += OUTSIDE
    states = {}
    for key in counter_keys():
        states[key] = first
        first += 1
    return indicators, states, first


def counter_clauses(indicators, states):
    """Define s[i,j] iff at least j of indicators[:i] are true."""
    z = indicators
    s = states
    yield (-s[1, 1], z[0])
    yield (s[1, 1], -z[0])
    for i in range(2, OUTSIDE + 1):
        x = z[i - 1]
        out = s[i, 1]
        previous = s[i - 1, 1]
        # out <-> previous OR x
        yield (-previous, out)
        yield (-x, out)
        yield (-out, previous, x)
        for j in range(2, min(i, COUNTER_LEVEL) + 1):
            out = s[i, j]
            diagonal = s[i - 1, j - 1]
            if j == i:
                # out <-> diagonal AND x; s[i-1,i] is the false boundary.
                yield (-out, diagonal)
                yield (-out, x)
                yield (out, -diagonal, -x)
            else:
                previous = s[i - 1, j]
                # out <-> previous OR (diagonal AND x)
                yield (-previous, out)
                yield (-diagonal, -x, out)
                yield (-out, previous, diagonal)
                yield (-out, previous, x)
    yield (-s[OUTSIDE, COUNTER_LEVEL],)


def suffix(q, r, base_variables):
    """Clauses appended after a complete h3887 direct or triangle formula."""
    validate(q, r, base_variables)
    variables = physical_map(q)
    for block in range(q):
        clique = list(range(4 * block, 4 * block + 4))
        outside = [v for v in range(ORDER) if v not in clique]
        red = block < r
        indicators, states, _ = block_layout(block, base_variables)
        for v, z in zip(outside, indicators):
            same_color = []
            for u in clique:
                edge = tuple(sorted((u, v)))
                literal = variables[edge]
                same_color.append(literal if red else -literal)
            # z iff all four same-color literals are false.
            for literal in same_color:
                yield (-z, -literal)
            yield tuple([z] + same_color)
        yield from counter_clauses(indicators, states)


def write_suffix(q, r, base_variables, path):
    meta = dimensions(q, r, base_variables)
    path = Path(path)
    digest = hashlib.sha256()
    size = count = width = 0
    with path.open("xb") as stream:
        line = f"p cnf {meta['variables']} {meta['clauses']}\n".encode()
        stream.write(line)
        digest.update(line)
        size += len(line)
        for clause in suffix(q, r, base_variables):
            line = (" ".join(map(str, clause)) + " 0\n").encode()
            stream.write(line)
            digest.update(line)
            size += len(line)
            count += 1
            width = max(width, len(clause))
    require(count == meta["clauses"] and width == meta["max_width"], "dimensions")
    return dict(meta, bytes=size, sha256=digest.hexdigest())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, required=True)
    parser.add_argument("--r", type=int, required=True)
    parser.add_argument("--base-variables", type=int, required=True)
    parser.add_argument("--cnf", required=True)
    args = parser.parse_args()
    print(json.dumps(write_suffix(args.q, args.r, args.base_variables, args.cnf),
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
