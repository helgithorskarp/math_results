#!/usr/bin/env python3
"""Exact power-ladder expansions of the common-neighbour Moser seed.

Fix C={1,omega,rho,rho*omega}, where omega=exp(pi*i/3) and
rho=(5+i*sqrt(11))/6.  For successively larger exact direction pools D,
form X={0} union C union (C+D).  Stop before 509 vertices.  Positive
colourings are definition-first witnesses; an UNSAT result is provisional
until independently certified.
"""

from __future__ import annotations

import argparse
import json
import time

from scratch_common_neighbor_sumsets import graph_for_centres
from scratch_four_circle_moser_layers import Q, cmul, dsatur


def geometry(maximum_power, symmetric, include_i):
    zero, one = Q(), Q([1])
    omega = (one / 2, Q([0, 1]) / 2)
    rho = (Q([5]) / 6, Q([0, 0, 1]) / 6)
    ii = (zero, one)
    rotations = [(one, zero)]
    for _ in range(5):
        rotations.append(cmul(rotations[-1], omega))

    positive = [(one, zero)]
    for _ in range(maximum_power):
        positive.append(cmul(positive[-1], rho))
    powers = positive
    if symmetric:
        rho_inverse = (rho[0], -rho[1])
        negative, power = [], (one, zero)
        for _ in range(maximum_power):
            power = cmul(power, rho_inverse)
            negative.append(power)
        powers = list(reversed(negative)) + positive

    phases = []
    for power in powers:
        phases.append(power)
        if include_i:
            phases.append(cmul(ii, power))
    directions, seen = [], set()
    for phase in phases:
        for rotation in rotations:
            value = cmul(phase, rotation)
            if value not in seen:
                seen.add(value)
                directions.append(value)
    centres = [(one, zero), omega, rho, cmul(rho, omega)]
    return centres, directions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-power", type=int, default=20)
    parser.add_argument("--symmetric", action="store_true")
    parser.add_argument("--include-i", action="store_true")
    parser.add_argument("--node-limit", type=int, default=20_000_000)
    args = parser.parse_args()
    first_power = 1
    for maximum_power in range(first_power, args.maximum_power + 1):
        started = time.monotonic()
        centres, directions = geometry(maximum_power, args.symmetric, args.include_i)
        points, addresses, edges, adjacency = graph_for_centres(centres, directions)
        row = {
            "maximum_power": maximum_power,
            "symmetric": args.symmetric,
            "include_i": args.include_i,
            "directions": len(directions),
            "vertices": len(points),
            "edges": len(edges),
            "maximum_degree": max(map(len, adjacency)),
            "multi_address_vertices": sum(len(value) > 1 for value in addresses),
        }
        if len(points) > 508:
            row["status"] = "OVER_RECORD_BOUNDARY"
            print(json.dumps(row, sort_keys=True), flush=True)
            break
        try:
            four, nodes4 = dsatur(adjacency, 4, args.node_limit)
        except RuntimeError:
            four, nodes4 = "unknown", args.node_limit
        row["nodes4"] = nodes4
        if four == "unknown":
            row["colour4"] = "unknown"
        elif four is None:
            row["colour4"] = False
            row["status"] = "NONCOLOUR4_PROVISIONAL"
        else:
            if not all(four[a] != four[b] for a, b in edges):
                raise ValueError("invalid four-colouring")
            row["colour4"] = True
            try:
                three, nodes3 = dsatur(adjacency, 3, args.node_limit)
            except RuntimeError:
                three, nodes3 = "unknown", args.node_limit
            row["nodes3"] = nodes3
            if three == "unknown":
                row["colour3"] = "unknown"
            else:
                if three is not None and not all(three[a] != three[b] for a, b in edges):
                    raise ValueError("invalid three-colouring")
                row["colour3"] = three is not None
        row["seconds"] = round(time.monotonic() - started, 3)
        print(json.dumps(row, sort_keys=True), flush=True)
        if four is None or four == "unknown":
            break


if __name__ == "__main__":
    main()

