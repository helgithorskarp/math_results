"""Exact unit-edge J77 fixture and an independent cupola construction.

Fixture order follows David McCooey's coordinate list, retrieved 2026-09-29:
https://dmccooey.com/polyhedra/ParagyrateDiminishedRhombicosidodecahedron.txt
The named-solid identification is checked by the independent construction below.
"""
from itertools import product
from q5 import Q, add, cross, dot, scale

C0, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10 = (
    Q(5, 1)/20, Q(1, 1)/4, Q(15, 1)/20, Q(3, 1)/4,
    Q(5, 4)/10, Q(1, 1)/2, Q(10, 3)/10, Q(5, 1)/4,
    Q(5, 2)/5, Q(2, 1)/2, Q(15, 13)/20,
)
VERTICES = (
    (Q('0.5'), Q('0.5'), C9),  # V0
    (Q('0.5'), Q('0.5'), -C9),  # V1
    (Q('0.5'), Q('-0.5'), C9),  # V2
    (Q('0.5'), Q('-0.5'), -C9),  # V3
    (Q('-0.5'), Q('0.5'), C9),  # V4
    (Q('-0.5'), Q('0.5'), -C9),  # V5
    (Q('-0.5'), Q('-0.5'), C9),  # V6
    (Q('-0.5'), Q('-0.5'), -C9),  # V7
    (C9, Q('0.5'), Q('0.5')),  # V8
    (C9, Q('0.5'), Q('-0.5')),  # V9
    (C9, Q('-0.5'), Q('0.5')),  # V10
    (C9, Q('-0.5'), Q('-0.5')),  # V11
    (-C9, Q('0.5'), Q('0.5')),  # V12
    (-C9, Q('0.5'), Q('-0.5')),  # V13
    (-C9, Q('-0.5'), Q('0.5')),  # V14
    (-C9, Q('-0.5'), Q('-0.5')),  # V15
    (Q('0.5'), C9, Q('-0.5')),  # V16
    (Q('0.5'), -C9, Q('0.5')),  # V17
    (Q('0.5'), -C4, -C6),  # V18
    (Q('-0.5'), C9, Q('-0.5')),  # V19
    (Q('-0.5'), -C9, Q('0.5')),  # V20
    (Q('-0.5'), -C4, -C6),  # V21
    (Q('0.0'), C3, -C7),  # V22
    (Q('0.0'), -C3, C7),  # V23
    (Q('0.0'), -C10, -C0),  # V24
    (C7, Q('0.0'), C3),  # V25
    (C7, Q('0.0'), -C3),  # V26
    (-C7, Q('0.0'), C3),  # V27
    (-C7, Q('0.0'), -C3),  # V28
    (C3, C7, Q('0.0')),  # V29
    (C3, -C7, Q('0.0')),  # V30
    (-C3, C7, Q('0.0')),  # V31
    (-C3, -C7, Q('0.0')),  # V32
    (C3, C1, C5),  # V33
    (C3, C1, -C5),  # V34
    (C3, -C1, C5),  # V35
    (C3, -C1, -C5),  # V36
    (-C3, C1, C5),  # V37
    (-C3, C1, -C5),  # V38
    (-C3, -C1, C5),  # V39
    (-C3, -C1, -C5),  # V40
    (C5, C3, C1),  # V41
    (C5, C3, -C1),  # V42
    (C5, -C3, C1),  # V43
    (C5, -C3, -C1),  # V44
    (-C5, C3, C1),  # V45
    (-C5, C3, -C1),  # V46
    (-C5, -C3, C1),  # V47
    (-C5, -C3, -C1),  # V48
    (C1, C5, -C3),  # V49
    (C1, -C5, C3),  # V50
    (C1, -C8, -C2),  # V51
    (-C1, C5, -C3),  # V52
    (-C1, -C5, C3),  # V53
    (-C1, -C8, -C2),  # V54
)
FACES = (
    (0, 33, 41, 29, 16, 19, 31, 45, 37, 4),
    (22, 52, 19, 16, 49),
    (23, 53, 20, 17, 50),
    (24, 54, 21, 18, 51),
    (25, 33, 0, 2, 35),
    (26, 36, 3, 1, 34),
    (27, 39, 6, 4, 37),
    (28, 38, 5, 7, 40),
    (29, 41, 8, 9, 42),
    (30, 44, 11, 10, 43),
    (31, 46, 13, 12, 45),
    (32, 47, 14, 15, 48),
    (1, 22, 49, 34),
    (2, 23, 50, 35),
    (3, 18, 21, 7),
    (5, 38, 52, 22),
    (6, 39, 53, 23),
    (8, 41, 33, 25),
    (9, 26, 34, 42),
    (10, 25, 35, 43),
    (11, 44, 36, 26),
    (12, 27, 37, 45),
    (13, 46, 38, 28),
    (14, 47, 39, 27),
    (15, 28, 40, 48),
    (16, 29, 42, 49),
    (17, 30, 43, 50),
    (18, 36, 44, 51),
    (19, 52, 46, 31),
    (20, 53, 47, 32),
    (21, 54, 48, 40),
    (0, 4, 6, 2),
    (1, 3, 7, 5),
    (8, 10, 11, 9),
    (12, 13, 15, 14),
    (17, 24, 51, 30),
    (20, 32, 54, 24),
    (22, 1, 5),
    (23, 2, 6),
    (24, 17, 20),
    (25, 10, 8),
    (26, 9, 11),
    (27, 12, 14),
    (28, 15, 13),
    (30, 51, 44),
    (32, 48, 54),
    (34, 49, 42),
    (35, 50, 43),
    (36, 18, 3),
    (38, 46, 52),
    (39, 47, 53),
    (40, 7, 21),
)


def cupola_construction():
    """Delete the two opposite cupolas and restore one gyrated by 36 degrees."""
    original = set()
    for base in ((Q(1)/2, Q(1)/2, C9), (Q(), C3, C7), (C3, C1, C5)):
        for signs in product((-1, 1), repeat=3):
            p = tuple(s*x for s, x in zip(signs, base))
            original.update((p, (p[1], p[2], p[0]), (p[2], p[0], p[1])))
    axis = (Q(), C5, Q(1))
    rim_height = Q(5, 3)/4
    cap_height = Q(9, 3)/4
    core = {p for p in original if -rim_height <= dot(axis, p) <= rim_height}
    cap = {p for p in original if dot(axis, p) == -cap_height}
    cosine = C1
    sine_over_axis_norm = Q(-1, 1)/4

    def rotate(p):
        return add(
            add(scale(cosine, p),
                scale((1-cosine)*dot(axis, p)/dot(axis, axis), axis)),
            scale(sine_over_axis_norm, cross(axis, p)),
        )

    return original, core, cap, {rotate(p) for p in cap}, axis
