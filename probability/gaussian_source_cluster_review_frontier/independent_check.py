#!/usr/bin/env python3
"""Independent exact audit of the source-cluster Gaussian defect packet.

This checker does not import or execute the producer under review.  It
reconstructs its public fixture through a minimum-spanning-tree description
of single-linkage cuts, checks the analytic handoffs with exact arithmetic,
and records a counterexample to the printed tolerance-schedule arithmetic.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET = REPO / "probability" / "gaussian_prior_localization"
EXPECTED = HERE / "REVIEW_EXPECTED.json"
CAP = Q(7, 50)

PINS = {
    "probability/gaussian_prior_localization/CLUSTER_DEFECT.md":
        "f5f1bcbcbd7df5f0809e6946bcabf7066a39a5ec7cdd9d040b26972b14b2fcf6",
    "probability/gaussian_prior_localization/cluster_defect.py":
        "8574eb8df4c00531d60b5fcaa6ba6ee341690f861265209e2486902bcab6b61f",
    "probability/gaussian_prior_localization/CLUSTER_EXPECTED.json":
        "ae8baba7666357ed9bdb74cc7a42b45b8022b379e7f2d452bea60e2cf34e3edc",
    "probability/gaussian_prior_localization/CLUSTER_FIXTURE.json":
        "08ed8b8f93d3201fa33ea685441388969422e390becbf4dac9f699034b7953d2",
    "probability/gaussian_prior_localization/CLUSTER_INPUTS.json":
        "d62b038525633410a6050fecf2cbf8194a8c50a387b261b2cc0f55bccda41a29",
    "probability/gaussian_prior_localization/DEFECT_LOCALIZATION.md":
        "57b179d6cdb98bab9a1fad42f12c441565c09880c3145588c6a39441d9c5180a",
    "probability/gaussian_majorisation_high_noise_window/SMALL_RADIUS_DEFECT.md":
        "dceeca7a790284d50b7c0fcebe7533859403e064d1b642e121637ec6a9237df1",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def stable_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def check_pins() -> None:
    for name, wanted in PINS.items():
        got = sha256((REPO / name).read_bytes()).hexdigest()
        require(got == wanted, f"changed reviewed input: {name}")


def exact(value: object) -> Q:
    require(type(value) in (int, str), "exact integer or rational string required")
    return Q(value)


def ceiling(value: Q) -> int:
    return -((-value.numerator) // value.denominator)


def distance_squared(a: tuple[Q, ...], b: tuple[Q, ...]) -> Q:
    return sum(((x - y) ** 2 for x, y in zip(a, b)), Q(0))


def binary_sqrt_bounds(value: Q, bits: int) -> tuple[Q, Q]:
    """Dyadic square-root enclosure found by binary search, not isqrt."""
    require(value >= 0 and bits >= 0, "square-root domain")
    scale = 1 << bits
    target = value.numerator * scale * scale
    denominator = value.denominator
    high = 1
    while high * high * denominator <= target:
        high *= 2
    low = high // 2
    while high - low > 1:
        middle = (low + high) // 2
        if middle * middle * denominator <= target:
            low = middle
        else:
            high = middle
    lower = Q(low, scale)
    if lower * lower == value:
        return lower, lower
    upper = Q(high, scale)
    require(lower * lower < value < upper * upper, "invalid root enclosure")
    return lower, upper


def read_fixture(obj: dict[str, object]):
    clouds = []
    for field in ("source", "target"):
        raw = obj[field]
        require(isinstance(raw, list) and raw, "nonempty point list")
        require(all(isinstance(row, list) and len(row) == 3 for row in raw), "dimension three")
        clouds.append([tuple(exact(value) for value in row) for row in raw])
    source, target = clouds
    raw_weights = obj["weights"]
    require(isinstance(raw_weights, list), "weight list")
    weights = [exact(value) for value in raw_weights]
    require(len(source) == len(target) == len(weights), "label counts")
    require(all(weight >= 0 for weight in weights) and sum(weights, Q(0)) == 1,
            "probability weights")
    variance = exact(obj.get("variance", 1))
    require(variance > 0, "positive variance")
    pair_checks = 0
    for i, j in combinations(range(len(source)), 2):
        require(distance_squared(target[i], target[j]) <= distance_squared(source[i], source[j]),
                "not a contraction")
        pair_checks += 1
    # The public fixture has no duplicate active source/image pairs.  Check
    # this explicitly rather than silently adopting the author canonicalizer.
    active = [(x, y, w, i) for i, (x, y, w) in enumerate(zip(source, target, weights)) if w]
    require(len({(x, y) for x, y, _, _ in active}) == len(active), "duplicate active pair")
    return ([x for x, _, _, _ in active], [y for _, y, _, _ in active],
            [w for _, _, w, _ in active], variance, pair_checks)


def prim_tree(distances: list[list[Q]]) -> list[tuple[Q, int, int]]:
    """Construct one exact MST; its threshold forests are single-linkage cuts."""
    n = len(distances)
    require(n > 0, "empty distance matrix")
    reached = {0}
    edges: list[tuple[Q, int, int]] = []
    while len(reached) < n:
        edge = min((distances[i][j], min(i, j), max(i, j))
                   for i in reached for j in range(n) if j not in reached)
        _, i, j = edge
        new_vertex = j if i in reached else i
        require(new_vertex not in reached, "Prim step did not grow tree")
        reached.add(new_vertex)
        edges.append(edge)
    require(len(edges) == n - 1, "MST edge count")
    return edges


def threshold_partitions(distances: list[list[Q]]) -> list[list[list[int]]]:
    n = len(distances)
    tree = prim_tree(distances)
    thresholds = sorted({weight for weight, _, _ in tree})
    partitions = [[[i] for i in range(n)]]
    for threshold in thresholds:
        parent = list(range(n))

        def find(i: int) -> int:
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        for weight, i, j in tree:
            if weight <= threshold:
                a, b = find(i), find(j)
                if a != b:
                    parent[max(a, b)] = min(a, b)
        groups: dict[int, list[int]] = {}
        for i in range(n):
            groups.setdefault(find(i), []).append(i)
        partition = sorted(groups.values(), key=lambda row: row[0])
        if partition != partitions[-1]:
            partitions.append(partition)
    require(len(partitions[-1]) == 1, "MST did not connect all labels")
    return partitions


def local_units(radius_squared: Q, bits: int) -> tuple[int, int | None]:
    units = 1 << bits
    if radius_squared == 0:
        return 0, None
    k = (Q(1, 8) / radius_squared).numerator // (Q(1, 8) / radius_squared).denominator
    if k < 2:
        return ceiling(CAP * units), k
    # Fixtures keep this exponent small.  Evaluating the exact Fraction here
    # is intentionally different from the authors bit-length shortcut.
    value = Q(16 * k * units, 1 << (5 * k))
    return min(ceiling(value), ceiling(CAP * units)), k


def wrong_label_units(center_distance_squared: Q, radius_upper: Q,
                      bits: int, geometry_bits: int) -> int:
    units = 1 << bits
    distance_lower, _ = binary_sqrt_bounds(center_distance_squared, geometry_bits)
    if distance_lower == 0:
        return units
    margin = distance_lower / 2 - radius_upper
    if margin < 0:
        return units
    exponent = (margin * margin / 2).numerator // (margin * margin / 2).denominator + 1
    if exponent >= bits:
        return 1
    return 1 << (bits - exponent)


def evaluate_partition(distances: list[list[Q]], weights: list[Q],
                       partition: list[list[int]], bits: int,
                       geometry_bits: int) -> dict[str, object]:
    units = 1 << bits
    rows = []
    for members in partition:
        radius_squared, anchor = min((max(distances[a][j] for j in members), a)
                                     for a in members)
        _, radius_upper = binary_sqrt_bounds(radius_squared, geometry_bits)
        error_units, k = local_units(radius_squared, bits)
        rows.append({"members": members, "anchor": anchor,
                     "radius_squared": radius_squared, "radius_upper": radius_upper,
                     "mass": sum((weights[j] for j in members), Q(0)),
                     "local_units": error_units, "k": k})

    total = Q(0)
    worst = 0
    for i, row in enumerate(rows):
        classification = sum((wrong_label_units(distances[row["anchor"]][other["anchor"]],
                                                row["radius_upper"], bits, geometry_bits)
                              for j, other in enumerate(rows) if i != j), 0)
        classification = min(units, classification)
        row["classification_units"] = classification
        cost = row["local_units"] + classification
        total += row["mass"] * cost
        worst = max(worst, cost)

    total_ceiling = ceiling(total)
    return {
        "weighted_units_ceiling": total_ceiling,
        "defect_upper_bound": str(min(CAP, Q(total_ceiling, units))),
        "all_masses_upper_bound": str(min(CAP, Q(worst, units))),
        "all_masses_scope":
            "Certified active components only; discarded zero-weight sites are not added to the cover",
        "components": [{
            "members": row["members"],
            "source_anchor": row["anchor"],
            "mass": str(row["mass"]),
            "radius_squared_over_variance": str(row["radius_squared"]),
            "normalized_radius_upper": str(row["radius_upper"]),
            "local_error_units": row["local_units"],
            "local_radius_k": row["k"],
            "classification_error_units": row["classification_units"],
        } for row in rows],
    }


def reconstruct_certificate(obj: dict[str, object], bits: int = 40,
                            geometry_bits: int = 16) -> tuple[dict[str, object], int]:
    source, target, weights, variance, pair_checks = read_fixture(obj)
    distances = [[distance_squared(a, b) / variance for b in source] for a in source]
    partitions = threshold_partitions(distances)
    candidates = [evaluate_partition(distances, weights, partition, bits, geometry_bits)
                  for partition in partitions]
    best = candidates[0]
    for candidate in candidates[1:]:
        if Q(candidate["defect_upper_bound"]) < Q(best["defect_upper_bound"]):
            best = candidate
    normalized = {
        "source": [[str(v) for v in row] for row in source],
        "target": [[str(v) for v in row] for row in target],
        "weights": [str(weight) for weight in weights],
        "variance": str(variance),
    }
    certificate = {
        "status": "ALL_THRESHOLD_DEFECT_UPPER_BOUND",
        "active_labels": len(weights),
        "bits": bits,
        "geometry_bits": geometry_bits,
        "variance": str(variance),
        "normalized_input_sha256": stable_digest(normalized),
        "candidate_component_counts": [len(partition) for partition in partitions],
        "selected_component_count": len(best["components"]),
        "certificate": best,
        "exact_majorisation_certified": Q(best["defect_upper_bound"]) == 0,
        "scope": "Actual all-threshold upper bound; no exact sign is inferred from a positive bound",
    }
    return certificate, pair_checks


def mixture_audit() -> int:
    checks = 0
    values = (Q(0), Q(1, 7), Q(3, 5), Q(11, 6))
    for entries in product(values, repeat=4):
        for threshold in (Q(0), Q(1, 9), Q(2, 3), Q(5, 4), Q(3)):
            interaction = max(Q(0), sum(entries, Q(0)) - threshold)
            interaction -= sum((max(Q(0), value - threshold) for value in entries), Q(0))
            for selected in range(4):
                require(0 <= interaction <= sum(entries, Q(0)) - entries[selected],
                        "hinge interaction inequality")
                checks += 1
    return checks


def voronoi_audit() -> int:
    checks = 0
    centers = [(Q(0), Q(0), Q(0)), (Q(4), Q(-1), Q(2)),
               (Q(-3), Q(5), Q(1)), (Q(2), Q(2), Q(-4))]
    observations = [tuple(Q((i + 2) * (j + 1) - 5, i + j + 3) for j in range(3))
                    for i in range(13)]
    for i, j in combinations(range(len(centers)), 2):
        difference = tuple(centers[j][h] - centers[i][h] for h in range(3))
        d2 = distance_squared(centers[i], centers[j])
        for point in observations:
            left = distance_squared(point, centers[j]) - distance_squared(point, centers[i])
            right = d2 - 2 * sum((difference[h] * (point[h] - centers[i][h])
                                  for h in range(3)), Q(0))
            require(left == right, "Voronoi half-space identity")
            checks += 1
    return checks


def uniform_region_audit() -> dict[str, str]:
    local = Q(16 * 8, 1 << 40)
    require(local == Q(1, 1 << 33), "radius-one-eighth local error")
    exponent = Q(63, 8) ** 2 / 2
    require(exponent == Q(3969, 128) > 31, "seven-ball exponent")
    # e>2 implies each wrong-label term is below 2^-32.
    classification = Q(6, 1 << 32)
    total = local + classification
    require(total == Q(13, 1 << 33) < Q(1, 500_000_000), "uniform region bound")
    return {"local_error": str(local), "tail_exponent": str(exponent),
            "classification_bound": str(classification), "total_bound": str(total)}


def schedule_audit() -> dict[str, object]:
    # Exact upper bound e < sum_{0..4}1/n! + geometric tail from n=5.
    e_upper = sum((Q(1, factorial(n)) for n in range(5)), Q(0)) + Q(1, factorial(5)) * Q(6, 5)
    require(e_upper == Q(1631, 600) < 3, "elementary upper bound for e")

    # Printed condition (8), with b=8, M=2, ell=0, s=1, radii zero:
    # d=4 exactly meets sqrt(2(b+ell)).  But t=d/2=2, so
    # eta=(1/2)e^-2 > 1/(2 e_upper^2) > 1/18 >> 2^-9.
    b, count, ell, distance = 8, 2, 0, Q(4)
    require(distance * distance == 2 * (b + ell), "original schedule boundary")
    exponent = (distance / 2) ** 2 / 2
    eta_lower = Q(1, 2) / (e_upper * e_upper)
    claimed = Q(1, 1 << (b + 1))
    require(exponent == 2 and eta_lower > Q(1, 18) > claimed,
            "schedule counterexample does not separate bounds")

    corrected_checks = 0
    for requested_bits in range(129):
        k = 1 + (requested_bits + 4) // 4
        require(Q(16 * k, 1 << (5 * k)) <= Q(1, 1 << (requested_bits + 1)),
                "local corrected schedule")
        for components in (2, 3, 7, 16, 129, 1025):
            log_count = (components - 2).bit_length()
            # Under d >= 2 r_max + 2 sqrt(2 s (b+ell)), the normalized
            # tail exponent is at least b+ell.  e>2 therefore bounds each
            # term by 2^[-(b+ell+1)].
            total_tail = Q(components - 1, 1 << (requested_bits + log_count + 1))
            require(components - 1 <= 1 << log_count and
                    total_tail <= Q(1, 1 << (requested_bits + 1)),
                    "corrected classification schedule")
            corrected_checks += 1
    return {
        "status": "PRINTED_SCHEDULE_REJECTED_FACTOR_FOUR_IN_EXPONENT",
        "counterexample": {"b": b, "components": count, "ell": ell,
                           "variance": "1", "radii": ["0", "0"],
                           "center_distance": str(distance),
                           "tail_exponent": str(exponent),
                           "certified_eta_lower": str(eta_lower),
                           "claimed_eta_upper": str(claimed)},
        "e_upper": str(e_upper),
        "correction":
            "replace sqrt(2s(b+ell)) by 2 sqrt(2s(b+ell)) in the separation condition",
        "corrected_schedule_checks": corrected_checks,
    }


def run() -> dict[str, object]:
    check_pins()
    published = json.loads((TARGET / "CLUSTER_EXPECTED.json").read_text())
    fixture = json.loads((TARGET / "CLUSTER_FIXTURE.json").read_text())
    rebuilt, pair_checks = reconstruct_certificate(fixture)
    require(rebuilt == published["fixture_certificate"], "fixture certificate mismatch")

    point = {"source": [[1, 2, 3]], "target": [[4, 0, -1]], "weights": [1]}
    point_rebuilt, point_pairs = reconstruct_certificate(point)
    require(point_rebuilt == published["point_certificate"], "point certificate mismatch")

    return {
        "status": "INDEPENDENT_SOURCE_CLUSTER_PARTIAL_REVIEW_PASS",
        "reviewed_commit": "e8f0528f71f366a945090afa8a1ebb5b160e4825",
        "source_pins": len(PINS),
        "accepted_scope":
            "weighted cluster theorem, seven-ball bound, and exact finite producer",
        "rejected_scope": "printed decreasing-error schedule (8)-(9)",
        "arithmetic": "Python integers and Fraction; no floating-point Gaussian evaluation",
        "independent_method": "Prim MST threshold forests and binary-search dyadic roots",
        "mixture_checks": mixture_audit(),
        "voronoi_identity_checks": voronoi_audit(),
        "fixture_pair_contractions": pair_checks,
        "point_pair_contractions": point_pairs,
        "fixture_certificate_digest": stable_digest(rebuilt),
        "fixture_candidate_component_counts": rebuilt["candidate_component_counts"],
        "fixture_selected_component_count": rebuilt["selected_component_count"],
        "fixture_bound": rebuilt["certificate"]["defect_upper_bound"],
        "fixture_all_masses_bound": rebuilt["certificate"]["all_masses_upper_bound"],
        "uniform_region": uniform_region_audit(),
        "schedule": schedule_audit(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check:
        require(result == json.loads(EXPECTED.read_text()),
                "review output differs from REVIEW_EXPECTED.json")
        print(result["status"], stable_digest(result))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
