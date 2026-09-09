#!/usr/bin/env python3
"""Produce the exact D3 quotient certificate for the HN2 radix frontier."""
from collections import Counter
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
SOURCE_SPEC = importlib.util.spec_from_file_location("hn2_complex_radix_verify", SOURCE / "verify.py")
HN2 = importlib.util.module_from_spec(SOURCE_SPEC)
SOURCE_SPEC.loader.exec_module(HN2)

SOURCE_COMMIT = "95687bd35321aa6fb767fc508eac6ab186ba6d2e"
OMEGA2 = (-1, 1)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def compose(p, q):
    """Permutation p after q, with permutations stored as image tuples."""
    return tuple(p[q[i]] for i in range(len(p)))


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


def conjugate_eisenstein(digit):
    # omega-bar=1-omega in the basis (1,omega).
    return digit[0] + digit[1], -digit[1]


def rotate_row(row):
    power = (1, 0)
    image = []
    for digit in row:
        image.append(G.emul(digit, power))
        power = G.emul(power, OMEGA2)
    return G.canon(tuple(image))


def conjugate_row(row):
    return G.canon(tuple(conjugate_eisenstein(digit) for digit in row))


def pair_image(pair, permutation):
    return tuple(sorted((permutation[pair[0]], permutation[pair[1]])))


def canonical_representatives(objects, group, image):
    return sorted({min(image(obj, action) for action in group) for obj in objects})


def histogram(counter):
    return {str(key): value for key, value in sorted(counter.items())}


def compute():
    rows, events, factors, factor_edges, base, collisions, _, circle = HN2.build()
    source_certificate = json.loads((SOURCE / "certificate.json").read_text())
    _, _, _, pairs = HN2.finite_cover(
        source_certificate["colour_specs"], factors, factor_edges, base
    )

    factor_ids = {factor: i for i, factor in enumerate(factors)}
    representative_rows = {}
    for row, event in zip(rows, events):
        if event:
            representative_rows.setdefault(factor_ids[event], row)
    assert len(representative_rows) == len(factors)

    def curve_image(curve_id, row_action):
        row = row_action(representative_rows[curve_id])
        nonzero = [j for j, digit in enumerate(row) if digit != (0, 0)]
        if len(nonzero) == 1:
            assert nonzero[0] > 0
            return circle
        return factor_ids[G.distance_event(row)]

    rotation = tuple(curve_image(i, rotate_row) for i in range(len(factors)))
    conjugation = tuple(curve_image(i, conjugate_row) for i in range(len(factors)))
    curve_group = generated_group(rotation, conjugation)
    identity = tuple(range(len(factors)))
    assert len(curve_group) == 6
    assert compose(rotation, compose(rotation, rotation)) == identity
    assert compose(conjugation, conjugation) == identity
    assert compose(conjugation, compose(rotation, conjugation)) == compose(rotation, rotation)

    curve_reps = canonical_representatives(
        range(len(factors)), curve_group, lambda item, action: action[item]
    )
    curve_orbit_sizes = Counter(len({action[item] for action in curve_group}) for item in curve_reps)
    curve_degrees = [HN2.degree(factor) for factor in factors]

    pair_set = set(pairs)
    pair_reps = canonical_representatives(pairs, curve_group, pair_image)
    pair_orbit_sizes = Counter()
    original_members = Counter()
    pair_closure_count = 0
    for pair in pair_reps:
        members = {pair_image(pair, action) for action in curve_group}
        pair_orbit_sizes[len(members)] += 1
        original_members[len(members & pair_set)] += 1
        pair_closure_count += len(members)
    pair_products = [curve_degrees[a] * curve_degrees[b] for a, b in pair_reps]

    collision_ids = {row: i for i, row in enumerate(collisions)}
    collision_rotation = tuple(collision_ids[rotate_row(row)] for row in collisions)
    collision_conjugation = tuple(collision_ids[conjugate_row(row)] for row in collisions)
    collision_group = generated_group(collision_rotation, collision_conjugation)
    collision_identity = tuple(range(len(collisions)))
    assert len(collision_group) == 6
    assert compose(collision_rotation, compose(collision_rotation, collision_rotation)) == collision_identity
    assert compose(collision_conjugation, collision_conjugation) == collision_identity
    assert compose(
        collision_conjugation, compose(collision_rotation, collision_conjugation)
    ) == compose(collision_rotation, collision_rotation)
    collision_reps = canonical_representatives(
        range(len(collisions)), collision_group, lambda item, action: action[item]
    )
    collision_orbit_sizes = Counter(
        len({action[item] for action in collision_group}) for item in collision_reps
    )
    collision_degrees = [len(row) - 1 for row in collisions]
    collision_rep_degrees = [collision_degrees[item] for item in collision_reps]

    certificate = {
        "schema": "hn-complex-radix-d3-quotient-v1",
        "source_commit": SOURCE_COMMIT,
        "source_certificate_sha256": hashlib.sha256((SOURCE / "certificate.json").read_bytes()).hexdigest(),
        "source_factor_inventory_sha256": HN2.digest(factors),
        "source_pair_inventory_sha256": HN2.digest(pairs),
        "source_collision_inventory_sha256": HN2.digest(collisions),
        "parameter_action": {
            "R": "(x,y)->((-x-3y)/2,(x-y)/2)",
            "C": "(x,y)->(x,-y)",
            "group": "D3=<R,C | R^3=C^2=1, CRC=R^-1>",
            "fundamental_chamber": "x>=0 and 0<=y<=x",
            "nonfour_radial_chamber": "1/4 < x^2+3*y^2 <= 4",
        },
        "curves": {
            "objects": len(factors),
            "orbits": len(curve_reps),
            "orbit_size_histogram": histogram(curve_orbit_sizes),
            "representative_degree_histogram": histogram(Counter(curve_degrees[i] for i in curve_reps)),
            "fixed_counts_sorted": sorted(
                sum(action[i] == i for i in range(len(factors))) for action in curve_group
            ),
            "rotation_permutation_sha256": digest(rotation),
            "conjugation_permutation_sha256": digest(conjugation),
            "representatives_sha256": digest(curve_reps),
        },
        "pairs": {
            "source_systems": len(pairs),
            "full_D3_closure_systems": pair_closure_count,
            "orbits": len(pair_reps),
            "orbit_size_histogram": histogram(pair_orbit_sizes),
            "source_members_per_orbit_histogram": histogram(original_members),
            "representatives_sha256": digest(pair_reps),
            "representative_degree_product_histogram": histogram(Counter(pair_products)),
            "parameter_orbit_bezout_bound": sum(pair_products),
        },
        "collisions": {
            "objects": len(collisions),
            "orbits": len(collision_reps),
            "orbit_size_histogram": histogram(collision_orbit_sizes),
            "representative_degree_histogram": histogram(Counter(collision_rep_degrees)),
            "fixed_counts_sorted": sorted(
                sum(action[i] == i for i in range(len(collisions)))
                for action in collision_group
            ),
            "representatives_sha256": digest(collision_reps),
            "parameter_orbit_degree_bound": sum(collision_rep_degrees),
        },
    }
    certificate["all_exceptional_parameter_orbits_upper_bound"] = (
        certificate["pairs"]["parameter_orbit_bezout_bound"]
        + certificate["collisions"]["parameter_orbit_degree_bound"]
    )
    data = {
        "curve_group": curve_group,
        "curve_representatives": curve_reps,
        "pair_representatives": pair_reps,
        "collision_group": collision_group,
        "collision_representatives": collision_reps,
        "collisions": collisions,
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
                "curve_orbits": certificate["curves"]["orbits"],
                "pair_orbits": certificate["pairs"]["orbits"],
                "collision_orbits": certificate["collisions"]["orbits"],
                "all_exceptional_parameter_orbits_upper_bound": certificate[
                    "all_exceptional_parameter_orbits_upper_bound"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
