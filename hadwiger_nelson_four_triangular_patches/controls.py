#!/usr/bin/env python3
"""Small negative controls for the XOR and colouring checkers."""

import json
import verify


def main():
    # An odd XOR triangle and odd XOR square must both be rejected.
    triangle = [(0, 1, 0), (1, 2, 0), (0, 2, 1)]
    square = [(0, 1, 0), (1, 2, 0), (2, 3, 0), (0, 3, 1)]
    verify.require(verify.solve_xor(3, triangle) is None,
                   "odd triangle corruption was accepted")
    verify.require(verify.solve_xor(4, square) is None,
                   "odd square corruption was accepted")
    # Removing the last inconsistent edge makes each system satisfiable.
    verify.require(verify.solve_xor(3, triangle[:-1]) is not None,
                   "triangle positive control failed")
    verify.require(verify.solve_xor(4, square[:-1]) is not None,
                   "square positive control failed")
    print(json.dumps({
        "verified": True,
        "rejected_corruptions": 2,
        "accepted_positive_controls": 2,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
