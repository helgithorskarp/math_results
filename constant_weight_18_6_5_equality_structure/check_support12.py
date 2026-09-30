#!/usr/bin/env python3
"""Exact checks of necessary local carriers, not a search for 72-word codes."""

import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def path_checks():
    """Count matching indicators directly, then impose pair codegrees.

    A fixed point in H has exactly one leave triple on each internal
    path point. Enumerate binary path-edge subsets with that degree
    condition. These two subsets are the possible indicator patterns.
    The remaining S third points are counted as actual consecutive
    three-point sets, rather than using the formula for c_i in the proof.
    """
    rows = []
    tested_indicators = 0
    for length in range(3, 19):
        edges = list(zip(range(length - 1), range(1, length)))
        patterns = []
        for flags in product((0, 1), repeat=len(edges)):
            tested_indicators += 1
            degrees = [0] * length
            for flag, (u, v) in zip(flags, edges):
                if flag:
                    degrees[u] += 1
                    degrees[v] += 1
            if all(degrees[x] == 1 for x in range(1, length - 1)):
                patterns.append(flags)
        require(len(patterns) == 2, "path must have two indicator patterns")
        triples = [frozenset((x - 1, x, x + 1))
                   for x in range(1, length - 1)]
        s_thirds = [sum(set(edge) <= triple for triple in triples)
                    for edge in edges]
        witnesses = []
        # All positive integer weights are at most four on a path edge.
        # Internal point weight sum five uniquely extends the first one.
        for first in range(1, 5):
            weights = [first]
            while len(weights) < len(edges):
                weights.append(5 - weights[-1])
            if 5 - weights[0] > 3 or 5 - weights[-1] > 3:
                continue  # External endpoints are in H, whose weights <= 3.
            for h in range(19 - length):
                for count0 in range(h + 1):
                    counts = (count0, h - count0)
                    covered = [s_thirds[j] + sum(counts[p] * patterns[p][j]
                                                for p in range(2))
                               for j in range(len(edges))]
                    if covered == [1 + 3 * w for w in weights]:
                        witnesses.append({"h": h, "weights": weights,
                                          "indicator_pattern_counts": list(counts)})
        rows.append({"length": length, "indicator_patterns": len(patterns),
                     "possible_h": sorted({w["h"] for w in witnesses}),
                     "witnesses": witnesses})
    require(rows[0]["possible_h"] == [15], "length-three boundary differs")
    require(rows[1]["possible_h"] == [14], "length-four boundary differs")
    require(all(not r["witnesses"] for r in rows[2:]),
            "a longer path passed the necessary conditions")
    return {"indicator_strings_checked": tested_indicators, "lengths": rows}


def omission_matching(nonedges, capacities):
    """Assign each nonedge to one endpoint's distinct omission slot."""
    slots = [v for v, cap in enumerate(capacities) for _ in range(cap)]
    if len(nonedges) > len(slots):
        return False
    assignment = [None] * len(slots)

    def augment(edge_index, visited):
        u, v = nonedges[edge_index]
        for slot, endpoint in enumerate(slots):
            if endpoint not in (u, v) or slot in visited:
                continue
            visited.add(slot)
            previous = assignment[slot]
            if previous is None or augment(previous, visited):
                assignment[slot] = edge_index
                return True
        return False

    return all(augment(i, set()) for i in range(len(nonedges)))


def omission_subset_test(nonedges, capacities):
    """Independent endpoint-capacity inequalities on every vertex subset.

    Necessity is immediate. Sufficiency follows from the ordinary Hall
    matching theorem: any set of nonedge nodes has its endpoints in W,
    so at most |E(W)| nodes must use the sum of capacities in W.
    """
    for mask in range(1 << len(capacities)):
        needed = sum((mask >> u) & (mask >> v) & 1 for u, v in nonedges)
        available = sum(cap for v, cap in enumerate(capacities) if mask >> v & 1)
        if needed > available:
            return False
    return True


def root_checks():
    """Exhaust every graph on six labeled roots and every even marking.

    A mark says that the corresponding point of S is isolated in T[S].
    At h=12 an isolated root has one omission slot, a paired root two.
    Further leave and block compatibility conditions are not tested.
    """
    pairs = list(combinations(range(6), 2))
    subsets = {a: list(combinations(range(6), a)) for a in (0, 2, 4, 6)}
    degree_carriers = Counter()
    admissible = {a: Counter() for a in subsets}
    marked_cases = 0
    for mask in range(1 << len(pairs)):
        edges = [e for i, e in enumerate(pairs) if mask >> i & 1]
        degrees = [sum(v in e for e in edges) for v in range(6)]
        if max(degrees) > 2:
            continue
        degree_carriers[len(edges)] += 1
        nonedges = [e for i, e in enumerate(pairs) if not (mask >> i & 1)]
        for a, choices in subsets.items():
            for isolated in choices:
                marked_cases += 1
                capacities = [1 if v in isolated else 2 for v in range(6)]
                matched = omission_matching(nonedges, capacities)
                require(matched == omission_subset_test(nonedges, capacities),
                        "matching and independent subset inequalities disagree")
                require(matched == (len(edges) >= 3 + a),
                        "six-root carrier has an additional or weaker count")
                if matched:
                    admissible[a][len(edges)] += 1
    return {
        "graph_masks_checked": 1 << len(pairs),
        "max_degree_two_graphs_by_edges": dict(sorted(degree_carriers.items())),
        "marked_cases_checked": marked_cases,
        "admissible_marked_graphs_by_isolated_count_and_edges": {
            str(a): dict(sorted(counts.items())) for a, counts in admissible.items()},
        "matching_and_subset_checks_agree": True,
    }


def arithmetic_checks():
    rows = []
    for h in (9, 10, 11):
        s = 18 - h
        # A simple graph of maximum degree two has at most s edges.
        minimum_nonedges = s * (s - 1) // 2 - s
        maximum_omissions = s * (h - 10)  # a >= 0
        require(minimum_nonedges > maximum_omissions, "bound fails")
        rows.append({"h": h, "s": s,
                     "minimum_root_nonedges": minimum_nonedges,
                     "maximum_omissions": maximum_omissions})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true",
                        help="regenerate the small exact validation report")
    args = parser.parse_args()
    report = {"path_carrier": path_checks(), "h_9_to_11": arithmetic_checks(),
              "h_12_root_carrier": root_checks(),
              "global_72_word_exclusion": False}
    data = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("ascii")
    if args.write_expected:
        (HERE / "support12_expected.json").write_bytes(data)
    else:
        require((HERE / "support12_expected.json").read_bytes() == data,
                "exact output disagrees with support12_expected.json")
    print(data.decode("ascii"), end="")


if __name__ == "__main__":
    main()
