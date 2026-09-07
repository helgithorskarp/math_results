#!/usr/bin/env python3
"""Small definition-level and certificate-format controls."""

import json

from colour import colour_graph, pack_row, unpack_row, valid_colouring
from model import (
    FOUR,
    ONE,
    direct_unit_edges,
    make_placement,
    mul,
    source_distance_edges,
    source_points,
    unit_graph,
)


def main():
    # Basis multiplication controls.
    sqrt3 = (0, 1, 0, 0)
    sqrt11 = (0, 0, 1, 0)
    sqrt33 = (0, 0, 0, 1)
    if mul(sqrt3, sqrt11) != sqrt33:
        raise AssertionError("sqrt(3)*sqrt(11) control failed")
    if mul(sqrt33, sqrt33) != (33, 0, 0, 0):
        raise AssertionError("sqrt(33)^2 control failed")

    base = source_points()
    unit, long = source_distance_edges(base)
    if (len(base), len(unit), len(long)) != (26, 75, 10):
        raise AssertionError("source control failed")

    graph_rows = []
    for reflected in (False, True):
        moved = make_placement(base, (3, 12), (0, 2), reflected)
        points, fast_edges = unit_graph(base, moved)
        slow_edges = direct_unit_edges(points)
        if fast_edges != slow_edges:
            raise AssertionError("origin-case edge construction missed an edge")
        row, _nodes = colour_graph(len(points), fast_edges, 4)
        if not valid_colouring(len(points), fast_edges, row):
            raise AssertionError("positive colouring control failed")
        packed = pack_row(row)
        if unpack_row(packed, len(points)) != row:
            raise AssertionError("colour packing round trip failed")
        broken = list(row)
        left, right = fast_edges[0]
        broken[left] = broken[right]
        if valid_colouring(len(points), fast_edges, broken):
            raise AssertionError("corrupted colouring was accepted")
        graph_rows.append({
            "reflected": reflected,
            "vertices": len(points),
            "edges": len(fast_edges),
        })

    malformed = bytearray(13)
    malformed[-1] = 1 << 6  # nonzero colour in padded position 51
    try:
        unpack_row(bytes(malformed), 49)
    except ValueError:
        padding_rejected = True
    else:
        raise AssertionError("nonzero certificate padding was accepted")

    print(json.dumps({
        "status": "controls passed",
        "field_products": ["sqrt(3)*sqrt(11)=sqrt(33)", "sqrt(33)^2=33"],
        "source": {"vertices": 26, "unit_edges": 75, "length_two_edges": 10},
        "definition_level_graph_comparisons": graph_rows,
        "corrupted_colouring_rejected": True,
        "nonzero_padding_rejected": padding_rejected,
        "floating_point_operations": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
