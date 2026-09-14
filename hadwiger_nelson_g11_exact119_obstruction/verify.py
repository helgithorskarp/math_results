#!/usr/bin/env python3
"""Independent exact verifier for the complete G_11 119-image obstruction.

The producer is not imported.  All graph, symmetry, quotient, cycle, rank and
coverage checks use Python integers and sets; no floating point or solver is
used.  The five-chromatic lower bound is an explicitly pinned predecessor.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE.parent / "hadwiger_nelson_g11_one_collision"
CHROMATIC = HERE.parent / "hadwiger_nelson_finite_abelian_lifts"
CERTIFICATE = HERE / "certificate.json"
EXPECTED = HERE / "EXPECTED.json"
Q = 11


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(point):
    return (point[0] * point[0] + point[1] * point[1]) % Q


def reconstruct_source():
    points = [(x, y) for x in range(Q) for y in range(Q)]
    unit_steps = {point for point in points if norm(point) == 1}
    edges = []
    for u, (x, y) in enumerate(points):
        for v in range(u + 1, len(points)):
            X, Y = points[v]
            if ((x - X) % Q, (y - Y) % Q) in unit_steps:
                edges.append((u, v))
    return points, edges


def orthogonal_matrices():
    answer = []
    for a, b, c, d in product(range(Q), repeat=4):
        if ((a * a + c * c) % Q == 1 and
                (b * b + d * d) % Q == 1 and
                (a * b + c * d) % Q == 0):
            answer.append((a, b, c, d))
    return answer


def apply(matrix, point):
    a, b, c, d = matrix
    x, y = point
    return ((a * x + b * y) % Q, (c * x + d * y) % Q)


def quotient_once(source_edges, identified):
    classes = []
    labels = {}
    mapping = []
    for old in range(Q * Q):
        representative = 0 if old == identified else old
        if representative not in labels:
            labels[representative] = len(classes)
            classes.append(representative)
        mapping.append(labels[representative])
    edge_set = set()
    for u, v in source_edges:
        a, b = mapping[u], mapping[v]
        require(a != b, "first fibre is not independent")
        edge_set.add((min(a, b), max(a, b)))
    return classes, mapping, sorted(edge_set)


def adjacency(vertex_count, edges):
    answer = [set() for _ in range(vertex_count)]
    for u, v in edges:
        require(0 <= u < v < vertex_count, "edge range")
        answer[u].add(v)
        answer[v].add(u)
    return answer


def binary_rank(rows):
    basis = {}
    for original in rows:
        require(type(original) is int and original >= 0, "binary row")
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def checked_predecessor_cycles(cycles, adj):
    rows = []
    require(type(cycles) is list and len(cycles) == 119,
            "predecessor cycle basis length")
    for cycle in cycles:
        require(type(cycle) is list and len(cycle) == 4 and
                all(type(v) is int and 0 <= v < 120 for v in cycle) and
                len(set(cycle)) == 4, "predecessor cycle format")
        a, b, c, d = cycle
        require(b in adj[a] and c in adj[b] and d in adj[c] and a in adj[d],
                "predecessor cycle absent")
        rows.append(sum(1 << vertex for vertex in cycle))
    require(binary_rank(rows) == 119, "predecessor basis rank")


def projected_rank(cycles, merged_a, merged_b):
    lo, hi = sorted((merged_a, merged_b))

    def target(vertex):
        if vertex == hi:
            vertex = lo
        return vertex - (vertex > hi)

    rows = []
    surviving = 0
    for cycle in cycles:
        image = [target(vertex) for vertex in cycle]
        if len(set(image)) != 4:
            continue
        surviving += 1
        rows.append(sum(1 << vertex for vertex in image))
    return surviving, binary_rank(rows)


def contract_edges(edges, merged_a, merged_b):
    lo, hi = sorted((merged_a, merged_b))

    def target(vertex):
        if vertex == hi:
            vertex = lo
        return vertex - (vertex > hi)

    answer = set()
    for u, v in edges:
        a, b = target(u), target(v)
        require(a != b, "second fibre is not independent")
        answer.add((min(a, b), max(a, b)))
    return sorted(answer)


def complete_cycle_rank(vertex_count, edges):
    adj = adjacency(vertex_count, edges)
    keys = set()
    rows = []
    for a, c in combinations(range(vertex_count), 2):
        for b, d in combinations(adj[a] & adj[c], 2):
            opposite = tuple(sorted(((a, c), tuple(sorted((b, d))))))
            if opposite in keys:
                continue
            keys.add(opposite)
            rows.append((1 << a) | (1 << b) | (1 << c) | (1 << d))
    return len(keys), binary_rank(rows)


def canonical_event(shell, shape, u, v, rank, compatible):
    return (json.dumps([shell, shape, u, v, rank, compatible],
                       separators=(",", ":")) + "\n").encode()


def validate_top_level(certificate):
    require(type(certificate) is dict and set(certificate) == {
        "schema", "field_order", "rank_prime", "source_vertices",
        "source_edges", "target_distinct_images", "normalized_events_checked",
        "events_by_fibre_shape", "five_colour_compatible_normalizations",
        "fallback_full_cycle_checks", "fallback_equations_checked",
        "all_final_ranks_mod_2", "event_stream_sha256",
        "dependencies_sha256", "shells",
    }, "certificate fields")
    require(certificate["schema"] == "hn-g11-exact119-rhombus-v1",
            "certificate schema")
    require(certificate["field_order"] == Q and
            certificate["rank_prime"] == 2 and
            certificate["source_vertices"] == 121 and
            certificate["source_edges"] == 726 and
            certificate["target_distinct_images"] == 119,
            "fixed parameters")
    require(type(certificate["event_stream_sha256"]) is str and
            len(certificate["event_stream_sha256"]) == 64,
            "event digest format")
    require(type(certificate["shells"]) is list and
            len(certificate["shells"]) == 9, "shell record count")


def run(certificate):
    validate_top_level(certificate)
    dependencies = certificate["dependencies_sha256"]
    require(dependencies == {
        "g11_one_collision_certificate.json":
            sha256(PREDECESSOR / "certificate.json"),
        "q11_four_unsat.drat": sha256(CHROMATIC / "q11_four_unsat.drat"),
        "q11_five_colouring.json":
            sha256(CHROMATIC / "q11_five_colouring.json"),
    }, "dependency hashes")
    predecessor = json.loads((PREDECESSOR / "certificate.json").read_text())
    predecessor_cases = {case["norm"]: case for case in predecessor["cases"]}
    points, source_edges = reconstruct_source()
    require(len(points) == 121 and len(source_edges) == 726,
            "source graph census")
    source_colours = json.loads((CHROMATIC / "q11_five_colouring.json").read_text())
    require(type(source_colours) is list and len(source_colours) == 121 and
            set(source_colours) == set(range(5)) and
            all(source_colours[u] != source_colours[v] for u, v in source_edges),
            "source five-colouring")
    matrices = orthogonal_matrices()
    require(len(matrices) == 24, "orthogonal group order")
    for matrix in matrices:
        require(all(norm(apply(matrix, point)) == norm(point) for point in points),
                "orthogonal action")
    require({point for point in points if norm(point) == 0} == {(0, 0)},
            "anisotropic norm")

    event_digest = hashlib.sha256()
    shell_records = []
    totals = Counter()
    for shell in range(2, 11):
        case = predecessor_cases[shell]
        representative = tuple(case["representative"])
        require(norm(representative) == shell, "representative norm")
        orbit = {apply(matrix, representative) for matrix in matrices}
        require(orbit == {point for point in points if norm(point) == shell} and
                len(orbit) == 12, "norm-shell orbit")
        identified = representative[0] * Q + representative[1]
        require(case["identified_source_addresses"] == [0, identified],
                "predecessor representative address")
        roots, mapping, edges = quotient_once(source_edges, identified)
        require(len(roots) == 120 and
                all((min(mapping[u], mapping[v]), max(mapping[u], mapping[v])) in edges
                    for u, v in source_edges), "one-collision quotient map")
        adj = adjacency(120, edges)
        checked_predecessor_cycles(case["basis_cycles"], adj)
        colours = case["five_colouring"]
        require(type(colours) is list and len(colours) == 120 and
                set(colours) == set(range(5)) and
                all(colours[u] != colours[v] for u, v in edges),
                "one-collision five-colouring")
        record = {
            "norm": shell,
            "representative": list(representative),
            "one_collision_edges": len(edges),
            "triple_events": 0,
            "two_pair_events": 0,
            "five_colour_compatible_triples": 0,
            "five_colour_compatible_two_pairs": 0,
            "projected_rank_histogram_triples": {},
            "projected_rank_histogram_two_pairs": {},
            "fallback_triples": 0,
            "fallback_two_pairs": 0,
        }
        histograms = {"triple": Counter(), "two_pairs": Counter()}

        def check_event(shape, u, v):
            surviving, projected = projected_rank(case["basis_cycles"], u, v)
            histograms[shape][projected] += 1
            compatible = colours[u] == colours[v]
            if projected < 118:
                complete_edges = contract_edges(edges, u, v)
                equations, final_rank = complete_cycle_rank(119, complete_edges)
                totals["fallback_events"] += 1
                totals["fallback_equations"] += equations
                record["fallback_triples" if shape == "triple"
                       else "fallback_two_pairs"] += 1
            else:
                final_rank = projected
            require(final_rank == 118, "nonmaximal final rhombus rank")
            event_digest.update(canonical_event(shell, shape, u, v,
                                                final_rank, compatible))
            totals["events"] += 1
            totals[shape] += 1
            totals["compatible"] += int(compatible)
            return compatible

        for third in range(1, 120):
            if third in adj[0]:
                continue
            compatible = check_event("triple", 0, third)
            record["triple_events"] += 1
            record["five_colour_compatible_triples"] += int(compatible)
        for u, v in combinations(range(1, 120), 2):
            if v in adj[u]:
                continue
            compatible = check_event("two_pairs", u, v)
            record["two_pair_events"] += 1
            record["five_colour_compatible_two_pairs"] += int(compatible)
        record["projected_rank_histogram_triples"] = {
            str(k): v for k, v in sorted(histograms["triple"].items())
        }
        record["projected_rank_histogram_two_pairs"] = {
            str(k): v for k, v in sorted(histograms["two_pairs"].items())
        }
        shell_records.append(record)

    require(shell_records == certificate["shells"], "shell records")
    require(certificate["normalized_events_checked"] == totals["events"] == 57735,
            "normalized event total")
    require(certificate["events_by_fibre_shape"] == {
        "triple": totals["triple"], "two_pairs": totals["two_pairs"]
    } == {"triple": 864, "two_pairs": 56871}, "shape totals")
    require(certificate["five_colour_compatible_normalizations"] ==
            totals["compatible"] == 12627, "five-colour compatibility total")
    require(certificate["fallback_full_cycle_checks"] ==
            totals["fallback_events"] == 777, "fallback total")
    require(certificate["fallback_equations_checked"] ==
            totals["fallback_equations"], "fallback equation total")
    require(certificate["all_final_ranks_mod_2"] == {"118": totals["events"]},
            "final rank histogram")
    require(certificate["event_stream_sha256"] == event_digest.hexdigest(),
            "event stream hash")
    return {
        "verified": True,
        "source_graph": "G_11=Cay(F_11^2,{d:d.x^2+d.y^2=1})",
        "source_vertices": 121,
        "source_edges": 726,
        "target_distinct_images": 119,
        "orthogonal_matrices": 24,
        "normalized_events_checked": totals["events"],
        "triple_normalizations": totals["triple"],
        "two_pair_normalizations": totals["two_pairs"],
        "five_colour_compatible_normalizations": totals["compatible"],
        "fallback_full_cycle_checks": totals["fallback_events"],
        "fallback_equations_checked": totals["fallback_equations"],
        "all_final_ranks_mod_2": [118],
        "all_edge_preserving_maps_with_exactly_119_images_excluded": True,
        "chromatic_lower_bound_imported_from_pinned_dependency": True,
        "physical_unit_distance_graph_produced": False,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(json.loads(args.certificate.read_text()))
    if args.check_expected:
        require(result == json.loads(EXPECTED.read_text()), "expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
