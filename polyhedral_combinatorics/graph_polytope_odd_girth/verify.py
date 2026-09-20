#!/usr/bin/env python3
"""Exact finite corroboration for the odd-girth Ehrhart theorem.

The universal proof, including local Euler--Maclaurin, is in PROOF.md.
This program imports no previous research package and uses no floats.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json


def require(test, message):
    if not test:
        raise ValueError(message)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def multiply(a, b):
    out = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def evaluate(p, x):
    result = 0
    for a in reversed(p):
        result = result*x+a
    return result


def lagrange_basis(nodes):
    result = []
    for x in nodes:
        numerator, denominator = [Q(1)], Q(1)
        for y in nodes:
            if y != x:
                numerator = multiply(numerator, [-y, 1])
                denominator *= x-y
        result.append([a/denominator for a in numerator])
    return result


def interpolate(values, basis):
    require(len(values) == len(basis), "interpolation length")
    return trim([sum(y*p[j] for y, p in zip(values, basis))
                 for j in range(len(basis))])


def parity_polynomial(d, counts, bases=None):
    require(len(counts) >= 2*d+4, "insufficient count values")
    if bases is None:
        bases = [lagrange_basis(list(range(r, 2*d+2, 2))) for r in (0, 1)]
    residue = [interpolate([counts[n] for n in range(r, 2*d+2, 2)], bases[r])
               for r in (0, 1)]
    for n in range(2*d+2, len(counts)):
        require(evaluate(residue[n % 2], n) == counts[n], "holdout count mismatch")
    padded = [p+[Q(0)]*(d+1-len(p)) for p in residue]
    return trim([(a-b)/2 for a, b in zip(*padded)])


def numerator(d, counts):
    h = [sum((-1)**j*comb(d+1, j)*counts[n-2*j]
             for j in range(min(d+1, n//2)+1)) for n in range(len(counts))]
    require(h[-2:] == [0, 0], "numerator tail is not zero")
    return trim(h)


def minus_one_order(p):
    order = 0
    p = trim(p)
    while len(p) > 1 and evaluate(p, -1) == 0:
        quotient = [p[0]]
        for a in p[1:-1]:
            quotient.append(a-quotient[-1])
        require(p[-1] == quotient[-1], "synthetic division remainder")
        p = trim(quotient)
        order += 1
    return order, evaluate(p, -1)


def validate_graph(d, edges):
    require(type(d) is int and d >= 1, "invalid dimension")
    require(all(type(u) is int and type(v) is int and 0 <= u < v < d
                for u, v in edges), "invalid edge")
    require(len(set(edges)) == len(edges), "duplicate edge")


def odd_cycles(d, edges):
    """Canonical unoriented shortest odd cycles, each represented once."""
    validate_graph(d, edges)
    es = set(edges)
    for size in range(3, d+1, 2):
        found = []
        for vertices in combinations(range(d), size):
            first = vertices[0]
            for tail in permutations(vertices[1:]):
                if tail[0] > tail[-1]:
                    continue
                cycle = (first,)+tail
                if all(tuple(sorted((cycle[i], cycle[(i+1) % size]))) in es
                       for i in range(size)):
                    found.append(cycle)
        if found:
            return found
    return []


def small_face_volume(d, edges, cycle):
    """Independent interval/area calculation, with at most 2 free coordinates."""
    outside = [v for v in range(d) if v not in cycle]
    require(len(outside) <= 2, "unsupported face dimension")
    es = set(edges)
    bounds = [Q(1, 2) if any(tuple(sorted((v, u))) in es for u in cycle)
              else Q(1) for v in outside]
    if not outside:
        return Q(1)
    if len(outside) == 1:
        return bounds[0]
    a, b = bounds
    area = a*b
    if tuple(outside) in es:
        excess = max(Q(0), a+b-1)
        area -= excess**2/2
    require(area > 0, "nonpositive face volume")
    return area


def all_graph_counts(d, max_n):
    """Count integer vectors once, then use the Boolean superset transform.

An assignment permits exactly those graph edges with x_u+x_v<=n.
Every graph contained in that permitted-edge mask accepts the assignment.
"""
    pairs = list(combinations(range(d), 2))
    counts = [[] for _ in range(1 << len(pairs))]
    assignments = 0
    for n in range(max_n+1):
        histogram = [0]*(1 << len(pairs))
        for values in product(range(n+1), repeat=d):
            allowed = 0
            for i, (u, v) in enumerate(pairs):
                if values[u]+values[v] <= n:
                    allowed |= 1 << i
            histogram[allowed] += 1
            assignments += 1
        for bit in range(len(pairs)):
            for mask in range(1 << len(pairs)):
                if not mask & (1 << bit):
                    histogram[mask] += histogram[mask | (1 << bit)]
        for mask, value in enumerate(histogram):
            counts[mask].append(value)
    return counts, assignments


def direct_count(d, edges, n):
    return sum(all(x[u]+x[v] <= n for u, v in edges)
               for x in product(range(n+1), repeat=d))


def audit_small_graphs():
    records = []
    totals = {"graphs": 0, "bipartite": 0, "nonbipartite": 0,
              "assignments": 0, "holdout_values": 0, "direct_comparisons": 0}
    for d in range(1, 6):
        pairs = list(combinations(range(d), 2))
        table, assignments = all_graph_counts(d, 2*d+5)
        totals["assignments"] += assignments
        bases = [lagrange_basis(list(range(r, 2*d+2, 2))) for r in (0, 1)]
        for mask, counts in enumerate(table):
            edges = [e for i, e in enumerate(pairs) if mask & (1 << i)]
            cycles = odd_cycles(d, edges)
            b = parity_polynomial(d, counts, bases)
            order, value = minus_one_order(numerator(d, counts))
            if cycles:
                g = len(cycles[0])
                volume_sum = sum(small_face_volume(d, edges, c) for c in cycles)
                require(len(b)-1 == d-g and b[-1] == volume_sum/2**(g+1),
                        f"parity theorem failed: d={d}, mask={mask}, B={b}")
                require(order == g and value == 2**(d-g)*factorial(d-g)*volume_sum,
                        f"pole theorem failed: d={d}, mask={mask}")
                totals["nonbipartite"] += 1
            else:
                g, volume_sum = None, Q(0)
                require(b == [0] and order >= d+1, "bipartite period failure")
                totals["bipartite"] += 1
            if d <= 3 or mask in (0, 1, (1 << len(pairs))-1):
                for n in range(4):
                    require(counts[n] == direct_count(d, edges, n),
                            "superset transform disagrees with direct count")
                    totals["direct_comparisons"] += 1
            totals["graphs"] += 1
            totals["holdout_values"] += 4
            records.append([d, mask, g, len(cycles), str(volume_sum),
                            [str(x) for x in b], order, str(value)])
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest()
    return {**totals, "record_sha256": digest}


def cycle_trace_counts(g, max_n, widths=None):
    """Trace transfer for independent-vertex blow-ups, not block-sum polytopes.

For width a, fixing the maximum r of its a coordinates has weight
(r+1)^a-r^a. Adjacency between two blocks means max_i+max_j<=n.
"""
    widths = [1]*g if widths is None else widths
    require(len(widths) == g and all(type(a) is int and a >= 1 for a in widths),
            "invalid blow-up widths")
    output = []
    for n in range(max_n+1):
        weights = [[(r+1)**a-r**a for r in range(n+1)] for a in widths]
        total = 0
        for first in range(n+1):
            dp = [0]*(n+1)
            dp[first] = weights[0][first]
            for index in range(1, g):
                prefix = []
                partial = 0
                for a in dp:
                    partial += a
                    prefix.append(partial)
                dp = [weights[index][r]*prefix[n-r] for r in range(n+1)]
            total += sum(dp[:n-first+1])
        output.append(total)
    return output


def audit_named_families():
    records = []
    for widths in [(1,)*3, (1,)*5, (1,)*7, (1,)*9,
                   (2, 1, 1, 1, 1), (2, 2, 1, 1, 1), (2, 1, 2, 1, 1, 1, 1)]:
        d, g = sum(widths), len(widths)
        cycle_count = 1
        for a in widths:
            cycle_count *= a
        counts = cycle_trace_counts(g, 2*d+5, widths)
        b = parity_polynomial(d, counts)
        order, residual = minus_one_order(numerator(d, counts))
        require(len(b)-1 == d-g and b[-1] == Q(cycle_count, 2**(d+1)),
                "cycle-blow-up parity mismatch")
        require(order == g and residual == factorial(d-g)*cycle_count,
                "cycle-blow-up residual mismatch")
        records.append({"widths": list(widths), "degree_B": len(b)-1,
                        "leading_B": str(b[-1]), "root_order": order,
                        "residual": str(residual)})
    # Complete-graph counts have a separate elementary maximum-coordinate sum.
    for d in (3, 4, 5, 6, 8):
        counts = []
        for n in range(2*d+6):
            k = n//2
            last = k if n % 2 == 0 else k+1
            counts.append((k+1)**d+d*sum(s**(d-1) for s in range(1, last+1)))
        b = parity_polynomial(d, counts)
        order, residual = minus_one_order(numerator(d, counts))
        require(len(b)-1 == d-3 and b[-1] == Q(comb(d, 3), 2**(d+1)),
                "complete-graph parity mismatch")
        require(order == 3 and residual == factorial(d)//6,
                "complete-graph residual mismatch")
        records.append({"complete_graph": d, "leading_B": str(b[-1]),
                        "root_order": order, "residual": str(residual)})
    # The triangle with a two-edge tail is not a dominating-cycle example.
    tail_edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
    require(small_face_volume(5, tail_edges, (0, 1, 2)) == Q(3, 8),
            "nondominating-cycle face area")
    require(Q(3, 8) != Q(1, 4), "missing-domination negative control")
    return {"cases": records, "nondominating_face_area": "3/8"}


def audit_local_cone():
    slack_cases = proper_faces = 0
    for g in (3, 5, 7, 9):
        # Twice T=(I+S)^-1; no floating-point matrix inversion.
        twice_t = [[(-1)**((j-i) % g) for j in range(g)] for i in range(g)]
        for i in range(g):
            for j in range(g):
                require(twice_t[i][j]+twice_t[(i+1) % g][j]
                        == (2 if i == j else 0), "cycle inverse")
        for slacks in product(range(2), repeat=g):
            tu = [sum(a*u for a, u in zip(row, slacks)) for row in twice_t]
            for n in (0, 1, 2):
                twice_x = [n-v for v in tu]
                integral = all(v % 2 == 0 for v in twice_x)
                require(integral == (sum(slacks) % 2 == n % 2), "slack parity")
                require(all(twice_x[i]+twice_x[(i+1) % g]
                            == 2*(n-slacks[i]) for i in range(g)), "slack inversion")
                slack_cases += 1
        # Every proper subset of active cycle equations has an integral point.
        # This is the needed quotient-lattice translation, not feasibility in P.
        for active in range((1 << g)-1):
            color = [None]*g
            adj = [[] for _ in range(g)]
            for i in range(g):
                if active & (1 << i):
                    j = (i+1) % g
                    adj[i].append(j)
                    adj[j].append(i)
            for root in range(g):
                if color[root] is not None:
                    continue
                color[root] = 0
                stack = [root]
                while stack:
                    u = stack.pop()
                    for v in adj[u]:
                        if color[v] is None:
                            color[v] = 1-color[u]
                            stack.append(v)
                        require(color[v] != color[u], "proper cycle subset not bipartite")
            require(all(color[i]+color[(i+1) % g] == 1 for i in range(g)
                        if active & (1 << i)), "proper-face integer translation")
            proper_faces += 1
    rejected = 0
    for d, edges in [(0, []), (3, [(0, 0)]), (3, [(0, 3)]),
                     (3, [(1, 0)]), (3, [(0, 1), (0, 1)])]:
        try:
            validate_graph(d, edges)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid graph accepted")
    return {"slack_parity_cases": slack_cases,
            "proper_face_integer_translations": proper_faces,
            "malformed_graphs_rejected": rejected,
            "local_jump_at_zero": {str(g): str(Q(1, 2**g)) for g in (3, 5, 7, 9)}}


def main():
    output = {"status": "PASS", "small_graphs": audit_small_graphs(),
              "named_families": audit_named_families(), "local_cones": audit_local_cone(),
              "scope": "Finite exact corroboration; universal proof uses local Euler-Maclaurin"}
    expected = Path(__file__).with_name("expected.json")
    if expected.exists():
        require(output == json.loads(expected.read_text()), "expected output mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
