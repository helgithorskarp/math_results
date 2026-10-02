"""Fraction endpoint corroboration, same author/shared formulas, not review."""
import interval as iv
import centered
import radial
from reference import R


def recompute():
    saved=(iv.I,iv.ZERO,iv.ONE,iv.GZERO,centered.I,radial.I)
    try:
        iv.I=R;iv.ZERO=R(0);iv.ONE=R(1);iv.GZERO=(iv.ZERO,)*6
        centered.I=R;radial.I=R
        return radial.certificate()
    finally:
        iv.I,iv.ZERO,iv.ONE,iv.GZERO,centered.I,radial.I=saved
