#!/usr/bin/env python3
"""Exact transport of h4071's Cayley representatives to our physical graphs."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import hashlib
import json
from verify import CASES, lin, need

SOURCE = Path(__file__).resolve().parent.parent/'hadwiger_nelson_three_wheel_symmetry_frontier'/'certificate.json'
EXPECTED_SHA = '14e2a5e3fc00af36d4ef57b6a8fdd964450633b0ab76f0f2783094172ec69132'


def run():
    data = SOURCE.read_bytes()
    need(hashlib.sha256(data).hexdigest() == EXPECTED_SHA, 'h4071 certificate hash')
    reps = json.loads(data)['collision_orbit_representatives']
    need(len(reps) == len(CASES), 'four h4071 representatives')
    results = []
    for case, rep in zip(CASES, reps):
        norms, delta, q, U, V = case
        need(rep['squared_norms'] == list(norms), 'norm type transport')
        r = rep['radicand']
        k = isqrt(3*delta//r)
        need(k > 0 and r > 0 and k*k*r == 3*delta, 'positive square-root transport')
        # st=-sqrt(3*delta)=-k*sqrt(r), so x=a+b*sqrt(r)=a-(b/k)st.
        for coeffs, z in ((rep['x_coefficients'], U), (rep['y_coefficients'], V)):
            need(len(coeffs) == 2, 'quadratic coordinate')
            a, b = map(F, coeffs)
            d = -b/k
            sz = lin(z, 0, 1)
            tz = (-delta*z[2], -delta*z[3], z[0], z[1])
            left = tuple(z[i]-a*sz[i]+3*d*tz[i] for i in range(4))
            right = (q, q*a, -3*q*d, 0)
            need(left == right, 'exact Cayley rotation identity')
        results.append({'norms': list(norms), 'exact_rotation_identities': 2})
    return {'status': 'H4071_REPRESENTATIVES_MATCH_PHYSICAL_COLOUR_CERTIFICATES',
            'source_certificate_sha256': EXPECTED_SHA, 'cases': results,
            'remaining_physical_classes_using_h4071': 5110,
            'remaining_factor_pair_representatives': 800,
            'solver_calls': 0, 'CAS_calls': 0}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
