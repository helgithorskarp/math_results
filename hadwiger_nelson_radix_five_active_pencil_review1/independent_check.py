#!/usr/bin/env python3
"""Independent checker for the h4171 exact-five affine-pencil frontier.

No h4171 module is imported.  The checker enumerates all two-dimensional
dual subspaces in RREF, reconstructs curves and incidence exclusions through
previous reviewer implementations, counts pencil lifts with an unrolled
bit-mask traversal, and validates every submitted extension witness.
"""

import argparse
from collections import Counter, defaultdict
from functools import reduce
from itertools import combinations, product
import hashlib
import importlib.util
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
FOUR_REVIEW_SOURCE = (
    HERE.parent
    / "hadwiger_nelson_radix_four_active_closure_review1"
    / "independent_check.py"
)
INCIDENCE_REVIEW_SOURCE = (
    HERE.parent
    / "hadwiger_nelson_radix_incidence_geometry_review1"
    / "independent_check.py"
)


def load(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


R4 = load("reviewer_h4151_inventory", FOUR_REVIEW_SOURCE)
RI = load("reviewer_h4167_incidence", INCIDENCE_REVIEW_SOURCE)

EXPECTED_TARGET_INTERFACE_FILE_SHA256 = (
    "fc12122b45703c2cd04a0f064a7f225081ac065c917118888679723106a97b7d"
)
EXPECTED_TARGET_INTERFACE_CANONICAL_SHA256 = (
    "eb03a45aa30f2ce0bd1b4989f72413001522b6eedbc329f0273427f94bdf3e20"
)
EXPECTED_QUOTIENT_FILE_SHA256 = (
    "90e6235fcd71a8998fe6c4229882f383fe9d18c7c3dd6c66cca9098fa5057998"
)
EXPECTED_PAIR_REPRESENTATIVES_SHA256 = (
    "ab9d291e1b59a234712eb9ef95aaeb70654921351542b825afeee887b118ccd6"
)
EXPECTED_REALIZED_PENCIL_SHA256 = (
    "bc43768f6eb36484fff008c505c72db554ba01076975e1a81cf1a2b1a821d0d0"
)
EXPECTED_LIFT_TRANSCRIPT_SHA256 = (
    "39615363ecd4c5d16ad997dac6b63d1f77e28d913c9b660276f7ac98943c9c5e"
)
EXPECTED_WITNESS_TRANSCRIPT_SHA256 = (
    "6d6663e8e7aba000969424640ad6775a90cfea3afee485f9b5957db655589d17"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def fmul(left, right):
    """Multiply in F4=F2[w]/(w^2+w+1), encoded 0,1,w,1+w."""
    a0, a1 = left & 1, left >> 1
    b0, b1 = right & 1, right >> 1
    return (a0 * b0 ^ a1 * b1) | (
        (a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1
    )


def fscale(scalar, vector):
    return tuple(fmul(scalar, entry) for entry in vector)


def fadd(left, right):
    return tuple(a ^ b for a, b in zip(left, right))


def normalize_affine_form(normal, constant):
    pivot = next(entry for entry in normal if entry)
    inverse = next(value for value in (1, 2, 3) if fmul(value, pivot) == 1)
    return fscale(inverse, normal), fmul(inverse, constant)


def rref_two_subspaces():
    """Enumerate the 2-subspaces of F4^4 by unique 2x4 RREF bases."""
    bases = []
    for first_pivot, second_pivot in combinations(range(4), 2):
        variables = []
        for column in range(first_pivot + 1, 4):
            if column != second_pivot:
                variables.append((0, column))
        for column in range(second_pivot + 1, 4):
            variables.append((1, column))
        for values in product(range(4), repeat=len(variables)):
            rows = [[0] * 4 for _ in range(2)]
            rows[0][first_pivot] = 1
            rows[1][second_pivot] = 1
            for (row, column), value in zip(variables, values):
                rows[row][column] = value
            bases.append((tuple(rows[0]), tuple(rows[1])))
    require(len(bases) == 357 and len(set(bases)) == 357, "RREF 2-subspace census")
    return tuple(bases)


PROJECTIVE_COEFFICIENTS = tuple((1, value) for value in range(4)) + ((0, 1),)


def pencil_from_rref(basis, constants):
    forms = []
    for left, right in PROJECTIVE_COEFFICIENTS:
        normal = fadd(fscale(left, basis[0]), fscale(right, basis[1]))
        constant = fmul(left, constants[0]) ^ fmul(right, constants[1])
        forms.append(normalize_affine_form(normal, constant))
    result = tuple(sorted(forms))
    require(len(set(result)) == 5, "RREF pencil lacks five directions")
    return result


def all_rref_pencils():
    pencils = sorted(
        pencil_from_rref(basis, constants)
        for basis in rref_two_subspaces()
        for constants in product(range(4), repeat=2)
    )
    require(len(pencils) == 357 * 16 == 5712, "abstract pencil census")
    require(len(set(pencils)) == len(pencils), "duplicate RREF pencils")
    return pencils


def theoretical_hyperplanes_and_masks():
    words = tuple(product(range(4), repeat=4))
    normals = sorted(
        {
            normalize_affine_form(normal, 0)[0]
            for normal in product(range(4), repeat=4)
            if any(normal)
        }
    )
    signatures = tuple(
        (normal, constant) for normal in normals for constant in range(4)
    )
    masks = {}
    for signature in signatures:
        normal, constant = signature
        mask = 0
        for index, word in enumerate(words):
            value = 0
            for left, right in zip(normal, word):
                value ^= fmul(left, right)
            if value == constant:
                mask |= 1 << index
        masks[signature] = mask
    require(len(normals) == 85 and len(signatures) == 340, "theoretical hyperplanes")
    require(len(set(masks.values())) == 340, "hyperplane masks are not unique")
    require(all(mask.bit_count() == 64 for mask in masks.values()), "hyperplane size")
    return words, normals, signatures, masks


def affine_plane_control():
    words = tuple(product(range(4), repeat=2))
    normals = sorted(
        {
            normalize_affine_form(normal, 0)[0]
            for normal in words
            if any(normal)
        }
    )
    lines = tuple((normal, constant) for normal in normals for constant in range(4))
    masks = {}
    for line in lines:
        mask = 0
        for index, word in enumerate(words):
            value = fmul(line[0][0], word[0]) ^ fmul(line[0][1], word[1])
            if value == line[1]:
                mask |= 1 << index
        masks[line] = mask
    full = (1 << 16) - 1
    profiles = Counter()
    covers = 0
    for family in combinations(lines, 5):
        union = 0
        for line in family:
            union |= masks[line]
        if union != full:
            continue
        covers += 1
        multiplicities = Counter(normal for normal, _ in family)
        profiles[tuple(sorted(multiplicities.values(), reverse=True))] += 1
    require(covers == 96, "AG(2,4) five-line cover census")
    require(profiles == {(4, 1): 80, (1, 1, 1, 1, 1): 16}, "AG(2,4) cover profiles")
    return covers, profiles


def make_owner(monomial_rows, row_to_curve, circle):
    def owner(row):
        normalized = R4.canonical_row(row)
        if normalized in monomial_rows:
            return None if monomial_rows[normalized] == 0 else circle
        return row_to_curve[normalized]

    return owner


def reconstruct_incidence_constraints(owner, circle):
    _, forbidden, raw_pairs, rule_applications = RI.enumerate_phase_exclusions(
        owner, circle
    )
    _, offset_pairs = RI.enumerate_offset_pairs(owner, circle)
    collision_pairs = {entry for entry in forbidden if len(entry) == 2}
    triples = {entry for entry in forbidden if len(entry) == 3}
    pair_constraints = collision_pairs | set(offset_pairs)
    require(len(collision_pairs) == 5976, "collision pair census")
    require(len(triples) == 176420, "collision triple census")
    require(len(offset_pairs) == len(pair_constraints) == 8376, "pair constraint census")
    require(collision_pairs <= set(offset_pairs), "collision pairs not contained in offsets")
    return pair_constraints, triples, raw_pairs, rule_applications


def constraint_masks(curve_count, pairs, triples):
    pair_bad = [0] * curve_count
    for left, right in pairs:
        pair_bad[left] |= 1 << right
        pair_bad[right] |= 1 << left
    triple_bad = {}
    for triple in triples:
        for left, right in combinations(triple, 2):
            remaining = next(curve for curve in triple if curve not in (left, right))
            key = tuple(sorted((left, right)))
            triple_bad[key] = triple_bad.get(key, 0) | (1 << remaining)
    return pair_bad, triple_bad


def extend_forbidden(chosen, forbidden, curve, pair_bad, triple_bad):
    result = forbidden | pair_bad[curve]
    for old in chosen:
        result |= triple_bad.get(tuple(sorted((old, curve))), 0)
    return result


def iter_bits(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length() - 1


def count_safe_quintets(domains, pair_bad, triple_bad):
    """Unrolled traversal; the largest bucket is reserved for bit counting."""
    last_index = max(range(5), key=lambda index: domains[index].bit_count())
    ordered = [domains[index] for index in range(5) if index != last_index]
    ordered.append(domains[last_index])
    first, second, third, fourth, fifth = ordered
    total = 0
    for a in iter_bits(first):
        forbidden_a = extend_forbidden((), 0, a, pair_bad, triple_bad)
        for b in iter_bits(second & ~forbidden_a):
            selected_ab = (a, b)
            forbidden_ab = extend_forbidden((a,), forbidden_a, b, pair_bad, triple_bad)
            for c in iter_bits(third & ~forbidden_ab):
                selected_abc = selected_ab + (c,)
                forbidden_abc = extend_forbidden(
                    selected_ab, forbidden_ab, c, pair_bad, triple_bad
                )
                for d in iter_bits(fourth & ~forbidden_abc):
                    forbidden_abcd = extend_forbidden(
                        selected_abc, forbidden_abc, d, pair_bad, triple_bad
                    )
                    total += (fifth & ~forbidden_abcd).bit_count()
    return total


def reconstruct_lift_frontier(realized_pencils, buckets, pairs, triples, curve_count):
    bucket_masks = {
        signature: sum(1 << curve for curve in curves)
        for signature, curves in buckets.items()
    }
    signature_by_curve = {
        curve: signature
        for signature, curves in buckets.items()
        for curve in curves
    }
    pencil_for_pair = {}
    for pencil in realized_pencils:
        for pair in combinations(pencil, 2):
            key = tuple(sorted(pair))
            require(key not in pencil_for_pair, "two pencils through a signature pair")
            pencil_for_pair[key] = pencil

    # Every accepted pair rule is structurally orthogonal to a realized pencil.
    for left, right in pairs:
        signatures = tuple(sorted((signature_by_curve[left], signature_by_curve[right])))
        require(signatures not in pencil_for_pair, "pair rule removes a pencil lift")

    pair_bad, triple_bad = constraint_masks(curve_count, pairs, triples)
    raw_total = 0
    safe_total = 0
    empty_pencils = 0
    profile_counts = defaultdict(lambda: [0, 0, 0, 0])
    transcript = hashlib.sha256()
    for pencil in realized_pencils:
        domains = [bucket_masks[signature] for signature in pencil]
        raw = math.prod(domain.bit_count() for domain in domains)
        safe = count_safe_quintets(domains, pair_bad, triple_bad)
        raw_total += raw
        safe_total += safe
        empty_pencils += safe == 0
        profile = tuple(
            sorted(sum(bool(coordinate) for coordinate in signature[0]) for signature in pencil)
        )
        record = profile_counts[profile]
        record[0] += 1
        record[1] += raw
        record[2] += raw
        record[3] += safe
        transcript.update(
            json.dumps([pencil, raw, raw, safe], separators=(",", ":")).encode()
            + b"\n"
        )
    return {
        "raw": raw_total,
        "after_pairs": raw_total,
        "after_triples": safe_total,
        "empty_after_pairs": 0,
        "empty_after_triples": empty_pencils,
        "profile_counts": {str(key): value for key, value in sorted(profile_counts.items())},
        "transcript_sha256": transcript.hexdigest(),
        "bucket_masks": bucket_masks,
        "signature_by_curve": signature_by_curve,
        "pencil_for_pair": pencil_for_pair,
        "pair_bad": pair_bad,
        "triple_bad": triple_bad,
    }


def load_quotient(path, factors):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_QUOTIENT_FILE_SHA256, "quotient file hash")
    quotient = json.loads(raw)
    representatives = quotient["pair_system_representatives"]
    require(len(representatives) == 132130, "h4117 pair census")
    require(digest(representatives) == EXPECTED_PAIR_REPRESENTATIVES_SHA256, "h4117 pair digest")
    require(representatives == sorted(representatives), "h4117 pair ordering")
    require(len({tuple(pair) for pair in representatives}) == len(representatives), "duplicate h4117 pair")
    require(
        all(
            len(pair) == 2
            and pair[0] < pair[1]
            and 0 <= pair[0] < len(factors)
            and 0 <= pair[1] < len(factors)
            for pair in representatives
        ),
        "h4117 pair domain",
    )
    return representatives


def classify_pair_frontier(representatives, factors, circle, pairs, signature_by_curve, pencil_for_pair):
    retained = [
        pair
        for pair in representatives
        if circle not in pair and tuple(pair) not in pairs
    ]
    modes = defaultdict(list)
    allowances = Counter()
    degrees = [max(i + j for i, j, _ in polynomial) for polynomial in factors]
    for pair in retained:
        left_signature = signature_by_curve[pair[0]]
        right_signature = signature_by_curve[pair[1]]
        if left_signature[0] == right_signature[0]:
            mode = "parallel_signatures_require_at_least_six"
        elif tuple(sorted((left_signature, right_signature))) not in pencil_for_pair:
            mode = "unrealized_pencil_type_requires_at_least_six"
        else:
            mode = "exact_five_compatible"
        modes[mode].append(pair)
        allowances[mode] += degrees[pair[0]] * degrees[pair[1]]
    return retained, dict(modes), allowances


def validate_target_interface(
    path,
    factors,
    circle,
    realized_pencils,
    signature_by_curve,
    modes,
    pencil_for_pair,
    pair_constraints,
    triple_constraints,
):
    raw = path.read_bytes()
    require(
        hashlib.sha256(raw).hexdigest() == EXPECTED_TARGET_INTERFACE_FILE_SHA256,
        "target interface file hash",
    )
    interface = json.loads(raw)
    require(digest(interface) == EXPECTED_TARGET_INTERFACE_CANONICAL_SHA256, "target interface canonical hash")
    require(interface["schema"] == "hn-radix-five-active-pencil-interface-v1", "interface schema")
    require(interface["curve_inventory_sha256"] == digest(factors), "interface curve inventory")
    require(interface["circle_id"] == circle, "interface circle")
    expected_signatures = [
        None if curve == circle else signature_by_curve[curve]
        for curve in range(len(factors))
    ]
    require(interface["curve_signatures"] == json.loads(json.dumps(expected_signatures)), "curve signatures")
    require(interface["realized_pencil_signatures"] == json.loads(json.dumps(realized_pencils)), "realized pencils")
    require(interface["pair_representatives"] == modes, "pair modes differ entrywise")

    exact_pairs = modes["exact_five_compatible"]
    witnesses = interface["constraint_avoiding_extension_witnesses"]
    require(len(witnesses) == len(exact_pairs), "extension witness count")
    transcript = hashlib.sha256()
    for expected_pair, record in zip(exact_pairs, witnesses):
        base, witness = record
        require(base == expected_pair, "extension witness pair order")
        require(witness == sorted(set(witness)) and len(witness) == 5, "extension witness shape")
        require(set(base) <= set(witness), "extension omits base pair")
        witness_signatures = {signature_by_curve[curve] for curve in witness}
        base_key = tuple(sorted((signature_by_curve[base[0]], signature_by_curve[base[1]])))
        require(witness_signatures == set(pencil_for_pair[base_key]), "extension does not fill its pencil")
        require(
            all(tuple(sorted(pair)) not in pair_constraints for pair in combinations(witness, 2)),
            "extension contains a forbidden pair",
        )
        require(
            all(tuple(sorted(triple)) not in triple_constraints for triple in combinations(witness, 3)),
            "extension contains a forbidden triple",
        )
        transcript.update(json.dumps(record, separators=(",", ":")).encode() + b"\n")
    require(transcript.hexdigest() == EXPECTED_WITNESS_TRANSCRIPT_SHA256, "witness transcript hash")
    return interface, len(witnesses), transcript.hexdigest()


def main(target_interface_path, four_interface_path, quotient_path):
    plane_cover_count, plane_profiles = affine_plane_control()
    words, normals, theoretical_signatures, theoretical_masks = theoretical_hyperplanes_and_masks()
    abstract_pencils = all_rref_pencils()
    full_mask = (1 << len(words)) - 1
    require(
        all(
            reduce(
                int.__or__, (theoretical_masks[item] for item in pencil), 0
            )
            == full_mask
            for pencil in abstract_pencils
        ),
        "RREF pencil fails to cover F4^4",
    )

    rows, factors, circle, monomial_rows, row_to_curve = R4.reconstruct_inventory()
    words3, words4, bad3, buckets, realized_masks, partition_patterns = R4.build_colour_data(
        row_to_curve
    )
    owner_counts = R4.direct_label_pair_audit(
        monomial_rows, row_to_curve, circle, words3, words4, bad3, realized_masks
    )
    obstruction_lookup, obstruction_arities = R4.load_and_check_obstructions(
        four_interface_path, monomial_rows, row_to_curve, circle
    )

    realized_signatures = set(buckets)
    missing_histogram = Counter(
        sum(signature not in realized_signatures for signature in pencil)
        for pencil in abstract_pencils
    )
    realized_pencils = [
        pencil
        for pencil in abstract_pencils
        if all(signature in realized_signatures for signature in pencil)
    ]
    require(missing_histogram == {0: 5382, 1: 324, 2: 6}, "missing-type pencil census")
    require(digest(realized_pencils) == EXPECTED_REALIZED_PENCIL_SHA256, "realized pencil digest")
    require(len(partition_patterns) == 81, "realized partition census")

    signature_by_curve = {
        curve: signature
        for signature, curves in buckets.items()
        for curve in curves
    }
    require(
        all(
            len({signature_by_curve[curve][0] for curve in obstruction}) == 1
            for obstruction in obstruction_lookup
        ),
        "h4151 obstruction crosses pencil directions",
    )

    owner = make_owner(monomial_rows, row_to_curve, circle)
    pair_constraints, triple_constraints, raw_disjoint_pairs, _rule_applications = (
        reconstruct_incidence_constraints(owner, circle)
    )
    lift = reconstruct_lift_frontier(
        realized_pencils,
        buckets,
        pair_constraints,
        triple_constraints,
        len(factors),
    )
    require(lift["raw"] == lift["after_pairs"] == 136094976, "raw/pair lift census")
    require(lift["after_triples"] == 132232896, "triple-pruned lift census")
    require(lift["empty_after_triples"] == 0, "empty realized pencil")
    require(lift["transcript_sha256"] == EXPECTED_LIFT_TRANSCRIPT_SHA256, "lift transcript")

    representatives = load_quotient(quotient_path, factors)
    retained, modes, allowances = classify_pair_frontier(
        representatives,
        factors,
        circle,
        pair_constraints,
        lift["signature_by_curve"],
        lift["pencil_for_pair"],
    )
    require(len(retained) == 131356, "retained pair frontier")
    require(
        {mode: len(items) for mode, items in modes.items()}
        == {
            "exact_five_compatible": 128616,
            "parallel_signatures_require_at_least_six": 2096,
            "unrealized_pencil_type_requires_at_least_six": 644,
        },
        "pair mode census",
    )
    require(
        dict(allowances)
        == {
            "exact_five_compatible": 7585472,
            "parallel_signatures_require_at_least_six": 129952,
            "unrealized_pencil_type_requires_at_least_six": 39104,
        },
        "pair mode allowances",
    )

    interface, witness_count, witness_transcript = validate_target_interface(
        target_interface_path,
        factors,
        circle,
        realized_pencils,
        lift["signature_by_curve"],
        modes,
        lift["pencil_for_pair"],
        pair_constraints,
        triple_constraints,
    )

    output = {
        "schema": "hn-radix-five-active-pencil-independent-review-v1",
        "AG_2_4_five_line_subsets_checked": math.comb(20, 5),
        "AG_2_4_five_line_covers": plane_cover_count,
        "AG_2_4_cover_profiles": {
            str(key): value for key, value in sorted(plane_profiles.items())
        },
        "RREF_two_subspaces": len(rref_two_subspaces()),
        "abstract_pencils": len(abstract_pencils),
        "abstract_partition_plus_extra_covers": len(normals) * (len(theoretical_signatures) - 4),
        "abstract_five_covers": len(abstract_pencils) + len(normals) * (len(theoretical_signatures) - 4),
        "realized_hyperplanes": len(buckets),
        "realized_partition_plus_extra_covers": len(partition_patterns) * (len(buckets) - 4),
        "realized_pencils": len(realized_pencils),
        "realized_five_covers": len(realized_pencils) + len(partition_patterns) * (len(buckets) - 4),
        "pencils_by_missing_type_count": {
            str(key): value for key, value in sorted(missing_histogram.items())
        },
        "realized_pencil_sha256": digest(realized_pencils),
        "label_pairs_audited": sum(owner_counts.values()),
        "h4151_obstruction_arity_histogram": {
            str(key): value for key, value in sorted(obstruction_arities.items())
        },
        "all_h4151_obstructions_parallel_normal": True,
        "h4167_raw_disjoint_states": raw_disjoint_pairs,
        "h4167_pair_constraints": len(pair_constraints),
        "h4167_triple_constraints": len(triple_constraints),
        "raw_pencil_quintets": lift["raw"],
        "after_h4167_pair_constraints": lift["after_pairs"],
        "after_h4167_triple_constraints": lift["after_triples"],
        "pencils_empty_after_constraints": lift["empty_after_triples"],
        "lift_profile_counts": lift["profile_counts"],
        "lift_transcript_sha256": lift["transcript_sha256"],
        "h4117_pair_representatives_imported": len(representatives),
        "retained_pair_representatives": len(retained),
        "pair_mode_counts": {mode: len(items) for mode, items in sorted(modes.items())},
        "pair_mode_allowances": dict(sorted(allowances.items())),
        "pair_mode_sha256": {mode: digest(items) for mode, items in sorted(modes.items())},
        "extension_witnesses_validated": witness_count,
        "extension_witness_transcript_sha256": witness_transcript,
        "target_interface_bytes": len(target_interface_path.read_bytes()),
        "target_interface_file_sha256": hashlib.sha256(target_interface_path.read_bytes()).hexdigest(),
        "target_interface_canonical_sha256": digest(interface),
        "partition_branch_requires_accepted_h4165": True,
        "pair_frontier_conditional_on_h4117": True,
        "six_active_gate_closed": False,
        "record_improvement": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-interface", type=Path, required=True)
    parser.add_argument("--four-interface", type=Path, required=True)
    parser.add_argument("--quotient", type=Path, required=True)
    arguments = parser.parse_args()
    main(arguments.target_interface, arguments.four_interface, arguments.quotient)
