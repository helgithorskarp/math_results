#!/usr/bin/env python3
"""Exact constructors for the claims in PROOF.md; Python standard library only."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations
import json
from pathlib import Path


def pairs(n):
    return list(combinations(range(n), 2))


@lru_cache(None)
def permutation_maps(n):
    edges = pairs(n)
    indices = {edge: i for i, edge in enumerate(edges)}
    return tuple(tuple(1 << indices[tuple(sorted((p[a], p[b])))]
                       for a, b in edges) for p in permutations(range(n)))


def canonical_graph(n, mask):
    occupied = [i for i in range(n * (n - 1) // 2) if (mask >> i) & 1]
    return min(sum(mapping[i] for i in occupied)
               for mapping in permutation_maps(n))


def graph_classes(max_n):
    """All simple graphs, up to isomorphism, by unrestricted vertex extension."""
    previous = [0]
    answer = {0: previous}
    for n in range(1, max_n + 1):
        indices = {edge: i for i, edge in enumerate(pairs(n))}
        old_edges = pairs(n - 1)
        candidates = set()
        for mask in previous:
            embedded = sum(1 << indices[edge] for i, edge in enumerate(old_edges)
                           if (mask >> i) & 1)
            for neighbors in range(1 << (n - 1)):
                extended = embedded | sum(1 << indices[(v, n - 1)]
                                          for v in range(n - 1)
                                          if (neighbors >> v) & 1)
                candidates.add(extended)
        previous = sorted({canonical_graph(n, mask) for mask in candidates})
        answer[n] = previous
    return answer


def graph_family(n, mask):
    return sorted([0] + [1 << v for v in range(n)] +
                  [(1 << a) | (1 << b) for i, (a, b) in enumerate(pairs(n))
                   if (mask >> i) & 1])


def star_size(family):
    support = 0
    for a in family:
        support |= a
    return max((sum(bool(a & (1 << v)) for a in family)
                for v in range(support.bit_length())), default=0)


def edge_coloring(n, mask):
    """Small exact search; the infinite existence proof uses Vizing, not search."""
    edges = [edge for i, edge in enumerate(pairs(n)) if (mask >> i) & 1]
    degree = [sum(v in edge for edge in edges) for v in range(n)]
    t = 1 + max(degree, default=0)
    used = [0] * n
    colors = {}
    full = (1 << t) - 1

    def visit(remaining, introduced):
        if not remaining:
            return True
        options = []
        for edge in remaining:
            a, b = edge
            available = full & ~(used[a] | used[b])
            options.append((available.bit_count(), edge, available))
        _, edge, available = min(options)
        a, b = edge
        rest = [e for e in remaining if e != edge]
        for c in range(min(introduced + 1, t)):
            bit = 1 << c
            if not available & bit:
                continue
            colors[edge] = c
            used[a] |= bit
            used[b] |= bit
            if visit(rest, max(introduced, c + 1)):
                return True
            used[a] ^= bit
            used[b] ^= bit
            del colors[edge]
        return False

    if not visit(edges, 0):
        raise RuntimeError("Completed search failed: contradicts Vizing or code bug")
    result = {(1 << a) | (1 << b): c for (a, b), c in colors.items()}
    for v in range(n):
        result[1 << v] = next(c for c in range(t) if not used[v] & (1 << c))
    return t, [result[a] for a in graph_family(n, mask)[1:]]


def equitable_colors(n, family, colors, t):
    """Balance an edge coloring after replacing each singleton by a pendant edge."""
    edges = []
    for a in family[1:]:
        vertices = [v for v in range(n) if a & (1 << v)]
        if len(vertices) == 1:
            v = vertices[0]
            edges.append((v, n + v))
        elif len(vertices) == 2:
            edges.append(tuple(vertices))
        else:
            raise ValueError("Equitable recoloring is only for rank-two families")
    result = colors[:]
    while True:
        counts = [result.count(c) for c in range(t)]
        high = max(range(t), key=lambda c: (counts[c], -c))
        low = min(range(t), key=lambda c: (counts[c], c))
        if counts[high] - counts[low] <= 1:
            return result
        incident = [[] for _ in range(2 * n)]
        unseen = {i for i, c in enumerate(result) if c in (high, low)}
        for i in unseen:
            for v in edges[i]:
                incident[v].append(i)
        chosen = None
        while unseen:
            stack = [min(unseen)]
            component = set()
            while stack:
                i = stack.pop()
                if i not in unseen:
                    continue
                unseen.remove(i)
                component.add(i)
                for v in edges[i]:
                    stack.extend(incident[v])
            difference = sum(1 if result[i] == high else -1 for i in component)
            if difference == 1:
                chosen = component
                break
        if chosen is None:
            raise RuntimeError("Bicolored path decomposition invariant failed")
        for i in chosen:
            result[i] = low if result[i] == high else high


def rank_two_certificate(n, mask, shift=0):
    family = graph_family(n, mask)
    t, colors = edge_coloring(n, mask)
    colors = equitable_colors(n, family, colors, t)
    return [a << shift for a in family], coloring_certificate(colors, t), t


def lift(core, t):
    """Empty-vertex lift; core is indexed by the nonempty sets."""
    m = len(core)
    n = m + 1
    if not 0 < t < n or any(len(row) != m for row in core):
        raise ValueError("Invalid lift dimensions or bound")
    sums = [sum(row) for row in core]
    q = [[F(sum(sums))] + [-F(a) for a in sums]]
    q += [[-F(sums[i])] + [F(a) for a in core[i]] for i in range(m)]
    return [[(q[i][j] + 1 - (t if i == j else 0)) / (n - t)
             for j in range(n)] for i in range(n)]


def coloring_certificate(colors, t):
    return lift([[t * int(a == b) - 1 for b in colors] for a in colors], t)


def extract_core(matrix, t):
    n = len(matrix)
    return [[(n - t) * matrix[i][j] + (t if i == j else 0) - 1
             for j in range(1, n)] for i in range(1, n)]


def union_certificate(components):
    """Components (family, matrix, s) must have disjoint coordinate supports."""
    support = 0
    t = max(s for _, _, s in components)
    entries = []
    blocks = []
    for family, matrix, s in components:
        current = 0
        for a in family:
            current |= a
        if support & current:
            raise ValueError("Union requires disjoint supports")
        support |= current
        core = extract_core(matrix, s)
        for i in range(len(core)):
            core[i][i] += t - s
        blocks.append(core)
        entries.extend(family[1:])
    size = len(entries)
    core = [[F(0) for _ in range(size)] for _ in range(size)]
    offset = 0
    for block in blocks:
        for i, row in enumerate(block):
            core[offset + i][offset:offset + len(row)] = row
        offset += len(block)
    return [0] + entries, lift(core, t), t


def restrict_certificate(family, matrix, t, retained):
    if not retained or retained[0] != 0 or star_size(retained) != t:
        raise ValueError("Restriction must retain empty set and largest-star size")
    index = {a: i - 1 for i, a in enumerate(family) if a}
    core = extract_core(matrix, t)
    sub = [[core[index[a]][index[b]] for b in retained[1:]]
           for a in retained[1:]]
    return lift(sub, t)


def cube_certificate(k, shift=0):
    if k < 1:
        raise ValueError("Nontrivial cube required")
    n = 1 << k
    family = [a << shift for a in range(n)]
    matrix = [[F(int(b == (n - 1) ^ a)) for b in range(n)] for a in range(n)]
    return family, matrix, n // 2


def matching_certificate(k, isolated=0, shift=0):
    """k disjoint graph edges and isolated singleton coordinates."""
    if k < 0 or isolated < 0 or k + isolated == 0:
        raise ValueError("Nontrivial matching family required")
    family = [0]
    colored = {}
    balance = 0
    for j in range(k):
        a, b = 1 << (shift + 2 * j), 1 << (shift + 2 * j + 1)
        # Each triple contributes +1 or -1 to the class-size difference.
        edge_color = 0 if balance >= 0 else 1
        colored[a | b] = edge_color
        colored[a] = colored[b] = 1 - edge_color
        balance += -1 if edge_color == 0 else 1
    for j in range(isolated):
        a = 1 << (shift + 2 * k + j)
        color = 0 if balance <= 0 else 1
        colored[a] = color
        balance += 1 if color == 0 else -1
    family += sorted(colored)
    t = 2 if k else 1
    colors = [colored[a] if k else 0 for a in family[1:]]
    return family, coloring_certificate(colors, t), t


def product_certificate(components):
    """Tensor constructor. Callers must verify BOTH spectral bounds on factors."""
    family, matrix = [0], [[F(1)]]
    support = 0
    total = 1
    proportions = []
    for other, factor, s in components:
        current = 0
        for a in other:
            current |= a
        if support & current:
            raise ValueError("Product requires disjoint coordinate supports")
        support |= current
        old_size, new_size = len(family), len(other)
        family = [a | b for a in family for b in other]
        matrix = [[matrix[i][j] * factor[a][b]
                   for j in range(old_size) for b in range(new_size)]
                  for i in range(old_size) for a in range(new_size)]
        total *= new_size
        proportions.append(F(s, new_size))
    bound = total * max(proportions)
    if bound.denominator != 1:
        raise RuntimeError("Nonintegral product-star size")
    return family, matrix, int(bound)


def main():
    classes = graph_classes(6)
    fixtures = []
    for n in range(1, 7):
        for mask in classes[n]:
            t, colors = edge_coloring(n, mask)
            colors = equitable_colors(n, graph_family(n, mask), colors, t)
            fixtures.append({"n": n, "edge_mask": mask, "s": t, "colors": colors})
    path = Path(__file__).with_name("rank_two_certificates.json")
    path.write_text(json.dumps(fixtures, separators=(",", ":")) + "\n")
    print(json.dumps({"classes_by_active_coordinates": {
        str(n): len(classes[n]) for n in range(1, 7)},
        "nontrivial_rank_two_classes": len(fixtures)}, sort_keys=True))


if __name__ == "__main__":
    main()
