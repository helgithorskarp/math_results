"""Exact witnesses for a nine-type split-graph cover obstruction.

Run with Python 3: python3 check.py
The proof is universal; this audits explicit finite instances without a solver.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json


SETS = ((0, 1, 2), (0, 1, 3), (0, 3), (1, 2, 3), (2, 3))
PACK = ((0, 2, 4), (0, 1, 5), (0, 3, 6), (1, 2, 7), (2, 3, 8))
# Twice an optimal fractional cover of ALL seed triangles, not just centered ones.
DUAL2 = {(0, 1): 1, (0, 3): 2, (1, 2): 1, (1, 3): 1, (2, 3): 2,
         (0, 4): 1, (2, 4): 1, (1, 5): 1, (1, 7): 1}


def require(value, message):
    if not value:
        raise ValueError(message)


def edge(a, b):
    return min(a, b), max(a, b)


def triangle_edges(t):
    return tuple(edge(a, b) for a, b in combinations(t, 2))


def seed():
    edges = set(combinations(range(4), 2))
    centered = []
    for i, neighbors in enumerate(SETS):
        edges.update((u, 4 + i) for u in neighbors)
        centered.extend((u, v, 4 + i) for u, v in combinations(neighbors, 2))
    triangles = list(combinations(range(4), 3)) + centered
    return edges, centered, triangles


def validate_primal(edges, weighted):
    loads = Counter()
    value = Q(0)
    count = 0
    for t, weight in weighted:
        require(len(set(t)) == 3 and weight >= 0, "primal domain")
        for e in triangle_edges(t):
            require(e in edges, "primal nonedge")
            loads[e] += weight
        value += weight
        count += 1
    require(all(x <= 1 for x in loads.values()), "primal overload")
    return value, count


def validate_dual(edges, triangles, weights2):
    require(all(e in edges and type(x) is int and x >= 0
                for e, x in weights2.items()), "dual domain")
    count = 0
    for t in triangles:
        require(all(e in edges for e in triangle_edges(t)), "dual triangle nonedge")
        require(sum(weights2.get(e, 0) for e in triangle_edges(t)) >= 2,
                "uncovered triangle")
        count += 1
    return Q(sum(weights2.values()), 2), count


def validate_packing(edges, triangles):
    used = set()
    count = 0
    digest = sha256()
    for t in triangles:
        require(len(set(t)) == 3, "packing repeated vertex")
        for e in triangle_edges(t):
            require(e in edges and e not in used, "packing edge conflict")
            used.add(e)
        digest.update((" ".join(map(str, t)) + "\n").encode())
        count += 1
    return count, digest.hexdigest()


def lifted_triangle(t, p):
    """A Latin-square decomposition of the balanced blow-up of one triangle."""
    a, b, c = t
    for x in range(p):
        for y in range(p):
            yield (a * p + x, b * p + y, c * p + (x + y) % p)


def graph(p):
    require(type(p) is int and p >= 2, "integer scale at least two")
    k = 4 * p
    centers = {}
    for i, neighbors in enumerate(SETS):
        lifted = tuple(u * p + x for u in neighbors for x in range(p))
        for z in range(p):
            centers[(4 + i) * p + z] = lifted
    for group in range(4):
        neighbors = tuple(group * p + x for x in range(p))
        for z in range(p - 1):
            centers[9 * p + group * (p - 1) + z] = neighbors
    edges = set(combinations(range(k), 2))
    for center, neighbors in centers.items():
        edges.update((u, center) for u in neighbors)
    return k, centers, edges


def all_triangles(k, centers):
    yield from combinations(range(k), 3)
    for center, neighbors in centers.items():
        for u, v in combinations(neighbors, 2):
            yield u, v, center


def centered_primal(p):
    _, centered, _ = seed()
    for t in centered:
        for lifted in lifted_triangle(t, p):
            yield lifted, Q(1, 2)
    for group in range(4):
        for z in range(p - 1):
            center = 9 * p + group * (p - 1) + z
            for x, y in combinations(range(p), 2):
                yield (group * p + x, group * p + y, center), Q(1, p - 1)


def full_dual(p):
    weights2 = {}
    for (a, b), w in DUAL2.items():
        for x in range(p):
            for y in range(p):
                weights2[a * p + x, b * p + y] = w
    for group in range(4):
        for x, y in combinations(range(p), 2):
            weights2[group * p + x, group * p + y] = 2
    return weights2


def direct_seed_cover():
    """Exhaust all subsets: independent of the fractional-cover lower bound."""
    edges, _, triangles = seed()
    ordered = sorted(edges)
    ids = {e: i for i, e in enumerate(ordered)}
    masks = [sum(1 << ids[e] for e in triangle_edges(t)) for t in triangles]
    best = len(edges)
    best_count = 0
    for mask in range(1 << len(edges)):
        size = mask.bit_count()
        if size > best or not all(mask & t for t in masks):
            continue
        if size < best:
            best, best_count = size, 0
        best_count += 1
    return best, best_count


def transversal_count(p):
    """Expand the averaging certificate for two small scales, without designs."""
    edges, _, _ = seed()
    counts = Counter()
    number = 0
    for choices in product(range(p), repeat=9):
        for u, v in edges:
            counts[u * p + choices[u], v * p + choices[v]] += 1
        number += 1
    require(number == p ** 9, "transversal count")
    require(len(counts) == 19 * p * p and set(counts.values()) == {p ** 7},
            "transversal edge multiplicity")
    require(Q(6 * number, p ** 7) == 6 * p * p, "averaged integer cover bound")
    return dict(scale=p, transversals=number, edges=len(counts),
                copies_per_edge=p ** 7, cover_lower=6 * p * p)


def phi(k, h):
    return Q(k * k, 4) - Q(k, 2) + h - h * h / (k * k) + Q(1, 4)


def check_family(p):
    k, centers, edges = graph(p)
    types = Counter(centers.values())
    require(len(types) == 9, "type count")
    require(all(m <= len(s) - 1 for s, m in types.items()), "multiplicity cap")
    require(sum(map(len, types)) == 17 * p, "D")
    require(len(centers) + k == 13 * p - 4, "vertex count")
    require(len(edges) == 25 * p * p - 6 * p, "edge count")
    primal, support = validate_primal(edges, centered_primal(p))
    dual, triangle_count = validate_dual(edges, all_triangles(k, centers), full_dual(p))
    h = Q(15 * p * p, 2) - 2 * p
    require(primal == dual == h, "full and centered fractional equality")
    packing, digest = validate_packing(
        edges, (t for old in PACK for t in lifted_triangle(old, p)))
    require(packing == 5 * p * p, "integer packing witness")

    # Partition all graph edges into the seed blow-up and four internal gadgets.
    seed_edges, _, _ = seed()
    external = {(u * p + x, v * p + y) for u, v in seed_edges
                for x in range(p) for y in range(p)}
    parts = [external]
    for group in range(4):
        base = tuple(range(group * p, (group + 1) * p))
        new = tuple(9 * p + group * (p - 1) + z for z in range(p - 1))
        part = set(combinations(base, 2)) | {(u, c) for u in base for c in new}
        require(len(part) == 3 * p * (p - 1) // 2, "internal edge count")
        for previous in parts:
            require(not part & previous, "cover components overlap")
        parts.append(part)
    require(set().union(*parts) == edges, "cover components incomplete")
    # The proof's transversal averaging gives 6p^2 on the first component.
    # Each internal component has an explicit fractional packing of C(p,2).
    cover_lower = 6 * p * p + 4 * (p * (p - 1) // 2)
    clique_cover = set(combinations(range(k), 2))
    require(cover_lower == len(clique_cover), "cover upper/lower equality")
    require(all(u < k <= v for u, v in edges - clique_cover), "cover fails")
    excess = cover_lower - phi(k, h)
    require(excess == Q(p * p, 64) + Q(p, 8), "quadratic excess")
    require(cover_lower < 2 * packing, "Tuza witness")
    return dict(scale=p, clique_order=k, vertices=13 * p - 4,
                types=9, D=17 * p, edges=len(edges),
                centered_fractional=str(h), full_fractional=str(h),
                fractional_support=support, triangles_checked=triangle_count,
                cover=cover_lower, packing_witness=packing,
                proposed_bound=str(phi(k, h)), excess=str(excess),
                packing_sha256=digest)


def rejected(operation):
    try:
        operation()
    except ValueError:
        return True
    raise AssertionError("damaged certificate accepted")


def audit():
    edges, centered, triangles = seed()
    primal, _ = validate_primal(edges, [(t, Q(1, 2)) for t in centered])
    dual, _ = validate_dual(edges, triangles, DUAL2)
    require(primal == dual == Q(11, 2), "seed full LP")
    optimum, optimal_covers = direct_seed_cover()
    require((optimum, optimal_covers) == (6, 20), "seed direct cover")
    validate_packing(edges, PACK)
    k, centers, expanded = graph(2)
    bad_dual = full_dual(2)
    bad_dual.pop((0, 1))  # An internal edge needed by a new-center triangle.
    missing = set(expanded)
    missing.remove((0, 1))
    controls = [
        rejected(lambda: validate_primal(edges, [(centered[0], Q(3, 2))])),
        rejected(lambda: validate_dual(expanded, all_triangles(k, centers), bad_dual)),
        rejected(lambda: validate_primal(missing, centered_primal(2))),
        rejected(lambda: validate_packing(edges, (*PACK, PACK[0]))),
        rejected(lambda: graph(1)),
    ]
    return dict(status="all exact checks passed",
                seed=dict(vertices=9, edges=19, centered_fractional="11/2",
                          full_fractional="11/2", cover=optimum,
                          optimal_covers=optimal_covers, edge_subsets=2 ** 19),
                transversal_audits=[transversal_count(p) for p in (2, 3)],
                families=[check_family(p) for p in (2, 3, 5, 11, 16, 31)],
                negative_controls=len(controls))


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
