#!/usr/bin/env python3
"""Exhaust and certify the cubic Cayley cases on A5, S5, A6, and S6."""

from __future__ import annotations

from collections import deque
from itertools import combinations, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """Return p after q."""
    return tuple(p[i] for i in q)


def inverse(p: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * len(p)
    for i, j in enumerate(p):
        answer[j] = i
    return tuple(answer)


def is_even(p: tuple[int, ...]) -> bool:
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2 == 0


def inverse_closed_triples(elements: tuple[tuple[int, ...], ...]):
    identity = tuple(range(len(elements[0])))
    inverses = {x: inverse(x) for x in elements}
    involutions = tuple(x for x in elements if x != identity and inverses[x] == x)
    seen = {identity, *involutions}
    pairs = []
    for x in elements:
        if x in seen:
            continue
        pair = tuple(sorted((x, inverses[x])))
        pairs.append(pair)
        seen.update(pair)
    yield from combinations(involutions, 3)
    for a in involutions:
        for pair in pairs:
            yield tuple(sorted((a, *pair)))


def distances(right_maps, generators, order):
    maps = [right_maps[g] for g in generators]
    distance = [-1] * order
    distance[0] = 0
    queue = deque([0])
    while queue:
        x = queue.popleft()
        for mapping in maps:
            y = mapping[x]
            if distance[y] == -1:
                distance[y] = distance[x] + 1
                queue.append(y)
    return distance


def conjugate(c, g):
    return compose(compose(c, g), inverse(c))


def canonical(generators, conjugators):
    return min(tuple(sorted(conjugate(c, g) for g in generators)) for c in conjugators)


def boundary_signature(elements, right_maps, generators):
    distance = distances(right_maps, generators, len(elements))
    assert -1 not in distance
    sphere = tuple(x for x, d in zip(elements, distance) if d == 7)
    difference = {compose(x, inverse(y)) for x in sphere for y in sphere}
    compatible = tuple(x for x in elements if x not in difference)
    compatible_set = set(compatible)
    maximum_degree = 0
    for x in compatible:
        degree = sum(
            compose(inverse(x), y) in compatible_set
            for y in compatible
            if y != x
        )
        maximum_degree = max(maximum_degree, degree)
    return {
        "sphere_size": len(sphere),
        "diameter": max(distance),
        "difference_size": len(difference),
        "compatible_size": len(compatible),
        "maximum_compatible_degree": maximum_degree,
    }


def run_group(name, expected):
    n = expected["n"]
    symmetric = tuple(permutations(range(n)))
    elements = tuple(x for x in symmetric if not expected["alternating"] or is_even(x))
    identity = tuple(range(n))
    assert elements[0] == identity
    index = {x: i for i, x in enumerate(elements)}
    right_maps = {
        g: tuple(index[compose(x, g)] for x in elements)
        for g in elements
        if g != identity
    }
    total = connected = four = six = 0
    class_counts = {}
    for generators in inverse_closed_triples(elements):
        total += 1
        distance = distances(right_maps, generators, len(elements))
        if -1 in distance:
            continue
        connected += 1
        sphere_size = distance.count(7)
        candidate = False
        if 4 * sphere_size == len(elements):
            four += 1
            candidate = True
        if 6 * sphere_size == len(elements):
            six += 1
            candidate = True
        if candidate:
            key = canonical(generators, symmetric)
            class_counts[key] = class_counts.get(key, 0) + 1

    observed = {
        "total_inverse_closed_triples": total,
        "connected_triples": connected,
        "four_center_candidates": four,
        "six_center_candidates": six,
    }
    for key, value in observed.items():
        assert value == expected[key], (name, key, value, expected[key])

    expected_reps = {
        tuple(tuple(g) for g in item["generators"]): item
        for item in expected["representatives"]
    }
    assert set(class_counts) == set(expected_reps), (name, set(class_counts), set(expected_reps))
    for generators, count in class_counts.items():
        item = expected_reps[generators]
        assert count == item["orbit_size"], (name, count, item["orbit_size"])
        signature = boundary_signature(elements, right_maps, generators)
        for key, value in signature.items():
            assert value == item[key], (name, key, value, item[key])

    print(
        f"{name} total={total} connected={connected} "
        f"k4_candidates={four} k6_candidates={six} classes={len(class_counts)}"
    )
    for i, generators in enumerate(sorted(class_counts)):
        sig = boundary_signature(elements, right_maps, generators)
        print(
            f"  {name}.{i} orbit={class_counts[generators]} "
            f"|T|={sig['sphere_size']} diameter={sig['diameter']} "
            f"|TT^-1|={sig['difference_size']} |A|={sig['compatible_size']} "
            f"maxdeg(A)={sig['maximum_compatible_degree']}"
        )


def main():
    data = json.loads((HERE / "certificates.json").read_text())
    for name in ("A5", "S5", "A6", "S6"):
        run_group(name, data[name])
    print("all exhaustive classification assertions passed")


if __name__ == "__main__":
    main()
