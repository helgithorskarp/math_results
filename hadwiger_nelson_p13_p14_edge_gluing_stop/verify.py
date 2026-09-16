#!/usr/bin/env python3
"""Independent exact checker for the frozen P13--P14 edge-gluing stop.

Only the Python standard library is used.  Coordinates are fractions in the
cyclotomic field Q(zeta_546), represented projectively as pairs of integral
polynomials.  Equality and unit distance are decided modulo Phi_546.
"""

import argparse
from collections import deque
from functools import lru_cache
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 546
STEP13 = 42
STEP14 = 39


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def trim(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def poly_div_exact(a, b):
    a, b = trim(a), trim(b)
    require(b[-1] == 1, "cyclotomic divisor is monic")
    q = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b):
        c, shift = a[-1], len(a) - len(b)
        q[shift] = c
        for i, x in enumerate(b):
            a[shift + i] -= c * x
        a = trim(a)
    require(not any(a), "exact cyclotomic division")
    return trim(q)


@lru_cache(None)
def cyclotomic(n):
    p = [-1] + [0] * (n - 1) + [1]
    for d in divisors(n)[:-1]:
        p = poly_div_exact(p, cyclotomic(d))
    return tuple(p)


PHI = cyclotomic(N)
DEGREE = len(PHI) - 1


def root_power_table():
    """Basis coordinates of 1,zeta,...,zeta^(N-1), in O(N*degree)."""
    roots = []
    one = [0] * DEGREE
    one[0] = 1
    roots.append(tuple(one))
    for _ in range(1, N):
        previous = roots[-1]
        top = previous[-1]
        current = [0] + list(previous[:-1])
        if top:
            # x^degree = -sum_{j<degree} PHI[j] x^j.
            for j in range(DEGREE):
                current[j] -= top * PHI[j]
        roots.append(tuple(current))
    return tuple(roots)


ROOTS = root_power_table()


def add(a, b, scale=1):
    ans = dict(a)
    for e, c in b.items():
        ans[e] = ans.get(e, 0) + scale * c
        if ans[e] == 0:
            del ans[e]
    return ans


def multiply(a, b):
    ans = {}
    for e, c in a.items():
        for f, d in b.items():
            k = e + f
            ans[k] = ans.get(k, 0) + c * d
    return {e: c for e, c in ans.items() if c}


def cyclic_key(word):
    coefficients = {}
    for e, c in word.items():
        k = e % N
        coefficients[k] = coefficients.get(k, 0) + c
        if not coefficients[k]:
            del coefficients[k]
    return tuple(sorted(coefficients.items()))


@lru_cache(None)
def field_remainder_key(key):
    answer = [0] * DEGREE
    for e, c in key:
        root = ROOTS[e]
        for j, x in enumerate(root):
            answer[j] += c * x
    return tuple(answer)


def field_remainder(word):
    return field_remainder_key(cyclic_key(word))


def field_zero(word):
    return not any(field_remainder(word))


def norm_word(a):
    ans = {}
    for e, c in a.items():
        for f, d in a.items():
            k = (e - f) % N
            ans[k] = ans.get(k, 0) + c * d
    return {e: c for e, c in ans.items() if c}


def monomial_difference(a, b):
    ans = {}
    ans[a % N] = ans.get(a % N, 0) + 1
    ans[b % N] = ans.get(b % N, 0) - 1
    return {e: c for e, c in ans.items() if c}


def equal(left, right):
    ln, ld = left
    rn, rd = right
    return field_zero(add(multiply(ln, rd), multiply(rn, ld), -1))


def unit(left, right):
    ln, ld = left
    rn, rd = right
    numerator = add(multiply(ln, rd), multiply(rn, ld), -1)
    denominator = multiply(ld, rd)
    return field_zero(add(norm_word(numerator), norm_word(denominator), -1))


def cloud(order, step, anchor_step):
    denominator = monomial_difference(0, anchor_step)
    require(not field_zero(denominator), "nonzero normalization edge")
    points, addresses = [], []
    for i in range(order):
        for j in range(order):
            point = (monomial_difference(step * i, step * j), denominator)
            if not any(equal(point, old) for old in points):
                points.append(point)
                addresses.append([i, j])
    return points, addresses


def components(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    unseen, answer = set(range(n)), []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        queue, comp = [root], []
        while queue:
            a = queue.pop()
            comp.append(a)
            for b in sorted(adj[a]):
                if b in unseen:
                    unseen.remove(b)
                    queue.append(b)
        answer.append(sorted(comp))
    return adj, answer


def k_core(adj, k):
    degree = list(map(len, adj))
    removed = [False] * len(adj)
    queue = deque(i for i, d in enumerate(degree) if d < k)
    while queue:
        a = queue.popleft()
        if removed[a]:
            continue
        removed[a] = True
        for b in adj[a]:
            if not removed[b]:
                degree[b] -= 1
                if degree[b] < k:
                    queue.append(b)
    return [i for i in range(len(adj)) if not removed[i]]


def cuts_and_bridges(adj):
    time = 0
    seen = [-1] * len(adj)
    low = [0] * len(adj)
    parent = [-1] * len(adj)
    cuts, bridges = set(), []

    def visit(a):
        nonlocal time
        seen[a] = low[a] = time
        time += 1
        children = 0
        for b in sorted(adj[a]):
            if seen[b] < 0:
                parent[b] = a
                children += 1
                visit(b)
                low[a] = min(low[a], low[b])
                if parent[a] < 0 and children > 1:
                    cuts.add(a)
                if parent[a] >= 0 and low[b] >= seen[a]:
                    cuts.add(a)
                if low[b] > seen[a]:
                    bridges.append([min(a, b), max(a, b)])
            elif b != parent[a]:
                low[a] = min(low[a], seen[b])

    for root in range(len(adj)):
        if seen[root] < 0:
            visit(root)
    return sorted(cuts), sorted(bridges)


def verify(expected):
    require(N == 546 and DEGREE == 144, "composite cyclotomic field")
    p13, a13 = cloud(13, STEP13, STEP13)
    p14, a14 = cloud(14, STEP14, 2 * STEP14)
    require(len(p13) == 157 and len(p14) == 99, "full cloud cardinalities")

    physical, provenance, membership = [], [], []

    def insert(point, source, address):
        hits = [i for i, old in enumerate(physical) if equal(point, old)]
        require(len(hits) <= 1, "collision uniqueness")
        if hits:
            i = hits[0]
            provenance[i].append([source, *address])
            membership[i].add(source)
            return i
        physical.append(point)
        provenance.append([[source, *address]])
        membership.append({source})
        return len(physical) - 1

    map13 = [insert(p, "P13", a) for p, a in zip(p13, a13)]
    map14 = [insert(p, "P14", a) for p, a in zip(p14, a14)]
    require(len(physical) == 253, "collision-merged base order")

    edges = [[a, b] for a in range(len(physical))
             for b in range(a + 1, len(physical)) if unit(physical[a], physical[b])]
    edge_set = {tuple(e) for e in edges}
    require(len(edges) == 492, "complete unit-edge count")
    require(sum(a in set(map13) and b in set(map13) for a, b in edges) == 312,
            "P13 source edge count")
    require(sum(a in set(map14) and b in set(map14) for a, b in edges) == 182,
            "P14 source edge count")

    shared = [i for i, m in enumerate(membership) if m == {"P13", "P14"}]
    private_cross = [[a, b] for a, b in edges
                     if (membership[a] == {"P13"} and membership[b] == {"P14"})
                     or (membership[a] == {"P14"} and membership[b] == {"P13"})]
    require(shared == [0, 1, 13], "three exact anchor collisions")
    require(not private_cross, "empty private cross-contact set")

    # The declared completion adds both equilateral apices of each private
    # cross edge.  Its input set is empty, so the complete final support is the
    # collision-merged base support just reconstructed.
    completion_points = 2 * len(private_cross)
    require(completion_points == 0, "empty declared completion")

    word = expected["three_word"]
    require(isinstance(word, str) and len(word) == len(physical)
            and set(word) <= set("012"), "three-word shape")
    require(all(word[a] != word[b] for a, b in edges), "proper three-word")
    odd_cycle = expected["odd_cycle"]
    require(len(odd_cycle) % 2 == 1 and len(set(odd_cycle)) == len(odd_cycle),
            "simple odd cycle")
    require(all(tuple(sorted((a, odd_cycle[(i + 1) % len(odd_cycle)]))) in edge_set
                for i, a in enumerate(odd_cycle)), "odd-cycle edges")

    adj, comps = components(len(physical), edges)
    cuts, bridges = cuts_and_bridges(adj)
    core3, core4 = k_core(adj, 3), k_core(adj, 4)
    edge_sha = hashlib.sha256((json.dumps(edges, separators=(",", ":")) + "\n").encode()).hexdigest()
    report = {
        "verified": True,
        "record_improvement": False,
        "scope": "one edge-normalized P13--P14 gluing and its private-cross equilateral completion",
        "cyclotomic_order": N,
        "cyclotomic_degree": DEGREE,
        "formal_cloud_orders": [len(p13), len(p14)],
        "physical_vertices": len(physical),
        "complete_unit_edges": len(edges),
        "shared_vertices": shared,
        "shared_provenance": {str(i): provenance[i] for i in shared},
        "private_cross_edges": len(private_cross),
        "completion_points": completion_points,
        "component_orders": sorted((len(c) for c in comps), reverse=True),
        "articulation_vertices": cuts,
        "bridges": bridges,
        "three_core_vertices": len(core3),
        "four_core_vertices": len(core4),
        "chromatic_number": 3,
        "odd_cycle_length": len(odd_cycle),
        "edge_sha256": edge_sha,
    }
    require(report == expected["report"], "expected report")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expected", type=Path, default=HERE / "expected.json")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    expected = json.loads(args.expected.read_text())
    report = verify(expected)
    if args.out:
        args.out.write_text(dump(report))
    print(dump(report), end="")


if __name__ == "__main__":
    main()
