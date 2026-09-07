#!/usr/bin/env python3
"""Independent exact audit of the weighted T721 fixed-host exclusion.

No code is imported from the reviewed package.  SymPy parses the pinned native
coordinates and supplies exact number-field arithmetic.  This file separately
checks the colouring DAG, every global deletion word, the integer incidence
certificate, and graph-theoretic Moser-spindle absence.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp
from sympy.parsing.mathematica import parse_mathematica


INPUT_SHA256 = "a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6"
CERTIFICATE_SHA256 = "78465aea5e7c976bbd53ceb0a2a6be1c45ee42510841bd64cb836a3fc3a53883"
WEIGHTS_SHA256 = "ce0e2090b494ff7cc4756d116e4a4f0b9d1bb6c219ced0685fe36e313c017a7f"
EXPECTED_COORDINATE_SHA256 = "2deed5f5295609400d2eb802ae88f933ba09119bb8cee11684c2aa14473451f6"
EXPECTED_EDGE_SHA256 = "1d35532bc1392476fcdfd53c4a0f21e4b7fc3cec3dcf921e37303b9e534bb6fd"
EXPECTED_GLOBAL_WORD_SHA256 = "0ca2f9d13ede3573e1c1fbb944d13ee11af9b00f3d7f91ad07d34a7f4d2a063a"
SCALE = 96
RADICANDS = (1, 2, 3, 6, 5, 10, 15, 30)
MODULAR_EMBEDDINGS = (
    (1511, {2: 352, 3: 55, 5: 691}),
    (1559, {2: 501, 3: 714, 5: 79}),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def coefficient_vector(value, radicals):
    simplified = sp.expand(sp.radsimp(value))
    terms = sp.collect(simplified, radicals[1:], evaluate=False)
    require(set(terms).issubset(set(radicals)), "coordinate outside radical basis")
    coefficients = tuple(sp.Rational(terms.get(radical, 0)) for radical in radicals)
    require(sp.expand(simplified - sum(c * r for c, r in zip(coefficients, radicals))) == 0,
            "coordinate basis reconstruction")
    scaled = tuple(SCALE * coefficient for coefficient in coefficients)
    require(all(coefficient.q == 1 for coefficient in scaled), "coordinate denominator")
    return tuple(int(coefficient) for coefficient in scaled)


def parse_half(path):
    raw = path.read_bytes()
    require(len(raw) == 40529 and digest(raw) == INPUT_SHA256, "native input identity")
    points = []
    for number, row in enumerate(raw.decode().splitlines(), 1):
        parsed = parse_mathematica(row)
        require(isinstance(parsed, sp.Tuple) and len(parsed) == 2,
                f"native point {number}")
        points.append(tuple(sp.expand(value) for value in parsed))
    require(len(points) == 721 and len(set(points)) == 721, "native half order")
    require(points[:2] == [(-sp.Integer(1), sp.Integer(0)),
                           (sp.Integer(1), sp.Integer(0))], "native terminals")
    return tuple(points)


def field_value(coefficients, basis, field):
    value = field.zero
    for coefficient, monomial in zip(coefficients, basis):
        if coefficient:
            value += field.convert(coefficient) * monomial
    return value


def modular_images(modulus, prime_roots):
    require(all(root * root % modulus == prime % modulus
                for prime, root in prime_roots.items()), "invalid modular root")
    images = []
    for radicand in RADICANDS:
        value = 1
        remainder = radicand
        for prime in (2, 3, 5):
            if remainder % prime == 0:
                value = value * prime_roots[prime] % modulus
                remainder //= prime
        require(remainder == 1, "radicand outside basis")
        images.append(value)
    return tuple(images)


def exact_edges(points, radicals):
    projections = []
    for modulus, roots in MODULAR_EMBEDDINGS:
        images = modular_images(modulus, roots)
        projections.append(tuple(
            (sum(a * b for a, b in zip(point[:8], images)) % modulus,
             sum(a * b for a, b in zip(point[8:], images)) % modulus)
            for point in points
        ))
    survivors = []
    for vertex in range(len(points)):
        for earlier in range(vertex):
            for (modulus, _), projection in zip(MODULAR_EMBEDDINGS, projections):
                dx = projection[vertex][0] - projection[earlier][0]
                dy = projection[vertex][1] - projection[earlier][1]
                if (dx * dx + dy * dy - SCALE * SCALE) % modulus:
                    break
            else:
                survivors.append((earlier, vertex))

    field = sp.QQ.algebraic_field(sp.sqrt(2), sp.sqrt(3), sp.sqrt(5))
    basis = tuple(field.from_sympy(radical) for radical in radicals)
    values = tuple(
        (field_value(point[:8], basis, field),
         field_value(point[8:], basis, field))
        for point in points
    )
    unit = field.convert(SCALE * SCALE)
    edges = []
    for u, v in survivors:
        dx = values[v][0] - values[u][0]
        dy = values[v][1] - values[u][1]
        if dx * dx + dy * dy == unit:
            edges.append((u, v))
    require(len(edges) == 7897, "unit-edge count")
    return tuple(sorted(edges)), len(survivors)


def multiply_basis(vector, basis_index):
    out = [0] * 8
    for index, coefficient in enumerate(vector):
        out[index ^ basis_index] += coefficient * RADICANDS[index & basis_index]
    return tuple(out)


def divide_vector(vector, denominator):
    require(all(coefficient % denominator == 0 for coefficient in vector),
            "nonintegral rotation coordinate")
    return tuple(coefficient // denominator for coefficient in vector)


def rotate60(point):
    x, y = point[:8], point[8:]
    root3x = multiply_basis(x, 2)
    root3y = multiply_basis(y, 2)
    return (divide_vector(tuple(a - b for a, b in zip(x, root3y)), 2)
            + divide_vector(tuple(a + b for a, b in zip(root3x, y)), 2))


def reconstruct_geometry(path):
    half_expressions = parse_half(path)
    root2, root3, root5 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(5)
    radicals = (sp.Integer(1), root2, root3, sp.sqrt(6), root5,
                sp.sqrt(10), sp.sqrt(15), sp.sqrt(30))
    phase_real, phase_imag = sp.Rational(7, 8), sp.sqrt(15) / 8
    right_expressions = tuple(
        (sp.expand(-1 + phase_real * (x + 1) - phase_imag * y),
         sp.expand(phase_imag * (x + 1) + phase_real * y))
        for x, y in half_expressions
    )
    half_points = tuple(coefficient_vector(x, radicals) + coefficient_vector(y, radicals)
                        for x, y in half_expressions)
    right_points = tuple(coefficient_vector(x, radicals) + coefficient_vector(y, radicals)
                         for x, y in right_expressions)
    require(len(set(half_points)) == len(set(right_points)) == 721,
            "half coordinate uniqueness")
    points = tuple(sorted(set(half_points) | set(right_points)))
    require(len(points) == 1441, "full host order")
    labels = {point: vertex for vertex, point in enumerate(points)}
    left = tuple(labels[point] for point in half_points)
    right = tuple(labels[point] for point in right_points)
    left_set, right_set = set(left), set(right)
    require(left_set & right_set == {left[0]} and left[0] == right[0],
            "half intersection")
    require(left_set | right_set == set(range(len(points))), "half union")

    edges, survivors = exact_edges(points, radicals)
    coordinate_stream = "".join(
        " ".join(map(str, point)) + "\n" for point in points).encode()
    edge_stream = "".join(f"{u} {v}\n" for u, v in edges).encode()
    coordinate_hash, edge_hash = digest(coordinate_stream), digest(edge_stream)
    require(coordinate_hash == EXPECTED_COORDINATE_SHA256, "coordinate stream digest")
    require(edge_hash == EXPECTED_EDGE_SHA256, "edge stream digest")

    local = {global_vertex: local_vertex
             for local_vertex, global_vertex in enumerate(left)}
    half_edges = tuple(sorted(
        tuple(sorted((local[u], local[v]))) for u, v in edges
        if u in left_set and v in left_set
    ))
    require(len(half_edges) == 3948, "half-edge count")
    left_edges = {tuple(sorted((left[u], left[v]))) for u, v in half_edges}
    right_edges = {tuple(sorted((right[u], right[v]))) for u, v in half_edges}
    actual_right = {edge for edge in edges
                    if edge[0] in right_set and edge[1] in right_set}
    require(right_edges == actual_right and left_edges.isdisjoint(right_edges),
            "right-half isometry")
    bridge = tuple(sorted((left[1], right[1])))
    require(set(edges) - left_edges - right_edges == {bridge}, "unique bridge")
    require(left[0] == 25 and bridge == (1391, 1428), "anchor or bridge labels")

    half_labels = {point: vertex for vertex, point in enumerate(half_points)}
    rotations = []
    current = half_points
    for power in range(6):
        require(all(point in half_labels for point in current),
                f"rotation {power} leaves native half")
        permutation = tuple(half_labels[point] for point in current)
        require(len(set(permutation)) == 721, f"rotation {power} permutation")
        require({tuple(sorted((permutation[u], permutation[v])))
                 for u, v in half_edges} == set(half_edges),
                f"rotation {power} edge action")
        rotations.append(permutation)
        current = tuple(rotate60(point) for point in current)
    require(current == half_points, "rotation order six")

    return {
        "points": points,
        "edges": edges,
        "left": left,
        "right": right,
        "half_edges": half_edges,
        "rotations": tuple(rotations),
        "terminals": (0, 1),
        "bridge": bridge,
        "anchor": left[0],
        "modular_survivors": survivors,
        "coordinate_sha256": coordinate_hash,
        "edge_sha256": edge_hash,
    }


def integer(value, lower, upper, message):
    require(type(value) is int and lower <= value < upper, message)
    return value


def check_word(word, order, edges, deleted=None, terminals=None):
    require(type(word) is str and len(word) == order, "colour-word length")
    for vertex, colour in enumerate(word):
        if vertex == deleted:
            require(colour == "-", "deleted vertex present")
        else:
            require(colour in "0123", "invalid colour or omission")
    if terminals is not None:
        require(deleted not in terminals and word[terminals[0]] != word[terminals[1]],
                "terminals not separated")
    checks = 0
    for u, v in edges:
        if deleted not in (u, v):
            require(word[u] != word[v], "monochromatic edge")
            checks += 1
    return checks


def decode_certificate(certificate, graph):
    order = len(graph["left"])
    terminals = graph["terminals"]
    require(type(certificate) is dict
            and set(certificate) == {"version", "target", "terminals", "baseline",
                                        "steps", "seed_batches"},
            "certificate fields")
    require(certificate["version"] == "heule-t721-spindle-cover-v1",
            "certificate version")
    require(type(certificate["target"]) is int and certificate["target"] == 508,
            "certificate target marker")
    require(type(certificate["terminals"]) is list
            and tuple(certificate["terminals"]) == terminals
            and all(type(vertex) is int for vertex in certificate["terminals"]),
            "certificate terminals")
    baseline = certificate["baseline"]
    half_checks = check_word(baseline, order, graph["half_edges"])
    steps = certificate["steps"]
    require(type(steps) is list, "certificate steps")
    words = {}
    kinds = Counter()
    inverse_rotations = []
    for permutation in graph["rotations"]:
        inverse = [None] * order
        for source, image in enumerate(permutation):
            inverse[image] = source
        inverse_rotations.append(tuple(inverse))

    for position, row in enumerate(steps):
        require(type(row) is dict, f"step {position} object")
        deleted = integer(row.get("deleted"), 0, order,
                          f"step {position} deletion")
        require(deleted not in terminals and deleted not in words,
                f"step {position} duplicate or terminal deletion")
        kind = row.get("kind")
        if kind == "seed":
            require(set(row) == {"kind", "deleted", "word"},
                    f"step {position} seed fields")
            word = row.get("word")
        else:
            parent = integer(row.get("parent"), 0, order,
                             f"step {position} parent")
            require(parent in words, f"step {position} forward parent")
            if kind == "rotation":
                require(set(row) == {"kind", "deleted", "parent", "power"},
                        f"step {position} rotation fields")
                power = integer(row.get("power"), 1, 6,
                                f"step {position} rotation power")
                permutation = graph["rotations"][power]
                require(deleted == permutation[parent],
                        f"step {position} rotated deletion")
                inverse = inverse_rotations[power]
                word = "".join(words[parent][inverse[vertex]]
                               for vertex in range(order))
            elif kind == "patch":
                require(set(row) == {"kind", "deleted", "parent", "changes"},
                        f"step {position} patch fields")
                changes = row.get("changes")
                require(type(changes) is list and changes,
                        f"step {position} empty patch")
                edited = list(words[parent])
                changed = set()
                for item in changes:
                    require(type(item) is list and len(item) == 2,
                            f"step {position} patch item")
                    vertex = integer(item[0], 0, order,
                                     f"step {position} patch vertex")
                    colour = item[1]
                    require(vertex not in changed and type(colour) is str
                            and len(colour) == 1 and colour in "-0123",
                            f"step {position} patch colour or duplicate")
                    require(edited[vertex] != colour,
                            f"step {position} redundant patch")
                    changed.add(vertex)
                    edited[vertex] = colour
                word = "".join(edited)
            else:
                raise ValueError(f"step {position} kind")
        half_checks += check_word(word, order, graph["half_edges"],
                                  deleted, terminals)
        words[deleted] = word
        kinds[kind] += 1

    require(len(words) == 236, "half omission count")
    require(kinds == Counter({"rotation": 196, "patch": 28, "seed": 12}),
            "step-kind census")
    batches = certificate["seed_batches"]
    require(type(batches) is list and all(type(value) is int and value >= 0
                                          for value in batches)
            and sum(batches) == kinds["seed"], "seed-batch accounting")
    return baseline, words, half_checks, dict(sorted(kinds.items()))


def palette_candidates():
    for image in itertools.product("0123", repeat=4):
        if len(set(image)) == 4:
            yield image


def glue_word(graph, left_word, right_word, deleted):
    a, b = graph["terminals"]
    for palette in palette_candidates():
        if (graph["left"][a] != deleted
                and left_word[a] != palette[int(right_word[a])]):
            continue
        if (deleted not in graph["bridge"]
                and left_word[b] == palette[int(right_word[b])]):
            continue
        full_word = [None] * len(graph["points"])
        for local, global_vertex in enumerate(graph["left"]):
            if global_vertex != deleted:
                full_word[global_vertex] = left_word[local]
        for local, global_vertex in enumerate(graph["right"]):
            if global_vertex == deleted:
                continue
            colour = palette[int(right_word[local])]
            require(full_word[global_vertex] in (None, colour),
                    "anchor colour conflict")
            full_word[global_vertex] = colour
        full_word[deleted] = "-"
        require(all(colour is not None for colour in full_word),
                "uncoloured global vertex")
        return "".join(full_word)
    raise ValueError("no palette gluing")


def deletion_cover(certificate, graph):
    baseline, half_words, half_checks, kinds = decode_certificate(certificate, graph)
    terminals = graph["terminals"]
    mandatory_half = tuple(sorted(set(terminals) | set(half_words)))
    require(len(mandatory_half) == 238, "mandatory-half order")
    mandatory_global = tuple(sorted({
        mapping[vertex]
        for mapping in (graph["left"], graph["right"])
        for vertex in mandatory_half
    }))
    require(len(mandatory_global) == 475
            and len(mandatory_global) == 2 * len(mandatory_half) - 1,
            "mandatory-global order")
    left_lookup = {vertex: local for local, vertex in enumerate(graph["left"])}
    right_lookup = {vertex: local for local, vertex in enumerate(graph["right"])}
    special = {graph["left"][terminals[0]], graph["left"][terminals[1]],
               graph["right"][terminals[1]]}
    word_digest = hashlib.sha256()
    global_checks = 0
    for deleted in mandatory_global:
        left_word = baseline
        right_word = baseline
        if deleted not in special:
            if deleted in left_lookup:
                left_word = half_words[left_lookup[deleted]]
            else:
                require(deleted in right_lookup, "mandatory vertex outside halves")
                right_word = half_words[right_lookup[deleted]]
        full_word = glue_word(graph, left_word, right_word, deleted)
        global_checks += check_word(full_word, len(graph["points"]),
                                    graph["edges"], deleted)
        word_digest.update(f"{deleted} {full_word}\n".encode())
    word_hash = word_digest.hexdigest()
    require(word_hash == EXPECTED_GLOBAL_WORD_SHA256, "global word-stream digest")
    mandatory_hash = digest((" ".join(map(str, mandatory_global)) + "\n").encode())
    return {
        "mandatory_half": mandatory_half,
        "mandatory_global": mandatory_global,
        "half_checks": half_checks,
        "global_checks": global_checks,
        "step_kinds": kinds,
        "global_word_sha256": word_hash,
        "mandatory_global_sha256": mandatory_hash,
    }


def weighted_bound(proof, graph, mandatory_global):
    order = len(graph["points"])
    mandatory = set(mandatory_global)
    require(type(proof) is dict
            and set(proof) == {"version", "minimum_degree", "outside_capacity",
                               "weights", "exceptional_outside"},
            "weight-certificate fields")
    require(proof["version"] == "t721-weighted-neighbour-v1",
            "weight-certificate version")
    require(type(proof["minimum_degree"]) is int and proof["minimum_degree"] == 4,
            "minimum-degree marker")
    require(type(proof["outside_capacity"]) is int and proof["outside_capacity"] == 2,
            "outside-capacity marker")
    require(type(proof["weights"]) is list and proof["weights"], "weight rows")
    weights = {}
    for row in proof["weights"]:
        require(type(row) is list and len(row) == 2, "weight row")
        vertex = integer(row[0], 0, order, "weighted vertex")
        weight = integer(row[1], 1, 3, "weight value")
        require(vertex in mandatory and vertex not in weights,
                "weight support or duplicate")
        weights[vertex] = weight

    incidence = [0] * order
    for u, v in graph["edges"]:
        incidence[u] += weights.get(v, 0)
        incidence[v] += weights.get(u, 0)
    outside = set(range(order)) - mandatory
    exceptional = tuple(vertex for vertex in sorted(outside) if incidence[vertex] > 2)
    require(type(proof["exceptional_outside"]) is list
            and all(type(vertex) is int for vertex in proof["exceptional_outside"])
            and tuple(proof["exceptional_outside"]) == exceptional,
            "outside exceptions")
    require(exceptional == (217,) and incidence[217] == 3,
            "exceptional incidence")
    require(max(incidence[vertex] for vertex in outside - {217}) == 2,
            "ordinary outside capacity")
    total_weight = sum(weights.values())
    mandatory_incidence = sum(incidence[vertex] for vertex in mandatory)
    outside_excess = sum(max(0, incidence[vertex] - 2) for vertex in outside)
    require(total_weight == 117 and mandatory_incidence == 269
            and outside_excess == 1, "incidence totals")

    # If S contains M and each weighted vertex has at least four neighbours in
    # S, then 4W <= sum_{u in S} t_u.  The right side is at most the exact
    # contribution on M, plus two per other vertex, plus the one-unit excess.
    required_incidence = 4 * total_weight
    gap = required_incidence - mandatory_incidence - outside_excess
    required_extra = max(0, math.ceil(Fraction(gap, 2)))
    minimum_order = len(mandatory) + required_extra
    require(required_incidence == 468 and gap == 198 and required_extra == 99
            and minimum_order == 574, "weighted lower bound")
    return {
        "weighted_vertices": len(weights),
        "weight_multiplicities": {
            str(weight): multiplicity
            for weight, multiplicity in sorted(Counter(weights.values()).items())
        },
        "total_weight": total_weight,
        "required_incidence": required_incidence,
        "incidence_in_mandatory": mandatory_incidence,
        "exceptional_outside_vertices": list(exceptional),
        "outside_excess": outside_excess,
        "required_extra_vertices": required_extra,
        "minimum_critical_order": minimum_order,
        "four_colourable_through": minimum_order - 1,
    }


def moser_audit(graph):
    adjacency = [set() for _ in graph["points"]]
    for u, v in graph["edges"]:
        adjacency[u].add(v)
        adjacency[v].add(u)
    arms = [set() for _ in graph["points"]]
    diamonds = 0
    for u, v in graph["edges"]:
        common = adjacency[u] & adjacency[v]
        require(len(common) <= 2, "unit edge has too many common neighbours")
        if len(common) == 2:
            a, b = sorted(common)
            require(b not in adjacency[a], "diamond tips adjacent")
            arms[a].add(b)
            arms[b].add(a)
            diamonds += 1
    contacts = sum(
        1 for apex in range(len(arms))
        for u, v in itertools.combinations(sorted(arms[apex]), 2)
        if v in adjacency[u]
    )
    require(diamonds == 1392 and contacts == 0, "Moser-spindle census")
    return diamonds, contacts


def run(target, input_path):
    certificate_raw = (target / "certificate.json").read_bytes()
    weights_raw = (target / "weights.json").read_bytes()
    require(digest(certificate_raw) == CERTIFICATE_SHA256, "certificate digest")
    require(digest(weights_raw) == WEIGHTS_SHA256, "weight-certificate digest")
    graph = reconstruct_geometry(input_path)
    cover = deletion_cover(json.loads(certificate_raw), graph)
    bound = weighted_bound(json.loads(weights_raw), graph, cover["mandatory_global"])
    diamonds, contacts = moser_audit(graph)
    require(bound["four_colourable_through"] == 573, "target conclusion")
    return {
        "accepted": True,
        "arbitrary_target_subsets_classified": True,
        "record_improvement": False,
        "vertices": len(graph["points"]),
        "edges": len(graph["edges"]),
        "half_vertices": len(graph["left"]),
        "half_edges": len(graph["half_edges"]),
        "half_terminals": list(graph["terminals"]),
        "shared_vertex": graph["anchor"],
        "bridge": list(graph["bridge"]),
        "moduli": [modulus for modulus, _ in MODULAR_EMBEDDINGS],
        "modular_survivors": graph["modular_survivors"],
        "coordinate_sha256": graph["coordinate_sha256"],
        "edge_sha256": graph["edge_sha256"],
        "input_sha256": INPUT_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "weights_sha256": WEIGHTS_SHA256,
        "half_omission_words": len(cover["mandatory_half"]) - 2,
        "required_half_vertices": len(cover["mandatory_half"]),
        "required_global_vertices": len(cover["mandatory_global"]),
        "deletion_cover_through": len(cover["mandatory_global"]) - 1,
        "step_kinds": cover["step_kinds"],
        "half_edge_checks": cover["half_checks"],
        "global_deletion_edge_checks": cover["global_checks"],
        "global_word_sha256": cover["global_word_sha256"],
        "mandatory_global_sha256": cover["mandatory_global_sha256"],
        **bound,
        "unit_diamonds": diamonds,
        "moser_arm_contacts": contacts,
        "moser_free": True,
        "geometry_engine": "SymPy Mathematica parser plus independent modular maps and AlgebraicField",
        "certificate_engine": "independent DAG decoder, palette enumeration, and direct edge checks",
        "bound_engine": "exact integer incidence double count",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    report = run(arguments.target, arguments.input)
    if arguments.expected:
        require(report == json.loads(arguments.expected.read_text()),
                "expected report mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))
