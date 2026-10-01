"""Exact support-to-margin constants; full G6 regeneration is still required.

Actual author six-sendov-1, researcher. The input is compact metadata
checked against the regenerated complete tensors by verify.py. This
arithmetic alone does not verify those tensors.
"""
from fractions import Fraction as F
from math import comb
import hashlib, json
from kernel import require
import controls as V


def tail_power(coefficients):
    n = len(coefficients)-1
    power = [F(0)]*(n+1)
    for i, value in enumerate(coefficients):
        for j in range(n-i+1):
            power[i+j] += value*comb(n, i)*comb(n-i, j)*(-1)**j
    return {j: value for j, value in enumerate(power) if value}


def unequal_controls(maximum_norm, light_lipschitz):
    def unit(h):
        return (1-h*h)/(1+h*h), 2*h/(1+h*h)
    def integral(b, heavy, first, second):
        light = [(F(1), F(0)), V.gs(V.ga(first, second), -b),
                 V.gs(V.gm(first, second), b*b)]
        total = F(0), F(0)
        for j in range(7):
            term = V.gs(V.gp(heavy, j), (-1)**j*comb(6, j)*b**j)
            for ell, coefficient in enumerate(light):
                total = V.ga(total, V.gs(V.gm(term, coefficient), F(9, j+ell+1)))
        return total
    records = []
    for b in (F(7, 8), F(15, 16), F(1)):
      for heavy_phase in (F(0), F(1, 5)):
       for center_phase in (F(0), F(1, 3)):
        for opening in (F(1, 10), F(1, 4)):
         for delta in (F(-1, 64), F(0), F(1, 64)):
            heavy, center = unit(heavy_phase), unit(center_phase)
            v = V.gm(center, unit(opening))
            w = V.gm(center, unit(-opening))
            require(all(V.gn(g) == 1 for g in (heavy, v, w)), 'Nonunit control phase')
            first, second = V.gs(v, 1+delta), V.gs(w, 1-delta)
            require(min(1+delta, 1-delta) >= 1/(1+b), 'Control radius floor failed')
            original = integral(b, heavy, first, second)
            equal = integral(b, heavy, v, w)
            difference = V.ga(original, V.gs(equal, -1))
            # Independently integrate the linear/quadratic radius difference.
            linear = V.gs(V.ga(v, V.gs(w, -1)), -b*delta)
            quadratic = V.gs(V.gm(v, w), -b*b*delta*delta)
            expected = F(0), F(0)
            for j in range(7):
                term = V.gs(V.gp(heavy, j), (-1)**j*comb(6, j)*b**j)
                for ell, coefficient in ((1, linear), (2, quadratic)):
                    expected = V.ga(expected, V.gs(V.gm(term, coefficient), F(9, j+ell+1)))
            require(difference == expected, 'Complete unequal-light integral difference failed')
            mean_original = (6*heavy[0]+first[0]+second[0])/8
            mean_equal = (6*heavy[0]+v[0]+w[0])/8
            require(mean_original-mean_equal == delta*(v[0]-w[0])/8,
                    'Actual-mean variance coefficient differs')
            require(abs(mean_original-mean_equal) <= abs(delta)/4, 'Mean-loss bound failed')
            require(V.gn(equal) <= maximum_norm**2
                    and V.gn(difference) <= light_lipschitz**2*delta**2,
                    'Integral norm/Lipschitz control failed')
            require((1-delta*delta)**2 <= 1, 'Unequal denominator comparison failed')
            records.append([str(b), str(delta), list(map(str, original)),
                            list(map(str, difference)), str(mean_original-mean_equal)])
    return {'points': len(records), 'sha256': V.digest(records)}


def derive(cases):
    n = 72
    # Degree elevation of (1-u)^2 versus the event "at least two failures".
    coefficients = [F(int(i <= n-2))-F(comb(n-i, 2), comb(n, 2))
                    for i in range(n+1)]
    require(all(value >= 0 for value in coefficients), 'Negative binomial tail coefficient')
    expected_power = {1: F(2), 2: F(-1), 71: F(-72), 72: F(71)}
    require(tail_power(coefficients) == expected_power, 'Complete tail basis identity differs')
    damaged = coefficients.copy()
    damaged[1] += 1
    require(tail_power(damaged) != expected_power, 'Altered tail coefficient accepted')
    rows, endpoint_floors = [], []
    for chart in ('nearer', 'farther'):
        record = cases['G6-'+chart]['certificate']
        require(record['negative'] == 0 and record['degrees'][0] == n
                and record['minimum_zero_b_index'] >= n-1,
                'G6 lacks the complete positive u-index0..70 slices')
        beta = F(record['minimum_positive'])
        clear = record['radius_clear']
        require(beta > 0 and clear >= 0, 'Invalid positive coefficient/scale')
        floor = beta*F(2)**(14-clear)/5**8
        endpoint_floors.append(floor)
        rows.append({'chart': chart, 'minimum_positive': str(beta),
                     'radius_clear': clear, 'normalized_endpoint_floor': str(floor)})
    alpha = min(F(1), *endpoint_floors)
    maximum_norm = 9*F(13, 6)**6*F(7, 2)**2
    light_lipschitz = 15*F(13, 6)**6
    derived_margin = alpha/(64*6400**4*maximum_norm**2)
    margin = F(1, 10**32)
    c0 = F(46643, 50000)
    # Original full light reciprocal-radius difference <= 10^-40(1-rho)^2.
    normalized_half_difference = F(1, 2*c0*10**40)
    require(derived_margin >= margin > 0, 'Rounded uniform origin margin fails')
    require(normalized_half_difference <= F(1, 128), 'Original polar mean gap insufficient')
    require(4*maximum_norm*light_lipschitz*normalized_half_difference <= margin,
            'Unequal-light perturbation exceeds half of the origin margin')
    return {'endpoint_records': rows, 'tail_degree': n, 'tail_signs': n+1,
            'full_tail_identity': True, 'damaged_tail_rejected': True,
            'tail_coefficients_sha256': hashlib.sha256(json.dumps(
                list(map(str, coefficients)), separators=(',', ':')).encode()).hexdigest(),
            'alpha': str(alpha), 'maximum_equal_integral': str(maximum_norm),
            'light_lipschitz': str(light_lipschitz), 'maximum_one_plus_k_squared': 6400,
            'derived_origin_margin': str(derived_margin),
            'rounded_origin_margin': str(margin),
            'original_full_light_radius_tube': '1/'+str(10**40),
            'normalized_half_difference_coefficient': str(normalized_half_difference),
            'polar_gap_denominator': 128,
            'unequal_integral_controls': unequal_controls(maximum_norm, light_lipschitz)}
