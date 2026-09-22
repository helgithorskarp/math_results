"""Integer optimal illumination directions for smooth d-body x smooth 2-body.

The construction is universal in the two chosen factor coordinates.  The proof,
not this generator, establishes optimality and all-dimensional coverage.
"""

import argparse
import json


def directions(d, n=None):
    if type(d) is not int or d < 1:
        raise ValueError("d must be a positive integer")
    if n is None:
        n = 2 * d + 3 + d % 2
    if type(n) is not int or n < d + 1:
        raise ValueError("n must be an integer at least d+1")
    h = (n + 1) // 2
    a = [tuple((-1) ** i * i ** k for k in range(d)) for i in range(n)]
    b = [(1, 2 * i) if i < h else (-1, -(2 * (i - h) + 1))
         for i in range(n)]
    return a, b


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("d", type=int)
    args = parser.parse_args()
    aa, bb = directions(args.d)
    print(json.dumps({"d": args.d, "directions": [list(a + b)
                                                   for a, b in zip(aa, bb)]},
                     indent=2))
