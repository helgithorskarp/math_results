"""Independent exact checks for the written regular Book review.

Actual author: six-reviewer-4, independent reviewer, 2026-10-01.
Standard library only. No author-code import or author fixture is used.
These checks validate small identities and Gram rigidity, not a host census
or the universal written spectral argument.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, column))
             for column in zip(*b)] for row in a]


def outer(v):
    return [[x * y for y in v] for x in v]


def rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    lead = 0
    for column in range(len(a[0])):
        pivot = next((i for i in range(lead, len(a)) if a[i][column]), None)
        if pivot is None:
            continue
        a[lead], a[pivot] = a[pivot], a[lead]
        divisor = a[lead][column]
        a[lead] = [x / divisor for x in a[lead]]
        for i in range(len(a)):
            if i != lead:
                multiple = a[i][column]
                a[i] = [x - multiple * y for x, y in zip(a[i], a[lead])]
        lead += 1
        if lead == len(a):
            break
    return lead


def polynomial_product(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for value in range(total + 1):
            for rest in compositions(total - value, parts - 1):
                yield (value,) + rest


def check_row_profiles():
    profiles = []
    tested = 0
    for sizes in combinations_with_replacement(range(4, 11), 11):
        tested += 1
        if sizes[-1] >= 9 and sum(sizes) <= 50 and sum(sizes) % 2 == 0:
            profiles.append(list(sizes))
    require(profiles == [[4] * 10 + [10], [4] * 9 + [5, 9]],
            "the two low-codegree row profiles")
    return {"size_multisets_tested": tested, "surviving_profiles": profiles}


def check_star_margins():
    accepted = rejected = checked_entries = 0
    for omitted in range(10):
        for five in combinations(range(10), 5):
            q = [int(i in five) for i in range(10)]
            z = [int(i != omitted) for i in range(10)]
            # The nine four-rows contribute zero to t, the size-nine row
            # contributes five, and the size-five row contributes one.
            margin = [6 - 5 * z[i] - q[i] for i in range(10)]
            require(sum(margin) == 10, "total weighted defect degree")
            if omitted not in five:
                require(margin[omitted] == 6 > sum(margin) // 2,
                        "omitted point excluded from five-row is impossible")
                rejected += 1
                continue
            r = [q[i] - int(i == omitted) for i in range(10)]
            f = [[int(i == omitted) * (1 - q[j])
                  + int(j == omitted) * (1 - q[i])
                  for j in range(10)] for i in range(10)]
            require(all(f[i][i] == 0 for i in range(10)), "defect has no loops")
            require(list(map(sum, f)) == margin, "star realizes all margins")
            zz, qq, rr = outer(z), outer(q), outer(r)
            for i in range(10):
                for j in range(10):
                    require(zz[i][j] + qq[i][j] + f[i][j] == 1 + rr[i][j],
                            "size-nine exact rank-one cancellation")
                    checked_entries += 1
            accepted += 1
    require((accepted, rejected) == (1260, 1260), "complete five-row domain")
    # Size ten has t_i=6 and consequently every nonnegative defect is zero.
    require([6 - (10 - 4)] * 10 == [0] * 10, "size-ten margins")
    return {"valid_star_configurations": accepted,
            "impossible_omitted_point_configurations": rejected,
            "star_identity_entries": checked_entries}


def check_trace_algebra():
    polynomial = polynomial_product([-1, 1], polynomial_product([2, 1], [2, 1]))
    require(polynomial == [-4, 0, 3, 1], "trace polynomial expansion")
    # Moments on the orthogonal complement after removing eigenvalue 3.
    moments = [9, -3, 21, -27]
    require(sum(c * m for c, m in zip(polynomial, moments)) == 0,
            "exact nonprincipal trace identity")
    for k in range(5):
        require(k <= 1 + k * (k - 1) // 2, "clique incidence inequality")
    for k in range(4):
        require(k == 1 + k * (k - 1) // 2 - int(k == 0) - int(k == 3),
                "triangle incidence identity")
    return {"trace_polynomial_low_to_high": polynomial,
            "nonprincipal_moments_order_zero_to_three": moments}


def check_gram_rigidity():
    # An explicit classical control: points are the ten weight-two masks
    # on five symbols, adjacency means disjoint support. All subsets are
    # inspected, not a list of purported independent sets supplied by an author.
    labels = [x for x in range(32) if x.bit_count() == 2]
    p = [[int(i != j and not (a & b)) for j, b in enumerate(labels)]
         for i, a in enumerate(labels)]
    pp = multiply(p, p)
    ppp = multiply(pp, p)
    require(list(map(sum, p)) == [3] * 10, "control is cubic")
    require(pp == [[2 * int(i == j) + 1 - p[i][j] for j in range(10)]
                   for i in range(10)], "control Moore relation")
    require(sum(pp[i][i] for i in range(10)) == 30 and
            sum(ppp[i][i] for i in range(10)) == 0, "control trace moments")
    k = [[2 * int(i == j) + 2 - 2 * p[i][j] for j in range(10)]
         for i in range(10)]
    require(k == [[4 * int(i == j) + 3 - 3 * p[i][j] - pp[i][j]
                   for j in range(10)] for i in range(10)], "two K formulas")
    sets = []
    histogram = Counter()
    for mask in range(1 << 10):
        s = [i for i in range(10) if mask >> i & 1]
        if all(not p[i][j] for i, j in combinations(s, 2)):
            histogram[len(s)] += 1
            if len(s) == 4:
                sets.append(s)
    require(max(histogram) == 4 and len(sets) == 5, "independence domain")
    for i in range(10):
        nonneighbors = [j for j in range(10) if j != i and not p[i][j]]
        require(len(nonneighbors) == 6 and
                all(sum(p[j][x] for x in nonneighbors) == 2 for j in nonneighbors),
                "six-point cycle degrees")
        triples = [s for s in combinations(nonneighbors, 3)
                   if all(not p[a][b] for a, b in combinations(s, 2))]
        require(len(triples) == 2 and set(triples[0]).isdisjoint(triples[1]),
                "alternating independent triples partition the six points")
        require(sum(i in s for s in sets) == 2, "two four-sets at each point")
    nonedges = [(i, j) for i, j in combinations(range(10), 2) if not p[i][j]]
    require(len(nonedges) == 30, "thirty nonedges")
    for i, j in nonedges:
        require(sum(i in s and j in s for s in sets) == 1,
                "every nonedge identifies one four-set")
    row_products = [outer([int(i in s) for i in range(10)]) for s in sets]
    require(k == [[2 * sum(row[i][j] for row in row_products)
                   for j in range(10)] for i in range(10)], "twice-five-sets Gram")
    require(sum(k[i][i] for i in range(10)) == 40 and sum(map(sum, k)) == 160,
            "nonnegative-factor equality budgets")
    require(rank(k) == rank([[int(i in s) for i in range(10)] for s in sets]) == 5,
            "exact rational ranks")
    solutions = []
    tested = 0
    for multiplicities in compositions(10, 5):
        tested += 1
        candidate = [[sum(m * row[i][j] for m, row in zip(multiplicities, row_products))
                      for j in range(10)] for i in range(10)]
        if candidate == k:
            solutions.append(list(multiplicities))
    require(tested == 1001 and solutions == [[2] * 5], "binary-factor uniqueness")
    # Remove any one of the ten rows for the synthetic r in the size-nine
    # case, then exhaust all ten choices for the one blue neighbor of b.
    pair_histogram = Counter()
    for synthetic in range(5):
        actual = [j for j in range(5) for _ in range(2 - int(j == synthetic))]
        for omitted_neighbor in range(10):
            adjacent = [t for t, value in enumerate(actual) if t != omitted_neighbor]
            counts = Counter(actual[t] for t in adjacent)
            pairs = sum(value * (value - 1) // 2 for value in counts.values())
            require(pairs >= 3, "at least three duplicated pairs adjacent to b")
            pair_histogram[pairs] += 1
    require(dict(pair_histogram) == {3: 40, 4: 10}, "all size-nine adjacency cases")
    return {"classical_control_point_labels_as_masks": labels,
            "independent_set_size_histogram": {str(a): b for a, b in sorted(histogram.items())},
            "independent_four_sets": sets, "unique_nonedge_four_set_checks": 30,
            "exact_Gram_rank": 5, "binary_multiplicity_vectors_tested": tested,
            "binary_multiplicity_solutions": solutions,
            "size_ten_forced_duplicate_pairs": 5,
            "size_nine_adjacent_duplicate_pair_histogram": {str(a): b for a, b in sorted(pair_histogram.items())}}


def build():
    return {"status": "PASS", "scope": "finite arithmetic controls for the written proof",
            "row_profiles": check_row_profiles(), "star_margins": check_star_margins(),
            "trace_algebra": check_trace_algebra(), "gram_rigidity": check_gram_rigidity()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("expected.json"))
    parser.add_argument("--emit", action="store_true", help="print complete regenerated data without comparison")
    args = parser.parse_args()
    record = build()
    data = json.dumps(record, sort_keys=True, indent=2) + "\n"
    if args.emit:
        print(data, end="")
        return
    require(json.loads(args.expected.read_text()) == record, "expected record mismatch")
    print(json.dumps({"status": "PASS", "valid_star_configurations": 1260,
                      "binary_multiplicity_vectors_tested": 1001,
                      "minimum_size_nine_adjacent_duplicate_pairs": 3,
                      "expected_sha256": hashlib.sha256(data.encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
