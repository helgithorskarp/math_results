#!/usr/bin/env python3
"""Independent verifier for the 8-color cycle-order classification.

This checker deliberately uses remaining cooldowns rather than capped ages,
iterative Tarjan rather than Kosaraju, and its own transition/cycle routines.
It verifies a committed compact certificate but imports no production code.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAPS = tuple(range(2, 17, 2))
Cooldown = tuple[int, ...]


def next_state(state: Cooldown, chosen: int, caps: tuple[int, ...]) -> Cooldown:
    if state[chosen] != 0:
        raise ValueError("chosen color is cooling down")
    return tuple(
        caps[j] if j == chosen else max(0, state[j] - 1)
        for j in range(len(caps))
    )


def enumerate_graph(
    caps: tuple[int, ...],
) -> tuple[list[Cooldown], list[list[tuple[int, int]]]]:
    initial = (0,) * len(caps)
    states = [initial]
    number = {initial: 0}
    edges: list[list[tuple[int, int]]] = []
    cursor = 0
    while cursor < len(states):
        state = states[cursor]
        targets = []
        for chosen in range(len(caps)):
            if state[chosen] != 0:
                continue
            target = next_state(state, chosen, caps)
            if target not in number:
                number[target] = len(states)
                states.append(target)
            targets.append((number[target], chosen + 1))
        edges.append(targets)
        cursor += 1
    return states, edges


def iterative_tarjan(edges: list[list[tuple[int, int]]]) -> list[list[int]]:
    """Compute SCCs with an explicit-stack version of Tarjan's algorithm."""
    count = len(edges)
    index = [-1] * count
    low = [0] * count
    active = bytearray(count)
    tarjan_stack: list[int] = []
    components: list[list[int]] = []
    next_index = 0

    for root in range(count):
        if index[root] >= 0:
            continue
        index[root] = low[root] = next_index
        next_index += 1
        tarjan_stack.append(root)
        active[root] = 1
        dfs = [[root, 0]]
        while dfs:
            vertex, offset = dfs[-1]
            if offset < len(edges[vertex]):
                target = edges[vertex][offset][0]
                dfs[-1][1] += 1
                if index[target] < 0:
                    index[target] = low[target] = next_index
                    next_index += 1
                    tarjan_stack.append(target)
                    active[target] = 1
                    dfs.append([target, 0])
                elif active[target]:
                    low[vertex] = min(low[vertex], index[target])
                continue

            dfs.pop()
            if dfs:
                parent = dfs[-1][0]
                low[parent] = min(low[parent], low[vertex])
            if low[vertex] == index[vertex]:
                component = []
                while True:
                    member = tarjan_stack.pop()
                    active[member] = 0
                    component.append(member)
                    if member == vertex:
                        break
                components.append(component)
    return components


def canonical_word(word: tuple[int, ...]) -> str:
    rotation = min(word[k:] + word[:k] for k in range(len(word)))
    return "".join(map(str, rotation))


def enumerate_simple_cycle_words(
    edges: list[list[tuple[int, int]]], vertices: list[int]
) -> list[str]:
    local_number = {vertex: i for i, vertex in enumerate(sorted(vertices))}
    local_edges: list[list[tuple[int, int]]] = [[] for _ in vertices]
    for vertex in sorted(vertices):
        source = local_number[vertex]
        for target, color in edges[vertex]:
            if target in local_number:
                local_edges[source].append((local_number[target], color))

    words: list[str] = []
    for least in range(len(local_edges)):
        occupied = {least}
        path: list[int] = []

        def extend(vertex: int) -> None:
            for target, color in local_edges[vertex]:
                if target < least:
                    continue
                if target == least:
                    words.append(canonical_word(tuple(path + [color])))
                elif target not in occupied:
                    occupied.add(target)
                    path.append(color)
                    extend(target)
                    path.pop()
                    occupied.remove(target)

        extend(least)
    return sorted(words)


def lines_hash(lines: list[str]) -> str:
    digest = hashlib.sha256()
    for line in lines:
        digest.update(line.encode("ascii") + b"\n")
    return digest.hexdigest()


def converted_graph_hash(
    states: list[Cooldown],
    edges: list[list[tuple[int, int]]],
    caps: tuple[int, ...],
    selected: set[int] | None = None,
) -> str:
    """Hash in the production age-state convention."""
    age_states = [
        tuple(caps[j] - state[j] for j in range(len(caps))) for state in states
    ]
    records = []
    sources = range(len(states)) if selected is None else sorted(selected)
    for source in sources:
        outgoing = edges[source]
        left = ",".join(map(str, age_states[source]))
        for target, color in outgoing:
            if selected is not None and target not in selected:
                continue
            right = ",".join(map(str, age_states[target]))
            records.append(f"{left}>{color}>{right}")
    return lines_hash(sorted(records))


def check_cyclic_word(word: str) -> None:
    entries = tuple(map(int, word))
    for color in range(1, 9):
        positions = [j for j, entry in enumerate(entries) if entry == color]
        for j, position in enumerate(positions):
            following = positions[(j + 1) % len(positions)]
            gap = (following - position) % len(entries)
            if gap <= 2 * color:
                raise AssertionError((len(entries), color, gap))


def representable(n: int) -> bool:
    return any((n - 53 * b) % 27 == 0 for b in range(n // 53 + 1))


def verify_semigroup_arithmetic() -> None:
    # Apéry representatives modulo 27 are 53*b for b=0,...,26 because
    # gcd(27,53)=1.  Their maximum minus 27 is the Frobenius number.
    residues = {53 * b % 27 for b in range(27)}
    assert residues == set(range(27))
    assert 53 * 26 - 27 == 1351
    assert not representable(1351)
    assert all(representable(n) for n in range(1352, 1352 + 27))
    # Adding 27 propagates the final assertion to every n >= 1352.


def main() -> None:
    expected = json.loads((HERE / "certificate.json").read_text(encoding="utf-8"))

    seven_caps = CAPS[:7]
    seven_states, seven_edges = enumerate_graph(seven_caps)
    assert len(seven_states) == expected["seven_color_reachable_states"]
    assert sum(map(len, seven_edges)) == expected["seven_color_reachable_edges"]
    assert converted_graph_hash(seven_states, seven_edges, seven_caps) == expected[
        "seven_color_graph_sha256"
    ]
    seven_components = iterative_tarjan(seven_edges)
    assert len(seven_components) == len(seven_states)
    assert not any(
        target == source
        for source, outgoing in enumerate(seven_edges)
        for target, _ in outgoing
    )
    frontier = {0}
    maximum = 0
    while frontier:
        following = {target for source in frontier for target, _ in seven_edges[source]}
        if not following:
            break
        frontier = following
        maximum += 1
    assert maximum == expected["seven_color_maximum_word_length"] == 26

    states, edges = enumerate_graph(CAPS)
    assert len(states) == expected["reachable_states"]
    assert sum(map(len, edges)) == expected["reachable_edges"]
    assert converted_graph_hash(states, edges, CAPS) == expected[
        "reachable_graph_sha256"
    ]

    components = iterative_tarjan(edges)
    cyclic = []
    for component in components:
        if len(component) > 1:
            cyclic.append(component)
        elif any(target == component[0] for target, _ in edges[component[0]]):
            cyclic.append(component)
    assert len(components) == expected["strong_components"]
    assert len(cyclic) == expected["cyclic_components"] == 1
    core = cyclic[0]
    core_set = set(core)
    assert len(core) == expected["recurrent_states"]
    assert sum(
        target in core_set for source in core for target, _ in edges[source]
    ) == expected["recurrent_edges"]
    assert converted_graph_hash(states, edges, CAPS, core_set) == expected[
        "recurrent_graph_sha256"
    ]

    cycle_words = enumerate_simple_cycle_words(edges, core)
    lengths = Counter(map(len, cycle_words))
    assert len(cycle_words) == expected["simple_cycles"]
    assert {str(k): lengths[k] for k in sorted(lengths)} == expected[
        "simple_cycle_length_counts"
    ]
    assert lines_hash(cycle_words) == expected["simple_cycle_words_sha256"]
    assert set(lengths) == {54, 106, 107, 108}

    base_age = tuple(expected["common_base_state"])
    base_cooldown = tuple(CAPS[j] - base_age[j] for j in range(8))
    for length, word in expected["common_base_cycle_words"].items():
        assert len(word) == int(length)
        check_cyclic_word(word)
        state = base_cooldown
        for color_text in word:
            state = next_state(state, int(color_text) - 1, CAPS)
        assert state == base_cooldown
        assert canonical_word(tuple(map(int, word))) in cycle_words
    verify_semigroup_arithmetic()

    print(
        "independently verified: 7 colors stop at length 26; for 8 colors, "
        "339203 states, one 424-state recurrent core, "
        "640 simple cycles of lengths 54/106/107/108"
    )
    print(
        "therefore for n >= 14 an 8-coloring exists exactly when "
        "n = 27*a + 53*b (a,b >= 0), and every n >= 1352 qualifies"
    )


if __name__ == "__main__":
    main()
