#!/usr/bin/env python3
"""Exact exploratory four-circle supports with nonintegral Moser-angle layers.

Centres are the regular two-variable paired-circle obstruction placement.
For each owner circle, directions are U*rho^k and i*U*rho^k, where U is the
sixth-root orbit and rho=(5+i*sqrt(11))/6.  Geometry is exact in
Q(sqrt(3),sqrt(11)); colouring is a deterministic DSATUR backtrack.

Exploratory only: positive colour words are checked definition-first below;
an UNSAT return is not yet a proof certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import time


class Q:
    """Q(sqrt(3),sqrt(11)) in basis 1,sqrt3,sqrt11,sqrt33."""

    def __init__(self, values=()):
        values = list(values)
        values += [0] * (4 - len(values))
        if len(values) != 4:
            raise ValueError("bad coefficient count")
        self.c = tuple(Fraction(value) for value in values)

    def __add__(self, other):
        other = qq(other)
        return Q(a + b for a, b in zip(self.c, other.c))

    def __sub__(self, other):
        other = qq(other)
        return Q(a - b for a, b in zip(self.c, other.c))

    def __neg__(self):
        return Q(-value for value in self.c)

    def __mul__(self, other):
        other = qq(other)
        out = [Fraction(0)] * 4
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                common = i & j
                factor = (3 if common & 1 else 1) * (11 if common & 2 else 1)
                out[i ^ j] += a * b * factor
        return Q(out)

    def __truediv__(self, value):
        return Q(coefficient / Fraction(value) for coefficient in self.c)

    def __eq__(self, other):
        return self.c == qq(other).c

    def __hash__(self):
        return hash(self.c)


def qq(value):
    return value if isinstance(value, Q) else Q([value])


def cadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def csub(a, b):
    return a[0] - b[0], a[1] - b[1]


def cmul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def norm2(a):
    return a[0] * a[0] + a[1] * a[1]


def exact_graph(max_power, symmetric=False):
    zero, one = Q(), Q([1])
    s3, s11 = Q([0, 1]), Q([0, 0, 1])
    ii = (zero, one)
    omega = (one / 2, s3 / 2)
    rho = (Q([5]) / 6, s11 / 6)
    centres = [
        (zero, zero),
        (s3 / 2, Q([-1]) / 2),
        (one / 2, s3 / 2 - 1),
        (one, Q([-1])),
    ]
    rotations = [(one, zero)]
    for _ in range(5):
        rotations.append(cmul(rotations[-1], omega))
    phases = []
    positive = [(one, zero)]
    for _ in range(max_power):
        positive.append(cmul(positive[-1], rho))
    if symmetric:
        rho_inverse = (rho[0], -rho[1])
        negative = []
        power = (one, zero)
        for _ in range(max_power):
            power = cmul(power, rho_inverse)
            negative.append(power)
        powers = list(reversed(negative)) + positive
    else:
        powers = positive
    for power in powers:
        phases.extend([power, cmul(ii, power)])
    directions = []
    seen_directions = set()
    for phase in phases:
        for rotation in rotations:
            value = cmul(phase, rotation)
            if value not in seen_directions:
                seen_directions.add(value)
                directions.append(value)
    points = []
    addresses = []
    point_index = {}

    def add(point, address):
        if point not in point_index:
            point_index[point] = len(points)
            points.append(point)
            addresses.append([])
        addresses[point_index[point]].append(address)

    for owner, centre in enumerate(centres):
        add(centre, ["centre", owner])
    for owner, centre in enumerate(centres):
        for direction_index, direction in enumerate(directions):
            add(cadd(centre, direction), ["rim", owner, direction_index])
    edges = []
    adjacency = [set() for _ in points]
    unit = Q([1])
    for a in range(len(points)):
        for b in range(a + 1, len(points)):
            if norm2(csub(points[a], points[b])) == unit:
                edges.append((a, b))
                adjacency[a].add(b)
                adjacency[b].add(a)
    return centres, directions, points, addresses, edges, adjacency


def dsatur(adjacency, colour_count, node_limit=20_000_000):
    n = len(adjacency)
    colours = [-1] * n
    neighbour_masks = [0] * n
    degree = list(map(len, adjacency))
    nodes = 0
    # Break global colour symmetry at a maximum-degree vertex.
    first = max(range(n), key=lambda v: degree[v])
    colours[first] = 0
    for w in adjacency[first]:
        neighbour_masks[w] |= 1

    def rec(done):
        nonlocal nodes
        nodes += 1
        if nodes > node_limit:
            raise RuntimeError("node limit")
        if done == n:
            return tuple(colours)
        candidates = (v for v in range(n) if colours[v] < 0)
        v = max(candidates, key=lambda w: (neighbour_masks[w].bit_count(), degree[w]))
        forbidden = neighbour_masks[v]
        # Only introduce a new colour after every smaller colour is present.
        used_global = 0
        for value in colours:
            if value >= 0:
                used_global |= 1 << value
        max_allowed = min(colour_count - 1, used_global.bit_length())
        for colour in range(max_allowed + 1):
            bit = 1 << colour
            if forbidden & bit:
                continue
            colours[v] = colour
            changed = []
            for w in adjacency[v]:
                if colours[w] < 0 and not neighbour_masks[w] & bit:
                    neighbour_masks[w] |= bit
                    changed.append(w)
            answer = rec(done + 1)
            if answer is not None:
                return answer
            for w in changed:
                neighbour_masks[w] ^= bit
            colours[v] = -1
        return None

    answer = rec(1)
    return answer, nodes


def check_colouring(edges, colouring):
    return colouring is not None and all(colouring[a] != colouring[b] for a, b in edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-power", type=int, default=10)
    parser.add_argument("--node-limit", type=int, default=20_000_000)
    parser.add_argument("--symmetric", action="store_true")
    args = parser.parse_args()
    for power in range(args.maximum_power + 1):
        start = time.monotonic()
        centres, directions, points, addresses, edges, adjacency = exact_graph(power, args.symmetric)
        row = {
            "maximum_power": power,
            "directions": len(directions),
            "vertices": len(points),
            "edges": len(edges),
            "maximum_degree": max(map(len, adjacency)),
            "multi_address_vertices": sum(len(value) > 1 for value in addresses),
        }
        if len(points) > 508:
            row["status"] = "over_budget"
            print(json.dumps(row, sort_keys=True), flush=True)
            break
        for colour_count in (3, 4):
            try:
                colouring, nodes = dsatur(adjacency, colour_count, args.node_limit)
            except RuntimeError:
                row[f"colour_{colour_count}"] = "unknown_node_limit"
                row[f"nodes_{colour_count}"] = args.node_limit
                break
            row[f"colour_{colour_count}"] = bool(colouring)
            row[f"nodes_{colour_count}"] = nodes
            if colouring is not None:
                if not check_colouring(edges, colouring):
                    raise ValueError("invalid positive colouring")
                row[f"word_{colour_count}"] = "".join(map(str, colouring))
                break
        row["seconds"] = round(time.monotonic() - start, 3)
        print(json.dumps(row, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

