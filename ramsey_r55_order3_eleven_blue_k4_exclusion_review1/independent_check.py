#!/usr/bin/env python3
"""Independent checker for the four-versus-seven blue-K4 exclusion.

The checker imports no submitted Python module.  It reconstructs the local
core universe, the effective normalizer action, the 197 orbits, the blue-K4
partition, the fixed/blue-triangle attachment sets, and the packing sum.
"""

from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations, permutations, product
from json import dump, dumps, load
from pathlib import Path


COVER_SHA = "8b6b7b1b17d4a8b62cbeff401acad021764bc55986e65cab557ed9500dad48ed"
CLASSIFICATION_SHA = "429289f6e84bbb8ec58fb007024c6b65a55096b4bbe606402d711157c4abc957"
SIGNATURES = (1, 2, 4, 8, 3, 5, 9, 6, 10, 12)
TRIANGLE_PAIRS = tuple(combinations(range(4), 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(TRIANGLE_PAIRS)}
COMPLEMENTARY_PAIR_INDICES = ((4, 9), (5, 8), (6, 7))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def set_digest(values):
    return sha256("".join(f"{value}\n" for value in sorted(values)).encode()).hexdigest()


def bit_word(code):
    return "".join(str(code >> index & 1) for index in range(18))


def edge_position(a, b):
    first, phase_a = divmod(a, 3)
    second, phase_b = divmod(b, 3)
    require(first != second, "internal edge has no cross position")
    if first > second:
        first, second = second, first
        phase_a, phase_b = phase_b, phase_a
    return 3 * PAIR_INDEX[first, second] + (phase_b - phase_a) % 3


def red_requirement(vertices):
    positions = []
    for a, b in combinations(vertices, 2):
        if a // 3 != b // 3:
            positions.append(edge_position(a, b))
    return sum(1 << position for position in set(positions))


def normalized(code):
    anchors = [code >> (3 * index) & 7 for index in range(3)]
    return all(word in (0, 1, 3) for word in anchors) and anchors == sorted(anchors)


def blue_k4_witness(code):
    for phases in product(range(3), repeat=4):
        if all(not (code >> (3 * index + (phases[j] - phases[i]) % 3) & 1)
               for index, (i, j) in enumerate(TRIANGLE_PAIRS)):
            return [3 * triangle + phases[triangle] for triangle in range(4)]
    return None


def transform(code, mapping):
    answer = 0
    for old, new in enumerate(mapping):
        if code >> old & 1:
            answer |= 1 << new
    return answer


def sigma(vertex):
    return 3 * (vertex // 3) + (vertex + 1) % 3 if vertex < 33 else vertex


def normalizer_maps():
    effective = set()
    full_maps = set()
    for permutation in permutations(range(4)):
        for shifts in product(range(3), repeat=4):
            for sign in (1, -1):
                core_map = [3 * permutation[triangle] + (sign * phase + shifts[triangle]) % 3
                            for triangle in range(4) for phase in range(3)]
                require(sorted(core_map) == list(range(12)), "core vertex map")
                bit_map = []
                for i, j in TRIANGLE_PAIRS:
                    for offset in range(3):
                        bit_map.append(edge_position(core_map[3 * i], core_map[3 * j + offset]))
                require(sorted(bit_map) == list(range(18)), "cross-bit permutation")
                effective.add(tuple(bit_map))

                full = core_map[:]
                full.extend(3 * triangle + sign * phase % 3
                            for triangle in range(4, 11) for phase in range(3))
                full.extend(range(33, 43))
                require(sorted(full) == list(range(43)), "full vertex map")
                for vertex in range(43):
                    expected = sigma(full[vertex]) if sign == 1 else sigma(sigma(full[vertex]))
                    require(full[sigma(vertex)] == expected, "normalizer identity")
                full_maps.add(tuple(full))
    require(len(effective) == 1296 and len(full_maps) == 3888, "normalizer counts")
    return sorted(effective), len(full_maps)


def primary_variables_and_later_maps():
    pair_classes = set()
    for a, b in combinations(range(43), 2):
        if b < 33 and a // 3 == b // 3:
            continue
        orbit = []
        x, y = a, b
        for _ in range(3):
            orbit.append(tuple(sorted((x, y))))
            x, y = sigma(x), sigma(y)
        pair_classes.add(min(orbit))
    moving = sorted(pair for pair in pair_classes if pair[1] < 33)
    fixed = sorted(pair for pair in pair_classes if pair[0] >= 33)
    links = sorted((pair for pair in pair_classes if pair[0] < 33 <= pair[1]),
                   key=lambda pair: (pair[1], pair[0]))
    require((len(moving), len(fixed), len(links)) == (165, 45, 110),
            "full primary orbit counts")
    identifier = {pair: index + 1 for index, pair in enumerate(moving + fixed + links)}
    core_variables = []
    for i, j in TRIANGLE_PAIRS:
        for offset in range(3):
            core_variables.append(identifier[(3 * i, 3 * j + offset)])
    require(core_variables == [1, 2, 3, 4, 5, 6, 7, 8, 9,
                               31, 32, 33, 34, 35, 36, 58, 59, 60],
            "minority primary variables")

    later = []
    for triangle in range(4, 11):
        mapping = list(range(43))
        mapping[3 * triangle:3 * triangle + 3] = [3 * triangle + 1,
                                                   3 * triangle + 2,
                                                   3 * triangle]
        later.append(mapping)
    for triangle in range(4, 10):
        mapping = list(range(43))
        mapping[3 * triangle:3 * triangle + 6] = list(range(3 * triangle + 3,
                                                              3 * triangle + 6)) + list(
                                                                  range(3 * triangle,
                                                                        3 * triangle + 3))
        later.append(mapping)
    for vertex in range(33, 42):
        mapping = list(range(43))
        mapping[vertex], mapping[vertex + 1] = mapping[vertex + 1], mapping[vertex]
        later.append(mapping)
    require(len(later) == 22, "later-map count")
    require(all(mapping[:12] == list(range(12))
                and sorted(mapping) == list(range(43))
                and all(mapping[sigma(vertex)] == sigma(mapping[vertex])
                        for vertex in range(43)) for mapping in later),
            "later core-fixing normalizers")
    return core_variables, len(pair_classes), len(later)


def core_census(cover):
    all_red_masks = {red_requirement(vertices) for vertices in combinations(range(12), 5)}
    occupancy_masks = set()
    for vertices in combinations(range(12), 5):
        profile = sorted(sum(vertex // 3 == triangle for vertex in vertices)
                         for triangle in range(4))
        if profile == [1, 1, 1, 2]:
            occupancy_masks.add(red_requirement(vertices))
    require(len(occupancy_masks) == 108, "occupancy-mask count")
    require(sorted(occupancy_masks) == cover["forbidden_patterns"],
            "occupancy masks entrywise")

    # A blue K5 is impossible because each of four internally red triangles
    # contributes at most one vertex.  The masks below cover every red K5
    # occupancy directly, including those with a complete cross word.
    valid = {code for code in range(1 << 18)
             if not any(code & mask == mask for mask in all_red_masks)}
    noncomplete = {code for code in range(1 << 18)
                   if all(code >> (3 * index) & 7 != 7 for index in range(6))}
    require(len(noncomplete) == 117649, "noncomplete-word count")
    require(len(valid) == 115543 and valid <= noncomplete, "literal valid-core count")
    require({code for code in noncomplete
             if not any(code & mask == mask for mask in occupancy_masks)} == valid,
            "occupancy reduction completeness")
    require(cover["raw_binary"] == 1 << 18 and cover["noncomplete"] == len(noncomplete),
            "cover domain counts")
    require(cover["labeled_valid"] == len(valid)
            and cover["labeled_invalid"] == len(noncomplete) - len(valid),
            "cover validity counts")
    require(cover["valid_sha256"] == set_digest(valid), "valid-core digest")
    require(cover["normalized_valid"] == sum(map(normalized, valid)) == 3378,
            "normalized-core count")
    return valid, len(all_red_masks)


def orbit_audit(cover, valid):
    maps, full_map_count = normalizer_maps()
    core_variables, primary_count, later_count = primary_variables_and_later_maps()
    require(cover["normalizer_maps"] == full_map_count
            and cover["effective_core_maps"] == len(maps), "cover action counts")
    cases = cover["cases"]
    require(len(cases) == cover["classes"] == 197, "class count")
    require([case["index"] for case in cases] == list(range(197)), "class indices")
    require([case["bits"] for case in cases] == sorted(case["bits"] for case in cases),
            "representative order")
    seen = set()
    membership = []
    for case in cases:
        code = sum(int(bit) << index for index, bit in enumerate(case["bits"]))
        require(code == case["code"] and bit_word(code) == case["bits"],
                "representative encoding")
        orbit = {transform(code, mapping) for mapping in maps}
        require(orbit <= valid and not orbit & seen, "invalid or overlapping orbit")
        choices = sorted(bit_word(member) for member in orbit if normalized(member))
        require(choices and choices[0] == case["bits"], "canonical representative")
        require((len(orbit), len(choices), set_digest(orbit))
                == (case["labeled"], case["normalized"], case["members_sha256"]),
                "orbit metadata")
        require(case["units"] == [variable if code >> index & 1 else -variable
                                  for index, variable in enumerate(core_variables)],
                "full-parent primary units")
        seen.update(orbit)
        membership.extend((member, code) for member in orbit)
    require(seen == valid, "orbit cover")
    membership_hash = sha256("".join(f"{member} {representative}\n"
                                      for member, representative in sorted(membership)).encode()).hexdigest()
    require(membership_hash == cover["membership_sha256"], "membership digest")
    return maps, membership_hash, core_variables, primary_count, later_count


def classification_audit(cover, classification, valid):
    excluded, retained = [], []
    for case in cover["cases"]:
        row = {"index": case["index"], "bits": case["bits"], "labeled": case["labeled"]}
        witness = blue_k4_witness(case["code"])
        if witness is None:
            retained.append(row)
        else:
            row["blue_k4"] = witness
            excluded.append(row)
    expected = {
        "format": "r55-k11-four-blue-k4-exclusion-v1",
        "cover_sha256": COVER_SHA,
        "excluded": excluded,
        "retained": retained,
        "excluded_classes": len(excluded),
        "retained_classes": len(retained),
        "excluded_labeled": sum(row["labeled"] for row in excluded),
        "retained_labeled": sum(row["labeled"] for row in retained),
    }
    require(classification == expected, "classification entrywise")
    direct_excluded = sum(blue_k4_witness(code) is not None for code in valid)
    require((len(excluded), len(retained)) == (118, 79), "classification counts")
    require(direct_excluded == expected["excluded_labeled"] == 63847,
            "direct labeled excluded count")
    require(len(valid) - direct_excluded == expected["retained_labeled"] == 51696,
            "direct labeled retained count")
    return len(excluded), len(retained), direct_excluded


def fixed_red_matrix(variant):
    require(variant in (0, 1, 2, 4), "fixed variant")
    red = [[False] * 10 for _ in range(10)]
    for i, j in combinations(range(10), 2):
        value = SIGNATURES[i] & SIGNATURES[j] == 0
        for bit, pair in enumerate(COMPLEMENTARY_PAIR_INDICES):
            if {i, j} == set(pair) and variant >> bit & 1:
                value = False
        red[i][j] = red[j][i] = value
    return red


def attachment_matrix(fixed, blue_mask):
    red = [row + [False] * 3 for row in fixed]
    red.extend([[False] * 13 for _ in range(3)])
    for fixed_vertex in range(10):
        for moving_vertex in range(10, 13):
            red[fixed_vertex][moving_vertex] = red[moving_vertex][fixed_vertex] = not (
                blue_mask >> fixed_vertex & 1)
    return red


def monochromatic_five(red):
    for vertices in combinations(range(len(red)), 5):
        colours = {red[a][b] for a, b in combinations(vertices, 2)}
        if len(colours) == 1:
            return vertices, next(iter(colours))
    return None


def attachment_audit(data):
    require(set(data) == {"format", "fixed_signatures", "complementary_variants",
                          "blue_fixed_masks", "max_pair_signatures",
                          "requires_singleton"}, "attachment fields")
    require(data["format"] == "r55-blue-triangle-fixed-attachments-v1",
            "attachment format")
    require(data["fixed_signatures"] == list(SIGNATURES), "signature labels")
    require(data["complementary_variants"] == [0, 1, 2, 4], "fixed variants")
    require(data["max_pair_signatures"] == 1 and data["requires_singleton"] is True,
            "attachment structural bounds")
    structural = set(range(1, 16))
    for pair_index, signature in enumerate(SIGNATURES[4:], 4):
        for singleton_subset in range(1, 16):
            if not singleton_subset & signature:
                structural.add((1 << pair_index) | singleton_subset)
    require(len(structural) == 33, "structural attachment count")
    require(sorted(structural) == data["blue_fixed_masks"], "structural attachment list")

    rows = []
    for variant in (0, 1, 2, 4):
        fixed = fixed_red_matrix(variant)
        allowed = [mask for mask in range(1 << 10)
                   if monochromatic_five(attachment_matrix(fixed, mask)) is None]
        require(allowed == sorted(structural), ("literal attachment set", variant))
        require(all(mask & 15 and (mask >> 4).bit_count() <= 1 for mask in allowed),
                "row-capacity bridge")
        local_degrees = [6 + sum(fixed[vertex]) for vertex in range(4, 10)]
        require(all(degree in (8, 9) for degree in local_degrees), "pair local degrees")
        minimum_blue_triangles = []
        for degree in local_degrees:
            feasible = [blue for blue in range(8) if degree + 3 * (7 - blue) <= 24]
            require(feasible == list(range(2, 8)), "degree-demand bridge")
            minimum_blue_triangles.append(feasible[0])
        rows.append({"variant": variant, "allowed": len(allowed),
                     "local_degrees": local_degrees,
                     "minimum_blue_triangles": minimum_blue_triangles})
    return rows


def parse_packing(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "* #variable= 42 #constraint= 13" and len(lines) == 14,
            "packing header")
    rows = []
    for line in lines[1:]:
        left, right = line.split(" >= ")
        require(right.endswith(" ;"), "packing terminator")
        rhs = int(right[:-2])
        tokens = left.split()
        require(len(tokens) % 2 == 0, "packing terms")
        coefficients = [0] * 42
        for coefficient, variable in zip(tokens[::2], tokens[1::2]):
            index = int(variable.removeprefix("x")) - 1
            require(0 <= index < 42 and coefficients[index] == 0, "packing variable")
            coefficients[index] = int(coefficient)
        rows.append((coefficients, rhs))
    for row, (coefficients, rhs) in enumerate(rows):
        expected = [0] * 42
        if row < 7:
            expected[6 * row:6 * row + 6] = [-1] * 6
            expected_rhs = -1
        else:
            for triangle in range(7):
                expected[6 * triangle + row - 7] = 1
            expected_rhs = 2
        require((coefficients, rhs) == (expected, expected_rhs), "packing semantics")
    return rows


def packing_audit(opb_path, certificate_path):
    rows = parse_packing(opb_path)
    with certificate_path.open() as stream:
        certificate = load(stream)
    require(certificate["format"] == "nonnegative-integer-row-sum-v1", "certificate format")
    weights = certificate["multipliers"]
    require(len(weights) == 13 and all(type(weight) is int and weight >= 0 for weight in weights),
            "certificate weights")
    coefficients = [sum(weight * rows[row][0][column]
                        for row, weight in enumerate(weights)) for column in range(42)]
    rhs = sum(weight * rows[row][1] for row, weight in enumerate(weights))
    require(coefficients == certificate["expected_coefficients"] == [0] * 42,
            "packing cancellation")
    require(rhs == certificate["expected_rhs"] == 5, "packing contradiction")
    return {"variables": 42, "inequalities": 13, "summed_rhs": rhs,
            "all_coefficients_zero": True}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo.resolve()
    core_dir = root / "ramsey_r55_order3_eleven_four_core"
    target_dir = root / "ramsey_r55_order3_eleven_blue_k4_exclusion"

    cover_raw = (core_dir / "cover.json").read_bytes()
    require(sha256(cover_raw).hexdigest() == COVER_SHA, "cover pin")
    cover = load((core_dir / "cover.json").open())
    classification_raw = (target_dir / "classification.json").read_bytes()
    require(sha256(classification_raw).hexdigest() == CLASSIFICATION_SHA,
            "classification pin")
    classification = load((target_dir / "classification.json").open())

    # The equality profile forced in the hand proof has incidence 16 and
    # saturates every triangle: four singletons plus all six pairs once.
    require(len(SIGNATURES) == 10 and set(SIGNATURES[:4]) == {1, 2, 4, 8},
            "singleton profile")
    require(set(SIGNATURES[4:]) == {3, 5, 6, 9, 10, 12}, "pair profile")
    require(sum(mask.bit_count() for mask in SIGNATURES) == 16, "incidence equality")
    require(all(sum(mask >> bit & 1 for mask in SIGNATURES) == 4 for bit in range(4)),
            "per-triangle incidence equality")

    valid, red_mask_count = core_census(cover)
    maps, membership_hash, core_variables, primary_count, later_count = orbit_audit(cover, valid)
    excluded, retained, labeled_excluded = classification_audit(cover, classification, valid)
    with (target_dir / "attachments.json").open() as stream:
        attachment_rows = attachment_audit(load(stream))
    packing = packing_audit(target_dir / "packing.opb",
                            target_dir / "packing_certificate.json")

    report = {
        "status": "accepted: blue-K4 core obstruction and 118-to-79 catalog reduction",
        "external_ramsey_input": "R(4,5)=25",
        "fixed_signature_profile": list(SIGNATURES),
        "fixed_signature_incidence": 16,
        "raw_core_codes": 1 << 18,
        "direct_red_k5_requirement_masks": red_mask_count,
        "noncomplete_word_codes": 117649,
        "locally_valid_codes": len(valid),
        "normalized_valid_codes": 3378,
        "full_normalizer_maps": 3888,
        "effective_core_maps": len(maps),
        "full_parent_primary_variables": primary_count,
        "core_cube_variables": core_variables,
        "later_core_fixing_normalizers": later_count,
        "core_classes": 197,
        "membership_sha256": membership_hash,
        "excluded_blue_k4_classes": excluded,
        "retained_classes": retained,
        "excluded_labeled_codes_direct": labeled_excluded,
        "retained_labeled_codes_direct": len(valid) - labeled_excluded,
        "classification_entrywise_match": True,
        "attachment_graphs_checked": 4 * (1 << 10),
        "allowed_attachment_masks_each_variant": 33,
        "attachment_rows": attachment_rows,
        "packing": packing,
        "row_capacity": 1,
        "column_demand": 2,
        "available_incidences": 7,
        "required_incidences": 12,
        "unresolved_four_versus_seven_classes": 79,
    }
    with args.report.open("w") as stream:
        dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(args.report)


if __name__ == "__main__":
    main()
