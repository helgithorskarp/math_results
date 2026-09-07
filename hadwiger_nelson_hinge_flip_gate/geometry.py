#!/usr/bin/env python3
"""Direct exact enumeration of all one-vertex two-anchor hinge outputs."""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
SEED = HERE.parent / "hadwiger_nelson_neutral_mutation_candidate"
sys.path.insert(0, str(SEED))
import verify as seed

MODULUS = 1000081
ROOTS = (964569, 816716, 970601)
SCALE = 96


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def norm_coefficients(a, b):
    difference = [x-y for x, y in zip(a, b)]
    return tuple(x+y for x, y in zip(
        seed.square(difference[:8]), seed.square(difference[8:])))


def strict_edges(rows):
    unit = (SCALE*SCALE,) + (0,)*7
    return [(a, b) for a, b in combinations(range(len(rows)), 2)
            if norm_coefficients(rows[a], rows[b]) == unit]


def modular_basis():
    require(all(r*r % MODULUS == d for r, d in zip(ROOTS, (3, 5, 11))),
            "invalid modular radical images")
    result = []
    for mask in range(8):
        value = 1
        for j, root in enumerate(ROOTS):
            if mask >> j & 1:
                value = value*root % MODULUS
        result.append(value)
    return tuple(result)


def modular_image(row, basis):
    return (sum(a*b for a, b in zip(row[:8], basis)) % MODULUS,
            sum(a*b for a, b in zip(row[8:], basis)) % MODULUS)


def enumerate_outputs(expected_seed_sha256):
    raw = (SEED / "certificate.json").read_bytes()
    require(digest(raw) == expected_seed_sha256, "seed certificate hash")
    certificate = json.loads(raw)
    labels, rows, swaps = seed.construct(certificate, seed.load_inputs(certificate))
    require(len(labels) == len(rows) == 509, "seed order")
    edges = strict_edges(rows)
    require(edges == seed.strict_edges(rows) and len(edges) == 2447, "seed edge set")
    neighbours = [set() for _ in rows]
    for a, b in edges:
        neighbours[a].add(b)
        neighbours[b].add(a)

    # If v is one common point of unit circles about a,b, the other is
    # q=a+b-v. This enumerates the geometry without square-root extraction.
    outputs = defaultdict(lambda: defaultdict(set))
    routes = 0
    degenerate = 0
    for moved in range(509):
        for a, b in combinations(sorted(neighbours[moved]), 2):
            routes += 1
            q = tuple(rows[a][i]+rows[b][i]-rows[moved][i] for i in range(16))
            if q == rows[moved]:
                degenerate += 1
                continue
            outputs[q][moved].add((a, b))

    seed_lookup = {row: vertex for vertex, row in enumerate(rows)}
    require(len(seed_lookup) == 509, "coincident seed coordinates")
    basis = modular_basis()
    seed_images = [modular_image(row, basis) for row in rows]
    external = []
    survivors = 0
    exact_checks = 0
    unit = (SCALE*SCALE,) + (0,)*7
    for q in sorted(set(outputs)-set(seed_lookup)):
        x, y = modular_image(q, basis)
        q_neighbours = []
        for vertex, (a, b) in enumerate(seed_images):
            dx, dy = (x-a) % MODULUS, (y-b) % MODULUS
            if (dx*dx+dy*dy) % MODULUS != SCALE*SCALE % MODULUS:
                continue
            survivors += 1
            exact_checks += 1
            if norm_coefficients(q, rows[vertex]) == unit:
                q_neighbours.append(vertex)
        for moved, anchor_pairs in sorted(outputs[q].items()):
            common = sorted(set(q_neighbours) & neighbours[moved])
            require(set(anchor_pairs) <= set(combinations(common, 2)),
                    "generating anchor missing")
            external.append({"point": list(q), "moved": moved,
                             "point_neighbours": q_neighbours,
                             "common_anchors": common,
                             "anchor_pairs": [list(pair) for pair in sorted(anchor_pairs)]})

    internal = []
    for q in sorted(set(outputs) & set(seed_lookup)):
        destination = seed_lookup[q]
        for moved, anchor_pairs in sorted(outputs[q].items()):
            internal.append([moved, destination,
                             [list(pair) for pair in sorted(anchor_pairs)]])

    summary = {
        "seed_vertices": 509,
        "seed_edges": len(edges),
        "anchor_pair_routes": routes,
        "degenerate_tangent_routes": degenerate,
        "internal_collision_outputs": len(internal),
        "external_output_pairs": len(external),
        "external_output_coordinates": len({tuple(row["point"]) for row in external}),
        "external_low_degree_outputs": sum(
            len(row["point_neighbours"]) < 4 for row in external),
        "nontrivial_external_outputs": sum(
            len(row["point_neighbours"]) >= 4 for row in external),
        "modular_survivors": survivors,
        "exact_neighbour_checks": exact_checks,
        "maximum_anchor_pairs_per_output": max(map(
            lambda row: len(row["anchor_pairs"]), external)),
        "maximum_common_anchors": max(map(
            lambda row: len(row["common_anchors"]), external)),
    }
    return labels, rows, swaps, edges, external, internal, summary
