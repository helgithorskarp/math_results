#!/usr/bin/env python3
"""Clean-room exact audit of the endpoint-block certificate.

This file deliberately imports no code from the reviewed packet.  It uses
definition-level rational distance tests, Boolean transitive closure, brute
ordered partitions, and minor enumeration rather than the producer's SCC and
row-reduction routines.
"""

from fractions import Fraction as F
from itertools import combinations, permutations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_endpoint_block_classification"


def q(x):
    if type(x) is int or isinstance(x, str):
        return F(x)
    raise ValueError("non-rational JSON coordinate")


def load_points(raw):
    return [tuple(q(x) for x in row) for row in raw]


def d2(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def det(a):
    n = len(a)
    if n == 0:
        return F(1)
    total = F(0)
    for perm in permutations(range(n)):
        inversions = sum(
            perm[i] > perm[j] for i in range(n) for j in range(i + 1, n)
        )
        term = F(-1 if inversions % 2 else 1)
        for i in range(n):
            term *= a[i][perm[i]]
        total += term
    return total


def minor_rank(a):
    """Rank over Q by exhaustive nonzero minors, independent of row reduction."""
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    for k in range(min(rows, cols), 0, -1):
        for rr in combinations(range(rows), k):
            for cc in combinations(range(cols), k):
                if det([[a[i][j] for j in cc] for i in rr]):
                    return k
    return 0


def graph(p, r):
    moved = [i for i in range(len(p)) if p[i] != r[i]]
    arcs = set()
    for i in moved:
        for j in moved:
            if i == j:
                continue
            lo, hi = d2(r[i], r[j]), d2(p[i], p[j])
            mixed = d2(r[i], p[j])
            if not (lo <= mixed <= hi):
                arcs.add((j, i))
    return moved, arcs


def closure(vertices, arcs):
    reach = {(i, i) for i in vertices} | set(arcs)
    for k in vertices:
        for i in vertices:
            if (i, k) not in reach:
                continue
            for j in vertices:
                if (k, j) in reach:
                    reach.add((i, j))
    return reach


def sccs(vertices, arcs):
    reach = closure(vertices, arcs)
    unseen, groups = set(vertices), []
    while unseen:
        i = min(unseen)
        group = frozenset(j for j in vertices if (i, j) in reach and (j, i) in reach)
        groups.append(group)
        unseen -= group
    return groups


def ordered_partitions(labels):
    if not labels:
        yield []
        return
    last = labels[-1]
    for old in ordered_partitions(labels[:-1]):
        for i in range(len(old)):
            new = [block[:] for block in old]
            new[i].append(last)
            yield new
        for i in range(len(old) + 1):
            yield old[:i] + [[last]] + old[i:]


def order_valid(partition, arcs):
    time = {v: t for t, block in enumerate(partition) for v in block}
    return all(time[u] <= time[v] for u, v in arcs)


def block_rows(p, r, indices):
    displacement = [list(sub(r[i], p[i])) for i in indices]
    augmented = [
        row + [(dot(r[i], r[i]) - dot(p[i], p[i])) / 2]
        for row, i in zip(displacement, indices)
    ]
    return displacement, augmented


def assert_contraction(p, r):
    assert len(p) == len(r) and len(set(p)) == len(p)
    assert all(d2(r[i], r[j]) <= d2(p[i], p[j])
               for i in range(len(p)) for j in range(i))


def check_certificate(p, r, certificate):
    moved, arcs = graph(p, r)
    asserted_arcs = {tuple(edge) for edge in certificate["precedence_edges"]}
    assert arcs == asserted_arcs
    groups = set(sccs(moved, arcs))
    stated_groups = {frozenset(block["indices"]) for block in certificate["blocks"]}
    assert groups == stated_groups

    valid = [part for part in ordered_partitions(moved) if order_valid(part, arcs)]
    optimum = min(max(map(len, part), default=0) for part in valid)
    assert optimum == certificate["minimum_maximum_switch_batch"] == 3

    current = p[:]
    for block in certificate["blocks"]:
        following = current[:]
        for i in block["indices"]:
            following[i] = r[i]
        assert all(d2(following[i], following[j]) <= d2(current[i], current[j])
                   for i in range(len(p)) for j in range(i))
        displacement, augmented = block_rows(p, r, block["indices"])
        rd, ra = minor_rank(displacement), minor_rank(augmented)
        assert (rd, ra) == (3, 3)
        anchor = tuple(q(x) for x in block["anchor"])
        assert all(d2(p[i], anchor) == d2(r[i], anchor)
                   for i in block["indices"])
        current = following
    assert current == r

    full_d, full_a = block_rows(p, r, moved)
    assert (minor_rank(full_d), minor_rank(full_a)) == (3, 4)
    return moved, arcs, groups, valid


def abstract_graph_census():
    vertices = list(range(4))
    possible = [(i, j) for i in vertices for j in vertices if i != j]
    partitions = list(ordered_partitions(vertices))
    histogram = {str(k): 0 for k in range(1, 5)}
    for mask in range(1 << len(possible)):
        arcs = {arc for bit, arc in enumerate(possible) if mask >> bit & 1}
        optimum = min(
            max(map(len, part)) for part in partitions if order_valid(part, arcs)
        )
        predicted = max(map(len, sccs(vertices, arcs)))
        assert optimum == predicted
        histogram[str(optimum)] += 1
    return len(partitions), histogram


def layered(m):
    p = [(F(2), F(2), F(2)), (F(3), F(2), F(2)),
         (F(2), F(3), F(2)), (F(2), F(2), F(3))]
    r = p[:]
    rays = [(F(1, 3), F(2, 3), F(2, 3)),
            (F(2, 3), F(1, 3), F(2, 3)),
            (F(6, 7), F(2, 7), F(3, 7))]
    for k in range(m):
        scale = F(8**k)
        for i, ray in enumerate(rays):
            p.append(tuple(-scale if j == i else F(0) for j in range(3)))
            r.append(tuple(F(3, 4) * scale * x for x in ray))
    return p, r


def layered_family_check():
    records = []
    for m in range(1, 6):
        p, r = layered(m)
        assert_contraction(p, r)
        moved, arcs = graph(p, r)
        groups = sccs(moved, arcs)
        assert sorted(map(len, groups)) == [3] * m
        for group in groups:
            d, a = block_rows(p, r, sorted(group))
            assert (minor_rank(d), minor_rank(a)) == (3, 3)
        d, a = block_rows(p, r, moved)
        ranks = (minor_rank(d), minor_rank(a))
        assert ranks == ((3, 3) if m == 1 else (3, 4))
        records.append({"layers": m, "components": len(groups),
                        "whole_ranks": list(ranks)})
    p, r = layered(1)
    paired = [list(p[i]) + list(r[i]) for i in range(7)]
    affine = [[x - y for x, y in zip(row, paired[0])] for row in paired[1:]]
    assert minor_rank(affine) == 6
    return records


def loss_telescope(p, r, certificate):
    n = len(p)
    denom = n * (n + 1) // 2
    weights = [F(i + 1, denom) for i in range(n)]

    def loss(x, y):
        return sum(
            weights[i] * weights[j] * (d2(x[i], x[j]) - d2(y[i], y[j]))
            for i in range(n) for j in range(n)
        )

    total = loss(p, r)
    stage, current = [], p[:]
    for block in certificate["blocks"]:
        following = current[:]
        for i in block["indices"]:
            following[i] = r[i]
        stage.append(loss(current, following))
        current = following
    assert all(x >= 0 for x in stage) and sum(stage) == total
    return str(total), [str(x) for x in stage]


def main():
    data = json.loads((TARGET / "INPUT.json").read_text())
    certificate = json.loads((TARGET / "CERTIFICATE.json").read_text())
    p, r = load_points(data["source"]), load_points(data["target"])
    assert_contraction(p, r)
    moved, arcs, groups, valid = check_certificate(p, r, certificate)
    weak_orders, histogram = abstract_graph_census()
    total_loss, stage_losses = loss_telescope(p, r, certificate)
    result = {
        "status": "INDEPENDENT_ENDPOINT_BLOCK_AUDIT_PASS",
        "arithmetic": "fractions.Fraction and exhaustive integer determinants",
        "imports_reviewed_code": False,
        "fixture_movers": len(moved),
        "fixture_arcs": len(arcs),
        "fixture_sccs": sorted(sorted(group) for group in groups),
        "fixture_valid_weak_orders": len(valid),
        "fixture_minimum_maximum_batch": 3,
        "directed_graphs_checked": 4096,
        "weak_orders_per_four_vertex_graph": weak_orders,
        "minimum_batch_histogram": histogram,
        "whole_fixture_ranks": [3, 4],
        "ordered_loss": total_loss,
        "stage_ordered_losses": stage_losses,
        "layered_family": layered_family_check(),
        "analytic_transfer_formalized": False,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
