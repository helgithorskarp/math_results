"""Square-cell Euler counting and its exact topology CNF.

Cell (x,y) is the closed unit square [x,x+1] x [y,y+1].  Foreground
components use eight neighbours and complementary components use four.
"""
from collections import deque

FOUR = ((1, 0), (-1, 0), (0, 1), (0, -1))
EIGHT = tuple((x, y) for x in (-1, 0, 1) for y in (-1, 0, 1) if x or y)


def components(cells, directions):
    remaining = set(cells)
    result = []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        found, queue = {start}, deque([start])
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                p = x + dx, y + dy
                if p in remaining:
                    remaining.remove(p)
                    found.add(p)
                    queue.append(p)
        result.append(found)
    return result


def flood_counts(cells):
    """Independent components-and-holes computation, including the empty case."""
    cells = set(cells)
    if not cells:
        return 0, 0
    lo_x = min(x for x, y in cells) - 1
    hi_x = max(x for x, y in cells) + 1
    lo_y = min(y for x, y in cells) - 1
    hi_y = max(y for x, y in cells) + 1
    background = {(x, y) for x in range(lo_x, hi_x + 1)
                  for y in range(lo_y, hi_y + 1)} - cells
    return len(components(cells, EIGHT)), len(components(background, FOUR)) - 1


def local_counts(cells):
    cells = set(cells)
    adjacent = sum((x + 1, y) in cells for x, y in cells)
    adjacent += sum((x, y + 1) in cells for x, y in cells)
    anchors = {(x - dx, y - dy) for x, y in cells
               for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1))}
    full = diagonal = 0
    for x, y in anchors:
        bits = [(x, y) in cells, (x + 1, y) in cells,
                (x, y + 1) in cells, (x + 1, y + 1) in cells]
        full += all(bits)
        diagonal += bits in ([True, False, False, True],
                            [False, True, True, False])
    return len(cells), adjacent, full, diagonal


def cubical_counts(cells):
    """Separate explicit vertex/edge/face construction for the Euler check."""
    cells, vertices, edges = set(cells), set(), set()
    for x, y in cells:
        corners = [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]
        vertices.update(corners)
        for a, b in zip(corners, corners[1:] + corners[:1]):
            edges.add(tuple(sorted((a, b))))
    return len(vertices), len(edges), len(cells)


def topology_constraint(circuit, occupancy, strict_disc=False, euler_target=1):
    """Enforce the target Euler characteristic; the default is one.

    Missing cells in the finite occupancy mapping are fixed to false.  Return
    compact size statistics.  Connectedness is REQUIRED for the hole-count
    interpretation.  With strict_disc, diagonal pinches are forbidden.
    """
    if not occupancy:
        circuit.clause([])
        return {"cells": 0, "adjacency_terms": 0, "block_terms": 0}
    vertices = {(x - dx, y - dy) for x, y in occupancy
                for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1))}
    adjacent = [circuit.and_([v, occupancy[q]])
                for (x, y), v in sorted(occupancy.items())
                for q in ((x + 1, y), (x, y + 1)) if q in occupancy]
    full, diagonal = [], []
    for x, y in sorted(vertices):
        a, b, c, d = [occupancy.get(p, circuit.false)
                      for p in ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))]
        full.append(circuit.and_([a, b, c, d]))
        pinch = circuit.or_([circuit.and_([a, -b, -c, d]),
                             circuit.and_([-a, b, c, -d])])
        diagonal.append(pinch)
        if strict_disc:
            circuit.clause([-pinch])
    literals = [*occupancy.values(), *full, *(-x for x in adjacent),
                *(-x for x in diagonal)]
    circuit.equal_count(literals, len(adjacent) + len(diagonal) + euler_target)
    return {"cells": len(occupancy), "adjacency_terms": len(adjacent),
            "block_terms": len(vertices)}
