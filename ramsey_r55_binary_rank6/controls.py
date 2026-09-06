#!/usr/bin/env python3
"""Bounded exhaustive and physical-certificate tests, not a graph search."""
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
from extract import extract, graph_rows
from verify import verify, verify_spread


def require(test, message):
    if not test:
        raise ValueError(message)


def from_coordinates(coordinates, complement=False):
    edges = []
    for i, j in combinations(range(len(coordinates)), 2):
        x, y = coordinates[i], coordinates[j]
        bit = (((x & 7) & (y >> 3)).bit_count()+((y & 7) & (x >> 3)).bit_count()) % 2
        if bit != complement:
            edges.append([i, j])
    return {"n": len(coordinates), "edges": edges}


def main():
    folder = Path(__file__).resolve().parent
    spread = json.loads((folder/"spread.json").read_text())
    pair_checks = verify_spread(spread)
    histogram, graphs = {}, 0
    for n in range(1, 7):
        pairs = list(combinations(range(n), 2))
        for mask in range(1 << len(pairs)):
            graph = {"n": n, "edges": [list(e) for k, e in enumerate(pairs) if mask >> k & 1]}
            certificate = extract(graph)
            rank = verify(graph, certificate, spread)
            histogram[rank] = histogram.get(rank, 0)+1
            graphs += 1
    instances = 0
    for m in range(4):
        allowed = ((1 << m)-1) | (((1 << m)-1) << 3)
        for seed in range(16):
            state, coordinates = seed, []
            for _ in range(43):
                state = (5*state+1) % 64
                coordinates.append(state & allowed)
            for complement in (False, True):
                graph = from_coordinates(coordinates, complement)
                certificate = extract(graph, "blue" if complement else "red")
                rank = verify(graph, certificate, spread)
                require(rank <= 2*m and len(certificate["independent_five"]) == 5, "43-vertex extraction")
                instances += 1
    high = {"n": 43, "edges": [list(e) for e in combinations(range(9), 2)]}
    high_certificate = extract(high)
    require(verify(high, high_certificate, spread) == 8 and high_certificate["status"] == "OUTSIDE_RANK_SIX",
            "High-rank guard")
    fixture = json.loads((folder/"fixture.json").read_text())
    certificate = json.loads((folder/"fixture_certificate.json").read_text())
    require(certificate == extract(fixture), "Fixture production changed")
    require(verify(fixture, certificate, spread) == 6, "Fixture rank")
    mutants = [deepcopy(certificate) for _ in range(4)]
    mutants[0]["binary_rank"] += 2
    mutants[1]["factor_pairs"][0][0] ^= 1
    mutants[2]["coordinates"][0] ^= 1
    mutants[3]["independent_five"][-1] = mutants[3]["independent_five"][0]
    for mutant in mutants:
        try:
            verify(fixture, mutant, spread)
        except ValueError:
            continue
        raise ValueError("Corrupted certificate accepted")
    spread_mutants = [deepcopy(spread) for _ in range(4)]
    spread_mutants[0]["classes"][0][0] = 0
    spread_mutants[1]["classes"][1][0] = spread_mutants[1]["classes"][0][0]
    left, right = spread_mutants[2]["classes"][:2]
    left[0], right[0] = right[0], left[0]
    spread_mutants[3]["zero_color"] = 1
    for mutant in spread_mutants:
        try:
            verify_spread(mutant)
        except ValueError:
            continue
        raise ValueError("Corrupted spread accepted")
    malformed = [{"n": 0, "edges": []}, {"n": True, "edges": []}, {"n": 2, "edges": [[0, 0]]},
                 {"n": 2, "edges": [[1, 0]]}, {"n": 2, "edges": [[0, 1], [0, 1]]},
                 {"n": 2, "edges": [[0, 1.0]]}, {"n": 2, "edges": [[0, 2]]},
                 {"n": 2, "edges": [], "extra": 0}]
    for graph in malformed:
        try:
            graph_rows(graph)
        except ValueError:
            continue
        raise ValueError("Malformed graph accepted")
    result = {"status": "VERIFIED_BINARY_RANK6_EXTRACTOR", "spread_vectors": 63,
              "spread_classes": 9, "isotropic_pair_checks": pair_checks,
              "small_graphs": graphs, "small_graph_binary_rank_histogram": histogram,
              "physical_43_vertex_extractions": instances, "high_rank_outside_control": True,
              "certificate_mutations_rejected": len(mutants), "spread_mutations_rejected": len(spread_mutants),
              "malformed_graphs_rejected": len(malformed),
              "fixture_independent_five": certificate["independent_five"],
              "independent_peer_review": False, "formalization": False}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
