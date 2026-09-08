#!/usr/bin/env python3
"""Independent finite audit for Discovery Net h3931.

This program imports no code from the reviewed package.  It reconstructs the
entire 4-by-4 capacity recurrence using a separately organized enumeration,
checks every committed extremal witness directly as a graph, and verifies the
unique equality structure at (omega, alpha) = (4, 4).
"""

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


SOURCE_COMMIT = "e7d5932b57e804bf1f2dcb00f89360af0f76fa2e"
MANIFEST_SHA256 = "164b68e641bc1401a76fcd61b44191b52075b86e493ccfcc6c83d3e955c3daf3"
EXPECTED_TABLE = [
    [1, 2, 3, 4],
    [2, 5, 7, 10],
    [3, 7, 11, 16],
    [4, 10, 16, 25],
]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest(source):
    manifest = source / "SHA256SUMS"
    need(sha256(manifest) == MANIFEST_SHA256, "manifest identity")
    names = []
    for line in manifest.read_text().splitlines():
        wanted, name = line.split("  ", 1)
        need(name not in names and "/" not in name and name not in (".", ".."),
             "manifest path")
        need(sha256(source / name) == wanted, "source hash " + name)
        names.append(name)
    need(len(names) == 17, "manifest entry count")
    return names


def cycle_sequences(cap, distance):
    """Enumerate positive C5 weights satisfying one cyclic capacity family."""
    edges = {tuple(sorted((i, (i + distance) % 5))) for i in range(5)}
    answer = []

    def extend(prefix):
        i = len(prefix)
        if i == 5:
            if all(prefix[u] + prefix[v] <= cap for u, v in edges):
                answer.append(tuple(prefix))
            return
        for value in range(1, cap):
            if all(v != i or u >= i or prefix[u] + value <= cap
                   for u, v in edges):
                extend(prefix + [value])

    extend([])
    return answer


def reconstruct_table():
    bounds = {}
    rows = []
    all_population = 0
    for total in range(2, 9):
        for a in range(1, 5):
            b = total - a
            if not 1 <= b <= 4:
                continue
            if (a, b) == (1, 1):
                ratio = Fraction(0)
                ratio_pairs = []
                perfect = 0
            else:
                scored = [
                    (Fraction(bounds[p, q], p * q), p, q)
                    for p in range(1, a + 1)
                    for q in range(1, b + 1)
                    if (p, q) != (a, b)
                ]
                ratio = max(value for value, _, _ in scored)
                ratio_pairs = [(p, q) for value, p, q in scored
                               if value == ratio]
                perfect = int(a * b * ratio)

            p_vectors = cycle_sequences(a, 1)
            q_vectors = cycle_sequences(b, 2)
            candidates = []
            best_cycle = 0
            maximizers = []
            for p_vector in p_vectors:
                for q_vector in q_vectors:
                    value = sum(bounds[p_vector[i], q_vector[i]]
                                for i in range(5))
                    candidates.append((p_vector, q_vector))
                    if value > best_cycle:
                        best_cycle = value
                        maximizers = [(p_vector, q_vector)]
                    elif value == best_cycle:
                        maximizers.append((p_vector, q_vector))
            upper = max(1 if (a, b) == (1, 1) else 0,
                        perfect, best_cycle)
            bounds[a, b] = upper
            all_population += len(candidates)
            rows.append({
                "omega": a,
                "alpha": b,
                "upper": upper,
                "perfect_upper": perfect,
                "c5_upper": best_cycle,
                "c5_population_count": len(candidates),
                "rho": [ratio.numerator, ratio.denominator],
                "rho_attainers": [[p, q] for p, q in ratio_pairs],
                "c5_maximizers": [[list(p), list(q)] for p, q in maximizers],
            })
    return bounds, rows, all_population


def graph_from_hex(order, raw):
    word = int(raw, 16)
    need(word < 1 << (order * (order - 1) // 2), "unused witness high bit")
    adjacency = [0] * order
    for index, (u, v) in enumerate(combinations(range(order), 2)):
        if word >> index & 1:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return adjacency


def maximum_clique(adjacency):
    """Exact bit-set branch and bound, distinct from the source subset audit."""
    best = 0
    calls = 0

    def search(candidates, size):
        nonlocal best, calls
        calls += 1
        if size + candidates.bit_count() <= best:
            return
        while candidates:
            if size + candidates.bit_count() <= best:
                return
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            search(candidates & adjacency[vertex], size + 1)
        best = max(best, size)

    search((1 << len(adjacency)) - 1, 0)
    return best, calls


def complement(adjacency):
    mask = (1 << len(adjacency)) - 1
    return [mask ^ (1 << vertex) ^ neighbours
            for vertex, neighbours in enumerate(adjacency)]


def is_path_on_five(adjacency, vertices):
    chosen = sum(1 << vertex for vertex in vertices)
    degrees = [(adjacency[vertex] & chosen).bit_count() for vertex in vertices]
    if sorted(degrees) != [1, 1, 2, 2, 2]:
        return False
    reached = 0
    frontier = 1 << vertices[0]
    while frontier:
        reached |= frontier
        neighbours = 0
        scan = frontier
        while scan:
            bit = scan & -scan
            scan ^= bit
            neighbours |= adjacency[bit.bit_length() - 1]
        frontier = neighbours & chosen & ~reached
    return reached == chosen


def audit_five_words():
    pairs = list(combinations(range(5), 2))
    path_words = complement_words = 0
    for word in range(1 << 10):
        adjacency = [0] * 5
        for index, (u, v) in enumerate(pairs):
            if word >> index & 1:
                adjacency[u] |= 1 << v
                adjacency[v] |= 1 << u
        path_words += is_path_on_five(adjacency, range(5))
        complement_words += is_path_on_five(complement(adjacency), range(5))
    need(path_words == complement_words == 60, "five-word classification")
    return path_words + complement_words


def expected_c5_c5():
    adjacency = [0] * 25
    for u, v in combinations(range(25), 2):
        outer_u, inner_u = divmod(u, 5)
        outer_v, inner_v = divmod(v, 5)
        if outer_u == outer_v:
            edge = (inner_u - inner_v) % 5 in (1, 4)
        else:
            edge = (outer_u - outer_v) % 5 in (1, 4)
        if edge:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return adjacency


def adjacency_word(adjacency):
    return sum(1 << index
               for index, (u, v) in enumerate(combinations(range(len(adjacency)), 2))
               if adjacency[u] >> v & 1)


def audit_five_vertex_equality_base():
    """Exhaust all graphs on five labels with omega,alpha <= 2."""
    pairs = list(combinations(range(5), 2))
    survivors = 0
    for word in range(1 << len(pairs)):
        adjacency = graph_from_hex(5, format(word, "x"))
        omega, _ = maximum_clique(adjacency)
        alpha, _ = maximum_clique(complement(adjacency))
        if omega <= 2 and alpha <= 2:
            survivors += 1
            need(all(neighbours.bit_count() == 2 for neighbours in adjacency),
                 "non-cycle (2,2) equality graph")
            need(is_path_on_five(adjacency, (0, 1, 2, 3, 4)) is False,
                 "C5 mistaken for P5")
    need(survivors == 12, "labeled C5 population")
    return survivors


def audit_witnesses(source, bounds):
    document = json.loads((source / "WITNESSES.json").read_text())
    graphs = document["graphs"]
    need(document["bit_order"] == "low bits for lexicographic unordered pairs",
         "witness bit convention")
    need(len(graphs) == 16, "witness count")
    graph_by_cap = {(graph["omega"], graph["alpha"]): graph for graph in graphs}
    need(len(graph_by_cap) == 16, "duplicate witness cap")
    five_sets = 0
    clique_calls = 0
    for cap, wanted_order in bounds.items():
        graph = graph_by_cap[cap]
        need(graph["n"] == wanted_order, "witness order")
        adjacency = graph_from_hex(graph["n"], graph["red_bits_hex"])
        omega, calls = maximum_clique(adjacency)
        alpha, cocalls = maximum_clique(complement(adjacency))
        clique_calls += calls + cocalls
        need((omega, alpha) == cap, "witness exact extrema")
        for vertices in combinations(range(graph["n"]), 5):
            need(not is_path_on_five(adjacency, vertices), "witness induced P5")
            need(not is_path_on_five(complement(adjacency), vertices),
                 "witness induced complement-P5")
            five_sets += 1

    top = graph_by_cap[4, 4]
    actual = graph_from_hex(25, top["red_bits_hex"])
    expected = expected_c5_c5()
    need(adjacency_word(actual) == adjacency_word(expected),
         "top witness is not the literal C5[C5]")
    need(sum(x.bit_count() for x in actual) // 2 == 150, "top edge count")
    need({x.bit_count() for x in actual} == {12}, "top degree")
    return five_sets, clique_calls


def compare_table(source_rows, independent_rows):
    need(len(source_rows) == len(independent_rows) == 16, "table row count")
    fields = ("omega", "alpha", "upper", "perfect_upper", "c5_upper",
              "c5_population_count", "rho", "rho_attainers")
    for source, independent in zip(source_rows, independent_rows):
        for field in fields:
            need(source[field] == independent[field], "table field " + field)
        source_maximizers = {
            (tuple(pair[0]), tuple(pair[1])) for pair in source["c5_maximizers"]
        }
        independent_maximizers = {
            (tuple(pair[0]), tuple(pair[1]))
            for pair in independent["c5_maximizers"]
        }
        need(source_maximizers == independent_maximizers,
             "cycle maximizer set")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path,
                        help="reviewed ramsey_r55_path_complement_core_exclusion directory")
    args = parser.parse_args()
    source = args.source.resolve()
    names = verify_manifest(source)
    table = json.loads((source / "TABLE.json").read_text())
    bounds, rows, population = reconstruct_table()
    compare_table(table["rows"], rows)
    need(population == table["c5_population_checks"] == 4761,
         "total C5 population")
    matrix = [[bounds[a, b] for b in range(1, 5)] for a in range(1, 5)]
    need(matrix == EXPECTED_TABLE, "capacity matrix")
    need(table["max_good_order"] == bounds[4, 4] == 25,
         "top capacity")
    need(table["excluded_core_order"] == 26, "excluded core order")
    top_row = next(row for row in rows
                   if (row["omega"], row["alpha"]) == (4, 4))
    need(top_row["perfect_upper"] == 21, "perfect top bound")
    need(top_row["c5_maximizers"] == [
        [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2]]
    ], "unique top C5 weight vector")
    labeled_c5 = audit_five_vertex_equality_base()
    five_words = audit_five_words()
    witness_five_sets, clique_calls = audit_witnesses(source, bounds)
    result = {
        "status": "INDEPENDENT_H3931_CORE_EXCLUSION_VERIFIED",
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_manifest_sha256": MANIFEST_SHA256,
        "manifest_entries": len(names),
        "capacity_table": matrix,
        "c5_cap_rows_enumerated": population,
        "top_perfect_upper": top_row["perfect_upper"],
        "top_c5_upper": top_row["c5_upper"],
        "top_weight_vector_unique": True,
        "labeled_order5_equality_graphs": labeled_c5,
        "order5_equality_isomorphism_types": 1,
        "five_vertex_words_classified": 1024,
        "path_or_complement_path_words": five_words,
        "witnesses_checked": 16,
        "witness_five_sets_checked": witness_five_sets,
        "independent_clique_search_calls": clique_calls,
        "exact_class_maximum": bounds[4, 4],
        "excluded_core_order": bounds[4, 4] + 1,
        "disjoint_patterns_forced_in_good43": 4,
        "solver_calls": 0,
        "good43_found": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
