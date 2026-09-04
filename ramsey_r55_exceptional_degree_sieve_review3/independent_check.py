#!/usr/bin/env python3
"""Independent exact audit of the exceptional-degree count relaxation.

This checker imports no code from the reviewed artifact.  It regenerates the
hard-branch degree profiles by a weight-budget recursion, solves every integer
edge-count system with an exact branch-and-bound search, and only then compares
its classification with the published certificate.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import comb, prod
from pathlib import Path


DEGREES = tuple(range(18, 25))
EXCEPTIONAL = tuple(d for d in DEGREES if d != 21)
EXTREMA = {18: 85, 19: 92, 20: 100, 21: 107,
           22: 114, 23: 122, 24: 132}
WEIGHT = {d: 29 - (2 * (EXTREMA[d] + EXTREMA[42-d])
                    - 1722 + 3*d*(42-d)) for d in DEGREES}
EXPECTED_HEADER = (
    "counts_18_to_24\tM\tW\tsplit_count\tstatus\t"
    "edge_counts\thalf_counts\tmultipliers"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def local_cap(degree, edges):
    """Substitute directly into the neighborhood edge-count inequality."""
    return (edges - comb(42-degree, 2) + EXTREMA[degree]
            + EXTREMA[42-degree] - 14 - 21*degree)


def generate_profiles():
    """Generate profiles recursively, without the target's Cartesian product."""
    profiles = []

    def visit(position, budget, counts):
        if position == len(EXCEPTIONAL):
            exceptional_count = sum(counts.values())
            if exceptional_count > 43:
                return
            full = tuple(counts.get(d, 43-exceptional_count if d == 21 else 0)
                         for d in DEGREES)
            degree_sum = sum(d*n for d, n in zip(DEGREES, full))
            weight = 39-budget
            if (weight in range(3, 40, 6) and degree_sum % 2 == 0
                    and 445 <= degree_sum//2 <= 451):
                profiles.append(full)
            return

        degree = EXCEPTIONAL[position]
        for count in range(budget // WEIGHT[degree] + 1):
            counts[degree] = count
            visit(position+1, budget-count*WEIGHT[degree], counts)
        del counts[degree]

    visit(0, 39, {})
    require(len(profiles) == len(set(profiles)), "duplicate generated profile")
    return tuple(sorted(profiles))


def split_count(counts, M):
    """Count the exceptional-degree allocations to one 21-vertex anchor side."""
    active = [(d, counts[d-18]) for d in EXCEPTIONAL if counts[d-18]]
    answer = 0
    for allocation in product(*(range(n+1) for _, n in active)):
        if sum((d-21)*a for (d, _), a in zip(active, allocation)) != M-220:
            continue
        on_first = sum(allocation)
        on_second = sum(n-a for (_, n), a in zip(active, allocation))
        require(on_first <= 21 and on_second <= 21,
                ("exceptional allocation does not fit anchor sides", counts))
        answer += 1
    return answer


def edge_box(counts):
    ns = dict(zip(DEGREES, counts))
    active = tuple(d for d in EXCEPTIONAL if ns[d])
    edge_types = []
    capacities = []
    for a, b in combinations_with_replacement(active, 2):
        capacity = comb(ns[a], 2) if a == b else ns[a]*ns[b]
        if capacity:
            edge_types.append((a, b))
            capacities.append(capacity)
    return ns, active, tuple(edge_types), tuple(capacities)


def direct_margins(counts, values):
    """Evaluate every class inequality literally, including degree 21."""
    ns, active, edge_types, capacities = edge_box(counts)
    require(len(values) == len(edge_types), ("edge-vector length", counts, values))
    require(all(0 <= q <= cap for q, cap in zip(values, capacities)),
            ("edge-count outside simple-graph capacity", counts, values))
    edges = sum(d*n for d, n in ns.items()) // 2
    incidence = {d: 0 for d in active}
    weighted_neighbors = {d: 0 for d in active}
    for (a, b), q in zip(edge_types, values):
        incidence[a] += q
        incidence[b] += q
        weighted_neighbors[a] += (b-21)*q
        weighted_neighbors[b] += (a-21)*q

    margins = [ns[d]*local_cap(d, edges)-weighted_neighbors[d]
               for d in active]
    central_weight = sum((d-21)*(ns[d]*d-incidence[d]) for d in active)
    margins.append(ns[21]*local_cap(21, edges)-central_weight)
    return tuple(margins)


def solve_profile(counts):
    """Exact integer feasibility via independently ordered interval search."""
    ns, active, edge_types, capacities = edge_box(counts)
    edges = sum(d*n for d, n in ns.items()) // 2
    row_caps = tuple(ns[d]*local_cap(d, edges) for d in active)
    lower_total = (sum((d-21)*ns[d]*d for d in active)
                   - ns[21]*local_cap(21, edges))

    columns = []
    for original, ((a, b), capacity) in enumerate(zip(edge_types, capacities)):
        coeff = tuple((int(d == a)*(b-21) + int(d == b)*(a-21))
                      for d in active)
        columns.append((original, capacity, coeff, sum(coeff)))

    # This order is deliberately different from the artifact's lexicographic
    # edge order: high-impact, small-domain variables branch first.
    columns.sort(key=lambda col: (-max(abs(c) for c in col[2]),
                                  col[1], -abs(col[3]), col[0]))
    column_count = len(columns)
    row_count = len(active)
    suffix_min = [[0]*row_count for _ in range(column_count+1)]
    suffix_total_max = [0]*(column_count+1)
    for k in range(column_count-1, -1, -1):
        _, capacity, coeff, total_coeff = columns[k]
        for row in range(row_count):
            suffix_min[k][row] = (suffix_min[k+1][row]
                                  + min(0, capacity*coeff[row]))
        suffix_total_max[k] = (suffix_total_max[k+1]
                               + max(0, capacity*total_coeff))

    nodes = 0
    assignments = [0]*column_count

    def visit(k, row_sums, total_sum):
        nonlocal nodes
        nodes += 1
        if any(row_sums[r]+suffix_min[k][r] > row_caps[r]
               for r in range(row_count)):
            return None
        if total_sum+suffix_total_max[k] < lower_total:
            return None
        if k == column_count:
            return tuple(assignments)

        _, capacity, coeff, total_coeff = columns[k]
        domain = range(capacity, -1, -1) if total_coeff > 0 else range(capacity+1)
        for value in domain:
            assignments[k] = value
            result = visit(
                k+1,
                tuple(row_sums[r]+value*coeff[r] for r in range(row_count)),
                total_sum+value*total_coeff,
            )
            if result is not None:
                return result
        return None

    search_order_witness = visit(0, (0,)*row_count, 0)
    witness = None
    if search_order_witness is not None:
        ordered = [0]*column_count
        for entry, q in zip(columns, search_order_witness):
            ordered[entry[0]] = q
        witness = tuple(ordered)
        require(all(margin >= 0 for margin in direct_margins(counts, witness)),
                ("search returned invalid witness", counts, witness))
    return witness, nodes, prod(cap+1 for cap in capacities)


def parse_vector(field):
    return tuple(map(int, field.split(","))) if field != "-" else ()


def read_certificate(path):
    lines = path.read_text(encoding="ascii").splitlines()
    require(lines and lines[0] == EXPECTED_HEADER, "unexpected certificate header")
    rows = {}
    for line in lines[1:]:
        fields = line.split("\t")
        require(len(fields) == 8, ("certificate row width", line))
        counts = parse_vector(fields[0])
        require(counts not in rows, ("duplicate certificate profile", counts))
        rows[counts] = fields
    return rows


def check_published_obstruction(counts, fields):
    """Check the published auxiliary witness directly, not by search code."""
    ns, active, edge_types, capacities = edge_box(counts)
    edges = sum(d*n for d, n in ns.items()) // 2
    halves, multipliers = fields[6], fields[7]
    if halves != "-":
        vector = tuple(Fraction(x, 2) for x in parse_vector(halves))
        require(any(q.denominator == 2 for q in vector), "integral half witness")
        require(all(margin >= 0 for margin in direct_margins(counts, vector)),
                ("bad half-integral witness", counts))
        return "half"

    lam = parse_vector(multipliers)
    require(len(lam) == len(active) and all(x >= 0 for x in lam),
            ("bad multiplier dimensions", counts))
    rhs = sum(x*ns[d]*local_cap(d, edges) for d, x in zip(active, lam))
    lower = 0
    for (a, b), capacity in zip(edge_types, capacities):
        coefficient = (lam[active.index(a)]*(b-21)
                       + lam[active.index(b)]*(a-21))
        lower += capacity*min(0, coefficient)
    require(lower > rhs, ("invalid linear obstruction", counts, lower, rhs))
    return "linear"


def main():
    here = Path(__file__).resolve().parent
    certificate_path = here.parent/"ramsey_r55_exceptional_degree_sieve"/"PROFILES.tsv"
    published = read_certificate(certificate_path)
    profiles = generate_profiles()
    require(set(profiles) == set(published), "generated/certificate universes differ")
    require(WEIGHT == {18: 21, 19: 12, 20: 3, 21: 0,
                       22: 3, 23: 12, 24: 21}, "derived weights differ")

    global_hist = Counter()
    split_hist = Counter()
    raw_rejected_box = 0
    directly_checked_rejections = 0
    search_nodes = 0
    obstruction_kinds = Counter()
    for counts in profiles:
        degree_sum = sum(d*n for d, n in zip(DEGREES, counts))
        edges = degree_sum//2
        M = edges-231
        W = sum(WEIGHT[d]*n for d, n in zip(DEGREES, counts))
        splits = split_count(counts, M)

        # Verify the q-independent total-margin identity before searching.
        ns = dict(zip(DEGREES, counts))
        P = sum((d-21)*ns[d]*d for d in EXCEPTIONAL)
        margin_total = (sum(ns[d]*local_cap(d, edges) for d in EXCEPTIONAL)
                        + ns[21]*local_cap(21, edges) - P)
        require(margin_total == (43-W)//2 and (43-W) % 2 == 0,
                ("paired-excess identity", counts, margin_total, W))

        witness, nodes, box_size = solve_profile(counts)
        search_nodes += nodes
        status = "feasible" if witness is not None else "excluded"
        global_hist[M, status] += 1
        split_hist[M, status] += splits

        fields = published[counts]
        require((int(fields[1]), int(fields[2]), int(fields[3]), fields[4])
                == (M, W, splits, status),
                ("independent classification mismatch", counts, status, fields))
        if status == "feasible":
            target_witness = parse_vector(fields[5])
            require(all(x >= 0 for x in direct_margins(counts, target_witness)),
                    ("bad published integer witness", counts))
            require(fields[6] == fields[7] == "-", "extras on feasible row")
        else:
            require(fields[5] == "-", "integer witness on excluded row")
            raw_rejected_box += box_size
            _, _, _, capacities = edge_box(counts)
            for candidate in product(*(range(cap+1) for cap in capacities)):
                directly_checked_rejections += 1
                require(not all(x >= 0 for x in direct_margins(counts, candidate)),
                        ("direct enumeration found a witness", counts, candidate))
            obstruction_kinds[check_published_obstruction(counts, fields)] += 1

    expected_global = {
        214: (1, 0), 215: (3, 0), 216: (7, 0), 217: (13, 1),
        218: (21, 0), 219: (20, 7), 220: (23, 8),
    }
    expected_splits = {
        214: (1, 0), 215: (5, 0), 216: (17, 0), 217: (39, 1),
        218: (69, 0), 219: (85, 10), 220: (105, 17),
    }
    for M in range(214, 221):
        require((global_hist[M, "feasible"], global_hist[M, "excluded"])
                == expected_global[M], ("global histogram", M, global_hist))
        require((split_hist[M, "feasible"], split_hist[M, "excluded"])
                == expected_splits[M], ("split histogram", M, split_hist))
    require(raw_rejected_box == 819, ("rejected box total", raw_rejected_box))
    require(directly_checked_rejections == raw_rejected_box,
            ("direct rejection count", directly_checked_rejections))
    require(obstruction_kinds == {"linear": 13, "half": 3}, obstruction_kinds)

    print("PASS derived degree weights: 21,12,3,0,3,12,21")
    print("PASS independent hard-branch profile recursion: 104 profiles")
    print("PASS independent anchor split census: 349 splits")
    print("PASS exact independent integer search: 88 feasible, 16 excluded")
    print("PASS direct enumeration of excluded boxes: all 819 integer tuples fail")
    print("PASS published auxiliary certificates: 13 linear, 3 half-integral")
    print("PASS retained profiles by M=214..220: 1,3,7,13,21,20,23")
    print("PASS retained splits by M=214..220: 1,5,17,39,69,85,105")
    print("PASS excluded splits by M=214..220: 0,0,0,1,0,10,17")
    print(f"INFO exact branch-and-bound nodes visited: {search_nodes}")
    print("SCOPE necessary aggregate edge-count relaxation; no survivor is a graph")


if __name__ == "__main__":
    main()
