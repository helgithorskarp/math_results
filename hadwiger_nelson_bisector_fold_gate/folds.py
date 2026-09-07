#!/usr/bin/env python3
"""Find a one-axis reflection contraction, or certify that none exists."""
from collections import deque
from fractions import Fraction as Q
import hashlib
from itertools import combinations
from math import lcm
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
SEED = HERE.parent / 'hadwiger_nelson_neutral_mutation_candidate'
sys.path.insert(0, str(SEED))
import verify as seed
import geometry as field_geometry
k = field_geometry.k
require = seed.require
MODULUS = 1000081
ROOTS = (964569, 816716, 970601)


def norm_coefficients(a, b):
    delta = [x-y for x, y in zip(a, b)]
    return tuple(x+y for x, y in zip(seed.square(delta[:8]), seed.square(delta[8:])))


def unit_edges(rows, scale):
    unit = (scale*scale,) + (0,)*7
    return [(p, q) for p, q in combinations(range(len(rows)), 2)
            if norm_coefficients(rows[p], rows[q]) == unit]


def modular_images(rows):
    require(all(r*r % MODULUS == d % MODULUS for r, d in zip(ROOTS, (3, 5, 11))),
            'invalid modular radical images')
    basis = []
    for mask in range(8):
        value = 1
        for j, r in enumerate(ROOTS):
            if mask >> j & 1:
                value = value*r % MODULUS
        basis.append(value)
    # Numerators are used directly; common coordinate denominators cancel
    # from every equal-distance comparison.
    return [(sum(a*b for a, b in zip(row[:8], basis)) % MODULUS,
             sum(a*b for a, b in zip(row[8:], basis)) % MODULUS) for row in rows]


def component_masks(adjacency, blocked):
    unseen = set(range(len(adjacency))) - blocked
    result = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        component = 1 << start
        while queue:
            for v in adjacency[queue.popleft()]:
                if v in unseen:
                    unseen.remove(v)
                    queue.append(v)
                    component |= 1 << v
        result.append(component)
    return tuple(result)


def reflection_witness(rows, scale, edges, pair, component):
    p, q = pair
    points = [(tuple(Q(a, scale) for a in row[:8]),
               tuple(Q(a, scale) for a in row[8:])) for row in rows]
    g = field_geometry
    d = g.sub(points[q], points[p])
    denominator = g.sqdist(points[p], points[q])
    inverse = k.inv(denominator, 3)
    transformed = []
    for v, point in enumerate(points):
        if component >> v & 1:
            twice_offset = g.sub(g.scale(point, 2), g.add(points[p], points[q]))
            dot = k.add(k.mul(twice_offset[0], d[0], 3),
                        k.mul(twice_offset[1], d[1], 3))
            factor = k.mul(dot, inverse, 3)
            point = tuple(k.sub(x, k.mul(factor, y, 3)) for x, y in zip(point, d))
        transformed.append(point)
    require(transformed[p] == transformed[q], 'claimed collision failed')
    unique = sorted(set(transformed))
    lookup = {point: v for v, point in enumerate(unique)}
    mapping = [lookup[point] for point in transformed]
    output_scale = lcm(*(a.denominator for point in unique for axis in point for a in axis))
    output_rows = [tuple(int(a*output_scale) for axis in point for a in axis) for point in unique]
    unit = (output_scale*output_scale,) + (0,)*7
    require(len(output_rows) < len(rows), 'no order reduction')
    require(all(norm_coefficients(output_rows[mapping[a]], output_rows[mapping[b]]) == unit
                for a, b in edges), 'unit edge not preserved')
    return {'colliding_pair': list(pair), 'reflected_vertices': [v for v in range(len(rows))
            if component >> v & 1], 'vertices': len(unique), 'scale': output_scale,
            'coordinates': output_rows, 'vertex_map': mapping, 'all_input_edges_preserved': True}


def analyse(rows, edges, scale=96, mask_output=None):
    n = len(rows)
    require(n >= 2 and type(scale) is int and scale > 0, 'invalid size or scale')
    require(all(len(row) == 16 and all(type(a) is int for a in row) for row in rows),
            'invalid coordinates')
    require(len(set(map(tuple, rows))) == n, 'input points must be distinct')
    require(edges == sorted(set(edges)) and all(0 <= a < b < n for a, b in edges),
            'invalid edge list')
    require(all(norm_coefficients(rows[a], rows[b]) == (scale*scale,)+(0,)*7
                for a, b in edges), 'input non-unit edge')
    adjacency = [[] for _ in rows]
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    images = modular_images(rows)
    squares = [(x*x+y*y) % MODULUS for x, y in images]
    cache = {}
    digest = hashlib.sha256()
    row_bytes = (n+7)//8
    counts = {'modular_paths': 0, 'exact_fallback_paths': 0}
    largest_removed = 0
    for p, q in combinations(range(n), 2):
        x, y = images[p]
        xx, yy = images[q]
        a, b, c = 2*(xx-x), 2*(yy-y), squares[q]-squares[p]
        blocked = {v for v, (vx, vy) in enumerate(images) if v not in (p, q)
                   and (a*vx+b*vy-c) % MODULUS == 0}
        mask = sum(1 << v for v in blocked)
        encoded_mask = mask.to_bytes(row_bytes, 'little')
        digest.update(encoded_mask)
        if mask_output is not None:
            mask_output.extend(encoded_mask)
        largest_removed = max(largest_removed, len(blocked))
        if mask not in cache:
            cache[mask] = component_masks(adjacency, blocked)
        if any(block >> p & 1 and block >> q & 1 for block in cache[mask]):
            counts['modular_paths'] += 1
            continue
        # A modular collision alone is not geometric evidence. Refine all
        # potentially on-axis vertices before producing a fold.
        exact = {v for v in blocked if norm_coefficients(rows[v], rows[p]) ==
                 norm_coefficients(rows[v], rows[q])}
        blocks = component_masks(adjacency, exact)
        selected = next(block for block in blocks if block >> p & 1)
        if selected >> q & 1:
            counts['exact_fallback_paths'] += 1
            continue
        return {'all_pairs_checked': False, 'every_one_axis_fold_injective': False,
                'candidate': reflection_witness(rows, scale, edges, (p, q), selected)}
    return {'vertices': n, 'edges': len(edges), 'pairs': n*(n-1)//2,
            'modulus': MODULUS, 'radical_images': list(ROOTS),
            'modular_images_distinct': len(set(images)) == n,
            'unique_modular_removed_sets': len(cache), 'maximum_removed_vertices': largest_removed,
            'pair_mask_sha256': digest.hexdigest(), **counts,
            'all_pairs_checked': True, 'every_one_axis_fold_injective': True}
