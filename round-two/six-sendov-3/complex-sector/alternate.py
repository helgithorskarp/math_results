"""Same-author Fraction-endpoint check of every new interval certificate field.

Polynomial formulas, derivative jet and analytic bridges remain shared.
This is arithmetic corroboration, not independent review.
"""
import interval as iv
import centered
import sector
from reference import R


def recompute():
    saved=(iv.I,iv.ZERO,iv.ONE,iv.GZERO,centered.I,sector.I)
    try:
        iv.I=R;iv.ZERO=R(0);iv.ONE=R(1);iv.GZERO=(iv.ZERO,)*6
        centered.I=R;sector.I=R
        return sector.certificate()
    finally:
        iv.I,iv.ZERO,iv.ONE,iv.GZERO,centered.I,sector.I=saved
