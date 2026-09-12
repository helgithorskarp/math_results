#!/usr/bin/env python3
"""Exact finite controls for proof.md; not a proof by enumeration.

Python 3.11+, standard library only. Vertices are zero-based and graphs are
tuples of open-neighborhood integer bitmasks. Coloring is computed by a
general independent-set partition DP, without using the five-cycle formula.
"""
from functools import lru_cache
from itertools import combinations, permutations
import json
from pathlib import Path


def graph(n, edges):
    a = [0] * n
    seen = set()
    for u, v in edges:
        if not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError("invalid edge")
        e = tuple(sorted((u, v)))
        if e in seen:
            raise ValueError("duplicate edge")
        seen.add(e)
        a[u] |= 1 << v
        a[v] |= 1 << u
    return tuple(a)


def edges(a):
    return [(u, v) for u, v in combinations(range(len(a)), 2) if a[u] >> v & 1]


def clique(n):
    return graph(n, combinations(range(n), 2))


def cycle(n):
    return graph(n, [(i, (i + 1) % n) for i in range(n)])


def substitute(base, pieces):
    assert len(base) == len(pieces)
    offsets = [0]
    for piece in pieces:
        assert piece
        offsets.append(offsets[-1] + len(piece))
    e = []
    for i, piece in enumerate(pieces):
        e.extend((u + offsets[i], v + offsets[i]) for u, v in edges(piece))
    for i, j in edges(base):
        e.extend((u, v) for u in range(offsets[i], offsets[i + 1])
                 for v in range(offsets[j], offsets[j + 1]))
    return graph(offsets[-1], e)


def join(a, b):
    return substitute(clique(2), [a, b])


def isomorphism_codes(n, template_edges):
    original = {tuple(sorted(e)) for e in template_edges}
    pairs = list(combinations(range(n), 2))
    return {
        sum(1 << i for i, (u, v) in enumerate(pairs)
            if tuple(sorted((p[u], p[v]))) in original)
        for p in permutations(range(n))
    }


P4 = isomorphism_codes(4, [(0, 1), (1, 2), (2, 3)])
P5 = isomorphism_codes(5, [(0, 1), (1, 2), (2, 3), (3, 4)])
BULL = isomorphism_codes(5, [(0, 1), (1, 2), (0, 2), (0, 3), (1, 4)])
BANNER = isomorphism_codes(5, [(0, 1), (1, 2), (2, 3), (0, 3), (0, 4)])
COGEM = isomorphism_codes(5, [(0, 1), (1, 2), (2, 3)])


def code(a, vertices):
    return sum(1 << i for i, (u, v) in enumerate(combinations(vertices, 2))
               if a[u] >> v & 1)


def avoidance(a):
    result = dict.fromkeys(["P5", "bull", "banner", "co_gem"], True)
    forbidden = {"P5": P5, "bull": BULL, "banner": BANNER, "co_gem": COGEM}
    for s in combinations(range(len(a)), 5):
        c = code(a, s)
        for name, codes in forbidden.items():
            if c in codes:
                result[name] = False
    return result


def exact_invariants(a):
    n = len(a)
    full = (1 << n) - 1

    @lru_cache(None)
    def alpha(mask):
        if not mask:
            return 0
        bit = mask & -mask
        v = bit.bit_length() - 1
        return max(alpha(mask ^ bit), 1 + alpha((mask ^ bit) & ~a[v]))

    independent = [True] + [False] * full
    containing = [[] for _ in a]
    for mask in range(1, full + 1):
        bit = mask & -mask
        v = bit.bit_length() - 1
        independent[mask] = independent[mask ^ bit] and not (a[v] & mask)
        if independent[mask]:
            for u in range(n):
                if mask >> u & 1:
                    containing[u].append(mask)

    @lru_cache(None)
    def chromatic(mask):
        if not mask:
            return 0
        if independent[mask]:
            return 1
        v = max((u for u in range(n) if mask >> u & 1),
                key=lambda u: (a[u] & mask).bit_count())
        return 1 + min(chromatic(mask ^ s) for s in containing[v]
                       if s & mask == s)

    k = chromatic(full)
    deleted = [chromatic(full ^ (1 << v)) for v in range(n)]
    rho, path = -1, None
    for s in combinations(range(n), 4):
        if code(a, s) not in P4:
            continue
        anti = full
        for v in s:
            anti &= ~(a[v] | (1 << v))
        r = alpha(anti)
        if r > rho:
            rho, path = r, list(s)
    return {
        "vertices": n, "edges": len(edges(a)), "chi": k,
        "vertex_deletion_chromatic_numbers": deleted,
        "critical": all(x == k - 1 for x in deleted),
        "alpha": alpha(full), "rho4": rho, "rho4_path_vertex_set": path,
        "avoidance": avoidance(a),
    }


def sharpness_graph(a):
    g, t = clique(1), 1
    for _ in range(1, a):
        epsilon = int(t % 2 == 0)
        j = join(g, clique(1)) if epsilon else g
        r = t + epsilon
        g = substitute(cycle(5), [j] + [clique(r)] * 4)
        t = (5 * r + 1) // 2
    return g, t


def sharpness_parameters(a_max):
    rows = []
    n, k = 1, 1
    for a in range(1, a_max + 1):
        rows.append({"alpha": a, "vertices": n, "chi": k,
                     "forbidden_P4_plus_isolates": a - 1})
        epsilon = int(k % 2 == 0)
        r = k + epsilon
        n += epsilon + 4 * r
        k = (5 * r + 1) // 2
    return rows


def main():
    for invalid in [[(0, 0)], [(0, 1), (1, 0)], [(0, 2)]]:
        try:
            graph(2, invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("malformed graph accepted")
    fixtures, results = {}, {}
    for a in range(1, 4):
        g, predicted = sharpness_graph(a)
        label = "sharp_alpha_" + str(a)
        fixtures[label] = {"vertices": len(g), "edges": edges(g)}
        r = exact_invariants(g)
        assert r["critical"] and r["chi"] == predicted and r["alpha"] == a
        assert r["avoidance"]["P5"] and r["avoidance"]["bull"]
        assert r["rho4"] == (-1 if a == 1 else a - 2)
        results[label] = r

    # Genuine negative control: criticality cannot be omitted.
    noncritical = join(cycle(5), graph(3, []))
    r = exact_invariants(noncritical)
    assert not r["critical"] and r["avoidance"]["P5"] and r["avoidance"]["bull"]
    assert r["rho4"] < r["alpha"] - 2
    results["criticality_necessary"] = r

    # General coloring and obstruction calculations on a graph outside P5-free.
    e = edges(cycle(5))
    e += [(5 + i, j) for i in range(5) for j in range(5)
          if cycle(5)[i] >> j & 1]
    e += [(10, i) for i in range(5, 10)]
    results["mycielski_C5_outside_class"] = exact_invariants(graph(11, e))
    r = results["mycielski_C5_outside_class"]
    assert r["chi"] == 4 and r["critical"] and r["avoidance"]["bull"]
    assert not r["avoidance"]["P5"] and r["rho4"] < r["alpha"] - 2

    census = []
    for n in range(1, 6):
        pairs = list(combinations(range(n), 2))
        counts = {"n": n, "labeled_graphs": 1 << len(pairs),
                  "critical_P5_bull_free": 0, "critical_P5_banner_free": 0}
        for mask in range(1 << len(pairs)):
            g = graph(n, [e for i, e in enumerate(pairs) if mask >> i & 1])
            r = exact_invariants(g)
            for name in ["bull", "banner"]:
                if r["critical"] and r["avoidance"]["P5"] and r["avoidance"][name]:
                    counts["critical_P5_" + name + "_free"] += 1
                    if r["alpha"] >= 2:
                        assert r["rho4"] == r["alpha"] - 2
        census.append(counts)
    # Check the explicit pair-palette certificate at a range of odd demands.
    for s in range(50):
        multiplicities = [s, s + 1, s + 1, s, s]
        demands = [multiplicities[i] + multiplicities[(i - 2) % 5] for i in range(5)]
        assert demands == [2 * s, 2 * s + 1, 2 * s + 1, 2 * s + 1, 2 * s + 1]
        assert sum(multiplicities) == 5 * s + 2
    return {"claim_status": "finite exact controls; universal claims use proof.md",
            "fixtures": fixtures, "exact_controls": results,
            "complete_small_labeled_controls": census,
            "construction_recurrence_parameters": sharpness_parameters(8),
            "pair_palette_controls_odd_demands": [1, 99]}


if __name__ == "__main__":
    result = main()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    expected = Path(__file__).with_name("expected.json")
    if expected.exists():
        assert output == expected.read_text(), "exact control output changed"
    print(output, end="")
