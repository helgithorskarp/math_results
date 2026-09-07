#!/usr/bin/env python3
"""Independent audit of the Heule catalogue 21-block positive certificate.

This checker imports no code from the reviewed package.  SymPy supplies a
primitive-number-field representation for the exhaustive distance test; a
meet-in-the-middle selector enumeration checks the weighted family.
"""

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


SOURCE_SPECS = (
    ("510.vtx", 510, 25_819, "66defa1743e64073776ed4c6a2e9c496abbd4628bf7d973dcc07cf834ce35b37"),
    ("517.vtx", 517, 26_167, "402aa7b8a1145843366cff178dcfac44b97f8a748e318ae753520cbeb6a784d5"),
    ("529.vtx", 529, 26_780, "ce0cf260e431972c1222521f1b552bc94e7c42040ddf4b4110cee0eaab518dbb"),
    ("553.vtx", 553, 28_611, "7e43a0250f4e54f362ffec98dcc0d364edd06d3d0963931b1ec7c32cc846d4fb"),
)
CERTIFICATE_SHA256 = "5733907c26804d6502fa8943d13071ee977d5e04d6c91027b5964adf4386291a"
EXPECTED_WEIGHTS = (27, 3, 4, 14, 2, 14, 77, 125, 1, 1, 7, 9, 1, 20, 256,
                    2, 15, 11, 3, 2, 117)
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288
LIMIT = 508


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def translated_pair(line):
    """Parse one Mathematica-style pair through SymPy's restricted namespace."""
    require(line.startswith("{") and line.endswith("}"), "bad coordinate row")
    text = line.replace("{", "(").replace("}", ")")
    text = text.replace("Sqrt[", "sqrt(").replace("]", ")")
    value = sp.sympify(text, locals={"sqrt": sp.sqrt})
    require(isinstance(value, tuple) and len(value) == 2, "coordinate arity")
    return value


def coefficient_vector(value, radicals):
    """Collect an element in the displayed multiquadratic basis."""
    simplified = sp.expand(sp.radsimp(value))
    terms = sp.collect(simplified, radicals[1:], evaluate=False)
    require(set(terms).issubset(set(radicals)), "unexpected radical term")
    coefficients = tuple(sp.Rational(terms.get(r, 0)) for r in radicals)
    require(all(c.is_Rational for c in coefficients), "nonrational coefficient")
    require(sp.expand(simplified - sum(c*r for c, r in zip(coefficients, radicals))) == 0,
            "basis reconstruction")
    scaled = tuple(SCALE*c for c in coefficients)
    require(all(c.q == 1 for c in scaled), "coordinate not integral at scale 288")
    return tuple(int(c) for c in scaled), coefficients


def field_value(coefficients, basis, field):
    result = field.zero
    for coefficient, monomial in zip(coefficients, basis):
        result += (field.convert(int(coefficient.p)) /
                   field.convert(int(coefficient.q))) * monomial
    return result


def load_geometry(inputs):
    radicals = (sp.Integer(1), sp.sqrt(3), sp.sqrt(5), sp.sqrt(15),
                sp.sqrt(11), sp.sqrt(33), sp.sqrt(55), sp.sqrt(165))
    field = sp.QQ.algebraic_field(sp.sqrt(3), sp.sqrt(5), sp.sqrt(11))
    basis = tuple(field.from_sympy(r) for r in radicals)
    sources = []
    values_by_vector = {}
    for name, expected_vertices, expected_bytes, expected_hash in SOURCE_SPECS:
        raw = (inputs / name).read_bytes()
        require(len(raw) == expected_bytes, f"{name}: byte count")
        require(digest(raw) == expected_hash, f"{name}: digest")
        source = set()
        for line in raw.decode("utf-8").splitlines():
            coordinate = []
            number_field_coordinate = []
            for value in translated_pair(line.strip()):
                vector, coefficients = coefficient_vector(value, radicals)
                coordinate.extend(vector)
                number_field_coordinate.append(field_value(coefficients, basis, field))
            coordinate = tuple(coordinate)
            require(coordinate not in source, f"{name}: duplicate point")
            source.add(coordinate)
            pair = tuple(number_field_coordinate)
            if coordinate in values_by_vector:
                require(values_by_vector[coordinate] == pair, "field/vector disagreement")
            else:
                values_by_vector[coordinate] = pair
        require(len(source) == expected_vertices, f"{name}: vertex count")
        sources.append(source)

    points = sorted(values_by_vector)
    require(len(points) == 711, "union order")
    source_sets = tuple(sources)
    blocks = {}
    for vertex, point in enumerate(points):
        membership = sum(1 << i for i, source in enumerate(source_sets) if point in source)
        # Basis positions divisible by 5 change sign under sqrt(5) -> -sqrt(5).
        fixed = all(point[8*axis+i] == 0 for axis in (0, 1)
                    for i, radicand in enumerate(RADICANDS) if radicand % 5 == 0)
        blocks.setdefault((0 if fixed else 1, membership), []).append(vertex)
    keys = tuple(sorted(blocks))
    atoms = tuple(tuple(blocks[key]) for key in keys)
    weights = tuple(map(len, atoms))
    require(weights == EXPECTED_WEIGHTS, "block weights")

    values = [values_by_vector[p] for p in points]
    edges = []
    one = field.one
    for v, (xv, yv) in enumerate(values):
        for u in range(v):
            xu, yu = values[u]
            dx, dy = xv-xu, yv-yu
            if dx*dx + dy*dy == one:
                edges.append((u, v))
    edges.sort()
    require(len(edges) == 3_844, "unit-edge count")
    return points, source_sets, keys, atoms, weights, edges


def load_certificate(target, atoms, edges):
    raw = (target / "certificate.json").read_bytes()
    require(digest(raw) == CERTIFICATE_SHA256, "certificate digest")
    certificate = json.loads(raw)
    require(certificate.get("version") == "heule-catalogue-atoms-v1", "version")
    require(type(certificate.get("target")) is int and certificate["target"] == LIMIT,
            "certificate target")
    covers = certificate.get("covers")
    require(isinstance(covers, list) and covers, "empty cover family")
    require(len(covers) == 50, "cover count")
    atom_of = {v: i for i, atom in enumerate(atoms) for v in atom}
    require(len(atom_of) == 711, "atom partition")
    cover_masks = []
    checked_edges = 0
    for item in covers:
        mask, word = item.get("mask"), item.get("word")
        require(type(mask) is int and 0 <= mask < 1 << len(atoms), "cover mask")
        require(isinstance(word, str) and len(word) == len(atom_of), "colour word length")
        for vertex in range(len(atom_of)):
            selected = bool(mask & (1 << atom_of[vertex]))
            require(word[vertex] in ("0123" if selected else "-"), "word support")
        for u, v in edges:
            if word[u] != "-" and word[v] != "-":
                require(word[u] != word[v], "monochromatic unit edge")
                checked_edges += 1
        cover_masks.append(mask)
    require(len(set(cover_masks)) == len(cover_masks), "duplicate cover")
    return tuple(cover_masks), checked_edges


def half_subsets(weights, offset):
    answer = []
    for local_mask in range(1 << len(weights)):
        total = sum(weight for i, weight in enumerate(weights) if local_mask & (1 << i))
        answer.append((local_mask << offset, total))
    return answer


def check_family(weights, cover_masks):
    """Meet-in-the-middle enumeration, with direct maximal-mask coverage."""
    split = 10
    left = half_subsets(weights[:split], 0)
    right = half_subsets(weights[split:], split)
    assignments = admissible = exact_target = 0
    maximal_masks = []
    for left_mask, left_order in left:
        for right_mask, right_order in right:
            assignments += 1
            order = left_order + right_order
            if order > LIMIT:
                continue
            admissible += 1
            exact_target += order == LIMIT
            mask = left_mask | right_mask
            residual = LIMIT - order
            if all(mask & (1 << i) or weight > residual
                   for i, weight in enumerate(weights)):
                maximal_masks.append(mask)
                require(any(mask & ~cover == 0 for cover in cover_masks),
                        f"uncovered maximal mask {mask}")
    require(assignments == 2**21, "assignment count")
    require(admissible == 1_648_500, "admissible count")
    require(exact_target == 3_840, "target-order count")
    require(len(maximal_masks) == 4_396, "maximal count")
    maximal_stream = "".join(f"{mask}\n" for mask in sorted(maximal_masks)).encode()
    return assignments, admissible, exact_target, tuple(maximal_masks), digest(maximal_stream)


def run(inputs, target):
    points, sources, keys, atoms, weights, edges = load_geometry(inputs)
    cover_masks, checked_edges = load_certificate(target, atoms, edges)
    assignments, admissible, exact_target, maximal, maximal_hash = \
        check_family(weights, cover_masks)

    # The crossover chooses every fixed block whose membership contains P510,
    # and every nonfixed block whose membership contains P553.
    crossover_mask = sum(1 << i for i, (side, membership) in enumerate(keys)
                         if (side == 0 and membership & 1) or
                            (side == 1 and membership & 8))
    selected = {v for i, atom in enumerate(atoms) if crossover_mask & (1 << i)
                for v in atom}
    require(crossover_mask == cover_masks[0], "first cover is not crossover")
    require(len(selected) == 508, "crossover order")
    crossover_edges = sum(u in selected and v in selected for u, v in edges)
    require(crossover_edges == 2_497, "crossover edge count")

    coordinate_stream = "".join(" ".join(map(str, p))+"\n" for p in points).encode()
    edge_stream = "".join(f"{u} {v}\n" for u, v in edges).encode()
    return {
        "accepted": True,
        "arbitrary_subsets_classified": False,
        "assignments": assignments,
        "admissible": admissible,
        "exact_target": exact_target,
        "maximal_admissible": len(maximal),
        "maximal_masks_sha256": maximal_hash,
        "vertices": len(points),
        "edges": len(edges),
        "pair_checks": len(points)*(len(points)-1)//2,
        "blocks": len(atoms),
        "block_keys": [list(key) for key in keys],
        "block_weights": list(weights),
        "colour_words": len(cover_masks),
        "checked_colour_edges": checked_edges,
        "crossover_mask": crossover_mask,
        "crossover_order": len(selected),
        "crossover_edges": crossover_edges,
        "coordinate_sha256": digest(coordinate_stream),
        "edge_sha256": digest(edge_stream),
        "certificate_sha256": CERTIFICATE_SHA256,
        "geometry_engine": "SymPy AlgebraicField exact ANP",
        "coverage_engine": "meet-in-the-middle plus direct maximal-mask containment",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--expected", type=Path)
    arguments = parser.parse_args()
    result = run(arguments.inputs, arguments.target)
    if arguments.expected:
        require(result == json.loads(arguments.expected.read_text()), "expected report mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
