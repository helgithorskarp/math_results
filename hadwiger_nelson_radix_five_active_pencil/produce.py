#!/usr/bin/env python3
"""Produce the exact five-active affine-pencil frontier for A5(z)."""

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARCH = ROOT / "hadwiger_nelson_complex_radix_architecture"
sys.path.insert(0, str(ARCH))
import geometry as G  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D3 = load("five_pencil_d3_producer", ROOT / "hadwiger_nelson_complex_radix_d3_quotient" / "produce.py")
FOUR = load("five_pencil_four_producer", ROOT / "hadwiger_nelson_radix_four_active_closure" / "produce.py")
INCIDENCE = load("five_pencil_incidence_producer", ROOT / "hadwiger_nelson_radix_incidence_geometry" / "produce.py")


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def fmul(a, b):
    a0, a1 = a & 1, a >> 1
    b0, b1 = b & 1, b >> 1
    return (a0 * b0 ^ a1 * b1) | (
        (a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1
    )


def projective(normal, constant):
    pivot = next(value for value in normal if value)
    inverse = next(value for value in (1, 2, 3) if fmul(pivot, value) == 1)
    return tuple(fmul(inverse, value) for value in normal), fmul(inverse, constant)


def signature(row):
    values = tuple((a & 1) | ((b & 1) << 1) for a, b in row)
    return projective(values[1:], values[0])


def combine(left, right, a, b):
    normal = tuple(
        fmul(a, x) ^ fmul(b, y)
        for x, y in zip(left[0], right[0])
    )
    constant = fmul(a, left[1]) ^ fmul(b, right[1])
    return projective(normal, constant)


def pencil(left, right):
    result = {
        combine(left, right, 1, 0),
        combine(left, right, 0, 1),
    }
    result.update(combine(left, right, 1, value) for value in range(4))
    if len(result) != 5:
        raise ValueError("two nonparallel affine forms do not generate five pencil sections")
    return tuple(sorted(result))


def source_interfaces():
    with tempfile.TemporaryDirectory(prefix="hn-five-pencil-") as directory:
        directory = Path(directory)
        four_path = directory / "four.json"
        incidence_path = directory / "incidence.json"
        FOUR.compute(four_path)
        INCIDENCE.compute(incidence_path)
        return json.loads(four_path.read_text()), json.loads(incidence_path.read_text())


def constraint_tables(factor_count, four_interface, incidence_interface, signatures):
    four_sets = [
        tuple(curves)
        for curves, _ in four_interface["forbidden_curve_sets_with_K4_labels"]
    ]
    if not all(len({signatures[curve][0] for curve in curves}) == 1 for curves in four_sets):
        raise ValueError("h4151 obstruction spans distinct projective normals")

    pair_sets = {
        tuple(sorted(curves))
        for curves in incidence_interface["injectivity_excluded_sets"]
        if len(curves) == 2
    }
    pair_sets.update(
        tuple(sorted(curves))
        for curves in incidence_interface["monic_degree_four_excluded_pairs"]
    )
    triple_sets = {
        tuple(sorted(curves))
        for curves in incidence_interface["injectivity_excluded_sets"]
        if len(curves) == 3
    }
    pair_bad = [0] * factor_count
    for a, b in pair_sets:
        pair_bad[a] |= 1 << b
        pair_bad[b] |= 1 << a
    triple_bad = {}
    for triple in triple_sets:
        for a, b in combinations(triple, 2):
            c = next(curve for curve in triple if curve not in (a, b))
            triple_bad[a, b] = triple_bad.get((a, b), 0) | (1 << c)
    return four_sets, pair_sets, triple_sets, pair_bad, triple_bad


def add_constraint_mask(selected, old_mask, new_curve, pair_bad, triple_bad):
    result = old_mask | pair_bad[new_curve]
    for curve in selected:
        key = tuple(sorted((curve, new_curve)))
        result |= triple_bad.get(key, 0)
    return result


def count_lifts(pencil_signatures, bucket_masks, pair_bad, triple_bad, use_triples):
    domains = sorted(
        (bucket_masks[item] for item in pencil_signatures),
        key=lambda mask: (mask.bit_count(), mask),
    )

    def visit(index, selected, forbidden):
        available = domains[index] & ~forbidden
        if index == 4:
            return available.bit_count()
        result = 0
        while available:
            bit = available & -available
            available ^= bit
            curve = bit.bit_length() - 1
            next_forbidden = forbidden | pair_bad[curve]
            if use_triples:
                for old in selected:
                    next_forbidden |= triple_bad.get(tuple(sorted((old, curve))), 0)
            result += visit(index + 1, selected + (curve,), next_forbidden)
        return result

    return visit(0, (), 0)


def extension_witness(base_pair, pencil_signatures, buckets, pair_bad, triple_bad):
    left, right = base_pair
    base_signatures = {buckets["signature_by_curve"][left], buckets["signature_by_curve"][right]}
    domains = sorted(
        (
            buckets["mask_by_signature"][item]
            for item in pencil_signatures
            if item not in base_signatures
        ),
        key=lambda mask: (mask.bit_count(), mask),
    )
    selected = (left, right)
    forbidden = pair_bad[left] | pair_bad[right] | triple_bad.get(base_pair, 0)

    def visit(index, chosen, bad):
        available = domains[index] & ~bad
        while available:
            bit = available & -available
            available ^= bit
            curve = bit.bit_length() - 1
            new_chosen = chosen + (curve,)
            if index == 2:
                return tuple(sorted(new_chosen))
            new_bad = add_constraint_mask(chosen, bad, curve, pair_bad, triple_bad)
            result = visit(index + 1, new_chosen, new_bad)
            if result is not None:
                return result
        return None

    return visit(0, selected, forbidden)


def make_certificate(export_interface=None):
    d3_certificate, d3_data = D3.compute()
    rows, events, factors, factor_edges, base, _, _, circle = D3.HN2.build()
    factor_ids = {factor: index for index, factor in enumerate(factors)}
    representative_rows = {}
    for row, event in zip(rows, events):
        if event:
            representative_rows.setdefault(factor_ids[event], row)
    if len(representative_rows) != len(factors):
        raise ValueError("curve representative inventory")

    signatures = {
        curve: signature(row)
        for curve, row in representative_rows.items()
        if curve != circle
    }
    curve_buckets = defaultdict(list)
    for curve, item in signatures.items():
        curve_buckets[item].append(curve)
    bucket_masks = {
        item: sum(1 << curve for curve in curves)
        for item, curves in curve_buckets.items()
    }

    normals = sorted(
        {
            projective(normal, 0)[0]
            for normal in product(range(4), repeat=4)
            if any(normal)
        }
    )
    all_signatures = [(normal, constant) for normal in normals for constant in range(4)]
    all_pencils = set()
    for index, left in enumerate(all_signatures):
        for right in all_signatures[index + 1 :]:
            if left[0] != right[0]:
                all_pencils.add(pencil(left, right))
    all_pencils = sorted(all_pencils)
    missing_histogram = Counter(
        sum(item not in curve_buckets for item in pattern)
        for pattern in all_pencils
    )
    realized_pencils = [
        pattern for pattern in all_pencils if all(item in curve_buckets for item in pattern)
    ]
    pencil_for_pair = {
        tuple(sorted(pair)): pattern
        for pattern in realized_pencils
        for pair in combinations(pattern, 2)
    }

    four_interface, incidence_interface = source_interfaces()
    four_sets, pair_sets, triple_sets, pair_bad, triple_bad = constraint_tables(
        len(factors), four_interface, incidence_interface, signatures
    )

    lift_transcript = hashlib.sha256()
    raw_lifts = pair_survivors = full_survivors = 0
    zero_after_pairs = zero_after_triples = 0
    profile_counts = defaultdict(lambda: [0, 0, 0, 0])
    for pattern in realized_pencils:
        raw = math.prod(len(curve_buckets[item]) for item in pattern)
        after_pairs = count_lifts(pattern, bucket_masks, pair_bad, {}, False)
        after_triples = count_lifts(pattern, bucket_masks, pair_bad, triple_bad, True)
        raw_lifts += raw
        pair_survivors += after_pairs
        full_survivors += after_triples
        zero_after_pairs += after_pairs == 0
        zero_after_triples += after_triples == 0
        profile = tuple(sorted(sum(bool(value) for value in item[0]) for item in pattern))
        aggregate = profile_counts[profile]
        aggregate[0] += 1
        aggregate[1] += raw
        aggregate[2] += after_pairs
        aggregate[3] += after_triples
        lift_transcript.update(
            json.dumps(
                [pattern, raw, after_pairs, after_triples], separators=(",", ":")
            ).encode()
            + b"\n"
        )

    degrees = [D3.HN2.degree(factor) for factor in factors]
    retained_pairs = [
        pair
        for pair in d3_data["pair_representatives"]
        if circle not in pair and tuple(pair) not in pair_sets
    ]
    modes = defaultdict(list)
    allowances = Counter()
    closure_counts = Counter()
    witness_transcript = hashlib.sha256()
    witnesses = []
    signature_by_curve = {
        "signature_by_curve": signatures,
        "mask_by_signature": bucket_masks,
    }
    for pair in retained_pairs:
        left, right = pair
        left_signature, right_signature = signatures[left], signatures[right]
        if left_signature[0] == right_signature[0]:
            mode = "parallel_signatures_require_at_least_six"
        else:
            key = tuple(sorted((left_signature, right_signature)))
            if key not in pencil_for_pair:
                mode = "unrealized_pencil_type_requires_at_least_six"
            else:
                mode = "exact_five_compatible"
                witness = extension_witness(
                    tuple(pair),
                    pencil_for_pair[key],
                    signature_by_curve,
                    pair_bad,
                    triple_bad,
                )
                if witness is None:
                    raise ValueError(f"constraint-infeasible exact-five pair {pair}")
                witnesses.append([list(pair), list(witness)])
                witness_transcript.update(
                    json.dumps([list(pair), list(witness)], separators=(",", ":")).encode()
                    + b"\n"
                )
        modes[mode].append(list(pair))
        allowances[mode] += degrees[left] * degrees[right]
        closure_counts[mode] += len(
            {D3.pair_image(pair, action) for action in d3_data["curve_group"]}
        )

    # The property must descend to global D3 representatives.
    structural_mode = {}
    for mode, pairs in modes.items():
        for pair in pairs:
            structural_mode[tuple(pair)] = mode
    for pair, mode in structural_mode.items():
        for member in {D3.pair_image(pair, action) for action in d3_data["curve_group"]}:
            left, right = member
            s, t = signatures[left], signatures[right]
            if s[0] == t[0]:
                member_mode = "parallel_signatures_require_at_least_six"
            elif tuple(sorted((s, t))) not in pencil_for_pair:
                member_mode = "unrealized_pencil_type_requires_at_least_six"
            else:
                member_mode = "exact_five_compatible"
            if member_mode != mode:
                raise ValueError("five-pencil mode is not D3 invariant")

    interface = {
        "schema": "hn-radix-five-active-pencil-interface-v1",
        "curve_inventory_sha256": digest(factors),
        "circle_id": circle,
        "realized_pencil_signatures": realized_pencils,
        "curve_signatures": [
            None if curve == circle else signatures[curve]
            for curve in range(len(factors))
        ],
        "pair_representatives": {
            mode: pairs for mode, pairs in sorted(modes.items())
        },
        "constraint_avoiding_extension_witnesses": witnesses,
        "scope": (
            "Global h4117 representatives after h4139 and h4167. Exact-five compatibility "
            "is necessary only for a counterexample with exactly five active noncircle curves; "
            "it does not exclude parameters with six or more active curves. Representatives "
            "must be solved globally and cannot be combined with a chamber restriction."
        ),
    }
    if export_interface is not None:
        path = Path(export_interface)
        if path.exists():
            raise FileExistsError(path)
        path.write_text(json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n")

    exact_mode = "exact_five_compatible"
    parallel_mode = "parallel_signatures_require_at_least_six"
    missing_mode = "unrealized_pencil_type_requires_at_least_six"
    return {
        "schema": "hn-radix-five-active-pencil-v1",
        "sources": {
            "architecture_certificate_sha256": hashlib.sha256(
                (ARCH / "certificate.json").read_bytes()
            ).hexdigest(),
            "d3_certificate_sha256": hashlib.sha256(
                (ROOT / "hadwiger_nelson_complex_radix_d3_quotient" / "certificate.json").read_bytes()
            ).hexdigest(),
            "four_active_certificate_sha256": hashlib.sha256(
                (ROOT / "hadwiger_nelson_radix_four_active_closure" / "certificate.json").read_bytes()
            ).hexdigest(),
            "four_concurrence_certificate_sha256": hashlib.sha256(
                (ROOT / "hadwiger_nelson_complex_radix_four_concurrence" / "certificate.json").read_bytes()
            ).hexdigest(),
            "incidence_geometry_certificate_sha256": hashlib.sha256(
                (ROOT / "hadwiger_nelson_radix_incidence_geometry" / "certificate.json").read_bytes()
            ).hexdigest(),
        },
        "affine_cover_classification": {
            "field_order": 4,
            "dimension": 4,
            "theoretical_hyperplanes": len(all_signatures),
            "realized_hyperplanes": len(curve_buckets),
            "abstract_five_covers": 85 * 336 + len(all_pencils),
            "abstract_partition_plus_extra_covers": 85 * 336,
            "abstract_pencil_covers": len(all_pencils),
            "realized_five_covers": 81 * 332 + len(realized_pencils),
            "realized_partition_plus_extra_covers": 81 * 332,
            "realized_pencil_covers": len(realized_pencils),
            "pencils_by_missing_type_count": {
                str(key): value for key, value in sorted(missing_histogram.items())
            },
            "realized_pencil_sha256": digest(realized_pencils),
            "partition_branch_excluded_by_h4165": True,
        },
        "curve_lift_frontier": {
            "raw_pencil_quintets": raw_lifts,
            "after_h4167_pair_exclusions": pair_survivors,
            "after_h4167_pair_and_triple_exclusions": full_survivors,
            "removed_by_h4167_pairs": raw_lifts - pair_survivors,
            "removed_additionally_by_h4167_triples": pair_survivors - full_survivors,
            "pencils_empty_after_pairs": zero_after_pairs,
            "pencils_empty_after_triples": zero_after_triples,
            "h4151_forbidden_sets": len(four_sets),
            "h4151_sets_excluded_from_pencils_by_parallel_normals": len(four_sets),
            "h4167_distinct_pair_exclusions": len(pair_sets),
            "h4167_triple_exclusions": len(triple_sets),
            "profile_counts_pattern_raw_pair_full": {
                str(key): value for key, value in sorted(profile_counts.items())
            },
            "entrywise_pencil_count_transcript_sha256": lift_transcript.hexdigest(),
        },
        "pair_frontier": {
            "h4117_global_pair_representatives": d3_certificate["pairs"]["orbits"],
            "after_h4139_and_h4167_pair_filters": len(retained_pairs),
            "exact_five_compatible_pair_orbits": len(modes[exact_mode]),
            "exact_five_compatible_allowance": allowances[exact_mode],
            "exact_five_compatible_D3_closure_systems": closure_counts[exact_mode],
            "requires_at_least_six_pair_orbits": len(modes[parallel_mode]) + len(modes[missing_mode]),
            "requires_at_least_six_allowance": allowances[parallel_mode] + allowances[missing_mode],
            "parallel_pair_orbits": len(modes[parallel_mode]),
            "parallel_pair_allowance": allowances[parallel_mode],
            "unrealized_pencil_pair_orbits": len(modes[missing_mode]),
            "unrealized_pencil_pair_allowance": allowances[missing_mode],
            "mode_pair_sha256": {
                mode: digest(pairs) for mode, pairs in sorted(modes.items())
            },
            "all_exact_five_pairs_have_constraint_avoiding_extension": True,
            "extension_witness_transcript_sha256": witness_transcript.hexdigest(),
            "classification_D3_invariant": True,
            "global_representatives_not_chamber_restricted": True,
        },
        "explicit_interface": {
            "bytes": len((json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n").encode()),
            "sha256": digest(interface),
        },
        "minimum_active_curves_remaining": 5,
        "six_active_gate_closed": False,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--export-interface", type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    certificate = make_certificate(args.export_interface)
    args.out.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
