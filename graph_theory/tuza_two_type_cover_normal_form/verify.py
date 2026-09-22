"""Independent definition-level regression tests; not a finite proof census.

The reference enumerates all triangle-free clique cores for clique order <=5
and computes their independence numbers without the normal-form theorem.
Tiny full graphs are also checked by direct triangle-hitting recursion.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json

from cover import reconstruct, rectangle_packing, solve


def triangle_masks(order, edges):
    index = {e: i for i, e in enumerate(edges)}
    answer = []
    for u, v, w in combinations(range(order), 3):
        triple = ((u, v), (u, w), (v, w))
        if all(e in index for e in triple):
            answer.append(sum(1 << index[e] for e in triple))
    return answer


@lru_cache(None)
def all_triangle_free_cores(k):
    edges = list(combinations(range(k), 2))
    triangles = triangle_masks(k, edges)
    result = []
    for mask in range(1 << len(edges)):
        if any(mask & t == t for t in triangles):
            continue
        adjacent = [0] * k
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                adjacent[u] |= 1 << v
                adjacent[v] |= 1 << u
        alpha = [0] * (1 << k)
        for s in range(1, 1 << k):
            v = (s & -s).bit_length() - 1
            remainder = s ^ (1 << v)
            alpha[s] = max(alpha[remainder], 1 + alpha[remainder & ~adjacent[v]])
        result.append((mask.bit_count(), tuple(alpha)))
    return result


def reference(a, b, c, d, m, n):
    k = a + b + c + d
    S = (1 << (c + a)) - 1
    T = ((1 << c) - 1) | (((1 << b) - 1) << (c + a))
    return min(k * (k - 1) // 2 - size + m * (a + c - alpha[S])
               + n * (b + c - alpha[T])
               for size, alpha in all_triangle_free_cores(k))


def direct_triangle_cover(order, edges):
    triangles = triangle_masks(order, edges)

    @lru_cache(None)
    def cost(mask):
        triangle = next((t for t in triangles if mask & t == t), None)
        if triangle is None:
            return 0
        return 1 + min(cost(mask ^ (1 << i)) for i in range(len(edges))
                       if triangle >> i & 1)

    return cost((1 << len(edges)) - 1)


def expanded_graph(a, b, c, d, m, n):
    k = a + b + c + d
    edges = set(combinations(range(k), 2))
    S = set(range(c + a))
    T = set(range(c)) | set(range(c + a, c + a + b))
    for i in range(m + n):
        edges.update((u, k + i) for u in (S if i < m else T))
    return k + m + n, sorted(edges)


def check_certificate(record):
    a, b, c, d, m, n = record["parameters"]
    k = a + b + c + d
    witness = reconstruct(record)
    A, B, S, T = (witness[s] for s in ("A", "B", "S", "T"))
    kept, left = witness["kept"], witness["left"]
    assert A <= S and B <= T
    assert all((u in left) != (v in left) for u, v in kept)
    assert not any({u, v} <= A or {u, v} <= B for u, v in kept)
    assert record["tau"] == (k * (k - 1) // 2 - len(kept)
                              + m * len(S - A) + n * len(T - B))


def check_rectangle(record):
    a, b, c, d, m, n = record["parameters"]
    k = a + b + c + d
    witness = reconstruct(record)
    used = set()
    triangles = rectangle_packing(record)
    for u, v, center in triangles:
        assert 0 <= u < k and 0 <= v < k and u != v
        assert k <= center < k + m + n
        neighbors = witness["S" if center < k + m else "T"]
        assert u in neighbors and v in neighbors
        for edge in combinations(sorted((u, v, center)), 2):
            assert edge not in used
            used.add(edge)
    expected = record["x"] * (record["z"] if record["mode"] == 1 else record["y"])
    assert len(triangles) == (0 if record["mode"] == 0 else expected)
    return bool(triangles)


def three_type_host(t):
    # Universal a=0; inner path vertices c=1,d=2; endpoint classes B,E.
    B, E = set(range(3, t + 3)), set(range(t + 3, 2 * t + 3))
    neighborhoods = [B | {2}, B | E, {1} | E]
    k = 2 * t + 3
    edges = [e for e in combinations(range(k), 2)
             if not any(set(e) <= s for s in neighborhoods)]
    return k, edges


def main():
    digest = sha256()
    cases = direct_cases = rectangle_cases = 0
    for k in range(6):
        for a in range(k + 1):
            for b in range(k - a + 1):
                for c in range(k - a - b + 1):
                    d = k - a - b - c
                    for m, n in product((0, 1, 2, 7), repeat=2):
                        params = (a, b, c, d, m, n)
                        record = solve(*params)
                        check_certificate(record)
                        rectangle_cases += check_rectangle(record)
                        assert record["tau"] == reference(*params), params
                        if k <= 3 and m + n <= 3:
                            order, edges = expanded_graph(*params)
                            assert record["tau"] == direct_triangle_cover(order, edges), params
                            direct_cases += 1
                        digest.update((json.dumps(record, sort_keys=True) + "\n").encode())
                        cases += 1
    obstruction_checks = []
    for t in (2, 3, 5):
        k, edges = three_type_host(t)
        tf = len(edges) - direct_triangle_cover(k, edges)
        cut = max(sum(((mask >> u) ^ (mask >> v)) & 1 for u, v in edges)
                  for mask in range(1 << (k - 1)))
        assert tf == 4 * t + 1 and cut == 4 * t
        obstruction_checks.append({"t": t, "triangle_free": tf, "max_cut": cut})
    large = solve(17, 13, 9, 11, 1000000007, 11)
    check_certificate(large)
    check_rectangle(large)
    # The stronger whole-residual bipartiteness assertion is false even for two types.
    small = solve(1, 1, 1, 0, 3, 3)
    order, edges = expanded_graph(1, 1, 1, 0, 3, 3)
    max_cut = max(sum(((mask >> u) ^ (mask >> v)) & 1 for u, v in edges)
                  for mask in range(1 << (order - 1)))
    assert small["tau"] == 2 and len(edges) - max_cut == 3
    rejected = 0
    for field, value in (("tau", 3), ("x", 2), ("w_left", -1), ("mode", 3)):
        mutation = dict(small, **{field: value})
        try:
            check_certificate(mutation)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(("accepted invalid certificate", field))
    summary = {"cover_cases": cases, "direct_triangle_hitting_cases": direct_cases,
               "nonempty_rectangle_packings_checked": rectangle_cases,
               "malformed_certificates_rejected": rejected,
               "records_sha256": digest.hexdigest(),
               "three_type_obstruction_checks": obstruction_checks,
               "large_multiplicity_example": large,
               "two_type_whole_graph_bipartization": {"tau": 2, "bipartization": 3}}
    expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
    assert summary == expected, ("unexpected regression output", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
