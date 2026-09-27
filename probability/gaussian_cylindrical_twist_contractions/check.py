#!/usr/bin/env python3
"""Exact algebra and controls for the cylindrical-twist proof; no numerics."""
from fractions import Fraction as F
from itertools import combinations
import json
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


# Sparse polynomials in eight formal real variables.
NVAR = 8


def constant(q):
    return {(0,) * NVAR: F(q)} if q else {}


def variable(i):
    e = [0] * NVAR
    e[i] = 1
    return {tuple(e): F(1)}


def plus(*polys):
    result = {}
    for p in polys:
        for e, q in p.items():
            result[e] = result.get(e, F(0)) + q
    return {e: q for e, q in result.items() if q}


def scale(p, q):
    return {e: c*q for e, c in p.items() if c*q}


def times(p, q):
    result = {}
    for e, a in p.items():
        for f, b in q.items():
            g = tuple(x+y for x, y in zip(e, f))
            result[g] = result.get(g, F(0)) + a*b
    return {e: q for e, q in result.items() if q}


def square(p):
    return times(p, p)


def minus(p, q):
    return plus(p, scale(q, -1))


ONE = constant(1)


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def subtract(x, y):
    return tuple(a-b for a, b in zip(x, y))


def norm(x):
    return dot(x, x)


def eliminate(rows):
    rows = [[F(x) for x in row] for row in rows]
    rank, determinant = 0, F(1)
    for c in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        if pivot != rank:
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            determinant *= -1
        value = rows[rank][c]
        determinant *= value
        rows[rank] = [q/value for q in rows[rank]]
        for i in range(len(rows)):
            if i != rank:
                value = rows[i][c]
                rows[i] = [q-value*r for q, r in zip(rows[i], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank, determinant if rank == len(rows) == len(rows[0]) else None


def polynomial_checks():
    a, h, q, x, y, dx, dy, dz = (variable(i) for i in range(NVAR))
    s = minus(ONE, square(a))
    # (5), multiplied by S=1-a^2. This checks all coefficients, not samples.
    image_x = times(a, minus(dx, times(times(q, y), dz)))
    image_y = times(a, plus(dy, times(times(q, x), dz)))
    image_z = times(h, dz)
    lhs = times(s, minus(plus(square(dx), square(dy), square(dz)),
                         plus(square(image_x), square(image_y), square(image_z))))
    completed_x = plus(times(s, dx), times(times(times(square(a), q), y), dz))
    completed_y = minus(times(s, dy), times(times(times(square(a), q), x), dz))
    remainder = minus(times(s, minus(ONE, square(h))),
                      times(times(square(a), square(q)), plus(square(x), square(y))))
    rhs = plus(square(completed_x), square(completed_y), times(remainder, square(dz)))
    require(lhs == rhs, 'differential square completion')
    completion_terms = len(lhs)
    # Relative contraction identity (13), with denominators cleared.
    k, r, s, t, hp, tp = (variable(i) for i in range(6))
    ks2 = plus(minus(ONE, s), times(s, square(hp)))
    kt2 = plus(minus(ONE, t), times(t, square(hp)))
    interval = minus(t, s)
    budget = minus(times(k, minus(ONE, square(hp))), times(square(r), square(tp)))
    lhs = minus(times(k, minus(ks2, kt2)), times(interval, times(square(r), square(tp))))
    rhs = times(interval, budget)
    require(lhs == rhs, 'relative motion budget')
    relative_terms = len(lhs)
    # Axial leapfrog identity (16).
    xx, yy, fx, fy, t = (variable(i) for i in range(5))
    delta, fd = minus(xx, yy), minus(fx, fy)
    lhs = plus(square(plus(times(minus(ONE, t), delta), times(t, fd))),
               times(times(t, minus(ONE, t)), square(minus(delta, fd))))
    rhs = plus(times(minus(ONE, t), square(delta)), times(t, square(fd)))
    require(lhs == rhs, 'axial leapfrog')
    leapfrog_terms = len(lhs)
    # (25): a strict gap for every 0<a<1, with x=sqrt(a).
    x = variable(0)
    lhs = minus(times(square(plus(ONE, x)), plus(ONE, square(x))), scale(square(x), 8))
    rhs = times(square(minus(ONE, x)), plus(square(x), scale(x, 4), ONE))
    require(lhs == rhs, 'strict gap from every C1 phase clock of the linear-meridian motion')
    return {'identities': 4, 'completion_terms': completion_terms,
            'relative_budget_terms': relative_terms, 'axial_leapfrog_terms': leapfrog_terms,
            'phase_budget_gap_terms': len(lhs)}


def parameter_controls():
    count = 0
    # These include saturated budgets, zero axial speed, no twist and
    # both signs of each derivative. They are controls, not a continuum proof.
    for a, r in ((F(3, 5), F(1)), (F(1, 2), F(2)), (F(4, 5), F(1, 2))):
        k = a**-2 - 1
        for hp in (F(-4, 5), F(-3, 5), F(0), F(3, 5), F(4, 5)):
            for tp in (F(-16, 15), F(-4, 5), F(0), F(4, 5), F(16, 15)):
                budget = k*(1-hp*hp)-r*r*tp*tp
                if budget < 0:
                    continue
                for s, t in combinations((F(0), F(1, 7), F(1, 3), F(2, 3), F(6, 7)), 2):
                    ks2, kt2 = 1-s+s*hp*hp, 1-t+t*hp*hp
                    relative_scale2 = (1+k*s)/(1+k*t)
                    radius_s2 = r*r/(1+k*s)
                    angle_derivative2 = (t-s)**2*tp*tp/ks2
                    axis_derivative2 = kt2/ks2
                    defect = 1-axis_derivative2-relative_scale2/(1-relative_scale2)*radius_s2*angle_derivative2
                    require(defect == (t-s)*budget/(k*ks2) and defect >= 0,
                            'relative budget control')
                    count += 1
    # A piecewise affine profile can reverse axial and angular order while
    # saturating the same derivative budget on every piece.
    a, r = F(3, 5), F(1)
    k = a**-2-1
    slopes = ((F(3, 5), F(16, 15)), (F(-3, 5), F(-16, 15)),
              (F(0), F(4, 3)), (F(4, 5), F(-4, 5)))
    require(all(k*(1-h*h)-r*r*q*q == 0 for h, q in slopes), 'nonlinear profile budget')
    heights = [F(0)]
    unfolded = [F(0)]
    for h, _ in slopes:
        heights.append(heights[-1]+h)
        unfolded.append(unfolded[-1]+abs(h))
    for i, j in combinations(range(len(heights)), 2):
        require(abs(heights[j]-heights[i]) <= unfolded[j]-unfolded[i], 'fold factorization control')
    return count, len(slopes)


def geometry_controls():
    a = c = F(3, 5)
    omega = F(16, 15)
    k = a**-2-1
    require(c*c+omega*omega/k == 1, 'saturation')
    # Last coordinate records the coefficient of H=15*pi/32.
    source = [tuple(map(F, p)) for p in
              ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
               (1, 0, 1), (0, 1, 1), (0, 0, -1))]
    target = [(F(0), F(0), F(0)), (a, F(0), F(0)), (F(0), a, F(0)),
              (F(0), F(0), c), (F(0), a, c), (-a, F(0), c), (F(0), F(0), c)]
    paired = [[*x, *y] for x, y in zip(source[1:], target[1:])]
    rank, determinant = eliminate(paired)
    require(rank == 6 and determinant == 4*c*a*a, 'rank-six paired determinant')
    # 3<pi<22/7, hence (45/32)^2<H^2<(165/112)^2.
    low_h2, high_h2 = F(45, 32)**2, F(165, 112)**2
    minimum = None
    for i, j in combinations(range(7), 2):
        ds, dt = subtract(source[i], source[j]), subtract(target[i], target[j])
        constant_loss = norm(ds[:2])-norm(dt[:2])
        h2_coefficient = ds[2]**2-dt[2]**2
        lower = constant_loss+h2_coefficient*(low_h2 if h2_coefficient >= 0 else high_h2)
        require(lower > 0, 'benchmark endpoint contraction')
        minimum = lower if minimum is None else min(minimum, lower)
    # Zero-loss differential directions at phases pi/2 and pi, for four
    # boundary azimuths, give rank five and the unique e,f axis relation.
    rows = []
    for phase in (1, 2):
        for u in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ju = (-F(u[1]), F(u[0]))
            qju = (-ju[1], ju[0]) if phase == 1 else (-ju[0], -ju[1])
            src = (a*ju[0], a*ju[1], F(1))
            dst = (*qju, c)
            require(norm(src) == norm(dst), 'tight differential direction')
            rows.append([*src, *(-q for q in dst)])
    scalar_rank, _ = eliminate(rows)
    kernel = (F(0), F(0), c, F(0), F(0), F(1))
    require(scalar_rank == 5 and all(dot(row, kernel) == 0 for row in rows),
            'scalar-defect axis constraints')
    require(norm(kernel[:3]) != norm(kernel[3:]), 'no two unit axes in kernel')
    helicity_coefficient = 2*a*(c-1)
    require(helicity_coefficient == F(-12, 25), 'non-normal helicity')
    return {'sites': 7, 'endpoint_pairs': 21, 'strict_pairs': 21,
            'paired_affine_rank': rank, 'paired_determinant_over_H_squared': str(determinant),
            'minimum_certified_pair_loss': str(minimum),
            'scalar_differential_rows': len(rows), 'scalar_constraint_rank': scalar_rank,
            'scalar_kernel': [str(x) for x in kernel],
            'helicity_over_H': str(helicity_coefficient)}


def adverse_controls():
    a = c = F(3, 5)
    omega = F(16, 15)
    k = a**-2-1
    # Raising the twist slope violates the exact endpoint budget.
    bad_omega = F(17, 15)
    bad_budget = k*(1-c*c)-bad_omega**2
    require(bad_budget == F(-11, 75), 'overspeed budget must fail')
    # Linear schedules of transverse scale and axial scale expand a pair
    # infinitesimally at t=0 despite the valid endpoint budget.
    initial_pair_derivative = 2*(-(1-a)-(1-c)+omega)
    require(initial_pair_derivative == F(8, 15) and initial_pair_derivative > 0,
            'linear schedule must fail')
    # Radius loss cannot be dropped from the characterization.
    wrong_radius_budget = k*(1-c*c)-4*omega**2
    require(wrong_radius_budget < 0, 'wrong cylinder radius must fail')
    return {'rejected_controls': 3, 'overspeed_budget': str(bad_budget),
            'bad_linear_schedule_pair_derivative': str(initial_pair_derivative)}


def main():
    require(len(sys.argv) == 1, 'no arguments accepted')
    symbolic = polynomial_checks()
    parameter_count, profile_pieces = parameter_controls()
    result = {'symbolic': symbolic,
              'relative_parameter_controls': parameter_count,
              'nonlinear_profile_pieces': profile_pieces,
              'benchmark': geometry_controls(), 'adverse': adverse_controls()}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
