#!/usr/bin/env python3
"""Exact arithmetic for the conditional r=30 transfer; standard library only.

This checks finite arithmetic, not the imported graph theorems or prose proof.
All graph orders and edge totals in the sampling recurrence are unrestricted.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def up(a, b=1):
    require(b > 0, "positive denominator required")
    return -((-a) // b)


def z(n):
    return (n // 2) * ((n - 1) // 2) * ((n - 2) // 2) * ((n - 3) // 2) // 4


def base(n):
    return [max(0, m - 3 * (n - 2), up(45*m - 203*(n-2), 9))
            for m in range(comb(n, 2) + 1)]


def hull(values):
    """Greatest convex minorant, retaining just its slope-change vertices."""
    h = []
    for x, y in enumerate(values):
        while len(h) >= 2:
            a, b = h[-2:]
            if (values[b]-values[a])*(x-b) < (y-values[b])*(b-a):
                break
            h.pop()
        h.append(x)
    return h


def tables(max_order=61):
    """Induction in order, with an exact integer version of sampled Jensen."""
    rows, hulls = {}, {}
    for n in range(4, max_order+1):
        values = base(n)
        nn = n*(n-1)
        for s in range(4, n):
            source, h = rows[s], hulls[s]
            ss = s*(s-1)
            j = 0
            for m in range(len(values)):
                mean_numerator = m*ss
                while j+2 < len(h) and h[j+1]*nn < mean_numerator:
                    j += 1
                a, b = h[j:j+2]
                require(a*nn <= mean_numerator <= b*nn, "bad hull interval")
                numerator = ((b-a)*nn*source[a]
                             + (source[b]-source[a])*(mean_numerator-a*nn))
                candidate = up(numerator*(n-2)*(n-3),
                               (b-a)*ss*(s-2)*(s-3))
                values[m] = max(values[m], candidate)
        rows[n], hulls[n] = values, hull(values)
    return rows, hulls


def sampled_affine(n, m, s):
    return (Q(5*m*(n-2)*(n-3), (s-2)*(s-3))
            - Q(203*n*(n-1)*(n-2)*(n-3), 9*s*(s-1)*(s-3)))


def marked_join_floor(r, n):
    """Every actual marked terminal join part occurs in this relaxation."""
    choices = []
    for k in range(4, r):
        for a in range(2*k-1, n-r+k+1):
            b = n-a
            twice = a*(k-1) + 2*k-6 + b*(r-k-1) + 2*a*b
            choices.append((up(twice, 2), k, a))
    require(bool(choices), "empty marked-part domain")
    return min(choices)


def small_hull_check(rows, hulls):
    """Definition-level two-support LP check, without using hull construction."""
    count = 0
    for n in range(4, 11):
        values, h = rows[n], hulls[n]
        for numerator in range(2*(len(values)-1)+1):
            x = Q(numerator, 2)
            candidates = []
            if x.denominator == 1:
                candidates.append(Q(values[x.numerator]))
            for a in range(len(values)):
                for b in range(a+1, len(values)):
                    if a <= x <= b:
                        candidates.append(((b-x)*values[a]+(x-a)*values[b])/(b-a))
            expected = min(candidates)
            actual = next(((b-x)*values[a]+(x-a)*values[b])/(b-a)
                          for a, b in zip(h, h[1:]) if a <= x <= b)
            require(actual == expected, "convex-minorant LP disagreement")
            count += 1
    return count


def structural_arithmetic():
    """Finite checks at D=28; the proof in PROOF.md handles every D>=27."""
    records = []
    for A in (0, 2, 4, 6):
        survivors = []
        for s in range(3, 31):
            lower_order = max(1, 29-A-s)
            lower_odd = lower_order if lower_order % 2 else lower_order+1
            if (s-1)*lower_odd > 59-s:
                continue
            twice_cap = 2*comb(61-2*s, 2) + 28*(2*s-59)+A
            if twice_cap < 0:
                continue
            survivors.append(s)
        require(survivors == [3, 30], "unexpected Tutte cardinality")
        records.append({"deficit": A, "barrier_sizes_after_two_filters": survivors,
                        "small_barrier_coloring_cap": 59-2*(28-A-3)})
    # At S=30, X=29, deleting a cross triangle leaves a 28-by-28 graph.
    hall = [[q, q*(28-q)] for q in range(2, 9)]
    require(min(v for _, v in hall) > 34, "Hall weight budget not contradicted")
    require(2*28-18 > 29 and 27 > 18 and 27 > 6, "triangle/Hall endpoint")
    return {"D28_barriers": records, "Hall_lower_weights": hall,
            "Hall_total_weight_cap": 34, "edge_endpoint_weight_cap": 18}


def result():
    rows, hulls = tables()
    for n, values in rows.items():
        require(values[-1] <= z(n), "complete-graph drawing control")
        require(all(a <= b for a, b in zip(values, values[1:])), "nonmonotone row")
        require(all(x == 0 for x in values[:3*n-5]), "planar edge control")
    controls = small_hull_check(rows, hulls)
    dispatch = []
    for n in range(35, 59):
        gallai = up(29*n+(n-30)*(60-n)-2, 2)
        join, k, a = marked_join_floor(30, n)
        floor = max(15*n, gallai, join)
        require(rows[n][floor] >= 9555, "unclosed small order")
        dispatch.append({"n": n, "edge_floor": floor, "crossing_floor": rows[n][floor],
                         "gallai_floor": gallai, "join_floor": join,
                         "minimizing_relaxed_mark": [k, a]})
    frontier = []
    for n in (59, 60, 61):
        values = rows[n]
        ceiling = max(m for m, value in enumerate(values) if value < 9555)
        lo = 15*n
        frontier.append({"n": n, "edge_floor": lo, "sampling_ceiling": ceiling,
                         "floor_crossing_bound": values[lo],
                         "next_edge_crossing_bound": values[ceiling+1]})
    require([r["sampling_ceiling"] for r in frontier] == [888, 900, 912], "frontier")
    odd = [[m, rows[59][m], 2*m-1770] for m in range(885, 889)]
    join59, k, a = marked_join_floor(30, 59)
    require(join59 == 896 and rows[59][join59] >= 9555, "complement connectivity")
    large = []
    for n in range(62, 78):
        value, s = max((sampled_affine(n, 15*n, s), s) for s in range(4, n+1))
        require(value >= 9555, "unclosed intermediate order")
        large.append({"n": n, "sample_order": s,
                      "bound_numerator": value.numerator, "bound_denominator": value.denominator})
    tail = Q(1500*15**3*78, 41209)
    require(tail > 9555 and Q(15) >= Q(677, 100), "crossing-lemma tail")
    # Rabern's radical ceiling is 18 at n=60, checked without a square root.
    require((4*17-15)**2 < 48*60+73 <= (4*18-15)**2, "Rabern ceiling")
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {"status": "R30_HIGH_MINIMUM_DEGREE_EXCLUSION_ARITHMETIC_PASS",
            "class_hypothesis": "30-critical G with minimum degree at least 30",
            "full_r30_corollary_import": "Cao-Mehat degree-gain lemma; R1 source-published audit, REVIEW.md Section 1",
            "Z30": 9555, "n35_to_58": dispatch, "n59_to_61": frontier,
            "n59_survivors_m_crossing_floor_deficit": odd,
            "disconnected_n59": {"edge_floor": join59, "crossing_floor": rows[59][join59]},
            "n62_to_77": large,
            "n_ge_78_tail": [tail.numerator, tail.denominator],
            "n60_Rabern_ceiling": 18,
            "structural": structural_arithmetic(),
            "table_entries": sum(map(len, rows.values())),
            "table_sha256": sha256(encoded).hexdigest(),
            "small_hull_LP_comparisons": controls}


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
