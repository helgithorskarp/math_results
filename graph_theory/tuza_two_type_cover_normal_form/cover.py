"""Exact triangle edge covers for split graphs with two neighborhood types.

Python 3.10+, standard library only.  The universal justification is PROOF.md,
not the regression tests.  All counts use arbitrary-precision integers.
"""

import argparse
import json
from itertools import combinations


def balanced_product(order, lower_left, lower_right):
    """Maximum t*(order-t), lower_left <= t <= order-lower_right."""
    assert 0 <= lower_left <= order - lower_right <= order
    left = max(lower_left, min(order // 2, order - lower_right))
    return left * (order - left), left


def host_optimum(x, y, z, w):
    """Maximum triangle-free edge count in K_w join (K_y,z + I_x).

    A maximizing cut has X,Y,Z monochromatic. Modes 0,1,2 put respectively
    XYZ, XY, XZ on the left; the other nonempty groups go on the right.
    """
    assert all(isinstance(v, int) and v >= 0 for v in (x, y, z, w))
    order = x + y + z + w
    candidates = []
    for mode, (lower_left, lower_right, forbidden) in enumerate(
            ((x + y + z, 0, 0), (x + y, z, x * z),
             (x + z, y, x * y))):
        value, left = balanced_product(order, lower_left, lower_right)
        candidates.append({"value": value - forbidden, "mode": mode,
                           "w_left": left - lower_left})
    return max(candidates, key=lambda row: (row["value"], -row["mode"]))


def solve(a, b, c, d, m, n):
    r"""Clique cells S\T, T\S, S intersect T, outside; multiplicities m,n.

    Returns an optimal value and a constant-length normal-form certificate.
    O(k^3) arithmetic operations, O(1) auxiliary space, k=a+b+c+d.
    The input describes the triangle-active subgraph; inactive vertices may
    be discarded. Zero multiplicities and empty neighborhoods are allowed.
    """
    assert all(isinstance(v, int) and v >= 0 for v in (a, b, c, d, m, n))
    k = a + b + c + d
    best = None
    for x in range(c + 1):
        for y in range(a + c - x + 1):
            for z in range(b + c - x + 1):
                if max(0, y - a) + max(0, z - b) > c - x:
                    continue
                host = host_optimum(x, y, z, k - x - y - z)
                retained = host["value"] + m * (x + y) + n * (x + z)
                if best is None or retained > best[0]:
                    best = retained, x, y, z, host
    retained, x, y, z, host = best
    total = k * (k - 1) // 2 + m * (a + c) + n * (b + c)
    return {"parameters": [a, b, c, d, m, n], "tau": total - retained,
            "x": x, "y": y, "z": z, "mode": host["mode"],
            "w_left": host["w_left"]}


def reconstruct(record):
    """Reconstruct protected sets and surviving clique edges from a record.

    Clique labels: intersection first, then S-only, T-only, and neither.
    Multiplicity classes are NOT expanded.
    """
    a, b, c, d, m, n = record["parameters"]
    k = a + b + c + d
    x, y, z = (record[name] for name in ("x", "y", "z"))
    assert 0 <= x <= c and y >= 0 and z >= 0
    yu, zu = max(0, y - a), max(0, z - b)
    assert yu + zu <= c - x
    X = set(range(x))
    Y = set(range(x, x + yu)) | set(range(c, c + y - yu))
    Z = set(range(x + yu, x + yu + zu)) | set(range(c + a, c + a + z - zu))
    W = sorted(set(range(k)) - X - Y - Z)
    assert len(X) == x and len(Y) == y and len(Z) == z
    assert 0 <= record["w_left"] <= len(W)
    mode = record["mode"]
    assert mode in (0, 1, 2)
    left = X | (Y if mode in (0, 1) else set()) | (Z if mode in (0, 2) else set())
    left |= set(W[:record["w_left"]])
    A, B = X | Y, X | Z
    kept = {(u, v) for u, v in combinations(range(k), 2)
            if (u in left) != (v in left)
            and not ({u, v} <= A or {u, v} <= B)}
    return {"S": set(range(c + a)),
            "T": set(range(c)) | set(range(c + a, c + a + b)),
            "A": A, "B": B, "left": left, "kept": kept}


def rectangle_packing(record):
    """Pack the missing crossing rectangle of an optimal certificate.

    This does not pack all edges needed for Tuza's inequality.
    The certificate's optimality implies the required multiplicity bound.
    """
    a, b, c, d, m, n = record["parameters"]
    k = a + b + c + d
    witness = reconstruct(record)
    A, B = witness["A"], witness["B"]
    X = sorted(A & B)
    mode = record["mode"]
    if mode == 0:
        return []
    Z = sorted(B - A if mode == 1 else A - B)
    if not X or not Z:
        return []
    h = max(len(X), len(Z))
    assert (n if mode == 1 else m) >= h
    first_center = k + (m if mode == 1 else 0)
    return [(u, v, first_center + (j - i) % h)
            for i, u in enumerate(X) for j, v in enumerate(Z)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parameters", type=int, nargs=6,
                        metavar=("a", "b", "c", "d", "m", "n"))
    args = parser.parse_args()
    if any(v < 0 for v in args.parameters):
        parser.error("all parameters must be nonnegative")
    print(json.dumps(solve(*args.parameters), sort_keys=True))
