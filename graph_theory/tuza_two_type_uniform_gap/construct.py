"""Exact bounds and deterministic witnesses for the uniform two-type gap.

Standard-library Python 3.10+. No optimal-cover or optimal-packing oracle.
The arithmetic bounds do not expand the six integer input parameters.
Witness construction uses O(k^3) time and O(k^2) memory/output.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
import argparse
import hashlib
import json


@dataclass(frozen=True)
class Parameters:
    a: int
    b: int
    c: int
    d: int
    m: int
    n: int

    def __post_init__(self):
        if any(type(v) is not int or v < 0 for v in self.as_tuple()):
            raise ValueError("all six parameters must be nonnegative integers")
        if self.k < 3:
            raise ValueError("this implementation requires clique order at least 3")

    def as_tuple(self):
        return self.a, self.b, self.c, self.d, self.m, self.n

    @property
    def k(self):
        return self.a + self.b + self.c + self.d

    @property
    def s(self):
        return self.a + self.c

    @property
    def t(self):
        return self.b + self.c

    @property
    def caps(self):
        return min(self.m, max(0, self.s - 1)), min(self.n, max(0, self.t - 1))


def arithmetic(p):
    """Return rational inequalities, not sampled or floating-point estimates."""
    k, s, t = p.k, p.s, p.t
    m, n = p.caps
    x, y = Q(m, s) if s else Q(0), Q(n, t) if t else Q(0)
    h_ideal = (x * s * s + y * t * t - x * y * p.c * p.c) / 2
    delta = 2 * h_ideal / (k * k)
    union = s + t - p.c
    total = m * s + n * t
    if 2 * union <= k:
        alpha, r, cover_density = Q(union, k), Q(0), Q(1, 4)
        if union:
            r = Q(total, union * k)
    else:
        alpha, r = Q(union, k), Q(total, union * k)
        z = min(alpha, (1 + r) / 2)
        cover_density = z * z - z + Q(1, 2) + r * (alpha - z)
    packing_density = max(delta, Q(1, 3) + 2 * delta * delta / 3)
    return {
        "H": h_ideal,
        "delta": delta,
        "alpha": alpha,
        "r": r,
        "F": cover_density,
        "p": packing_density,
        "packing_lower": k * k * packing_density / 2 - Q(k, 2),
        "cover_upper": k * k * cover_density - Q(k, 2) + Q(1, 4),
        "density_gap": packing_density - cover_density,
        "uniform_gap": Q(k * k, 228) - Q(k, 2) - Q(1, 4),
    }


def neighborhoods(p):
    # Common cell first, then S-only, T-only, and outside.
    common = set(range(p.c))
    s_set = common | set(range(p.c, p.c + p.a))
    t_set = common | set(range(p.c + p.a, p.c + p.a + p.b))
    return s_set, t_set


def color_matchings(vertices):
    vertices = sorted(vertices)
    size = len(vertices)
    classes = [[] for _ in range(size)]
    for i, j in combinations(range(size), 2):
        classes[(i + j) % size].append((vertices[i], vertices[j]))
    return classes


def make_witness(p):
    """A compressed cover and an explicit packing in the capped subgraph.

    Packing labels: clique 0..k-1, then m_cap S-centers, then n_cap
    T-centers. Extra original copies are not expanded. Retained sets
    describe the spokes kept at EVERY original vertex of each type.
    """
    k = p.k
    m, n = p.caps
    s_set, t_set = neighborhoods(p)
    classes_s, classes_t = color_matchings(s_set), color_matchings(t_set)

    def score_s(color):
        edges = classes_s[color]
        common_edges = sum(u in t_set and v in t_set for u, v in edges)
        return p.t * len(edges) - n * common_edges if p.t else len(edges)

    chosen_s = sorted(range(p.s), key=lambda i: (-score_s(i), i))[:m]
    base_edges = set()
    packing = []
    for center, color in enumerate(chosen_s, k):
        for u, v in classes_s[color]:
            base_edges.add((u, v))
            packing.append((u, v, center))

    def score_t(color):
        return sum(edge not in base_edges for edge in classes_t[color])

    chosen_t = sorted(range(p.t), key=lambda i: (-score_t(i), i))[:n]
    # Distinct T colors have disjoint base edges, so their scores remain valid.
    for center, color in enumerate(chosen_t, k + m):
        for u, v in classes_t[color]:
            if (u, v) not in base_edges:
                base_edges.add((u, v))
                packing.append((u, v, center))
    centered_size = len(packing)

    counts = [0] * k
    for u, v, w in combinations(range(k), 3):
        if not ({(u, v), (u, w), (v, w)} & base_edges):
            counts[(u + v + w) % k] += 1
    best_color = max(range(k), key=lambda i: (counts[i], -i))
    for u, v, w in combinations(range(k), 3):
        if ((u + v + w) % k == best_color
                and not ({(u, v), (u, w), (v, w)} & base_edges)):
            packing.append((u, v, w))

    # Exact optimal cut with both capped independent types on the same side.
    weights = [m * (v in s_set) + n * (v in t_set) for v in range(k)]
    order = sorted(range(k), key=lambda v: (-weights[v], v))
    total, prefix = sum(weights), 0
    best = None
    for ell in range(k + 1):
        internal = ell * (ell - 1) // 2 + (k - ell) * (k - ell - 1) // 2
        candidate = internal + total - prefix, ell
        if best is None or candidate < best:
            best = candidate
        if ell < k:
            prefix += weights[order[ell]]
    left = set(order[:best[1]])
    core = {edge for edge in combinations(range(k), 2)
            if (edge[0] in left) != (edge[1] in left)}
    retained = [s_set & left, t_set & left]
    for i, (neigh, original, cap) in enumerate(((s_set, p.m, m), (t_set, p.n, n))):
        if original > cap:
            core.difference_update(combinations(sorted(neigh), 2))
            retained[i] = set(neigh)
    deleted = sorted(set(combinations(range(k), 2)) - core)
    cover_size = (len(deleted) + p.m * (p.s - len(retained[0]))
                  + p.n * (p.t - len(retained[1])))
    if cover_size > best[0]:
        raise RuntimeError("multiplicity-cap lifting increased cover size")
    return {
        "parameters": list(p.as_tuple()),
        "caps": [m, n],
        "packing": [list(t) for t in packing],
        "centered_size": centered_size,
        "residual_color": best_color,
        "deleted_clique": [list(e) for e in deleted],
        "retained": [sorted(a) for a in retained],
        "cover_size": cover_size,
    }


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("counts", nargs=6, type=int, metavar="N")
    parser.add_argument("--construct", action="store_true", help="also build O(k^2)-size witnesses")
    args = parser.parse_args()
    p = Parameters(*args.counts)
    result = {key: str(value) for key, value in arithmetic(p).items()}
    if args.construct:
        witness = make_witness(p)
        result["witness"] = {"packing": len(witness["packing"]), "cover": witness["cover_size"],
                             "sha256": digest(witness)}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
