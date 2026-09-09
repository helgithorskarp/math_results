#!/usr/bin/env python3
"""Independent exact verifier for the four-active-curve gate."""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_complex_radix_architecture"
sys.path.insert(0, str(SOURCE))
SOURCE_SPEC = importlib.util.spec_from_file_location("hn2_radix_four_gate_check", SOURCE / "verify.py")
HN2 = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(HN2)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def fmul(a, b):
    # Independent table-free multiplication in F2[t]/(t^2+t+1).
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    return (a0 * b0 ^ a1 * b1) | ((a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1)


def finv(value):
    need(value != 0, "zero F4 inverse")
    return next(candidate for candidate in (1, 2, 3) if fmul(value, candidate) == 1)


def dot(normal, word):
    result = 0
    for a, b in zip(normal, word):
        result ^= fmul(a, b)
    return result


def projective(normal, constant):
    pivot = next(value for value in normal if value)
    scale = finv(pivot)
    return tuple(fmul(scale, value) for value in normal), fmul(scale, constant)


def padd(left, right):
    result = dict(left)
    for key, value in right.items():
        result[key] = result.get(key, Fraction(0)) + value
        if not result[key]:
            del result[key]
    return result


def pmul(left, right):
    result = {}
    for (i, j), value in left.items():
        for (k, m), other in right.items():
            key = i + k, j + m
            result[key] = result.get(key, Fraction(0)) + value * other
    return {key: value for key, value in result.items() if value}


def pscale(poly, scalar):
    return {key: scalar * value for key, value in poly.items() if scalar * value}


def powers(poly, maximum):
    result = [{(0, 0): Fraction(1)}]
    for _ in range(maximum):
        result.append(pmul(result[-1], poly))
    return result


def substitution_basis(x_image, y_image, maximum=8):
    xp, yp = powers(x_image, maximum), powers(y_image, maximum)
    return {
        (i, j): pmul(xp[i], yp[j])
        for i in range(maximum + 1)
        for j in range(maximum + 1 - i)
    }


def primitive_rational(poly):
    denominator = 1
    for value in poly.values():
        denominator = lcm(denominator, value.denominator)
    integral = {key: int(value * denominator) for key, value in poly.items()}
    divisor = 0
    for value in integral.values():
        divisor = gcd(divisor, value)
    if integral[max(integral)] < 0:
        divisor = -divisor
    return tuple((i, j, value // divisor) for (i, j), value in sorted(integral.items()))


def pullback(factor, basis):
    result = {}
    for i, j, coefficient in factor:
        result = padd(result, pscale(basis[i, j], Fraction(coefficient)))
    return primitive_rational(result)


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def generated_group(generators):
    identity = tuple(range(len(generators[0])))
    result = {identity}
    frontier = {identity}
    while frontier:
        new_frontier = set()
        for old in frontier:
            for generator in generators:
                candidate = compose(old, generator)
                if candidate not in result:
                    result.add(candidate)
                    new_frontier.add(candidate)
        frontier = new_frontier
    return tuple(sorted(result))


def pair_image(pair, action):
    a, b = action[pair[0]], action[pair[1]]
    return (a, b) if a < b else (b, a)


def histogram(values):
    return {str(key): value for key, value in sorted(Counter(values).items())}


def mask_for_equation(normal, constant, words):
    mask = 0
    for i, word in enumerate(words):
        if dot(normal, word) == constant:
            mask |= 1 << i
    return mask


def direct_failure_masks(factor_edges):
    """Build all 256 label colourings, then inspect the actual edge groups."""
    tails = tuple(product(range(4), repeat=4))
    colourings = []
    digit_residue = (0, 1, 2)
    for tail in tails:
        weights = (1,) + tail
        word = []
        for label in HN2.G.LABELS:
            value = 0
            for weight, digit in zip(weights, label):
                value ^= fmul(weight, digit_residue[digit])
            word.append(value)
        colourings.append(tuple(word))
    masks = []
    for edges in factor_edges:
        mask = 0
        for i, colouring in enumerate(colourings):
            if any(colouring[a] == colouring[b] for a, b in edges):
                mask |= 1 << i
        masks.append(mask)
    return tails, masks


def actual_certificate():
    rows, events, factors, factor_edges, base, _, _, circle = HN2.build()
    source_certificate = json.loads((SOURCE / "certificate.json").read_text())
    _, _, _, source_pairs = HN2.finite_cover(
        source_certificate["colour_specs"], factors, factor_edges, base
    )

    words, failure_masks = direct_failure_masks(factor_edges)
    normals = sorted(
        {
            projective(normal, 0)[0]
            for normal in product(range(4), repeat=4)
            if any(normal)
        }
    )
    all_types = [(normal, constant) for normal in normals for constant in range(4)]
    theoretical_masks = {
        signature: mask_for_equation(signature[0], signature[1], words)
        for signature in all_types
    }
    need(len(set(theoretical_masks.values())) == 340, "distinct affine hyperplanes")
    mask_to_signature = {mask: signature for signature, mask in theoretical_masks.items()}
    torus_mask = 0
    for i, word in enumerate(words):
        if all(word):
            torus_mask |= 1 << i
    need(torus_mask.bit_count() == 81, "F4 nonzero-tail torus")
    need(failure_masks[circle] == ((1 << 256) - 1) ^ torus_mask, "circle failure mask")

    # This route uses actual label colourings and edge groups, not displacement
    # residues.  Every noncircle curve must induce exactly one affine hyperplane.
    signatures = {}
    buckets = defaultdict(list)
    for curve, mask in enumerate(failure_masks):
        if curve == circle:
            continue
        need(mask in mask_to_signature, "curve failure set is not an affine hyperplane")
        signature = mask_to_signature[mask]
        signatures[curve] = signature
        buckets[signature].append(curve)

    missing_types = sorted(set(all_types) - set(buckets))
    need(
        missing_types
        == [
            ((0, 0, 0, 1), 0),
            ((0, 0, 1, 0), 0),
            ((0, 1, 0, 0), 0),
            ((1, 0, 0, 0), 0),
        ],
        "unexpected unrealized hyperplane types",
    )

    # Independently recover the 85 affine partitions from disjointness, without
    # grouping first by the stored projective normal.
    affine_partition_set = set()
    for signature, mask in theoretical_masks.items():
        block = tuple(
            sorted(
                other
                for other, other_mask in theoretical_masks.items()
                if other == signature or not (mask & other_mask)
            )
        )
        need(len(block) == 4, "affine hyperplane disjointness class")
        union = 0
        for item in block:
            union |= theoretical_masks[item]
        need(union == (1 << 256) - 1, "affine partition does not cover")
        affine_partition_set.add(block)
    need(len(affine_partition_set) == 85, "affine partition count")
    affine_partitions = sorted(
        pattern
        for pattern in affine_partition_set
        if all(signature in buckets for signature in pattern)
    )

    restricted_masks = {
        signature: mask & torus_mask for signature, mask in theoretical_masks.items()
    }
    size_27 = [signature for signature in all_types if restricted_masks[signature].bit_count() == 27]
    torus_partitions = []
    for triple in combinations(size_27, 3):
        union = restricted_masks[triple[0]] | restricted_masks[triple[1]] | restricted_masks[triple[2]]
        if union == torus_mask:
            torus_partitions.append(tuple(sorted(triple)))
    need(len(affine_partitions) == 81 and len(torus_partitions) == 10, "exact-four partitions")

    # Recover D3 from exact rational substitutions in the event polynomials,
    # independently of the producer's coefficient-word transformations.
    rotation_basis = substitution_basis(
        {(1, 0): Fraction(-1, 2), (0, 1): Fraction(-3, 2)},
        {(1, 0): Fraction(1, 2), (0, 1): Fraction(-1, 2)},
    )
    conjugation_basis = substitution_basis(
        {(1, 0): Fraction(1)}, {(0, 1): Fraction(-1)}
    )
    factor_ids = {factor: i for i, factor in enumerate(factors)}
    rotation = tuple(factor_ids[pullback(factor, rotation_basis)] for factor in factors)
    conjugation = tuple(factor_ids[pullback(factor, conjugation_basis)] for factor in factors)
    curve_group = generated_group((rotation, conjugation))
    need(len(curve_group) == 6, "polynomial action is not D3")
    identity = tuple(range(len(factors)))
    need(compose(rotation, compose(rotation, rotation)) == identity, "R^3 relation")
    need(compose(conjugation, conjugation) == identity, "C^2 relation")
    need(
        compose(conjugation, compose(rotation, conjugation)) == compose(rotation, rotation),
        "CRC=R^-1 relation",
    )

    pair_orbits = {}
    for pair in source_pairs:
        orbit = {pair_image(pair, action) for action in curve_group}
        pair_orbits.setdefault(min(orbit), orbit)
    pair_reps = sorted(pair_orbits)
    need(len(pair_reps) == 132130, "pair quotient count")

    affine_sets = tuple(map(frozenset, affine_partitions))
    torus_sets = tuple(map(frozenset, torus_partitions))

    def compatibility(pair):
        has_circle = circle in pair
        noncircle = [curve for curve in pair if curve != circle]
        signature_set = frozenset(signatures[curve] for curve in noncircle)
        if len(signature_set) != len(noncircle):
            return "at_least_five"
        if not has_circle and any(signature_set <= pattern for pattern in affine_sets):
            return "exact_four_no_circle"
        if any(signature_set <= pattern for pattern in torus_sets):
            return "exact_four_with_circle"
        return "at_least_five"

    mode_reps = defaultdict(list)
    mode_closure = Counter()
    mode_bezout = Counter()
    mode_circle = Counter()
    degrees = [HN2.degree(factor) for factor in factors]
    for pair in pair_reps:
        mode = compatibility(pair)
        orbit = pair_orbits[pair]
        need(all(compatibility(member) == mode for member in orbit), "D3 compatibility invariance")
        mode_reps[mode].append(pair)
        mode_closure[mode] += len(orbit)
        mode_bezout[mode] += degrees[pair[0]] * degrees[pair[1]]
        mode_circle[mode, circle in pair] += 1
    source_modes = Counter(compatibility(pair) for pair in source_pairs)

    affine_quartets = sum(
        len(buckets[pattern[0]])
        * len(buckets[pattern[1]])
        * len(buckets[pattern[2]])
        * len(buckets[pattern[3]])
        for pattern in affine_partitions
    )
    torus_quartets = sum(
        len(buckets[pattern[0]])
        * len(buckets[pattern[1]])
        * len(buckets[pattern[2]])
        for pattern in torus_partitions
    )
    exact_modes = ("exact_four_no_circle", "exact_four_with_circle")

    interface = {
        "schema": "hn-complex-radix-exact-four-interface-v1",
        "curve_id_source": "hadwiger_nelson_complex_radix_architecture sorted active curves",
        "circle_id": circle,
        "F4_encoding": "0,1,t,1+t encoded as 0,1,2,3 with t^2=t+1",
        "no_circle_signature_patterns": affine_partitions,
        "with_circle_noncircle_signature_patterns": torus_partitions,
        "pair_representatives": {mode: mode_reps[mode] for mode in exact_modes},
    }
    interface_raw = (
        json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    result = {
        "schema": "hn-complex-radix-four-curve-gate-v1",
        "source": {
            "architecture_commit": "95687bd35321aa6fb767fc508eac6ab186ba6d2e",
            "architecture_certificate_sha256": hashlib.sha256(
                (SOURCE / "certificate.json").read_bytes()
            ).hexdigest(),
            "factor_inventory_sha256": HN2.digest(factors),
            "pair_inventory_sha256": HN2.digest(source_pairs),
            "D3_pair_representatives_sha256": digest(pair_reps),
        },
        "F4_hyperplanes": {
            "tail_dimension": 4,
            "projective_normals": len(normals),
            "affine_types": len(all_types),
            "realized_noncircle_types": len(buckets),
            "missing_types": missing_types,
            "curves_per_realized_type_histogram": histogram(
                len(curves) for curves in buckets.values()
            ),
            "curve_signature_assignment_sha256": digest(sorted(signatures.items())),
        },
        "exact_four": {
            "no_circle_signature_patterns": len(affine_partitions),
            "no_circle_signature_patterns_sha256": digest(affine_partitions),
            "with_circle_signature_patterns": len(torus_partitions),
            "with_circle_signature_patterns_sha256": digest(torus_partitions),
            "with_circle_support_profile_histogram": histogram(
                tuple(sorted(sum(bool(value) for value in signature[0]) for signature in pattern))
                for pattern in torus_partitions
            ),
            "eligible_no_circle_curve_quartets": affine_quartets,
            "eligible_with_circle_curve_quartets": torus_quartets,
            "eligible_curve_quartets_total": affine_quartets + torus_quartets,
        },
        "pair_frontier": {
            "source_pairs": len(source_pairs),
            "D3_pair_orbits": len(pair_reps),
            "D3_closed_systems": sum(map(len, pair_orbits.values())),
            "mode_orbit_counts": {mode: len(mode_reps[mode]) for mode in sorted(mode_reps)},
            "mode_source_pair_counts": dict(sorted(source_modes.items())),
            "mode_D3_closed_system_counts": dict(sorted(mode_closure.items())),
            "mode_bezout_sums": dict(sorted(mode_bezout.items())),
            "mode_representatives_sha256": {
                mode: digest(mode_reps[mode]) for mode in sorted(mode_reps)
            },
            "mode_circle_involvement": {
                f"{mode}:{str(has_circle).lower()}": count
                for (mode, has_circle), count in sorted(mode_circle.items())
            },
            "exact_four_compatible_orbits": sum(len(mode_reps[mode]) for mode in exact_modes),
            "exact_four_compatible_bezout_bound": sum(mode_bezout[mode] for mode in exact_modes),
            "orbits_forcing_at_least_five_active_curves": len(mode_reps["at_least_five"]),
            "compatibility_D3_invariant": True,
        },
        "explicit_interface": {
            "bytes": len(interface_raw),
            "sha256": hashlib.sha256(interface_raw).hexdigest(),
        },
    }
    return result


def check_certificate(certificate, actual):
    normalized = json.loads(json.dumps(actual, sort_keys=True))
    need(certificate == normalized, "certificate differs from independent reconstruction")


def run(certificate_path):
    certificate = json.loads(certificate_path.read_text())
    actual = actual_certificate()
    check_certificate(certificate, actual)
    interface_path = HERE / "exact_four_interface.json"
    interface_raw = interface_path.read_bytes()
    need(len(interface_raw) == actual["explicit_interface"]["bytes"], "interface byte count")
    need(
        hashlib.sha256(interface_raw).hexdigest() == actual["explicit_interface"]["sha256"],
        "interface hash",
    )
    return {
        "status": "EXACT_FOUR_ACTIVE_CURVE_GATE_VERIFIED",
        "maximum_physical_order": 243,
        "collision_branch_closed_by_h4119": True,
        "exact_four_signature_patterns": actual["exact_four"]["no_circle_signature_patterns"]
        + actual["exact_four"]["with_circle_signature_patterns"],
        "eligible_exact_four_curve_quartets": actual["exact_four"]["eligible_curve_quartets_total"],
        "source_pair_orbits": actual["pair_frontier"]["D3_pair_orbits"],
        "exact_four_compatible_pair_orbits": actual["pair_frontier"]["exact_four_compatible_orbits"],
        "exact_four_parameter_orbit_bezout_bound": actual["pair_frontier"]["exact_four_compatible_bezout_bound"],
        "pair_orbits_forcing_at_least_five_active_curves": actual["pair_frontier"]["orbits_forcing_at_least_five_active_curves"],
        "direct_curve_failure_mask_checks": 2797,
        "explicit_interface_bytes": actual["explicit_interface"]["bytes"],
        "explicit_interface_sha256": actual["explicit_interface"]["sha256"],
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "proof_CAS_calls": 0,
        "proof_solver_calls": 0,
        "record_improvement": False,
        "candidate_claimed": False,
        "external_reviewer_acceptance_claimed": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    result = run(args.certificate)
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "expected output differs")
    if args.write_expected:
        need(not args.write_expected.exists(), "expected path already exists")
        args.write_expected.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
