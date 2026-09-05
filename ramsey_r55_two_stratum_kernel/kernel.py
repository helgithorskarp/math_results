#!/usr/bin/env python3
"""Exact three-anchor / six-signature completion interface; standard library only."""
from collections import deque
from itertools import combinations


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode(doc):
    require(set(doc) == {"n", "red_edges"}, "graph fields")
    n = doc["n"]
    require(type(n) is int and n >= 3, "graph order")
    edges = doc["red_edges"]
    require(type(edges) is list, "edge list")
    for e in edges:
        require(type(e) is list and len(e) == 2 and
                all(type(v) is int for v in e) and 0 <= e[0] < e[1] < n,
                "edge endpoints")
    require(edges == sorted(edges) and len({tuple(e) for e in edges}) == len(edges),
            "edge order / duplicates")
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def document(adj):
    return {"n": len(adj), "red_edges": [[u, v] for u, v in
            combinations(range(len(adj)), 2) if adj[u] >> v & 1]}


def signatures(adj):
    result = [-1] * 3 + [sum(1 << i for i in range(3) if adj[i] >> v & 1)
                         for v in range(3, len(adj))]
    require(all(1 <= s <= 6 for s in result[3:]), "proper nonempty signatures required")
    return result


def free_edges(adj):
    sig = signatures(adj)
    return [(u, v) for u, v in combinations(range(3, len(adj)), 2)
            if sig[u] ^ sig[v] == 7]


def cliques(adj, red, size, vertices=None):
    n = len(adj)
    if vertices is None:
        vertices = range(n)
    candidates = sum(1 << v for v in vertices)
    mask = (1 << n) - 1
    rows = adj if red else [mask ^ a ^ (1 << v) for v, a in enumerate(adj)]
    answer = []

    def visit(prefix, available):
        if len(prefix) == size:
            answer.append(list(prefix))
            return
        while available.bit_count() >= size - len(prefix):
            bit = available & -available
            available ^= bit
            v = bit.bit_length() - 1
            visit(prefix + (v,), available & rows[v])

    visit((), candidates)
    return answer


def preflight(adj):
    sig = signatures(adj)
    root_rows = []
    for root in range(3):
        for red in (True, False):
            vertices = [v for v in range(len(adj)) if v != root and
                        bool(adj[root] >> v & 1) == red]
            root_rows.append({"root": root, "color": "red" if red else "blue",
                              "same_k4": cliques(adj, red, 4, vertices),
                              "opposite_k5": cliques(adj, not red, 5, vertices)})
    singletons = [v for v in range(3, len(adj)) if sig[v].bit_count() == 1]
    pairs = [v for v in range(3, len(adj)) if sig[v].bit_count() == 2]
    extra = {"red_singleton_k5": cliques(adj, True, 5, singletons),
             "blue_pair_k5": cliques(adj, False, 5, pairs)}
    passed = not any(r["same_k4"] or r["opposite_k5"] for r in root_rows)
    return {"passes": passed and not any(extra.values()),
            "roots": root_rows, **extra}


def compile_kernel(adj):
    """All residual colored five-set clauses, including empty obstruction rows."""
    free = free_edges(adj)
    positions = {e: j for j, e in enumerate(free)}
    rows = []
    for five in combinations(range(len(adj)), 5):
        variables, fixed_colors = [], set()
        for u, v in combinations(five, 2):
            if (u, v) in positions:
                variables.append(positions[u, v])
            else:
                fixed_colors.add((adj[u] >> v) & 1)
        for color in (1, 0):
            if fixed_colors <= {color}:
                rows.append({"color": "red" if color else "blue",
                             "vertices": list(five), "variables": sorted(variables)})
    return {"variables": [list(e) for e in free], "clauses": rows}


def satisfies(kernel, assignment):
    require(type(assignment) is int and 0 <= assignment < 1 << len(kernel["variables"]),
            "assignment out of range")
    for row in kernel["clauses"]:
        mask = sum(1 << j for j in row["variables"])
        selected = assignment & mask
        if selected == (mask if row["color"] == "red" else 0):
            return False
    return True


def complete(adj, assignment):
    free = free_edges(adj)
    require(type(assignment) is int and 0 <= assignment < 1 << len(free),
            "assignment out of range")
    out = list(adj)
    for j, (u, v) in enumerate(free):
        out[u] &= ~(1 << v)
        out[v] &= ~(1 << u)
        if assignment >> j & 1:
            out[u] |= 1 << v
            out[v] |= 1 << u
    return out


def bipartite(left, right):
    """Exact margin feasibility, with edge witness or elementary cut certificate."""
    require(all(type(x) is int for x in left + right), "nonintegral margins")
    a, b = len(left), len(right)
    if any(x < 0 or x > b for x in left) or any(x < 0 or x > a for x in right):
        return {"feasible": False, "reason": "out_of_range"}
    if sum(left) != sum(right):
        return {"feasible": False, "reason": "total_mismatch"}
    sink = a + b + 1
    size = sink + 1
    capacity = [[0] * size for _ in range(size)]
    for i, x in enumerate(left):
        capacity[0][i + 1] = x
    for i in range(a):
        for j in range(b):
            capacity[i + 1][a + 1 + j] = 1
    for j, x in enumerate(right):
        capacity[a + 1 + j][sink] = x
    residual = [row[:] for row in capacity]
    value = 0
    while True:
        pred = {0: -1}
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for v, cap in enumerate(residual[u]):
                if cap and v not in pred:
                    pred[v] = u
                    queue.append(v)
        if sink not in pred:
            break
        v = sink
        while v:
            u = pred[v]
            residual[u][v] -= 1
            residual[v][u] += 1
            v = u
        value += 1
    chosen = [[i, j] for i in range(a) for j in range(b)
              if residual[i + 1][a + 1 + j] == 0]
    reachable = sorted(pred)
    cut = sum(capacity[u][v] for u in pred for v in range(size) if v not in pred)
    require(cut == value, "flow-cut mismatch")
    return {"feasible": value == sum(left), "flow": value, "required": sum(left),
            "edges": chosen, "reachable": reachable, "cut_capacity": cut}


def degree_interface(adj, target):
    require(len(target) == len(adj) and all(type(x) is int for x in target),
            "degree target")
    sig = signatures(adj)
    free = free_edges(adj)
    fixed = list(adj)
    for u, v in free:
        fixed[u] &= ~(1 << v)
        fixed[v] &= ~(1 << u)
    require(all(target[e] == fixed[e].bit_count() for e in range(3)), "root degrees")
    margins = [target[v] - fixed[v].bit_count() for v in range(len(adj))]
    blocks = []
    for s in (1, 2, 3):
        left = [v for v in range(3, len(adj)) if sig[v] == s]
        right = [v for v in range(3, len(adj)) if sig[v] == 7 - s]
        lm, rm = [margins[v] for v in left], [margins[v] for v in right]
        blocks.append({"left": left, "right": right, "left_margins": lm,
                       "right_margins": rm, "certificate": bipartite(lm, rm)})
    return {"margins": margins, "blocks": blocks,
            "degree_feasible": all(b["certificate"]["feasible"] for b in blocks)}
