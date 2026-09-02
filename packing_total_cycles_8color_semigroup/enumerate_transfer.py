#!/usr/bin/env python3
"""Exact transfer-graph proof computation for packing-total colorings of cycles.

The colors are 1,...,8.  After color i is used, another i is forbidden for
the next 2*i positions.  A state records, for every color, the capped age of
its most recent occurrence.  The all-saturated state accepts every finite
valid word, so every periodic valid word occurs in the reachable graph.

This production implementation uses Kosaraju's algorithm for SCCs and an
exhaustive least-vertex DFS for simple directed cycles.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import reduce
from pathlib import Path
from typing import Iterable


CAPS = tuple(range(2, 17, 2))
State = tuple[int, ...]


def step(state: State, color: int) -> State:
    """Append a one-based color to an age state."""
    chosen = color - 1
    if state[chosen] != CAPS[chosen]:
        raise ValueError(f"color {color} is unavailable in state {state}")
    return tuple(
        0 if j == chosen else min(state[j] + 1, CAPS[j])
        for j in range(8)
    )


def reachable_graph() -> tuple[list[State], list[list[tuple[int, int]]]]:
    """Enumerate every state reachable from the unconstrained initial state."""
    states: list[State] = [CAPS]
    index = {CAPS: 0}
    adjacency: list[list[tuple[int, int]]] = []

    for state in states:
        outgoing: list[tuple[int, int]] = []
        for color, cap in enumerate(CAPS, start=1):
            if state[color - 1] != cap:
                continue
            target = step(state, color)
            target_index = index.get(target)
            if target_index is None:
                target_index = len(states)
                index[target] = target_index
                states.append(target)
            outgoing.append((target_index, color))
        adjacency.append(outgoing)
    return states, adjacency


def seven_color_graph() -> tuple[list[State], list[list[tuple[int, int]]]]:
    """Independently enumerate line words over colors 1,...,7."""
    caps = CAPS[:7]
    states: list[State] = [caps]
    index = {caps: 0}
    adjacency: list[list[tuple[int, int]]] = []
    for state in states:
        outgoing = []
        for chosen, cap in enumerate(caps):
            if state[chosen] != cap:
                continue
            target = tuple(
                0 if j == chosen else min(state[j] + 1, caps[j])
                for j in range(7)
            )
            if target not in index:
                index[target] = len(states)
                states.append(target)
            outgoing.append((index[target], chosen + 1))
        adjacency.append(outgoing)
    return states, adjacency


def maximum_word_length(adjacency: list[list[tuple[int, int]]]) -> int:
    """Return the last nonempty exact-length layer from initial state zero."""
    frontier = {0}
    length = 0
    while frontier:
        following = {
            target for source in frontier for target, _ in adjacency[source]
        }
        if not following:
            return length
        frontier = following
        length += 1
    raise AssertionError("unreachable")


def kosaraju_components(
    adjacency: list[list[tuple[int, int]]],
) -> tuple[list[int], list[int]]:
    """Return component labels and component sizes without recursion."""
    count = len(adjacency)
    reverse: list[list[int]] = [[] for _ in range(count)]
    for source, outgoing in enumerate(adjacency):
        for target, _ in outgoing:
            reverse[target].append(source)

    seen = bytearray(count)
    finishing_order: list[int] = []
    for root in range(count):
        if seen[root]:
            continue
        seen[root] = 1
        stack = [(root, 0)]
        while stack:
            vertex, offset = stack[-1]
            if offset < len(adjacency[vertex]):
                target = adjacency[vertex][offset][0]
                stack[-1] = (vertex, offset + 1)
                if not seen[target]:
                    seen[target] = 1
                    stack.append((target, 0))
            else:
                finishing_order.append(vertex)
                stack.pop()

    component = [-1] * count
    sizes: list[int] = []
    for root in reversed(finishing_order):
        if component[root] >= 0:
            continue
        label = len(sizes)
        size = 0
        component[root] = label
        stack = [root]
        while stack:
            vertex = stack.pop()
            size += 1
            for source in reverse[vertex]:
                if component[source] < 0:
                    component[source] = label
                    stack.append(source)
        sizes.append(size)
    return component, sizes


def recurrent_core(
    states: list[State], adjacency: list[list[tuple[int, int]]]
) -> tuple[list[State], list[list[tuple[int, int]]], int, list[int]]:
    """Extract all vertices in nontrivial SCCs or singleton self-loops."""
    component, sizes = kosaraju_components(adjacency)
    cyclic_labels = {
        label for label, size in enumerate(sizes) if size > 1
    }
    for vertex, outgoing in enumerate(adjacency):
        if any(target == vertex for target, _ in outgoing):
            cyclic_labels.add(component[vertex])

    vertices = [
        vertex for vertex, label in enumerate(component) if label in cyclic_labels
    ]
    local = {vertex: offset for offset, vertex in enumerate(vertices)}
    core_states = [states[vertex] for vertex in vertices]
    core_adjacency: list[list[tuple[int, int]]] = []
    for vertex in vertices:
        core_adjacency.append(
            [
                (local[target], color)
                for target, color in adjacency[vertex]
                if target in local
            ]
        )
    return core_states, core_adjacency, len(sizes), sorted(cyclic_labels)


def canonical_rotation(word: tuple[int, ...]) -> tuple[int, ...]:
    return min(word[offset:] + word[:offset] for offset in range(len(word)))


def simple_cycles(
    adjacency: list[list[tuple[int, int]]],
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Enumerate each simple directed cycle once at its least vertex."""
    cycles: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for root in range(len(adjacency)):
        visited = {root}
        path_vertices = [root]
        path_colors: list[int] = []

        def visit(vertex: int) -> None:
            for target, color in adjacency[vertex]:
                if target < root:
                    continue
                if target == root:
                    cycles.append(
                        (tuple(path_vertices), tuple(path_colors + [color]))
                    )
                elif target not in visited:
                    visited.add(target)
                    path_vertices.append(target)
                    path_colors.append(color)
                    visit(target)
                    path_colors.pop()
                    path_vertices.pop()
                    visited.remove(target)

        visit(root)
    return cycles


def record_hash(lines: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for line in lines:
        digest.update(line.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def graph_hash(
    states: list[State], adjacency: list[list[tuple[int, int]]]
) -> str:
    records = []
    for source, outgoing in enumerate(adjacency):
        source_text = ",".join(map(str, states[source]))
        for target, color in outgoing:
            target_text = ",".join(map(str, states[target]))
            records.append(f"{source_text}>{color}>{target_text}")
    return record_hash(sorted(records))


def trace_word(state: State, word: Iterable[int]) -> State:
    for color in word:
        state = step(state, color)
    return state


def cyclic_gaps(word: tuple[int, ...], color: int) -> list[int]:
    positions = [position for position, entry in enumerate(word) if entry == color]
    if not positions:
        return []
    return [
        positions[(j + 1) % len(positions)] - positions[j]
        if j + 1 < len(positions)
        else positions[0] + len(word) - positions[j]
        for j in range(len(positions))
    ]


def build_certificate() -> dict[str, object]:
    seven_states, seven_adjacency = seven_color_graph()
    seven_component, seven_sizes = kosaraju_components(seven_adjacency)
    if any(size > 1 for size in seven_sizes):
        raise AssertionError("the seven-color graph unexpectedly contains a cycle")
    if any(target == source for source, outgoing in enumerate(seven_adjacency) for target, _ in outgoing):
        raise AssertionError("the seven-color graph unexpectedly contains a self-loop")
    del seven_component

    states, adjacency = reachable_graph()
    core_states, core_adjacency, component_count, cyclic_labels = recurrent_core(
        states, adjacency
    )
    cycles = simple_cycles(core_adjacency)
    cycle_words = sorted(canonical_rotation(word) for _, word in cycles)
    length_counts = Counter(map(len, cycle_words))

    words_by_length: dict[int, list[tuple[tuple[int, ...], tuple[int, ...]]]] = {}
    for vertices, word in cycles:
        words_by_length.setdefault(len(word), []).append((vertices, word))
    common_vertices = reduce(
        set.intersection,
        (
            set().union(*(set(vertices) for vertices, _ in words_by_length[length]))
            for length in (54, 106, 107)
        ),
    )
    base = min(common_vertices, key=core_states.__getitem__)
    generator_words: dict[str, str] = {}
    for length in (54, 106, 107):
        rotations = []
        for vertices, word in words_by_length[length]:
            if base not in vertices:
                continue
            offset = vertices.index(base)
            rotations.append(word[offset:] + word[:offset])
        generator_words[str(length)] = "".join(map(str, min(rotations)))

    for length_text, word_text in generator_words.items():
        word = tuple(map(int, word_text))
        if len(word) != int(length_text):
            raise AssertionError("word length mismatch")
        if trace_word(core_states[base], word) != core_states[base]:
            raise AssertionError("generator word is not closed at the base state")
        for color in range(1, 9):
            if any(gap <= 2 * color for gap in cyclic_gaps(word, color)):
                raise AssertionError("invalid cyclic generator word")

    return {
        "schema": "packing-total-8-transfer-v1",
        "colors": list(range(1, 9)),
        "cooldown_caps": list(CAPS),
        "seven_color_reachable_states": len(seven_states),
        "seven_color_reachable_edges": sum(map(len, seven_adjacency)),
        "seven_color_graph_sha256": graph_hash(seven_states, seven_adjacency),
        "seven_color_maximum_word_length": maximum_word_length(seven_adjacency),
        "reachable_states": len(states),
        "reachable_edges": sum(map(len, adjacency)),
        "strong_components": component_count,
        "cyclic_components": len(cyclic_labels),
        "recurrent_states": len(core_states),
        "recurrent_edges": sum(map(len, core_adjacency)),
        "reachable_graph_sha256": graph_hash(states, adjacency),
        "recurrent_graph_sha256": graph_hash(core_states, core_adjacency),
        "simple_cycles": len(cycle_words),
        "simple_cycle_length_counts": {
            str(length): length_counts[length] for length in sorted(length_counts)
        },
        "simple_cycle_words_sha256": record_hash(
            "".join(map(str, word)) for word in cycle_words
        ),
        "common_base_state": list(core_states[base]),
        "common_base_cycle_words": generator_words,
        "closed_walk_length_semigroup": [54, 106, 107],
        "even_half_length_semigroup": [27, 53],
        "largest_nonrepresentable_cycle_order": 1351,
        "all_cycle_orders_from": 1352,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    rendered = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.check is not None:
        expected = args.check.read_text(encoding="utf-8")
        if rendered != expected:
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"verified production certificate: {args.check}")
    elif args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
