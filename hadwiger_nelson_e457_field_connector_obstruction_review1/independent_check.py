#!/usr/bin/env python3
"""Clean-room exact audit of the rotated-field obstruction for E457.

This checker imports no reviewed executable.  It implements the relevant
biquadratic field, the rotation, a separate residue-colour calculation, exact
physical distances, and both forms of the two-overlap recovery formula.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_e457_field_connector_obstruction"
CORE = ROOT / "hadwiger_nelson_e457_equal_pair_source" / "core.json"
TARGET_SOURCE_COMMIT = "78daa396fb1673907034f4c41ccc8af227456a1f"
TARGET_RECEIPT_COMMIT = "13d6c0c0db403402f0eed643ac3a6c0d8897f7cb"
FIELD_SOURCE_COMMIT = "825d763c59e6e299f2c7df4b8c93b13dece6d511"
FIELD_REVIEW_COMMIT = "0d54b52f753674be64f78b6aa57754d873464347"

PINNED = {
    "hadwiger_nelson_e457_field_connector_obstruction/.gitignore":
        "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "hadwiger_nelson_e457_field_connector_obstruction/DISCOVERY_RECEIPT.json":
        "fd93cc1ca4e4c84d27b28c0ff8b5cedb7baf9ce8741e5dc9c9970ac40ddcfcc5",
    "hadwiger_nelson_e457_field_connector_obstruction/README.md":
        "0e43fdcbae615c142c64b885830fa8d458a01b523579b5e117c12832383e51c5",
    "hadwiger_nelson_e457_field_connector_obstruction/SHA256SUMS":
        "335bc204eabbe2645ea5951d8afe962b46c3f1964ae119a1dd2ba739e010dcc4",
    "hadwiger_nelson_e457_field_connector_obstruction/controls.py":
        "906fbc2bfef50a8ff912c8fb36ac855ca7a4f589aae28487899631e4f427d76d",
    "hadwiger_nelson_e457_field_connector_obstruction/expected.json":
        "c08cf95e1b41aeddf87fb18f4d1b9ef59f7f193013747a511d841f5dcaa464af",
    "hadwiger_nelson_e457_field_connector_obstruction/expected.min.json":
        "ce9d76355e67b7fdfca37d5dfed01a5a89dbabedc120dec7144fd9e875ebcb0d",
    "hadwiger_nelson_e457_field_connector_obstruction/verify.py":
        "e7efe338a586e0d20aee8ef5941c163feed2a5fcf08c12096947570d8826fca8",
    "hadwiger_nelson_e457_equal_pair_source/core.json":
        "d377e9526d13cc76aba6762ecd6a79bd04fe12d61e03a0b585a5ea38820d833b",
    "hadwiger_nelson_nonmono_field_obstruction/PROOF.md":
        "b5baa3fb96fa976e95983522d74eea3683534b8c8fb6f4ea949498d10eba4ec7",
    "hadwiger_nelson_nonmono_field_obstruction/coloring.py":
        "a612f6f145f511340d930cf093939cf102128e960ae12977e86dfb1d1e5b486e",
    "hadwiger_nelson_nonmono_field_obstruction_review3/README.md":
        "6fdefb8029066dff966b38cfa0c4aba4ed83c5d293f22de2629ed2037227e2db",
    "hadwiger_nelson_nonmono_field_obstruction_review3/independent_check.py":
        "0a316136327509c0bc6a4e3a9b70e55040a173e68f498d4eb3af058435b43399",
}

ZERO = (Q(0),) * 4
ONE = (Q(1), Q(0), Q(0), Q(0))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def json_digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def add(first, second):
    return tuple(a + b for a, b in zip(first, second, strict=True))


def negate(value):
    return tuple(-entry for entry in value)


def subtract(first, second):
    return add(first, negate(second))


def conjugate(value):
    """Complex conjugation in E with basis 1,sqrt(33),i*sqrt(3),i*sqrt(11)."""
    return value[0], value[1], -value[2], -value[3]


def multiply(first, second):
    """Product in E, independently written from its basis relations."""
    a, b, c, d = first
    A, B, C, D = second
    return (
        a*A + 33*b*B - 3*c*C - 11*d*D,
        a*B + b*A - c*D - d*C,
        a*C + c*A + 11*(b*D + d*B),
        a*D + d*A + 3*(b*C + c*B),
    )


def inverse(value):
    real_norm = multiply(value, conjugate(value))
    require(real_norm[2:] == (0, 0), "complex norm not real")
    a, b = real_norm[:2]
    rational_norm = a*a - 33*b*b
    require(rational_norm != 0, "inverse of zero")
    return multiply(conjugate(value),
                    (a/rational_norm, -b/rational_norm, Q(0), Q(0)))


def e_norm(value):
    result = multiply(value, conjugate(value))
    require(result[2:] == (0, 0), "E norm has imaginary component")
    return result[:2]


def f_norm(value):
    """Squared Euclidean norm in F basis sqrt(3),sqrt(11),i,i*sqrt(33)."""
    a, b, c, d = value
    return (3*a*a + 11*b*b + c*c + 33*d*d, 2*(a*b + c*d))


def rotate_to_e(value):
    """Multiply an F-basis value by conjugate((sqrt(3)+i)/2)."""
    a, b, c, d = value
    return ((3*a+c)/2, (b+d)/2, (c-a)/2, (3*d-b)/2)


def rotate_to_f(value):
    """Inverse map, multiplication by (sqrt(3)+i)/2."""
    a, b, c, d = value
    return ((a-c)/2, (3*b-d)/2, (a+3*c)/2, (b+d)/2)


def in_f_cartesian(real, imaginary):
    """Membership in F using the basis 1,sqrt(3),sqrt(11),sqrt(33)."""
    require(len(real) == len(imaginary) == 4, "Cartesian basis length")
    return (real[0] == real[3] == 0 and
            imaginary[1] == imaginary[2] == 0)


def branch_root33(bits):
    """Independently select the Hensel branch via exhaustive roots for t."""
    require(type(bits) is int and 1 <= bits <= 16, "unsupported root precision")
    modulus = 1 << bits
    roots = [t for t in range(modulus) if (4*t*t+t-2) % modulus == 0]
    require(len(roots) == 1, ("Hensel root not unique", bits, roots))
    root = (1 + 8*roots[0]) % modulus
    require((root*root-33) % modulus == 0, "bad sqrt(33) residue")
    return root


def colour_from_representation(numerators, denominator):
    """Two zero-th 2-adic digits for an E coefficient representation."""
    require(type(denominator) is int and denominator > 0, "bad denominator")
    require(len(numerators) == 4 and all(type(x) is int for x in numerators),
            "bad numerators")
    a, b, c, d = numerators
    exponent = (denominator & -denominator).bit_length() - 1
    modulus = 1 << (exponent + 1)
    root = branch_root33(exponent + 1)
    odd_inverse = pow(3*(denominator >> exponent), -1, modulus)
    local_a = ((3*a+3*b*root+3*c+d*root)*odd_inverse) % modulus
    local_b = ((6*c+2*d*root)*odd_inverse) % modulus
    return (local_a >> exponent) | (2*(local_b >> exponent))


def colour(value):
    denominator = lcm(*(entry.denominator for entry in value))
    numerators = tuple(int(entry*denominator) for entry in value)
    return colour_from_representation(numerators, denominator)


def edge_set(rows):
    edges = []
    norm_matches = 0
    for first, second in combinations(range(len(rows)), 2):
        delta = tuple(Q(a-b, 36) for a, b in zip(rows[first], rows[second], strict=True))
        image = rotate_to_e(delta)
        require(f_norm(delta) == e_norm(image), "pair norm rotation mismatch")
        norm_matches += 1
        if f_norm(delta) == (Q(1), Q(0)):
            edges.append((first, second))
    return edges, norm_matches


def algebra_controls():
    basis = [tuple(Q(int(i == j)) for i in range(4)) for j in range(4)]
    quadratic_probes = list(basis)
    quadratic_probes.extend(add(basis[i], basis[j]) for i, j in combinations(range(4), 2))
    require(all(f_norm(value) == e_norm(rotate_to_e(value))
                for value in quadratic_probes), "quadratic-form identity")
    require(all(rotate_to_f(rotate_to_e(value)) == value and
                rotate_to_e(rotate_to_f(value)) == value
                for value in quadratic_probes), "rotation inverse")
    unit = (Q(1, 2), Q(0), Q(1, 2), Q(0))
    require(f_norm(unit) == (Q(1), Q(0)), "rotation multiplier not unit")

    s = (Q(0), Q(1), Q(0), Q(0))
    alpha = (Q(0), Q(0), Q(1), Q(0))
    beta = (Q(0), Q(0), Q(0), Q(1))
    require(multiply(s, s) == (Q(33), Q(0), Q(0), Q(0)), "s square")
    require(multiply(alpha, alpha) == (Q(-3), Q(0), Q(0), Q(0)), "alpha square")
    require(multiply(beta, beta) == (Q(-11), Q(0), Q(0), Q(0)), "beta square")
    require(multiply(alpha, beta) == negate(s), "alpha beta")
    cartesian_zero = (Q(0),) * 4
    require(in_f_cartesian((Q(0), Q(1), Q(0), Q(0)), cartesian_zero),
            "sqrt(3) not recognized in F")
    require(not in_f_cartesian((Q(3), Q(0), Q(0), Q(0)), cartesian_zero),
            "F incorrectly closed under squaring sqrt(3)")

    for bits in range(1, 13):
        branch_root33(bits)
    residues = {(a, b): (a*a-a*b+b*b) % 2
                for a, b in product(range(2), repeat=2) if (a, b) != (0, 0)}
    require(set(residues.values()) == {1}, "binary norm has nonzero isotropic vector")

    # One overlap cannot imply field containment.  The F-native unit segment
    # {0,i}, rotated by (3+4i)/5 about 0, sends i to (-4+3i)/5.  In the
    # Cartesian basis (1,sqrt(3),sqrt(11),sqrt(33)), F permits real positions
    # 1,2 and imaginary positions 0,3 only; the rational real part escapes.
    multiplier_cartesian = (Q(3, 5), Q(4, 5))
    image_cartesian = (Q(-4, 5), Q(3, 5))
    require(sum(entry*entry for entry in multiplier_cartesian) == 1,
            "one-overlap witness is not an isometry")
    image_real = (image_cartesian[0], Q(0), Q(0), Q(0))
    image_imaginary = (image_cartesian[1], Q(0), Q(0), Q(0))
    image_is_in_f = in_f_cartesian(image_real, image_imaginary)
    require(not image_is_in_f, "one-overlap witness did not escape F")
    return len(quadratic_probes), len(residues)


def colour_controls():
    representation_checks = 0
    unit_checks = 0
    values = []
    for index, row in enumerate(product(range(-2, 3), repeat=4)):
        if index >= 160:
            break
        denominator = (1, 2, 3, 4, 5, 8, 12, 16)[index % 8]
        value = tuple(Q(entry, denominator) for entry in row)
        values.append(value)
        original = colour(value)
        for scale in (3, 6, 10):
            require(colour_from_representation(tuple(scale*entry for entry in row),
                                               scale*denominator) == original,
                    "representation-dependent colour")
            representation_checks += 1

        q = Q((index % 17)-8, (index % 9)+1)
        w = (Q(0), Q(0), q, Q((index % 7)-3, (index % 11)+1))
        unit = multiply(add(ONE, w), inverse(subtract(ONE, w)))
        require(e_norm(unit) == (Q(1), Q(0)), "Cayley value not unit")
        require(colour(value) != colour(add(value, unit)), "monochromatic unit pair")
        unit_checks += 1
    return values, representation_checks, unit_checks


def placement_controls(values):
    tested = 0
    for index in range(40):
        b1 = values[index]
        b2 = values[index+41]
        require(b1 != b2, "placement control repeated point")
        q = Q((index % 13)-6, (index % 8)+1)
        w = (Q(0), Q(0), q, Q((index % 5)-2, (index % 7)+1))
        multiplier = multiply(add(ONE, w), inverse(subtract(ONE, w)))
        translation = values[index+83]
        require(e_norm(multiplier) == (Q(1), Q(0)), "nonisometric control")

        a1 = add(multiply(multiplier, b1), translation)
        a2 = add(multiply(multiplier, b2), translation)
        recovered = multiply(subtract(a1, a2), inverse(subtract(b1, b2)))
        recovered_translation = subtract(a1, multiply(recovered, b1))
        require(recovered == multiplier and recovered_translation == translation,
                "orientation-preserving recovery")
        tested += 1

        a1 = add(multiply(multiplier, conjugate(b1)), translation)
        a2 = add(multiply(multiplier, conjugate(b2)), translation)
        recovered = multiply(subtract(a1, a2),
                             inverse(subtract(conjugate(b1), conjugate(b2))))
        recovered_translation = subtract(a1, multiply(recovered, conjugate(b1)))
        require(recovered == multiplier and recovered_translation == translation,
                "orientation-reversing recovery")
        tested += 1
    return tested


def rejection_controls():
    trials = (
        lambda: inverse(ZERO),
        lambda: branch_root33(0),
        lambda: colour_from_representation((0, 0, 0), 1),
        lambda: colour_from_representation((0, 0, 0, 0), 0),
    )
    rejected = 0
    for trial in trials:
        try:
            trial()
        except RuntimeError:
            rejected += 1
    require(rejected == len(trials), "malformed arithmetic control accepted")
    return rejected


def main():
    for relative, expected in PINNED.items():
        require(file_digest(ROOT / relative) == expected, ("pinned source hash", relative))

    quadratic_controls, nonzero_residues = algebra_controls()
    values, representation_checks, unit_checks = colour_controls()
    placement_checks = placement_controls(values)
    rejected_controls = rejection_controls()

    core = json.loads(CORE.read_text())
    require(core.get("schema") == "hn-e457-equal-pair-v1", "E457 schema")
    rows = core.get("points")
    require(type(rows) is list and len(rows) == 457 and
            all(type(row) is list and len(row) == 4 and
                all(type(entry) is int for entry in row) for row in rows), "E457 rows")
    require(len({tuple(row) for row in rows}) == 457, "E457 tuple collision")
    require(rows[:2] == [[0, 0, 0, 0], [0, 0, 96, 0]], "E457 terminals")

    images = [rotate_to_e(tuple(Q(entry, 36) for entry in row)) for row in rows]
    require(all(rotate_to_f(image) == tuple(Q(entry, 36) for entry in row)
                for image, row in zip(images, rows, strict=True)), "E457 rotation round trip")
    edges, norm_matches = edge_set(rows)
    require(len(edges) == 2329 and norm_matches == 104196, "E457 graph census")
    colours = list(map(colour, images))
    require(all(colours[first] != colours[second] for first, second in edges),
            "field colouring has monochromatic E457 edge")
    require(colours[0] == colours[1] == 0, "field colouring separates endpoints")

    endpoint = images[1]
    require(endpoint == (Q(4, 3), Q(0), Q(4, 3), Q(0)), "rotated endpoint")
    endpoint_local = (Q(8, 3), Q(8, 3))
    require(colour(endpoint) == 0, "endpoint residue")

    edge_digest = json_digest(edges)
    point_digest = json_digest(rows)
    word_digest = sha256(bytes(colours)).hexdigest()
    require(point_digest == "b5f9ca3e0c497fcefb073c05bb0168dee8c5dcd65ff1b9a6653684e52b816904",
            "point digest")
    require(edge_digest == "ead61d74b31afa49c15d8f7abccc9ee4ca40ced3562ece1558bf6c66f7dbd6ae",
            "edge digest")
    require(word_digest == "a7a2fbbeac17fbb566605aaba3ff0730a0e531f930b8dda03589841d1c2958fb",
            "colour digest")

    result = {
        "status": "ROTATED-FIELD CONNECTOR OBSTRUCTION INDEPENDENTLY REPRODUCED",
        "verdict": "ACCEPT_HIGH_CONFIDENCE_WITH_TERMINOLOGY_CORRECTION",
        "target_source_commit": TARGET_SOURCE_COMMIT,
        "target_receipt_commit": TARGET_RECEIPT_COMMIT,
        "field_theorem_source_commit": FIELD_SOURCE_COMMIT,
        "field_theorem_review_commit": FIELD_REVIEW_COMMIT,
        "imports_reviewed_executable_code": False,
        "algebraic_basis": "E=Q+Q*sqrt(33)+Q*i*sqrt(3)+Q*i*sqrt(11)",
        "support": "F=Q*sqrt(3)+Q*sqrt(11)+i*(Q+Q*sqrt(33))",
        "rotation": "u=(sqrt(3)+i)/2; F=uE; conjugate(u)F=E",
        "rotation_squared_norm": "1",
        "quadratic_form_identity_basis_and_pair_probes": quadratic_controls,
        "rotation_inverse_checked_on_same_probes": True,
        "f_is_literal_field": False,
        "terminology_correction": "F is a unit-rotated scalar copy of E, not a multiplicatively closed field",
        "hensel_unique_t_precisions": 12,
        "nonzero_binary_norm_residues": nonzero_residues,
        "colour_representation_checks": representation_checks,
        "exact_unit_translation_checks": unit_checks,
        "two_overlap_recovery_checks": placement_checks,
        "orientation_preserving_and_reversing_checked": True,
        "malformed_arithmetic_controls_rejected": rejected_controls,
        "e457_vertices": len(rows),
        "e457_all_pair_norm_identities": norm_matches,
        "e457_complete_unit_edges": len(edges),
        "e457_point_sha256": point_digest,
        "e457_edge_sha256": edge_digest,
        "e457_field_word_sha256": word_digest,
        "e457_colour_histogram": [Counter(colours)[index] for index in range(4)],
        "e457_endpoint_image": ["4/3", "0", "4/3", "0"],
        "endpoint_local_coordinates": [str(value) for value in endpoint_local],
        "endpoint_local_valuations": [3, 3],
        "endpoint_colours": [colours[0], colours[1]],
        "complete_unit_graph_on_f_four_colourable": True,
        "no_finite_f_connector_forces_endpoints_different": True,
        "two_overlap_f_native_assemblies_remain_in_f": True,
        "connectors_outside_f_excluded": False,
        "one_overlap_assemblies_excluded": False,
        "one_overlap_escape_witness": "{0,i} rotated by (3+4i)/5 maps i to (-4+3i)/5 outside F",
        "five_chromatic_graph_constructed": False,
        "record_improvement": False,
        "global_hadwiger_nelson_progress": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
