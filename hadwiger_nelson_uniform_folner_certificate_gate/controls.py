"""Small tests of cancellation, exact bounds and malformed input rejection."""
from fractions import Fraction as F
from itertools import product
import verify


def expect_bad(action):
    try:
        action()
    except (ValueError, SyntaxError):
        return
    raise ValueError('malformed control was accepted')


def main():
    a, b, c = (0, 1), (2, 3), (4, 5)
    y, pairs = [F(2), F(2)], [(a, b), (b, c)]
    coefficients, classes, raw, norm = verify.fraction_coefficients(y, pairs)
    verify.require(raw == 4 and norm == 2 and coefficients[b] == 0, 'telescoping')
    # Direct finite maximization checks sharpness of the independent-range bound.
    mx = max(sum(coefficients[s] * value for s, value in zip([a, b, c], word))
             for word in product([F(0), F(1)], repeat=3))
    verify.require(mx == norm, 'range-bound extremizer')
    _, _, raw_cycle, norm_cycle = verify.fraction_coefficients(
        [F(1)] * 3, [(a, b), (b, c), (c, a)])
    verify.require(raw_cycle == 3 and norm_cycle == 0, 'closed cancellation cycle')
    co, _, _, single_norm = verify.fraction_coefficients([F(9)], [((0,), (1,))])
    verify.require(co == {} and single_norm == 0, 'singleton cancellation')
    # Brute-force the quadratic bound for small n, without using square roots.
    for n in range(1, 60):
        brute = max(m for m in range(n*n+1) if 2*m*m-n*m <= n*n*(n-1))
        verify.require(brute == verify.unit_edge_bound(n), 'edge-bound rounding')
    # On a path of M translation positions, the exact one-step defect is 1/M.
    for m in range(1, 20):
        r = set(range(m))
        verify.require(len({x+1 for x in r} - r) == 1, 'translation endpoint')
    expect_bad(lambda: verify.unit_edge_bound(0))
    expect_bad(lambda: verify.parse({'rational_dual.txt': b'1 0\n',
                                    'congruences.txt': b'0 [0,1] = [2,3]\n'}))
    expect_bad(lambda: verify.parse({'rational_dual.txt': b'1 2\n',
                                    'congruences.txt': b'0 [0,0] = [2,3]\n'}))
    expect_bad(lambda: verify.parse({'rational_dual.txt': b'1 2\n',
                                    'congruences.txt': b'0 [0,1] = [2,29]\n'}))
    expect_bad(lambda: verify.parse({'rational_dual.txt': b'1 2\n',
                                    'congruences.txt': b'0 [0] = [2,3]\n'}))
    expect_bad(lambda: verify.parse({'rational_dual.txt': b'1 2\n',
                                    'congruences.txt': b'garbage\n'}))
    print('PASS: cancellation, interval bound, edge rounding, translation, six malformed controls')


if __name__ == '__main__':
    main()
