"""Exact rational diagnostics for the written unrestricted-motion reductions.

This module checks finite axis-locked examples. It is not a search over real
placements or a machine proof of the universal sector/density lemmas.
"""
from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
from itertools import product
from math import lcm


DEPENDENCY_FILES = {
    'kaplan17.json': '24ceb5aefe2e0843d16d7ab7ced16f17356789426a12607b00cf956df02dbe51',
    'kaplan17_depth3.witness.json': 'c5f4c30ceff27b40a39ef006960b7b5de22489c52e71b429196d1f51cdc32f04',
    'cover_evidence.json': '244a988b3bdd465a6935920b85a46876ccbd23dad2a3246577f7df477a3e9126',
    'growth20_manifest.json': '8f96c536c15f739130b6ca7e5a67fcba1ff1e51fa4bbc18b16d652182c24ff85',
}


def check_dependency(prior):
    for name, digest in DEPENDENCY_FILES.items():
        assert hashlib.sha256((prior/name).read_bytes()).hexdigest() == digest, name+' provenance mismatch'


def normalize(cells):
    raw = [tuple(p) for p in cells]
    if not raw or len(set(raw)) != len(raw):
        raise ValueError("empty tile or duplicate cell")
    if any(len(p) != 2 or any(type(x) is not int for x in p) for p in raw):
        raise ValueError("integer cell pairs required")
    x0 = min(p[0] for p in raw)
    y0 = min(p[1] for p in raw)
    return tuple(sorted((x-x0, y-y0) for x, y in raw))


def variants(tile):
    """Eight signed coordinate permutations, rather than iterated rotations."""
    result = set()
    for swap, sx, sy in product((False, True), (-1, 1), (-1, 1)):
        cells = [(sx*(y if swap else x), sy*(x if swap else y)) for x, y in tile]
        result.add(normalize(cells))
    return result


def dimensions(tile):
    tile = normalize(tile)
    w, h = 1+max(x for x, y in tile), 1+max(y for x, y in tile)
    return len(tile), w, h, max(w, h)


def mesh_denominator(tile, depth):
    if type(depth) is not int or depth < 0:
        raise ValueError("nonnegative integer depth required")
    m, w, h, span = dimensions(tile)
    return ((w+2*depth*span)*(h+2*depth*span)) // m


def unrestricted_upper(tile, blocking_radius):
    """Conditional bound: caller must have a complete checked grid obstruction."""
    if type(blocking_radius) is not int or blocking_radius < 0:
        raise ValueError("nonnegative integer radius required")
    m, w, h, span = dimensions(tile)
    return ((w+2*blocking_radius+2*span)*(h+2*blocking_radius+2*span)) // m - 1


@dataclass(frozen=True)
class Pose:
    level: int
    shape: tuple
    tx: Fraction
    ty: Fraction

    def squares(self):
        return tuple((self.tx+x, self.ty+y) for x, y in self.shape)


def load_poses(tile, records):
    shapes = variants(normalize(tile))
    result = []
    for r in records:
        shape = tuple(sorted(tuple(p) for p in r['shape']))
        if shape not in shapes:
            raise ValueError("noncongruent or unnormalized shape")
        if type(r['level']) is not int or r['level'] < 0:
            raise ValueError("invalid level")
        # The JSON format uses integer or exact rational strings, not floats.
        if any(type(x) not in (str, int) for x in r['translation']):
            raise ValueError("exact translation strings required")
        result.append(Pose(r['level'], shape, *(Fraction(x) for x in r['translation'])))
    return result


def phase_compress(poses, denominator):
    if type(denominator) is not int or denominator < 1:
        raise ValueError("positive integer denominator required")
    mappings = []
    for axis in ('tx', 'ty'):
        phases = sorted({Fraction(0)} | {getattr(p, axis) % 1 for p in poses})
        if len(phases) > denominator:
            raise ValueError("denominator too small for distinct phases")
        mappings.append({f: Fraction(i, denominator) for i, f in enumerate(phases)})
    result = []
    for p in poses:
        coords = []
        for t, mapping in zip((p.tx, p.ty), mappings):
            coords.append(t // 1 + mapping[t % 1])
        result.append(replace(p, tx=coords[0], ty=coords[1]))
    return result


def floor_poses(poses):
    return [replace(p, tx=Fraction(p.tx // 1), ty=Fraction(p.ty // 1)) for p in poses]


def contact_graph(poses):
    """Closed rectangle intersections; independent of arrangement occupancy."""
    squares = [p.squares() for p in poses]
    graph = [set() for _ in poses]
    for i, left in enumerate(squares):
        for j in range(i):
            if any(abs(x-u) <= 1 and abs(y-v) <= 1
                   for x, y in left for u, v in squares[j]):
                graph[i].add(j)
                graph[j].add(i)
    return graph


def arrangement(poses, target=()):
    """Map all exact coordinate cuts monotonically to an integer pixel grid."""
    groups = [p.squares() for p in poses]
    target = list(target)
    all_squares = [z for g in groups for z in g] + target
    if not all_squares:
        raise ValueError("empty arrangement")
    cuts = []
    for axis in (0, 1):
        values = {z[axis]+offset for z in all_squares for offset in (0, 1)}
        values.update((min(values)-1, max(values)+1))
        cuts.append({x: i for i, x in enumerate(sorted(values))})

    def pixels(squares):
        result = set()
        for x, y in squares:
            for a in range(cuts[0][x], cuts[0][x+1]):
                for b in range(cuts[1][y], cuts[1][y+1]):
                    result.add((a, b))
        return result

    footprints = [pixels(g) for g in groups]
    used = set()
    for footprint in footprints:
        if used & footprint:
            raise ValueError("overlapping interiors")
        used.update(footprint)
    return footprints, pixels(target)


FOUR = ((1, 0), (-1, 0), (0, 1), (0, -1))
EIGHT = tuple((x, y) for x, y in product((-1, 0, 1), repeat=2) if (x, y) != (0, 0))


def components(cells, offsets=FOUR):
    remaining = set(cells)
    total = 0
    while remaining:
        total += 1
        queue = [remaining.pop()]
        while queue:
            x, y = queue.pop()
            for dx, dy in offsets:
                q = x+dx, y+dy
                if q in remaining:
                    remaining.remove(q)
                    queue.append(q)
    return total


def boundary_disc(cells):
    """Connected foreground plus a single simple boundary cycle.

    This differs from the dependency's Euler/holes implementation. The
    finite union of these rectangles is a closed disc exactly in this case.
    """
    adjacency = {}
    for x, y in cells:
        edges = [((x, y), (x+1, y), (x, y-1)),
                 ((x+1, y), (x+1, y+1), (x+1, y)),
                 ((x+1, y+1), (x, y+1), (x, y+1)),
                 ((x, y+1), (x, y), (x-1, y))]
        for a, b, outside in edges:
            if outside not in cells:
                adjacency.setdefault(a, set()).add(b)
                adjacency.setdefault(b, set()).add(a)
    bad = sum(len(ns) != 2 for ns in adjacency.values())
    remaining = set(adjacency)
    loops = 0
    while remaining:
        loops += 1
        todo = [remaining.pop()]
        while todo:
            for q in adjacency[todo.pop()]:
                if q in remaining:
                    remaining.remove(q)
                    todo.append(q)
    foreground = components(cells)
    return {'disc': bool(cells) and foreground == 1 and not bad and loops == 1,
            'boundary_components': loops, 'nonmanifold_vertices': bad,
            'foreground_components': foreground}


def check_corona(tile, depth, poses, holes_last=False):
    tile = normalize(tile)
    if type(depth) is not int or depth < 0 or not boundary_disc(set(tile))['disc']:
        raise ValueError("disc tile and nonnegative depth required")
    valid = variants(tile)
    if any(p.shape not in valid or type(p.level) is not int or not 0 <= p.level <= depth
           for p in poses):
        raise ValueError("invalid tile or level")
    roots = [p for p in poses if p.level == 0]
    if len(roots) != 1 or roots[0].shape != tile or roots[0].tx or roots[0].ty:
        raise ValueError("incorrect root")
    footprints, _ = arrangement(poses)
    previous = set()
    stats = []
    for level in range(depth+1):
        new = [footprints[i] for i, p in enumerate(poses) if p.level == level]
        if level:
            for cells in new:
                if not any((x+dx, y+dy) in previous for x, y in cells for dx, dy in EIGHT):
                    raise ValueError("tile does not touch preceding prefix")
        prefix = previous | set().union(*new)
        if level:
            halo = {(x+dx, y+dy) for x, y in previous for dx, dy in EIGHT} - previous
            if not halo <= prefix:
                raise ValueError("incomplete surround")
        topo = boundary_disc(prefix)
        if not (holes_last and level == depth) and not topo['disc']:
            raise ValueError("invalid prefix topology")
        if components(prefix, EIGHT) != 1:
            raise ValueError("disconnected prefix")
        stats.append({'level': level, 'tiles': len(new), **topo})
        previous = prefix
    return stats


def check_covering(poses, target):
    footprints, required = arrangement(poses, target)
    if not required <= set().union(*footprints):
        raise ValueError("incomplete whole-cell coverage")
    return True


def rasterize(tile, poses, max_cells=20000):
    """Exact comparison input for the older pixel witness checker.

    The size guard is operational, never a mathematical exclusion.
    """
    denominator = lcm(*(t.denominator for p in poses for t in (p.tx, p.ty)))
    if len(tile)*len(poses)*denominator**2 > max_cells:
        raise ValueError("diagnostic raster size exceeds local guard")
    def cells(shape, tx=Fraction(0), ty=Fraction(0)):
        return sorted((int(denominator*(x+tx))+dx, int(denominator*(y+ty))+dy)
                      for x, y in shape for dx in range(denominator)
                      for dy in range(denominator))
    return cells(tile), [{'level': p.level, 'cells': cells(p.shape, p.tx, p.ty)} for p in poses]
