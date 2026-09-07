"""Exact cut-capacity arithmetic and a complete F27 low-rank family map."""
import json
from itertools import combinations
from math import prod

PAIRS = list(combinations(range(43), 2))
A = list(range(7, 27))
B = [v for v in range(43) if v not in A]


def capacity(a, rank):
    if not 1 <= a <= 21 or rank < 0:
        raise ValueError("invalid smaller side or rank")
    slots = 1 << rank
    if a <= 9:
        return slots - 1
    if a <= 18:
        return 2 * (slots - 1)
    if a == 19:
        return 2 * slots
    return 5 * slots - 1


def lower_bound(a):
    return next(r for r in range(a + 1) if capacity(a, r) >= a)


def matrix_count(m, n, k):
    if not 0 <= k <= min(m, n):
        return 0
    top = prod(((1 << m) - (1 << i)) * ((1 << n) - (1 << i))
               for i in range(k))
    bottom = prod((1 << k) - (1 << i) for i in range(k))
    result, remainder = divmod(top, bottom)
    if remainder:
        raise RuntimeError("nonintegral matrix count")
    return result


def pins():
    result = {}
    for start in (2, 7, 12, 17, 22):
        for u, v in combinations(range(start, start + 5), 2):
            result[u, v] = int((v - u) in (1, 4))
    result[0, 1] = 1
    for u in (0, 1):
        for v in range(2, 7):
            result[u, v] = 1
    return result


def internal_free():
    fixed = pins()
    return [e for e in PAIRS if e not in fixed and ((e[0] in A) == (e[1] in A))]


def family(u, v, internal, color="red"):
    """U has 20 rows of two bits; V has 23 columns of two bits. M = U V."""
    if (len(u) != 20 or len(v) != 23 or
            any(type(t) is not int or not 0 <= t < 4 for t in list(u) + list(v)) or
            type(internal) is not int or not 0 <= internal < (1 << 382) or
            color not in ("red", "blue")):
        raise ValueError("invalid complete-family parameters")
    edges = pins()
    for i, x in enumerate(A):
        for j, y in enumerate(B):
            bit = (u[i] & v[j]).bit_count() % 2
            edges[tuple(sorted((x, y)))] = bit ^ (color == "blue")
    for i, pair in enumerate(internal_free()):
        edges[pair] = (internal >> i) & 1
    if set(edges) != set(PAIRS):
        raise RuntimeError("physical pair coverage failed")
    packed = sum(edges[e] << i for i, e in enumerate(PAIRS))
    return {"n": 43, "red_hex": format(packed, "0226x"),
            "cut": A, "rank_color": color}


def report():
    cross = [e for e in PAIRS if (e[0] in A) != (e[1] in A)]
    counts = [matrix_count(20, 23, k) for k in range(3)]
    total = sum(counts)
    return {
        "status": "COMPLETE_LOW_CUT_RANK_FAMILY_EXCLUDED",
        "n": 43,
        "profile": [{"smaller_side": a, "rank_lower_bound": lower_bound(a),
                     "capacity_at_rank_2": capacity(a, 2)} for a in range(1, 22)],
        "rank_width_lower_bound_each_color": 3,
        "linear_rank_width_lower_bound_each_color": 4,
        "F27": {"cut": A, "other_side": B, "pins": len(pins()),
                "cross_pairs": len(cross),
                "cross_pins": sum(e in pins() for e in cross),
                "other_free_pairs": len(internal_free()),
                "distinct_cross_matrices_by_rank": counts,
                "distinct_cross_matrices_rank_at_most_2": total,
                "distinct_graphs_per_color": total * (1 << 382),
                "factor_parameter_bits": 86,
                "internal_parameter_bits": 382,
                "color_union_count_claimed": False},
        "trust_boundary": "Analytic proof with imported R(4,5)<=25; not a formal proof or target graph."
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
