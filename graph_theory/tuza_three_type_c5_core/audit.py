"""Independent small-graph checks of both infinite reductions, not their proof.

Enumerate literal clique-core edge subsets and independent sets. This audit
does not use template colors to decide triangle-freeness or optimality.
"""
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations, product
import json
import cover


def require(condition, message):
    if not condition:
        raise ValueError(message)


def literal_graphs(k):
    pairs = list(combinations(range(k), 2))
    result = []
    for bits in range(1 << len(pairs)):
        neighbors = [0] * k
        for i, (a, b) in enumerate(pairs):
            if (bits >> i) & 1:
                neighbors[a] |= 1 << b
                neighbors[b] |= 1 << a
        if any((bits >> i) & 1 and neighbors[a] & neighbors[b]
               for i, (a, b) in enumerate(pairs)):
            continue
        alpha = [0] * (1 << k)
        for s in range(1, 1 << k):
            v = (s & -s).bit_length() - 1
            rest = s ^ (1 << v)
            alpha[s] = max(alpha[rest], 1 + alpha[rest & ~neighbors[v]])
        result.append((bits, bits.bit_count(), alpha))
    return pairs, result


def canonical(c):
    for p in permutations(range(3)):
        transform = [sum(((v >> i) & 1) << p[i] for i in range(3)) for v in range(8)]
        if tuple(c[transform[v]] for v in range(8)) > c:
            return False
    return True


def check_witness(answer):
    c, m, a = answer["cells"], answer["multiplicities"], answer["retained_cells"]
    table, x, index = answer["allocation"], answer["free_left"], answer["template_index"]
    require(len(c) == len(a) == len(table) == 8 and len(m) == 3, "dimensions")
    require(all(type(z) is int and z >= 0 for row in table for z in row), "entries")
    require(all(len(row) == 8 for row in table), "rows")
    require([sum(row) for row in table] == list(c), "original totals")
    require([sum(row[j] for row in table) for j in range(8)] == list(a), "retained totals")
    require(all(table[b][r] == 0 for b in range(8) for r in range(8) if b & r != r),
            "spokes outside original neighborhoods")
    require(type(x) is int and 0 <= x <= a[0], "free split")
    require(type(index) is int and 0 <= index < len(cover.TEMPLATES), "template index")
    original, retained = [], []
    for b in range(8):
        for r in range(8):
            original.extend([b] * table[b][r])
            retained.extend([r] * table[b][r])
    labels, free_seen = [], 0
    for r in retained:
        if r:
            labels.append(r - 1)
        else:
            labels.append(7 if free_seen < x else 8)
            free_seen += 1
    edges, left, right, colors = cover.TEMPLATES[index]
    allowed = {tuple(sorted((b - 1, r - 1))) for b, r in edges}
    allowed.update((b - 1, 7) for b in left)
    allowed.update((b - 1, 8) for b in right)
    allowed.add((7, 8))
    k = len(labels)
    core = [(i, j) for i in range(k) for j in range(i + 1, k)
            if tuple(sorted((labels[i], labels[j]))) in allowed]
    neighbors = [set() for _ in range(k)]
    for i, j in core:
        neighbors[i].add(j)
        neighbors[j].add(i)
        require(not (retained[i] & retained[j]), "protected clique edge")
        require((colors[labels[i]] - colors[labels[j]]) % 5 in (1, 4), "C5 map")
    require(all(not (neighbors[i] & neighbors[j]) for i, j in core), "core triangle")
    spokes = sum(m[i] * sum((r >> i) & 1 for r in retained) for i in range(3))
    total = k * (k - 1) // 2 + sum(m[i] * sum((r >> i) & 1 for r in original)
                                   for i in range(3))
    require(answer["surviving_edges"] == len(core) + spokes, "surviving edge count")
    require(answer["tau"] == total - len(core) - spokes, "cover size")
    return len(core)


def run():
    digest = sha256()
    core_cases = cover_cases = shape_cases = 0
    graph_counts = {}
    require(len(cover.UPPER_SETS) == 18, "upper set count")
    for k in range(6):
        pairs, graphs = literal_graphs(k)
        graph_counts[k] = len(graphs)
        vectors = list(cover.compositions(k, 8))
        values = {}
        for a in vectors:
            masks = [v for v in range(8) for _ in range(a[v])]
            host = sum(1 << j for j, (b, c) in enumerate(pairs) if not (masks[b] & masks[c]))
            direct = max(e for bits, e, _ in graphs if bits & ~host == 0)
            calculated = cover.core_maximum(a)[0]
            require(direct == calculated, "protected-host optimum mismatch")
            values[a] = calculated
            core_cases += 1
            digest.update(json.dumps(["core", a, direct], separators=(",", ":")).encode())
        for c in vectors:
            if not canonical(c):
                continue
            shape_cases += 1
            masks = [v for v in range(8) for _ in range(c[v])]
            sets = [sum(1 << j for j, v in enumerate(masks) if (v >> i) & 1)
                    for i in range(3)]
            literal = [(e, tuple(alpha[s] for s in sets)) for _, e, alpha in graphs]
            reduced = [(values[a], tuple(sum(a[b] for b in range(8) if (b >> i) & 1)
                                        for i in range(3))) for a in vectors if cover.feasible(a, c)]
            for m in product(range(3), repeat=3):
                expected = max(e + sum(m[i] * sizes[i] for i in range(3)) for e, sizes in literal)
                actual = max(e + sum(m[i] * sizes[i] for i in range(3)) for e, sizes in reduced)
                require(actual == expected, "three-type cover optimum mismatch")
                cover_cases += 1
                digest.update(json.dumps(["cover", c, m, actual], separators=(",", ":")).encode())
    examples = []
    for c, m in [((0,) * 8, (0, 1, 2)), ((0, 1, 0, 0, 0, 0, 0, 0), (10**20, 2, 3)),
                 ((0, 0, 0, 0, 0, 0, 0, 5), (1, 2, 1)),
                 ((1, 1, 0, 2, 1, 0, 2, 0), (22, 22, 22))]:
        answer = cover.solve(c, m)
        core_edges = check_witness(answer)
        examples.append({"cells": c, "multiplicities": m, "tau": answer["tau"],
                         "core_edges": core_edges})
    require(examples[-1]["tau"] == 12 and examples[-1]["core_edges"] == 9,
            "known three-type odd-core obstruction")
    original = cover.solve((1, 1, 0, 2, 1, 0, 2, 0), (22, 22, 22))
    rejected = 0
    for kind in range(4):
        bad = deepcopy(original)
        if kind == 0:
            bad["free_left"] = 2
        elif kind == 1:
            bad["tau"] += 1
        elif kind == 2:
            bad["allocation"][0][0] += 1
        else:
            bad["template_index"] = 392
        try:
            check_witness(bad)
        except ValueError:
            rejected += 1
    require(rejected == 4, "malformed witness accepted")
    return {"protected_hosts": core_cases, "three_type_shapes": shape_cases,
            "cover_instances": cover_cases, "literal_triangle_free_graph_counts": graph_counts,
            "upper_set_constraints": len(cover.UPPER_SETS), "examples": examples,
            "malformed_witnesses_rejected": rejected, "record_sha256": digest.hexdigest()}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
