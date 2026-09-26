"""Finite-field definitions used by the quadratic-moment author audit."""

from itertools import product

FORM_COUNTS = {
    "rank0": (31, 0, 0),
    "rank1_square": (6, 25, 0),
    "rank1_nonsquare": (6, 0, 25),
    "rank2_split": (11, 10, 10),
    "rank2_anisotropic": (1, 15, 15),
    "rank3_square_det": (6, 15, 10),
    "rank3_nonsquare_det": (6, 10, 15),
}


def character(value):
    value %= 5
    return 0 if value == 0 else 1 if value in (1, 4) else -1


def projective_points():
    return [v for v in product(range(5), repeat=3)
            if any(v) and next(x for x in v if x) == 1]
