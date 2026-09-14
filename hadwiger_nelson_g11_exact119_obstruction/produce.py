#!/usr/bin/env python3
"""Produce the complete exact-119-image G_11 rhombus-rank certificate."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDECESSOR = HERE.parent / "hadwiger_nelson_g11_one_collision"
CHROMATIC = HERE.parent / "hadwiger_nelson_finite_abelian_lifts"
Q = 11


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_graph():
    points = [(x, y) for x in range(Q) for y in range(Q)]
    edges = []
    for u, v in combinations(range(len(points)), 2):
        x, y = points[u]
        X, Y = points[v]
        if ((x - X) ** 2 + (y - Y) ** 2) % Q == 1:
            edges.append((u, v))
    return points, edges


def one_collision(source_edges, identified):
    roots = []
    labels = {}
    mapping = []
    for old in range(Q * Q):
        root = 0 if old == identified else old
        if root not in labels:
            labels[root] = len(roots)
            roots.append(root)
        mapping.append(labels[root])
    edges = sorted({tuple(sorted((mapping[u], mapping[v])))
                    for u, v in source_edges})
    if any(u == v for u, v in edges):
        raise ValueError("the first collision contracts an edge")
    return roots, mapping, edges


def projected_rank(cycles, merged_a, merged_b):
    lo, hi = sorted((merged_a, merged_b))

    def target(vertex):
        if vertex == hi:
            vertex = lo
        return vertex - (vertex > hi)

    basis = {}
    surviving = 0
    for cycle in cycles:
        image = [target(vertex) for vertex in cycle]
        if len(set(image)) != 4:
            continue
        surviving += 1
        row = sum(1 << vertex for vertex in image)
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return surviving, len(basis)


def contract_graph(edges, merged_a, merged_b):
    lo, hi = sorted((merged_a, merged_b))

    def target(vertex):
        if vertex == hi:
            vertex = lo
        return vertex - (vertex > hi)

    answer = sorted({tuple(sorted((target(u), target(v)))) for u, v in edges})
    if any(u == v for u, v in answer):
        raise ValueError("the second collision contracts an edge")
    return answer


def full_cycle_rank(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    equations = set()
    basis = {}
    for a, c in combinations(range(vertex_count), 2):
        for b, d in combinations(sorted(adjacency[a] & adjacency[c]), 2):
            key = tuple(sorted(((a, c), (b, d))))
            if key in equations:
                continue
            equations.add(key)
            row = (1 << a) | (1 << b) | (1 << c) | (1 << d)
            while row:
                pivot = row.bit_length() - 1
                if pivot not in basis:
                    basis[pivot] = row
                    break
                row ^= basis[pivot]
    return len(equations), len(basis)


def canonical_event(shell, shape, u, v, final_rank, compatible):
    return (json.dumps([shell, shape, u, v, final_rank, compatible],
                       separators=(",", ":")) + "\n").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    points, source_edges = source_graph()
    predecessor = json.loads((PREDECESSOR / "certificate.json").read_text())
    cases = {case["norm"]: case for case in predecessor["cases"]}
    event_digest = hashlib.sha256()
    shell_records = []
    totals = Counter()

    for shell in range(2, 11):
        case = cases[shell]
        identified = case["identified_source_addresses"][1]
        roots, mapping, quotient_edges = one_collision(source_edges, identified)
        if len(roots) != 120 or len(case["basis_cycles"]) != 119:
            raise ValueError("bad predecessor case")
        colours = case["five_colouring"]
        if len(colours) != 120 or any(colours[u] == colours[v]
                                      for u, v in quotient_edges):
            raise ValueError("bad predecessor five-colouring")
        adjacency = [set() for _ in roots]
        for u, v in quotient_edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        record = {
            "norm": shell,
            "representative": case["representative"],
            "one_collision_edges": len(quotient_edges),
            "triple_events": 0,
            "two_pair_events": 0,
            "five_colour_compatible_triples": 0,
            "five_colour_compatible_two_pairs": 0,
            "projected_rank_histogram_triples": {},
            "projected_rank_histogram_two_pairs": {},
            "fallback_triples": 0,
            "fallback_two_pairs": 0,
        }
        projected_histograms = {
            "triple": Counter(),
            "two_pairs": Counter(),
        }

        def check_event(shape, u, v):
            surviving, rank = projected_rank(case["basis_cycles"], u, v)
            projected_histograms[shape][rank] += 1
            compatible = colours[u] == colours[v]
            if rank < 118:
                final_edges = contract_graph(quotient_edges, u, v)
                equation_count, final_rank = full_cycle_rank(119, final_edges)
                totals["fallback_equations"] += equation_count
                totals["fallback_events"] += 1
                record["fallback_triples" if shape == "triple"
                       else "fallback_two_pairs"] += 1
            else:
                final_rank = rank
            if final_rank != 118:
                raise ValueError("a normalized event survives the rank gate")
            event_digest.update(canonical_event(shell, shape, u, v,
                                                final_rank, compatible))
            totals["events"] += 1
            totals[shape] += 1
            totals["compatible"] += int(compatible)
            return compatible

        # Fibre-size shape (3,1,...,1).
        for third in range(1, len(roots)):
            if third in adjacency[0]:
                continue
            compatible = check_event("triple", 0, third)
            record["triple_events"] += 1
            record["five_colour_compatible_triples"] += int(compatible)

        # Fibre-size shape (2,2,1,...,1).
        for u, v in combinations(range(1, len(roots)), 2):
            if v in adjacency[u]:
                continue
            compatible = check_event("two_pairs", u, v)
            record["two_pair_events"] += 1
            record["five_colour_compatible_two_pairs"] += int(compatible)

        record["projected_rank_histogram_triples"] = {
            str(k): v for k, v in sorted(projected_histograms["triple"].items())
        }
        record["projected_rank_histogram_two_pairs"] = {
            str(k): v for k, v in sorted(projected_histograms["two_pairs"].items())
        }
        shell_records.append(record)

    certificate = {
        "schema": "hn-g11-exact119-rhombus-v1",
        "field_order": Q,
        "rank_prime": 2,
        "source_vertices": len(points),
        "source_edges": len(source_edges),
        "target_distinct_images": 119,
        "normalized_events_checked": totals["events"],
        "events_by_fibre_shape": {
            "triple": totals["triple"],
            "two_pairs": totals["two_pairs"],
        },
        "five_colour_compatible_normalizations": totals["compatible"],
        "fallback_full_cycle_checks": totals["fallback_events"],
        "fallback_equations_checked": totals["fallback_equations"],
        "all_final_ranks_mod_2": {"118": totals["events"]},
        "event_stream_sha256": event_digest.hexdigest(),
        "dependencies_sha256": {
            "g11_one_collision_certificate.json":
                sha256(PREDECESSOR / "certificate.json"),
            "q11_four_unsat.drat": sha256(CHROMATIC / "q11_four_unsat.drat"),
            "q11_five_colouring.json":
                sha256(CHROMATIC / "q11_five_colouring.json"),
        },
        "shells": shell_records,
    }
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "normalized_events_checked": totals["events"],
        "fallback_full_cycle_checks": totals["fallback_events"],
        "five_colour_compatible_normalizations": totals["compatible"],
        "certificate_sha256": sha256(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
