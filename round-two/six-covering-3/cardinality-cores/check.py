"""Independent certificate audit; imports no producer, model or encoder."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def assignment(smaller, larger):
    """Different smaller labels must go to different larger resources."""
    for ordered in permutations(smaller):
        if all(a % b == 0 for a, b in zip(larger, ordered)):
            return ordered
    return None


def local_supports(points, labels):
    if not points:
        return [frozenset()]
    universe = frozenset(points)
    families = {d: set(frozenset(x for x in universe if x % d == a)
                       for a in range(d)) for d in labels}
    supports = []
    for d in labels:
        if universe in families[d]:
            supports.append(frozenset((d,)))
    for d, e in combinations(labels, 2):
        if any(left | right == universe for left in families[d] for right in families[e]):
            supports.append(frozenset((d, e)))
    return supports


def audit(cert):
    require(cert.get("schema") == "covering-cardinality-cores-v1", "schema")
    require(cert.get("agent") == "six-covering-3" and cert.get("role") == "researcher", "author")
    labels = tuple(d for d in range(1, 316) if 315 % d == 0)
    prefix = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
    base = [n for n in range(8, 2521) if 2520 % n == 0 and n not in {d for d, a in prefix}]
    require(cert.get("D") == list(labels), "resource labels")
    require(cert.get("prefix") == [list(p) for p in prefix], "root prefix")
    require(cert.get("base_moduli") == base and len(base) == 36, "shared base labels")
    originals = {(1,) + rest: k for b, k in ((2, 3), (4, 2), (7, 1))
                 for rest in combinations(labels[1:], b - 1)}
    require(len(originals) == cert.get("original_predicates") == 638, "predicate count")
    front = cert.get("frontier")
    require(isinstance(front, list) and len(front) == cert.get("frontier_predicates") == 15, "frontier count")
    require(Counter(row["required"] for row in front) == {3: 3, 2: 6, 1: 6}, "frontier thresholds")
    covered_resource_pairs = front_pair_count = 0
    for row in front:
        B = tuple(row["B"])
        require(B in originals and row["required"] == originals[B], "frontier is not an original constraint")
        allowed = set(labels) - set(B)
        pair_rows = row["pairs"]
        require(len(set(map(tuple, pair_rows))) == len(pair_rows), "duplicate pair")
        require(all(len(p) == 2 and p[0] < p[1] and set(p) <= allowed for p in pair_rows), "illegal or cloned pair")
        for larger in combinations(sorted(allowed), 2):
            require(any(assignment(p, larger) is not None for p in pair_rows), "incomplete local pair reduction")
            covered_resource_pairs += 1
        front_pair_count += len(pair_rows)
    maps = cert.get("implications")
    require(isinstance(maps, list) and len(maps) == len(originals), "missing implication")
    require(all(isinstance(m, list) and len(m) == 2 and type(m[0]) is int
                and 0 <= m[0] < (1 << len(labels)) for m in maps), "bad target mask")
    decoded = [(tuple(d for j, d in enumerate(labels) if mask & (1 << j)), i)
               for mask, i in maps]
    require(len({B for B, i in decoded}) == len(maps), "duplicate target")
    require({B for B, i in decoded} == set(originals), "wrong target universe")
    mapped_pairs = 0
    for B, i in decoded:
        require(type(i) is int and 0 <= i < len(front), "bad frontier index")
        source = front[i]
        require(source["required"] >= originals[B], "threshold implication reversed")
        target_pairs = tuple(combinations(sorted(set(labels) - set(B)), 2))
        for larger in source["pairs"]:
            require(any(assignment(p, larger) is not None for p in target_pairs), "support implication reversed or incomplete")
            mapped_pairs += 1

    different_families = set()
    minimal_by_B = {}
    for B in originals:
        pairs = tuple(combinations(sorted(set(labels) - set(B)), 2))
        minima = tuple(p for p in pairs if not any(q != p and assignment(q, p) is not None for q in pairs))
        different_families.add(minima)
        minimal_by_B[B] = minima
    require(cert.get("distinct_pair_families") == len(different_families) == 155, "intermediate family census")
    require(all(tuple(map(tuple, row["pairs"])) == minimal_by_B[tuple(row["B"])] for row in front), "frontier pair table is not minimal")

    # Audit the mathematical class-containment rule with actual315-point sets.
    classes = {d: tuple(frozenset(range(a, 315, d)) for a in range(d)) for d in labels}
    literal_divisor_phases = 0
    for d in labels:
        for e in labels:
            if d % e != 0:
                continue
            for a in range(d):
                require(classes[d][a] <= classes[e][a % e], "literal congruence containment failed")
                literal_divisor_phases += 1
    special = next(row for row in front if row["B"] == [1, 3])
    require(special["pairs"] == [[5, 7], [5, 9], [5, 15], [7, 9], [7, 21]], "five-pair subfamily changed")
    phase_pair_audits = 0
    for d, e in combinations([x for x in labels if x not in (1, 3)], 2):
        smaller = next(assignment(p, (d, e)) for p in special["pairs"]
                       if assignment(p, (d, e)) is not None)
        for a in range(d):
            for b in range(e):
                old_union = classes[d][a] | classes[e][b]
                new_union = classes[smaller[0]][a % smaller[0]] | classes[smaller[1]][b % smaller[1]]
                require(old_union <= new_union and smaller[0] != smaller[1], "phase-union domination failed")
                phase_pair_audits += 1

    padding_cases = 0
    for m in range(8):
        for b in range(13):
            for a in range(m + 1):
                old = 24 * a + 10 * b >= 12 * m + 6 * max(0, 2 * m - 6) - 60
                padded = 24 * (a + 7 - m) + 10 * b >= 72
                require(old == padded, "empty-padding equivalence failed")
                padding_cases += 1
    fixtures = (
        ("shape-obstruction", ((87, 93, 142), (2, 17, 32, 47), (87, 93, 142),
                                (5, 40, 75), (87, 93, 142), (2, 23, 44), (87, 93, 142))),
        ("same-signature-control", ((87, 88), (2, 17), (87, 88), (5, 40),
                                     (87, 88), (2, 23), (87, 88))),
        ("all-empty", ((),) * 7),
        ("seven-singletons", ((2,),) * 7),
        ("two-nonempty", ((87, 93, 142), (2, 17, 32, 47)) + ((),) * 5),
        ("seven-gcd-one-doubletons", ((2, 3),) * 7),
    )
    fixture_rows = []
    for name, fibers in fixtures:
        require(all(all(x % d != a for d, a in prefix)
                    for x in range(2520) if x % 8 and x % 315 in fibers[x % 8 - 1]),
                "fixture lies outside the initial root holes")
        supports = [local_supports(v, labels) for v in fibers]
        if name == "seven-gcd-one-doubletons":
            require(all({s for s in row if len(s) == 1} == {frozenset((1,))}
                        for row in supports), "prior q2 counterexample has an extra single eraser")
        original_values = {B: sum(any(not (set(B) & support) for support in ss) for ss in supports)
                           for B in originals}
        actual = all(original_values[B] >= originals[B] for B in originals)
        compressed = all(original_values[tuple(row["B"])] >= row["required"] for row in front)
        require(actual == compressed, "literal638/15 equivalence failed")
        fixture_rows.append({"name": name, "passed": actual,
                             "violated_originals": sum(original_values[B] < originals[B] for B in originals),
                             "violated_frontier": sum(original_values[tuple(r["B"])] < r["required"] for r in front)})
    require([row["passed"] for row in fixture_rows] == [False, True, True, True, True, True], "fixture status changed")
    require(cert.get("frontier_full_phase_pairs_per_fiber") == sum(d * e for row in front for d, e in row["pairs"]) == 31037, "phase count")
    return {"agent": "six-covering-3", "role": "researcher", "status": "EXACT IMPLICATION AUDIT PASSED",
            "original_predicates": len(originals), "frontier_predicates": len(front),
            "distinct_pair_families": len(different_families),
            "threshold_counts": {"3": 3, "2": 6, "1": 6},
            "frontier_pairs": front_pair_count, "covered_original_resource_pairs": covered_resource_pairs,
            "checked_implication_pairs": mapped_pairs, "literal_divisor_phase_containments": literal_divisor_phases,
            "literal_B13_phase_union_containments": phase_pair_audits,
            "B13_reduced_phase_pairs": sum(d * e for d, e in special["pairs"]),
            "empty_padding_cases": padding_cases, "fixtures": fixture_rows,
            "gcd_one_doubletons_prior_q2_cover": {"value": 3, "threshold": 20, "excluded": True},
            "certificate_sha256": sha256(json.dumps(cert, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "scope": "Equivalent necessary cut family; no claim of logical irredundancy, tail sufficiency or root exclusion."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    ap.add_argument("--expected", type=Path)
    args = ap.parse_args()
    start = time.monotonic()
    evidence = audit(json.loads(args.certificate.read_text()))
    if args.expected is not None:
        require(evidence == json.loads(args.expected.read_text()), "frozen evidence differs")
    print(json.dumps({"evidence": evidence, "seconds": round(time.monotonic() - start, 6),
                      "max_RSS_KiB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))
