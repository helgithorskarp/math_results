"""Independent literal-set audit; imports no producer/model/stage code."""

import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import resource
import time

PERIOD = 10080
PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
LABELS = (1, 3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315)
INPUTS = (
    ("shape-obstruction", ((87, 93, 142), (2, 17, 32, 47),
                           (87, 93, 142), (5, 40, 75),
                           (87, 93, 142), (2, 23, 44),
                           (87, 93, 142))),
    ("same-signature-control", ((87, 88), (2, 17), (87, 88), (5, 40),
                                (87, 88), (2, 23), (87, 88))),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_supports(fibers):
    all_supports = []
    phase_pairs = phase_singles = 0
    for points in fibers:
        families = [tuple(frozenset(x for x in points if x % d == a)
                          for a in range(d)) for d in LABELS]
        supports = []
        for j, family in enumerate(families):
            phase_singles += len(family)
            if max(map(len, family)) == len(points):
                supports.append(1 << j)
        for j, k in combinations(range(len(LABELS)), 2):
            best = 0
            for left in families[j]:
                for right in families[k]:
                    phase_pairs += 1
                    best = max(best, len(left | right))
            if best == len(points):
                supports.append((1 << j) | (1 << k))
        all_supports.append(supports)
    return all_supports, phase_singles, phase_pairs


def minimum_cover(supports, q):
    """Enumerate exceptional parents, then solve a resource independent set.

    For q=3, supports of size2 form a graph on resource labels. Singles
    force their resource vertices into the cover. This optimizer has no
    right-subset loop and does not use the producer's A(B) statistic.
    """
    require(q in (2, 3), "audit supports only these two cutoffs")
    best = 10 ** 9
    state_count = 0
    for exceptional in range(1 << len(supports)):
        forced = 0
        adjacent = [0] * len(LABELS)
        for i, options in enumerate(supports):
            if exceptional & (1 << i):
                continue
            for s in options:
                if s.bit_count() == 1:
                    forced |= s
                elif q == 3:
                    j = (s & -s).bit_length() - 1
                    k = (s ^ (1 << j)).bit_length() - 1
                    adjacent[j] |= 1 << k
                    adjacent[k] |= 1 << j

        @lru_cache(None)
        def independent(available):
            if available == 0:
                return 0
            j = max((v for v in range(len(LABELS)) if available & (1 << v)),
                    key=lambda v: (adjacent[v] & available).bit_count())
            without = available & ~(1 << j)
            return max(independent(without), 1 + independent(without & ~adjacent[j]))

        available = ((1 << len(LABELS)) - 1) & ~forced
        covered_resources = len(LABELS) - independent(available)
        state_count += independent.cache_info().currsize
        left, right = (8, 3) if q == 2 else (24, 10)
        best = min(best, left * exceptional.bit_count() + right * covered_resources)
    return best, state_count


def physical_audit(fibers):
    demand = frozenset(x for x in range(PERIOD) if x % 8 != 0 and x % 315 in fibers[x % 8 - 1])
    require(len(demand) == 4 * sum(map(len, fibers)), "incorrect demand lift")
    require(all(all(x % n != a for n, a in PREFIX) for x in demand), "demand violates root")
    capacities = []
    checked_phases = checked_progression_points = 0
    for depth in (16, 32):
        for d in LABELS:
            n = depth * d
            maximum = 0
            for a in range(n):
                actual = frozenset(x for x in range(a, PERIOD, n) if x in demand)
                expected = frozenset(x for x in demand if x % depth == a % depth and x % d == a % d)
                require(actual == expected, "original phase differs from depth/cofactor interpretation")
                maximum = max(maximum, len(actual))
                checked_phases += 1
                checked_progression_points += PERIOD // n
            capacities.append(maximum)
    return demand, capacities, checked_phases, checked_progression_points


def audit(certificate):
    require(certificate.get("schema") == "few-class-erasers-v1", "wrong certificate schema")
    require(certificate.get("agent") == "six-covering-3" and certificate.get("role") == "researcher", "wrong author")
    require(certificate.get("cofactor_period") == 315 and certificate.get("physical_period") == PERIOD, "wrong periods")
    require(certificate.get("binary_parent_depth") == 3 and certificate.get("replication") == 2, "wrong layers")
    require(certificate.get("labels") == list(LABELS), "wrong or cloned cofactor resources")
    original = [16 * d for d in LABELS] + [32 * d for d in LABELS]
    require(certificate.get("first_original_moduli") == original[:12], "wrong first original pool")
    require(certificate.get("last_original_moduli") == original[12:], "wrong last original pool")
    require(len(set(original)) == 24, "original moduli repeat between pools")
    fixtures = certificate.get("fixtures")
    require(isinstance(fixtures, list) and len(fixtures) == 2, "missing fixture")
    evidence = []
    total_singles = total_pairs = total_phases = total_progressions = 0
    for fixture, (name, fibers) in zip(fixtures, INPUTS):
        require(fixture.get("name") == name and fixture.get("prefixes") == list(range(1, 8)), "wrong fixture/prefixes")
        require(fixture.get("fibers") == [list(v) for v in fibers], "wrong literal hole shape")
        signatures = []
        for points in fibers:
            g = 315
            for x in points:
                g = gcd(g, x - points[0])
            signatures.append(g)
        require(fixture.get("signatures") == signatures == [1, 15, 1, 35, 1, 21, 1], "wrong signatures")
        supports, singles, pairs = local_supports(fibers)
        demand, capacities, phases, progressions = physical_audit(fibers)
        require(fixture.get("physical_demands") == len(demand), "wrong physical demand")
        require(fixture.get("uniform_tail_capacities") == capacities, "wrong uniform capacity table")
        require(fixture.get("uniform_tail_capacity") == sum(capacities), "wrong uniform capacity sum")
        cuts = []
        for q, field, threshold in ((2, "single_cost_cut", 20), (3, "pair_cost_cut", 72)):
            options = [[s for s in row if s.bit_count() < q] for row in supports]
            cut = fixture.get(field)
            require(isinstance(cut, dict) and cut.get("supports") == options, "wrong local erasure supports")
            require(cut.get("threshold") == threshold and cut.get("first_erasure_lower_bound") == 8, "wrong count threshold")
            c, b = cut.get("exceptional_parents"), cut.get("right_labels")
            require(isinstance(c, list) and all(type(i) is int and 0 <= i < 7 for i in c) and len(set(c)) == len(c), "bad exceptional parents")
            require(isinstance(b, list) and all(type(d) is int and d in LABELS for d in b) and len(set(b)) == len(b), "bad right cover")
            right_mask = sum(1 << LABELS.index(d) for d in b)
            require(all(i in c or s & right_mask for i, row in enumerate(options) for s in row), "uncovered cheap erasure support")
            supplied = (8 if q == 2 else 24) * len(c) + (3 if q == 2 else 10) * len(b)
            minimum, visited = minimum_cover(options, q)
            require(cut.get("value") == supplied == minimum, "wrong minimum cover")
            require(type(cut.get("excluded")) is bool and cut["excluded"] == (minimum < threshold), "wrong exclusion status")
            cuts.append({"q": q, "minimum": minimum, "threshold": threshold,
                         "excluded": minimum < threshold, "independent_set_states": visited})
        evidence.append({"name": name, "signatures": signatures, "physical_demands": len(demand),
                         "uniform_tail_capacity": sum(capacities), "cuts": cuts,
                         "cheap_support_counts": [len(v) for v in supports],
                         "demand_sha256": sha256(json.dumps(sorted(demand), separators=(",", ":")).encode()).hexdigest()})
        total_singles += singles
        total_pairs += pairs
        total_phases += phases
        total_progressions += progressions
    require(evidence[0]["uniform_tail_capacity"] >= evidence[0]["physical_demands"], "uniform capacity comparison should pass")
    require(evidence[0]["cuts"][1]["excluded"] and not evidence[1]["cuts"][1]["excluded"], "no shape distinction")
    return {"agent": "six-covering-3", "role": "researcher", "status": "EXACT LITERAL AUDIT PASSED",
            "fixtures": evidence, "cofactor_single_phases": total_singles,
            "cofactor_pair_phase_combinations": total_pairs, "physical_original_phases": total_phases,
            "physical_progression_points": total_progressions,
            "scope": "Conditional tail-shape obstruction and passing cut control, not a covering witness or numerical L_min(8) bound."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    parser.add_argument("--expected", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    result = audit(json.loads(args.certificate.read_text()))
    if args.expected is not None:
        require(result == json.loads(args.expected.read_text()), "frozen evidence differs")
    print(json.dumps({"evidence": result, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
