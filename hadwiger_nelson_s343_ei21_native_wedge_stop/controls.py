#!/usr/bin/env python3
"""Definition-level controls for the mixed-source interval gate."""

from fractions import Fraction as Q

import verify


def point(x, y):
    return ((Q(x), Q(x)), (Q(y), Q(y)))


def must_reject(s, e, text):
    try:
        verify.private_cross_margins([s], [e])
    except ValueError as exc:
        if text not in str(exc):
            raise
        return
    raise ValueError("control was not rejected")


def main():
    checks, separation, gap = verify.private_cross_margins(
        [point(0, 0)], [point(3, 0)])
    verify.need((checks, separation, gap) == (1, 9, 8), "positive control")
    must_reject(point(1, 0), point(1, 0), "collision")
    must_reject(point(1, 0), point(2, 0), "unit pair")
    result = verify.verify()
    verify.need(result["chromatic_number"] == 4, "full replay")
    print("S343--EI21 CONTROLS PASSED")


if __name__ == "__main__":
    main()
