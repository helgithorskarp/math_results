#!/usr/bin/env python3
from itertools import combinations, product
import json
import verify as v
import audit


def main():
    zero = (0,)*8
    left = ((-144,)+(0,)*7, zero)
    right = ((144,)+(0,)*7, zero)
    top = (zero, (0, 144)+(0,)*6)
    bottom = (zero, (0, -144)+(0,)*6)
    points = [left, right, top, bottom]
    edges, groups = v.geometry(points)
    v.require(len(edges) == 5 and len(groups) == 3, 'unit diamond')
    t = (zero, (0, 288)+(0,)*6)
    assignments = positive = 0
    for choices in product((0, 1), repeat=4):
        images = [tuple(tuple(x+choice*y for x, y in zip(axis, delta, strict=True))
                        for axis, delta in zip(p, t, strict=True))
                  for p, choice in zip(points, choices, strict=True)]
        preserve = all(v.norm(images[a], images[b]) == (288**2,)+(0,)*7 for a, b in edges)
        # Hand-derived for this diamond: the base moves together, the upper
        # tip cannot rise away from it, and the lower tip cannot stay below it.
        edge_rule = choices[0] == choices[1] and choices[2] <= choices[0] <= choices[3]
        v.require(preserve == edge_rule, 'Boolean geometry control')
        assignments += 1
        if preserve and len(set(images)) == 3:
            positive += 1
    v.require(positive == 2, 'actual unit-preserving collision controls')
    diamond_robust = all(v.spanning_tree(4, [e for k, g in enumerate(groups) if k not in (i,j) for e in g])
                         is not None for i,j in combinations(range(3),2))
    v.require(not diamond_robust, 'criterion must not exclude diamond contraction')
    k4 = list(combinations(range(4), 2))
    for a, b in combinations(k4, 2):
        e = [x for x in k4 if x not in (a, b)]
        v.require(v.spanning_tree(4, e) is not None and audit.connected(4, e), 'graph control')
    v.require(v.spanning_tree(4, [(0,1),(2,3)]) is None and
              not audit.connected(4, [(0,1),(2,3)]), 'disconnection control')
    try:
        v.canonical_direction(left, left)
    except ValueError:
        pass
    else:
        raise ValueError('zero direction accepted')
    print(json.dumps(dict(all_checks=True, diamond_assignments_checked=assignments,
                          actual_three_image_translations=positive, abstract_k4_deletions=15,
                          rejected_zero_direction=True), sort_keys=True))


if __name__ == '__main__':
    main()
