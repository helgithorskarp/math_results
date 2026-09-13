#!/usr/bin/env python3
"""Independent exact checker for the split-barrier r=30 proof review.

Standard-library Python only.  This checks the finite arithmetic and the two
integer-partition joins in REVIEW.md.  It does not formalize the cited graph
theorems or the prose bridges from those theorems to these finite statements.
"""

from fractions import Fraction as Q
from functools import lru_cache
from math import comb


TARGET = 9555


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def ceil_q(x):
    return -((-x.numerator) // x.denominator)


def falling(n, k):
    ans = 1
    for i in range(k):
        ans *= n - i
    return ans


def hill(n):
    return ((n // 2) * ((n - 1) // 2) *
            ((n - 2) // 2) * ((n - 3) // 2) // 4)


def sampled(n, m, q):
    """Integer-aware induced-q-subgraph form of the BK affine inequality."""
    require(4 <= q <= n, "invalid sample order")
    local_constant = (203 * (q - 2)) // 9
    inside = Q(5 * m * q * (q - 1), n * (n - 1)) - local_constant
    return inside * Q(falling(n, 4), falling(q, 4))


def best_sample(n, m):
    return max((sampled(n, m, q), q) for q in range(4, n + 1))


CRK = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0,
       5: 1, 6: 3, 7: 9, 8: 18, 9: 36, 10: 60, 11: 100, 12: 150}


def cr_complete_lower(n):
    """Counting recursion, seeded only by cr(K_12)=150 and smaller values."""
    if n not in CRK:
        CRK[n] = -(-n * cr_complete_lower(n - 1) // (n - 4))
    return CRK[n]


def gks_floor(r, n):
    twice = (r - 1) * n + (n - r) * (2 * r - n) - 2
    return -(-twice // 2)


def join_floor(r, n):
    """Minimum of Cao--Mehat's strengthened terminal-join expression."""
    choices = []
    for k in range(4, r):
        for a in range(2 * k - 1, n - r + k + 1):
            value = (Q(a * k, 2) + Q((n - a) * (r - k - 1), 2)
                     + a * (n - a))
            choices.append((value, a, k))
    require(choices, "empty join domain")
    return min(choices)


@lru_cache(maxsize=None)
def recursive_min_cost(rem, max_part, odd_needed, free):
    """Minimum forced deficit over nonincreasing integer partitions."""
    if rem == 0:
        return 0 if odd_needed == 0 else 10**9
    best = 10**9
    for c in range(min(rem, max_part), 0, -1):
        cost = c * max(0, free - c)
        nxt = recursive_min_cost(rem - c, c, max(0, odd_needed - c % 2), free)
        best = min(best, cost + nxt)
    return best


def forward_min_cost(total, odd_required, free):
    """Independent unbounded-knapsack computation of the same minimum."""
    inf = 10**9
    dp = [[inf] * (odd_required + 1) for _ in range(total + 1)]
    dp[0][0] = 0
    for c in range(1, total + 1):
        price = c * max(0, free - c)
        for used in range(c, total + 1):
            for old_odd in range(odd_required + 1):
                prior = dp[used - c][old_odd]
                if prior == inf:
                    continue
                new_odd = min(odd_required, old_odd + c % 2)
                dp[used][new_odd] = min(dp[used][new_odd], prior + price)
    return dp[total][odd_required]


def barrier_cost_table(n, first_s, odd_offset, free_constant):
    """Return (s, minimum deficit) for every cardinality-feasible barrier."""
    out = []
    last_s = (n + odd_offset) // 2
    for s in range(first_s, last_s + 1):
        total = n - s
        odd_required = s - odd_offset
        free = free_constant - s
        a = recursive_min_cost(total, total, odd_required, free)
        b = forward_min_cost(total, odd_required, free)
        require(a == b, "partition algorithms disagree at s=%d" % s)
        out.append((s, a))
    return out


def partitions_with_cost(total, odd_required, free, cap):
    out = []

    def visit(rem, largest, odd, cost, parts):
        if cost > cap:
            return
        if rem == 0:
            if odd >= odd_required:
                out.append(tuple(parts))
            return
        for c in range(min(rem, largest), 0, -1):
            visit(rem - c, c, odd + c % 2,
                  cost + c * max(0, free - c), parts + [c])

    visit(total, total, 0, 0, [])
    return out


def fmt(x):
    return str(x.numerator) if x.denominator == 1 else str(x)


def main():
    require(hill(30) == TARGET, "wrong Hill target")
    require(cr_complete_lower(28) == 6250, "wrong K28 counting bound")
    require(cr_complete_lower(29) == 7250, "wrong K29 counting bound")

    print("Albertson r=30 split-barrier independent review")
    print("Z(30) =", TARGET)
    print("crK counting bounds: K28=%d K29=%d" %
          (cr_complete_lower(28), cr_complete_lower(29)))

    print("\nORDER REDUCTION")
    for n in (35, 36):
        m = gks_floor(30, n)
        value, q = best_sample(n, m)
        require(value >= TARGET, "small order not closed")
        print("n=%d m>=%d q=%d B-Z=%s" % (n, m, q, fmt(value - TARGET)))

    for n in range(54, 59):
        value, a, k = join_floor(30, n)
        m = ceil_q(value)
        sampled_value, q = best_sample(n, m)
        require(sampled_value >= TARGET, "join order not closed")
        print("n=%d join>=%s ceil=%d at (a,k)=(%d,%d); q=%d B-Z=%s" %
              (n, fmt(value), m, a, k, q, fmt(sampled_value - TARGET)))

    for n in (59, 60):
        value, a, k = join_floor(30, n)
        require(ceil_q(value) == (899 if n == 59 else 915), "join endpoint")
        cross, q = best_sample(n, ceil_q(value))
        require(cross >= TARGET, "disconnected endpoint not closed")
        print("disconnected n=%d: join>=%s ceil=%d at (a,k)=(%d,%d); "
              "q=%d B-Z=%s" %
              (n, fmt(value), ceil_q(value), a, k, q, fmt(cross - TARGET)))

    for n, expected in ((59, 891), (60, 903)):
        lo = 15 * n
        open_rows = []
        for m in range(lo, lo + 40):
            value, q = best_sample(n, m)
            if value < TARGET:
                open_rows.append(m)
        require(open_rows == list(range(lo, expected + 1)), "sampling cutoff")
        nxt, q = best_sample(n, expected + 1)
        print("n=%d direct-sampling rows %d..%d; m=%d closes with q=%d, B-Z=%s" %
              (n, lo, expected, expected + 1, q, fmt(nxt - TARGET)))

    large = []
    for n in range(61, 85):
        value, q = best_sample(n, 15 * n)
        require(value >= TARGET, "large finite order not closed")
        large.append((n, q, value - TARGET))
    smallest = min(large, key=lambda row: row[2])
    print("n=61..84: all 24 minimum-edge rows close; smallest margin %s at n=%d q=%d" %
          (fmt(smallest[2]), smallest[0], smallest[1]))

    print("\nBARRIER PARTITIONS")
    odd = barrier_cost_table(59, 3, 1, 29)
    even = barrier_cost_table(60, 6, 4, 30)
    odd_live = [s for s, cost in odd if cost <= 12]
    even_live = [s for s, cost in even if cost <= 6]
    require(odd_live == [3, 28, 29, 30], "order-59 barrier sizes")
    require(even_live == [6, 29, 30, 31, 32], "order-60 barrier sizes")
    require(min(cost for s, cost in odd if 4 <= s <= 27) == 23,
            "order-59 middle gap")
    require(min(cost for s, cost in even if 7 <= s <= 28) == 20,
            "order-60 middle gap")
    print("n=59 cap12 live s=%s; min excluded-middle cost=23" % odd_live)
    print("n=60 cap6  live s=%s; min excluded-middle cost=20" % even_live)

    p59 = partitions_with_cost(56, 2, 26, 12)
    p60 = partitions_with_cost(54, 2, 24, 6)
    require(p59 == [(29, 27)], "order-59 small partition")
    require(p60 == [(29, 25), (27, 27)], "order-60 small partitions")
    print("n=59 s=3 partitions:", p59)
    print("n=60 s=6 partitions:", p60)

    print("\nTERMINAL SPLIT BOUNDS")
    # No-triangle order-59 case: K28 plus a 31-vertex graph with >=417 edges.
    split59tf = Q(cr_complete_lower(28)) + sampled(31, 417, 12)
    # Triangle/barrier order-59, s=30: K29 plus >=415 edges on S.
    split59s30 = Q(cr_complete_lower(29)) + sampled(30, 415, 12)
    # Order-60 barrier sizes 30,31,32, using only the worst edge bounds.
    split60s30 = sampled(30, 425, 11) + sampled(30, 422, 11)
    split60s31 = sampled(29, 403, 11) + sampled(31, 430, 12)
    split60s32 = Q(cr_complete_lower(28)) + sampled(32, 435, 13)
    splits = [("n59 triangle-free", split59tf),
              ("n59 s=30", split59s30),
              ("n60 s=30", split60s30),
              ("n60 s=31", split60s31),
              ("n60 s=32", split60s32)]
    for label, value in splits:
        require(value >= TARGET, label + " not closed")
        print("%s: lower=%s margin=%s" % (label, fmt(value), fmt(value - TARGET)))

    # At n=59,s=3, G contains K_{29,27}; count induced K_{6,27}'s.
    k629 = Q(29 * 28, 30) * (6 * 13 * 13)
    require(k629 > TARGET, "K29,27 bound")
    print("n59 s=3: cr(K29,27)>=%s > Z" % fmt(k629))

    # Order 60: if no two disjoint triangles, H-T has at least 783 edges.
    degree_sum = -(-(4 * 783) // 57)
    require(degree_sum == 55, "degree-sum threshold")
    clique_pair = min(cr_complete_lower(a) + cr_complete_lower(55 - a)
                      for a in range(25, 31) if 25 <= 55 - a <= 30)
    require(clique_pair == 11607 and clique_pair > TARGET,
            "two-disjoint-triangle split")
    print("n60 no-disjoint-triangles: neighbor-clique sum>=55, cr lower=%d" %
          clique_pair)

    # Rabern's radical term equals 18 at n=60, without floating point.
    require((4 * 17 - 15) ** 2 < 48 * 60 + 73 <= (4 * 18 - 15) ** 2,
            "Rabern ceiling")
    print("n60 regular row: Rabern radical ceiling=18")
    print("\nPASS: every exact finite check agrees with REVIEW.md")


if __name__ == "__main__":
    main()
