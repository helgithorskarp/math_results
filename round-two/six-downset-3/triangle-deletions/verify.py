#!/usr/bin/env python3
"""Exact infinite signs, literal certificates, compression identities and controls."""
import bootstrap
import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import resource
from time import monotonic
from poly import R, polynomial, exact_divide
from exact import require, schur_psd, polynomial_psd, lift, integral, digest
from signs import lower_sign
from floor import regenerate
from certificate import scalar, restricted, trade, construct, literal_base, template_rayleigh
from linear import solve, inverse, energy

ROOT = Path(__file__).resolve().parent


def dot(v, w):
    return sum(x*y for x, y in zip(v, w))


def trade_checks(domain, families, r, ell, positive):
    size = len(r)
    require(all(not r[i][i] and all(r[i][j] == r[j][i] and (not r[i][j] or not domain[i+1]&domain[j+1])
                    for j in range(size)) for i in range(size)), 'trade support/symmetry differs')
    require(all(dot(row, families[0]) == 0 for row in r), 'trade forced-star kernel differs')
    extras = [[x-y for x, y in zip(families[h], families[3])] for h in [1, 2]]
    gram = [[sum(v[i]*r[i][j]*w[j] for i in range(size) for j in range(size)) for w in extras] for v in extras]
    require(gram == [[2, 0], [0, 2]], 'extra-kernel trade form differs')
    require(all(r[i][j] == sum((v[i]*v[j]-w[i]*w[j])/2 for v, w in zip(positive, ell))
                for i in range(size) for j in range(size)), 'positive/negative rank-two split differs')
    return extras


def audit(q, k, characteristic):
    info, domain, star, repaired = construct(q, k)
    n, s = info['N'], info['s']
    original_domain, seed, families, _ = restricted(q, k)
    require(original_domain == domain, 'literal domains differ')
    r, ell, positive = trade(domain)
    extras = trade_checks(domain, families, r, ell, positive)
    require(all(dot(row, v) == 0 for row in seed for v in [star]+extras), 'restricted kernel differs')
    require(schur_psd(seed) == n-4, 'restricted PSD/rank differs')
    included = set(domain)
    require(n == len(domain) and all(a^(1 << i) in included for a in domain for i in range(q+3) if a >> i & 1),
            'literal downward closure/cardinality differs')
    actual_stars = [sum(a >> i & 1 for a in domain) for i in range(q+3)]
    require(actual_stars == [s, s-k, s-k]+[q+5]*k+[q+6]*(q-k), 'literal actual stars differ')
    require(dot(star, star) == s and all(dot(row, star) == 0 for row in repaired), 'repaired saturated star differs')
    upper = [[F(n*int(i == j)-1)-repaired[i][j] for j in range(n-1)] for i in range(n-1)]
    require(schur_psd(repaired) == n-2 and schur_psd(upper) == n-1, 'repaired core PSD/ranks differ')
    gap = [[upper[i][j]-info['gamma']/2*int(i == j) for j in range(n-1)] for i in range(n-1)]
    schur_psd(gap)
    l = lift(repaired)
    full_upper = [[F(n*int(i == j))-l[i][j] for j in range(n)] for i in range(n)]
    require(schur_psd(l) == n-1 and schur_psd(full_upper) == n-1, 'full slack PSD/ranks differ')
    upper_lift = lift(upper)
    require(all(upper_lift[i][j]-1 == full_upper[i][j] for i in range(n) for j in range(n)), 'upper lift identity differs')
    m = [[F(l[i][j]-s*int(i == j))/(n-s) for j in range(n)] for i in range(n)]
    require(all(sum(row) == 1 for row in m), 'whole row sums differ')
    require(all(m[i][j] == m[j][i] for i in range(n) for j in range(n)), 'whole symmetry differs')
    require(all(not m[i][j] for i, a in enumerate(domain) for j, b in enumerate(domain) if a & b), 'whole support differs')
    centered = [n*int(a & 1 != 0)-s for a in domain]
    require(all(dot(row, centered) == 0 for row in l), 'centered whole star differs')
    cp = polynomial_psd(repaired) if characteristic else None
    up = polynomial_psd(upper) if characteristic else None
    if characteristic:
        require(cp[0] == n-2 and up[0] == n-1, 'characteristic positivity/rank differs')
    nums, den = integral(m)
    return {'q': q, 'k': k, 'N': n, 's': s, 'chi': str(info['chi']), 'gamma': str(info['gamma']),
            't': str(info['t']), 'rank_L': n-1, 'rank_upper': n-1, 'M_denominator': den,
            'M_numerators_sha256': digest(nums), 'C_polynomial_sha256': cp[1] if cp else None,
            'U_polynomial_sha256': up[1] if up else None, 'literal_upper_gap_bound_pass': True}


def compression_check(k):
    q = 4
    domain, cp, families, old = restricted(q, k)
    base_domain, c, base_families, keep = old
    n, s = len(domain), 3*q+4
    m0 = len(c)
    removed = [i for i in range(m0) if i not in keep]
    a0 = [[F(n*int(i == j))-c[i][j] for j in range(m0)] for i in range(m0)]
    rhs = [[F(1)]+[F(int(i == j)) for j in removed] for i in range(m0)]
    solved = solve(a0, rhs)
    b1 = [r[0] for r in solved]
    bs = [[solved[i][h+1] for h in range(k)] for i in removed]
    binv = inverse(bs)
    rest = [[F(n*int(i == j))-cp[i][j] for j in range(n-1)] for i in range(n-1)]
    rest_solve = solve(rest, [[F(1)] for _ in rest])
    lhs = sum(r[0] for r in rest_solve)
    rhs = sum(b1)-sum(b1[i]*binv[h][j]*b1[removed[j]] for h, i in enumerate(removed) for j in range(k))
    require(lhs == rhs, 'inverse compression identity differs')
    c0, alpha = F(1, 2), F(q*(q+1), 2)+F(3*(q+1), 3*q+5)
    h0, g = F(1, 3*q+5), n-2*s
    require(all(b1[i] == (n-c0+c0*h0)/(n*(n-c0)) for i in removed), 'removed resolvent constant differs')
    require(sum(b1) == F(m0, n)+c0*alpha/(n*(n-c0)), 'resolvent constant energy differs')
    require(sum(sum(row) for row in bs) <= F(k*(n-s-k), n*g), 'resolvent compression energy bound differs')
    r, ell, positive = trade(domain)
    trade_checks(domain, families, r, ell, positive)
    anchors = [domain[1:].index(a) for a in [1, 2, 4]]
    restricted_energy = energy(cp, ell, anchors)
    full_ell = [[F(0)]*m0 for _ in ell]
    for h, v in enumerate(ell):
        for i, j in enumerate(keep):
            full_ell[h][j] = v[i]
        for j in removed:
            full_ell[h][j] = -F(1, k)
    require(all(dot(v, f) == 0 for v in full_ell for f in base_families), 'range extensions do not annihilate old kernel')
    old_anchors = [base_domain[1:].index(a) for a in [1, 2, 4, 3]]
    old_energy = energy(c, full_ell, old_anchors)
    require(restricted_energy == old_energy, 'restricted/base range energy identity differs')
    ygram = [[dot(v, w) for w in full_ell] for v in full_ell]
    require(ygram == [[3+F(1, k), 1+F(1, k)], [1+F(1, k), 3+F(1, k)]], 'extension Gram differs')
    schur_psd([[4*ygram[i][j]-old_energy[i][j] for j in range(2)] for i in range(2)])
    return {'q': q, 'k': k, 'compression_energy': str(lhs),
            'range_energy_sha256': digest([[str(v) for v in row] for row in old_energy]),
            'all_compression_and_range_identities_pass': True}


def base_floor_literal():
    q = 4
    _, c, families = literal_base(q)
    gram = [[dot(v, w) for w in families] for v in families]
    inv = inverse(gram)
    size = len(c)
    projected = [[F(int(i == j))-sum(families[a][i]*inv[a][b]*families[b][j]
                    for a in range(4) for b in range(4)) for j in range(size)] for i in range(size)]
    shifted = [[c[i][j]-projected[i][j]/4 for j in range(size)] for i in range(size)]
    require(schur_psd(shifted) == size-4, 'literal quarter-floor rank differs')
    return {'q': q, 'floor': '1/4', 'literal_shifted_rank': size-4}


def uniform_trade_obstruction(q, k):
    domain, c, families, _ = restricted(q, k)
    size, points = len(c), q+3
    delta = []
    for a in domain[1:]:
        row = []
        for b in domain[1:]:
            sizes = tuple(sorted((a.bit_count(), b.bit_count())))
            weight = (points-2)*(points-3) if sizes == (1, 1) else -(points-3) if sizes == (1, 2) else 1 if sizes == (2, 2) else 0
            row.append(F(weight if not a & b else 0))
        delta.append(row)
    v = [x-y for x, y in zip(families[1], families[3])]
    w = [dot(row, v) for row in delta]
    require(all(dot(row, v) == 0 for row in c), 'obstruction vector is not in restricted kernel')
    require(dot(v, w) == 0 and dot(w, w) == F(3*q*(q+1)*(6*q-1), 2), 'uniform trade obstruction identities differ')
    require(dot(w, w) > 0, 'uniform trade obstruction vanishes')
    return {'q': q, 'k': k, 'uniform_trade_kernel_quadratic': '0', 'uniform_trade_residual_norm_squared': str(dot(w, w)),
            'two_by_two_determinant': '-t^2*'+str(dot(w, w)**2),
            'scope': 'restricted base core plus any nonzero scalar of the full all-star singleton/pair trade'}


def controls(expected):
    tested = []
    def reject(name, callback):
        try:
            callback()
        except (ValueError, TypeError, ZeroDivisionError):
            tested.append(name)
        else:
            raise ValueError('Damage control accepted: '+name)
    for name, q, k in [('q_below_generic_scope', 3, 1), ('floating_q', 4.0, 1), ('boolean_k', 4, True),
                       ('zero_deletion', 4, 0), ('too_many_deletions', 4, 5), ('unmet_sufficient_cap_condition', 4, 2)]:
        reject(name, lambda q=q, k=k: scalar(q, k))
    bad_hashes = dict(bootstrap.EXPECTED); bad_hashes['poly.py'] = '0'*64
    reject('changed_pinned_dependency', lambda: bootstrap.setup(expected=bad_hashes))
    reject('negative_floor_constant', lambda: lower_sign(polynomial((-1, 1))))
    reject('negative_floor_nonconstant', lambda: lower_sign(polynomial((1, -1))))
    reject('floating_polynomial', lambda: polynomial((1, 0.5)))
    reject('zero_symbolic_denominator', lambda: R(1, 0))
    reject('nonexact_polynomial_division', lambda: exact_divide(polynomial(1), polynomial((1, 1))))
    reject('floating_linear_system', lambda: solve([[0.5]], [[F(1)]]))
    reject('singular_linear_system', lambda: solve([[F(0)]], [[F(1)]]))
    domain, _, families, _ = restricted(4, 1)
    r, ell, positive = trade(domain)
    broken = copy.deepcopy(r); i, j = domain[1:].index(1), domain[1:].index(2); broken[i][j] = broken[j][i] = 0
    reject('missing_balancing_trade_edge', lambda: trade_checks(domain, families, broken, ell, positive))
    simple = [[F(0)]*len(r) for _ in r]
    i, j = domain[1:].index(2), domain[1:].index(4); simple[i][j] = simple[j][i] = 1
    extras = [[x-y for x, y in zip(families[h], families[3])] for h in [1, 2]]
    bad_gram = [[sum(v[i]*simple[i][j]*w[j] for i in range(len(r)) for j in range(len(r))) for w in extras] for v in extras]
    reject('two_smaller_singletons_trade_is_not_positive_on_extra_kernel', lambda: schur_psd(bad_gram))
    bad = copy.deepcopy(expected); bad['signs'][0]['coefficients'][0] = '0'
    reject('changed_stored_floor_coefficient', lambda: require(bad == expected, 'signs differ'))
    bad2 = copy.deepcopy(expected); bad2['signs'].pop()
    reject('missing_floor_sign', lambda: require(bad2 == expected, 'signs differ'))
    reject('floating_matrix', lambda: schur_psd([[0.5]]))
    reject('indefinite_zero_pivot', lambda: schur_psd([[F(0), F(1)], [F(1), F(0)]]))
    reject('negative_characteristic_root', lambda: polynomial_psd([[F(-1)]]))
    positives = [([[F(0)]], 0), ([[F(2, 3)]], 1), ([[F(1), F(1)], [F(1), F(1)]], 1)]
    for matrix, rank in positives:
        require(schur_psd(matrix) == polynomial_psd(matrix)[0] == rank, 'positive control differs')
    return {'rejections': tested, 'rejection_count': len(tested), 'positive_matrix_controls': len(positives)}


def replay():
    expected = json.loads((ROOT/'SIGNS.json').read_text())
    actual = regenerate()
    require(actual == expected, 'stored infinite certificates differ')
    literal = [audit(q, k, characteristic) for q, k, characteristic in [(4, 1, True), (5, 1, True), (6, 1, True), (10, 2, False)]]
    compression = [compression_check(k) for k in [1, 2, 4]]
    obstruction = [uniform_trade_obstruction(4, k) for k in [1, 2, 4]]
    require(template_rayleigh(4, 4) == F(-551, 34), 'zero-total cap separator differs')
    region = []
    for q, k in [(12, 1), (24, 2), (60, 5), (120, 10), (1200, 100)]:
        data = scalar(q, k)
        require(q >= 12*k and data['chi'] > 0 and 0 < data['t'] <= F(1, 48), 'proved large-region scalar check differs')
        region.append({key: str(data[key]) if isinstance(data[key], F) else data[key] for key in data})
    result = {'agent': 'six-downset-3', 'role': 'researcher', 'infinite_floor_sign_count': actual['sign_count'],
              'infinite_single_deletion_cap_sign_count': 1, 'infinite_certificates_sha256': actual['certificate_sha256'],
              'literal_certificates': literal, 'compression_and_range_checks': compression,
              'literal_base_floor': base_floor_literal(), 'uniform_trade_obstructions': obstruction,
              'zero_total_cap_separator_q4_k4': '-551/34', 'large_region_scalar_checks': region,
              'controls': controls(expected)}
    result['records_sha256'] = digest(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-results', type=Path)
    args = parser.parse_args()
    start = monotonic(); result = replay()
    if args.write_results:
        args.write_results.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(result == json.loads((ROOT/'RESULTS.json').read_text()), 'stored results differ')
    print(json.dumps({'passed': True, 'floor_signs': result['infinite_floor_sign_count'],
                      'literal_case_count': len(result['literal_certificates']),
                      'compression_identity_count': len(result['compression_and_range_checks']),
                      'damage_rejections': result['controls']['rejection_count'],
                      'records_sha256': result['records_sha256'], 'seconds': round(monotonic()-start, 3),
                      'peak_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
