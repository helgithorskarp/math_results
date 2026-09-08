#!/usr/bin/env python3
"""Independent exact audit of the H510 near-injective realization theorem.

This deliberately imports none of the reviewed Python modules and does not use
their rank bases, orientation-prefix cover, or polynomial combinations.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd, isqrt
from pathlib import Path
import random


PACKAGE = "hadwiger_nelson_heule510_plane_realizations"
SIBLING = "hadwiger_nelson_parts509_heule_union_minimum"
ALIGN = f"{SIBLING}/aligned_510.json"
UNION = f"{SIBLING}/union_510.json"
RAD = (1, 3, 5, 15, 11, 33, 55, 165)
QZERO = (F(0), F(0))
QONE = (F(1), F(0))
RANK_PRIME = 1_000_000_009
ORIENTATION_PRIME = 1_000_000_097


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for d in range(3, isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True


def norm2(p, q):
    """Square a difference in the multiquadratic radical basis."""
    out = defaultdict(F)
    for axis in range(2):
        terms = [(RAD[i], p[axis][i] - q[axis][i]) for i in range(8)]
        terms = [(r, a) for r, a in terms if a]
        for r, a in terms:
            for s, b in terms:
                common = gcd(r, s)
                out[r * s // (common * common)] += a * b * common
    return tuple(sorted((r, a) for r, a in out.items() if a))


def load_and_derive(root: Path):
    pkg = root / PACKAGE
    pins = json.loads((pkg / "inputs.json").read_text())
    require(set(pins) == {ALIGN, UNION}, "unexpected input pins")
    raw = {}
    for name, digest in pins.items():
        data = (root / name).read_bytes()
        require(sha256(data).hexdigest() == digest, f"input hash: {name}")
        raw[name] = json.loads(data)

    aligned = raw[ALIGN]
    require(aligned["vtx"] == "510.vtx", "source identity")
    points = []
    for point in aligned["aligned_H"]:
        require(len(point) == 2 and all(len(axis) == 8 for axis in point), "point shape")
        points.append(tuple(tuple(F(x) for x in axis) for axis in point))
    require(len(points) == len(set(points)) == 510, "source distinctness")
    require(points[0] == ((F(0),) * 8, (F(0),) * 8), "origin label")

    # Derive the graph from all pairs, rather than inheriting the union edge list.
    unit = ((1, F(1)),)
    edges = []
    for v in range(510):
        for u in range(v):
            if norm2(points[u], points[v]) == unit:
                edges.append((u, v))
    edges.sort()
    require(len(edges) == 2504, "independent strict-edge census")

    union = raw[UNION]
    union_points = [tuple(tuple(F(x) for x in axis) for axis in point) for point in union["points"]]
    require(len(union_points) == len(set(union_points)) == 553, "union distinctness")
    lookup = {point: i for i, point in enumerate(union_points)}
    h_to_u = [lookup[p] for p in points]
    back = {u: h for h, u in enumerate(h_to_u)}
    inherited = sorted(
        (min(back[u], back[v]), max(back[u], back[v]))
        for u, v in union["edges"]
        if u in back and v in back
    )
    require(inherited == edges, "independent edge list differs from restricted union")

    K = []
    for x, y in points:
        require(all(not x[i] for i in (1, 3, 4, 6)), "unexpected x radical")
        require(all(not y[i] for i in (0, 2, 5, 7)), "unexpected y radical")
        K.append((x[0], x[2], x[5], x[7], y[1], y[3], y[4], y[6]))
    return points, edges, K


def build_rhombi(edges, K):
    adj = [set() for _ in range(510)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    rows = []
    opposite = {}
    for a, b in combinations(range(510), 2):
        common = tuple(sorted(adj[a] & adj[b]))
        require(len(common) <= 2, "source K2,3")
        if len(common) == 2 and (a, b) < common:
            rid = len(rows)
            row = (a, b, common[0], common[1])
            rows.append(row)
            require((a, b) not in opposite and common not in opposite, "reused opposite pair")
            opposite[(a, b)] = rid
            opposite[common] = rid
    require(len(rows) == 3953 and len(opposite) == 7906, "rhombus census")
    for a, b, c, d in rows:
        require(all(K[a][j] + K[b][j] == K[c][j] + K[d][j] for j in range(8)),
                "archived kernel identity")
    return rows, adj, opposite


def sparse_basis(rows, order, prime):
    """Select independent rows using sparse modular elimination."""
    pivots = {}
    selected = []
    for rid in order:
        a, b, c, d = rows[rid]
        row = {a: 1, b: 1, c: prime - 1, d: prime - 1}
        while row:
            col = min(row)
            if col not in pivots:
                inv = pow(row[col], -1, prime)
                pivots[col] = {j: value * inv % prime for j, value in row.items()}
                selected.append(rid)
                break
            factor = row[col]
            for j, value in pivots[col].items():
                new = (row.get(j, 0) - factor * value) % prime
                if new:
                    row[j] = new
                else:
                    row.pop(j, None)
    return selected


def dense_rank_mod(rows, prime):
    matrix = [[int(F(x).numerator) * pow(int(F(x).denominator), -1, prime) % prime
               for x in row] for row in rows]
    rank = 0
    width = len(matrix[0])
    for col in range(width):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [x * inv % prime for x in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][col]:
                factor = matrix[i][col]
                matrix[i] = [(x - factor * y) % prime for x, y in zip(matrix[i], matrix[rank])]
        rank += 1
        if rank == width:
            break
    return rank


def quotient_k23(edges, collision_pairs):
    parent = list(range(510))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def merge(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a

    for a, b in collision_pairs:
        merge(a, b)
    require(not any(find(u) == find(v) for u, v in edges), "collision collapses an edge")
    qadj = defaultdict(set)
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            qadj[a].add(b)
            qadj[b].add(a)
    reps = sorted({find(i) for i in range(510)})
    for i, a in enumerate(reps):
        for b in reps[i + 1:]:
            common = sorted(qadj[a] & qadj[b])
            if len(common) >= 3:
                return (a, b, common[0], common[1], common[2])
    raise ValueError("exceptional quotient has no K2,3")


def audit_rank_resilience(rows, adj, opposite, K, edges):
    require(is_prime(RANK_PRIME), "review rank modulus is not prime")
    require(dense_rank_mod([(F(1),) + tuple(k) for k in K], RANK_PRIME) == 9,
            "nine kernel columns not independent")

    orders = [list(range(len(rows))), list(reversed(range(len(rows))))]
    for seed in range(30):
        order = list(range(len(rows)))
        random.Random(10_000 + seed).shuffle(order)
        orders.append(order)
    bases = [sparse_basis(rows, order, RANK_PRIME) for order in orders]
    require(all(len(basis) == 501 for basis in bases), "review modular row rank")

    sets = [set(basis) for basis in bases]
    full = (1 << len(sets)) - 1
    masks = [sum(1 << j for j, basis in enumerate(sets) if rid in basis)
             for rid in range(len(rows))]
    require(all(mask != full for mask in masks), "uncovered single invalid row")
    pair_hits = [(r, s) for r, s in combinations(range(len(rows)), 2)
                 if masks[r] | masks[s] == full]
    require(len(pair_hits) == 2, f"review bases leave {len(pair_hits)} row pairs")

    k23 = []
    for r, s in pair_hits:
        for p in (rows[r][:2], rows[r][2:]):
            for q in (rows[s][:2], rows[s][2:]):
                k23.append(quotient_k23(edges, (p, q)))
    require(len(k23) == 8, "exceptional quotient coverage")

    graph = [set() for _ in range(510)]
    for u, v in opposite:
        graph[u].add(v)
        graph[v].add(u)
    triangle_count = 0
    triangle_hits = []
    for u in range(510):
        for v in sorted(w for w in graph[u] if w > u):
            for w in sorted(graph[u] & graph[v]):
                if w <= v:
                    continue
                triangle_count += 1
                ids = tuple(sorted((opposite[(u, v)], opposite[(u, w)], opposite[(v, w)])))
                require(len(set(ids)) == 3, "triple has repeated invalid row")
                if masks[ids[0]] | masks[ids[1]] | masks[ids[2]] == full:
                    triangle_hits.append(((u, v, w), ids))
    require(triangle_count == 31582, "opposition-triangle census")
    require(len(triangle_hits) == 2, "unexpected triple rank exceptions")
    require(all(any(set(pair).issubset(ids) for pair in pair_hits) for _, ids in triangle_hits),
            "triple exception not reduced to impossible pair")
    return {
        "review_rank_prime": RANK_PRIME,
        "review_rank_bases": len(bases),
        "rhombi": len(rows),
        "rank": 501,
        "pair_exceptions": [list(pair) for pair in pair_hits],
        "k23_quotients": len(k23),
        "opposition_triangles": triangle_count,
        "triple_exceptions": len(triangle_hits),
    }


class Quadratic:
    """Exact a+b*sqrt(square), represented by a pair of Fractions."""

    def __init__(self, square):
        self.square = square

    def add(self, x, y):
        return (x[0] + y[0], x[1] + y[1])

    def neg(self, x):
        return (-x[0], -x[1])

    def sub(self, x, y):
        return self.add(x, self.neg(y))

    def mul(self, x, y):
        return (x[0] * y[0] + self.square * x[1] * y[1],
                x[0] * y[1] + x[1] * y[0])

    def inv(self, x):
        den = x[0] * x[0] - self.square * x[1] * x[1]
        require(den != 0, "quadratic zero divisor")
        return (x[0] / den, -x[1] / den)

    def scale(self, x, q):
        q = F(q)
        return (q * x[0], q * x[1])

    def rational(self, q):
        return (F(q), F(0))

    def rref(self, rows, width):
        a = [list(row) for row in rows if any(x != QZERO for x in row)]
        rank = 0
        pivots = []
        for col in range(width):
            pivot = next((i for i in range(rank, len(a)) if a[i][col] != QZERO), None)
            if pivot is None:
                continue
            a[rank], a[pivot] = a[pivot], a[rank]
            inverse = self.inv(a[rank][col])
            a[rank] = [self.mul(x, inverse) for x in a[rank]]
            for i in range(len(a)):
                if i != rank and a[i][col] != QZERO:
                    factor = a[i][col]
                    a[i] = [self.sub(x, self.mul(factor, y)) for x, y in zip(a[i], a[rank])]
            pivots.append(col)
            rank += 1
            if rank == len(a):
                break
        return a[:rank], pivots

    def reduce(self, vector, rref, pivots):
        out = list(vector)
        for row, pivot in zip(rref, pivots):
            if out[pivot] != QZERO:
                factor = out[pivot]
                out = [self.sub(x, self.mul(factor, y)) for x, y in zip(out, row)]
        return tuple(out)


class ModularQuadratic:
    """The finite field F_p[t]/(t^2+3), with -3 a nonsquare."""

    def __init__(self, prime):
        self.prime = prime
        require(is_prime(prime), "orientation modulus is not prime")
        require(pow(prime - 3, (prime - 1) // 2, prime) == prime - 1,
                "-3 is not a quadratic nonresidue")

    def add(self, x, y):
        return ((x[0] + y[0]) % self.prime, (x[1] + y[1]) % self.prime)

    def sub(self, x, y):
        return ((x[0] - y[0]) % self.prime, (x[1] - y[1]) % self.prime)

    def mul(self, x, y):
        return ((x[0] * y[0] - 3 * x[1] * y[1]) % self.prime,
                (x[0] * y[1] + x[1] * y[0]) % self.prime)

    def inv(self, x):
        den = (x[0] * x[0] + 3 * x[1] * x[1]) % self.prime
        require(den, "finite-field zero inverse")
        inverse = pow(den, -1, self.prime)
        return (x[0] * inverse % self.prime, -x[1] * inverse % self.prime)

    def rational(self, q):
        q = F(q)
        return (q.numerator * pow(q.denominator, -1, self.prime) % self.prime, 0)

    def rref(self, rows, width):
        zero = (0, 0)
        a = [list(row) for row in rows if any(x != zero for x in row)]
        rank = 0
        pivots = []
        for col in range(width):
            pivot = next((i for i in range(rank, len(a)) if a[i][col] != zero), None)
            if pivot is None:
                continue
            a[rank], a[pivot] = a[pivot], a[rank]
            inverse = self.inv(a[rank][col])
            a[rank] = [self.mul(x, inverse) for x in a[rank]]
            for i in range(len(a)):
                if i != rank and a[i][col] != zero:
                    factor = a[i][col]
                    a[i] = [self.sub(x, self.mul(factor, y)) for x, y in zip(a[i], a[rank])]
            pivots.append(col)
            rank += 1
            if rank == len(a):
                break
        return a[:rank], pivots

    def reduce(self, vector, rref, pivots):
        out = list(vector)
        for row, pivot in zip(rref, pivots):
            if out[pivot] != (0, 0):
                factor = out[pivot]
                out = [self.sub(x, self.mul(factor, y)) for x, y in zip(out, row)]
        return tuple(out)


def canonical_direction(row):
    first = next(x for x in row if x)
    return tuple(row) if first > 0 else tuple(-x for x in row)


def derive_directions(edges, K):
    directions = sorted({canonical_direction(tuple(K[v][j] - K[u][j] for j in range(8)))
                         for u, v in edges})
    require(len(directions) == 36, "direction census")
    triads = []
    for i, j, k in combinations(range(36), 3):
        identities = []
        for sj, sk in product((-1, 1), repeat=2):
            if all(directions[i][h] + sj * directions[j][h] + sk * directions[k][h] == 0
                   for h in range(8)):
                identities.append((i, j, k, sj, -sk))
        if identities:
            require(len(identities) == 1, "ambiguous direction triad")
            triads.extend(identities)
    require(len(triads) == 12, f"found {len(triads)} direction triads")
    require(sorted(i for triad in triads for i in triad[:3]) == list(range(36)),
            "direction triads do not partition")
    return directions, triads


def audit_all_orientations(K, directions, triads):
    field = Quadratic(-3)
    modular = ModularQuadratic(ORIENTATION_PRIME)
    certified_loss_floor_hist = Counter()
    survivors = []
    for word in product((-1, 1), repeat=12):
        equations = []
        modular_equations = []
        for epsilon, (i, j, _, s, _) in zip(word, triads):
            factor = (F(-s, 2), F(epsilon, 2))
            equations.append([
                field.sub(field.rational(directions[j][h]),
                          field.mul(factor, field.rational(directions[i][h])))
                for h in range(8)
            ])
            modular_factor = (modular.rational(F(-s, 2))[0],
                              modular.rational(F(epsilon, 2))[0])
            modular_equations.append([
                modular.sub(modular.rational(directions[j][h]),
                            modular.mul(modular_factor, modular.rational(directions[i][h])))
                for h in range(8)
            ])
        basis, pivots = field.rref(equations, 8)
        modular_basis, modular_pivots = modular.rref(modular_equations, 8)
        groups = defaultdict(list)
        for vertex, row in enumerate(K):
            residue = modular.reduce(tuple(modular.rational(x) for x in row),
                                     modular_basis, modular_pivots)
            groups[residue].append(vertex)

        parent = list(range(510))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        exact_loss = 0
        for group in groups.values():
            if len(group) < 2:
                continue
            for u, v in combinations(group, 2):
                difference = tuple(field.rational(K[u][h] - K[v][h]) for h in range(8))
                if field.reduce(difference, basis, pivots) == (QZERO,) * 8:
                    a, b = find(u), find(v)
                    if a != b:
                        parent[b] = a
                        exact_loss += 1
                        if exact_loss >= 3:
                            break
            if exact_loss >= 3:
                break

        # A modular specialization is used only to propose exact equalities.
        # If it does not yield three verified losses, do the full exact census.
        if exact_loss < 3:
            normal = []
            for row in K:
                normal.append(field.reduce(tuple(field.rational(x) for x in row), basis, pivots))
            exact_loss = 510 - len(set(normal))
        loss = exact_loss
        certified_loss_floor_hist[loss] += 1
        if loss < 3:
            require(loss == 0 and len(basis) == 4, "unexpected near-injective orientation")
            sigma_found = []
            for sigma in (-1, 1):
                relations = []
                for x, y, denominator in ((0, 4, 1), (1, 5, 1), (2, 6, 3), (3, 7, 3)):
                    row = [QZERO] * 8
                    row[x] = (F(0), F(-sigma, denominator))
                    row[y] = QONE
                    relations.append(tuple(row))
                if all(field.reduce(row, basis, pivots) == (QZERO,) * 8 for row in relations):
                    sigma_found.append(sigma)
            require(len(sigma_found) == 1, "survivor frame identification")
            survivors.append((word, sigma_found[0]))
    require(len(survivors) == 2 and sorted(x[1] for x in survivors) == [-1, 1],
            "orientation survivor classification")
    return {
        "orientation_words_directly_enumerated": sum(certified_loss_floor_hist.values()),
        "orientation_survivors": len(survivors),
        "orientation_screen_prime": ORIENTATION_PRIME,
        "orientation_min_rejected_loss": min(k for k in certified_loss_floor_hist if k),
        "orientation_certified_loss_floor_histogram": {
            str(k): v for k, v in sorted(certified_loss_floor_hist.items())
        },
    }


def p_add(field, left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        value = field.add(out.get(monomial, QZERO), coefficient)
        if value == QZERO:
            out.pop(monomial, None)
        else:
            out[monomial] = value
    return out


def p_scale(field, poly, scalar):
    return {m: field.mul(c, scalar) for m, c in poly.items() if field.mul(c, scalar) != QZERO}


def p_mul(field, left, right):
    out = {}
    for a, ca in left.items():
        for b, cb in right.items():
            monomial = tuple(x + y for x, y in zip(a, b))
            value = field.add(out.get(monomial, QZERO), field.mul(ca, cb))
            if value == QZERO:
                out.pop(monomial, None)
            else:
                out[monomial] = value
    return out


def audit_polynomial_elimination(directions):
    field = Quadratic(33)
    zero_m = (0, 0, 0, 0)
    variables = [{tuple(int(i == j) for i in range(4)): QONE} for j in range(4)]
    const = lambda x: {zero_m: x}
    zero = {}
    one = const(QONE)
    c = (F(0), F(1))

    # Parameters A,B,C,D,E,F,G,H as real + t*imaginary, t^2=-3.
    params = [
        (one, zero),
        (variables[0], variables[1]),
        (const(c), zero),
        (variables[2], variables[3]),
        (zero, one),
        (p_scale(field, variables[1], field.rational(-3)), variables[0]),
        (zero, const(field.scale(c, F(1, 3)))),
        (p_scale(field, variables[3], field.rational(-1)),
         p_scale(field, variables[2], field.rational(F(1, 3)))),
    ]
    equations = []
    for direction in directions:
        real = {}
        imag = {}
        for coefficient, (r, i) in zip(direction, params):
            real = p_add(field, real, p_scale(field, r, field.rational(coefficient)))
            imag = p_add(field, imag, p_scale(field, i, field.rational(coefficient)))
        equation = p_add(field, p_mul(field, real, real),
                         p_scale(field, p_mul(field, imag, imag), field.rational(3)))
        equation = p_add(field, equation, const(field.rational(-1)))
        equations.append(equation)

    targets = {
        "b2_plus_3y2_minus_5": p_add(
            field,
            p_add(field, p_mul(field, variables[0], variables[0]),
                  p_scale(field, p_mul(field, variables[1], variables[1]), field.rational(3))),
            const(field.rational(-5))),
        "y": variables[1],
        "z": variables[3],
        "d_minus_c_b": p_add(field, variables[2], p_scale(field, variables[0], field.neg(c))),
    }
    monomials = sorted({m for poly in equations + list(targets.values()) for m in poly})
    require(len(monomials) == 13, f"quadratic monomial census: {len(monomials)}")
    rows = [[poly.get(m, QZERO) for m in monomials] for poly in equations]
    basis, pivots = field.rref(rows, len(monomials))
    for name, poly in targets.items():
        vector = tuple(poly.get(m, QZERO) for m in monomials)
        require(field.reduce(vector, basis, pivots) == (QZERO,) * len(monomials),
                f"target polynomial not implied: {name}")
    return {"unit_polynomial_rows": len(equations), "unit_polynomial_monomials": len(monomials),
            "unit_polynomial_rank": len(basis),
            "independently_derived_identities": sorted(targets)}


def audit_four_drawings(points, edges, K):
    hashes = []
    for sign5, sign11 in product((-1, 1), repeat=2):
        transformed = []
        for point, row in zip(points, K):
            axes = [list(point[0]), list(point[1])]
            for axis in range(2):
                for j, rad in enumerate(RAD):
                    factor = (-1 if sign5 == -1 and rad % 5 == 0 else 1)
                    factor *= (-1 if sign11 == -1 and rad % 11 == 0 else 1)
                    axes[axis][j] *= factor
            transformed.append((tuple(axes[0]), tuple(axes[1])))
            expected = (row[0], sign5 * row[1], sign11 * row[2], sign5 * sign11 * row[3],
                        row[4], sign5 * row[5], sign11 * row[6], sign5 * sign11 * row[7])
            actual = (axes[0][0], axes[0][2], axes[0][5], axes[0][7],
                      axes[1][1], axes[1][3], axes[1][4], axes[1][6])
            require(actual == expected, "normalized parameter/Galois mismatch")
        require(len(set(transformed)) == 510, "conjugate point collision")
        require(all(norm2(transformed[u], transformed[v]) == ((1, F(1)),) for u, v in edges),
                "conjugate edge failure")
        serial = repr(transformed).encode()
        hashes.append(sha256(serial).hexdigest())
    return {"normalized_drawings": 4, "unit_incidence_checks": 4 * len(edges),
            "review_drawing_hashes": hashes}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_root", type=Path)
    args = parser.parse_args()
    points, edges, K = load_and_derive(args.source_root)
    rows, adj, opposite = build_rhombi(edges, K)
    result = {"source_vertices": len(points), "strict_source_edges": len(edges)}
    result.update(audit_rank_resilience(rows, adj, opposite, K, edges))
    directions, triads = derive_directions(edges, K)
    result.update(unit_directions=len(directions), independently_derived_triads=len(triads))
    result.update(audit_all_orientations(K, directions, triads))
    result.update(audit_polynomial_elimination(directions))
    result.update(audit_four_drawings(points, edges, K))
    result["status"] = "INDEPENDENT_H510_NEAR_INJECTIVE_CLASSIFICATION_VERIFIED"
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
