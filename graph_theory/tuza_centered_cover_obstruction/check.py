"""Exact certificates for an affine family obstructing a centered-LP cover bound.

Python 3 standard library only. Run: python3 check.py
No solver, network, random input, or external certificate is used.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json


NEIGHBORHOODS = ((0, 1, 2), (0, 1, 3), (0, 3), (1, 2, 3), (2, 3))
PACKING_PAIRS = ((0, 2), (0, 1), (0, 3), (1, 2), (2, 3))
# F_4 = F_2[a]/(a^2+a+1), represented by 0,1,a,1+a.
PRODUCT = ((0, 0, 0, 0), (0, 1, 2, 3),
           (0, 2, 3, 1), (0, 3, 1, 2))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(u, v):
    return (min(u, v), max(u, v))


def triangle_edges(t):
    return tuple(edge(u, v) for u, v in combinations(t, 2))


def gadget():
    edges = set(combinations(range(4), 2))
    centered = []
    packing = []
    for i, neighbors in enumerate(NEIGHBORHOODS):
        center = 4 + i
        edges.update((v, center) for v in neighbors)
        centered.extend((u, v, center) for u, v in combinations(neighbors, 2))
        packing.append((*PACKING_PAIRS[i], center))
    # All omitted dual edge weights are zero.
    dual = {(0, 3): Q(1), (2, 3): Q(1),
            (0, 4): Q(1, 2), (1, 4): Q(1, 2), (2, 4): Q(1, 2),
            (1, 5): Q(1), (1, 7): Q(1)}
    return edges, centered, packing, dual


def check_primal(edges, triangles, weights):
    require(len(triangles) == len(weights), "weight count")
    loads = Counter()
    for t, weight in zip(triangles, weights):
        require(len(set(t)) == 3 and weight >= 0, "triangle or weight")
        for e in triangle_edges(t):
            require(e in edges, "primal triangle outside graph")
            loads[e] += weight
    require(all(x <= 1 for x in loads.values()), "primal capacity")
    return sum(weights, Q(0))


def check_dual(edges, centered, dual):
    require(all(e in edges and x >= 0 for e, x in dual.items()), "dual domain")
    for t in centered:
        require(sum(dual.get(e, Q(0)) for e in triangle_edges(t)) >= 1,
                "uncovered centered triangle")
    return sum(dual.values(), Q(0))


def check_packing(edges, triangles):
    used = set()
    for t in triangles:
        require(len(set(t)) == 3, "repeated triangle vertex")
        for e in triangle_edges(t):
            require(e in edges and e not in used, "invalid packing edge")
            used.add(e)
    return len(triangles)


def direct_gadget_optima(edges, centered):
    """Definition-level enumeration, independent of the LP argument."""
    ordered = sorted(edges)
    ids = {e: i for i, e in enumerate(ordered)}
    all_triangles = [t for t in combinations(range(9), 3)
                     if all(e in edges for e in triangle_edges(t))]
    masks = [sum(1 << ids[e] for e in triangle_edges(t)) for t in all_triangles]
    tested = 0
    optimum_cover = None
    for size in range(7):
        for positions in combinations(range(len(edges)), size):
            cover = sum(1 << p for p in positions)
            tested += 1
            if all(cover & t for t in masks):
                optimum_cover = size
                break
        if optimum_cover is not None:
            break

    def packing_optimum(candidates):
        reachable = {0: 0}
        for t in candidates:
            mask = sum(1 << ids[e] for e in triangle_edges(t))
            new = dict(reachable)
            for used, count in reachable.items():
                if not (used & mask):
                    new[used | mask] = max(new.get(used | mask, 0), count + 1)
            reachable = new
        return max(reachable.values())

    return dict(triangles=len(all_triangles), cover=optimum_cover,
                cover_subsets_tested=tested, packing=packing_optimum(all_triangles),
                centered_packing=packing_optimum(centered))


def scalar(a, vector, dimension):
    result = 0
    for j in range(dimension):
        result |= PRODUCT[a][(vector >> (2 * j)) & 3] << (2 * j)
    return result


def affine_lines(dimension):
    require(type(dimension) is int and dimension >= 1, "positive dimension")
    k = 4 ** dimension
    lines = []
    for direction in range(1, k):
        first = next((direction >> (2 * j)) & 3 for j in range(dimension)
                     if (direction >> (2 * j)) & 3)
        if first != 1:
            continue
        offsets = [scalar(a, direction, dimension) for a in range(4)]
        for origin in range(k):
            line = tuple(sorted(origin ^ v for v in offsets))
            if origin == line[0]:
                lines.append(line)
    return sorted(lines)


def polynomial_product(a, b):
    """Independent bit-polynomial multiplication, reduced by X^2+X+1."""
    value = 0
    for j in range(2):
        if (b >> j) & 1:
            value ^= a << j
    if value & 4:
        value ^= 7
    return value


def pair_generated_lines(dimension):
    """Generate every line from pairs, without normalized directions/cosets."""
    k = 4 ** dimension
    lines = set()
    for x, y in combinations(range(k), 2):
        delta = x ^ y
        points = []
        for a in range(4):
            offset = sum(polynomial_product(a, (delta >> (2 * j)) & 3)
                         << (2 * j) for j in range(dimension))
            points.append(x ^ offset)
        lines.add(tuple(sorted(points)))
    return sorted(lines)


def check_design(k, lines):
    pairs = set()
    for line in lines:
        require(len(line) == 4 and len(set(line)) == 4, "four distinct points")
        require(all(type(v) is int and 0 <= v < k for v in line), "point domain")
        for u, v in combinations(line, 2):
            e = edge(u, v)
            require(e not in pairs, "repeated pair")
            pairs.add(e)
    require(pairs == set(combinations(range(k), 2)), "missing pair")


def phi(k, h):
    return Q(k * k, 4) - Q(k, 2) + h - h * h / (k * k) + Q(1, 4)


def check_family(dimension):
    k = 4 ** dimension
    lines = affine_lines(dimension)
    require(lines == pair_generated_lines(dimension), "line generators disagree")
    check_design(k, lines)
    local_edges, local_triangles, local_packing, local_dual = gadget()
    all_edges = set()
    all_triangles = []
    all_packing = []
    dual = {}
    fingerprint = sha256()
    neighborhoods = set()
    for index, line in enumerate(lines):
        labels = (*line, *(k + 5 * index + i for i in range(5)))
        mapped_edges = {edge(labels[u], labels[v]) for u, v in local_edges}
        require(not (all_edges & mapped_edges), "gadget edges overlap")
        all_edges.update(mapped_edges)
        for neighbors in NEIGHBORHOODS:
            neighborhood = tuple(sorted(labels[v] for v in neighbors))
            require(neighborhood not in neighborhoods, "duplicate type")
            neighborhoods.add(neighborhood)
        for t in local_triangles:
            mapped = tuple(labels[v] for v in t)
            all_triangles.append(mapped)
            fingerprint.update(("T " + " ".join(map(str, mapped)) + "\n").encode())
        for t in local_packing:
            mapped = tuple(labels[v] for v in t)
            all_packing.append(mapped)
            fingerprint.update(("P " + " ".join(map(str, mapped)) + "\n").encode())
        for (u, v), weight in local_dual.items():
            e = edge(labels[u], labels[v])
            require(e not in dual, "dual edge repeated")
            dual[e] = weight
    b = len(lines)
    q = k * (k - 1) // 2
    require(6 * b == q and len(all_edges) == 19 * b, "graph edge counts")
    h = check_primal(all_edges, all_triangles, [Q(1, 2)] * len(all_triangles))
    require(h == check_dual(all_edges, all_triangles, dual) == Q(11 * b, 2),
            "fractional optimum")
    require(check_packing(all_edges, all_packing) == 5 * b, "integer packing")
    # Every center is private to one block; integer centered optima add.
    integer_centered_upper = 5 * b
    require(integer_centered_upper == len(all_packing), "centered optimum")
    # Separate integer cover lower bounds add because gadget edges are disjoint.
    cover_lower = 6 * b
    clique_edges = {e for e in all_edges if e[1] < k}
    require(len(clique_edges) == q == cover_lower, "cover equality")
    require(all(u < k <= v for u, v in all_edges - clique_edges),
            "remaining graph is not bipartite")
    bound = phi(k, h)
    gap = q - bound
    require(gap == Q((k - 1) ** 2, 576) + Q(k - 1, 24), "gap identity")
    require(gap > 0 and (dimension == 1 or gap > 1), "strict failure")
    return dict(dimension=dimension, clique_order=k, blocks=b,
                neighborhood_types=5 * b, vertices=k + 5 * b, edges=19 * b,
                centered_fractional=str(h), centered_integer=5 * b,
                triangle_cover=q, proposed_bound=str(bound), excess=str(gap),
                line_sha256=sha256(json.dumps(lines, separators=(",", ":")).encode()).hexdigest(),
                witness_sha256=fingerprint.hexdigest())


def rejected(function):
    try:
        function()
    except ValueError:
        return True
    raise AssertionError("bad certificate accepted")


def audit():
    edges, centered, packing, dual = gadget()
    require(len(edges) == 19 and len(centered) == 11, "gadget size")
    h = check_primal(edges, centered, [Q(1, 2)] * 11)
    require(h == check_dual(edges, centered, dual) == Q(11, 2), "gadget LP")
    require(check_packing(edges, packing) == 5, "gadget packing")
    direct = direct_gadget_optima(edges, centered)
    require((direct['cover'], direct['packing'], direct['centered_packing']) == (6, 5, 5),
            "direct gadget optima")
    for a in range(4):
        for b in range(4):
            require(polynomial_product(a, b) == PRODUCT[a][b], "field table")
    bad_primal = [Q(1, 2)] * 11
    bad_primal[0] = Q(3, 2)
    bad_dual = dict(dual)
    del bad_dual[(0, 3)]
    lines = affine_lines(2)
    controls = [
        rejected(lambda: check_primal(edges, centered, bad_primal)),
        rejected(lambda: check_dual(edges, centered, bad_dual)),
        rejected(lambda: check_packing(edges, packing + [packing[0]])),
        rejected(lambda: check_design(16, lines + [lines[0]])),
        rejected(lambda: check_design(16, lines[:-1])),
    ]
    families = [check_family(d) for d in range(1, 5)]
    return dict(status="all exact checks passed", gadget=dict(vertices=9, edges=19,
                centered_triangles=11, centered_fractional="11/2", **direct),
                negative_controls=len(controls), families=families)


if __name__ == '__main__':
    print(json.dumps(audit(), indent=2, sort_keys=True))
