#!/usr/bin/env python3
"""Independent checker for the exact five-active affine-pencil frontier."""

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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


D3 = load("five_pencil_d3_checker", ROOT / "hadwiger_nelson_complex_radix_d3_quotient" / "produce.py")
FOUR = load("five_pencil_four_checker", ROOT / "hadwiger_nelson_radix_four_active_closure" / "verify.py")
INCIDENCE = load("five_pencil_incidence_checker", ROOT / "hadwiger_nelson_radix_incidence_geometry" / "verify.py")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def precheck_certificate(certificate):
    need(certificate.get("schema") == "hn-radix-five-active-pencil-v1", "schema")
    cover = certificate["affine_cover_classification"]
    need(cover["field_order"] == 4 and cover["dimension"] == 4, "ambient affine space")
    need(cover["theoretical_hyperplanes"] == 340, "theoretical hyperplane count")
    need(cover["realized_hyperplanes"] == 336, "realized hyperplane count")
    need(
        cover["abstract_five_covers"]
        == cover["abstract_partition_plus_extra_covers"] + cover["abstract_pencil_covers"],
        "abstract cover partition",
    )
    need(
        cover["realized_five_covers"]
        == cover["realized_partition_plus_extra_covers"] + cover["realized_pencil_covers"],
        "realized cover partition",
    )
    need(
        sum(cover["pencils_by_missing_type_count"].values())
        == cover["abstract_pencil_covers"],
        "missing-type pencil partition",
    )
    lift = certificate["curve_lift_frontier"]
    need(
        lift["raw_pencil_quintets"] - lift["removed_by_h4167_pairs"]
        == lift["after_h4167_pair_exclusions"],
        "pair-exclusion arithmetic",
    )
    need(
        lift["after_h4167_pair_exclusions"]
        - lift["removed_additionally_by_h4167_triples"]
        == lift["after_h4167_pair_and_triple_exclusions"],
        "triple-exclusion arithmetic",
    )
    need(lift["pencils_empty_after_triples"] == 0, "unexpected empty pencil")
    frontier = certificate["pair_frontier"]
    need(
        frontier["exact_five_compatible_pair_orbits"]
        + frontier["requires_at_least_six_pair_orbits"]
        == frontier["after_h4139_and_h4167_pair_filters"],
        "pair-mode partition",
    )
    need(
        frontier["parallel_pair_orbits"] + frontier["unrealized_pencil_pair_orbits"]
        == frontier["requires_at_least_six_pair_orbits"],
        "at-least-six partition",
    )
    need(
        frontier["parallel_pair_allowance"] + frontier["unrealized_pencil_pair_allowance"]
        == frontier["requires_at_least_six_allowance"],
        "at-least-six allowance",
    )
    need(frontier["classification_D3_invariant"], "D3 invariance flag")
    need(frontier["global_representatives_not_chamber_restricted"], "chamber warning")
    need(certificate["minimum_active_curves_remaining"] == 5, "minimum active count")
    need(not certificate["six_active_gate_closed"], "six-active scope")
    need(not certificate["record_improvement"], "record scope")


def expected_projection(certificate):
    cover = certificate["affine_cover_classification"]
    lift = certificate["curve_lift_frontier"]
    frontier = certificate["pair_frontier"]
    return {
        "status": "FIVE_ACTIVE_PENCIL_FRONTIER_VERIFIED",
        "abstract_five_covers": cover["abstract_five_covers"],
        "realized_pencil_covers": cover["realized_pencil_covers"],
        "raw_pencil_quintets": lift["raw_pencil_quintets"],
        "constraint_surviving_pencil_quintets": lift[
            "after_h4167_pair_and_triple_exclusions"
        ],
        "retained_global_pair_orbits": frontier[
            "after_h4139_and_h4167_pair_filters"
        ],
        "exact_five_compatible_pair_orbits": frontier[
            "exact_five_compatible_pair_orbits"
        ],
        "pair_orbits_forcing_at_least_six": frontier[
            "requires_at_least_six_pair_orbits"
        ],
        "exact_five_compatible_allowance": frontier[
            "exact_five_compatible_allowance"
        ],
        "record_improvement": certificate["record_improvement"],
    }


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


def dot(left, right):
    value = 0
    for a, b in zip(left, right):
        value ^= fmul(a, b)
    return value


def projective(normal, constant):
    pivot = next(value for value in normal if value)
    inverse = next(value for value in (1, 2, 3) if fmul(pivot, value) == 1)
    return tuple(fmul(inverse, value) for value in normal), fmul(inverse, constant)


def direct_signature(row, edges, colourings, words):
    masks = 0
    for index, colours in enumerate(colourings):
        if any(colours[u] == colours[v] for u, v in edges):
            masks |= 1 << index
    normal_values = tuple((a & 1) | ((b & 1) << 1) for a, b in row[1:])
    constant_value = (row[0][0] & 1) | ((row[0][1] & 1) << 1)
    signature = projective(normal_values, constant_value)
    predicted = sum(
        1 << index
        for index, word in enumerate(words)
        if dot(signature[0], word) == signature[1]
    )
    need(masks == predicted and masks.bit_count() == 64, "direct edge failure mask")
    return signature, masks


def source_interfaces():
    four_result, four_interface = FOUR.compute()
    with tempfile.TemporaryDirectory(prefix="hn-five-pencil-check-") as directory:
        incidence_path = Path(directory) / "incidence.json"
        incidence_result = INCIDENCE.compute(incidence_path)
        incidence_interface = json.loads(incidence_path.read_text())
    need(four_result["forbidden_incidence_count"] == 3006, "h4151 interface")
    need(incidence_result["combined_nonfour_excluded_sets"] == 184796, "h4167 interface")
    return four_interface, incidence_interface


def build_constraint_masks(count, four_interface, incidence_interface, signatures):
    four_sets = [
        tuple(curves)
        for curves, _ in four_interface["forbidden_curve_sets_with_K4_labels"]
    ]
    need(
        all(len({signatures[curve][0] for curve in curves}) == 1 for curves in four_sets),
        "every h4151 set lies in one parallel class",
    )
    pairs = {
        tuple(sorted(curves))
        for curves in incidence_interface["injectivity_excluded_sets"]
        if len(curves) == 2
    }
    pairs.update(
        tuple(sorted(curves))
        for curves in incidence_interface["monic_degree_four_excluded_pairs"]
    )
    triples = {
        tuple(sorted(curves))
        for curves in incidence_interface["injectivity_excluded_sets"]
        if len(curves) == 3
    }
    pair_bad = [0] * count
    for a, b in pairs:
        pair_bad[a] |= 1 << b
        pair_bad[b] |= 1 << a
    triple_bad = {}
    for triple in triples:
        for a, b in combinations(triple, 2):
            c = next(value for value in triple if value not in (a, b))
            triple_bad[a, b] = triple_bad.get((a, b), 0) | (1 << c)
    return four_sets, pairs, triples, pair_bad, triple_bad


def count_choices(domains, pair_bad, triple_bad, triples_enabled):
    domains = sorted(domains, key=lambda mask: (mask.bit_count(), mask))

    def visit(index, chosen, forbidden):
        available = domains[index] & ~forbidden
        if index == 4:
            return available.bit_count()
        total = 0
        while available:
            bit = available & -available
            available ^= bit
            curve = bit.bit_length() - 1
            new_forbidden = forbidden | pair_bad[curve]
            if triples_enabled:
                for old in chosen:
                    new_forbidden |= triple_bad.get(tuple(sorted((old, curve))), 0)
            total += visit(index + 1, chosen + (curve,), new_forbidden)
        return total

    return visit(0, (), 0)


def find_extension(pair, pattern, signatures, bucket_masks, pair_bad, triple_bad):
    base = tuple(pair)
    base_signatures = {signatures[curve] for curve in base}
    domains = sorted(
        (bucket_masks[item] for item in pattern if item not in base_signatures),
        key=lambda mask: (mask.bit_count(), mask),
    )
    forbidden = pair_bad[base[0]] | pair_bad[base[1]] | triple_bad.get(base, 0)

    def visit(index, chosen, bad):
        available = domains[index] & ~bad
        while available:
            bit = available & -available
            available ^= bit
            curve = bit.bit_length() - 1
            next_chosen = chosen + (curve,)
            if index == 2:
                return tuple(sorted(next_chosen))
            next_bad = bad | pair_bad[curve]
            for old in chosen:
                next_bad |= triple_bad.get(tuple(sorted((old, curve))), 0)
            result = visit(index + 1, next_chosen, next_bad)
            if result is not None:
                return result
        return None

    return visit(0, base, forbidden)


def compute(export_interface=None):
    factors, circle, data, base = FOUR.inventory()
    words = tuple(product(range(4), repeat=4))
    colourings = []
    for weights in words:
        colouring = []
        for label in FOUR.LABELS:
            value = 0
            for weight, digit in zip((1,) + weights, label):
                value ^= fmul(weight, digit)
            colouring.append(value)
        colourings.append(tuple(colouring))
    signatures = {}
    hyperplane_masks = {}
    curve_buckets = defaultdict(list)
    for curve, (row, edges) in sorted(data.items()):
        item, mask = direct_signature(row, edges, colourings, words)
        signatures[curve] = item
        hyperplane_masks.setdefault(item, mask)
        curve_buckets[item].append(curve)
    need(len(curve_buckets) == 336, "realized hyperplane types")
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
    theoretical_signatures = [(normal, constant) for normal in normals for constant in range(4)]
    theoretical_masks = {
        item: sum(
            1 << index
            for index, word in enumerate(words)
            if dot(item[0], word) == item[1]
        )
        for item in theoretical_signatures
    }
    need(len(set(theoretical_masks.values())) == 340, "theoretical affine hyperplanes")

    # Independent pencil reconstruction: a codimension-two affine flat is the
    # 16-point intersection of two nonparallel hyperplanes; exactly five
    # hyperplanes contain it.
    pencil_by_flat = {}
    for index, left in enumerate(theoretical_signatures):
        for right in theoretical_signatures[index + 1 :]:
            if left[0] == right[0]:
                continue
            flat = theoretical_masks[left] & theoretical_masks[right]
            need(flat.bit_count() == 16, "nonparallel intersection size")
            pencil_by_flat.setdefault(flat, set()).update((left, right))
    abstract_pencils = []
    for flat in sorted(pencil_by_flat):
        containing = tuple(
            sorted(
                item
                for item, mask in theoretical_masks.items()
                if flat & ~mask == 0
            )
        )
        need(len(containing) == 5, "five hyperplanes through an affine codimension-two flat")
        abstract_pencils.append(containing)
    need(len(abstract_pencils) == 5712 and len(set(abstract_pencils)) == 5712, "abstract pencil census")
    realized_pencils = sorted(
        pattern
        for pattern in abstract_pencils
        if all(item in curve_buckets for item in pattern)
    )
    missing_histogram = Counter(
        sum(item not in curve_buckets for item in pattern)
        for pattern in abstract_pencils
    )
    pencil_for_pair = {
        tuple(sorted(pair)): pattern
        for pattern in realized_pencils
        for pair in combinations(pattern, 2)
    }

    # Check both cover forms directly on all 256 words.
    full = (1 << 256) - 1
    for pattern in realized_pencils:
        union = 0
        for item in pattern:
            union |= theoretical_masks[item]
        need(union == full, "pencil does not cover F4^4")
    realized_partitions = [
        tuple((normal, constant) for constant in range(4))
        for normal in normals
        if all((normal, constant) in curve_buckets for constant in range(4))
    ]
    need(len(realized_partitions) == 81, "realized partition census")
    for pattern in realized_partitions:
        union = 0
        for item in pattern:
            union |= theoretical_masks[item]
        need(union == full, "parallel partition")

    four_interface, incidence_interface = source_interfaces()
    four_sets, pair_sets, triple_sets, pair_bad, triple_bad = build_constraint_masks(
        len(factors), four_interface, incidence_interface, signatures
    )

    raw_total = pair_total = full_total = 0
    zero_pairs = zero_triples = 0
    profiles = defaultdict(lambda: [0, 0, 0, 0])
    transcript = hashlib.sha256()
    for pattern in realized_pencils:
        domains = [bucket_masks[item] for item in pattern]
        raw = math.prod(domain.bit_count() for domain in domains)
        pair_count = count_choices(domains, pair_bad, {}, False)
        full_count = count_choices(domains, pair_bad, triple_bad, True)
        raw_total += raw
        pair_total += pair_count
        full_total += full_count
        zero_pairs += pair_count == 0
        zero_triples += full_count == 0
        profile = tuple(sorted(sum(bool(value) for value in item[0]) for item in pattern))
        record = profiles[profile]
        record[0] += 1
        record[1] += raw
        record[2] += pair_count
        record[3] += full_count
        transcript.update(
            json.dumps([pattern, raw, pair_count, full_count], separators=(",", ":")).encode()
            + b"\n"
        )

    d3_certificate, d3_data = D3.compute()
    rows, events, source_factors, factor_edges, universal, _, _, source_circle = D3.HN2.build()
    need(digest(source_factors) == digest(factors) and source_circle == circle, "curve ID alignment")
    degrees = [D3.HN2.degree(factor) for factor in source_factors]
    retained = [
        pair
        for pair in d3_data["pair_representatives"]
        if circle not in pair and tuple(pair) not in pair_sets
    ]
    modes = defaultdict(list)
    allowances = Counter()
    closures = Counter()
    witnesses = []
    witness_transcript = hashlib.sha256()
    for pair in retained:
        s, t = signatures[pair[0]], signatures[pair[1]]
        if s[0] == t[0]:
            mode = "parallel_signatures_require_at_least_six"
        elif tuple(sorted((s, t))) not in pencil_for_pair:
            mode = "unrealized_pencil_type_requires_at_least_six"
        else:
            mode = "exact_five_compatible"
            witness = find_extension(
                tuple(pair), pencil_for_pair[tuple(sorted((s, t)))],
                signatures, bucket_masks, pair_bad, triple_bad
            )
            need(witness is not None, "compatible pair lacks a constraint-avoiding lift")
            witnesses.append([list(pair), list(witness)])
            witness_transcript.update(
                json.dumps([list(pair), list(witness)], separators=(",", ":")).encode()
                + b"\n"
            )
        modes[mode].append(list(pair))
        allowances[mode] += degrees[pair[0]] * degrees[pair[1]]
        closures[mode] += len(
            {D3.pair_image(pair, action) for action in d3_data["curve_group"]}
        )

    for mode, pairs in modes.items():
        for pair in pairs:
            for member in {
                D3.pair_image(tuple(pair), action) for action in d3_data["curve_group"]
            }:
                s, t = signatures[member[0]], signatures[member[1]]
                if s[0] == t[0]:
                    observed = "parallel_signatures_require_at_least_six"
                elif tuple(sorted((s, t))) not in pencil_for_pair:
                    observed = "unrealized_pencil_type_requires_at_least_six"
                else:
                    observed = "exact_five_compatible"
                need(observed == mode, "D3 invariance")

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

    exact = "exact_five_compatible"
    parallel = "parallel_signatures_require_at_least_six"
    missing = "unrealized_pencil_type_requires_at_least_six"
    certificate = {
        "schema": "hn-radix-five-active-pencil-v1",
        "sources": {
            "architecture_certificate_sha256": hashlib.sha256((ARCH / "certificate.json").read_bytes()).hexdigest(),
            "d3_certificate_sha256": hashlib.sha256((ROOT / "hadwiger_nelson_complex_radix_d3_quotient" / "certificate.json").read_bytes()).hexdigest(),
            "four_active_certificate_sha256": hashlib.sha256((ROOT / "hadwiger_nelson_radix_four_active_closure" / "certificate.json").read_bytes()).hexdigest(),
            "four_concurrence_certificate_sha256": hashlib.sha256((ROOT / "hadwiger_nelson_complex_radix_four_concurrence" / "certificate.json").read_bytes()).hexdigest(),
            "incidence_geometry_certificate_sha256": hashlib.sha256((ROOT / "hadwiger_nelson_radix_incidence_geometry" / "certificate.json").read_bytes()).hexdigest(),
        },
        "affine_cover_classification": {
            "field_order": 4,
            "dimension": 4,
            "theoretical_hyperplanes": 340,
            "realized_hyperplanes": 336,
            "abstract_five_covers": 85 * 336 + len(abstract_pencils),
            "abstract_partition_plus_extra_covers": 85 * 336,
            "abstract_pencil_covers": len(abstract_pencils),
            "realized_five_covers": len(realized_partitions) * 332 + len(realized_pencils),
            "realized_partition_plus_extra_covers": len(realized_partitions) * 332,
            "realized_pencil_covers": len(realized_pencils),
            "pencils_by_missing_type_count": {str(k): v for k, v in sorted(missing_histogram.items())},
            "realized_pencil_sha256": digest(realized_pencils),
            "partition_branch_excluded_by_h4165": True,
        },
        "curve_lift_frontier": {
            "raw_pencil_quintets": raw_total,
            "after_h4167_pair_exclusions": pair_total,
            "after_h4167_pair_and_triple_exclusions": full_total,
            "removed_by_h4167_pairs": raw_total - pair_total,
            "removed_additionally_by_h4167_triples": pair_total - full_total,
            "pencils_empty_after_pairs": zero_pairs,
            "pencils_empty_after_triples": zero_triples,
            "h4151_forbidden_sets": len(four_sets),
            "h4151_sets_excluded_from_pencils_by_parallel_normals": len(four_sets),
            "h4167_distinct_pair_exclusions": len(pair_sets),
            "h4167_triple_exclusions": len(triple_sets),
            "profile_counts_pattern_raw_pair_full": {str(k): v for k, v in sorted(profiles.items())},
            "entrywise_pencil_count_transcript_sha256": transcript.hexdigest(),
        },
        "pair_frontier": {
            "h4117_global_pair_representatives": d3_certificate["pairs"]["orbits"],
            "after_h4139_and_h4167_pair_filters": len(retained),
            "exact_five_compatible_pair_orbits": len(modes[exact]),
            "exact_five_compatible_allowance": allowances[exact],
            "exact_five_compatible_D3_closure_systems": closures[exact],
            "requires_at_least_six_pair_orbits": len(modes[parallel]) + len(modes[missing]),
            "requires_at_least_six_allowance": allowances[parallel] + allowances[missing],
            "parallel_pair_orbits": len(modes[parallel]),
            "parallel_pair_allowance": allowances[parallel],
            "unrealized_pencil_pair_orbits": len(modes[missing]),
            "unrealized_pencil_pair_allowance": allowances[missing],
            "mode_pair_sha256": {mode: digest(pairs) for mode, pairs in sorted(modes.items())},
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
    return certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--export-interface", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    submitted = json.loads(args.certificate.read_text())
    precheck_certificate(submitted)
    actual = compute(args.export_interface)
    precheck_certificate(actual)
    need(actual == submitted, "certificate mismatch")
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(expected_projection(actual) == expected, "expected output mismatch")
    print(json.dumps(actual, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
