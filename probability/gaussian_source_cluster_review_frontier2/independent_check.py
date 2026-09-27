#!/usr/bin/env python3
"""Independent exact audit of the source-cluster finite certificate and schedule."""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_prior_localization"
CAP = F(7, 50)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


def point(row):
    return tuple(F(str(value)) for value in row)


def squared_distance(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


def pinned_files():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "target manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target byte: {relative}")
    return manifest


def read_active_fixture():
    raw = json.loads((TARGET / "CLUSTER_FIXTURE.json").read_text())
    xs = [point(row) for row in raw["source"]]
    ys = [point(row) for row in raw["target"]]
    ws = [F(str(value)) for value in raw["weights"]]
    variance = F(str(raw.get("variance", 1)))
    require(len(xs) == len(ys) == len(ws), "fixture lengths")
    require(sum(ws) == 1 and all(w >= 0 for w in ws), "fixture weights")
    require(variance > 0, "fixture variance")
    pair_checks = 0
    for i, j in combinations(range(len(xs)), 2):
        require(squared_distance(ys[i], ys[j]) <= squared_distance(xs[i], xs[j]),
                "fixture is not a contraction")
        pair_checks += 1
    merged = {}
    for x, y, w in zip(xs, ys, ws):
        if w:
            merged[x, y] = merged.get((x, y), F(0)) + w
    return ([key[0] for key in merged], [key[1] for key in merged],
            list(merged.values()), variance, pair_checks)


def components_at(distances, threshold):
    """Connected components rebuilt by graph search, not incremental union-find."""
    count = len(distances)
    remaining = set(range(count))
    answer = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        stack = [seed]
        component = []
        while stack:
            i = stack.pop()
            component.append(i)
            adjacent = {j for j in remaining if distances[i][j] <= threshold}
            remaining.difference_update(adjacent)
            stack.extend(adjacent)
        answer.append(sorted(component))
    return sorted(answer, key=lambda row: row[0])


def candidate_partitions(distances):
    singleton = [[i] for i in range(len(distances))]
    answer = [singleton]
    levels = sorted({distances[i][j]
                     for i, j in combinations(range(len(distances)), 2)})
    for level in levels:
        part = components_at(distances, level)
        if part != answer[-1]:
            answer.append(part)
    return answer


def dyadic_sqrt_bounds(q, bits):
    """Exact monotone binary search for dyadic square-root bounds."""
    require(q >= 0, "negative root")
    scale = 1 << bits
    low, high = 0, 1
    while high * high * q.denominator <= q.numerator * scale * scale:
        low, high = high, 2 * high
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle * q.denominator <= q.numerator * scale * scale:
            low = middle
        else:
            high = middle
    lower = F(low, scale)
    upper = lower if lower * lower == q else F(high, scale)
    require(lower * lower <= q <= upper * upper, "bad root enclosure")
    return lower, upper


def local_units(radius2, bits):
    scale = 1 << bits
    if radius2 == 0:
        return 0, None
    k = int(F(1, 8) / radius2)
    if k < 2:
        return ceiling(CAP * scale), k
    exact_scaled = F(16 * k * scale, 1 << (5 * k))
    return min(ceiling(exact_scaled), ceiling(CAP * scale)), k


def classification_units(distance2, radius_upper, bits, geometry_bits):
    scale = 1 << bits
    lower, _ = dyadic_sqrt_bounds(distance2, geometry_bits)
    if lower == 0:
        return scale
    margin = lower / 2 - radius_upper
    if margin < 0:
        return scale
    power = int(margin * margin / 2) + 1
    return 1 if power >= bits else 1 << (bits - power)


def evaluate(distances, weights, partition, bits=40, geometry_bits=16):
    scale = 1 << bits
    rows = []
    for members in partition:
        radius2, anchor = min(
            (max(distances[a][j] for j in members), a) for a in members
        )
        radius_upper = dyadic_sqrt_bounds(radius2, geometry_bits)[1]
        local, k = local_units(radius2, bits)
        rows.append({
            "members": members,
            "anchor": anchor,
            "mass": sum(weights[j] for j in members),
            "radius2": radius2,
            "radius_upper": radius_upper,
            "local_units": local,
            "k": k,
        })
    total = F(0)
    worst = 0
    for i, row in enumerate(rows):
        wrong = sum(
            classification_units(distances[row["anchor"]][other["anchor"]],
                                 row["radius_upper"], bits, geometry_bits)
            for j, other in enumerate(rows) if i != j
        )
        row["classification_units"] = min(scale, wrong)
        cost = row["local_units"] + row["classification_units"]
        total += row["mass"] * cost
        worst = max(worst, cost)
    weighted = ceiling(total)
    return {
        "weighted_units": weighted,
        "defect_bound": str(min(CAP, F(weighted, scale))),
        "all_masses_bound": str(min(CAP, F(worst, scale))),
        "component_count": len(rows),
        "rows": rows,
    }


def audit():
    manifest = pinned_files()
    xs, _, weights, variance, pair_checks = read_active_fixture()
    distances = [[squared_distance(x, y) / variance for y in xs] for x in xs]
    partitions = candidate_partitions(distances)
    candidates = [evaluate(distances, weights, partition) for partition in partitions]
    best = min(candidates, key=lambda row: F(row["defect_bound"]))

    public = json.loads((TARGET / "CLUSTER_EXPECTED.json").read_text())["fixture_certificate"]
    require([len(part) for part in partitions] == public["candidate_component_counts"],
            "candidate component counts differ")
    certificate = public["certificate"]
    require(best["weighted_units"] == certificate["weighted_units_ceiling"],
            "weighted certificate differs")
    require(best["defect_bound"] == certificate["defect_upper_bound"],
            "defect bound differs")
    require(best["all_masses_bound"] == certificate["all_masses_upper_bound"],
            "all-masses bound differs")
    require(best["component_count"] == public["selected_component_count"] == 7,
            "selected partition differs")
    require([row["members"] for row in best["rows"]] ==
            [row["members"] for row in certificate["components"]],
            "component memberships differ")
    require([row["anchor"] for row in best["rows"]] ==
            [row["source_anchor"] for row in certificate["components"]],
            "component anchors differ")
    require([row["local_units"] for row in best["rows"]] ==
            [row["local_error_units"] for row in certificate["components"]],
            "local error units differ")
    require([row["classification_units"] for row in best["rows"]] ==
            [row["classification_error_units"] for row in certificate["components"]],
            "classification units differ")

    seven_ball = F(13, 1 << 33)
    require(seven_ball < F(1, 500_000_000), "seven-ball decimal comparison")
    require(local_units(F(1, 64), 40) == (128, 8), "seven-ball local units")

    # The author's (8), with M=2, b=8, r=0, s=1, permits d=4.
    # Its normalized margin is two, hence margin^2/2=2 rather than b+ell=8.
    b, ell = 8, 0
    author_distance2 = F(2 * (b + ell))
    guaranteed_exponent = author_distance2 / 8
    needed_exponent = F(b + ell)
    corrected_distance2 = F(8 * (b + ell))
    require(guaranteed_exponent == F(2) < needed_exponent,
            "schedule gap was not reproduced")
    require(corrected_distance2 / 8 == needed_exponent,
            "corrected separation does not close the exponent")
    # e < 3 follows from 1+1+1/2 plus a geometric bound 1/4 on its tail.
    # Thus psi(2)=1/(2e^2) > 1/18, far above the claimed 1/512.
    require(F(11, 4) < 3, "elementary exponential comparison")
    claimed_eta = F(1, 1 << (b + 1))
    require(F(1, 18) > claimed_eta, "schedule witness does not violate eta claim")

    return {
        "status": "SOURCE_CLUSTER_REVIEW_QUALIFIED_PASS",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "active_labels": len(xs),
        "pair_contraction_checks": pair_checks,
        "candidate_component_counts": [len(part) for part in partitions],
        "selected_component_count": best["component_count"],
        "weighted_units": best["weighted_units"],
        "fixture_defect_bound": best["defect_bound"],
        "fixture_all_masses_bound": best["all_masses_bound"],
        "component_local_units": [row["local_units"] for row in best["rows"]],
        "component_classification_units": [row["classification_units"] for row in best["rows"]],
        "uniform_seven_ball_bound": str(seven_ball),
        "uniform_seven_ball_less_than": "1/500000000",
        "schedule_gap": {
            "b": b,
            "M": 2,
            "ell": ell,
            "author_saturating_distance_squared": str(author_distance2),
            "guaranteed_tail_exponent": str(guaranteed_exponent),
            "needed_tail_exponent": str(needed_exponent),
            "claimed_eta_upper_bound": str(claimed_eta),
            "author_psi_is_strictly_greater_than": "1/18",
            "corrected_saturating_distance_squared": str(corrected_distance2),
            "corrected_separation": "2*max_radius + sqrt(8*s*(b+ell))"
        },
        "verdict": "Core cluster theorem, seven-ball bound, and finite producer accepted; equations (8)-(9) require the stated separation correction"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path, default=HERE / "REVIEW_EXPECTED.json")
    args = parser.parse_args()
    result = audit()
    if args.check:
        require(result == json.loads(args.expected.read_text()), "review record differs")
        print(result["status"])
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
