"""Axial regular-hexagon geometry and independent signed-corona checker."""
import itertools

NEIGHBORS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
turns_count = 6


def boundary(tile):
    cells = set(map(tuple, tile))
    return sorted((c, (c[0] + dx, c[1] + dy)) for c in cells
                  for dx, dy in NEIGHBORS if (c[0] + dx, c[1] + dy) not in cells)


def transform(p, reflect, turns):
    x, y = p
    if reflect:
        x, y = x + y, -y
    for _ in range(turns):
        x, y = -y, x + y
    return x, y


def oriented(tile, reflect, turns):
    raw = [transform(p, reflect, turns) for p in tile]
    x0, y0 = min(x for x, y in raw), min(y for x, y in raw)
    cells = tuple(sorted((x - x0, y - y0) for x, y in raw))
    ports = []
    for owner, neighbor in boundary(tile):
        a, b = [transform(p, reflect, turns) for p in (owner, neighbor)]
        a, b = (a[0] - x0, a[1] - y0), (b[0] - x0, b[1] - y0)
        ends = tuple(sorted((a, b)))
        ports.append((ends, 0 if ends[0] == a else 1))
    return cells, ports


def halo(tile):
    cells = set(tile)
    return {(x + dx, y + dy) for x, y in cells for dx, dy in NEIGHBORS} - cells


def span(tile):
    return 1 + max(max(f(x, y) for x, y in tile) - min(f(x, y) for x, y in tile)
                   for f in (lambda x, y: x, lambda x, y: y, lambda x, y: x + y))


def extra_overhang(cells, root):
    """The third axial projection obeys the same contact-radius bound."""
    lo, hi = min(x + y for x, y in root), max(x + y for x, y in root)
    return max(0, lo - min(x + y for x, y in cells),
               max(x + y for x, y in cells) - hi)


def topology_constraint(circuit, occupancy, strict_disc=True):
    """For connected polyhexes, chi=F-A+T and disc iff chi=1."""
    if not occupancy:
        circuit.clause([])
        return {}
    adjacent = [circuit.and_([z, occupancy[n]]) for (x, y), z in sorted(occupancy.items())
                for n in ((x + 1, y), (x, y + 1), (x - 1, y + 1)) if n in occupancy]
    triples = [circuit.and_([z, occupancy[a], occupancy[b]])
               for (x, y), z in sorted(occupancy.items())
               for a, b in (((x + 1, y), (x, y + 1)), ((x + 1, y), (x + 1, y - 1)))
               if a in occupancy and b in occupancy]
    circuit.equal_count([*occupancy.values(), *triples, *(-x for x in adjacent)], len(adjacent) + 1)
    return {"cells": len(occupancy), "adjacency_terms": len(adjacent), "triple_terms": len(triples)}


def check_witness(witness):
    from marked_corona import component_count
    tile = tuple(map(tuple, witness["tile"]))
    if not tile or len(set(tile)) != len(tile) or any(len(v) != 2 or any(type(z) is not int for z in v) for v in tile):
        raise ValueError("invalid base cells")
    if min(x for x, y in tile) or min(y for x, y in tile):
        raise ValueError("base cells must be normalized")
    if component_count(tile, NEIGHBORS) != 1:
        raise ValueError("disconnected base")
    original_ports = {port: i for i, port in enumerate(boundary(tile))}
    signs, depth = witness["signs"], witness["depth"]
    if type(depth) is not int or depth < 0 or len(signs) != len(original_ports) or any(type(s) is not int or s not in (-1, 0, 1) for s in signs):
        raise ValueError("invalid labels or depth")
    levels = [set() for _ in range(depth + 1)]
    copies, edge_labels = [], {}
    roots = 0
    for record in witness["patch"]:
        k, reflect, turns = record["level"], record["reflect"], record["turns"]
        if type(k) is not int or not 0 <= k <= depth or type(reflect) is not bool or type(turns) is not int or not 0 <= turns < 6:
            raise ValueError("invalid motion or level")
        tx, ty = record["translation"]
        if type(tx) is not int or type(ty) is not int:
            raise ValueError("invalid translation")

        def forward(p):
            a, b = p
            if reflect:
                a, b = a + b, -b
            for _ in range(turns):
                a, b = -b, a + b
            return a, b

        raw = [forward(p) for p in tile]
        x0, y0 = min(x for x, y in raw), min(y for x, y in raw)
        cells = {(x - x0 + tx, y - y0 + ty) for x, y in raw}

        def inverse(p):
            a, b = p[0] + x0 - tx, p[1] + y0 - ty
            for _ in range(turns):
                a, b = a + b, -a
            if reflect:
                a, b = a + b, -b
            return a, b

        if any(cells & previous for previous in levels):
            raise ValueError("overlap")
        if k == 0:
            roots += 1
            if reflect or turns or tx or ty or cells != set(tile):
                raise ValueError("incorrect central copy")
        levels[k].update(cells)
        copies.append((k, cells))
        # Decode from each actual exposed cell incidence using the inverse map.
        # This does not use the generator's forward oriented-port list.
        for owner in sorted(cells):
            for dx, dy in NEIGHBORS:
                neighbor = owner[0] + dx, owner[1] + dy
                if neighbor in cells:
                    continue
                index = original_ports[inverse(owner), inverse(neighbor)]
                edge = tuple(sorted((owner, neighbor)))
                side = 0 if edge[0] == owner else 1
                incident = edge_labels.setdefault(edge, [])
                if incident and (len(incident) != 1 or incident[0][0] == side or incident[0][1] != -signs[index]):
                    raise ValueError("noncomplementary boundary edge")
                incident.append((side, signs[index]))
    if roots != 1:
        raise ValueError("expected one root")
    prefixes = [set(levels[0])]
    for k in range(1, depth + 1):
        prefixes.append(prefixes[-1] | levels[k])
    for k, cells in copies:
        if k and not halo(cells) & prefixes[k - 1]:
            raise ValueError("new copy fails to touch preceding prefix")
    stats = []
    for k, cells in enumerate(prefixes):
        if k < depth and not halo(cells) <= prefixes[k + 1]:
            raise ValueError("incomplete corona")
        if component_count(cells, NEIGHBORS) != 1:
            raise ValueError("disconnected prefix")
        x0, x1 = min(x for x, y in cells) - 1, max(x for x, y in cells) + 1
        y0, y1 = min(y for x, y in cells) - 1, max(y for x, y in cells) + 1
        background = {(x, y) for x in range(x0, x1 + 1)
                      for y in range(y0, y1 + 1)} - cells
        if component_count(background, NEIGHBORS) != 1:
            raise ValueError("hole in prefix")
        stats.append({"level": k, "tiles": sum(lev == k for lev, _ in copies),
                      "cells": len(cells), "holes": 0})
    p, q = signs.count(1), signs.count(-1)
    return {"signed_counts": [p, q, signs.count(0)], "finite_charge": p != q,
            "prefixes": stats}
