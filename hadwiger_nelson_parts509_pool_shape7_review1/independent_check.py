#!/usr/bin/env python3
"""Independent review checker and alternative CNF for the Parts a=7 closure.

The reviewed verifier and its cardinality encoder are never imported.  Exact
geometry is obtained from the already accepted a=6 independent checker, whose
source hash is pinned.  This checker parses the compact positive cover,
optionally checks every regenerated colouring, and emits a different master:
capped unary prefix counters plus elementary guarded subset degree clauses.
"""

import argparse
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_parts509_pool_shape7_verified"
GEOMETRY_SOURCE = (REPOSITORY /
                   "hadwiger_nelson_parts509_pool_shape6_review1" /
                   "independent_check.py")
SOURCE_HASHES = {
    "geometry_checker": "a3f2de1702cbd55650e77ae97759294ff2915d183e8aec6944adb2813037d416",
    "interface": "a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637",
    "killing": "a7bc0aadf72becb81cc66000fa5d00135ddbfa95fcb375f47d36c08ce4a80ade",
    "hints": "c539a762dcfabaae7599800eb72d5e9143033482ae2eaca77773f9da5211cc5b",
    "target_verify": "10734e621c6a06b2dfe2f382c6e7c1ec954a3e303da479bbe1cf16c478498372",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    answer = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def load_geometry():
    require(digest(GEOMETRY_SOURCE) == SOURCE_HASHES["geometry_checker"],
            "accepted geometry checker hash")
    spec = importlib.util.spec_from_file_location("accepted_a6_geometry",
                                                  GEOMETRY_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    denominator, points, vertices, universe, edges = module.read_geometry()
    require(denominator == 288, ("geometry denominator", denominator))
    require(len(vertices) == 677 and len(universe) == 303 and len(edges) == 3400,
            "geometry census")
    return points, vertices, universe, edges


def read_killing_family():
    path = TARGET / "killing_clauses.cnf"
    hints_path = TARGET / "interface_hints.json"
    verify_path = TARGET / "verify.py"
    require(digest(path) == SOURCE_HASHES["killing"], "killing instance hash")
    require(digest(hints_path) == SOURCE_HASHES["hints"], "hint hash")
    require(digest(verify_path) == SOURCE_HASHES["target_verify"],
            "reviewed verifier hash")
    with path.open(encoding="ascii") as stream:
        require(stream.readline().split() == ["p", "cnf", "303", "12824"],
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
    require(len(rows) == len(set(rows)) == 12824, "killing family size")
    hints = json.loads(hints_path.read_text())
    require(len(hints) == len(rows) and
            all(type(value) is int and 0 <= value < 20 for value in hints),
            "hint dimensions")
    return tuple(rows), tuple(hints)


def check_positive_colourings(cache_path, universe, edges, killing, hints):
    interface_path = (REPOSITORY / "hadwiger_nelson_parts509_interface_lemma" /
                      "interface_L.json")
    require(digest(interface_path) == SOURCE_HASHES["interface"], "interface hash")
    left_rows = tuple(
        record["witness_colouring_L"]
        for record in json.loads(interface_path.read_text())["classes"]
    )
    require(len(left_rows) == 20 and
            all(len(row) == 374 and set(row) <= set("0123") for row in left_rows),
            "left colouring dimensions")
    left_edges = tuple((a, b) for a, b in edges if b < 374)
    require(all(all(row[a] != row[b] for a, b in left_edges)
                for row in left_rows), "improper left colouring")

    position = {vertex: i for i, vertex in enumerate(universe)}
    inner = tuple((position[a], position[b]) for a, b in edges
                  if a in position and b in position)
    cross = tuple((a, position[b]) if a < 374 else (b, position[a])
                  for a, b in edges if (a < 374) != (b < 374))
    seen = set()
    cache_hash = digest(cache_path)
    with cache_path.open(encoding="ascii") as stream:
        for line in stream:
            record = json.loads(line)
            index, interface, colors = record["i"], record["p"], record["c"]
            require(type(index) is int and 0 <= index < len(killing) and
                    index not in seen, ("colouring index", index))
            require(type(interface) is int and interface == hints[index],
                    ("interface hint", index))
            require(len(colors) == 303 and set(colors) <= set(".0123"),
                    ("colouring alphabet", index))
            require(tuple(i + 1 for i, color in enumerate(colors) if color == ".") ==
                    killing[index], ("deleted set", index))
            require(all(colors[a] == "." or colors[b] == "." or
                        colors[a] != colors[b] for a, b in inner),
                    ("inner edge", index))
            left = left_rows[interface]
            require(all(colors[u] == "." or colors[u] != left[l]
                        for l, u in cross), ("cross edge", index))
            seen.add(index)
    require(seen == set(range(len(killing))), "incomplete colouring cache")
    return len(left_rows), len(inner), len(cross), cache_hash


def check_target_replay(work, killing):
    master = work / "master.cnf"
    proof = work / "master.drat"
    require(digest(master) ==
            "ed3ae96f4a4d2664c69914520ae40c469440481c2c035b6551d0ecd2d3d4ece6",
            "target master hash")
    with master.open(encoding="ascii") as stream:
        require(stream.readline().split() == ["p", "cnf", "4641", "33387"],
                "target master header")
        for expected in killing:
            require(tuple(map(int, stream.readline().split())) == expected + (0,),
                    "target killing prefix")
    result = json.loads((work / "result.json").read_text())
    require(result["status"] == "a=7 COLOURING COVER AND DRAT VERIFIED",
            "target replay status")
    require(proof.is_file() and proof.stat().st_size > 0, "target proof missing")
    return {
        "master_sha256": digest(master),
        "proof_sha256": digest(proof),
        "proof_bytes": proof.stat().st_size,
        "solver_seconds": result["solver_seconds"],
        "checker_seconds": result["checker_seconds"],
        "total_seconds": result["total_seconds"],
    }


def negate(item):
    return not item if type(item) is bool else -item


def prefix_counter(literals, wanted, top):
    """Encode r[i,j] iff at least j of the first i literals hold.

    Only thresholds through wanted+1 are represented.  The four Tseitin
    clauses for r[i,j] <=> r[i-1,j] OR (x_i AND r[i-1,j-1]) make the meaning
    bidirectional; asserting wanted and rejecting wanted+1 enforces equality.
    """
    clauses = []
    previous = {0: True}
    meanings = {}

    def emit(*items):
        if any(type(item) is bool and item for item in items):
            return
        clauses.append([item for item in items if type(item) is not bool])

    for prefix, literal in enumerate(literals, 1):
        current = {0: True}
        for threshold in range(1, min(prefix, wanted + 1) + 1):
            top += 1
            state = top
            current[threshold] = state
            meanings[state] = (prefix, threshold)
            old_same = previous.get(threshold, False)
            old_lower = previous.get(threshold - 1, False)
            emit(negate(old_same), state)
            emit(-literal, negate(old_lower), state)
            emit(-state, old_same, literal)
            emit(-state, old_same, old_lower)
        previous = current
    emit(previous.get(wanted, False))
    emit(negate(previous.get(wanted + 1, False)))
    return top, clauses, meanings


def clause_true(clause, assignment):
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


def unit_conflict(clauses, initial):
    assignment = dict(initial)
    while True:
        changed = False
        for clause in clauses:
            if any(abs(literal) in assignment and
                   assignment[abs(literal)] == (literal > 0)
                   for literal in clause):
                continue
            unknown = [literal for literal in clause
                       if abs(literal) not in assignment]
            if not unknown:
                return True, assignment
            if len(unknown) == 1:
                literal = unknown[0]
                variable, value = abs(literal), literal > 0
                if variable in assignment and assignment[variable] != value:
                    return True, assignment
                if variable not in assignment:
                    assignment[variable] = value
                    changed = True
        if not changed:
            return False, assignment


def check_small_counters():
    tests = 0
    for size in range(1, 9):
        for wanted in range(size + 1):
            for sign in (-1, 1):
                literals = tuple(sign * (i + 1) for i in range(size))
                _, clauses, meanings = prefix_counter(literals, wanted, size)
                for bits in product((False, True), repeat=size):
                    tests += 1
                    assignment = {i + 1: bit for i, bit in enumerate(bits)}
                    count = sum(assignment[abs(literal)] == (literal > 0)
                                for literal in literals)
                    for variable, (prefix, threshold) in meanings.items():
                        partial = sum(assignment[abs(literal)] == (literal > 0)
                                      for literal in literals[:prefix])
                        assignment[variable] = partial >= threshold
                    require(all(clause_true(clause, assignment) for clause in clauses) ==
                            (count == wanted),
                            ("counter truth-table semantics", size, wanted, bits))
                    conflict, propagated = unit_conflict(
                        clauses, {i + 1: bit for i, bit in enumerate(bits)})
                    require(conflict == (count != wanted),
                            ("counter propagation", size, wanted, bits))
                    if not conflict:
                        require(propagated == assignment,
                                ("counter auxiliary forcing", size, wanted, bits))
    require(tests == 8192, ("counter control count", tests))
    return tests


def direct_degree_clauses(guard, neighbors, need):
    if need <= 0:
        return []
    if need > len(neighbors):
        return [[guard]]
    return [[guard] + list(subset)
            for subset in combinations(neighbors, len(neighbors) - need + 1)]


def check_small_degree_constraints():
    tests = 0
    for size in range(0, 9):
        neighbors = tuple(range(2, size + 2))
        for need in range(0, size + 2):
            clauses = direct_degree_clauses(-1, neighbors, need)
            for selected_guard in (False, True):
                for bits in product((False, True), repeat=size):
                    tests += 1
                    assignment = {1: selected_guard}
                    assignment.update({i + 2: bit for i, bit in enumerate(bits)})
                    actual = all(clause_true(clause, assignment) for clause in clauses)
                    expected = (not selected_guard) or sum(bits) >= need
                    require(actual == expected,
                            ("degree truth table", size, need, selected_guard, bits))
    require(tests == 9216, ("degree control count", tests))
    return tests


def build_master(universe, edges, killing):
    selected_id = {vertex: i + 1 for i, vertex in enumerate(universe)}
    clauses = [list(clause) for clause in killing]
    top = len(universe)
    top, counter_clauses, _ = prefix_counter(
        tuple(-selected_id[vertex] for vertex in universe[:135]), 8, top)
    clauses.extend(counter_clauses)
    top, counter_clauses, _ = prefix_counter(
        tuple(selected_id[vertex] for vertex in universe[135:]), 7, top)
    clauses.extend(counter_clauses)

    left = set(range(374))
    pool = set(universe)
    adjacency = {vertex: set() for vertex in left | pool}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    degree_clause_count = 0
    histogram = {}
    for vertex in universe[135:]:
        neighbors = tuple(sorted(adjacency[vertex] & pool))
        need = 4 - len(adjacency[vertex] & left)
        histogram[(len(neighbors), need)] = histogram.get(
            (len(neighbors), need), 0) + 1
        added = direct_degree_clauses(
            -selected_id[vertex],
            tuple(selected_id[neighbor] for neighbor in neighbors), need)
        clauses.extend(added)
        degree_clause_count += len(added)
    return top, clauses, degree_clause_count, tuple(sorted(histogram.items()))


def dimacs(variables, clauses):
    return (f"p cnf {variables} {len(clauses)}\n" +
            "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
            ).encode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--colourings", type=Path)
    parser.add_argument("--target-work", type=Path)
    args = parser.parse_args()
    require(__debug__, "run without Python optimization flags")

    counter_tests = check_small_counters()
    degree_tests = check_small_degree_constraints()
    _, _, universe, edges = load_geometry()
    killing, hints = read_killing_family()
    positive = None
    if args.colourings is not None:
        positive = check_positive_colourings(
            args.colourings, universe, edges, killing, hints)
    target_replay = None
    if args.target_work is not None:
        target_replay = check_target_replay(args.target_work, killing)

    variables, clauses, degree_count, histogram = build_master(
        universe, edges, killing)
    encoded = dimacs(variables, clauses)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(encoded)

    result = {
        "status": "INDEPENDENT INPUT AUDIT AND ALTERNATIVE CNF GENERATED",
        "points": 677,
        "unit_edges": len(edges),
        "pool_points": len(universe),
        "killing_clauses": len(killing),
        "counter_assignment_controls": counter_tests,
        "degree_assignment_controls": degree_tests,
        "degree_clauses": degree_count,
        "degree_histogram": [[list(pattern), count]
                             for pattern, count in histogram],
        "alternative_variables": variables,
        "alternative_clauses": len(clauses),
        "alternative_bytes": len(encoded),
        "alternative_sha256": sha256(encoded).hexdigest(),
        "positive_colourings": None if positive is None else {
            "count": len(killing),
            "left_interfaces": positive[0],
            "inner_pool_edges": positive[1],
            "cross_edges": positive[2],
            "cache_sha256": positive[3],
        },
        "target_replay": target_replay,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
