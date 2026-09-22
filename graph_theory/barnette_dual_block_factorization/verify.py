#!/usr/bin/env python3
"""Definition-level audit for the block and cactus product formulas."""

from __future__ import annotations

import hashlib
import json
from itertools import combinations


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    adj = {v: set() for v in vertices}
    for u, v in edges:
        if u in vertices and v in vertices:
            adj[u].add(v)
            adj[v].add(u)
    seen = set()
    todo = [next(iter(vertices))]
    while todo:
        v = todo.pop()
        if v in seen:
            continue
        seen.add(v)
        todo.extend(adj[v] - seen)
    return seen == vertices


def is_tree(vertices, edges):
    vertices = set(vertices)
    kept = {tuple(sorted(e)) for e in edges if set(e) <= vertices}
    return connected(vertices, kept) and len(kept) == len(vertices) - 1


def canonical_cycle(seq):
    seq = tuple(seq)
    variants = []
    for word in (seq, tuple(reversed(seq))):
        for i in range(len(word)):
            variants.append(word[i:] + word[:i])
    return min(variants)


def cycles(vertices, edges):
    adj = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    found = set()
    for start in vertices:
        stack = [(start, (start,), frozenset((start,)))]
        while stack:
            v, path, used = stack.pop()
            for w in adj[v]:
                if w == start and len(path) >= 4:
                    found.add(canonical_cycle(path))
                elif w not in used and w >= start:
                    stack.append((w, path + (w,), used | {w}))
    return sorted(found)


def biconnected_blocks(vertices, edges):
    """Return the edge sets of all undirected blocks (bridges included)."""
    vertices = tuple(vertices)
    edges = tuple(tuple(sorted(e)) for e in edges)
    adj = {v: [] for v in vertices}
    for eid, (u, v) in enumerate(edges):
        adj[u].append((v, eid))
        adj[v].append((u, eid))
    discovery = {}
    low = {}
    edge_stack = []
    components = []
    tick = 0

    def visit(v, parent_edge):
        nonlocal tick
        tick += 1
        discovery[v] = low[v] = tick
        for w, eid in adj[v]:
            if eid == parent_edge:
                continue
            if w not in discovery:
                edge_stack.append(eid)
                visit(w, eid)
                low[v] = min(low[v], low[w])
                if low[w] >= discovery[v]:
                    block = []
                    while True:
                        top = edge_stack.pop()
                        block.append(top)
                        if top == eid:
                            break
                    components.append(block)
            elif discovery[w] < discovery[v]:
                edge_stack.append(eid)
                low[v] = min(low[v], discovery[w])

    visit(vertices[0], None)
    if len(discovery) != len(vertices):
        return None
    blocks = []
    for block in components:
        blocks.append(tuple(sorted(edges[eid] for eid in block)))
    return tuple(sorted(blocks))


def cactus_blocks(vertices, edges):
    """Return cycle-block vertex sets, or None when the graph is not a cactus."""
    cycle_blocks = []
    for block_edges in biconnected_blocks(vertices, edges):
        if len(block_edges) == 1:
            continue
        local_degree = {}
        for edge in block_edges:
            for v in edge:
                local_degree[v] = local_degree.get(v, 0) + 1
        if (len(block_edges) != len(local_degree)
                or set(local_degree.values()) != {2}):
            return None
        cycle_blocks.append(tuple(sorted(local_degree)))
    return tuple(sorted(cycle_blocks))


def is_cut_vertex(vertices, edges, v):
    rest = set(vertices) - {v}
    return bool(rest) and not connected(rest, edges)


def predicted_count(blue, green, edges):
    vertices = tuple(blue) + tuple(green)
    cs = cactus_blocks(vertices, edges)
    if cs is None:
        raise ValueError("not a cactus")
    degrees = {v: 0 for v in vertices}
    for u, v in edges:
        degrees[u] += 1
        degrees[v] += 1
    product = 1
    factors = []
    for cyc in cs:
        q = sum(v in green and degrees[v] == 2 for v in cyc)
        factors.append(q)
        product *= q
    return product, tuple(sorted(factors))


def block_product(blue, green, edges):
    """General block-factorization prediction from the theorem."""
    vertices = tuple(blue) + tuple(green)
    cut = {v for v in vertices if is_cut_vertex(vertices, edges, v)}
    product = 1
    factors = []
    for block_edges in biconnected_blocks(vertices, edges):
        if len(block_edges) == 1:
            continue
        block_vertices = set(v for e in block_edges for v in e)
        optional = sorted((block_vertices & set(green)) - cut)
        factor = 0
        for mask in range(1 << len(optional)):
            deleted = {optional[i] for i in range(len(optional)) if mask >> i & 1}
            if is_tree(block_vertices - deleted, block_edges):
                factor += 1
        factors.append(factor)
        product *= factor
    return product, tuple(sorted(factors))


def direct_count(blue, green, edges):
    total = 0
    witnesses = []
    for mask in range(1 << len(green)):
        chosen = {green[i] for i in range(len(green)) if mask >> i & 1}
        vertices = set(blue) | chosen
        if is_tree(vertices, edges):
            total += 1
            witnesses.append(tuple(sorted(set(green) - chosen)))
    return total, tuple(witnesses)


def audit_box(a, b):
    blue = tuple(range(a))
    green = tuple(range(a, a + b))
    possible = [(u, v) for u in blue for v in green]
    accepted = cactus_zero = cactus_witness_total = 0
    general = general_zero = general_witness_total = 0
    records = []
    for mask in range(1 << len(possible)):
        edges = [possible[i] for i in range(len(possible)) if mask >> i & 1]
        degrees = {v: 0 for v in blue + green}
        for u, v in edges:
            degrees[u] += 1
            degrees[v] += 1
        if min(degrees.values(), default=0) < 2:
            continue
        if not connected(blue + green, edges):
            continue
        direct, witnesses = direct_count(blue, green, edges)
        general_pred, general_factors = block_product(blue, green, edges)
        assert direct == general_pred
        general += 1
        general_zero += general_pred == 0
        general_witness_total += direct

        cs = cactus_blocks(blue + green, edges)
        if cs is None:
            records.append((a, b, tuple(edges), general_factors, direct, False))
            continue
        # A separate simple-cycle routine agrees on every accepted cactus.
        assert {frozenset(c) for c in cycles(blue + green, edges)} == {
            frozenset(c) for c in cs
        }
        pred, factors = predicted_count(blue, green, edges)
        assert direct == pred
        # Check the structural certificate, not only the aggregate count.
        cycle_sets = [set(c) for c in cs]
        for deleted in witnesses:
            assert len(deleted) == len(cs)
            assert all(sum(v in deleted for v in c) == 1 for c in cycle_sets)
            assert all(degrees[v] == 2 for v in deleted)
            assert all(not is_cut_vertex(blue + green, edges, v) for v in deleted)
        accepted += 1
        cactus_zero += pred == 0
        cactus_witness_total += direct
        records.append((a, b, tuple(edges), general_factors, factors, direct, True))
    return {
        "blue": a,
        "green": b,
        "connected_min_degree_two": general,
        "general_zero_products": general_zero,
        "general_induced_trees": general_witness_total,
        "labeled_cacti": accepted,
        "cactus_zero_products": cactus_zero,
        "cactus_induced_trees": cactus_witness_total,
    }, records


def main():
    boxes = []
    all_records = []
    for a in range(2, 5):
        for b in range(2, 5):
            box, records = audit_box(a, b)
            boxes.append(box)
            all_records.extend(records)

    # Positive hand controls: C4 has two choices; two C4s sharing a blue
    # cut vertex have four independent choices.
    c4_edges = [(0, 2), (0, 3), (1, 2), (1, 3)]
    assert predicted_count((0, 1), (2, 3), c4_edges)[0] == 2
    assert direct_count((0, 1), (2, 3), c4_edges)[0] == 2
    fig8_blue = (0, 1, 2)
    fig8_green = (3, 4, 5, 6)
    fig8_edges = [
        (0, 3), (1, 3), (0, 4), (1, 4),
        (0, 5), (2, 5), (0, 6), (2, 6),
    ]
    assert predicted_count(fig8_blue, fig8_green, fig8_edges)[0] == 4
    assert direct_count(fig8_blue, fig8_green, fig8_edges)[0] == 4
    assert block_product(fig8_blue, fig8_green, fig8_edges)[0] == 4

    # A central C4 whose two green vertices are articulation vertices has a
    # zero central factor, even though both leaf-cycle factors are positive.
    zero_blue = (0, 1, 2, 3, 4, 5)
    zero_green = (6, 7, 8, 9)
    zero_edges = [
        (0, 6), (1, 6), (0, 7), (1, 7),
        (2, 6), (3, 6), (2, 8), (3, 8),
        (4, 7), (5, 7), (4, 9), (5, 9),
    ]
    assert predicted_count(zero_blue, zero_green, zero_edges)[0] == 0
    assert direct_count(zero_blue, zero_green, zero_edges)[0] == 0
    assert block_product(zero_blue, zero_green, zero_edges)[0] == 0

    # Negative controls: K2,3 is not a cactus, and disconnectivity is
    # rejected before the theorem is applied.
    try:
        predicted_count((0, 1), (2, 3, 4),
                        [(u, v) for u in (0, 1) for v in (2, 3, 4)])
    except ValueError:
        pass
    else:
        raise AssertionError("theta control accepted as cactus")
    assert not connected((0, 1, 2, 3), [(0, 2), (1, 3)])

    digest = hashlib.sha256(
        repr(all_records).encode("utf-8")
    ).hexdigest()
    result = {
        "boxes": boxes,
        "controls": {
            "C4_product": 2,
            "blue_cut_figure_eight_product": 4,
            "green_cut_zero_product": 0,
            "theta_rejected": True,
            "disconnected_rejected": True,
        },
        "record_digest_sha256": digest,
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
