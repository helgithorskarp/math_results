"""Exact finite corroboration; see PROOF.md for the universal theorem.

Uses rational elimination to check positive circuits independently of the
Lagrange formula, and a complete rational arrangement of planar normal rays.
There are no floating-point operations, solver calls, or external packages.
"""

from fractions import Fraction as F
from functools import cmp_to_key
from hashlib import sha256
from itertools import combinations
from math import gcd, prod
from pathlib import Path
import json

from construct import directions


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def det(rows):
    """Rational Gaussian determinant, including the empty determinant."""
    n = len(rows)
    m = [[F(x) for x in row] for row in rows]
    ans = F(1)
    for j in range(n):
        p = next((r for r in range(j, n) if m[r][j]), None)
        if p is None:
            return F(0)
        if p != j:
            m[j], m[p] = m[p], m[j]
            ans = -ans
        pivot = m[j][j]
        ans *= pivot
        for r in range(j + 1, n):
            q = m[r][j] / pivot
            for c in range(j + 1, n):
                m[r][c] -= q * m[j][c]
    return ans


def solve(rows, rhs):
    n = len(rows)
    require(n == len(rhs) and all(len(row) == n for row in rows),
            "non-square linear system")
    m = [[F(x) for x in row] + [F(y)] for row, y in zip(rows, rhs)]
    for j in range(n):
        p = next((r for r in range(j, n) if m[r][j]), None)
        require(p is not None, "singular affine circuit")
        m[j], m[p] = m[p], m[j]
        pivot = m[j][j]
        m[j] = [x / pivot for x in m[j]]
        for r in range(n):
            if r != j:
                q = m[r][j]
                m[r] = [x - q * y for x, y in zip(m[r], m[j])]
    return tuple(row[-1] for row in m)


def circuit(vectors):
    d = len(vectors[0])
    require(len(vectors) == d + 1, "wrong circuit size")
    rows = [[v[k] for v in vectors] for k in range(d)]
    weights = solve(rows + [[1] * (d + 1)], [0] * d + [1])
    require(all(w > 0 for w in weights), "circuit is not positive")
    require(all(sum(w * v[k] for w, v in zip(weights, vectors)) == 0
                for k in range(d)), "nonzero circuit residual")
    require(det([v for v in vectors[:-1]]) != 0, "circuit lacks full rank")
    return weights


def primitive(v):
    g = gcd(abs(v[0]), abs(v[1]))
    require(g > 0, "zero planar ray")
    return (v[0] // g, v[1] // g)


def half(v):
    return 0 if v[1] > 0 or (v[1] == 0 and v[0] > 0) else 1


def angle_cmp(u, v):
    if half(u) != half(v):
        return -1 if half(u) < half(v) else 1
    c = u[0] * v[1] - u[1] * v[0]
    return -1 if c > 0 else 1 if c < 0 else 0


def normal_cells(b):
    """One exact vector in every open cell and on every boundary ray."""
    rays = set()
    for x, y in b:
        if x or y:
            v = primitive((-y, x))
            rays.update((v, (-v[0], -v[1])))
    rays = sorted(rays, key=cmp_to_key(angle_cmp))
    require(len(rays) > 2, "insufficient normal arrangement")
    cells = []
    for i, u in enumerate(rays):
        v = rays[(i + 1) % len(rays)]
        require(u[0] * v[1] - u[1] * v[0] > 0,
                "adjacent normal rays not less than pi apart")
        cells.append(("boundary", u))
        cells.append(("interior", primitive((u[0] + v[0], u[1] + v[1]))))
    return cells


def separator(vectors, d):
    """Find and explicitly validate a nonzero u with all a.u >= 0.

    Used only to produce negative-control witnesses. Failure to find one is
    not used as a positive-spanning certificate.
    """
    for subset in combinations(vectors, d - 1):
        u = tuple((-1) ** k * det([[v[j] for j in range(d) if j != k]
                                   for v in subset]) for k in range(d))
        if not any(u):
            continue
        for sign in (1, -1):
            w = tuple(sign * x for x in u)
            if all(dot(w, v) >= 0 for v in vectors):
                return w
    return None


def uncovered_pair(a, b):
    d = len(a[0])
    for _, v in normal_cells(b):
        active = [x for x, y in zip(a, b) if dot(y, v) < 0]
        u = separator(active, d)
        if u is not None:
            require(any(u) and any(v), "zero witness")
            require(all(dot(x, u) >= 0 or dot(y, v) >= 0
                        for x, y in zip(a, b)), "invalid uncovered pair")
            return [list(map(str, u)), list(v)]
    raise ValueError("negative control has no certified uncovered pair")


def validate_dimension(d):
    a, b = directions(d)
    n = len(a)
    digest = sha256()

    def record(obj):
        digest.update(json.dumps(obj, separators=(",", ":"), sort_keys=True).encode())
        digest.update(b"\n")

    record({"a": a, "b": b})
    blocks = []
    wrap_blocks = 0
    determinants = []
    for start in range(n):
        indices = tuple((start + r) % n for r in range(d + 1))
        vectors = [a[j] for j in indices]
        weights = circuit(vectors)
        # Independent comparison with the proof's explicit Lagrange weights.
        raw = [F((-1) ** j, prod(j - k for k in indices if k != j)) for j in indices]
        normalized = tuple(w / sum(raw) for w in raw)
        require(weights == normalized, "elimination disagrees with Lagrange")
        blocks.append(set(indices))
        wrap_blocks += int(start + d >= n)
        determinants.append(det(vectors[:-1]))
        record([indices, list(map(str, weights))])
    for i in range(n):
        require((determinants[(i + 1) % n] > 0)
                == ((-1) ** d * determinants[i] > 0),
                "cyclic determinant sign recurrence failed")
    cells = normal_cells(b)
    minimum = n
    for kind, v in cells:
        active = {i for i in range(n) if dot(b[i], v) < 0}
        minimum = min(minimum, len(active))
        require(len(active) >= d + 1, "too few active directions")
        chosen = next((i for i, block in enumerate(blocks) if block <= active), None)
        require(chosen is not None, "no certified positive circuit in active set")
        if kind == "boundary":
            require(sum(dot(y, v) == 0 for y in b) == 1, "boundary degeneracy")
        else:
            require(all(dot(y, v) != 0 for y in b), "cell point lies on boundary")
        record([kind, v, sorted(active), chosen])
    require(minimum == d + 1, "unexpected minimum semicircle count")
    require(len(cells) == 4 * n, "normal arrangement is incomplete")
    return {"d": d, "directions": n, "positive_circuits": n,
            "wrap_circuits": wrap_blocks, "boundary_cells": 2 * n,
            "open_cells": 2 * n, "minimum_active": minimum,
            "sha256": digest.hexdigest()}


def negative_controls():
    out = {}
    for d in (1, 3, 5):
        a, b = directions(d, 2 * d + 3)
        out[f"odd_dimension_{d}_one_too_few"] = uncovered_pair(a, b)
    a, b = directions(3)
    changed = list(a)
    changed[0] = tuple(-x for x in changed[0])
    out["flipped_first_moment_vector"] = uncovered_pair(changed, b)
    changed_b = list(b)
    changed_b[0] = (0, 0)
    out["zero_first_planar_vector"] = uncovered_pair(a, changed_b)
    # Every direction is necessary in these optimal small constructions.
    deletion_count = 0
    for d in range(1, 7):
        a, b = directions(d)
        for i in range(len(a)):
            uncovered_pair(a[:i] + a[i + 1:], b[:i] + b[i + 1:])
            deletion_count += 1
    out["certified_single_direction_deletions"] = deletion_count
    return out


def main():
    rows = [validate_dimension(d) for d in range(1, 17)]
    result = {"arithmetic": "Python arbitrary-precision integers and Fraction",
              "scope": "finite corroboration; universal theorem in PROOF.md",
              "dimensions": rows, "negative_controls": negative_controls()}
    path = Path(__file__).with_name("EXPECTED.json")
    require(path.is_file(), "missing EXPECTED.json")
    require(result == json.loads(path.read_text()), "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
