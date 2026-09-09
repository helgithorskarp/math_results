#!/usr/bin/env python3
"""Produce the exact four-active-curve hyperplane gate."""
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_complex_radix_architecture"
sys.path.insert(0, str(SOURCE))
import geometry as G  # noqa: E402

SOURCE_SPEC = importlib.util.spec_from_file_location("hn2_radix_four_gate", SOURCE / "verify.py")
HN2 = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(HN2)

OMEGA2 = (-1, 1)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def fmul(a, b):
    """Multiply bit-encoded a0+a1*t in F4, where t^2=t+1."""
    a0, a1 = a & 1, (a >> 1) & 1
    b0, b1 = b & 1, (b >> 1) & 1
    return (a0 * b0 ^ a1 * b1) | ((a0 * b1 ^ a1 * b0 ^ a1 * b1) << 1)


def finv(value):
    if not value:
        raise ZeroDivisionError("zero in F4")
    return next(candidate for candidate in range(1, 4) if fmul(value, candidate) == 1)


def residue(digit):
    return (digit[0] & 1) ^ ((digit[1] & 1) << 1)


def projective(normal, constant):
    pivot = next(value for value in normal if value)
    scale = finv(pivot)
    return tuple(fmul(scale, value) for value in normal), fmul(scale, constant)


def dot(normal, word):
    result = 0
    for a, b in zip(normal, word):
        result ^= fmul(a, b)
    return result


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def generated_group(*generators):
    identity = tuple(range(len(generators[0])))
    group = {identity}
    pending = [identity]
    while pending:
        old = pending.pop()
        for generator in generators:
            new = compose(generator, old)
            if new not in group:
                group.add(new)
                pending.append(new)
    return tuple(sorted(group))


def rotate_row(row):
    power = (1, 0)
    image = []
    for digit in row:
        image.append(G.emul(digit, power))
        power = G.emul(power, OMEGA2)
    return G.canon(tuple(image))


def conjugate_row(row):
    return G.canon(tuple((a + b, -b) for a, b in row))


def pair_image(pair, action):
    return tuple(sorted((action[pair[0]], action[pair[1]])))


def histogram(values):
    return {str(key): value for key, value in sorted(Counter(values).items())}


def theoretical_patterns():
    normals = sorted(
        {
            projective(normal, 0)[0]
            for normal in product(range(4), repeat=4)
            if any(normal)
        }
    )
    all_types = [(normal, constant) for normal in normals for constant in range(4)]
    torus = tuple(product(range(1, 4), repeat=4))
    masks = {
        signature: frozenset(
            i for i, word in enumerate(torus) if dot(signature[0], word) == signature[1]
        )
        for signature in all_types
    }
    size_27 = [signature for signature in all_types if len(masks[signature]) == 27]
    torus_partitions = []
    for triple in combinations(size_27, 3):
        if len(set().union(*(masks[item] for item in triple))) == 81:
            torus_partitions.append(tuple(sorted(triple)))
    return normals, all_types, torus_partitions


def compute():
    rows, events, factors, factor_edges, base, _, _, circle = HN2.build()
    source_certificate = json.loads((SOURCE / "certificate.json").read_text())
    _, _, _, source_pairs = HN2.finite_cover(
        source_certificate["colour_specs"], factors, factor_edges, base
    )

    factor_ids = {factor: i for i, factor in enumerate(factors)}
    representative_rows = {}
    for row, event in zip(rows, events):
        if event:
            representative_rows.setdefault(factor_ids[event], row)
    if len(representative_rows) != len(factors):
        raise ValueError("incomplete curve representatives")

    signatures = {}
    buckets = defaultdict(list)
    for curve in range(len(factors)):
        if curve == circle:
            continue
        row = representative_rows[curve]
        signature = projective(
            tuple(residue(digit) for digit in row[1:]), residue(row[0])
        )
        signatures[curve] = signature
        buckets[signature].append(curve)

    normals, all_types, torus_partitions = theoretical_patterns()
    missing_types = sorted(set(all_types) - set(buckets))
    affine_partitions = [
        tuple((normal, constant) for constant in range(4))
        for normal in normals
        if all((normal, constant) in buckets for constant in range(4))
    ]
    if len(normals) != 85 or len(all_types) != 340:
        raise ValueError("F4 projective hyperplane inventory")
    if len(buckets) != 336 or len(affine_partitions) != 81 or len(torus_partitions) != 10:
        raise ValueError("unexpected exact-four signature inventory")

    affine_sets = tuple(map(frozenset, affine_partitions))
    torus_sets = tuple(map(frozenset, torus_partitions))

    def curve_image(curve_id, row_action):
        row = row_action(representative_rows[curve_id])
        nonzero = [j for j, digit in enumerate(row) if digit != (0, 0)]
        if len(nonzero) == 1:
            if nonzero[0] == 0:
                raise ValueError("universal event in active inventory")
            return circle
        return factor_ids[G.distance_event(row)]

    rotation = tuple(curve_image(i, rotate_row) for i in range(len(factors)))
    conjugation = tuple(curve_image(i, conjugate_row) for i in range(len(factors)))
    curve_group = generated_group(rotation, conjugation)
    if len(curve_group) != 6:
        raise ValueError("curve action is not D3")
    identity = tuple(range(len(factors)))
    if compose(rotation, compose(rotation, rotation)) != identity:
        raise ValueError("R^3 relation")
    if compose(conjugation, conjugation) != identity:
        raise ValueError("C^2 relation")
    if compose(conjugation, compose(rotation, conjugation)) != compose(rotation, rotation):
        raise ValueError("CRC=R^-1 relation")

    pair_orbits = {}
    for pair in source_pairs:
        orbit = {pair_image(pair, action) for action in curve_group}
        pair_orbits.setdefault(min(orbit), orbit)
    pair_reps = sorted(pair_orbits)
    if len(pair_reps) != 132130:
        raise ValueError("D3 pair quotient mismatch")

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
        if any(compatibility(member) != mode for member in orbit):
            raise ValueError("four-curve compatibility is not D3-invariant")
        mode_reps[mode].append(pair)
        mode_closure[mode] += len(orbit)
        mode_bezout[mode] += degrees[pair[0]] * degrees[pair[1]]
        mode_circle[mode, circle in pair] += 1
    source_modes = Counter(compatibility(pair) for pair in source_pairs)

    affine_quartets = sum(
        len(buckets[normal, 0])
        * len(buckets[normal, 1])
        * len(buckets[normal, 2])
        * len(buckets[normal, 3])
        for normal in normals
        if all((normal, constant) in buckets for constant in range(4))
    )
    torus_quartets = sum(
        len(buckets[a]) * len(buckets[b]) * len(buckets[c])
        for a, b, c in torus_partitions
    )

    compatible_modes = ("exact_four_no_circle", "exact_four_with_circle")
    exact_four_pair_orbits = sum(len(mode_reps[mode]) for mode in compatible_modes)
    exact_four_bezout = sum(mode_bezout[mode] for mode in compatible_modes)
    interface = {
        "schema": "hn-complex-radix-exact-four-interface-v1",
        "curve_id_source": "hadwiger_nelson_complex_radix_architecture sorted active curves",
        "circle_id": circle,
        "F4_encoding": "0,1,t,1+t encoded as 0,1,2,3 with t^2=t+1",
        "no_circle_signature_patterns": affine_partitions,
        "with_circle_noncircle_signature_patterns": torus_partitions,
        "pair_representatives": {
            mode: mode_reps[mode] for mode in compatible_modes
        },
    }
    interface_raw = (
        json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    certificate = {
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
            "exact_four_compatible_orbits": exact_four_pair_orbits,
            "exact_four_compatible_bezout_bound": exact_four_bezout,
            "orbits_forcing_at_least_five_active_curves": len(
                mode_reps["at_least_five"]
            ),
            "compatibility_D3_invariant": True,
        },
        "explicit_interface": {
            "bytes": len(interface_raw),
            "sha256": hashlib.sha256(interface_raw).hexdigest(),
        },
    }
    data = {
        "affine_partitions": affine_partitions,
        "torus_partitions": torus_partitions,
        "signatures": signatures,
        "pair_representatives_by_mode": dict(mode_reps),
        "interface": interface,
        "interface_raw": interface_raw,
    }
    return certificate, data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.out.exists() and not args.force:
        raise FileExistsError(args.out)
    certificate, _ = compute()
    raw = (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode()
    args.out.write_bytes(raw)
    print(
        json.dumps(
            {
                "path": str(args.out),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "exact_four_signature_patterns": certificate["exact_four"][
                    "no_circle_signature_patterns"
                ]
                + certificate["exact_four"]["with_circle_signature_patterns"],
                "exact_four_compatible_pair_orbits": certificate["pair_frontier"][
                    "exact_four_compatible_orbits"
                ],
                "pair_orbits_forcing_at_least_five": certificate["pair_frontier"][
                    "orbits_forcing_at_least_five_active_curves"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
