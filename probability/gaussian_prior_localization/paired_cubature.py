#!/usr/bin/env python3
"""Exact paired cubature and finite-budget controls; no Gaussian sign evaluator."""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb, factorial, floor, isqrt
from pathlib import Path

from rational_frontier import norm2, rational, require, sub


def exponents(p):
    require(type(p) is int and p >= 0, "nonnegative integer degree")
    return [(a, b, t-a-b) for t in range(1, p+1)
            for a in range(t+1) for b in range(t-a+1)]


def monomial(x, alpha):
    return x[0]**alpha[0] * x[1]**alpha[1] * x[2]**alpha[2]


def data(xs, ys, weights):
    require(len(xs) == len(ys) == len(weights) and len(xs) > 0, "label counts")
    xs = [tuple(map(rational, x)) for x in xs]
    ys = [tuple(map(rational, y)) for y in ys]
    weights = list(map(rational, weights))
    require(all(len(x) == 3 for x in xs + ys), "dimension")
    require(all(w >= 0 for w in weights) and sum(weights) == 1, "probability weights")
    for i, j in combinations(range(len(xs)), 2):
        require(norm2(sub(xs[i], xs[j])) >= norm2(sub(ys[i], ys[j])),
                "expansion or inconsistent source collision")
    return xs, ys, weights


def null_vector(columns):
    """Return one exact nonzero dependence; all input columns have first entry1."""
    width = len(columns)
    matrix = [list(row) for row in zip(*columns)]
    pivots = []
    row = 0
    for col in range(width):
        pivot = next((j for j in range(row, len(matrix)) if matrix[j][col]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][col]
        matrix[row] = [v/scale for v in matrix[row]]
        for j in range(len(matrix)):
            if j != row and matrix[j][col]:
                scale = matrix[j][col]
                matrix[j] = [a-scale*b for a, b in zip(matrix[j], matrix[row])]
        pivots.append(col)
        row += 1
        if row == len(matrix):
            break
    free = next((j for j in range(width) if j not in pivots), None)
    require(free is not None, "no affine dependence")
    out = [F(0)] * width
    out[free] = F(1)
    for j, col in enumerate(pivots):
        out[col] = -matrix[j][free]
    require(all(sum(c[j]*v for c, v in zip(columns, out)) == 0
                for j in range(len(columns[0]))), "invalid dependence")
    require(any(v > 0 for v in out) and any(v < 0 for v in out), "affine signs")
    return out


def compress(xs, ys, weights, degree):
    """Preserve both marginal moments on shared actual sites and positive weights."""
    xs, ys, weights = data(xs, ys, weights)
    powers = exponents(degree)
    columns = [(F(1),) + tuple(monomial(x, a) for a in powers)
               + tuple(monomial(y, a) for a in powers) for x, y in zip(xs, ys)]
    cap = 2*comb(degree+3, 3)-1
    active = [j for j, w in enumerate(weights) if w]
    steps = 0
    while len(active) > cap:
        labels = active[:cap+1]
        v = null_vector([columns[j] for j in labels])
        step = min(weights[j]/u for j, u in zip(labels, v) if u > 0)
        for j, u in zip(labels, v):
            weights[j] -= step*u
            require(weights[j] >= 0, "negative cubature weight")
        newer = [j for j in active if weights[j]]
        require(len(newer) < len(active), "cubature did not eliminate a site")
        active = newer
        steps += 1
    return {"indices": active, "weights": [weights[j] for j in active],
            "degree": degree, "cap": cap, "eliminations": steps}


def verify_moments(xs, ys, weights, result):
    """Definition-level check of every marginal monomial, using no elimination data."""
    xs, ys, weights = data(xs, ys, weights)
    ids, p = result['indices'], result['degree']
    ws = list(map(rational, result['weights']))
    require(type(p) is int and p >= 0, "cubature verification degree")
    require(len(ids) == len(ws) <= 2*comb(p+3, 3)-1, "cubature support count")
    require(len(set(ids)) == len(ids) and all(type(i) is int and 0 <= i < len(xs)
                                               for i in ids), "cubature indices")
    require(all(w > 0 for w in ws) and sum(ws) == 1, "cubature masses")
    checked = 0
    for sites in (xs, ys):
        for a, b, c in product(range(p+1), repeat=3):
            if a+b+c > p:
                continue
            before = sum(w*x[0]**a*x[1]**b*x[2]**c for w, x in zip(weights, sites))
            after = sum(w*sites[i][0]**a*sites[i][1]**b*sites[i][2]**c
                        for i, w in zip(ids, ws))
            require(before == after, "marginal moment mismatch")
            checked += 1
    return checked


def tail_upper(a, degree):
    a = rational(a)
    require(a >= 0 and type(degree) is int and degree >= 0, "tail parameters")
    require(a < degree+2, "geometric tail ratio must be below one")
    return a**(degree+1)/factorial(degree+1)/(1-a/F(degree+2))


def pair_loss(xs, ys, weights):
    return sum((weights[i]*weights[j]
                * (norm2(sub(xs[i], xs[j]))-norm2(sub(ys[i], ys[j]))))
               for i, j in product(range(len(xs)), repeat=2))


def budget(k):
    require(type(k) is int and k >= 1, "positive integer k")
    ell = (k-1).bit_length()
    unit_degree = 2*ell+3
    unit_atoms = k**3*(2*comb(unit_degree+3, 3)-1)
    width = isqrt(ell+1)
    cells = (k+width-1)//width
    wide_degree = 4*ell+8
    wide_atoms = cells**3*(2*comb(wide_degree+3, 3)-1)
    cap = min(unit_atoms, wide_atoms)
    return {"k": k, "ell": ell, "unit_degree": unit_degree,
            "unit_atoms": unit_atoms, "wide_width": width,
            "wide_cells_per_axis": cells, "wide_degree": wide_degree,
            "wide_atoms": wide_atoms, "atoms": cap,
            "coordinate_denominator": 256*k**3,
            "weight_denominator": 4*k*cap, "largest_power": 2**16*k**8,
            "compact_error_bound": str(F(11, 4*k)),
            "rational_beta_error_bound": str(F(3107, 768*k))}


def check_grid(k, xs, ys, ns):
    b = budget(k)
    cap, L, W = b['atoms'], b['coordinate_denominator'], b['weight_denominator']
    require(len(xs) == len(ys) == len(ns) and 1 <= len(ns) <= cap, "grid label budget")
    require(all(len(p) == 3 and all(type(a) is int for a in p) for p in xs+ys),
            "integer grid centers")
    require(xs[0] == ys[0] == (0, 0, 0), "grid anchor")
    require(all(norm2(p) <= (3*k*L)**2 for p in xs+ys), "grid radius")
    require(all(type(n) is int and n >= 0 for n in ns) and sum(ns) == W, "grid masses")
    losses = [norm2(sub(xs[i], xs[j]))-norm2(sub(ys[i], ys[j]))
              for i, j in combinations(range(len(ns)), 2)]
    require(all(t >= 256*k*k for t in losses), "integer pair margin")
    expected = sum((F(ns[i]*ns[j], W*W*L*L)
                    * (norm2(sub(xs[i], xs[j]))-norm2(sub(ys[i], ys[j])))
                   for i, j in product(range(len(ns)), repeat=2)), F(0))
    positive = sum(n > 0 for n in ns)
    if positive >= 2:
        require(expected >= F(1, 2048*k**6*cap**2), "pair-loss floor")
    else:
        require(expected == 0, "point equality")
    return {"positive_weights": positive,
            "minimum_integer_pair_margin": min(losses) if losses else None,
            "ordered_expected_pair_loss": str(expected)}


def round_instance(k, xs, ys, weights):
    """The previous feasible-rounding proof with the NEW atom and mass budgets."""
    xs, ys, weights = data(xs, ys, weights)
    b = budget(k)
    cap, L, W = b['atoms'], b['coordinate_denominator'], b['weight_denominator']
    require(len(xs) <= cap, "compact atom budget")
    require(xs[0] == ys[0] == (0, 0, 0), "compact anchor")
    require(all(norm2(p) <= 4*k*k for p in xs+ys), "compact radius")
    radius = F(1, 4*k)
    expansion = 1+F(1, 8*k*k)
    reps = [0]
    for i in range(1, len(xs)):
        if all(norm2(sub(xs[i], xs[j])) > radius**2 for j in reps):
            reps.append(i)
    ws = [F(0)]*len(reps)
    for i, w in enumerate(weights):
        j = next(t for t, r in enumerate(reps) if norm2(sub(xs[i], xs[r])) <= radius**2)
        require(norm2(sub(ys[i], ys[reps[j]])) <= radius**2, "image merging error")
        ws[j] += w
    xx = [tuple(floor(L*expansion*a+F(1, 2)) for a in xs[i]) for i in reps]
    yy = [tuple(floor(L*a+F(1, 2)) for a in ys[i]) for i in reps]
    ns = [floor(W*w) for w in ws]
    missing = W-sum(ns)
    require(0 <= missing < len(ws), "largest-remainder count")
    order = sorted(range(len(ws)), key=lambda j: (-(W*ws[j]-ns[j]), j))
    for i in order[:missing]:
        ns[i] += 1
    error = sum(abs(w-F(n, W)) for w, n in zip(ws, ns))
    require(error <= F(len(ws), W) <= F(1, 4*k), "weight error")
    checked = check_grid(k, xx, yy, ns)
    return {"k": k, "input_atoms": len(xs), "output_atoms": len(ws),
            "atom_cap": cap, "coordinate_denominator": L, "weight_denominator": W,
            "source_integer_centers": xx, "target_integer_centers": yy,
            "weight_numerators": ns, "weight_l1_error": str(error), **checked}


def reject(action):
    try:
        action()
    except ValueError:
        return True
    return False


def report():
    base_unit = tail_upper(F(3, 4), 3)
    base_wide = F(16, 13)*F(9, 16)**9
    require(base_unit == F(135, 8704) < F(1, 64), "unit base tail")
    require(base_wide < F(1, 64) and F(9, 16)**4 < F(1, 4), "wide schedule constants")
    rows = []
    for k in [1, 2, 4, 8, 16, 64, 100, 128, 129, 256, 1000, 10000]:
        b = budget(k)
        unit = tail_upper(F(3, 4), b['unit_degree'])
        wide = tail_upper(F(3*b['wide_width']**2, 4), b['wide_degree'])
        require(unit < F(1, 64*k*k) and wide < F(1, 64*k*k), "uniform endpoint tails")
        require(F(11, 4)+F(2, 3)+F(161, 256) == F(3107, 768), "composed error")
        require(F(1, 2)+F(3107, 768*9) < 1, "epsilon consumer")
        require(F(2, b['weight_denominator']**2 * 256*k**4)
                == F(1, 2048*k**6*b['atoms']**2), "new pair-loss denominator")
        rows.append(b | {"old_atoms": k**6})

    xs = list(product([F(-3, 8), F(-1, 8), F(1, 8), F(3, 8)], repeat=3))
    ys = [(abs(x), y/2, z/3) for x, y, z in xs]
    weights = [F(i+1, sum(range(1, 65))) for i in range(64)]
    original_pair_loss = pair_loss(xs, ys, weights)
    cases = []
    grid_controls = []
    for p in [1, 2, 3]:
        result = compress(xs, ys, weights, p)
        checked = verify_moments(xs, ys, weights, result)
        ids, ws = result['indices'], result['weights']
        xx, yy = [xs[i] for i in ids], [ys[i] for i in ids]
        if p >= 2:
            require(pair_loss(xx, yy, ws) == original_pair_loss, "pair loss not preserved")
        # Independent endpoint translations anchor the retained geometry.
        ax, ay = xx[0], yy[0]
        grid = round_instance(1, [sub(x, ax) for x in xx], [sub(y, ay) for y in yy], ws)
        grid_controls.append({k: v for k, v in grid.items()
                              if k not in ['source_integer_centers', 'target_integer_centers', 'weight_numerators']})
        cases.append({"name": "nonlinear_absolute_value", "degree": p,
                      "input_atoms": len(xs), "output_atoms": len(ids),
                      "pair_loss_equality_checked": p >= 2,
                      "moment_equalities": checked, "indices": ids,
                      "weights": list(map(str, ws)), "eliminations": result['eliminations']})

    # Coincident source labels, zero weights, point/isometry boundaries.
    edge_x = [(0, 0, 0), (0, 0, 0), (F(1, 8), 0, 0), (F(-1, 8), 0, 0)]
    edge_y = list(edge_x)
    edge_w = [F(1, 3), 0, F(1, 3), F(1, 3)]
    edge = compress(edge_x, edge_y, edge_w, 1)
    verify_moments(edge_x, edge_y, edge_w, edge)
    grid_controls.append(round_instance(1, [(0, 0, 0)], [(0, 0, 0)], [1]))

    # Source-only linear moments need not match the image moments.
    require(sum([F(-1, 4), 0, F(1, 4)])/3 == 0, "source-only mean")
    target_mean_failure = (F(1, 4)+F(1, 4))/3
    require(target_mean_failure == F(1, 6), "source-only target mismatch")

    good = compress(xs, ys, weights, 1)
    damaged = dict(good)
    damaged['weights'] = good['weights'][:-1]
    controls = [
        reject(lambda: compress([(0, 0, 0)]*2, [(0, 0, 0), (1, 0, 0)], [F(1, 2)]*2, 1)),
        reject(lambda: compress([(0, 0, 0)], [(0, 0, 0)], [1.0], 1)),
        reject(lambda: verify_moments(xs, ys, weights, damaged)),
        reject(lambda: tail_upper(F(5), 1)),
        reject(lambda: check_grid(1, [(0, 0, 0)], [(0, 0, 0)], [4])),
    ]
    require(all(controls), "a malformed control was accepted")
    # Tensor cancellation checked directly in two different expansions.
    tensor_checks = 0
    result = compress(xs, ys, weights, 2)
    signed = [-w for w in weights]
    for i, w in zip(result['indices'], result['weights']):
        signed[i] += w
    for sites in (xs, ys):
        for j in range(3):
            pair = sum(signed[a]*signed[b]*sum(u*v for u, v in zip(sites[a], sites[b]))**j
                       for a, b in product(range(len(xs)), repeat=2))
            require(pair == 0, "Gaussian kernel polynomial cancellation")
            tensor_checks += 1
    return {"status": "PAIRED_CUBATURE_FRONTIER_CONTROLS_PASS",
            "unit_tail_base": str(base_unit), "wide_tail_base": str(base_wide),
            "budgets": rows, "cubatures": cases, "grid_controls": grid_controls,
            "source_only_target_mean_error": str(target_mean_failure),
            "original_ordered_pair_loss": str(original_pair_loss),
            "kernel_cancellation_controls": tensor_checks,
            "malformed_inputs_rejected": len(controls),
            "scope": "Exact finite controls and constants; no Gaussian moment, hinge sign, parameter cover or independent review."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.check:
        require(encoded == Path(__file__).with_name('CUBATURE_EXPECTED.json').read_text(),
                "expected cubature report mismatch")
    print(result['status'], sha256(encoded.encode()).hexdigest())
    if not args.check:
        print(encoded, end='')


if __name__ == '__main__':
    main()
