#!/usr/bin/env python3
"""Independent exact audit of direction-dependent convex normal bundles.

The checker imports no target code.  It uses rational cube-normal fixtures,
Pythagorean angular factors, direct four-dimensional trajectories, and
whole-ray leading-coefficient witnesses.  Universal convex projection and
the two external transfer theorems remain written-mathematics boundaries.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "target manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target input: {relative}")
    return manifest


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def add(first, second):
    return tuple(a + b for a, b in zip(first, second))


def sub(first, second):
    return tuple(a - b for a, b in zip(first, second))


def scale(value, vector):
    return tuple(value * coordinate for coordinate in vector)


def distance_squared(first, second):
    return dot(sub(first, second), sub(first, second))


def clip_cube(point):
    return tuple(max(F(-1), min(F(1), coordinate)) for coordinate in point)


def cube_normal(base, direction):
    if dot(direction, direction) != 1 or any(abs(x) > 1 for x in base):
        return False
    return all(not u or p == (1 if u > 0 else -1)
               for p, u in zip(base, direction))


def ray_specs():
    zero = F(0)
    return [
        ("face_x", (F(1), zero, zero), (F(1), zero, zero), F(0), F(1)),
        ("parallel_x", (F(1), F(1, 2), F(-1, 2)),
         (F(1), zero, zero), F(0), F(1)),
        ("face_y", (zero, F(1), zero), (zero, F(1), zero), F(0), F(1)),
        ("face_z", (zero, zero, F(1)), (zero, zero, F(1)), F(4, 5), F(3, 5)),
        ("edge", (F(1), F(1), zero), (F(3, 5), F(4, 5), zero), F(3, 5), F(4, 5)),
        ("vertex", (F(1), F(1), F(1)),
         (F(1, 3), F(2, 3), F(2, 3)), F(3, 5), F(4, 5)),
        ("opposite_x", (F(-1), zero, zero), (F(-1), zero, zero), F(12, 13), F(5, 13)),
    ]


def build_sites():
    sites = []
    core = [
        (F(0), F(0), F(0)),
        (F(1, 2), F(-1, 3), F(1, 4)),
        (F(1), F(1), F(1)),
        (F(-1), F(0), F(1)),
    ]
    for index, point in enumerate(core):
        sites.append({"name": f"core_{index}", "core": True, "point": point})
    for name, base, direction, factor, complement in ray_specs():
        require(cube_normal(base, direction), f"invalid cube normal: {name}")
        require(factor * factor + complement * complement == 1,
                f"factor complement: {name}")
        for radius in (F(1, 3), F(1), F(5, 2)):
            point = add(base, scale(radius, direction))
            require(clip_cube(point) == base, f"projection recovery: {name}")
            sites.append({"name": f"{name}_{radius}", "core": False,
                          "point": point, "base": base, "direction": direction,
                          "radius": radius, "factor": factor,
                          "complement": complement})
    require(len({site["point"] for site in sites}) == len(sites), "distinct sources")
    return sites


ANGLES = [(F(1), F(0)), (F(12, 13), F(5, 13)),
          (F(4, 5), F(3, 5)), (F(3, 5), F(4, 5)),
          (F(5, 13), F(12, 13)), (F(0), F(1))]


def angular_conditions():
    rays = ray_specs()
    pair_checks = parallel_checks = 0
    minimum_reserve = None
    for first, second in combinations(rays, 2):
        _, _, u, a, sa = first
        _, _, v, b, sb = second
        cosine = dot(u, v)
        reserve = sa * sb - cosine * (1 - a * b)
        require(reserve >= 0, "angular condition")
        minimum_reserve = reserve if minimum_reserve is None else min(minimum_reserve, reserve)
        if u == v:
            require(a == b, "parallel factors differ")
            parallel_checks += 1
        pair_checks += 1
    return pair_checks, parallel_checks, minimum_reserve


def raised(site, cosine, sine):
    if site["core"]:
        return site["point"] + (F(0),)
    a, sa = site["factor"], site["complement"]
    A = (a + cosine) / (1 + a * cosine)
    B = sa * sine / (1 + a * cosine)
    horizontal = add(site["base"], scale(site["radius"] * A, site["direction"]))
    return horizontal + (site["radius"] * B,)


def lowered(site, time):
    if site["core"]:
        return site["point"] + (F(0),)
    horizontal = add(site["base"],
                     scale(site["radius"] * site["factor"], site["direction"]))
    return horizontal + ((1 - time) * site["radius"] * site["complement"],)


def motion_controls():
    sites = build_sites()
    path_pairs = raise_inequalities = lower_inequalities = 0
    offset_sign_checks = 0
    for first, second in combinations(sites, 2):
        if not first["core"] and not second["core"]:
            displacement = sub(first["base"], second["base"])
            require(dot(displacement, first["direction"]) >= 0,
                    "first projection-offset sign")
            require(dot(displacement, second["direction"]) <= 0,
                    "second projection-offset sign")
            offset_sign_checks += 2
        raised_distances = [distance_squared(raised(first, c, s), raised(second, c, s))
                            for c, s in ANGLES]
        require(all(left >= right for left, right in
                    zip(raised_distances, raised_distances[1:])), "raising distance")
        raise_inequalities += len(raised_distances) - 1
        lower_times = (F(0), F(1, 3), F(2, 3), F(1))
        lowered_distances = [distance_squared(lowered(first, t), lowered(second, t))
                             for t in lower_times]
        require(raised_distances[-1] == lowered_distances[0], "stage join")
        require(all(left >= right for left, right in
                    zip(lowered_distances, lowered_distances[1:])), "lowering distance")
        require(raised_distances[0] == distance_squared(first["point"], second["point"]),
                "source endpoint")
        lower_inequalities += len(lowered_distances) - 1
        path_pairs += 1
    return {
        "sites": len(sites),
        "pair_paths": path_pairs,
        "raise_inequalities": raise_inequalities,
        "lower_inequalities": lower_inequalities,
        "projection_offset_signs": offset_sign_checks,
    }


def regularized_injection():
    sites = build_sites()
    epsilon = F(1, 7)
    target_images = []
    projection_recoveries = 0
    stage_horizontal_injections = 0
    for site in sites:
        if site["core"]:
            target_images.append(site["point"])
            continue
        factor = epsilon + (1 - epsilon) * site["factor"]
        require(factor > 0, "regularized factor positivity")
        image = add(site["base"], scale(site["radius"] * factor, site["direction"]))
        require(clip_cube(image) == site["base"], "regularized target projection")
        target_images.append(image)
        projection_recoveries += 1
    require(len(set(target_images)) == len(target_images), "regularized target injection")

    for cosine, _ in ANGLES:
        horizontals = []
        for site in sites:
            if site["core"]:
                horizontals.append(site["point"])
                continue
            factor = epsilon + (1 - epsilon) * site["factor"]
            A = (factor + cosine) / (1 + factor * cosine)
            require(A > 0, "regularized raised radial coefficient")
            horizontal = add(site["base"], scale(site["radius"] * A, site["direction"]))
            require(clip_cube(horizontal) == site["base"], "raised projection recovery")
            horizontals.append(horizontal)
            projection_recoveries += 1
        require(len(set(horizontals)) == len(horizontals), "raised-stage injection")
        stage_horizontal_injections += len(horizontals)
    return {
        "epsilon": str(epsilon),
        "target_injective_sites": len(target_images),
        "raised_horizontal_injective_entries": stage_horizontal_injections,
        "projection_recoveries": projection_recoveries,
    }


def ball_offset_loss(a, b, cosine, r, s, length):
    source_u = 1 + length * r
    source_v = 1 + length * s
    target_u = 1 + length * a * r
    target_v = 1 + length * b * s
    return (source_u * source_u + source_v * source_v
            - 2 * cosine * source_u * source_v
            - target_u * target_u - target_v * target_v
            + 2 * cosine * target_u * target_v)


def whole_ray_boundary():
    # Each row violates the cone condition.  The radii are the exact
    # minimising witness r=c(1-ab), s=1-a^2.
    rows = [(F(0), F(4, 5), F(13, 20)),
            (F(0), F(12, 13), F(3, 5)),
            (F(3, 5), F(4, 5), F(1))]
    witnesses = []
    for a, b, cosine in rows:
        sa2, sb2 = 1 - a * a, 1 - b * b
        cross = cosine * (1 - a * b)
        require(cross > 0 and cross * cross > sa2 * sb2, "expected cone violation")
        r, s = cross, sa2
        leading = sa2 * r * r + sb2 * s * s - 2 * cross * r * s
        require(leading < 0, "negative whole-ray witness")
        values = [(length, ball_offset_loss(a, b, cosine, r, s, F(length)))
                  for length in range(1, 129)]
        first_negative = next((length for length, loss in values if loss < 0), None)
        require(first_negative is not None, "offset failed to reveal cone violation")
        witnesses.append({"a": str(a), "b": str(b), "cosine": str(cosine),
                          "leading_loss": str(leading),
                          "loss_at_one": str(values[0][1]),
                          "first_negative_integer_scale": first_negative})

    # Equal directions force equal factors, independently of the base offset.
    a, b = F(0), F(1, 2)
    parallel_lead = (a - b) * (a - b)
    require(parallel_lead > 0, "unequal parallel factors not detected")
    return {"bad_factor_pairs": len(rows), "witnesses": witnesses,
            "unequal_parallel_factor_square": str(parallel_lead)}


def cube_example_scope():
    e1 = (F(1), F(0), F(0))
    oblique = (F(1, 3), F(2, 3), F(2, 3))
    factor_axis = abs(e1[0] * e1[1] * e1[2])
    factor_oblique = abs(oblique[0] * oblique[1] * oblique[2])
    require(factor_axis == 0 and factor_oblique == F(4, 27),
            "equal-distance directional separation")

    # For the cube h_C(x)=|x_1|+|x_2|+|x_3|.  If C=D+bB with b>0,
    # h_D=h_C-b|.| would violate subadditivity on e1,e2 because sqrt(2)<2.
    require(F(2) * F(2) > F(2), "strict triangle comparison")
    core_points = [(F(0), F(0), F(0)), (F(1, 2), F(-1, 2), F(1, 3)),
                   (F(1), F(1), F(1))]
    require(all(clip_cube(point) == point for point in core_points), "cube fixed core")
    return {"axis_factor": str(factor_axis), "oblique_factor": str(factor_oblique),
            "equal_normal_distance_controls": 2,
            "support_subadditivity_obstruction": "sqrt(2)<2"}


def damaged_controls():
    rejected = 0
    candidates = [
        ((F(1), F(0), F(0)), (F(-1), F(0), F(0))),
        ((F(0), F(0), F(0)), (F(1), F(0), F(0))),
        ((F(1), F(1), F(0)), (F(1), F(1), F(0))),
    ]
    for base, direction in candidates:
        if not cube_normal(base, direction):
            rejected += 1
    require(rejected == len(candidates), "damaged normals accepted")
    return rejected


def audit():
    manifest = pin_inputs()
    angular_pairs, parallel_pairs, reserve = angular_conditions()
    return {
        "status": "INDEPENDENT_DIRECTIONAL_NORMAL_BUNDLE_REVIEW_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "angular_condition_pairs": angular_pairs,
        "parallel_direction_pairs": parallel_pairs,
        "minimum_angular_reserve": str(reserve),
        "motion": motion_controls(),
        "regularized_injection": regularized_injection(),
        "whole_ray_boundary": whole_ray_boundary(),
        "cube_example_scope": cube_example_scope(),
        "damaged_normal_rejections": damaged_controls(),
        "verdict": ("accept the direction-dependent complete-normal-ray class; "
                    "external transfers and historical novelty remain trust boundaries"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    parser.add_argument("--print-record", action="store_true")
    args = parser.parse_args()
    result = audit()
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.print_record:
        print(raw, end="")
        return
    require(result == json.loads(args.expected.read_text()), "review record differs")
    print(result["status"])
    print("record_sha256", sha256(raw.encode()).hexdigest())


if __name__ == "__main__":
    main()
