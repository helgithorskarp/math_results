#!/usr/bin/env python3
"""Exact finite controls; this does not mechanize the analytic theorem."""

import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def rref(matrix):
    a = [[F(x) for x in row] for row in matrix]
    row = 0
    pivots = []
    for col in range(len(a[0])):
        found = next((j for j in range(row, len(a)) if a[j][col]), None)
        if found is None:
            continue
        a[row], a[found] = a[found], a[row]
        pivot = a[row][col]
        a[row] = [x / pivot for x in a[row]]
        for j in range(len(a)):
            if j != row and a[j][col]:
                multiplier = a[j][col]
                a[j] = [x - multiplier*y for x, y in zip(a[j], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def inverse(a):
    n = len(a)
    require(all(len(row) == n for row in a), "inverse requires square matrix")
    augmented = [list(row) + [F(i == j) for j in range(n)]
                 for i, row in enumerate(a)]
    reduced, pivots = rref(augmented)
    require(pivots == list(range(n)), "singular matrix")
    inv = [row[n:] for row in reduced]
    require(all(sum(a[i][k]*inv[k][j] for k in range(n)) == F(i == j)
                for i in range(n) for j in range(n)), "inverse multiplication")
    return inv


def rigidity(points, edges):
    rows = []
    for i, j in edges:
        d = sub(points[i], points[j])
        row = [F(0)] * (3 * len(points))
        for k in range(3):
            row[3*i+k], row[3*j+k] = F(d[k]), F(-d[k])
        rows.append(row)
    return rows


def gauges(points, weights):
    rows = [[F(0)] * (3 * len(points)) for _ in range(6)]
    for i, (x, p) in enumerate(zip(points, weights)):
        for k in range(3):
            rows[k][3*i+k] = p
            unit = tuple(F(k == j) for j in range(3))
            torque = cross(x, unit)
            for j in range(3):
                rows[3+j][3*i+k] = p * torque[j]
    return rows


def ceiling(q):
    return -(-q.numerator // q.denominator)


def verify():
    points = [(i, i*i-4, i*i*i) for i in range(-3, 4)]
    n = len(points)
    weights = [F(1, n)] * n
    require(all(sum(p*x[k] for p, x in zip(weights, points)) == 0
                for k in range(3)), "source centering")
    for label, x in enumerate(points):
        normal = (2*x[0], -1, 0)
        require(all(dot(normal, x) > dot(normal, y)
                    for j, y in enumerate(points) if j != label),
                "vertex supporting functional")

    facets = []
    normals = {}
    for tri in combinations(range(n), 3):
        a, b, c = (points[i] for i in tri)
        normal = cross(sub(b, a), sub(c, a))
        signs = [dot(normal, sub(points[j], a)) for j in range(n) if j not in tri]
        require(all(signs), "four coplanar moment-curve sites")
        if all(s > 0 for s in signs):
            normal = tuple(-x for x in normal)
        elif not all(s < 0 for s in signs):
            continue
        facets.append(tri)
        normals[tri] = normal
    edges = sorted({edge for face in facets for edge in combinations(face, 2)})
    require(len(facets) == 10 and len(edges) == 15, "hull counts")
    require(all(sum(set(edge).issubset(face) for face in facets) == 2
                for edge in edges), "edge incidence")

    edge_matrix = rigidity(points, edges)
    gauge_matrix = gauges(points, weights)
    require(rank(edge_matrix) == 15, "edge rigidity rank")
    full_matrix = edge_matrix + gauge_matrix
    require(rank(full_matrix) == 21, "gauge rank")
    inv = inverse(full_matrix)
    # ||h_i||_2 <= sqrt(3) max_(coordinate,e)|inv[coordinate,e]| sum |s_e|.
    c_edge = 3 * max(abs(row[j]) for row in inv for j in range(len(edges)))
    require(c_edge > 0, "positive edge norm bound")

    covariance = [[sum(p*x[i]*x[j] for x, p in zip(points, weights))
                   for j in range(3)] for i in range(3)]
    require(covariance == [[4, 0, 28], [0, 12, 0], [28, 0, F(1588, 7)]],
            "covariance entries")
    require(covariance[0][0] > 0 and covariance[1][1] > 0
            and covariance[0][0]*covariance[2][2]-covariance[0][2]**2 > 0,
            "covariance positivity")
    inv_cov = inverse(covariance)
    kappa = 1 / max(sum(abs(a) for a in row) for row in inv_cov)
    radius = max(sum(abs(a) for a in x) for x in points)
    separation = min(max(abs(a) for a in sub(points[i], points[j]))
                     for i, j in combinations(range(n), 2))

    beta_bounds = []
    for edge in edges:
        adj = [face for face in facets if set(edge).issubset(face)]
        a, b = (normals[face] for face in adj)
        numerator = max(abs(v) for v in cross(a, b))
        require(numerator > 0, "positive normal angle")
        # alpha >= sin(alpha) = |a cross b|/(|a||b|), and l <= ||edge||_1.
        denominator = (2 * sum(abs(v) for v in a) * sum(abs(v) for v in b)
                       * sum(abs(v) for v in sub(points[edge[0]], points[edge[1]])))
        beta_bounds.append(F(numerator, denominator))
    beta = min(beta_bounds)
    c_width = beta / (2 * c_edge)
    m = radius + 1
    nu = F(separation, 2)
    b_tail = F(20*n*(n-1), 1) / nu
    # log(1/p_*)=log(7)<7 and pi<4 give rational upper bounds.
    a_tail_upper = 280*m + 248 + b_tail*(n + m*m)
    r0 = ceiling(max(F(2), 4*m, 16*a_tail_upper/c_width,
                     (16*b_tail/c_width)**2))
    require(r0 >= 2 and r0 >= 4*m, "radial cutoff")
    require(4*a_tail_upper/F(r0) <= c_width/4, "constant tail error")
    require(F(r0) >= (16*b_tail/c_width)**2, "logarithmic tail error")
    # beta*nu/(8*pi*C_E*N(N-1)) is bounded below using pi<4.
    geometric_displacement = beta*separation/(32*c_edge*n*(n-1))
    q_exponent = F((r0+2*radius)**2, 2) + (r0+4*radius)**2

    # An eighth, strictly interior atom at zero. Its uniform covariance
    # is 7/8 of the hull covariance, so the recorded floor scales exactly.
    offsets = [dot(normals[face], points[face[0]]) for face in facets]
    require(min(offsets) > 0, "centroid is strictly interior")
    rho = min(F(offset, sum(abs(a) for a in normals[face]))
              for face, offset in zip(facets, offsets))
    require(all(rho*sum(abs(a) for a in normals[face]) <= offset
                for face, offset in zip(facets, offsets)), "interior ball")
    kappa8 = F(7, 8) * kappa
    interior_factor = max(F(1), 2*radius/rho)
    c_edge8 = (2 + F(radius**2)/(2*kappa8)) * interior_factor * c_edge
    require(c_edge8 > 0 and rho > 0, "interior coercivity constants")
    covariance8 = [[F(7, 8)*v for v in row] for row in covariance]
    points8 = points + [(0, 0, 0)]
    require(all(sum(F(1, 8)*x[i]*x[j] for x in points8) == covariance8[i][j]
                for i in range(3) for j in range(3)), "interior covariance")
    require(rank(rigidity(points8, edges)) == 15 < 3*8-6,
            "interior argument needs contraction constraints, not edge rank alone")

    deleted_rank = rank(edge_matrix[:-1])
    deleted_gauge_rank = rank(edge_matrix[:-1] + gauge_matrix)
    require(deleted_rank == 14 and deleted_gauge_rank == 20, "deleted-edge control")
    cube = list(product((-1, 1), repeat=3))
    cube_edges = [(i, j) for i, j in combinations(range(8), 2)
                  if sum(a != b for a, b in zip(cube[i], cube[j])) == 1]
    cube_rank = rank(rigidity(cube, cube_edges))
    require(len(cube_edges) == 12 and cube_rank == 12 < 18, "cube control")

    i0 = F(factorial(0)) / F(2, 3)
    i12 = sum(F(factorial(k)) / F(2, 3)**(k+1) for k in (1, 2))
    require(i0 == F(3, 2) and i12 == 9, "exterior integral constants")
    require(F(9, 4)*2 + 4 == F(17, 2) <= 10, "off-wall error")
    require(F(25, 8)+1 == F(33, 8) <= 5, "wall error")
    require(5*i12 == 45 and 2*i12 == 18 and 2*i0+i12 == 12,
            "exterior derivative collection")
    # For R=2+s, 60R(M+1)-(45RM+18M+12)
    # has coefficients (constant,s,M,sM)=(108,60,12,15), all positive.
    residual = [60*2-12, 60, (60-45)*2-18, 60-45]
    require(residual == [108, 60, 12, 15] and min(residual) > 0,
            "exterior remainder polynomial")
    require(40+240 == 280 and 8+240 == 248, "tail constant collection")

    return {
        "status": "RIGID_HULL_RELATIVE_TAIL_EXACT_CONTROLS_PASS",
        "scope": "Finite rational controls only; the analytic theorem is not machine certified.",
        "points": points,
        "weights": [str(p) for p in weights],
        "facets": facets,
        "edges": edges,
        "rigidity_rank": 15,
        "augmented_rank": 21,
        "covariance": [[str(v) for v in row] for row in covariance],
        "constants": {
            "R_x_upper": str(radius), "nu_0_lower": str(separation),
            "kappa_lower": str(kappa), "C_E_upper": str(c_edge),
            "beta_lower": str(beta), "c_lower": str(c_width),
            "geometric_delta_lower": str(geometric_displacement),
            "A_tail_upper": str(a_tail_upper), "B_tail": str(b_tail),
            "R_0_integer": str(r0), "q_0_negative_log": str(q_exponent),
            "delta_star_expression": "min(1,nu_0/4,geometric_delta,kappa*exp(-q_0_negative_log)/(16*R_x))",
        },
        "negative_controls": {
            "deleted_edge_rank": deleted_rank,
            "deleted_edge_augmented_rank": deleted_gauge_rank,
            "cube_edge_rank": cube_rank,
            "meaning": "Failed rank hypotheses, not failed Gaussian inequalities.",
        },
        "tail_arithmetic": {
            "integrals": [str(i0), str(i12)],
            "exterior_residual_coefficients": residual,
            "combined_M_constant": 280, "combined_constant": 248,
        },
        "interior_atom_extension": {
            "point": [0, 0, 0], "all_weights": "1/8",
            "rho_lower": str(rho), "kappa_lower": str(kappa8),
            "K_upper": str(interior_factor), "C_E_upper": str(c_edge8),
            "hull_rigidity_rank": 15,
            "meaning": "Equation (5a) controls all eight velocities using the interior pair-strain inequalities.",
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare with committed EXPECTED.json")
    args = parser.parse_args()
    result = verify()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "EXPECTED.json mismatch")
        print(result["status"])
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
