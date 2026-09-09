#!/usr/bin/env python3
"""Boundary and corruption controls for the proof kernel, standard library only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from copy import deepcopy
import json
import arithmetic as A
from norm_check import NormBlock
from verify import projection_check
import inputs

HERE = Path(__file__).resolve().parent


def vector(p):
    return [p.get((i, j), 0) for i in range(3) for j in range(3)]


def rejects(name, function, results):
    try:
        function()
    except (ValueError, IndexError, KeyError):
        results.append(name)
    else:
        raise RuntimeError('accepted corruption: '+name)


def run():
    tests = []; rejected = []
    A.need(A.primitive((-4,)) == (1,), 'negative constant normalization')
    f = vector({(1, 1): 1, (0, 0): 1}); g = vector({(1, 1): 1, (0, 0): 2})
    A.need(A.resultant_y(f, g) == (0, 1), 'leading degree loss resultant')
    A.need(A.Quotient((0, 1)).y_gcd(f, g) == ((1,),), 'extraneous projection root is empty')
    tests.append('leading-coefficient degree loss and empty fibre')
    f = vector({(1, 0): 1, (0, 1): -2, (0, 0): -1})
    g = vector({(1, 0): 1, (0, 1): -2, (0, 0): 1})
    A.need(A.resultant_y(f, g) == (1,), 'negative constant Sylvester determinant')
    tests.append('negative constant resultant, including source system 770')
    f = vector({(1, 0): 1}); g = vector({(1, 0): 1, (0, 0): -1})
    A.need(A.resultant_y(f, g) == (1,), 'coprime univariate system')
    rejects('common univariate factor', lambda: A.resultant_y(f, f), rejected)
    rejects('nonunit quotient coefficient', lambda: A.Quotient((-1, 0, 1)).inverse((-1, 1)), rejected)
    rejects('vertical common component', lambda: A.Quotient((0, 1)).y_gcd(vector({(1, 1): 1}), vector({(1, 1): 1, (1, 0): 1})), rejected)

    # Compare two different unit algorithms on linear, quadratic, reducible,
    # and nonreduced quotients, with an exhaustive small event-polynomial grid.
    fixtures = [
        ((-2, 0, 1), ((0, -1), (1,))),
        ((-2, 0, 1), ((0, -1), (), (1,))),
        ((1, -2, 1), ((), (), (1,))),
        ((-1, 0, 1), ((1,), (1,))),
    ]
    compared = 0
    for r, h in fixtures:
        Q = A.Quotient(r)
        matrix, norm = A.ModBlock(Q.r, h, 1009), NormBlock(Q.r, h, 1009)
        for c, x, y, xy, yy in product((-1, 0, 1), repeat=5):
            p = vector({(0, 0): c, (1, 0): x, (0, 1): y, (1, 1): xy, (0, 2): yy})
            A.need(matrix.unit(p) == norm.unit(p), 'matrix/norm control comparison')
            compared += 1
    tests.append('972 entry-level matrix/norm comparisons, including nilpotents')
    h = ((0, -1), (1,)); r = (-2, 0, 1)
    for p in (1009, 1013):
        norm = NormBlock(A.Quotient(r).r, h, p)
        A.need(norm.unit(vector({(0, 0): 1009})) == (p != 1009), 'bad-prime false edge control')
        A.need(not norm.unit(vector({(0, 1): 1, (1, 0): -1})), 'zero quotient element not unit')
    tests.append('bad prime resolved by second modulus; zero relation rejected')
    rejects('bad rational denominator', lambda: NormBlock((F(1, 1009), F(1)), ((0,), (1,)), 1009), rejected)
    rejects('undeclared or composite modulus', lambda: NormBlock((-2, 0, 1), h, 1000), rejected)

    cert = json.loads((HERE/'certificate.json').read_text())
    source = json.loads((inputs.SOURCE/'certificate.json').read_text())
    symmetry = json.loads((inputs.SYMMETRY/'certificate.json').read_text())
    a, b = symmetry['pair_orbit_representatives'][0]
    rfactors = [tuple(r) for r in cert['rfactors']]
    row = [{'r': r, 'multiplicity': m} for r, m, action in cert['systems'][0]]
    projection_check(source['factors'][a], source['factors'][b], row, rfactors)
    rejects('missing projection factor', lambda: projection_check(source['factors'][a], source['factors'][b], row[1:], rfactors), rejected)
    corrupt = deepcopy(rfactors); r = row[0]['r']; z = list(corrupt[r]); z[0] += 1; corrupt[r] = tuple(z)
    rejects('wrong projection coefficient', lambda: projection_check(source['factors'][a], source['factors'][b], row, corrupt), rejected)
    Q = A.Quotient((4, -9, 3))
    h1, h2 = ((1, -1), (1,)), ((-1, 2), (1,))
    expected = ((F(5, 3), F(-3)), (F(0), F(1)), (F(1),))
    A.need(Q.y_mul(h1, h2) == expected and h1 != expected, 'nontrivial complete split')
    tests.append('last quadratic envelope split identity')
    # A constant word fails on actual Cartesian unit edges, independently of
    # any quotient or solver encoding.
    rejects('monochromatic Cartesian edge', lambda: inputs.bad_factors('0'*343, set(), [(0, 1)], []), rejected)
    rejects('truncated colour word', lambda: inputs.bad_factors('0'*342, set(), [], []), rejected)
    return {'status': 'CONTROLS_PASSED', 'boundary_controls': tests,
            'matrix_norm_comparisons': compared, 'rejected_corruptions': rejected,
            'solver_calls': 0, 'CAS_calls': 0}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
