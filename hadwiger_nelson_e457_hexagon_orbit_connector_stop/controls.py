#!/usr/bin/env python3
"""Small semantic controls for the paired-hexagon connector verifier."""

from fractions import Fraction as F

import verify as V


def rejected(action, message):
    try:
        action()
    except (ValueError, TypeError):
        return
    raise ValueError(message)


def main():
    V.need(V.mul(V.SQRT3, V.SQRT3) == V.scale(V.ONE, 3), "sqrt(3) square")
    V.need(V.mul(V.SQRT47, V.SQRT47) == V.scale(V.ONE, 47), "sqrt(47) square")
    V.need(V.mul(V.SQRT3, V.SQRT47) == V.SQRT141, "mixed radical")
    points = V.connector_points()
    edges = V.complete_edges(points)
    V.need(len(edges) == 26, "edge count control")
    V.need(V.norm2(V.point_sub(points[0], points[1])) == V.scale(V.ONE, F(64, 9)),
           "terminal distance control")

    damaged = list(points)
    damaged[2] = V.point_add(damaged[2], (V.scale(V.ONE, F(1, 1000)), V.ZERO))
    rejected(
        lambda: V.need(V.complete_edges(damaged) == edges, "damaged geometry accepted"),
        "geometry control failed",
    )
    rejected(
        lambda: V.need(V.proper("33" + "010101" + "021212", edges, 4),
                       "damaged word accepted"),
        "colour control failed",
    )
    rejected(
        lambda: V.need(V.k_colourable(5, list(__import__("itertools").combinations(range(5), 2)), 4),
                       "K5 accepted"),
        "negative colouring control failed",
    )
    print("controls: 8 passed")


if __name__ == "__main__":
    main()
