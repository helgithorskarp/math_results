"""Exact unit-edge J74 model; coordinates checked against cupola gyration.
Geometric data cross-check: https://www.dmccooey.com/polyhedra/MetabigyrateRhombicosidodecahedron.txt
The checker uses an independent constructive identification, not a web fetch.
"""
from itertools import product
from q5 import Q, add, cross, dot, scale
s = Q(0, 1)
C0 = (5 + s) / 20
C1 = (1 + s) / 4
C2 = (15 + s) / 20
C3 = (3 + s) / 4
C4 = (5 + 4 * s) / 10
C5 = (1 + s) / 2
C6 = (10 + 3 * s) / 10
C7 = (5 + s) / 4
C8 = (5 + 2 * s) / 5
C9 = (2 + s) / 2
C10 = (15 + 13 * s) / 20
VERTICES = (
    (Q(0.5), Q(0.5), C9),
    (Q(0.5), Q(0.5), -C9),
    (Q(0.5), Q(-0.5), C9),
    (Q(0.5), Q(-0.5), -C9),
    (Q(-0.5), Q(0.5), C9),
    (Q(-0.5), Q(0.5), -C9),
    (Q(-0.5), Q(-0.5), C9),
    (Q(-0.5), Q(-0.5), -C9),
    (C9, Q(0.5), Q(0.5)),
    (C9, Q(0.5), Q(-0.5)),
    (C9, Q(-0.5), Q(0.5)),
    (C9, Q(-0.5), Q(-0.5)),
    (-C9, Q(0.5), Q(0.5)),
    (-C9, Q(0.5), Q(-0.5)),
    (-C9, Q(-0.5), Q(0.5)),
    (-C9, Q(-0.5), Q(-0.5)),
    (Q(0.5), C4, C6),
    (Q(0.5), C9, Q(-0.5)),
    (Q(0.5), -C4, C6),
    (Q(0.5), -C9, Q(-0.5)),
    (Q(-0.5), C4, C6),
    (Q(-0.5), C9, Q(-0.5)),
    (Q(-0.5), -C4, C6),
    (Q(-0.5), -C9, Q(-0.5)),
    (Q(0.0), C10, C0),
    (Q(0.0), C3, -C7),
    (Q(0.0), -C10, C0),
    (Q(0.0), -C3, -C7),
    (C7, Q(0.0), C3),
    (C7, Q(0.0), -C3),
    (-C7, Q(0.0), C3),
    (-C7, Q(0.0), -C3),
    (C3, C7, Q(0.0)),
    (C3, -C7, Q(0.0)),
    (-C3, C7, Q(0.0)),
    (-C3, -C7, Q(0.0)),
    (C3, C1, C5),
    (C3, C1, -C5),
    (C3, -C1, C5),
    (C3, -C1, -C5),
    (-C3, C1, C5),
    (-C3, C1, -C5),
    (-C3, -C1, C5),
    (-C3, -C1, -C5),
    (C5, C3, C1),
    (C5, C3, -C1),
    (C5, -C3, C1),
    (C5, -C3, -C1),
    (-C5, C3, C1),
    (-C5, C3, -C1),
    (-C5, -C3, C1),
    (-C5, -C3, -C1),
    (C1, C8, C2),
    (C1, C5, -C3),
    (C1, -C8, C2),
    (C1, -C5, -C3),
    (-C1, C8, C2),
    (-C1, C5, -C3),
    (-C1, -C8, C2),
    (-C1, -C5, -C3),
)
FACES = (
    (24, 56, 20, 16, 52),
    (25, 57, 21, 17, 53),
    (26, 54, 18, 22, 58),
    (27, 55, 19, 23, 59),
    (28, 36, 0, 2, 38),
    (29, 39, 3, 1, 37),
    (30, 42, 6, 4, 40),
    (31, 41, 5, 7, 43),
    (32, 44, 8, 9, 45),
    (33, 47, 11, 10, 46),
    (34, 49, 13, 12, 48),
    (35, 50, 14, 15, 51),
    (32, 17, 24, 52),
    (1, 25, 53, 37),
    (33, 54, 26, 19),
    (3, 39, 55, 27),
    (34, 56, 24, 21),
    (5, 41, 57, 25),
    (35, 23, 26, 58),
    (7, 27, 59, 43),
    (8, 44, 36, 28),
    (9, 29, 37, 45),
    (10, 28, 38, 46),
    (11, 47, 39, 29),
    (12, 30, 40, 48),
    (13, 49, 41, 31),
    (14, 50, 42, 30),
    (15, 31, 43, 51),
    (36, 44, 52, 16),
    (17, 32, 45, 53),
    (38, 18, 54, 46),
    (19, 55, 47, 33),
    (40, 20, 56, 48),
    (21, 57, 49, 34),
    (42, 50, 58, 22),
    (23, 35, 51, 59),
    (0, 4, 6, 2),
    (1, 3, 7, 5),
    (8, 10, 11, 9),
    (12, 13, 15, 14),
    (20, 4, 0, 16),
    (22, 18, 2, 6),
    (24, 17, 21),
    (25, 1, 5),
    (26, 23, 19),
    (27, 7, 3),
    (28, 10, 8),
    (29, 9, 11),
    (30, 12, 14),
    (31, 15, 13),
    (32, 52, 44),
    (33, 46, 54),
    (34, 48, 56),
    (35, 58, 50),
    (36, 16, 0),
    (37, 53, 45),
    (38, 2, 18),
    (39, 47, 55),
    (40, 4, 20),
    (41, 49, 57),
    (42, 22, 6),
    (43, 59, 51),
)

def cupola_construction():
    phi = (1+s)/2
    original = set()
    for base in ((Q(1)/2, Q(1)/2, (2+s)/2),
                 (Q(), (3+s)/4, (5+s)/4),
                 ((3+s)/4, (1+s)/4, phi)):
        for signs in product((-1, 1), repeat=3):
            p = tuple(t*x for t, x in zip(signs, base))
            original.update((p, (p[1], p[2], p[0]), (p[2], p[0], p[1])))
    axes = ((Q(), phi, Q(1)), (Q(), -phi, Q(1)))
    height = (9+3*s)/4
    caps = [{p for p in original if dot(a, p) == height} for a in axes]
    cosine = (1+s)/4
    sine_over_axis = (s-1)/4
    gyrated = []
    for axis, cap in zip(axes, caps):
        def rotate(p):
            return add(add(scale(cosine, p),
                           scale((1-cosine)*dot(axis, p)/dot(axis, axis), axis)),
                       scale(sine_over_axis, cross(axis, p)))
        gyrated.append({rotate(p) for p in cap})
    core = original-set.union(*caps)
    return original, caps, gyrated, core | set.union(*gyrated), axes
