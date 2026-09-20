#!/usr/bin/env python3
"""Verify and generate the radius-three CNF for the order-28 witness.

Only the Python standard library is used.  The program reconstructs the
Cayley graph, validates the 42 six-partitions, and emits the exact DIMACS
formula whose separately recorded DRAT refutation proves the theorem.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path


GROUP_VERTICES = tuple((i, j) for j in range(4) for i in range(7))
GROUP_INDEX = {element: index for index, element in enumerate(GROUP_VERTICES)}
IDENTITY = (0, 0)
CONNECTION_SET = frozenset(
    {
        (2, 0),
        (5, 0),
        (3, 0),
        (4, 0),
        (0, 1),
        (0, 3),
        (1, 1),
        (1, 3),
        (3, 1),
        (3, 3),
        (1, 2),
        (6, 2),
    }
)

# Delete group vertex 0, the identity, and relabel old vertices 1,...,27 as
# local vertices 0,...,26.
N = 27
PAIRS = tuple(combinations(range(N), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
EXPECTED_CNF_SHA256 = "ec2fa762b02b8c385948e533cf9608fb5a290c7e2191cc701b23b38a41d5f421"


def multiply(x, y):
    """Multiply a^i b^j and a^k b^l when b a b^-1 = a^-1."""
    i, j = x
    k, ell = y
    return ((i + (-1 if j % 2 else 1) * k) % 7, (j + ell) % 4)


def build_order28_adjacency():
    rows = []
    for x in GROUP_VERTICES:
        rows.append(
            sum(1 << GROUP_INDEX[multiply(x, step)] for step in CONNECTION_SET)
        )
    return tuple(rows)


ORDER28_ADJACENCY = build_order28_adjacency()
BASE_EDGES = tuple(
    (u, v)
    for u, v in PAIRS
    if (ORDER28_ADJACENCY[u + 1] >> (v + 1)) & 1
)
BASE_EDGE_SET = frozenset(BASE_EDGES)


def edge_var(u, v):
    if u > v:
        u, v = v, u
    return 1 + PAIR_INDEX[u, v]


def parse_colourings(path):
    codes = []
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        code = raw.partition("#")[0].strip()
        if not code:
            continue
        assert len(code) == N, (line_number, "wrong length")
        assert set(code) == set("012345"), (line_number, "wrong alphabet")
        codes.append(code)
    assert len(codes) == len(set(codes)) == 42
    return tuple(codes)


def partition_from_code(code):
    return tuple(
        tuple(vertex for vertex, digit in enumerate(code) if digit == colour)
        for colour in "012345"
    )


def encode_at_most_three_deletions(next_var):
    """Forward sequential counter for false variables on inherited edges."""
    clauses = []
    state = {}
    for i in range(len(BASE_EDGES)):
        for count in range(1, 4):
            state[i, count] = next_var
            next_var += 1

    for i, edge in enumerate(BASE_EDGES):
        inherited_edge = edge_var(*edge)
        clauses.append((inherited_edge, state[i, 1]))
        if i == 0:
            continue
        for count in range(1, 4):
            clauses.append((-state[i - 1, count], state[i, count]))
        for count in range(2, 4):
            clauses.append(
                (
                    inherited_edge,
                    -state[i - 1, count - 1],
                    state[i, count],
                )
            )
        clauses.append((inherited_edge, -state[i - 1, 3]))
    return tuple(clauses), next_var


def build_formula(codes):
    clauses = []

    # A K4-free graph must omit at least one of the six edges on every four
    # vertices.
    for four in combinations(range(N), 4):
        clauses.append(
            tuple(-edge_var(u, v) for u, v in combinations(four, 2))
        )

    counter, next_var = encode_at_most_three_deletions(len(PAIRS) + 1)
    clauses.extend(counter)

    # To be a counterexample, the graph must break every listed six-colouring
    # by containing at least one edge within one of its colour classes.
    for code in codes:
        clause = []
        for colour_class in partition_from_code(code):
            clause.extend(
                edge_var(u, v) for u, v in combinations(colour_class, 2)
            )
        clauses.append(tuple(clause))

    variables = next_var - 1
    assert variables == 819
    assert len(clauses) == 18678
    return variables, tuple(clauses)


def render_dimacs(variables, clauses):
    lines = [f"p cnf {variables} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def validate_graph():
    assert len(GROUP_VERTICES) == 28
    assert GROUP_INDEX[IDENTITY] == 0
    assert IDENTITY not in CONNECTION_SET
    assert all(row.bit_count() == 12 for row in ORDER28_ADJACENCY)
    assert all(
        ((ORDER28_ADJACENCY[u] >> v) & 1)
        == ((ORDER28_ADJACENCY[v] >> u) & 1)
        for u in range(28)
        for v in range(28)
    )
    assert sum(row.bit_count() for row in ORDER28_ADJACENCY) // 2 == 168
    assert len(BASE_EDGES) == 156

    # Direct K4 check and an explicit check that all left translations are
    # graph automorphisms justify reducing deletion of an arbitrary vertex to
    # deletion of the identity.
    assert not any(
        all(
            (ORDER28_ADJACENCY[u] >> v) & 1
            for u, v in combinations(four, 2)
        )
        for four in combinations(range(28), 4)
    )
    edge_set = {
        (u, v)
        for u, v in combinations(range(28), 2)
        if (ORDER28_ADJACENCY[u] >> v) & 1
    }
    for left_factor in GROUP_VERTICES:
        permutation = tuple(
            GROUP_INDEX[multiply(left_factor, x)] for x in GROUP_VERTICES
        )
        translated = {
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edge_set
        }
        assert translated == edge_set


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-cnf",
        type=Path,
        help="write the byte-canonical DIMACS formula to this path",
    )
    args = parser.parse_args()

    validate_graph()
    codes = parse_colourings(Path(__file__).with_name("colourings.txt"))

    monochromatic_inherited = []
    for code in codes:
        monochromatic_inherited.append(
            sum(code[u] == code[v] for u, v in BASE_EDGES)
        )
    distribution = Counter(monochromatic_inherited)
    assert distribution == Counter({0: 11, 1: 22, 2: 7, 3: 2})
    assert all(count == 0 for count in monochromatic_inherited[:6])

    variables, clauses = build_formula(codes)
    encoded = render_dimacs(variables, clauses)
    digest = sha256(encoded).hexdigest()
    assert digest == EXPECTED_CNF_SHA256

    if args.write_cnf is not None:
        args.write_cnf.parent.mkdir(parents=True, exist_ok=True)
        args.write_cnf.write_bytes(encoded)

    print("order28_vertices=28 edges=168 k4_free=yes left_transitive=yes")
    print("deleted_identity_vertices=27 inherited_edges=156")
    print("colouring_blockers=42 seed_radius2_blockers=6")
    print("monochromatic_inherited_edges=0:11,1:22,2:7,3:2")
    print(f"cnf_variables={variables} cnf_clauses={len(clauses)}")
    print(f"cnf_bytes={len(encoded)}")
    print(f"cnf_sha256={digest}")
    if args.write_cnf is not None:
        print(f"wrote_cnf={args.write_cnf}")


if __name__ == "__main__":
    main()
