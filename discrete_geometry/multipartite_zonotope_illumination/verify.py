#!/usr/bin/env python3
"""Exact corroboration of complete multipartite zonotope illumination.

CPython 3.11+, standard library only. No assertions, solver, or floats.
The universal statements are proved in PROOF.md; these are finite checks.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import lcm
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parts_of(sizes):
    require(len(sizes) >= 2, "at least two parts required")
    require(all(type(s) is int and s > 0 for s in sizes), "invalid part size")
    parts = []
    first = 0
    for s in sizes:
        parts.append(tuple(range(first, first + s)))
        first += s
    return parts


def edges_of(parts):
    return tuple(sorted((min(a, b), max(a, b))
                        for i, p in enumerate(parts) for q in parts[i + 1:]
                        for a in p for b in q))


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for a in range(minimum, n + 1):
        for rest in partitions(n - a, a):
            yield (a,) + rest


def arcs_of(edges, bits):
    return tuple((a, b) if bits >> j & 1 else (b, a)
                 for j, (a, b) in enumerate(edges))


def source_set(n, arcs):
    return frozenset(set(range(n)) - {b for a, b in arcs})


def is_acyclic(n, arcs):
    remaining = set(range(n))
    while remaining:
        ready = {x for x in remaining
                 if all(b != x or a not in remaining for a, b in arcs)}
        if not ready:
            return False
        remaining -= ready
    return True


def order_orientation(edges, order):
    rank = {v: j for j, v in enumerate(order)}
    return sum(1 << j for j, (a, b) in enumerate(edges) if rank[a] < rank[b])


def all_orientations(n, edges):
    # Complete because every acyclic orientation has a topological ordering.
    return sorted({order_orientation(edges, p) for p in permutations(range(n))})


def masks(n):
    return tuple(range(1, (1 << n) - 1))


def selected_sum(vector, mask):
    return sum(x for i, x in enumerate(vector) if mask >> i & 1)


def vertex(n, edges, bits, weights):
    require(len(weights) == len(edges) and all(w > 0 for w in weights),
            "strictly positive weights required")
    v = [0] * n
    for (a, b), w in zip(arcs_of(edges, bits), weights):
        v[a] -= w
        v[b] += w
    return tuple(v)


def supports(n, edges, weights):
    return tuple(sum(w for (a, b), w in zip(edges, weights)
                     if ((mask >> a) ^ (mask >> b)) & 1)
                 for mask in masks(n))


def active_cuts(n, v, h):
    result = []
    for mask, height in zip(masks(n), h):
        value = selected_sum(v, mask)
        require(-height <= value <= height, "vertex violates a support")
        if value == height:
            result.append(mask)
    require(result, "vertex has no nonconstant active support")
    return tuple(result)


def illuminates(u, active):
    return all(selected_sum(u, mask) < 0 for mask in active)


def direction(n, sources):
    return tuple(n - len(sources) if i in sources else -len(sources)
                 for i in range(n))


def certificates(parts, edges):
    result = []
    for i, part in enumerate(parts):
        for s in range(1, len(part) + 1):
            for subset in combinations(part, s):
                S = frozenset(subset)
                middle = tuple(v for k in range(1, len(parts))
                               for v in parts[(i + k) % len(parts)])
                order = tuple(subset) + middle + tuple(v for v in part if v not in S)
                result.append((i, S, order_orientation(edges, order)))
    return result


def opposing_cut(parts, first, second):
    i, S, _ = first
    j, T, _ = second
    if i == j:
        return 1 << min(S ^ T)
    low = set(S) | (set(parts[j]) - T)
    k = (i + 1) % len(parts)
    while k != j:
        low.update(parts[k])
        k = (k + 1) % len(parts)
    return sum(1 << v for v in low)


def reachable(n, arcs, start):
    reached = {start}
    while True:
        more = reached | {b for a, b in arcs if a in reached}
        if more == reached:
            return reached
        reached = more


def weight_assignments(edges):
    rational = [Fraction(1 + (7*j) % 13, 1 + (5*j) % 7)
                for j in range(len(edges))]
    denominator = lcm(*(w.denominator for w in rational))
    # Global clearing of denominators is exact and preserves all signs.
    return [tuple(1 for _ in edges),
            tuple(1 + (3*j) % 11 for j in range(len(edges))),
            tuple(int(w * denominator) for w in rational)]


def check_family(sizes):
    parts = parts_of(sizes)
    n = sum(sizes)
    edges = edges_of(parts)
    orientations = all_orientations(n, edges)
    brute_count = 0
    if n <= 6:
        brute = [bits for bits in range(1 << len(edges))
                 if is_acyclic(n, arcs_of(edges, bits))]
        require(brute == orientations, "independent orientation enumeration disagrees")
        brute_count = 1 << len(edges)
    certs = certificates(parts, edges)
    target = sum((1 << s) - 1 for s in sizes)
    require(len(certs) == target, "wrong certificate cardinality")
    require(len({c[2] for c in certs}) == target, "repeated certificate vertex")
    directions = [direction(n, S) for _, S, _ in certs]
    checks = pairs = exact_steps = 0
    baseline_active = {}
    for wi, weights in enumerate(weight_assignments(edges)):
        h = supports(n, edges, weights)
        seen_vertices = set()
        for bits in orientations:
            arcs = arcs_of(edges, bits)
            S = source_set(n, arcs)
            require(S and any(S <= set(p) for p in parts), "sources cross parts")
            for a in S:
                require(reachable(n, arcs, a) == (set(range(n)) - set(S)) | {a},
                        "source reachability fails")
            u = direction(n, S)
            v = vertex(n, edges, bits, weights)
            require(sum(v) == sum(u) == 0, "not in the sum-zero space")
            seen_vertices.add(v)
            active = active_cuts(n, v, h)
            if wi == 0:
                baseline_active[bits] = active
            else:
                require(active == baseline_active[bits], "positive weight fan changed")
            require(illuminates(u, active), "claimed source direction fails")
            checks += len(active)
            # Give an actual rational step which makes every cut strict.
            caps = [Fraction(height - selected_sum(v, mask), selected_sum(u, mask))
                    for mask, height in zip(masks(n), h)
                    if selected_sum(u, mask) > 0]
            step = min([Fraction(1)] + caps) / 2
            require(step > 0, "no positive step")
            require(all(selected_sum(v, mask) + step * selected_sum(u, mask) < height
                        for mask, height in zip(masks(n), h)),
                    "literal step is not interior")
            exact_steps += 1
        require(len(seen_vertices) == len(orientations), "vertex map not injective")
        vertices = [vertex(n, edges, bits, weights) for _, _, bits in certs]
        for a, b in combinations(range(target), 2):
            mask = opposing_cut(parts, certs[a], certs[b])
            require(mask in masks(n), "constant antipodal witness")
            height = h[mask - 1]
            x, y = selected_sum(vertices[a], mask), selected_sum(vertices[b], mask)
            require(height > 0 and x == -y and abs(x) == height,
                    "antipodal support certificate fails")
            pairs += 1
        # The certificate vertices also show that every selected direction is needed.
        for a, v in enumerate(vertices):
            active = active_cuts(n, v, h)
            lit = [b for b, u in enumerate(directions) if illuminates(u, active)]
            require(lit == [a], "canonical cover is not separated by its certificate")
    return {"parts": list(sizes), "edges": len(edges), "vertices": len(orientations),
            "illumination": target, "brute_orientations": brute_count,
            "strict_active_cut_checks": checks, "antipodal_pairs": pairs,
            "exact_interior_steps": exact_steps}


def connected(n, edges):
    return len(reachable(n, edges + tuple((b, a) for a, b in edges), 0)) == n


def forbidden_triple(n, edges):
    E = set(edges)
    for a, b in edges:
        for c in range(n):
            if c not in (a, b) and tuple(sorted((a, c))) not in E and tuple(sorted((b, c))) not in E:
                return a, b, c
    return None


def check_characterization():
    counts = {"connected_graphs": 0, "complete_multipartite": 0,
              "obstruction_certificates": 0, "orientations_in_positive_cases": 0}
    for n in range(2, 6):
        possible = tuple(combinations(range(n), 2))
        for code in range(1 << len(possible)):
            edges = tuple(e for j, e in enumerate(possible) if code >> j & 1)
            if not connected(n, edges):
                continue
            counts["connected_graphs"] += 1
            triple = forbidden_triple(n, edges)
            if triple is None:
                counts["complete_multipartite"] += 1
                for bits in all_orientations(n, edges):
                    arcs = arcs_of(edges, bits)
                    S = source_set(n, arcs)
                    require(all(reachable(n, arcs, a) == (set(range(n)) - set(S)) | {a}
                                for a in S), "characterization positive case fails")
                    counts["orientations_in_positive_cases"] += 1
            else:
                a, b, c = triple
                order = (a, c, b) + tuple(v for v in range(n) if v not in triple)
                bits = order_orientation(edges, order)
                arcs = arcs_of(edges, bits)
                S = source_set(n, arcs)
                R = reachable(n, arcs, c)
                require(a in S and c in S and b not in R and b not in S,
                        "induced triple did not create the required source obstruction")
                u = tuple(n if v == c else -2*len(S) if v == b else 1 if v in S else -1
                          for v in range(n))
                require(sum(u) == 0 and all((u[v] > 0) == (v in S) for v in range(n)),
                        "obstruction direction has wrong sign pattern")
                mask = sum(1 << v for v in R)
                weights = (1,) * len(edges)
                v = vertex(n, edges, bits, weights)
                h = supports(n, edges, weights)
                require(selected_sum(v, mask) == h[mask - 1] and selected_sum(u, mask) > 0,
                        "obstruction direction does not violate an active support")
                counts["obstruction_certificates"] += 1
    return counts


def negative_controls():
    checked = []
    for sizes in ((), (2,), (0, 2), (-1, 3), (True, 1)):
        try:
            parts_of(sizes)
        except ValueError:
            checked.append("invalid_parts_" + repr(sizes))
        else:
            raise ValueError("invalid parts accepted")
    for w in (0, -1):
        try:
            vertex(2, ((0, 1),), 1, (w,))
        except ValueError:
            checked.append("invalid_weight_" + str(w))
        else:
            raise ValueError("invalid weight accepted")
    parts = parts_of((2, 2))
    edges = edges_of(parts)
    i, S, bits = certificates(parts, edges)[0]
    v = vertex(4, edges, bits, (1,) * len(edges))
    active = active_cuts(4, v, supports(4, edges, (1,) * len(edges)))
    require(not illuminates((0, 0, 0, 0), active), "tangent direction accepted")
    require(not illuminates(tuple(-x for x in direction(4, S)), active),
            "reversed direction accepted")
    checked += ["tangent_rejected", "reversed_direction_rejected"]
    # Uniform source directions are NOT asserted to work outside the class.
    path = ((0, 1), (1, 2), (2, 3))
    bits = order_orientation(path, (0, 2, 1, 3))
    S = source_set(4, arcs_of(path, bits))
    v = vertex(4, path, bits, (1, 1, 1))
    active = active_cuts(4, v, supports(4, path, (1, 1, 1)))
    require(not illuminates(direction(4, S), active), "P4 tangent obstruction lost")
    checked.append("P4_uniform_source_tangency_detected")
    return checked


def main():
    cases = [p for n in range(2, 7) for p in partitions(n) if len(p) >= 2]
    cases += [(3, 4), (2, 2, 3), (1, 2, 2, 2), (1, 1, 1, 1, 1, 1, 1)]
    rows = [check_family(p) for p in cases]
    totals = {key: sum(row[key] for row in rows)
              for key in ("vertices", "brute_orientations", "strict_active_cut_checks",
                          "antipodal_pairs", "exact_interior_steps")}
    print(json.dumps({"status": "VERIFIED", "arithmetic": "exact integers and Fraction",
                      "weight_assignments_per_case": 3, "cases": rows, "totals": totals,
                      "source_cone_characterization": check_characterization(),
                      "negative_controls": negative_controls()}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
