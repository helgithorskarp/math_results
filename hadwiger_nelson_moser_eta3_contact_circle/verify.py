#!/usr/bin/env python3
"""Solver-free exact replay of the eta^3 fixed-phase circle theorem."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from model import DEPENDENCY, K, fixed_case, mul, product, require, serial_inventory
from family import ONE, ZERO, eadd, ecscale, econj, emul, scale, spindle
from geometry import Geometry, proper
from two_factor import event_graph, event_phase

HERE = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def run(library, certificate, audit=True):
    cert = json.loads(Path(certificate).read_text())
    require(cert["format"] == "fixed-eta3-circle-v1", "certificate format")
    words = cert["words"]
    require(all(len(word) == 343 and set(word) <= set("0123") for word in words), "word syntax")
    require(
        cert["word_hashes"] == [hashlib.sha256(word.encode()).hexdigest() for word in words],
        "word hashes",
    )

    M = spindle()
    from family import norm, sub
    unit_edges_M = [(i, j) for i in range(7) for j in range(i + 1, 7) if norm(sub(M[i], M[j])) == ONE]
    require(len(unit_edges_M) == 11, "Moser source edges")
    require(
        not any(all(word[i] != word[j] for i, j in unit_edges_M) for word in product(range(3), repeat=7)),
        "Moser source unexpectedly three-colourable",
    )
    require(
        any(all(word[i] != word[j] for i, j in unit_edges_M) for word in product(range(4), repeat=7)),
        "Moser source lacks a four-colouring",
    )
    eta, rho = M[4], M[2]
    symmetry = mul(eta, rho)
    require({mul(symmetry, K.conj(point)) for point in M} == set(M), "conjugation symmetry")

    u, B, Db, Dm, groups, baseline, stats = fixed_case()
    require(len(B) == 49 and len(baseline) == 1617, "fixed support dimensions")
    require(len(groups) == 922, "exceptional inventory size")
    require(len(cert["assignment"]) == len(groups), "certificate coverage")
    require(cert["u"] == [str(x) for x in u], "certificate phase")
    require(cert["filters"] == stats, "certificate filter census")
    require(cert["vertices"] == 343 and cert["baseline_edges"] == len(baseline), "certificate dimensions")
    require(cert["exceptional_quadratics"] == len(groups), "certificate inventory size")

    geometry = Geometry(library)
    edge_counts = Counter()
    radicands = set()
    edge_stream = hashlib.sha256()
    audited_pairs = 0
    for index, ((key, group), word_id) in enumerate(zip(groups, cert["assignment"])):
        require(isinstance(word_id, int) and 0 <= word_id < len(words), "word index")
        expected = event_graph(Db, Dm, set(baseline), group)
        phase = event_phase(key, group)
        roots = ((phase[0], phase[1]), (phase[0], scale(phase[1], -1)))
        actual_roots = []
        for root in roots:
            require(emul(root, econj(root), group["ss"]) == (ONE, ZERO), "unit phase")
            vm = [ecscale(root, m) for m in M]
            points = [eadd((a, ZERO), w) for a, w in product(B, vm)]
            require(len(points) == len(set(points)) == 343, "injective physical support")
            actual = geometry.graph(points, group["ss"], audit)
            require(actual == expected, "contact inventory and complete geometry disagree")
            actual_roots.append(actual)
            audited_pairs += 343 * 342 // 2
        require(actual_roots[0] == actual_roots[1], "conjugate phase graphs disagree")
        colours = list(words[word_id])
        proper(colours, expected)
        try:
            proper(["0"] * 343, expected)
        except ValueError:
            pass
        else:
            raise ValueError("constant-colour negative control accepted")
        edge_counts[len(expected)] += 1
        radicands.add(group["ss"])
        edge_stream.update((str(index) + ":" + digest(expected) + "\n").encode())
        if (index + 1) % 250 == 0:
            print(f"exact cases {index + 1}/{len(groups)}", file=sys.stderr, flush=True)

    inventory = serial_inventory(u, groups)
    final_edge_counts = {str(k): edge_counts[k] for k in sorted(edge_counts)}
    require(cert["edge_counts"] == final_edge_counts, "certificate edge census")
    return {
        "claim": "Every strict unit-distance graph on M + eta^3 M + v M is four-chromatic for every unit complex v; likewise for eta^-3 by conjugation",
        "record_improvement": False,
        "source_vertices": 7,
        "source_edges": len(unit_edges_M),
        "two_factor_vertices": len(B),
        "support_vertices_outside_base_field": 343,
        "baseline_edges": len(baseline),
        "filters": stats,
        "exceptional_quadratics": len(groups),
        "physical_exceptional_phases": 2 * len(groups),
        "distinct_radicands": len(radicands),
        "certificate_words": len(words),
        "certificate_sha256": hashlib.sha256(Path(certificate).read_bytes()).hexdigest(),
        "edge_counts": final_edge_counts,
        "exact_inventory_sha256": digest(inventory),
        "edge_stream_sha256": edge_stream.hexdigest(),
        "audited_unordered_pairs": audited_pairs,
        "negative_controls": {"constant_colour_rejections": len(groups)},
        "dependency": str(DEPENDENCY.name),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--certificate", default=str(HERE / "certificate.json"))
    parser.add_argument("--skip-real-audit", action="store_true")
    args = parser.parse_args()
    print(json.dumps(run(args.library, args.certificate, not args.skip_real_audit), indent=2, sort_keys=True))
