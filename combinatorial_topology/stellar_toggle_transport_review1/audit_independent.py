#!/usr/bin/env python3
"""Independent exact audit of stellar toggle-word transport.

This checker does not import the target compiler.  Complexes and game states
are integer bit sets, while local macros are found by dynamic programming over
all one-use generator subsets rather than by the target clearing recurrence.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from collections import Counter, deque
from functools import lru_cache
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "stellar_toggle_transport"
COUNTS: Counter[str] = Counter()
DIGEST = hashlib.sha256()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def subfaces(face: int) -> tuple[int, ...]:
    values = []
    part = face
    while True:
        values.append(part)
        if part == 0:
            return tuple(values)
        part = (part - 1) & face


def closure(facets: tuple[int, ...] | list[int]) -> frozenset[int]:
    return frozenset({0}.union(*(subfaces(f) for f in facets)))


def is_subset(a: int, b: int) -> bool:
    return a & b == a


def upper_mu(complex_: frozenset[int]) -> dict[int, int]:
    """Upper Mobius values by the alternating Boolean coface formula."""
    return {
        f: -sum(
            (-1) ** (g.bit_count() - f.bit_count())
            for g in complex_
            if is_subset(f, g)
        )
        for f in complex_
    }


def all_four_label_complexes() -> tuple[frozenset[int], ...]:
    """Generate complexes as closures of all facet selections, then dedupe."""
    candidates = tuple(range(1, 16))
    closed = {frozenset({0})}
    for selection in range(1, 1 << len(candidates)):
        facets = tuple(candidates[i] for i in range(15) if selection >> i & 1)
        closed.add(closure(facets))
    return tuple(sorted(closed, key=lambda k: (len(k), tuple(sorted(k)))))


def stellar(complex_: frozenset[int], sigma: int, new_bit: int) -> frozenset[int]:
    require(sigma and sigma in complex_, "invalid stellar face")
    require(new_bit > 0 and new_bit & (new_bit - 1) == 0, "new label is not one bit")
    require(all(not f & new_bit for f in complex_), "new label is not fresh")
    result = {f for f in complex_ if not is_subset(sigma, f)}
    for carrier in complex_:
        if is_subset(sigma, carrier):
            outside = carrier ^ sigma
            for a in subfaces(sigma):
                if a != sigma:
                    result.add(new_bit | outside | a)
    return frozenset(result)


def replay(
    complex_: frozenset[int], word: tuple[int, ...] | list[int], start: int = 0
) -> tuple[int, Counter[int], Counter[int]]:
    faces = tuple(sorted(complex_))
    index = {f: i for i, f in enumerate(faces)}
    mu = upper_mu(complex_)
    full = (1 << len(faces)) - 1
    require(start & ~full == 0, "state uses an absent face")
    state = start
    uses: Counter[int] = Counter()
    signed: Counter[int] = Counter()
    for generator in word:
        require(generator in index and mu[generator], "forbidden generator")
        ideal = sum(1 << i for i, face in enumerate(faces) if is_subset(face, generator))
        color = state & ideal
        require(color in (0, ideal), "nonmonochromatic ideal")
        signed[generator] += 1 if color == 0 else -1
        uses[generator] += 1
        state ^= ideal
        COUNTS["replayed_moves"] += 1
    return state, uses, signed


@lru_cache(maxsize=None)
def search_local_macro(s: int, c: int) -> tuple[tuple[int, ...], int]:
    """Find and count all legal orders using each fiber generator once."""
    require(1 <= s <= 4 and c >= 1, "local exhaustive range")
    sigma = (1 << s) - 1
    common = ((1 << c) - 1) << s
    sigma_bits = tuple(1 << i for i in range(s))
    facets = tuple(common | (sigma ^ bit) for bit in sigma_bits)
    complex_ = closure(facets)
    faces = tuple(sorted(complex_))
    generators = tuple(common | a for a in subfaces(sigma) if a != sigma)
    ideals = tuple(
        sum(1 << i for i, face in enumerate(faces) if is_subset(face, generator))
        for generator in generators
    )
    n = len(generators)
    states = [0] * (1 << n)
    for mask in range(1, 1 << n):
        bit = mask & -mask
        i = bit.bit_length() - 1
        states[mask] = states[mask ^ bit] ^ ideals[i]
    ways = [0] * (1 << n)
    ways[0] = 1
    parent: dict[int, tuple[int, int]] = {}
    for used in range(1 << n):
        if ways[used] == 0:
            continue
        state = states[used]
        for i, ideal in enumerate(ideals):
            if used >> i & 1 or state & ideal not in (0, ideal):
                continue
            nxt = used | (1 << i)
            ways[nxt] += ways[used]
            parent.setdefault(nxt, (used, i))
    full_generators = (1 << n) - 1
    full_faces = (1 << len(faces)) - 1
    require(states[full_generators] == full_faces, "fiber XOR is not the whole local complex")
    require(ways[full_generators] > 0, "no one-use local macro")
    order = []
    cursor = full_generators
    while cursor:
        previous, i = parent[cursor]
        order.append(generators[i] ^ common)
        cursor = previous
    order.reverse()
    actual = tuple(common | a for a in order)
    state, uses, _ = replay(complex_, actual)
    require(state == full_faces and set(uses.values()) == {1}, "bad local search witness")
    COUNTS["local_searches"] += 1
    COUNTS["local_dp_subsets"] += 1 << n
    return tuple(order), ways[full_generators]


def map_local_order(order: tuple[int, ...], sigma: int, common: int) -> tuple[int, ...]:
    actual_bits = tuple(1 << i for i in range(sigma.bit_length()) if sigma >> i & 1)
    result = []
    for abstract in order:
        a = 0
        for i, bit in enumerate(actual_bits):
            if abstract >> i & 1:
                a |= bit
        result.append(common | a)
    return tuple(result)


def carrier(face: int, sigma: int, new_bit: int) -> int:
    return face if not face & new_bit else (face ^ new_bit) | sigma


def audit_stellar_case(complex_: frozenset[int], sigma: int) -> None:
    new_bit = 16
    subdiv = stellar(complex_, sigma, new_bit)
    old_mu = upper_mu(complex_)
    new_mu = upper_mu(subdiv)
    s = sigma.bit_count()
    for face in subdiv:
        if face & new_bit:
            old = carrier(face, sigma, new_bit)
            exponent = s - (face & sigma).bit_count() - 1
            expected = (-1) ** exponent * old_mu[old]
            if expected and (expected > 0) != (old_mu[old] > 0):
                COUNTS["fiber_sign_flips"] += 1
        else:
            expected = old_mu[face]
        require(new_mu[face] == expected, "Mobius transport failed")
        COUNTS["mobius_transport_faces"] += 1

    for old_face in complex_:
        preimage = {
            face for face in subdiv
            if is_subset(carrier(face, sigma, new_bit), old_face)
        }
        if not is_subset(sigma, old_face):
            expected = set(subfaces(old_face))
            require(preimage == expected, "unaffected carrier preimage failed")
            COUNTS["unaffected_preimages"] += 1
            continue
        outside = old_face ^ sigma
        common = new_bit | outside
        facets = tuple(common | (sigma ^ bit)
                       for bit in (1 << i for i in range(sigma.bit_length()) if sigma >> i & 1))
        local = closure(facets)
        require(preimage == set(local), "affected carrier preimage failed")
        COUNTS["affected_preimages"] += 1
        if old_mu[old_face] == 0:
            COUNTS["zero_mobius_affected_faces"] += 1
            continue
        c = common.bit_count()
        abstract_order, _ = search_local_macro(s, c)
        block = map_local_order(abstract_order, sigma, common)
        require(all(new_mu[g] for g in block), "local block requests zero Mobius")
        faces = tuple(sorted(subdiv))
        local_state = sum(1 << i for i, f in enumerate(faces) if f in local)
        after_add, uses, _ = replay(subdiv, block)
        require(after_add == local_state and set(uses.values()) == {1}, "addition block failed")
        after_remove, _, _ = replay(subdiv, tuple(reversed(block)), start=local_state)
        require(after_remove == 0, "removal block failed")
        COUNTS["audited_addition_blocks"] += 1
        COUNTS["audited_removal_blocks"] += 1
    COUNTS["stellar_pairs"] += 1
    DIGEST.update(json.dumps([
        sorted(complex_), sigma, sorted(subdiv),
        sorted(new_mu.items()),
    ], separators=(",", ":")).encode())
    DIGEST.update(b"\n")


def direct_barycentric(complex_: frozenset[int], labels: dict[int, int]) -> frozenset[int]:
    faces = tuple(sorted(complex_ - {0}))
    result = {0}
    for selection in range(1, 1 << len(faces)):
        chosen = [faces[i] for i in range(len(faces)) if selection >> i & 1]
        if all(is_subset(a, b) or is_subset(b, a)
               for a, b in itertools.combinations(chosen, 2)):
            result.add(sum(labels[f] for f in chosen))
    return frozenset(result)


def ordered_bell_values(limit: int) -> tuple[int, ...]:
    values = [1]
    for n in range(1, limit + 1):
        values.append(sum(
            comb(n, j) * values[n - j]
            for j in range(1, n + 1)
        ))
    return tuple(values)


def audit_barycentric(complex_: frozenset[int]) -> None:
    current = complex_
    labels = {face: face for face in complex_ if face.bit_count() == 1}
    next_bit = 16
    for face in sorted(complex_, key=lambda f: (-f.bit_count(), f)):
        if face.bit_count() < 2:
            continue
        current = stellar(current, face, next_bit)
        labels[face] = next_bit
        next_bit <<= 1
    expected = direct_barycentric(complex_, labels)
    require(current == expected, "descending stellar sequence is not barycentric")
    old_mu = upper_mu(complex_)
    new_mu = upper_mu(current)
    reverse_labels = {label: face for face, label in labels.items()}
    for chain in current:
        if chain == 0:
            predicted = old_mu[0]
        else:
            old_chain = [old for label, old in reverse_labels.items() if chain & label]
            maximum = max(old_chain, key=int.bit_count)
            predicted = (-1) ** (maximum.bit_count() - chain.bit_count()) * old_mu[maximum]
        require(new_mu[chain] == predicted, "barycentric Mobius formula failed")
        COUNTS["barycentric_mu_faces"] += 1
    bells = ordered_bell_values(max((f.bit_count() for f in complex_), default=0))
    predicted_length = abs(old_mu[0]) + sum(
        bells[f.bit_count()] * abs(old_mu[f]) for f in complex_ if f
    )
    require(sum(abs(value) for value in new_mu.values()) == predicted_length,
            "ordered-Bell multiplicity sum failed")
    COUNTS["barycentric_complexes"] += 1


def surface_signature(complex_: frozenset[int]) -> tuple[int, int, int, int, bool]:
    vertices = tuple(f for f in complex_ if f.bit_count() == 1)
    edges = tuple(f for f in complex_ if f.bit_count() == 2)
    triangles = tuple(f for f in complex_ if f.bit_count() == 3)
    require(all(f.bit_count() <= 3 for f in complex_), "surface has a high-dimensional face")
    incident = {edge: [tri for tri in triangles if is_subset(edge, tri)] for edge in edges}
    require(all(len(value) == 2 for value in incident.values()), "edge incidence is not two")
    for vertex in vertices:
        link_edges = [tri ^ vertex for tri in triangles if tri & vertex]
        link_vertices = {
            bit for edge in link_edges for bit in subfaces(edge)
            if bit.bit_count() == 1
        }
        require(all(sum(bool(edge & point) for edge in link_edges) == 2
                    for point in link_vertices), "vertex link degree is not two")
        graph = {point: set() for point in link_vertices}
        for edge in link_edges:
            ends = tuple(point for point in link_vertices if edge & point)
            require(len(ends) == 2, "bad link edge")
            graph[ends[0]].add(ends[1])
            graph[ends[1]].add(ends[0])
        reached = {next(iter(graph))}
        queue = deque(reached)
        while queue:
            vertex_in_link = queue.popleft()
            for neighbor in graph[vertex_in_link] - reached:
                reached.add(neighbor)
                queue.append(neighbor)
        require(reached == set(graph), "vertex link is disconnected")

    orientation: dict[int, int] = {triangles[0]: 1}
    queue_triangles = deque([triangles[0]])
    orientable = True
    while queue_triangles:
        tri = queue_triangles.popleft()
        ordered_tri = tuple(1 << i for i in range(tri.bit_length()) if tri >> i & 1)
        for missing_index, missing in enumerate(ordered_tri):
            edge = tri ^ missing
            other = next(t for t in incident[edge] if t != tri)
            other_order = tuple(1 << i for i in range(other.bit_length()) if other >> i & 1)
            other_missing_index = other_order.index(other ^ edge)
            wanted = -orientation[tri] * ((-1) ** missing_index) * ((-1) ** other_missing_index)
            if other in orientation:
                orientable &= orientation[other] == wanted
            else:
                orientation[other] = wanted
                queue_triangles.append(other)
    require(len(orientation) == len(triangles), "surface facets are disconnected")
    return (
        len(vertices), len(edges), len(triangles),
        len(vertices) - len(edges) + len(triangles), orientable,
    )


def shelling_reachable_masks(facets: tuple[int, ...]) -> set[int]:
    """Return triangle subsets reachable by pure shelling additions."""
    n = len(facets)
    reachable = {1 << i for i in range(n)}
    for size in range(1, n):
        for selected in tuple(mask for mask in reachable if mask.bit_count() == size):
            old = closure([facets[i] for i in range(n) if selected >> i & 1])
            for i, facet in enumerate(facets):
                if selected >> i & 1:
                    continue
                intersection = {face for face in subfaces(facet) if face in old}
                maximal = {
                    face for face in intersection
                    if not any(face != other and is_subset(face, other) for other in intersection)
                }
                if maximal and all(face.bit_count() == 2 for face in maximal):
                    reachable.add(selected | (1 << i))
    return reachable


def audit_seeds() -> dict[str, dict[str, object]]:
    seeds = json.loads((TARGET / "seeds.json").read_text())
    summary: dict[str, dict[str, object]] = {}
    for seed in seeds:
        facets = tuple(sum(1 << v for v in face) for face in seed["facets"])
        complex_ = closure(list(facets))
        word = tuple(sum(1 << v for v in face) for face in seed["word"])
        final, uses, signed = replay(complex_, word)
        full = (1 << len(complex_)) - 1
        mu = upper_mu(complex_)
        require(final == full, "seed word is not winning")
        require(all(uses[f] == abs(mu[f]) and signed[f] == -mu[f] for f in complex_),
                "seed word is not facewise optimal")
        signature = surface_signature(complex_)
        n = len(facets)
        reachable_masks = shelling_reachable_masks(facets)
        shellable = (1 << n) - 1 in reachable_masks
        summary[seed["name"]] = {
            "f_vector": list(signature[:3]),
            "euler_characteristic": signature[3],
            "orientable": signature[4],
            "word_length": len(word),
            "facewise_lower_bound": sum(abs(v) for v in mu.values()),
            "shellable": shellable,
            "shelling_reachable_subsets": len(reachable_masks),
        }
        COUNTS["surface_seeds"] += 1
    return summary


def rejection_controls() -> None:
    edge = closure([3])
    controls = [
        lambda: stellar(edge, 0, 4),
        lambda: stellar(edge, 7, 4),
        lambda: stellar(edge, 3, 2),
        lambda: replay(edge, (0,)),  # zero-Mobius empty face of a simplex
        lambda: replay(closure([5, 6]), (4, 5, 6)),  # corrupted s=2 macro
        lambda: replay(edge, (7,)),  # absent generator
    ]
    for control in controls:
        try:
            control()
        except ValueError:
            COUNTS["negative_controls"] += 1
        else:
            raise ValueError("negative control was accepted")


def run() -> dict[str, object]:
    complexes = all_four_label_complexes()
    require(len(complexes) == 167, "wrong four-label complex count")
    local_summary = {}
    for s in range(1, 5):
        for c in range(1, 4):
            order, ways = search_local_macro(s, c)
            local_summary[f"s{s}_c{c}"] = {
                "generators": (1 << s) - 1,
                "legal_one_use_orders": ways,
                "first_order": list(order),
            }
    for complex_ in complexes:
        for sigma in sorted(complex_ - {0}):
            audit_stellar_case(complex_, sigma)
        audit_barycentric(complex_)
        COUNTS["four_label_complexes"] += 1
    seeds = audit_seeds()
    rejection_controls()
    return {
        "status": "verified",
        "python": platform.python_version(),
        "counts": dict(sorted(COUNTS.items())),
        "local_macro_search": local_summary,
        "seeds": seeds,
        "entrywise_sha256": DIGEST.hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
