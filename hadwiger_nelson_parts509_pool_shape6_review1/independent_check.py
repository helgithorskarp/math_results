#!/usr/bin/env python3
"""Independent audit and alternative CNF for the Parts pool a=6 closure.

No module from the reviewed contribution is imported.  Original Parts
coordinates are read from the integer scale-96 table, completion points are
parsed as Fractions, and all selected-pool unit edges are reconstructed.
The alternative master uses one-hot counting automata and direct degree
clauses instead of the reviewed totalizer encoding.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_parts509_pool_shape6_verified"
RUN_HASHES = {
    "colourings.jsonl": "cccc3f4effc5880387017bc426b6d221bb597ad85bcdbe2d04f0ba5f639c3816",
    "master.cnf": "b171d62e559a4ea78a368f0c5fd842eaf4895cf7a238bcad252d57bf70ad2eec",
    "master.drat": "499cfc2907322d196c6acec628486884124e0d93cde747fd7eabd26ddc99eade",
}
SOURCE_HASHES = {
    "points": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "completion": "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "pool": "fd636275fccdd84266655ba9ada22412f7d2aef66a0ad66f6ee5bd738570939e",
    "interface": "a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637",
    "killing": "23c440f74f78a8f6adf675de4e5f284cda4d5b1fe1e353eac48efff381b46288",
    "hints": "c847c98c15bbe847a2a94bdb8c79bfbe3b1b80ed85d8cfc711c28c4d13d0ac53",
}
PRIMES = (3, 5, 11)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    answer = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def field_multiply(left, right):
    """Multiply in the bit-mask basis of Q(sqrt(3),sqrt(5),sqrt(11))."""
    answer = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            coefficient = a * b
            overlap = i & j
            for bit, prime in enumerate(PRIMES):
                if overlap & (1 << bit):
                    coefficient *= prime
            answer[i ^ j] += coefficient
    return tuple(answer)


def squared_distance(first, second):
    dx = tuple(a - b for a, b in zip(first[0], second[0], strict=True))
    dy = tuple(a - b for a, b in zip(first[1], second[1], strict=True))
    sx = field_multiply(dx, dx)
    sy = field_multiply(dy, dy)
    return tuple(a + b for a, b in zip(sx, sy, strict=True))


def read_geometry():
    originals_path = (REPOSITORY / "hadwiger_nelson_parts509_completion_census_degree9" /
                      "points.tsv")
    completion_path = (REPOSITORY / "hadwiger_nelson_parts509_swap_closure" /
                       "completion_points.json")
    pool_path = (REPOSITORY / "hadwiger_nelson_parts509_s_replacement_budget" /
                 "pool_S.json")
    require(digest(originals_path) == SOURCE_HASHES["points"], "original point hash")
    require(digest(completion_path) == SOURCE_HASHES["completion"], "completion hash")
    require(digest(pool_path) == SOURCE_HASHES["pool"], "pool hash")

    originals = []
    for line in originals_path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        require(len(row) == 16, ("point width", len(originals)))
        originals.append((row[:8], row[8:]))
    require(len(originals) == 509, ("original point count", len(originals)))

    raw_completion = json.loads(completion_path.read_text())
    completion = []
    denominator = 96
    for record in raw_completion["points"]:
        point = (tuple(Fraction(x) for x in record["x"]),
                 tuple(Fraction(y) for y in record["y"]))
        require(len(point[0]) == len(point[1]) == 8, "completion point width")
        for coefficient in point[0] + point[1]:
            denominator = lcm(denominator, coefficient.denominator)
        completion.append(point)
    require(len(completion) == 1158, ("completion count", len(completion)))

    points = [
        (tuple((denominator // 96) * x for x in point[0]),
         tuple((denominator // 96) * y for y in point[1]))
        for point in originals
    ]
    points.extend(
        (tuple(int(denominator * x) for x in point[0]),
         tuple(int(denominator * y) for y in point[1]))
        for point in completion
    )

    pool = json.loads(pool_path.read_text())
    universe = tuple(sorted(pool["W_S"]))
    require(universe[:135] == tuple(range(374, 509)), "S indexing")
    require(universe[135:] == tuple(sorted(pool["Q5"])), "Q5 indexing")
    require(len(universe) == 303 and len(universe[135:]) == 168, "pool sizes")
    vertices = tuple(range(374)) + universe
    require(len(vertices) == len(set(vertices)) == 677, "selected vertex labels")
    require(len({points[vertex] for vertex in vertices}) == 677, "coordinate collision")

    target = (denominator * denominator,) + (0,) * 7
    edges = tuple(
        (first, second)
        for first, second in combinations(vertices, 2)
        if squared_distance(points[first], points[second]) == target
    )
    require(denominator == 288 and len(edges) == 3400,
            ("geometry census", denominator, len(edges)))
    edge_text = "".join(f"{a},{b}\n" for a, b in edges).encode("ascii")
    require(sha256(edge_text).hexdigest() ==
            "64a0f52154cb05b657a320c16569316cd1cba90748ed6dff71d4f45ca862b550",
            "edge stream hash")
    return denominator, points, vertices, universe, edges


def read_killing_family():
    path = TARGET / "killing_clauses.cnf"
    hints_path = TARGET / "interface_hints.json"
    require(digest(path) == SOURCE_HASHES["killing"], "killing instance hash")
    require(digest(hints_path) == SOURCE_HASHES["hints"], "hint hash")
    with path.open(encoding="ascii") as stream:
        require(stream.readline().split() == ["p", "cnf", "303", "6777"],
                "killing DIMACS header")
        rows = []
        for line in stream:
            clause = tuple(map(int, line.split()))
            require(clause and clause[-1] == 0, "unterminated killing clause")
            clause = clause[:-1]
            require(clause and clause == tuple(sorted(set(clause))) and
                    all(1 <= literal <= 303 for literal in clause),
                    ("bad killing clause", len(rows)))
            rows.append(clause)
    require(len(rows) == len(set(rows)) == 6777, "killing family size")
    hints = json.loads(hints_path.read_text())
    require(len(hints) == 6777 and all(type(x) is int for x in hints), "hint list")
    return tuple(rows), tuple(hints)


def check_positive_colourings(work, universe, edges, killing, hints):
    interface_path = (REPOSITORY / "hadwiger_nelson_parts509_interface_lemma" /
                      "interface_L.json")
    require(digest(interface_path) == SOURCE_HASHES["interface"], "interface hash")
    left_rows = tuple(
        record["witness_colouring_L"]
        for record in json.loads(interface_path.read_text())["classes"]
    )
    require(len(left_rows) == 20 and
            all(len(row) == 374 and set(row) <= set("0123") for row in left_rows),
            "left coloring dimensions")
    left_edges = tuple((a, b) for a, b in edges if b < 374)
    require(all(all(row[a] != row[b] for a, b in left_edges) for row in left_rows),
            "improper left coloring")

    position = {vertex: i for i, vertex in enumerate(universe)}
    inner = tuple((position[a], position[b]) for a, b in edges
                  if a in position and b in position)
    cross = tuple((a, position[b]) if a < 374 else (b, position[a])
                  for a, b in edges if (a < 374) != (b < 374))
    cache_path = work / "colourings.jsonl"
    require(digest(cache_path) == RUN_HASHES["colourings.jsonl"], "color cache hash")
    seen = set()
    with cache_path.open(encoding="ascii") as stream:
        for line in stream:
            record = json.loads(line)
            index, interface, colors = record["i"], record["p"], record["c"]
            require(type(index) is int and 0 <= index < len(killing) and index not in seen,
                    ("coloring index", index))
            require(type(interface) is int and interface == hints[index] and
                    0 <= interface < len(left_rows), ("interface hint", index))
            require(len(colors) == 303 and set(colors) <= set(".0123"),
                    ("coloring alphabet", index))
            require(tuple(i + 1 for i, color in enumerate(colors) if color == ".") ==
                    killing[index], ("deleted set", index))
            require(all(colors[a] == "." or colors[b] == "." or colors[a] != colors[b]
                        for a, b in inner), ("inner edge", index))
            left = left_rows[interface]
            require(all(colors[u] == "." or colors[u] != left[l] for l, u in cross),
                    ("cross edge", index))
            seen.add(index)
    require(seen == set(range(6777)), "incomplete coloring cache")
    return len(left_rows), len(inner), len(cross)


def parse_target_master(work, killing):
    master = work / "master.cnf"
    proof = work / "master.drat"
    require(digest(master) == RUN_HASHES["master.cnf"], "target master hash")
    require(digest(proof) == RUN_HASHES["master.drat"], "target proof hash")
    require(proof.stat().st_size == 57_623_889, "target proof size")
    with master.open(encoding="ascii") as stream:
        require(stream.readline().split() == ["p", "cnf", "4588", "26660"],
                "target master header")
        for expected in killing:
            actual = tuple(map(int, stream.readline().split()))
            require(actual == expected + (0,), "target killing prefix")
    result = json.loads((work / "result.json").read_text())
    require(result["status"] == "a=6 COLOURING COVER AND DRAT VERIFIED",
            "target reproduction status")


def exactly_one(variables):
    return [list(variables)] + [[-a, -b] for a, b in combinations(variables, 2)]


def counting_automaton(literals, wanted, next_variable):
    """One-hot capped exact-count BDD, distinct from the target totalizer."""
    cap = wanted + 1
    rows = []
    clauses = []
    meanings = {}
    for prefix in range(len(literals) + 1):
        row = []
        for count in range(min(prefix, cap) + 1):
            next_variable += 1
            row.append(next_variable)
            meanings[next_variable] = (prefix, count)
        rows.append(tuple(row))
        clauses.extend(exactly_one(row))
    for prefix, literal in enumerate(literals):
        for count, state in enumerate(rows[prefix]):
            same = rows[prefix + 1][count]
            incremented = rows[prefix + 1][min(count + 1, cap)]
            clauses.append([-state, literal, same])
            clauses.append([-state, -literal, incremented])
    clauses.append([rows[-1][wanted]])
    return clauses, next_variable, meanings


def clause_true(clause, assignment):
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


def unit_conflict(clauses, initial):
    assignment = dict(initial)
    while True:
        changed = False
        for clause in clauses:
            if any(abs(literal) in assignment and
                   assignment[abs(literal)] == (literal > 0) for literal in clause):
                continue
            unknown = [literal for literal in clause if abs(literal) not in assignment]
            if not unknown:
                return True
            if len(unknown) == 1:
                literal = unknown[0]
                variable, value = abs(literal), literal > 0
                if variable in assignment and assignment[variable] != value:
                    return True
                if variable not in assignment:
                    assignment[variable] = value
                    changed = True
        if not changed:
            return False


def check_small_automata():
    checks = 0
    for size in range(1, 8):
        for wanted in range(size + 1):
            inputs = tuple(range(1, size + 1))
            clauses, _, meanings = counting_automaton(inputs, wanted, size)
            for bits in product((False, True), repeat=size):
                checks += 1
                assignment = dict(zip(inputs, bits, strict=True))
                if sum(bits) == wanted:
                    for variable, (prefix, count) in meanings.items():
                        assignment[variable] = count == min(sum(bits[:prefix]), wanted + 1)
                    require(all(clause_true(clause, assignment) for clause in clauses),
                            ("valid BDD assignment rejected", size, wanted, bits))
                else:
                    require(unit_conflict(clauses, assignment),
                            ("invalid count not refuted", size, wanted, bits))
    require(checks == 1792, ("small automaton checks", checks))
    return checks


def alternative_master(universe, edges, killing):
    S, Q5 = universe[:135], universe[135:]
    identifiers = {vertex: i + 1 for i, vertex in enumerate(universe)}
    clauses = [list(clause) for clause in killing]
    next_variable = len(universe)

    rows, next_variable, _ = counting_automaton(
        tuple(-identifiers[vertex] for vertex in S), 7, next_variable)
    clauses.extend(rows)
    rows, next_variable, _ = counting_automaton(
        tuple(identifiers[vertex] for vertex in Q5), 6, next_variable)
    clauses.extend(rows)

    selected = set(universe)
    left = set(range(374))
    adjacency = {vertex: set() for vertex in tuple(range(374)) + universe}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    degree_histogram = {}
    degree_clauses = 0
    for vertex in Q5:
        need = 4 - len(adjacency[vertex] & left)
        neighbors = tuple(sorted(adjacency[vertex] & selected))
        degree_histogram[(len(neighbors), need)] = degree_histogram.get(
            (len(neighbors), need), 0) + 1
        guard = -identifiers[vertex]
        if need <= 0:
            continue
        if need > len(neighbors):
            clauses.append([guard])
            degree_clauses += 1
            continue
        width = len(neighbors) - need + 1
        for subset in combinations(neighbors, width):
            clauses.append([guard] + [identifiers[other] for other in subset])
            degree_clauses += 1
    return next_variable, clauses, degree_clauses, tuple(sorted(degree_histogram.items()))


def dimacs(variables, clauses):
    return (f"p cnf {variables} {len(clauses)}\n" +
            "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)).encode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    controls = check_small_automata()
    denominator, _, _, universe, edges = read_geometry()
    killing, hints = read_killing_family()
    interfaces, inner_edges, cross_edges = check_positive_colourings(
        args.work, universe, edges, killing, hints)
    parse_target_master(args.work, killing)

    variables, clauses, degree_clauses, degree_histogram = alternative_master(
        universe, edges, killing)
    encoded = dimacs(variables, clauses)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded)

    print("PASS pinned inputs and independently reconstructed exact scale-288 geometry")
    print(f"PASS selected pool: points=677 unit_edges={len(edges)} S=135 Q5=168")
    print(f"PASS positive cover: killing_sets={len(killing)} colourings=6777 L_interfaces={interfaces}")
    print(f"PASS coloring edge partition: inner_U={inner_edges} cross_LU={cross_edges}")
    print("PASS target reproduction artifacts: master CNF and 57623889-byte DRAT hashes match")
    print(f"PASS alternative one-hot counter controls: assignment_checks={controls}")
    print(f"PASS alternative direct-degree clauses={degree_clauses} patterns={degree_histogram}")
    print(f"ALT_CNF variables={variables} clauses={len(clauses)} bytes={len(encoded)}")
    print(f"ALT_CNF sha256={sha256(encoded).hexdigest()}")
    print("SCOPE degree-admissible a=6 cover; unconditional result additionally imports a=5 closure")


if __name__ == "__main__":
    main()
