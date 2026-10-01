"""Canonical incidence-graph refinement, independently written by reviewer2.

Branch on every point in an intrinsic nonsingleton cell, refine the colored
point/block incidence graph, and collect all minimal leaf certificates.
"""
from collections import Counter
from itertools import combinations
import time
from carrier import N, IDENTITY, PROFILE, check_star, require, points, image_star, compose, inverse

def canonical(star, cap=200000, seconds=10):
    require(type(cap) is int and 0 <= cap <= 200000 and 0 < seconds <= 10, 'invalid incidence guard')
    star = tuple(sorted(star))
    check_star(star)
    neighbors = [set() for _ in range(N + len(star))]
    for i, w in enumerate(star, N):
        for z in points(w):
            neighbors[z].add(i)
            neighbors[i].add(z)
    initial = ((0,), (1, 2, 3), tuple(range(4, N)), tuple(range(N, N + len(star))))
    best, maps, states, leaves = None, [], 0, 0
    start = time.monotonic()

    def refine(cells):
        while True:
            color = {v: j for j, cell in enumerate(cells) for v in cell}
            result = []
            for cell in cells:
                buckets = {}
                for v in cell:
                    counts = Counter(color[u] for u in neighbors[v])
                    key = tuple(counts[j] for j in range(len(cells)))
                    buckets.setdefault(key, []).append(v)
                result.extend(tuple(buckets[key]) for key in sorted(buckets))
            result = tuple(result)
            if len(result) == len(cells):
                return result
            cells = result

    def visit(cells):
        nonlocal best, maps, states, leaves
        states += 1
        require(states <= cap and time.monotonic() - start <= seconds, 'INCOMPLETE incidence guard')
        cells = refine(cells)
        choices = [(len(cell), j, cell) for j, cell in enumerate(cells) if len(cell) > 1 and cell[0] < N]
        if not choices:
            order = tuple(cell[0] for cell in cells if cell[0] < N)
            require(len(order) == N and sorted(order) == list(range(N)), 'incidence leaf point labeling incomplete')
            labeling = inverse(order)
            key = image_star(star, labeling)
            leaves += 1
            if best is None or key < best:
                best, maps = key, [order]
            elif key == best:
                maps.append(order)
            return
        _, index, cell = min(choices)
        for v in cell:
            next_cells = cells[:index] + ((v,), tuple(u for u in cell if u != v)) + cells[index + 1:]
            visit(next_cells)

    visit(initial)
    require(best is not None and maps and len(maps) == len(set(maps)), 'incidence canonical leaves missing/duplicated')
    base_inv = inverse(maps[0])
    automorphisms = tuple(sorted(compose(point, base_inv) for point in maps))
    aut_set = set(automorphisms)
    require(len(aut_set) == len(maps) and IDENTITY in aut_set, 'bad canonical automorphism maps')
    for point in automorphisms:
        require(sorted(point) == list(range(N)) and tuple(PROFILE[point[z]] for z in range(N)) == PROFILE and image_star(star, point) == star, 'false literal automorphism')
    for a in automorphisms:
        for b in automorphisms:
            require(compose(a, b) in aut_set, 'canonical automorphism group not closed')
    return dict(canonical=best, automorphisms=automorphisms, order=len(automorphisms), states=states, leaves=leaves)

def group_invariants(automorphisms):
    orders = Counter()
    for g in automorphisms:
        power, order = g, 1
        while power != IDENTITY:
            power = compose(g, power)
            order += 1
            require(order <= len(automorphisms), 'element order exceeds group size')
        orders[order] += 1
    unseen, orbits = set(range(N)), []
    while unseen:
        z = min(unseen)
        orbit = sorted({g[z] for g in automorphisms})
        require(set(orbit) <= unseen, 'point orbit overlap')
        unseen.difference_update(orbit)
        orbits.append(orbit)
    group = set(automorphisms)
    def power(g, k):
        result = IDENTITY
        for _ in range(k):
            result = compose(g, result)
        return result
    if len(group) == 18:
        odd = {g for g in group if power(g, 3) == IDENTITY}
        require(len(odd) == 9 and all(compose(a, b) in odd and compose(a, b) == compose(b, a) for a in odd for b in odd), 'order18 odd subgroup is not elementary abelian')
        a = min(odd - {IDENTITY})
        b = min(odd - {power(a, k) for k in range(3)})
        t = min(g for g in group - {IDENTITY} if power(g, 2) == IDENTITY)
        require({compose(power(a, i), power(b, j)) for i in range(3) for j in range(3)} == odd, 'two order3 generators do not generate the nine-group')
        require(all(compose(t, compose(g, t)) == inverse(g) for g in odd), 'involution does not invert odd subgroup')
        require(odd | {compose(t, g) for g in odd} == group, 'order18 semidirect product coverage incomplete')
        kind, witnesses = 'Dih(C3 x C3) = (C3 x C3) semidirect inversion C2', (a, b, t)
    elif len(group) == 6 and orders[6] == 2:
        a = min(g for g in group if power(g, 3) != IDENTITY and power(g, 2) != IDENTITY)
        require({power(a, k) for k in range(6)} == group, 'order6 generator does not generate full group')
        kind, witnesses = 'C6', (a,)
    elif len(group) == 6:
        a = min(g for g in group - {IDENTITY} if power(g, 3) == IDENTITY)
        t = min(g for g in group - {IDENTITY} if power(g, 2) == IDENTITY)
        require(compose(t, compose(a, t)) == inverse(a), 'S3 presentation relation fails')
        require({power(a, k) for k in range(3)} | {compose(t, power(a, k)) for k in range(3)} == group, 'S3 presentation fails complete group coverage')
        kind, witnesses = 'S3', (a, t)
    elif len(group) == 2:
        a = min(group - {IDENTITY})
        require(power(a, 2) == IDENTITY, 'order2 presentation relation fails')
        kind, witnesses = 'C2', (a,)
    else:
        raise ValueError('unexpected automorphism group order')
    return {'element_orders': sorted(orders.items()), 'point_orbits': orbits, 'abstract_group': kind, 'presentation_generators': witnesses}
