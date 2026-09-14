#!/usr/bin/env python3
"""Clean-room checker for the capped full-Parts-gadget field closure.

This imports no implementation from the target or field-colouring package.
It uses a generic bit-mask radical algebra, reconstructs every archived
residual isometry, and independently implements the reviewed 2-adic colouring.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TARGET = REPO / "hadwiger_nelson_parts_full_gadget_overlap_closure"
POINTS = REPO / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
SEEDS = REPO / "hadwiger_nelson_parts509_two_overlap_library_census/residual_seeds.tsv"

RAD = (1, 3, 5, 15, 11, 33, 55, 165)
Z8 = (F(0),) * 8
O8 = (F(1),) + (F(0),) * 7

PINS = {
    "target/README.md": "4dd6a701e448e635d78c32779d6253d3871ccaa5eedb0328c9f94fd5a6da0d47",
    "target/EXPECTED.json": "8c8d241d8367ed88a378e934c14939c9de6f56dd9693bc3bb1095b49fa498b8c",
    "target/VALIDATION.json": "afe4ef03134f60ac48328a02bbf04e7bafdd3a6922a17fd108c98518f02c6a40",
    "target/CONTROLS.json": "ca61d232948b2cdd4dcae460aa5d293ec26d970f4e892dac651107df594bb432",
    "target/verify.py": "16d73ae3cc114c75ade89161a4211d2441f76b9b6827175bcd9f397c431dbc40",
    "target/controls.py": "e3381d348169127d0b41ab0c0a31497421cae32b3b19a9300167dc69048b1101",
    "target/inputs.json": "84e20ed0afc38b1eba2bc33d8811fa497f251af0508982bcf46ec541b8e0f191",
    "field/PROOF.md": "b5baa3fb96fa976e95983522d74eea3683534b8c8fb6f4ea949498d10eba4ec7",
    "field/coloring.py": "a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e",
    "field-review/README.md": "6fdefb8029066dff966b38cfa0c4aba4ed83c5d293f22de2629ed2037227e2db",
    "residual-review/README.md": "a2dec8ee2ca1c910f23e8c77a12901dbeeaa4773e84dce3fe1ef80b54af9fd44",
    "points.tsv": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "residual_seeds.tsv": "385d4434132fe7c84a8ab59f5f4836a9b16838fd4c302990bad4e2e4a0488bfd",
}


def need(condition, detail):
    if not condition:
        raise ValueError(detail)


def rejects(function):
    try:
        function()
    except (ValueError, ZeroDivisionError):
        return
    raise ValueError("negative control was accepted")


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def json_hash(value):
    return sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def radd(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def rneg(a):
    return tuple(-x for x in a)


def rscale(a, scalar):
    return tuple(scalar * x for x in a)


def rmul(a, b):
    """Multiply in Q(sqrt(3),sqrt(5),sqrt(11)) by subset masks."""
    out = [F(0)] * 8
    left = [(i, x) for i, x in enumerate(a) if x]
    right = [(j, y) for j, y in enumerate(b) if y]
    for i, x in left:
        for j, y in right:
            out[i ^ j] += RAD[i & j] * x * y
    return tuple(out)


def cadd(z, w):
    return radd(z[0], w[0]), radd(z[1], w[1])


def cneg(z):
    return rneg(z[0]), rneg(z[1])


def csub(z, w):
    return cadd(z, cneg(w))


def cmul(z, w):
    return radd(rmul(z[0], w[0]), rneg(rmul(z[1], w[1]))), radd(
        rmul(z[0], w[1]), rmul(z[1], w[0])
    )


def cconj(z):
    return z[0], rneg(z[1])


def cinv(z):
    norm, imaginary = cmul(z, cconj(z))
    need(imaginary == Z8 and all(not norm[i] for i in range(8) if i not in (0, 5)), "norm field")
    a, b = norm[0], norm[5]
    denominator = a * a - 33 * b * b
    need(denominator != 0, "division by zero")
    inverse_norm = (a / denominator,) + (F(0),) * 4 + (-b / denominator,) + (F(0),) * 2
    return cmul(cconj(z), (inverse_norm, Z8))


def cdiv(z, w):
    return cmul(z, cinv(w))


def is_unit(z):
    return cmul(z, cconj(z)) == (O8, Z8)


def in_E(z):
    return all(not z[0][i] for i in range(8) if i not in (0, 5)) and all(
        not z[1][i] for i in range(8) if i not in (1, 4)
    )


def e4(z):
    need(in_E(z), "point outside E")
    return z[0][0], z[0][5], z[1][1], z[1][4]


def e_unit_difference(z, w):
    a, b, c, d = e4(csub(z, w))
    return a * a + 33 * b * b + 3 * c * c + 11 * d * d == 1 and a * b + c * d == 0


def complete_E(points):
    need(len(points) == len(set(points)), "point collision")
    coefficients = [e4(z) for z in points]
    denominator = lcm(*(value.denominator for row in coefficients for value in row))
    rows = [tuple(int(value * denominator) for value in row) for row in coefficients]
    square = denominator * denominator
    edges = []
    for i, (a, b, c, d) in enumerate(rows):
        for j in range(i + 1, len(rows)):
            A, B, C, D = rows[j]
            x, y, z, w = a - A, b - B, c - C, d - D
            if x * x + 33 * y * y + 3 * z * z + 11 * w * w == square and x * y + z * w == 0:
                edges.append((i, j))
    return edges


@lru_cache(maxsize=None)
def lift_root33(bits):
    need(type(bits) is int and bits >= 1, "root precision")
    t = 0
    for precision in range(max(0, bits - 3)):
        modulus = 1 << (precision + 1)
        if (4 * t * t + t - 2) % modulus:
            t += 1 << precision
        need((4 * t * t + t - 2) % modulus == 0, "Hensel lift")
    modulus = 1 << bits
    root = (1 + 8 * t) % modulus
    need((root * root - 33) % modulus == 0, "bad root")
    return root


@lru_cache(maxsize=None)
def colour(z):
    coefficients = e4(z)
    denominator = lcm(*(value.denominator for value in coefficients))
    a, b, c, d = (int(value * denominator) for value in coefficients)
    exponent = (denominator & -denominator).bit_length() - 1
    modulus = 1 << (exponent + 1)
    root = lift_root33(exponent + 1)
    odd_inverse = pow(3 * (denominator >> exponent), -1, modulus)
    first = ((3 * a + 3 * b * root + 3 * c + d * root) * odd_inverse) % modulus
    second = ((6 * c + 2 * d * root) * odd_inverse) % modulus
    return (first >> exponent) + 2 * (second >> exponent)


def checked_word(points, edges):
    word = "".join(map(str, map(colour, points)))
    need(len(word) == len(points) and set(word) <= set("0123"), "colour domain")
    need(all(word[a] != word[b] for a, b in edges), "monochromatic unit edge")
    return word


def point_from_row(row, denominator=96):
    need(len(row) == 16, "coordinate width")
    return tuple(F(x, denominator) for x in row[:8]), tuple(F(x, denominator) for x in row[8:])


def integer_row(z, denominator):
    values = [value * denominator for axis in z for value in axis]
    need(all(value.denominator == 1 for value in values), "nonintegral row")
    return tuple(int(value) for value in values)


def encode_fraction(value):
    return [value.numerator, value.denominator]


def encode_point(z):
    return [encode_fraction(value) for value in e4(z)]


def read_inputs():
    paths = {
        "target/README.md": TARGET / "README.md",
        "target/EXPECTED.json": TARGET / "EXPECTED.json",
        "target/VALIDATION.json": TARGET / "VALIDATION.json",
        "target/CONTROLS.json": TARGET / "CONTROLS.json",
        "target/verify.py": TARGET / "verify.py",
        "target/controls.py": TARGET / "controls.py",
        "target/inputs.json": TARGET / "inputs.json",
        "field/PROOF.md": REPO / "hadwiger_nelson_nonmono_field_obstruction/PROOF.md",
        "field/coloring.py": REPO / "hadwiger_nelson_nonmono_field_obstruction/coloring.py",
        "field-review/README.md": REPO / "hadwiger_nelson_nonmono_field_obstruction_review3/README.md",
        "residual-review/README.md": REPO / "hadwiger_nelson_parts509_two_overlap_library_review1/README.md",
        "points.tsv": POINTS,
        "residual_seeds.tsv": SEEDS,
    }
    for name, expected in PINS.items():
        need(file_hash(paths[name]) == expected, ("review pin", name))
    for relative, pin in json.loads((TARGET / "inputs.json").read_text()).items():
        path = REPO / relative
        need(path.stat().st_size == pin["bytes"] and file_hash(path) == pin["sha256"], ("target pin", relative))
    rows = [
        tuple(map(int, line.split()))
        for line in POINTS.read_text().splitlines()
        if line and not line.startswith("#")
    ]
    seeds = [
        tuple(map(int, line.split()))
        for line in SEEDS.read_text().splitlines()
        if line and not line.startswith("#")
    ]
    need(len(rows) == len(set(rows)) == 509 and all(len(row) == 16 for row in rows), "point table")
    need(len(seeds) == len(set(seeds)) == 2772, "seed table")
    return rows, seeds, json.loads((TARGET / "EXPECTED.json").read_text())


def place(seed, L, B, conjugate_B, L_index):
    orientation, first, second = seed
    p0, q0 = divmod(first, 136)
    p1, q1 = divmod(second, 136)
    need(0 <= orientation < 2840 and 0 <= p0 < p1 < 374 and q0 != q1, "seed domain")
    source = conjugate_B if orientation >= 1420 else B
    u = cdiv(csub(L[p1], L[p0]), csub(source[q1], source[q0]))
    need(is_unit(u), "seed segments have unequal length")
    t = csub(L[p0], cmul(u, source[q0]))
    placed = [cadd(cmul(u, z), t) for z in source]
    need(all(in_E(z) for z in placed) and len(placed) == len(set(placed)) == 136, "placed gadget")
    overlaps = sorted((L_index[z], q) for q, z in enumerate(placed) if z in L_index)
    need(overlaps == sorted(((p0, q0), (p1, q1))), ("overlap mismatch", seed, overlaps))
    merged = list(dict.fromkeys(L + placed))
    need(len(merged) == 508, "residual order")
    return u, t, placed, overlaps, merged


def sample_result(index, seed, merged, overlaps):
    edges = complete_E(merged)
    word = checked_word(merged, edges)
    return {
        "seed_index": index,
        "seed": list(seed),
        "overlaps": [list(pair) for pair in overlaps],
        "points": len(merged),
        "all_pairs": len(merged) * (len(merged) - 1) // 2,
        "unit_edges": len(edges),
        "four_colouring": word,
        "edge_sha256": json_hash(edges),
    }


def run():
    rows, seeds, expected = read_inputs()

    basis = [tuple(F(int(i == j)) for i in range(8)) for j in range(8)]
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            need(rmul(a, b) == rscale(basis[i ^ j], RAD[i & j]), ("basis", i, j))
    for bits in range(1, 129):
        lift_root33(bits)
    need({(a * a - a * b + b * b) % 2 for a, b in ((0, 1), (1, 0), (1, 1))} == {1}, "binary norm")

    points = [point_from_row(row) for row in rows]
    L = points[:374]
    small = [points[0]] + points[374:]
    rho = (rscale(O8, F(7, 8)), rscale(basis[3], F(1, 8)))
    bar_rho = cconj(rho)
    need(is_unit(rho) and cmul(rho, bar_rho) == (O8, Z8), "rho is not unit")
    B = [cmul(bar_rho, z) for z in small]
    conjugate_B = [cconj(z) for z in B]
    need(all(in_E(z) for z in L + B), "gadget normalization")
    need(all(cmul(rho, z) == source for z, source in zip(B, small, strict=True)), "rho roundtrip")
    need(sum(not in_E(z) for z in small) == 135, "original small field boundary")
    need(set(L) & set(small) == {points[0]}, "original overlap boundary")

    normalized_rows = [integer_row(z, 768) for z in B]
    normalized_hash = json_hash(normalized_rows)
    need(normalized_hash == expected["normalized_small_integer_rows_sha256"], "normalized rows")

    large_edges = complete_E(L)
    small_edges = complete_E(B)
    need((len(large_edges), len(small_edges)) == (1860, 564), "internal graph counts")
    large_word, small_word = checked_word(L, large_edges), checked_word(B, small_edges)
    need(large_word == expected["large_four_colouring"], "large colour identity")
    need(small_word == expected["normalized_small_four_colouring"], "small colour identity")

    outside = list(B[1])
    bad_x = list(outside[0])
    bad_x[2] += 1
    outside[0] = tuple(bad_x)
    rejects(lambda: e4(tuple(outside)))
    rejects(lambda: complete_E([L[0], L[0]]))
    rejects(lambda: lift_root33(0))
    rejects(lambda: cinv((Z8, Z8)))
    corrupt_word = list(large_word)
    corrupt_word[large_edges[0][1]] = corrupt_word[large_edges[0][0]]
    need(any(corrupt_word[a] == corrupt_word[b] for a, b in large_edges), "colour corruption control")

    original_edges = [
        (i, j)
        for i, j in combinations(range(509), 2)
        if is_unit(csub(points[i], points[j]))
    ]
    need(len(original_edges) == 2442, "original Parts edge count")

    L_index = {z: i for i, z in enumerate(L)}
    target_samples = {row["seed_index"]: row for row in expected["direct_samples"]}
    independent_indices = (1, 347, 693, 1039, 1386, 1732, 2078, 2424, 2770)
    sample_indices = set(target_samples) | set(independent_indices)
    target_matches = 0
    independent_samples = []
    parameter_stream = sha256()
    placement_stream = sha256()
    colour_stream = sha256()
    orientations = Counter()
    overlap_histogram = Counter()
    order_histogram = Counter()
    max_parameter_denominator_bits = 0
    all_sample_pairs = 0
    all_sample_edges = 0

    for index, seed in enumerate(seeds):
        u, t, placed, overlaps, merged = place(seed, L, B, conjugate_B, L_index)
        orientations["reversing" if seed[0] >= 1420 else "preserving"] += 1
        overlap_histogram[len(overlaps)] += 1
        order_histogram[len(merged)] += 1
        encoded_parameters = [list(seed), encode_point(u), encode_point(t)]
        parameter_stream.update(json.dumps(encoded_parameters, separators=(",", ":")).encode() + b"\n")
        for z in placed:
            placement_stream.update(json.dumps(encode_point(z), separators=(",", ":")).encode() + b"\n")
        word = bytes(colour(z) for z in merged)
        need(len(word) == 508 and max(word) <= 3, "residual colour word")
        colour_stream.update(word)
        max_parameter_denominator_bits = max(
            max_parameter_denominator_bits,
            *(value.denominator.bit_length() for z in (u, t) for value in e4(z)),
        )
        if index in sample_indices:
            sample = sample_result(index, seed, merged, overlaps)
            all_sample_pairs += sample["all_pairs"]
            all_sample_edges += sample["unit_edges"]
            if index in target_samples:
                need(sample == target_samples[index], ("target sample mismatch", index))
                target_matches += 1
            if index in independent_indices:
                independent_samples.append({
                    "seed_index": index,
                    "unit_edges": sample["unit_edges"],
                    "edge_sha256": sample["edge_sha256"],
                })

    need(overlap_histogram == {2: 2772} and order_histogram == {508: 2772}, "archive coverage")
    need(target_matches == 4, "target sample coverage")
    need(orientations == {"preserving": 1372, "reversing": 1400}, "orientation counts")

    result = {
        "archive_colour_words_sha256": colour_stream.hexdigest(),
        "archive_order_histogram": {str(k): v for k, v in sorted(order_histogram.items())},
        "archive_overlap_histogram": {str(k): v for k, v in sorted(overlap_histogram.items())},
        "archive_parameter_stream_sha256": parameter_stream.hexdigest(),
        "archive_placed_point_stream_sha256": placement_stream.hexdigest(),
        "archive_residuals_reconstructed": len(seeds),
        "basis_product_controls": 64,
        "cap_requires_at_least_two_overlaps": 510 - 508,
        "field_root_precisions": 128,
        "independent_sample_all_pairs": all_sample_pairs,
        "independent_sample_total_unit_edges": all_sample_edges,
        "independent_samples": independent_samples,
        "large_edges": len(large_edges),
        "large_edge_sha256": json_hash(large_edges),
        "large_points": len(L),
        "max_parameter_denominator_bits": max_parameter_denominator_bits,
        "negative_controls_rejected": 5,
        "normalized_small_integer_rows_sha256": normalized_hash,
        "original_parts_edge_sha256": json_hash(original_edges),
        "original_parts_edges": len(original_edges),
        "original_parts_points": len(points),
        "orientation_counts": dict(sorted(orientations.items())),
        "reviewed_field_dependency_pinned": True,
        "small_edges": len(small_edges),
        "small_edge_sha256": json_hash(small_edges),
        "small_with_origin_points": len(B),
        "source_sample_graphs_matched": target_matches,
        "status": "INDEPENDENT_FULL_PARTS_GADGET_FIELD_NORMALIZATION_PASS",
        "universal_cap_and_field_bridge_conditions_checked": True,
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(run(), indent=2, sort_keys=True))
