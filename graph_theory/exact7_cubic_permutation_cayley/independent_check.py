#!/usr/bin/env python3
"""Independent orbit-coverage and translate-obstruction audit."""

from __future__ import annotations

from itertools import combinations, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def multiply(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    q = [None] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def even(p):
    seen = set()
    cycles = 0
    for i in range(len(p)):
        if i in seen:
            continue
        cycles += 1
        j = i
        while j not in seen:
            seen.add(j)
            j = p[j]
    return (len(p) - cycles) % 2 == 0


def triples(group):
    identity = tuple(range(len(group[0])))
    involutions = [x for x in group if x != identity and multiply(x, x) == identity]
    inverse_pairs = []
    used = {identity, *involutions}
    for x in group:
        if x not in used:
            pair = frozenset((x, inv(x)))
            inverse_pairs.append(pair)
            used.update(pair)
    answer = [frozenset(x) for x in combinations(involutions, 3)]
    answer += [frozenset((a, *pair)) for a in involutions for pair in inverse_pairs]
    assert len(answer) == len(set(answer))
    return answer


def layers(order, generators, right_maps):
    reached = {0}
    layer = {0}
    result = [{0}]
    while layer:
        next_layer = {
            right_maps[g][x]
            for x in layer
            for g in generators
        } - reached
        if not next_layer:
            break
        reached.update(next_layer)
        layer = next_layer
        result.append(layer)
    return result, reached


def conjugacy_orbit(rep, symmetric):
    result = set()
    for c in symmetric:
        ci = inv(c)
        result.add(frozenset(multiply(multiply(c, g), ci) for g in rep))
    return result


def audit(name, spec):
    n = spec["n"]
    symmetric = tuple(permutations(range(n)))
    group = tuple(x for x in symmetric if not spec["alternating"] or even(x))
    identity = tuple(range(n))
    assert group[0] == identity
    index = {x: i for i, x in enumerate(group)}
    right_maps = {
        g: tuple(index[multiply(x, g)] for x in group)
        for g in group
        if g != identity
    }
    representatives = [
        frozenset(tuple(g) for g in item["generators"])
        for item in spec["representatives"]
    ]
    orbits = [conjugacy_orbit(rep, symmetric) for rep in representatives]
    assert all(len(orbit) == item["orbit_size"] for orbit, item in zip(orbits, spec["representatives"]))
    assert all(orbits[i].isdisjoint(orbits[j]) for i in range(len(orbits)) for j in range(i))

    total = connected = four = six = 0
    hits = [0] * len(orbits)
    for generators in triples(group):
        total += 1
        distance_layers, reached = layers(len(group), generators, right_maps)
        if len(reached) != len(group):
            continue
        connected += 1
        sphere_size = len(distance_layers[7]) if len(distance_layers) > 7 else 0
        if 4 * sphere_size == len(group):
            four += 1
        if 6 * sphere_size == len(group):
            six += 1
        if 4 * sphere_size == len(group) or 6 * sphere_size == len(group):
            memberships = [i for i, orbit in enumerate(orbits) if generators in orbit]
            assert len(memberships) == 1, (name, generators, memberships)
            hits[memberships[0]] += 1

    assert total == spec["total_inverse_closed_triples"]
    assert connected == spec["connected_triples"]
    assert four == spec["four_center_candidates"]
    assert six == spec["six_center_candidates"]
    assert hits == [item["orbit_size"] for item in spec["representatives"]]

    for rep, item in zip(representatives, spec["representatives"]):
        distance_layers, reached = layers(len(group), rep, right_maps)
        assert len(reached) == len(group)
        sphere = {group[i] for i in distance_layers[7]}
        difference = {multiply(x, inv(y)) for x in sphere for y in sphere}
        compatible = set(group) - difference
        degrees = [
            sum(multiply(inv(x), y) in compatible for y in compatible if y != x)
            for x in compatible
        ]
        assert len(sphere) == item["sphere_size"]
        assert len(distance_layers) - 1 == item["diameter"]
        assert len(difference) == item["difference_size"]
        assert len(compatible) == item["compatible_size"]
        assert max(degrees, default=0) == item["maximum_compatible_degree"]
        # Six centers would require a 5-clique among the shifts compatible
        # with the normalized identity translate.  Maximum degree <= 2 rules
        # this out without trusting an exact-cover implementation.
        assert max(degrees, default=0) < 4

    print(f"{name} independent orbit coverage and boundary audit passed")


def main():
    data = json.loads((HERE / "certificates.json").read_text())
    for name in ("A5", "S5", "A6", "S6"):
        audit(name, data[name])
    print("all independent assertions passed")


if __name__ == "__main__":
    main()
