#!/usr/bin/env python3
"""Definition-level checker, without importing the classifier or its pruning.

All rejected boxes (819 points total) are enumerated directly. Surviving
count matrices and the three fractional witnesses are checked literally.
"""

import argparse
import json
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations_with_replacement, product
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEGREES = tuple(range(18, 25))
WEIGHT = {18: 21, 19: 12, 20: 3, 21: 0, 22: 3, 23: 12, 24: 21}
EXTREMA = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}
HEADER = "counts_18_to_24\tM\tW\tsplit_count\tstatus\tedge_counts\thalf_counts\tmultipliers"


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def profile_universe():
    """Budget recursion, independent of the generator's Cartesian product."""
    output = set()
    exceptional = tuple(d for d in DEGREES if d != 21)

    def visit(position, budget, counts):
        if position == len(exceptional):
            counts = dict(counts)
            counts[21] = 43-sum(counts.values())
            degree_sum = sum(d*n for d, n in counts.items())
            used = 39-budget
            if used % 6 == 3 and degree_sum % 2 == 0 and degree_sum <= 902:
                output.add(tuple(counts[d] for d in DEGREES))
            return
        degree = exceptional[position]
        for count in range(budget // WEIGHT[degree] + 1):
            visit(position+1, budget-count*WEIGHT[degree], counts+[(degree, count)])

    visit(0, 39, [])
    return output


def edge_types(counts):
    ns = dict(zip(DEGREES, counts))
    active = [d for d in DEGREES if d != 21 and ns[d]]
    edges = []
    caps = []
    for a, b in combinations_with_replacement(active, 2):
        capacity = comb(ns[a], 2) if a == b else ns[a]*ns[b]
        if capacity:
            edges.append((a, b))
            caps.append(capacity)
    return ns, active, edges, caps


def local_cap(degree, m):
    # Direct substitution into the neighborhood-degree identity, not b(d).
    return m-comb(42-degree, 2)+EXTREMA[degree]+EXTREMA[42-degree]-14-21*degree


def margins(counts, values):
    ns, active, edges, caps = edge_types(counts)
    require(len(values) == len(edges), ("wrong edge-vector length", counts))
    require(all(0 <= x <= c for x, c in zip(values, caps)), "edge capacity")
    m = sum(d*n for d, n in ns.items()) // 2
    incidence = {d: 0 for d in active}
    neighbor_weight = {d: 0 for d in active}
    for (a, b), value in zip(edges, values):
        incidence[a] += value
        incidence[b] += value
        neighbor_weight[a] += (b-21)*value
        neighbor_weight[b] += (a-21)*value
    result = [ns[d]*local_cap(d, m)-neighbor_weight[d] for d in active]
    central_weight = sum((d-21)*(ns[d]*d-incidence[d]) for d in active)
    result.append(ns[21]*local_cap(21, m)-central_weight)
    weight = sum(WEIGHT[d]*ns[d] for d in DEGREES)
    require(sum(result) == Fraction(43-weight, 2), "total excess identity")
    return result


def accepted(counts, values):
    return all(x >= 0 for x in margins(counts, values))


def integer_list(field):
    return tuple(map(int, field.split(","))) if field != "-" else ()


def verify(path):
    extrema_path = HERE.parent/"ramsey_r55_local_extremal_deficiency"/"extrema.json"
    require(sha256(extrema_path.read_bytes()).hexdigest() ==
            "7233dd701f47de79c65ecccb6b06ad8f79b16b92c08cfcf73bcef1ed3b4d5b10", "extrema provenance")
    require({int(d): n for d, n in json.loads(extrema_path.read_text())["max_edges"].items()}
            == EXTREMA, "extrema values")
    for d in DEGREES:
        require(WEIGHT[d] == 29-(2*(EXTREMA[d]+EXTREMA[42-d])-1722+3*d*(42-d)),
                "degree weight derivation")
    lines = path.read_text(encoding="ascii").splitlines()
    require(lines and lines[0] == HEADER, "header")
    seen = set()
    hist = Counter()
    split_hist = Counter()
    rejected_points = fractional_cases = linear_cases = 0
    retained_types = excluded_types = 0
    first_witness = None
    for line in lines[1:]:
        fields = line.split("\t")
        require(len(fields) == 8, "row width")
        raw, cross, weight, splits, status, values, halves, mult = fields
        counts = integer_list(raw)
        require(len(counts) == 7 and min(counts) >= 0 and sum(counts) == 43, "counts")
        require(counts not in seen, "duplicate profile")
        seen.add(counts)
        ns, active, edges, caps = edge_types(counts)
        m = sum(d*n for d, n in ns.items()) // 2
        require(int(cross) == m-231, "M")
        require(int(weight) == sum(WEIGHT[d]*ns[d] for d in DEGREES), "W")
        # The anchor has degree 21 and is removed before splitting its neighbors.
        split_count = 0
        for a_counts in product(*(range(ns[d]+1) for d in active)):
            if sum((d-21)*a for d, a in zip(active, a_counts)) == m-451:
                require(sum(a_counts) <= 21 and sum(ns[d] for d in active)-sum(a_counts) <= 21,
                        "split size")
                split_count += 1
        require(int(splits) == split_count, "split multiplicity")
        hist[int(cross), status] += 1
        split_hist[int(cross), status] += split_count
        if status == "feasible":
            vector = integer_list(values)
            require(accepted(counts, vector), ("invalid witness", counts))
            require(halves == mult == "-", "survivor extras")
            retained_types += 1
            first_witness = first_witness or (counts, vector)
        else:
            require(status == "excluded" and values == "-", "status")
            excluded_types += 1
            # No branch pruning or classifier import: visit every bounded tuple.
            for candidate in product(*(range(c+1) for c in caps)):
                rejected_points += 1
                require(not accepted(counts, candidate), ("false exclusion", counts, candidate))
            if halves != "-":
                require(mult == "-", "mixed obstruction kinds")
                vector = tuple(Fraction(x, 2) for x in integer_list(halves))
                require(any(x.denominator == 2 for x in vector), "fractional witness is integral")
                require(accepted(counts, vector), "invalid half-integral witness")
                fractional_cases += 1
            else:
                multipliers = integer_list(mult)
                require(len(multipliers) == len(active) and min(multipliers) >= 0, "multipliers")
                weighted = dict(zip(active, multipliers))
                rhs = sum(weighted[d]*ns[d]*local_cap(d, m) for d in active)
                lower = sum(cap*min(0, weighted[a]*(b-21)+weighted[b]*(a-21))
                            for (a, b), cap in zip(edges, caps))
                require(lower > rhs, "invalid linear contradiction")
                linear_cases += 1
    require(seen == profile_universe(), "profile universe mismatch")
    require((retained_types, excluded_types, rejected_points, linear_cases, fractional_cases)
            == (88, 16, 819, 13, 3), "aggregate totals")
    expected_global = [(1,0), (3,0), (7,0), (13,1), (21,0), (20,7), (23,8)]
    expected_split = [(1,0), (5,0), (17,0), (39,1), (69,0), (85,10), (105,17)]
    for i, cross in enumerate(range(214, 221)):
        require((hist[cross,"feasible"], hist[cross,"excluded"]) == expected_global[i], hist)
        require((split_hist[cross,"feasible"], split_hist[cross,"excluded"]) == expected_split[i], split_hist)

    # Reject an out-of-box purported witness without dependence on assertions/-O.
    counts, vector = first_witness
    _, _, _, caps = edge_types(counts)
    if not caps:
        counts = (0, 0, 3, 40, 0, 0, 0)
        vector = (0,)
        caps = (3,)
    try:
        margins(counts, (caps[0]+1,)+vector[1:])
    except ValueError:
        pass
    else:
        raise ValueError("out-of-capacity witness was accepted")

    print("PASS pinned extrema manifest and derived degree weights")
    print("PASS complete hard-branch universe: 104 global profiles and 349 split profiles")
    print("PASS degree-weight margins sum exactly to paired excess (43-W)/2")
    print("PASS integer count-matrix witnesses: 88 profiles (not graph constructions)")
    print("PASS excluded integer boxes: 16 profiles, all 819 tuples rejected directly")
    print("PASS real-valued linear obstruction certificates: 13 profiles")
    print("PASS half-integral witnesses for the other 3 exclusions; integrality is necessary")
    print("PASS retained global counts M214..220: 1,3,7,13,21,20,23 total=88")
    print("PASS retained split counts M214..220: 1,5,17,39,69,85,105 total=321")
    print("PASS excluded split counts M214..220: 0,0,0,1,0,10,17 total=28")
    print("PASS malformed edge-capacity witness rejected")
    print("SCOPE necessary aggregate relaxation only; all 321 survivors remain unproved")
    print("certificate_sha256="+sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path, nargs="?", default=HERE/"PROFILES.tsv")
    verify(parser.parse_args().certificate)
