"""Finite subset-cover compiler with full-footprint binary conflicts.

This deliberately proves only cover impossibility on the stated exact mesh.
The written half/quarter-grid bridge supplies any all-motion implication.
"""
from collections import defaultdict
from fractions import Fraction as Q
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'finite-contact-types'))
from contact import require


def compile_subset(tile, fixed, scale, target):
    require(scale in (1, 2, 4), 'unsupported mesh')
    target = set(map(tuple, target))
    old = set().union(*(tile.pixels(p, scale) for p in fixed))
    require(target.isdisjoint(old), 'target overlaps fixed union')
    pool = []
    for o in range(len(tile.orientations)):
        op = tile.pixels((o, 0, 0), scale)
        shifts = {(x-a, y-b) for x, y in target for a, b in op}
        for x, y in sorted(shifts):
            physical = frozenset((a+x, b+y) for a, b in op)
            if old.isdisjoint(physical):
                pool.append(((o, Q(x, scale), Q(y, scale)), physical))
    require(len(pool) <= 6000, 'candidate guard: incomplete compilation')
    owners = defaultdict(list)
    for i, (pose, pixels) in enumerate(pool, 1):
        for q in target & pixels:
            owners[q].append(i)
    # All whole-footprint intersections, including pixels outside the target.
    clauses = [[-i-1, -j-1] for i, (A, pa) in enumerate(pool)
               for j, (B, pb) in enumerate(pool[:i]) if not pa.isdisjoint(pb)]
    clauses.extend(owners[q] for q in sorted(target))
    return pool, clauses, len(pool)


def audit_subset(tile, fixed, scale, target, pool):
    """Independent complete pool from bounding boxes and unit rectangles."""
    targets = set(map(tuple, target))
    fixed_rects = [(int(x*scale), int(y*scale))
                   for p in fixed for x, y in tile.anchors(p)]
    xmin, xmax = min(x for x, y in targets), max(x for x, y in targets)
    ymin, ymax = min(y for x, y in targets), max(y for x, y in targets)
    found = set()
    for o, cells in enumerate(tile.orientations):
        w, h = max(x for x, y in cells)+1, max(y for x, y in cells)+1
        op = [(a*scale, b*scale) for a, b in cells]
        for x in range(xmin-w*scale+1, xmax+1):
            for y in range(ymin-h*scale+1, ymax+1):
                if not any(x+a <= u < x+a+scale and y+b <= v < y+b+scale
                           for a, b in op for u, v in targets):
                    continue
                if any(abs(x+a-u) < scale and abs(y+b-v) < scale
                       for a, b in op for u, v in fixed_rects):
                    continue
                found.add((o, x, y))
    actual = set()
    for pose, pixels in pool:
        o, x, y = pose
        key = o, int(x*scale), int(y*scale)
        require(key not in actual, 'duplicate subset candidate')
        actual.add(key)
        rebuilt = {(key[1]+a*scale+i, key[2]+b*scale+j)
                   for a, b in tile.orientations[o]
                   for i in range(scale) for j in range(scale)}
        require(rebuilt == pixels, 'subset footprint mismatch')
    require(actual == found, 'subset pool incomplete or extra')
    return len(actual)
