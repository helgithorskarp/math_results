"""Symbolic matrix identities and exact finite arithmetic for the cycle theorem."""
from pathlib import Path
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from exact import A as Field, matmul, matpower, require

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT/'hadwiger_nelson_cross_six_cycle/identities.py'
PIN = '2c0b7986b5da71c06f5d152a4c83c0c6196c2cdac3942cab6243f5da0541e370'
require(sha256(SOURCE.read_bytes()).hexdigest() == PIN, 'polynomial utility pin mismatch')
spec = importlib.util.spec_from_file_location('cycle_polynomials', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
P, variables = module.P, module.variables


def remainder(coefficients, trace):
    """Remainder modulo X^2-trace*X+1; ascending rational coefficients."""
    c = list(map(Q, coefficients))
    while len(c) > 2:
        v = c.pop()
        c[-1] += trace*v
        c[-2] -= v
    return c+[Q(0)]*(2-len(c))


def main():
    records = []

    def identity(name, left, right):
        require(not (P(left)-P(right)).terms, 'polynomial failure: '+name)
        text = json.dumps([(list(m), str(c)) for m, c in sorted(P(left).terms.items())],
                          separators=(',', ':'))
        records.append({'identity': name, 'left_terms': len(P(left).terms),
                        'left_sha256': sha256(text.encode()).hexdigest()})

    a, b, h, r, s = variables('A B H r s')
    d = a*b
    L = [[-d, 2*b*h], [-2*a*h, 4*h*h-d]]
    tr = 4*h*h-2*d
    identity('scaled_matrix_determinant', L[0][0]*L[1][1]-L[0][1]*L[1][0], d*d)
    identity('scaled_matrix_trace', L[0][0]+L[1][1], tr)
    square = matmul(L, L)
    for i in range(2):
        for j in range(2):
            identity(f'cayley_hamilton_{i}{j}', square[i][j]-tr*L[i][j],
                     -(d*d) if i == j else 0)
    rr, ss = L[0][0]*r+L[0][1]*s, L[1][0]*r+L[1][1]*s
    F = a*r*r+b*s*s-2*h*r*s
    identity('positive_form_preserved', a*rr*rr+b*ss*ss-2*h*rr*ss, d*d*F)
    other_r = 2*h*s-a*r
    identity('first_root_exchange', a*other_r*other_r+a*a*b*s*s-2*a*h*other_r*s, a*a*F)
    other_s = 2*h*r-b*s
    identity('second_root_exchange', b*b*a*r*r+b*other_s*other_s-2*b*h*r*other_s, b*b*F)

    divisors = [d for d in range(1, 133) if 132 % (d*d) == 0]
    require(divisors == [1, 2] and 33 > 16, 'quadratic trace denominator arithmetic')
    # With b=0, tau=m/2; boundedness and integral norm force m even.
    traces = [Q(m, 2) for m in range(-4, 5) if m*m % 4 == 0]
    require(traces == [-2, -1, 0, 1, 2], 'rational trace list')
    orders = []
    for t, n, poly in [(-1, 3, [-1, 0, 0, 1]), (0, 4, [1, 0, 1]),
                       (1, 6, [1, 0, 0, 1])]:
        rem = remainder(poly, t)
        require(rem == [0, 0], 'order-polynomial remainder')
        C = [[0, -1], [1, t]]
        require(matpower(C, n) == [[1, 0], [0, 1]]
                and all(matpower(C, j) != [[1, 0], [0, 1]] for j in range(1, n)),
                'companion order control')
        orders.append({'trace': t, 'order': n, 'cycle_length': 2*n,
                       'AB_over_H_squared': str(Q(4, t+2)), 'polynomial_remainder': list(map(str, rem))})

    require(1+3*Q(1)**2 == 4 and 1+3*Q(1, 3)**2 == Q(4, 3), 'angle field roots')
    residue_pairs = [(x, y) for x in range(2) for y in range(2) if (x, y) != (0, 0)]
    require(all((x*x-x*y+y*y) % 2 == 1 for x, y in residue_pairs), 'even norm-valuation seed')
    root2 = Field({2: 1})
    C = [[Field(0), Field(-1)], [Field(1), root2]]
    require(matpower(C, 4) == [[-1, 0], [0, -1]] and matpower(C, 8) == [[1, 0], [0, 1]],
            'larger real-field order-eight control')
    require(all(matpower(C, j) != [[1, 0], [0, 1]] for j in range(1, 8)), 'order is not eight')
    require(not root2.in_field() and root2.norm() == 2, 'norm-two extension control')
    output = {'polynomial_identities': records, 'identities_checked': len(records),
              'quadratic_coefficient_denominators': divisors, 'finite_order_trace_values': list(map(int, traces)),
              'remaining_order_cases': orders, 'nonzero_binary_norm_pairs': len(residue_pairs),
              'larger_real_field_order_eight_control': True, 'larger_field_has_norm_two': True,
              'uniform_cycle_claim_requires_PROOF_md': True}
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
