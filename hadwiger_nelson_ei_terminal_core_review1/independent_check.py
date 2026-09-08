#!/usr/bin/env python3
"""Independent exact checker for the 1003-vertex EI spindle review.

This file deliberately imports no claimant module.  Algebraic numbers are
represented in Q(sqrt(3), sqrt(11), sqrt(247)) by their eight square-free
basis coefficients, and multiplication is implemented from exponent triples.
All coordinate numerators use the common physical denominator 4608.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


RADICANDS = (3, 11, 247)
BASIS = tuple(tuple((mask >> bit) & 1 for bit in range(3)) for mask in range(8))
BASIS_INDEX = {powers: i for i, powers in enumerate(BASIS)}
ONE = (1,) + (0,) * 7
SCALE = 4608

EXPECTED = {
    "rows": 502,
    "half_edges": 2620,
    "full_vertices": 1003,
    "full_edges": 5241,
    "pairs": 502503,
    "coordinate_rows_sha256": "bb612d002dd19264ab2548758343f3695155589b66228979f405578aa11c713e",
    "full_integer_points_sha256": "bd0d1c6a44a755951550747d85ea762bce47f2023e301b07287753bb5fa10fbf",
    "half_edges_sha256": "a9780844011764e5a7c4871b849a96dce20a6deb2556eb8f916a4b5b3e42e214",
    "full_edges_sha256": "3bd6457906d0a3012b26fc9a243ffafb081bb668e33ea849bfcac032bcba491b",
    "cnf_sha256": "3867b33e6e2a2b1669d8c7ae95231021b4fc3670fefb420f68ab845d923acb55",
    "boundary_words_sha256": "7cde84924a222e21d751de3f3bb38fc71a67e0b204fceed9af276862e6d11502",
    "boundary_words_bytes": 214154,
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def vector(terms=()):
    out = [0] * 8
    for coefficient, powers in terms:
        out[BASIS_INDEX[powers]] += coefficient
    return tuple(out)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def negate(value):
    return tuple(-x for x in value)


def scale(multiplier, value):
    return tuple(multiplier * x for x in value)


def multiply(left, right):
    out = [0] * 8
    for i, x in enumerate(left):
        if x == 0:
            continue
        for j, y in enumerate(right):
            if y == 0:
                continue
            total = tuple(BASIS[i][k] + BASIS[j][k] for k in range(3))
            factor = 1
            reduced = []
            for exponent, radicand in zip(total, RADICANDS):
                factor *= radicand ** (exponent // 2)
                reduced.append(exponent % 2)
            out[BASIS_INDEX[tuple(reduced)]] += x * y * factor
    return tuple(out)


def point(row, rotated):
    a, b, c, d = row
    x36 = vector(((a, (1, 0, 0)), (b, (0, 1, 0))))
    y36 = vector(((c, (0, 0, 0)), (d, (1, 1, 0))))
    if not rotated:
        return scale(128, x36), scale(128, y36)
    root247 = vector(((1, (0, 0, 1)),))
    # 4608 R(x36/36,y36/36), with cos=119/128 and
    # sin=3*sqrt(247)/128.
    x = add(scale(119, x36), negate(scale(3, multiply(root247, y36))))
    y = add(scale(3, multiply(root247, x36)), scale(119, y36))
    return x, y


def squared_distance(left, right):
    dx = add(left[0], negate(right[0]))
    dy = add(left[1], negate(right[1]))
    return add(multiply(dx, dx), multiply(dy, dy))


def digest(value):
    payload = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def enumerate_edges(points):
    unit = scale(SCALE * SCALE, ONE)
    return [
        (i, j)
        for i, j in itertools.combinations(range(len(points)), 2)
        if squared_distance(points[i], points[j]) == unit
    ]


def check_colouring(word, vertices, edges, colours, omitted=None):
    require(type(word) is str and len(word) == vertices, "colour word length/type")
    require(set(word) <= set(map(str, range(colours))), "colour word alphabet")
    require(
        all(word[u] != word[v] for u, v in edges if omitted not in (u, v)),
        "colour word violates an edge",
    )


def colour_cnf(vertices, edges, pins):
    clauses = []
    for vertex in range(vertices):
        clauses.append([4 * vertex + colour + 1 for colour in range(4)])
        for first, second in itertools.combinations(range(4), 2):
            clauses.append(
                [-(4 * vertex + first + 1), -(4 * vertex + second + 1)]
            )
    for left, right in edges:
        for colour in range(4):
            clauses.append(
                [-(4 * left + colour + 1), -(4 * right + colour + 1)]
            )
    clauses.extend(([4 * pins[0] + 1], [4 * pins[1] + 2]))
    text = f"p cnf {4 * vertices} {len(clauses)}\n"
    text += "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return clauses, text.encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--cnf", required=True, type=Path)
    parser.add_argument("--boundary-words", required=True, type=Path)
    args = parser.parse_args()

    package = args.package.resolve()
    rows = json.loads((package / "coordinates.json").read_text())
    certificate = json.loads((package / "certificate.json").read_text())
    boundary = json.loads((package / "boundary_certificate.json").read_text())

    require(
        type(rows) is list
        and all(
            type(row) is list
            and len(row) == 4
            and all(type(entry) is int for entry in row)
            for row in rows
        ),
        "coordinate schema",
    )
    require(rows == sorted(rows) and len({tuple(row) for row in rows}) == len(rows),
            "coordinate ordering/distinctness")
    require(len(rows) == EXPECTED["rows"], "half vertex count")
    require(digest(rows) == EXPECTED["coordinate_rows_sha256"], "coordinate-row identity")

    origin_row, terminal_row = [0, 0, 0, 0], [0, 0, 96, 0]
    origin, terminal = rows.index(origin_row), rows.index(terminal_row)
    require(certificate["pins"] == [origin, terminal], "terminal labels")

    left_points = [point(row, False) for row in rows]
    right_rows = [i for i in range(len(rows)) if i != origin]
    points = left_points + [point(rows[i], True) for i in right_rows]
    require(len(points) == len(set(points)) == EXPECTED["full_vertices"],
            "full exact point distinctness")
    require(digest(points) == EXPECTED["full_integer_points_sha256"],
            "full point identity")

    full_edges = enumerate_edges(points)
    half_edges = [(u, v) for u, v in full_edges if v < len(rows)]
    require(len(points) * (len(points) - 1) // 2 == EXPECTED["pairs"],
            "full pair count")
    require(len(full_edges) == EXPECTED["full_edges"], "full edge count")
    require(len(half_edges) == EXPECTED["half_edges"], "half edge count")
    require(digest(full_edges) == EXPECTED["full_edges_sha256"], "full edge identity")
    require(digest(half_edges) == EXPECTED["half_edges_sha256"], "half edge identity")

    label = {origin: origin}
    for full_label, half_label in enumerate(right_rows, start=len(rows)):
        label[half_label] = full_label
    copied_edges = set(half_edges)
    copied_edges.update(
        tuple(sorted((label[u], label[v]))) for u, v in half_edges
    )
    cross_edges = set(full_edges) - copied_edges
    terminal_edge = tuple(sorted((terminal, label[terminal])))
    require(cross_edges == {terminal_edge}, "non-shared cross-edge classification")

    # Direct geometric anchor checks, independent of the edge totals.
    endpoint_distance = squared_distance(points[origin], points[terminal])
    require(endpoint_distance == scale((8 * SCALE // 3) ** 2, ONE),
            "terminal distance 8/3")
    require(squared_distance(points[terminal], points[label[terminal]]) ==
            scale(SCALE * SCALE, ONE), "rotated terminals are not unit-separated")

    half_word = certificate["half_four_colouring"]
    full_word = certificate["full_five_colouring"]
    check_colouring(half_word, len(rows), half_edges, 4)
    check_colouring(full_word, len(points), full_edges, 5)
    require(half_word[origin] == half_word[terminal], "published half word terminal equality")
    require(set(half_word) == set("0123") and set(full_word) == set("01234"),
            "published witness palettes")

    clauses, cnf = colour_cnf(len(rows), half_edges, (origin, terminal))
    require(len(clauses) == 13996, "CNF clause count")
    require(hashlib.sha256(cnf).hexdigest() == EXPECTED["cnf_sha256"], "CNF identity")
    require(args.cnf.read_bytes() == cnf, "independent CNF differs from proof CNF")

    words_bytes = args.boundary_words.read_bytes()
    require(len(words_bytes) == EXPECTED["boundary_words_bytes"], "boundary byte count")
    require(hashlib.sha256(words_bytes).hexdigest() == EXPECTED["boundary_words_sha256"],
            "boundary word identity")
    words = json.loads(words_bytes)
    local = boundary["mandatory_half_nonterminals"]
    require(
        len(local) == len(set(local)) == 416
        and local == sorted(local)
        and origin not in local
        and terminal not in local,
        "local mandatory-set identity",
    )
    require(set(words) == set(map(str, local)), "local deletion-word coverage")

    def combine(left, right):
        return left + "".join(colour for i, colour in enumerate(right) if i != origin)

    checked = set()
    for vertex in local:
        local_word = words[str(vertex)]
        require(local_word[origin] == "0" and local_word[terminal] == "1",
                "local word terminal normalization")
        left_deletion = combine(local_word, half_word)
        right_deletion = combine(half_word, local_word)
        check_colouring(left_deletion, len(points), full_edges, 4, vertex)
        check_colouring(right_deletion, len(points), full_edges, 4, label[vertex])
        checked.update((vertex, label[vertex]))

    copied = combine(half_word, half_word)
    check_colouring(copied, len(points), full_edges, 4, terminal)
    check_colouring(copied, len(points), full_edges, 4, label[terminal])
    checked.update((terminal, label[terminal]))
    renamed = half_word.translate(str.maketrans("01", "10"))
    origin_deletion = combine(half_word, renamed)
    check_colouring(origin_deletion, len(points), full_edges, 4, origin)
    checked.add(origin)
    require(len(checked) == 835, "global mandatory-set count")

    result = {
        "verified": True,
        "representation": "exact exponent-triple radical algebra; no claimant-code imports",
        "half_vertices": len(rows),
        "half_edges": len(half_edges),
        "full_vertices": len(points),
        "full_edges": len(full_edges),
        "full_pairs_checked": len(points) * (len(points) - 1) // 2,
        "proper_nonshared_cross_edges": len(cross_edges),
        "half_four_colouring_checked": True,
        "full_five_colouring_checked": True,
        "independent_cnf_byte_match": True,
        "cnf_variables": 4 * len(rows),
        "cnf_clauses": len(clauses),
        "local_deletion_words_checked": len(local),
        "global_vertex_deletion_colourings_checked": len(checked),
        "mandatory_vertices_in_every_non_four_colourable_host_subgraph": len(checked),
        "all_host_subgraphs_at_most_vertices_four_colourable": len(checked) - 1,
        "global_lower_bound_claimed": False,
        "sub_509_target_achieved": len(points) < 509,
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
