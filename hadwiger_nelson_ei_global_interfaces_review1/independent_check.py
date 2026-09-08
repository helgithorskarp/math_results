#!/usr/bin/env python3
"""No-import independent check of the h3885 8,585-point construction.

The checker uses exact arithmetic in a squarefree radical basis, reconstructs
the geometry from the pinned tables, checks the colouring CNF and positive-hint
LRAT proof, and uses a separate DSATUR-style search for the T375 premise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path


TARGET_MANIFEST = "1825c1f03c50589c2ba305f5933f4ab958523886d69345923a98e7a7f63ff021"
T375_MANIFEST = "420c0108b4e3a2e55ea3bcfe1ae4871c583bcf56e3bb9ff9cdc4823dc28636d9"
EI_MANIFEST = "f93f0ff1afe9ed7db3dc6d70a0400a754329b277217637148f9a1256116ba87f"
RADICANDS = (3, 11, 247)
ZERO = (F(0),) * 8
ONE = (F(1),) + (F(0),) * 7


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: Path):
    return json.loads(path.read_text())


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(directory: Path, digest: str, entries: int) -> None:
    path = directory / "SHA256SUMS"
    require(file_sha(path) == digest, f"manifest identity: {directory.name}")
    lines = path.read_text().splitlines()
    require(len(lines) == entries, f"manifest cardinality: {directory.name}")
    names = set()
    for line in lines:
        pieces = line.split("  ", 1)
        require(len(pieces) == 2, "manifest syntax")
        wanted, name = pieces
        require(name and name not in names and not Path(name).is_absolute(), "manifest name")
        names.add(name)
        require(file_sha(directory / name) == wanted, f"manifest entry: {directory.name}/{name}")


# Elements of Q(sqrt(3),sqrt(11),sqrt(247)) in the bit-indexed basis.
def scalar(value) -> tuple[F, ...]:
    return (F(value),) + (F(0),) * 7


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, value):
    return tuple(x * value for x in a)


def mul(a, b):
    answer = [F(0)] * 8
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if not y:
                continue
            factor = 1
            for k, radicand in enumerate(RADICANDS):
                if (i & j) >> k & 1:
                    factor *= radicand
            answer[i ^ j] += factor * x * y
    return tuple(answer)


def point_add(p, q):
    return add(p[0], q[0]), add(p[1], q[1])


def point_sub(p, q):
    return sub(p[0], q[0]), sub(p[1], q[1])


def conjugate(p):
    return p[0], neg(p[1])


def complex_mul(p, q):
    return sub(mul(p[0], q[0]), mul(p[1], q[1])), add(mul(p[0], q[1]), mul(p[1], q[0]))


def norm(p):
    return add(mul(p[0], p[0]), mul(p[1], p[1]))


def distance(p, q):
    return norm(point_sub(p, q))


def point(row):
    a, b, c, d = row
    return (F(0), F(a), F(b), F(0), F(0), F(0), F(0), F(0)), (
        F(c), F(0), F(0), F(d), F(0), F(0), F(0), F(0)
    )


def row(p):
    x, y = p
    require(not any(x[k] for k in (0, 3, 4, 5, 6, 7)), "unexpected x support")
    require(not any(y[k] for k in (1, 2, 4, 5, 6, 7)), "unexpected y support")
    values = (x[1], x[2], y[0], y[3])
    require(all(value.denominator == 1 for value in values), "nonintegral row")
    return tuple(int(value) for value in values)


def frame(source_a, source_b, target_a, target_b, squared_length: int, reflected: bool = False):
    if reflected:
        source_a, source_b = conjugate(source_a), conjugate(source_b)
    source_delta = point_sub(source_b, source_a)
    target_delta = point_sub(target_b, target_a)
    require(norm(source_delta) == scalar(squared_length), "source frame length")
    require(norm(target_delta) == scalar(squared_length), "target frame length")
    multiplier = tuple(scale(axis, F(1, squared_length)) for axis in complex_mul(target_delta, conjugate(source_delta)))
    require(norm(multiplier) == ONE, "non-isometric frame")
    translation = point_sub(target_a, complex_mul(multiplier, source_a))
    return multiplier, translation, reflected


def apply(mapping, p):
    multiplier, translation, reflected = mapping
    if reflected:
        p = conjugate(p)
    return point_add(translation, complex_mul(multiplier, p))


def row_distance(p, q):
    a, b, c, d = (x - y for x, y in zip(p, q))
    return 3 * a * a + 11 * b * b + c * c + 33 * d * d, 2 * (a * b + c * d)


def exact_edges(rows, numerator: int = 1296):
    return [(u, v) for u, v in combinations(range(len(rows)), 2) if row_distance(rows[u], rows[v]) == (numerator, 0)]


def reconstruct_t375(t375: Path):
    rotation = scalar(F(-1, 2)), (F(0), F(1, 2), F(0), F(0), F(0), F(0), F(0), F(0))
    orbit = set()
    for raw in read_json(t375 / "appendix.json"):
        p = point(raw)
        for _ in range(3):
            orbit.add(p)
            orbit.add((neg(p[0]), p[1]))  # reflection in the y-axis
            p = complex_mul(rotation, p)
    terminals = list(map(point, ((0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0))))
    require(set(terminals) <= orbit and len(orbit) == 627, "T375 reference orbit")
    reference = terminals + sorted(orbit - set(terminals))
    certificate = read_json(t375 / "certificate.json")
    kept = certificate["retained_reference_indices"]
    require(len(kept) == 375 and kept[:3] == [0, 1, 2] and kept == sorted(set(kept)), "T375 retained set")
    points = [reference[index] for index in kept]
    rows = [row(p) for p in points]
    edges = exact_edges(rows)
    require(len(edges) == 1661 and certificate["vertices"] == 375 and certificate["edges"] == 1661, "T375 inventory")
    word = certificate["unpinned_colouring"]
    require(len(word) == 375 and set(word) <= set("0123"), "T375 colouring format")
    require(all(word[u] != word[v] for u, v in edges), "T375 supplied colouring")
    require(all(row_distance(rows[u], rows[v]) == (432, 0) for u, v in combinations(range(3), 2)), "T375 terminals")
    return points, rows, edges


def t375_dsatur(edges):
    """Independent named-colour search; no domain propagation is shared."""
    n = 375
    neighbours = [set() for _ in range(n)]
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    colours = [-1] * n
    for vertex in (0, 1, 2):
        colours[vertex] = 0
    nodes = 0

    def visit(done: int) -> bool:
        nonlocal nodes
        nodes += 1
        if done == n:
            return True
        choice = None
        choice_key = None
        legal_colours = None
        for vertex, colour in enumerate(colours):
            if colour >= 0:
                continue
            forbidden = {colours[u] for u in neighbours[vertex] if colours[u] >= 0}
            legal = [colour_name for colour_name in range(4) if colour_name not in forbidden]
            if not legal:
                return False
            key = (len(legal), -len(forbidden), -len(neighbours[vertex]), vertex)
            if choice_key is None or key < choice_key:
                choice, choice_key, legal_colours = vertex, key, legal
        used = {colour for colour in colours if colour >= 0}
        tried_new = False
        for colour in legal_colours:
            if colour not in used:
                if tried_new:
                    continue
                tried_new = True
            colours[choice] = colour
            if visit(done + 1):
                return True
        colours[choice] = -1
        return False

    satisfiable = visit(3)
    require(not satisfiable and nodes == 21593, "independent T375 search")
    return nodes


def reconstruct_layer(ei: Path):
    g40_rows = list(map(tuple, read_json(ei / "g40.json")))
    g49_rows = list(map(tuple, read_json(ei / "g49.json")))
    g40 = list(map(point, g40_rows))
    g49 = list(map(point, g49_rows))
    pairs = [pair for pair in combinations(range(40), 2) if row_distance(*(g40_rows[v] for v in pair)) == (4752, 0)]
    triangles = [triple for triple in combinations(range(49), 3) if all(row_distance(g49_rows[u], g49_rows[v]) == (432, 0) for u, v in combinations(triple, 2))]
    source_certificate = read_json(ei / "certificate.json")
    selected_pairs = sorted(
        set(source_certificate["g40"]["essential"])
        | {value for k, value in enumerate(source_certificate["g40"]["optional"]) if 1682 >> k & 1}
    )
    require(len(pairs) == 59 and len(triangles) == 18 and len(selected_pairs) == 53, "source incidence")
    union = set(g40)
    targets = set()
    for pair_index in selected_pairs:
        u, v = pairs[pair_index]
        mapping = frame(g49[0], g49[1], g40[u], g40[v], 4752)
        placed = [apply(mapping, p) for p in g49]
        union.update(placed)
        for triangle_index in source_certificate["g49"]["essential"]:
            targets.add(tuple(sorted(placed[v] for v in triangles[triangle_index])))
    points = sorted(union)
    rows = [row(p) for p in points]
    labels = {p: index for index, p in enumerate(points)}
    labelled_targets = sorted(tuple(labels[p] for p in triangle) for triangle in targets)
    pins = [labels[p] for p in g40[:2]]
    edges = exact_edges(rows)
    require((len(points), len(edges), len(labelled_targets), pins) == (1167, 6472, 321, [804, 820]), "intermediate layer inventory")
    return points, rows, edges, labelled_targets, pins


def expected_cnf(n, edges, triangles, pins):
    for vertex in range(n):
        yield tuple(4 * vertex + colour + 1 for colour in range(4))
        for a, b in combinations(range(4), 2):
            yield (-(4 * vertex + a + 1), -(4 * vertex + b + 1))
    for u, v in edges:
        for colour in range(4):
            yield (-(4 * u + colour + 1), -(4 * v + colour + 1))
    yield (4 * pins[0] + 1,)
    yield (4 * pins[1] + 2,)
    for triangle in triangles:
        for colour in range(4):
            yield tuple(-(4 * vertex + colour + 1) for vertex in triangle)


def check_cnf(path: Path, n: int, edges, triangles, pins):
    clauses = []
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        header = handle.readline()
        digest.update(header)
        words = header.split()
        require(words[:2] == [b"p", b"cnf"] and list(map(int, words[2:])) == [4 * n, 34139], "CNF header")
        for wanted in expected_cnf(n, edges, triangles, pins):
            line = handle.readline()
            require(line, "truncated CNF")
            digest.update(line)
            got = tuple(map(int, line.split()))
            require(got == wanted + (0,), f"CNF clause {len(clauses) + 1}")
            clauses.append(wanted)
        require(not handle.read(1) and len(clauses) == 34139, "CNF length")
    require(digest.hexdigest() == "0755271bc61f32262c16eba4b34f7fbe7e43f5a25ad1f13e79fe900c4b5e5df8", "CNF identity")
    return clauses


def check_lrat(path: Path, clauses, variables: int):
    database = {index: clause for index, clause in enumerate(clauses, 1)}
    last_addition = len(clauses)
    additions = deletions = hint_steps = 0
    empty = False
    with path.open() as proof:
        for line_number, line in enumerate(proof, 1):
            tokens = line.split()
            require(tokens, "empty LRAT line")
            identifier = int(tokens[0])
            if len(tokens) > 1 and tokens[1] == "d":
                ids = list(map(int, tokens[2:]))
                require(ids and ids[-1] == 0 and 0 not in ids[:-1], "LRAT deletion syntax")
                for clause_id in ids[:-1]:
                    require(clause_id in database, "LRAT absent deletion")
                    del database[clause_id]
                    deletions += 1
                continue
            require(not empty and identifier > last_addition, "LRAT addition order")
            values = list(map(int, tokens[1:]))
            require(0 in values, "LRAT clause terminator")
            split = values.index(0)
            clause, hints = values[:split], values[split + 1 :]
            require(hints and hints[-1] == 0 and all(hint > 0 for hint in hints[:-1]), "positive RUP hints required")
            require(len(clause) == len(set(clause)) and all(0 < abs(lit) <= variables for lit in clause), "LRAT clause")
            assignment = {}
            for literal in clause:
                variable = abs(literal)
                require(variable not in assignment, "LRAT tautology")
                assignment[variable] = literal < 0  # negate the candidate clause
            conflict = False
            for hint in hints[:-1]:
                require(hint in database and not conflict, "LRAT missing/trailing hint")
                unresolved = []
                for literal in database[hint]:
                    value = assignment.get(abs(literal))
                    require(value is None or value != (literal > 0), "LRAT satisfied hint")
                    if value is None:
                        unresolved.append(literal)
                require(len(unresolved) <= 1, f"LRAT nonunit hint at line {line_number}")
                if not unresolved:
                    conflict = True
                else:
                    literal = unresolved[0]
                    assignment[abs(literal)] = literal > 0
                hint_steps += 1
            require(conflict, f"LRAT lacks conflict at line {line_number}")
            database[identifier] = tuple(clause)
            last_addition = identifier
            additions += 1
            empty = not clause
    require(empty and (additions, deletions, hint_steps) == (22714, 56826, 1188643), "LRAT receipt")
    return additions, deletions, hint_steps


def check_deletion_words(certificate, n, edges, selected, pins):
    require(certificate["vertices"] == n and certificate["edges"] == len(edges), "certificate graph metadata")
    require(certificate["pins"] == pins and len(selected) == 20, "certificate pins/support")
    words = certificate["deletion_colourings"]
    require(len(words) == 20, "deletion witness count")
    for omitted, word in enumerate(words):
        require(len(word) == n and set(word) <= set("0123"), "deletion word format")
        require(word[pins[0]] == "0" and word[pins[1]] == "1", "deletion word pins")
        require(all(word[u] != word[v] for u, v in edges), "deletion word edge")
        for index, triangle in enumerate(selected):
            require((len({word[v] for v in triangle}) == 1) == (index == omitted), "deletion word support")


def point_digest(points) -> str:
    digest = hashlib.sha256()
    for p in sorted(points):
        encoded = [[[value.numerator, value.denominator] for value in axis] for axis in p]
        digest.update(json.dumps(encoded, separators=(",", ":")).encode() + b"\n")
    return digest.hexdigest()


def completed_construction(layer, selected, t375_points):
    half = set(layer)
    for triangle in selected:
        targets = [layer[v] for v in triangle]
        mapping = frame(t375_points[0], t375_points[1], targets[0], targets[1], 432)
        if apply(mapping, t375_points[2]) != targets[2]:
            mapping = frame(t375_points[0], t375_points[1], targets[0], targets[1], 432, True)
        placed = [apply(mapping, p) for p in t375_points]
        require(placed[:3] == targets and len(set(placed)) == 375, "T375 placement")
        half.update(placed)
    half = sorted(half)
    require(len(half) == 4293, "half order")
    rotation = scalar(F(119, 128)), (F(0), F(0), F(0), F(0), F(3, 128), F(0), F(0), F(0))
    require(norm(rotation) == ONE, "spindle rotation norm")
    origin = point((0, 0, 0, 0))
    rotated = {complex_mul(rotation, p) for p in half}
    require(set(half) & rotated == {origin}, "half intersection")
    full = set(half) | rotated
    require(len(full) == 8585, "full order")
    return half, full, rotation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--cnf", required=True, type=Path)
    parser.add_argument("--lrat", required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    target = source / "hadwiger_nelson_ei_global_interfaces"
    t375 = source / "hadwiger_nelson_small_triangle_forcer375"
    ei = source / "hadwiger_nelson_ei_interface_minima"
    verify_manifest(target, TARGET_MANIFEST, 14)
    verify_manifest(t375, T375_MANIFEST, 16)
    verify_manifest(ei, EI_MANIFEST, 14)

    t375_points, _, t375_edges = reconstruct_t375(t375)
    dsatur_nodes = t375_dsatur(t375_edges)
    layer, _, edges, available, pins = reconstruct_layer(ei)
    certificate = read_json(target / "certificate.json")
    selected = list(map(tuple, certificate["selected_triangles"]))
    require(selected == sorted(set(selected)) and all(triangle in available for triangle in selected), "selected triangles")
    check_deletion_words(certificate, len(layer), edges, selected, pins)
    clauses = check_cnf(args.cnf.resolve(), len(layer), edges, selected, pins)
    additions, deletions, hints = check_lrat(args.lrat.resolve(), clauses, 4 * len(layer))
    half, full, rotation = completed_construction(layer, selected, t375_points)
    require(distance(layer[pins[0]], layer[pins[1]]) == scalar(9216), "outer endpoint distance")
    require(distance(layer[pins[1]], complex_mul(rotation, layer[pins[1]])) == scalar(1296), "spindle edge")
    half_hash = point_digest(half)
    full_hash = point_digest(full)
    require(half_hash == "42d27b5f427335eb0ccc1bec96a3142d79675ad83e385ab632c8159ce7a7af21", "half hash")
    require(full_hash == "a03d0f3c06913a498b948e34360b9c7e13fcd06404c59f0dbf3ae560e579e04e", "full hash")
    result = {
        "status": "INDEPENDENT_8585_POINT_NONFOURCOLOURABILITY_VERIFIED",
        "source_commit": "cf662bafba272382968b3128a68a8173e3eb7a6e",
        "intermediate_vertices": len(layer),
        "intermediate_unit_edges": len(edges),
        "available_triangles": len(available),
        "selected_triangles": len(selected),
        "deletion_witnesses": len(certificate["deletion_colourings"]),
        "cnf_variables": 4 * len(layer),
        "cnf_clauses": len(clauses),
        "lrat_additions": additions,
        "lrat_deletions": deletions,
        "lrat_hint_steps": hints,
        "t375_vertices": len(t375_points),
        "t375_unit_edges": len(t375_edges),
        "independent_t375_dsatur_nodes": dsatur_nodes,
        "half_vertices": len(half),
        "full_vertices": len(full),
        "half_point_sha256": half_hash,
        "full_point_sha256": full_hash,
        "record_improvement": False,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
