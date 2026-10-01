#!/usr/bin/env python3
"""Exact replay of a Boolean cube with two differently marked pendant edges.

Standard library only. The credited definition checker is verify.py.
Literal cube orders 3..6; the theorem's unbounded coverage is analytic.
"""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
import verify as base


def dot(u, v):
    return sum(x*y for x, y in zip(u, v))


def matvec(a, v):
    return [dot(row, v) for row in a]


def gram(a, coefficients, independent):
    images = [matvec(a, c) for c in coefficients]
    sparse = [[(i, x) for i, x in enumerate(c) if x] for c in coefficients]
    return [[sum(x*images[j][k] for k, x in sparse[i])+independent[i][j]
             for j in range(len(coefficients))] for i in range(len(coefficients))]


def sector_check(q):
    """Rational congruences of the complete three- and two-dimensional frames."""
    base.require(type(q) is int and q >= 4, "frame parameter q>=4")
    n = 2*q+4
    b = F(q-4, 2*q)
    eta = F(q*q+10*q-16, 4*q)
    squares = [F(q, 3), F(2*q*(q-2), 3*(q+1)), F((q+2)*(q-1), q+1)]
    diagonal = [1+F(3*q, 2), F(1), F(q+2)]
    gaps = [n-z for z in diagonal]
    theta = sum(z/g for z, g in zip(squares, gaps))/2
    base.require(theta < 1-F(2, q+6), "symmetric rank-one cap budget")
    base.require(min(gaps) == F(q+6, 2), "smallest symmetric diagonal gap")
    symmetric = [[(gaps[i]-1)*squares[i]*int(i == j)-squares[i]*squares[j]/2
                  for j in range(3)] for i in range(3)]
    base.require(base.psd_rank(symmetric) == 3, "symmetric frame unit margin")
    anti_squares = [F(q), eta]  # Basis H_x-H_y, W.
    v_dot = [b*q, eta]
    anti_diag = [1+F(q, 2), F(0)]
    antisymmetric = [[(n-1-anti_diag[i])*anti_squares[i]*int(i == j)-2*v_dot[i]*v_dot[j]
                      for j in range(2)] for i in range(2)]
    base.require(base.psd_rank(antisymmetric) == 2, "antisymmetric frame unit margin")
    base.require(q*b*b+eta == F(q+1, 2), "leaf variance identity")
    trace_anti = 1+F(q, 2)+2*(q*b*b+eta)
    base.require(trace_anti == F(3*q, 2)+2 and n-trace_anti >= 4,
                 "antisymmetric trace cap")
    base.require(3+2+(q-2)+(q-3) == 2*q, "complete frame dimension")
    return {"q": q, "symmetric_rank": 3, "antisymmetric_rank": 2,
            "symmetric_theta": str(theta), "theta_gap_lower": str(F(2, q+6)),
            "antisymmetric_trace": str(trace_anti), "old_high_multiplicity": q-2,
            "old_low_multiplicity": q-3, "frame_rank": 2*q}


def build(n):
    base.require(type(n) is int and 3 <= n <= 6, "literal cube order3..6 guard")
    q = 1 << (n-1)
    s, total, full = q+1, 2*q+4, 2*q-1
    x, y, a, d = 1, 2, 1 << n, 1 << (n+1)
    family = list(range(2*q))+[a, a | x, d, d | y]
    old = list(range(1, 2*q))
    m = len(old)
    c0 = [[F(s*int(u == v)+q*int(u ^ v == full)-1) for v in old] for u in old]
    base.require(base.psd_rank(c0) == m, "shifted old cube is positive definite")
    ex, ey = [F(-bool(u & x)) for u in old], [F(-bool(u & y)) for u in old]
    base.require(matvec(c0, ex) == ex and matvec(c0, ey) == ey,
                 "marked star vectors belong to eigenvalue-one space")
    one = [F(1)]*m
    k = [z+u+v for z, u, v in zip(one, ex, ey)]
    delta = [u-v for u, v in zip(ex, ey)]
    hg = [(z-1)/(q+1) for z in matvec(c0, one)]
    kp = [(u+v)/3 for u, v in zip(ex, ey)]
    k0 = [z-h+F(2, 3)*(u+v) for z, h, u, v in zip(one, hg, ex, ey)]
    frame_vectors = [kp, k0, hg, delta]
    frame_gram = gram(c0, frame_vectors, [[F(0)]*4 for _ in range(4)])
    expected_norms = [F(q, 3), F(2*q*(q-2), 3*(q+1)),
                      F((q+2)*(q-1), q+1), F(q)]
    base.require(frame_gram == [[expected_norms[i]*int(i == j) for j in range(4)]
                               for i in range(4)], "literal orthogonal frame decomposition")
    base.require(matvec(c0, hg) == [(q+2)*z for z in hg] and matvec(c0, k0) == k0,
                 "literal high/low frame eigenvalues")
    b, eta = F(q-4, 2*q), F(q*q+10*q-16, 4*q)
    coefficients = [[F(i == j) for j in range(m)] for i in range(m)]
    coefficients += [[-z/2+b*t for z, t in zip(k, delta)], ex,
                     [-z/2-b*t for z, t in zip(k, delta)], ey]
    signs = [0]*m+[1, 0, -1, 0]
    seed = gram(c0, coefficients, [[eta*u*v for v in signs] for u in signs])
    base.require(all(sum(row) == 0 for row in seed), "centered seed identity")
    raw_coefficients = [row[:] for row in coefficients]
    raw_coefficients[m] = [-z/q for z in ex]
    raw_coefficients[m+2] = [-z/q for z in ey]
    residual = [[F(q*q-1, q)*int(i == j and i in (m, m+2))
                 for j in range(total-1)] for i in range(total-1)]
    raw = gram(c0, raw_coefficients, residual)
    row_form = sum(map(sum, raw))
    trace = (total-1)*(s-1)+row_form
    base.require(row_form == 4*q-4+F(1, q), "raw constant-form identity")
    base.require(trace == 2*q*q+7*q-4+F(1, q), "raw Q trace identity")
    epsilon = 1/(2*(1+trace))
    mixed = [[(1-epsilon)*seed[i][j]+epsilon*raw[i][j] for j in range(total-1)]
             for i in range(total-1)]
    return family, s, q, seed, raw, mixed, epsilon, trace


def check_literal(n):
    family, s, q, seed, raw, mixed, epsilon, trace = build(n)
    total = len(family)
    sm, rm, mm = base.lift(seed, s), base.lift(raw, s), base.lift(mixed, s)
    checked, sc = base.check(family, mm, s), base.check(family, sm, s)
    base.require(checked["lower_rank"] == total-2 and checked["upper_rank"] == total-1,
                 "repaired endpoint ranks")
    base.require(sc["lower_rank"] == total-3 and sc["upper_rank"] == total-1,
                 "centered seed endpoint ranks")
    base.require(base.psd_rank(raw) == total-3, "raw core has only the two forced kernels")
    base.require(base.psd_rank([[(total-1)*int(i == j)-seed[i][j]
                                for j in range(total-1)] for i in range(total-1)]) == total-1,
                 "seed frame margin1")
    # This checks the claimed gap on the original indices, independently of sector formulas.
    half = [[(total-s)*(int(i == j)-mm[i][j])-F(1, 2)*(int(i == j)-F(1, total))
             for j in range(total)] for i in range(total)]
    base.require(base.psd_rank(half) == total-1, "original-index repaired half-gap")
    base.require(mm == [[(1-epsilon)*sm[i][j]+epsilon*rm[i][j] for j in range(total)]
                       for i in range(total)], "core/full mixture identity")
    stars = [[int(bool(z & mark)) for z in family] for mark in (1, 2)]
    lower = [[(total-s)*mm[i][j]+s*int(i == j) for j in range(total)] for i in range(total)]
    for star in stars:
        centered = [F(z)-F(s, total) for z in star]
        base.require(matvec(lower, centered) == [0]*total, "forced maximum-star null vector")
    checked.update(cube_order=n, q=q, ground_points=n+2,
                   seed_lower_rank=sc["lower_rank"], seed_sha256=sc["matrix_sha256"],
                   raw_lower_rank=total-2, raw_matrix_sha256=base.fingerprint(rm),
                   epsilon=str(epsilon), raw_Q_trace=str(trace),
                   scaled_seed_margin=1, scaled_repaired_margin="1/2",
                   nonunit_upper_gap_lower=str(F(1, 2*(q+3))))
    return checked


def rejection_controls():
    checked = []

    def reject(label, function):
        try:
            function()
        except ValueError:
            checked.append(label)
            return
        raise ValueError("rejection control accepted: "+label)

    for n, label in ((2, "small order"), (7, "literal size guard"),
                     (3.0, "floating order"), (True, "Boolean order")):
        reject(label, lambda n=n: build(n))
    reject("small frame parameter", lambda: sector_check(3))
    family, s, _, _, _, c, _, _ = build(3)
    good = base.lift(c, s)
    bad = [row[:] for row in good]
    bad[0][0] += 1
    reject("corrupt row sum", lambda: base.check(family, bad, s))
    bad = [row[:] for row in good]
    i, j = 1, 3  # Old {x} and {x,y}; perturb while preserving symmetry and row sums.
    bad[i][j] += 1; bad[j][i] += 1
    bad[i][0] -= 1; bad[0][i] -= 1
    bad[j][0] -= 1; bad[0][j] -= 1
    bad[0][0] += 2
    reject("corrupt intersecting entry", lambda: base.check(family, bad, s))
    reject("wrong star parameter", lambda: base.check(family, good, s-1))
    reject("negative PSD pivot", lambda: base.psd_rank([[-1, 0], [0, 1]]))
    reject("zero pivot nonzero residual", lambda: base.psd_rank([[0, 1], [1, 0]]))
    return checked


def results():
    entries = [check_literal(n) for n in range(3, 7)]
    parameters = sorted(set([1 << k for k in range(2, 21)]+[5, 6, 7, 31, 10000]))
    sectors = [sector_check(q) for q in parameters]
    return {"schema": 1, "author": "six-downset-1", "role": "researcher",
            "status": "author-checked unformalized proof; exact finite validation",
            "coverage": {"literal_cube_orders": [3, 4, 5, 6], "largest_literal_N": 68,
                         "all_order_theorem": "n>=3; proved in TWO_MARKED_CUBE.md",
                         "scalar_frame_fixtures": len(sectors)},
            "entries": entries, "frame_fixtures": sectors,
            "rejection_controls": rejection_controls()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    answer = results()
    encoded = (json.dumps(answer, indent=2, sort_keys=True)+"\n").encode()
    if args.write:
        args.write.write_bytes(encoded)
    else:
        base.require(json.loads(args.check.read_text()) == answer, "expected-result mismatch")
        base.require(args.check.read_bytes() == encoded, "expected-result byte mismatch")
    print(json.dumps({"literal_instances": len(answer["entries"]),
                      "frame_fixtures": len(answer["frame_fixtures"]),
                      "rejection_controls": len(answer["rejection_controls"]),
                      "largest_N": 68, "results_sha256": sha256(encoded).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
