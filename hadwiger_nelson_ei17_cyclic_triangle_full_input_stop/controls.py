#!/usr/bin/env python3
"""Independent controls for the EI17 cyclic-triangle stopping computation."""

from __future__ import annotations

from collections import Counter
import json

import verify as V


def independent_source_orbit_count(edges):
    """Fixed vertex order, unlike the DSATUR-style order in verify.py."""
    adjacency = [set() for _ in range(17)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colour = [-1] * 17
    leaves = 0
    nodes = 0

    def visit(vertex, maximum):
        nonlocal leaves, nodes
        nodes += 1
        if vertex == 17:
            if maximum == 3:
                leaves += 1
            return
        forbidden = {colour[w] for w in adjacency[vertex] if w < vertex}
        for value in range(min(3, maximum + 1) + 1):
            if value not in forbidden:
                colour[vertex] = value
                visit(vertex + 1, max(maximum, value))
        colour[vertex] = -1

    visit(0, -1)
    return leaves, nodes


def independent_extension(domains, adjacency):
    """Simple recursive colouring, deliberately separate from verify.py's solver."""
    domains = list(domains)
    assigned = [-1] * len(domains)

    def visit():
        choices = [v for v in range(len(domains)) if assigned[v] < 0]
        if not choices:
            return tuple(assigned)
        vertex = min(
            choices,
            key=lambda v: (
                sum(assigned[w] < 0 for w in adjacency[v]),
                -sum(assigned[w] >= 0 for w in adjacency[v]),
                v,
            ),
        )
        mask = domains[vertex]
        for neighbour in adjacency[vertex]:
            if assigned[neighbour] >= 0:
                mask &= ~(1 << assigned[neighbour])
        while mask:
            bit = mask & -mask
            mask -= bit
            assigned[vertex] = bit.bit_length() - 1
            answer = visit()
            if answer is not None:
                return answer
        assigned[vertex] = -1
        return None

    return visit()


def contactful_domain_controls(graph, colourings):
    base = graph["addresses"][0]
    base_at = {physical: source for source, physical in enumerate(base)}
    new_vertices = tuple(v for v in range(48) if v not in base_at)
    new_at = {physical: local for local, physical in enumerate(new_vertices)}
    adjacency = [set() for _ in new_vertices]
    base_neighbours = [[] for _ in new_vertices]
    for a, b in graph["edges"]:
        for left, right in ((a, b), (b, a)):
            if left in new_at:
                if right in new_at:
                    adjacency[new_at[left]].add(new_at[right])
                else:
                    base_neighbours[new_at[left]].append(base_at[right])

    states = set()
    for word in colourings:
        domains = []
        for neighbours in base_neighbours:
            forbidden = sum(1 << colour for colour in {word[v] for v in neighbours})
            domains.append(15 & ~forbidden)
        states.add(tuple(domains))

    for domains in states:
        answer = independent_extension(domains, adjacency)
        V.require(answer is not None, "independent solver rejected a claimed extending state")
        V.require(all(domains[v] & (1 << answer[v]) for v in range(len(answer))),
                  "independent witness violates a base domain")
        V.require(all(answer[v] != answer[w] for v in range(len(answer)) for w in adjacency[v] if v < w),
                  "independent witness violates a new--new edge")
    return len(states)


def expect_failure(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError("corrupted control was accepted")


def run():
    points, _ = V.seed.certify()
    edges = tuple(map(tuple, json.loads((V.SOURCE / "seed_edges.json").read_text())))
    colourings = V.enumerate_source_colourings(edges)

    independent_orbits, independent_nodes = independent_source_orbit_count(edges)
    V.require(independent_orbits == len(colourings) == 85088,
              "independent source-colouring enumeration disagrees")

    graphs = [
        V.build_conservative_graph(points, edges, edge, reverse, reflected)
        for edge in edges
        for reverse in (False, True)
        for reflected in (False, True)
    ]
    contactful = [graph for graph in graphs if graph["extra_edges"]]
    state_histogram = Counter(contactful_domain_controls(graph, colourings) for graph in contactful)
    V.require(state_histogram == {27: 4, 39: 4}, "independent domain-state census disagrees")

    plain = next(graph for graph in graphs if not graph["extra_edges"])
    corrupted = dict(plain)
    witness = V.structural_extension(colourings[0], plain)
    equal_pair = next((a, b) for a in range(48) for b in range(a + 1, 48)
                      if witness[a] == witness[b])
    corrupted["edges"] = tuple(sorted(plain["edges"] + (equal_pair,)))
    expect_failure(lambda: V.structural_extension(colourings[0], corrupted))

    a = V.exact_point(0, 0)
    b = V.exact_point(1, 0)
    half = V.I.rational(V.F(1, 2))
    zeta = (-half, V.I.rational(3).sqrt() * half)
    c = (half, V.I.rational(3).sqrt() * half)
    triangle = (a, b, c)
    cyclic_images = tuple(V.cyclic_map(point, zeta) for point in triangle)
    for actual, target in zip(cyclic_images, (b, c, a)):
        V.require(not V.separated(actual[0], target[0]) and not V.separated(actual[1], target[1]),
                  "cyclic map missed an equilateral vertex")
    for left, right in ((a, b), (b, c), (c, a)):
        V.require(V.intervals.squared_distance(left, right).contains(1),
                  "equilateral side does not enclose unit distance")

    return {
        "verified": True,
        "independent_fixed_order_source_orbits": independent_orbits,
        "independent_fixed_order_search_nodes": independent_nodes,
        "contactful_frames_rechecked": len(contactful),
        "independent_initial_domain_state_histogram": dict(sorted(state_histogram.items())),
        "corrupted_structural_witness_rejected": True,
        "equilateral_cyclic_map_checked": True,
        "normal_assertions_not_required": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
