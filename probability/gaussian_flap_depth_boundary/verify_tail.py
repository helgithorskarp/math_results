#!/usr/bin/env python3
"""Exact algebra/geometry controls for TAIL_BLOWUP.md, using stdlib only.

This is not a verifier of the analytic limit or the surface-integral proof.
The octant area moment is an analytic input explained in TAIL_BLOWUP.md.
No quadrature, stochastic search, numerical optimizer, or large data is used.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def vec(values):
    return tuple(map(F, values))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def poly_add(*terms):
    result = {}
    for term in terms:
        for exponents, coefficient in term.items():
            result[exponents] = result.get(exponents, F(0)) + coefficient
    return {k: v for k, v in result.items() if v}


def poly_scale(c, term):
    return {k: c*v for k, v in term.items() if c*v}


def poly_mul(left, right):
    result = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            key = (a+c, b+d)
            result[key] = result.get(key, F(0)) + x*y
    return {k: v for k, v in result.items() if v}


def gram_identities():
    one, lam, eta = {(0, 0): F(1)}, {(1, 0): F(1)}, {(0, 1): F(1)}
    plus = poly_add(lam, eta)
    denominator = poly_add(one, poly_mul(lam, eta))
    q_squared = poly_add(one, poly_scale(-1, poly_mul(lam, lam)))
    h_squared_complement = poly_add(one, poly_scale(-1, poly_mul(eta, eta)))
    norm_left = poly_add(poly_mul(plus, plus),
                         poly_mul(h_squared_complement, q_squared))
    require(norm_left == poly_mul(denominator, denominator), 'first Gram identity')
    require(poly_add(poly_mul(lam, plus), q_squared) == denominator,
            'cross Gram identity')
    derivative_numerator = poly_add(denominator, poly_scale(-1, poly_mul(eta, plus)))
    require(derivative_numerator == h_squared_complement,
            'monotone physical coefficient derivative')
    return 3


def check_geometry(vertices, normals, heights):
    require(dot(sub(vertices[1], vertices[0]),
                cross(sub(vertices[2], vertices[0]), sub(vertices[3], vertices[0]))) != 0,
            'tetrahedron must be nondegenerate')
    count = 0
    for i in range(4):
        require(heights[i] > 0, 'normal heights must be positive')
        for k in range(4):
            for j in range(4):
                require(dot(normals[i], sub(vertices[k], vertices[j])) ==
                        heights[i]*((k == i)-(j == i)), 'normal/edge dual identity')
                count += 1
    return count


def band_constants(vertices, normals, heights, i, j, edge_bound, gap_bound, normal_bound):
    k, ell = [z for z in range(4) if z not in (i, j)]
    require(edge_bound > 0 and gap_bound > 0 and normal_bound > 0, 'positive bounds')
    edge = sub(vertices[i], vertices[j])
    normal_sum = add(normals[k], normals[ell])
    require(0 < dot(edge, edge) <= edge_bound**2, 'edge norm bound')
    require(0 < dot(normal_sum, normal_sum) <= normal_bound**2, 'normal sum norm bound')
    require(dot(edge, normal_sum) == 0, 'wall direction is perpendicular to edge')
    for z in (k, ell):
        gap_vector = sub(vertices[i], vertices[z])
        require(dot(gap_vector, gap_vector) <= gap_bound**2, 'gap vector norm bound')
        require(-dot(gap_vector, normal_sum) == heights[z], 'strict wall gap numerator')
    delta = min(heights[k], heights[ell])/normal_bound
    rho = min(F(1, 4), delta/(8*gap_bound))
    require(delta > 0 and 0 < rho <= F(1, 4), 'positive angular patch radius')
    require(2*gap_bound*rho <= delta/4, 'patch projection error bound')
    # Used in the proof for |b|<=1/4 and B/(R E)<=delta/8.
    require(F(3, 4)*F(7, 8)-F(1, 8) >= F(1, 2), 'band retains half the wall gap')
    return {'delta': delta, 'rho': rho, 'coefficient': rho**3/(24*edge_bound)}


def fixture():
    vertices = tuple(map(vec, ((0, 0, 0), (2, 0, 0), (1, 3, 0), (1, 1, 4))))
    normals = tuple(map(vec, (('-1/2', '-1/6', '-1/12'), (1, '-1/3', '-1/6'),
                              (0, 1, '-1/4'), (0, 0, '5/4'))))
    heights = vec((1, 2, 3, 5))
    dual_count = check_geometry(vertices, normals, heights)
    vertex_bound, normal_bound = F(5), F(2)
    require(all(dot(v, v) <= vertex_bound**2 for v in vertices), 'vertex norm bound')
    require(all(dot(d, d) <= normal_bound**2 for d in normals), 'moving vector norm bound')
    constants = {}
    for i in range(4):
        for j in range(4):
            if i != j:
                constants[i, j] = band_constants(vertices, normals, heights, i, j,
                                                  F(5), F(5), F(2))
    chosen = band_constants(vertices, normals, heights, 1, 0, F(2), F(5), F(2))
    require(chosen['delta'] == F(3, 2) and chosen['rho'] == F(3, 80),
            'displayed asymmetric angular constants')
    wi, beta = F(1, 4), F(1, 16)
    coefficient = heights[1]*wi*beta*chosen['coefficient']
    require(coefficient == F(9, 262144000), 'displayed strict lower bound coefficient')
    gamma = sum(heights[i]*wi*beta for i, j in constants)
    require(gamma == F(33, 64), 'uniform sixteen-label Gamma')
    c_geometry = min(v['coefficient'] for v in constants.values())
    total_coefficient = sum(heights[i]*wi*beta*c['coefficient']
                            for (i, j), c in constants.items())
    require(total_coefficient >= c_geometry*gamma > 0, 'summed weight-uniform lower bound')
    center_bound = vertex_bound+normal_bound
    return {'normal_edge_identities': dual_count, 'ordered_pair_bands': len(constants),
            'V': str(vertex_bound), 'D': str(normal_bound), 'M': str(center_bound),
            'Gamma': str(gamma), 'selected_pair_i_j': [1, 0],
            'selected_delta': str(chosen['delta']), 'selected_rho': str(chosen['rho']),
            'selected_L0_prefactor': str(coefficient),
            'exponential_constant': str(3*(2+center_bound**2)),
            'exponential_tau_coefficient': str(6*normal_bound),
            'common_c_geometry': str(c_geometry),
            'summed_L_prefactor_using_E5_B5_N2': str(total_coefficient)}


def normalization_and_isometry_controls():
    vertices = tuple(map(vec, ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))))
    normals = tuple(map(vec, ((-1, -1, -1), (1, 0, 0), (0, 1, 0), (0, 0, 1))))
    heights = vec((1, 1, 1, 1))
    dual_count = check_geometry(vertices, normals, heights)
    alpha = vec((0, '1/4', '1/4', '1/4'))
    beta = {(1, 0): F(1, 4)}
    w = tuple(alpha[j]+sum(m for (i, tip), m in beta.items() if tip == j)
              for j in range(4))
    require(w == (F(1, 4),)*4 and sum(w) == 1, 'normalization fixture weights')
    require(normals[1] == vec((1, 0, 0)), 'linear logarithmic integrand coordinate')
    require(all(sub(vertices[j], vertices[0]) == normals[j] for j in (1, 2, 3)),
            'tip zero fan is the negative octant')
    gamma = sum(heights[i]*mass*w[i] for (i, j), mass in beta.items())
    # Analytic input: integral over negative octant of theta_1 is -pi/4.
    # The code only checks multiplication by the exact log-ratio coefficient -2.
    pi_tau_coefficient = F(-2)*F(-1, 4)
    require(pi_tau_coefficient == F(1, 2) and gamma == F(1, 16),
            'analytic octant normalization coefficient')

    # A separate zero-Gamma control: equal core and flap mass at the same tip.
    iso_alpha, iso_beta = vec(('1/2', 0, 0, 0)), {(2, 0): F(1, 2)}
    iso_w = tuple(iso_alpha[j]+sum(m for (i, tip), m in iso_beta.items() if tip == j)
                  for j in range(4))
    iso_gamma = sum(heights[i]*mass*iso_w[i] for (i, j), mass in iso_beta.items())
    require(sum(iso_w) == 1 and iso_gamma == 0, 'zero-Gamma control')
    # The two weighted labels are v0 and v0 +/- t d2. Their entire squared
    # distance polynomial is (0,0,|d2|^2) on both sides.
    base_difference = sub(vertices[0], vertices[0])
    source_velocity = tuple(-x for x in normals[2])
    target_velocity = normals[2]
    minus_poly = (dot(base_difference, base_difference),
                  2*dot(base_difference, source_velocity), dot(source_velocity, source_velocity))
    plus_poly = (dot(base_difference, base_difference),
                 2*dot(base_difference, target_velocity), dot(target_velocity, target_velocity))
    require(minus_poly == plus_poly == (0, 0, 1), 'isometric positive-label distance')
    # Point reflection x -> 2v0-x maps both affine trajectories exactly.
    require(tuple(-x for x in source_velocity) == normals[2], 'explicit reflection witness')
    return {'normal_edge_identities': dual_count, 'octant_Gamma': str(gamma),
            'octant_L_coefficient_of_pi_tau': str(pi_tau_coefficient),
            'octant_moment_is_written_analytic_input': '-pi/4',
            'isometry_Gamma': str(iso_gamma),
            'isometry_squared_distance_polynomial': list(map(str, minus_poly))}


def run():
    return {'scope': 'Exact controls only; analytic tail and strict-sign proofs are in TAIL_BLOWUP.md',
            'universal_polynomial_identities': gram_identities(),
            'asymmetric_fixture': fixture(),
            'normalization_and_isometry': normalization_and_isometry_controls()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare with TAIL_EXPECTED.json')
    args = parser.parse_args()
    result = run()
    canonical = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    if args.check:
        expected = Path(__file__).with_name('TAIL_EXPECTED.json').read_bytes()
        require(canonical == expected, 'TAIL_EXPECTED.json mismatch')
        print('PASS: three universal polynomial identities; 128 normal/edge identities; 12 angular bands')
        print('PASS: exact positive coefficient; octant normalization algebra; reflection equality control')
        print('TAIL_EXPECTED.json sha256', hashlib.sha256(canonical).hexdigest())
    else:
        print(canonical.decode(), end='')


if __name__ == '__main__':
    main()
