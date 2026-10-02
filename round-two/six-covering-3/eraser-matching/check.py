"""Independent literal verifier. Does not import model.py or produce.py."""

import argparse
from fractions import Fraction
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def graph_by_residues(period, cofactor, parent_power, prefixes, fibers, resources, copies):
    require(len(prefixes) == len(fibers), "parent/fiber count")
    require(len(set(prefixes)) == len(prefixes), "duplicate parent")
    power = parent_power * copies
    require(period % (power * cofactor) == 0, "period factorization")
    require(all(0 <= r < parent_power for r in prefixes), "parent prefix range")
    require(resources == sorted(set(resources)), "duplicate/unsorted resource")
    require(all(type(d) is int and d > 0 and cofactor % d == 0 for d in resources),
            "invalid divisor resource")
    result = []
    targets = []
    for r, v in zip(prefixes, fibers):
        require(v and len(v) == len(set(v)), "empty/duplicate cofactor demand")
        require(all(type(z) is int and 0 <= z < cofactor for z in v), "cofactor range")
        for child in range(copies):
            u = r + parent_power * child
            target = [x for x in range(period) if x % power == u and x % cofactor in v]
            require(len(target) == len(v) * period // (power * cofactor), "literal fiber size")
            result.append([d for d in resources
                           if len({x % (power * d) for x in target}) == 1])
            targets.append(target)
    return result, targets


def check_matching(graph, resources, cert):
    pairs = cert["matching"]
    left = cert["cover_left"]
    right = cert["cover_right"]
    require(left == sorted(set(left)) and right == sorted(set(right)), "cover duplicates")
    require(all(type(i) is int and 0 <= i < len(graph) for i in left), "cover left range")
    require(set(right) <= set(resources), "cover resource range")
    require(len({i for i, d in pairs}) == len(pairs), "matching repeats target")
    require(len({d for i, d in pairs}) == len(pairs), "matching repeats original resource")
    require(all(type(i) is int and 0 <= i < len(graph) and d in graph[i]
                for i, d in pairs), "matching contains nonedge")
    require(all(i in left or d in right for i, row in enumerate(graph) for d in row),
            "uncovered graph edge")
    require(len(pairs) == len(left) + len(right) == cert["value"], "matching/cover values differ")


def check_certificate(packet):
    require(packet["schema"] == 1, "schema")
    require(packet["agent"] == "six-covering-3" and packet["role"] == "researcher", "identity")
    t = packet["toy"]
    require((t["ambient_period"], t["cofactor"], t["parent_power"], t["prime"]) ==
            (1680, 105, 4, 2), "toy setting changed")
    require(t["parent_prefixes"] == [1, 2] and t["resources_per_layer"] == [1, 3, 5, 7],
            "toy resource inventory")
    literal_v = [z for z in range(105)
                 if (z % 3, z % 5, z % 7) in [(0, 1, 0), (0, 0, 1), (1, 0, 0)]]
    require(t["points"] == literal_v == [15, 21, 70], "triangle demand")
    graph, _ = graph_by_residues(1680, 105, 4, [1, 2], [literal_v, literal_v], [1, 3, 5, 7], 2)
    require(graph == t["graph"] == [[1]] * 4, "toy literal graph")
    check_matching(graph, [1, 3, 5, 7], t["matching_certificate"])
    cover = t["weighted_cover"]
    require(cover["cover_left"] == [] and cover["cover_right"] == [1], "toy weighted cover")
    require(cover["parent_subset"] == 3, "toy subset")
    require(cover["value"] == 4 * len(cover["cover_left"]) + 3 * len(cover["cover_right"]) == 3,
            "weighted cost")
    threshold = 4 * len(graph) - 3 * len(t["resources_per_layer"])
    require(t["two_layer_threshold"] == threshold == 4 and cover["value"] < threshold,
            "strict two-layer cut")
    require(t["integer_completion"] is False, "toy scope/status")
    demand = [x for x in range(1680) if x % 4 in [1, 2] and x % 105 in literal_v]
    require(len(demand) == 24, "physical demand size")
    coverage = {x: Fraction(0) for x in demand}
    rows = t["fractional_phases"]
    require(sorted(row["modulus"] for row in rows) == [8, 16, 24, 40, 48, 56, 80, 112],
            "eight original moduli")
    for row in rows:
        n = row["modulus"]
        phases = row["phases"]
        require(len({a for a, num, den in phases}) == len(phases), "duplicate fractional phase")
        require(all(type(a) is int and 0 <= a < n and type(num) is int and type(den) is int
                    and num > 0 and den > 0 for a, num, den in phases), "fractional phase legality")
        require(sum((Fraction(num, den) for a, num, den in phases), Fraction(0)) == 1,
                "resource marginal not one")
        for x in demand:
            coverage[x] += sum((Fraction(num, den) for a, num, den in phases if x % n == a),
                               Fraction(0))
    require(t["point_coverage"] == [9, 8] and set(coverage.values()) == {Fraction(9, 8)},
            "literal fractional coverage")

    s = packet["saturated_terminal_control"]
    require((s["ambient_period"], s["parent_power"], s["cofactor"]) == (10080, 16, 315),
            "terminal setting")
    require(s["parent_prefixes"] == [1, 2, 3, 4, 5, 6], "terminal parents")
    require(s["signatures"] == [3, 15, 21, 63, 105, 315], "terminal signatures")
    require(s["fibers"] == [[2, 5], [2, 17], [2, 23], [2, 65], [2, 107], [2]],
            "terminal fibers")
    resources = [d for d in range(1, 316) if 315 % d == 0]
    sat_graph, sat_targets = graph_by_residues(10080, 315, 16, s["parent_prefixes"],
                                              s["fibers"], resources, 2)
    require(sat_graph == s["graph"], "terminal literal eraser graph")
    check_matching(sat_graph, resources, s["matching_certificate"])
    require(s["matching_certificate"]["value"] == 12, "terminal perfect matching")
    phases = s["completion_phases"]
    require(sorted(n for n, a in phases) == [32 * d for d in resources], "terminal original labels")
    require(all(type(a) is int and 0 <= a < n for n, a in phases), "terminal phase legality")
    sat_points = sorted(x for target in sat_targets for x in target)
    require(len(sat_points) == 22 and len(set(sat_points)) == 22, "terminal demands")
    require(all(any(x % n == a for n, a in phases) for x in sat_points), "terminal literal completion")

    current = packet["period10080"]
    require((current["ambient_period"], current["base_period"], current["cofactor"]) ==
            (10080, 2520, 315), "current period")
    require(current["prefix"] == [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]], "current open prefix")
    require(current["cofactor_resources"] == resources, "current cofactor resources")
    require(current["subset_minimum_eraser_labels"] == {"5": 2, "6": 4, "7": 7},
            "current subset cuts")
    for count, minimum in current["subset_minimum_eraser_labels"].items():
        require(minimum == (8 * int(count) - 36 + 2) // 3, "cut arithmetic")
    require(current["max_nonempty_signature_one_fibers"] == 4, "plain fiber limit")
    return {"toy_points": len(demand), "fractional_entries": sum(len(row["phases"]) for row in rows),
            "toy_matching": 1, "toy_weighted_cost": 3, "toy_threshold": 4,
            "fractional_coverage": "9/8", "terminal_points": len(sat_points),
            "terminal_matching": 12}


def check_decoder(packet):
    current = packet["period10080"]
    period, base, cofactor = 10080, 2520, 315
    prefix = current["prefix"]
    used = {n for n, a in prefix}
    resources = [n for n in range(8, period + 1) if period % n == 0 and n not in used]
    base_resources = [n for n in resources if base % n == 0]
    tail_resources = [n for n in resources if base % n != 0]
    require(len(base_resources) == current["unused_base_count"] == 36, "base resource count")
    require(len(tail_resources) == current["unused_tail_count"] == 24, "tail resource count")
    expected_tail = sorted(power * d for power in [16, 32]
                           for d in range(1, 316) if cofactor % d == 0)
    require(tail_resources == expected_tail and len(resources) == 60, "complete original inventory")
    base_holes = [x for x in range(base) if not any(x % n == a for n, a in prefix)]
    physical_holes = [x for x in range(period) if not any(x % n == a for n, a in prefix)]
    require(len(base_holes) == current["base_holes"] == 1398, "base holes")
    require(len(physical_holes) == current["physical_holes"] == 5592, "physical holes")
    require([sum(x % 8 == r for x in base_holes) for r in range(8)] == current["base_fiber_sizes"],
            "base fiber sizes")
    require(set(physical_holes) == {x + base * j for x in base_holes for j in range(4)},
            "four-copy physical residual")

    # Exhaust every original phase. Each raw class has period/n points.
    # Its literal points satisfy the decoded predicate, whose point count
    # is independently period/n. Equality of these finite sets follows.
    phase_count = point_count = 0
    require(len({(x % 32, x % cofactor) for x in range(period)}) == period,
            "literal CRT coordinate bijection")
    for n in resources:
        headers = set()
        for a in range(n):
            phase_count += 1
            if base % n == 0:
                for x in range(a, period, n):
                    require((x % base) % n == a, "base phase copy decoding")
                    point_count += 1
            else:
                power = 16 if n % 32 != 0 else 32
                d = n // power
                u, b = a % power, a % d
                r, child = u % 8, u // 8
                headers.add((r, child, b))
                expected_copies = 2 if power == 16 else 1
                require(expected_copies * (cofactor // d) == period // n, "tail decoded size")
                for x in range(a, period, n):
                    z = x % cofactor
                    j = (x % 32) // 8
                    require(x % 8 == r and z % d == b, "tail prefix/cofactor predicate")
                    require((j % 2 == child) if power == 16 else (j == child), "tail copy predicate")
                    point_count += 1
        if base % n != 0:
            require(len(headers) == n, "complete tail phase headers")
    require(point_count == len(resources) * period, "complete phase-member count")
    return {"original_resources": len(resources), "base_resources": len(base_resources),
            "tail_resources": len(tail_resources), "all_phases": phase_count,
            "all_positive_members": point_count, "base_holes": len(base_holes),
            "physical_holes": len(physical_holes)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--certificate-only", action="store_true")
    args = parser.parse_args()
    packet = json.loads(args.certificate.read_text())
    result = {"certificate": check_certificate(packet)}
    if not args.certificate_only:
        result["decoder"] = check_decoder(packet)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
