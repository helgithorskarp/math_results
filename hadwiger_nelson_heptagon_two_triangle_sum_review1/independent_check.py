#!/usr/bin/env python3
"""Independent exact review of the fixed 483-point two-spindle sum.

The reviewed package is not imported.  Exact arithmetic comes from the
reviewer's previously accepted Q[t,s]/(Phi_42,s^2+11) implementation.  This
file newly constructs the two-triangle sum, scans its complete unit graph,
and checks the universal F2^2 extension identity.
"""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import importlib.util
import json


HERE = Path(__file__).resolve().parent
BASE_PATH = (HERE.parent / "hadwiger_nelson_heptagon_moser_sum_collisions_review1"
             / "independent_check.py")
BASE_SHA256 = "c854ee538254bd272cd604bc9aa4dabb57e0b48b184b1fde28ac5dc0d965e1a2"
SOURCE_FILES = {
    "SHA256SUMS": "e788b91d3df57263a1425e3064e188c664937c439085c7be88ef3540c594c2e0",
    "README.md": "ec269ebcf35ae82dd96c5ceed2be89d150a9831bd6030a1c70063b852239a051",
    "build.py": "46d1ce612333dd93dfca56b82d0aca7a3c858dc5aea31a9e322af8cc8395cacc",
    "verify.py": "4e455a319bd4983ddbed0be32d5a2715f3d2f6be9ed58f9e10a632e7db25bbfe",
    "expected.json": "93d491f0ce2c71813196c2fd5017de83fbbe724992f4087c18d90be69452b28d",
    "validation.json": "9dacf47fa60e762993b98783d8812bb3824a97a9ec31a59a4263a53c96f82f76",
    "certificate.json": "0656dd5d65128fbf0aed0b852ee9b26c1cc6455b33e781fbc0e3e69317bae212",
}
GRAPH = {"bytes": 88_893,
         "sha256": "f2568bd02c121d37500d8d05f4e352212ac0db16d82d34f6075272db8491b5da"}
H_LABELS = [0, 1, 2, 3, 4, 5, 6, 7, 14, 8, 15]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_info(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


need(file_info(BASE_PATH)["sha256"] == BASE_SHA256,
     "reviewer-owned exact arithmetic has drifted")
spec = importlib.util.spec_from_file_location("reviewer_exact_field", BASE_PATH)
need(spec is not None and spec.loader is not None, "cannot load exact arithmetic")
B = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B)


def source_identity(source):
    observed = {}
    for name, wanted in SOURCE_FILES.items():
        got = file_info(source / name)["sha256"]
        need(got == wanted, f"reviewed source drift: {name}")
        observed[name] = got
    return observed


def decode_fixed(row, denominator):
    need(isinstance(row, list) and len(row) == 24, "wrong coordinate width")
    need(all(isinstance(value, int) for value in row), "nonintegral coordinate")
    return (tuple(Fraction(value, denominator) for value in row[:12]),
            tuple(Fraction(value, denominator) for value in row[12:]))


def proper(colors, edges, number_of_colors):
    return (len(colors) > 0
            and all(isinstance(c, int) and 0 <= c < number_of_colors for c in colors)
            and all(colors[a] != colors[b] for a, b in edges))


def host_coloring_count(edges):
    neighbors = [set() for _ in range(11)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    order = sorted(range(11), key=lambda v: (-len(neighbors[v]), v))
    colors = [-1] * 11
    count = 0

    def visit(position):
        nonlocal count
        if position == len(order):
            count += 1
            return
        vertex = order[position]
        forbidden = {colors[w] for w in neighbors[vertex] if colors[w] >= 0}
        for color in range(4):
            if color not in forbidden:
                colors[vertex] = color
                visit(position + 1)
        colors[vertex] = -1

    visit(0)
    need(count == (3 ** 7 - 3) * 6 ** 2 == 78_624,
         "host four-coloring count differs")
    return count


def support_vector(host, a, b):
    first = (0, (1 << 0) ^ (1 << 7), (1 << 0) ^ (1 << 8),
             (1 << 7) ^ (1 << 8), (1 << 0) ^ (1 << 7),
             (1 << 0) ^ (1 << 8), 0)
    second = (0, (1 << 1) ^ (1 << 9), (1 << 1) ^ (1 << 10),
              (1 << 9) ^ (1 << 10), (1 << 1) ^ (1 << 9),
              (1 << 1) ^ (1 << 10), 0)
    return (1 << host) ^ first[a] ^ second[b]


def evaluate(mask, host_colors):
    value = 0
    for index, color in enumerate(host_colors):
        if mask & (1 << index):
            value ^= color
    return value


def check_symbols(fibres, labels, edges, host_edges, certificate):
    supports = []
    for fibre in fibres:
        choices = {support_vector(h, a, b) for h, a, b in fibre}
        need(len(choices) == 1, "symbolic coloring does not descend through a fibre")
        supports.append(choices.pop())
    need(all(supports[labels[h][0][0]] == 1 << h for h in range(11)),
         "embedded host colors are not preserved")
    allowed = {(1 << a) ^ (1 << b): (a, b) for a, b in host_edges}
    projection = Counter()
    for a, b in edges:
        difference = supports[a] ^ supports[b]
        need(difference in allowed, "unit edge does not project to a host edge")
        projection[allowed[difference]] += 1
    expected_projection = {
        (0, 1): 49, (0, 6): 49, (0, 7): 306, (0, 8): 306,
        (1, 2): 49, (1, 9): 306, (1, 10): 306, (2, 3): 49,
        (3, 4): 49, (4, 5): 49, (5, 6): 49, (7, 8): 247,
        (9, 10): 247,
    }
    need(dict(projection) == expected_projection, "edge projection census differs")
    host_colors = certificate["H_colouring"]
    need(proper(host_colors, host_edges, 4) and set(host_colors) == {0, 1, 2},
         "explicit host certificate is invalid")
    full_colors = [evaluate(mask, host_colors) for mask in supports]
    need(proper(full_colors, edges, 4) and set(full_colors) == {0, 1, 2, 3},
         "explicit extended coloring is invalid")
    # The edge-difference check proves the same assertion for every proper
    # F2^2-valued host coloring, without relying on enumeration of a library.
    return supports, full_colors, projection


def check_target_serialization(work, H, M, R, N, points, labels, fibres,
                               host_edges, spindle_edges, rotated_edges,
                               edges, factor, supports, colors, rotation):
    graph_path = work / "graph.json"
    need(file_info(graph_path) == GRAPH, "reviewed generated graph identity differs")
    graph = json.loads(graph_path.read_text())
    need(graph["denominator"] == 42 and graph["H_labels"] == H_LABELS,
         "serialized construction metadata differs")
    decode = lambda rows: [decode_fixed(row, 42) for row in rows]
    need(decode(graph["H"]) == H and decode(graph["M"]) == M
         and decode(graph["R"]) == R and decode(graph["N"]) == N
         and decode(graph["points"]) == points, "serialized exact support differs")
    need(decode_fixed(graph["rotation"], 1) == rotation, "serialized rotation differs")
    need(graph["labels"] == labels and graph["fibres"] == fibres,
         "serialized labels or fibres differ")
    need(list(map(tuple, graph["H_edges"])) == host_edges
         and list(map(tuple, graph["M_edges"])) == spindle_edges
         and list(map(tuple, graph["R_edges"])) == rotated_edges,
         "serialized factor edges differ")
    need(list(map(tuple, graph["edges"])) == edges
         and list(map(tuple, graph["factor_edges"])) == sorted(factor),
         "serialized full edges differ")
    need(graph["symbolic_masks"] == supports and graph["colouring"] == colors,
         "serialized symbolic certificate differs")
    result = json.loads((work / "result.json").read_text())
    # The producer's result is already pinned by its source-level expected.json;
    # retain only its exact byte identity here.
    need(file_info(work / "result.json")["sha256"] ==
         "93d491f0ce2c71813196c2fd5017de83fbbe724992f4087c18d90be69452b28d",
         "generated result identity differs")
    need(result["vertices"] == 483 and result["edges"] == 2061
         and result["every_host_four_colouring_extends"]
         and not result["target_found"], "generated result boundary differs")
    return {"graph": file_info(graph_path),
            "result": file_info(work / "result.json"),
            "certificate": file_info(work / "certificate.json"),
            "entrywise_support_comparison": True,
            "entrywise_edge_comparison": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--target-work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    all_host, M = B.construct_factors()
    H = [all_host[index] for index in H_LABELS]
    rotation = B.etpow(6)
    need(B.enorm(rotation) == B.OE, "rotation is not unit modulus")
    R = [B.emul(rotation, point) for point in M]
    N = sorted({B.eadd(a, b) for a in M for b in R})
    points = sorted({B.eadd(h, n) for h in H for n in N})
    need((len(H), len(M), len(R), len(N), len(points)) == (11, 7, 7, 49, 483),
         "factor or support size differs")
    index = {point: i for i, point in enumerate(points)}
    labels = [[[index[B.eadd(h, B.eadd(a, b))] for b in R] for a in M] for h in H]
    fibres = [[] for _ in points]
    for h, a, b in product(range(11), range(7), range(7)):
        fibres[labels[h][a][b]].append([h, a, b])
    histogram = Counter(map(len, fibres))
    need(histogram == Counter({1: 441, 2: 28, 3: 14})
         and sum(size * count for size, count in histogram.items()) == 539,
         "fibre partition differs")

    host_edges = B.unit_edges_exact(H)
    spindle_edges = B.unit_edges_exact(M)
    rotated_edges = B.unit_edges_exact(R)
    need((len(host_edges), len(spindle_edges), len(rotated_edges)) == (13, 11, 11)
         and spindle_edges == rotated_edges, "factor unit graph differs")
    models = B.finite_models()
    edges, candidates, false_positives = B.complete_edges(points, models)
    need(len(edges) == 2061 and candidates == 2061 and false_positives == 0,
         "complete exact unit-edge scan differs")
    factor = {
        tuple(sorted((labels[i][a][b], labels[j][a][b])))
        for i, j in host_edges for a, b in product(range(7), repeat=2)
    }
    factor |= {
        tuple(sorted((labels[h][i][b], labels[h][j][b])))
        for i, j in spindle_edges for h, b in product(range(11), range(7))
    }
    factor |= {
        tuple(sorted((labels[h][a][i], labels[h][a][j])))
        for i, j in rotated_edges for h, a in product(range(11), range(7))
    }
    need(set(edges) == factor and len(factor) == 2061,
         "factor images do not equal the complete unit graph")

    certificate = json.loads((args.source / "certificate.json").read_text())
    need(set(certificate) == {"H_colouring"}, "unexpected certificate fields")
    supports, colors, projection = check_symbols(
        fibres, labels, edges, host_edges, certificate)
    need(len(set(supports)) == 112, "symbolic support count differs")
    host_colorings = host_coloring_count(host_edges)

    # A retained translated spindle proves the lower bound four.
    triangle = {(0, 1), (0, 2), (1, 2)}
    need(triangle <= set(spindle_edges), "normalized spindle triangle missing")
    proper_three = 0
    for tail in product(range(3), repeat=4):
        proper_three += proper([0, 1, 2] + list(tail), spindle_edges, 3)
    need(proper_three == 0, "spindle unexpectedly has a three-coloring")
    embedding = [labels[0][a][0] for a in range(7)]
    need(len(set(embedding)) == 7
         and all(tuple(sorted((embedding[a], embedding[b]))) in factor
                 for a, b in spindle_edges), "retained spindle embedding differs")

    target = check_target_serialization(
        args.target_work, H, M, R, N, points, labels, fibres,
        host_edges, spindle_edges, rotated_edges, edges, factor,
        supports, colors, rotation)
    result = {
        "verdict_scope": "fixed Hstar+M+t^6M construction and all its subgraphs",
        "exact_algebra": {"representation": "Q[t,s]/(Phi42(t),s^2+11)",
                          "reviewer_base_sha256": BASE_SHA256,
                          "finite_field_models": [list(model) for model in models],
                          "finite_fields_used_only_as_rejection_filters": True},
        "construction": {"host_vertices": 11, "M_vertices": 7, "rotated_M_vertices": 7,
                         "M_plus_rotated_M_vertices": 49, "formal_triples": 539,
                         "vertices": 483, "fibre_histogram": dict(sorted(histogram.items())),
                         "host_edges": 13, "M_edges": 11, "rotated_M_edges": 11},
        "complete_graph": {"pair_norms_classified": 116403, "modular_candidates": candidates,
                           "exact_unit_edges": len(edges), "modular_false_positives": false_positives,
                           "factor_edge_images": len(factor), "extra_mixed_edges": len(set(edges)-factor)},
        "universal_extension": {"fibres_checked": len(fibres),
                                "distinct_formal_supports": len(set(supports)),
                                "unit_edge_symbolic_differences_checked": len(edges),
                                "host_embeddings_preserved": 11,
                                "proper_labeled_host_four_colorings": host_colorings,
                                "edge_projection_histogram": [list(edge) + [count]
                                                              for edge, count in sorted(projection.items())]},
        "chromatic_number": {"explicit_full_colors_used": len(set(colors)),
                             "normalized_spindle_three_color_cases": 81,
                             "proper_spindle_three_colorings": proper_three,
                             "spindle_embeddings_checked": 1,
                             "value": 4},
        "target_serialization": target,
        "reviewed_source": source_identity(args.source),
        "target_graph_found": False,
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS exact 483-point graph and universal host-coloring extension")


if __name__ == "__main__":
    main()
