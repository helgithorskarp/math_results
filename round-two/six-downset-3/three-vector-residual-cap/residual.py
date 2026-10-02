"""exact three-vector sufficient comparison, not a converse.

Uses the immutable published 9582 orbit forms.  Original row actions are
calibrated by calibrate_actions.py before any new boundary samples.
"""
from fractions import Fraction as F
from pathlib import Path
import sys

import input_pins
input_pins.check()
ROOT = Path(__file__).resolve().parents[3]
PARENT = Path(__file__).resolve().parent.parent / 'remaining-deletion-orders'
sys.path.insert(0, str(PARENT))
import orbits
import three_vectors
from exact import require, schur_psd, digest
from dual import negative_vector


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    require(len(a[0]) == len(b), 'matrix multiplication shape')
    return [[sum(x*y for x, y in zip(row, column))
             for column in zip(*b)] for row in a]


def inverse(a):
    n = len(a)
    b = [[F(x) for x in row]+[F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        require(pivot is not None, 'singular exact physical frame')
        b[j], b[pivot] = b[pivot], b[j]
        value = b[j][j]
        b[j] = [x/value for x in b[j]]
        for i in range(n):
            if i != j:
                value = b[i][j]
                b[i] = [x-value*y for x, y in zip(b[i], b[j])]
    result = [row[n:] for row in b]
    require(multiply(a, result) == [[F(i == j) for j in range(n)] for i in range(n)],
            'exact frame inverse residual')
    return result


def moments(data):
    # The original physical orbit basis has frame diag(orbit sizes).
    amplitudes = transpose(three_vectors.vectors(data))
    weights = data['sizes']
    weighted = [[weights[i]*x for x in row] for i, row in enumerate(amplitudes)]
    frame = multiply(transpose(amplitudes), weighted)
    hv = multiply(data['U0'], amplitudes)
    action = [[x/weights[i] for x in row] for i, row in enumerate(hv)]
    first = multiply(transpose(amplitudes), hv)
    second = multiply(transpose(action), hv)
    n, q, k = data['N']-1, data['q'], data['k']
    ell = 5*q+4-k
    require(frame == [[n, q, ell], [q, q, 0], [ell, 0, ell]],
            'physical three-vector frame formula')
    require(schur_psd(frame) == 3, 'positive physical frame')
    three_vectors.check(data)
    return {'frame': frame, 'first': first, 'second': second,
            'actions': action, 'amplitudes': amplitudes}


def compare(q, k):
    require(type(q) is int and type(k) is int and k >= 2 and q >= 3*k,
            'sufficient comparison domain k>=2,q>=3k')
    data = orbits.forms(q, k)
    values = moments(data)
    frame, a, second = (values[key] for key in ('frame', 'first', 'second'))
    inv = inverse(frame)
    projection = multiply(multiply(a, inv), a)
    residual = [[second[i][j]-projection[i][j] for j in range(3)] for i in range(3)]
    schur_psd(residual)
    g = F(data['N']-2*data['s'])
    require(g > 0, 'whole complement gap')
    sufficient = [[a[i][j]-residual[i][j]/g for j in range(3)] for i in range(3)]
    b2 = sum(multiply(inv, residual)[i][i] for i in range(3))
    require(b2 >= 0, 'physical cross norm bound')
    candidate = negative_vector(sufficient)
    record = {'q': q, 'k': k, 'N': data['N'], 'g': str(g),
              'frame': frame, 'first': a, 'second': second,
              'residual': residual, 'sufficient': sufficient, 'b2': b2,
              'three_vector_necessary_Q': three_vectors.scalars(q, k)['Q'],
              'comparison_status': 'failed sufficient comparison; no nonexistence inference'}
    if candidate is not None:
        record['failed_comparison_vector'] = candidate
        return record
    # A rational certified floor; absence at this bounded scale is inconclusive.
    for exponent in range(0, 41):
        delta = F(1, 1 << exponent)
        shifted = [[sufficient[i][j]-delta*frame[i][j] for j in range(3)] for i in range(3)]
        try:
            rank = schur_psd(shifted)
        except ValueError:
            continue
        mu = min(g/2, delta/(1+2*b2/(g*g)))
        kappa = min(F(1, 8), mu/(4*(16*data['s']+1)))
        trade = kappa/24
        require(mu > 0 and 16*data['s']*kappa+2*trade < mu/4,
                'whole quantitative upper perturbation')
        require(orbits.floor(data, kappa, trade, 3*mu/4) == 23,
                'finite exact entire invariant-space cap calibration')
        record.update({'comparison_status': 'strict sufficient comparison',
                       'delta': delta, 'shifted_rank': rank, 'mu': mu,
                       'kappa': kappa, 'trade': trade,
                       'nonempty_cap_floor': 3*mu/4})
        return record
    record['comparison_status'] = 'PSD comparison, bounded strict-floor search inconclusive'
    return record


def rational_point(q, k):
    """Explicit rational floor from 3x3 reciprocal trace, no bounded search."""
    data = orbits.forms(q, k)
    values = moments(data)
    d, a, second = (values[key] for key in ('frame', 'first', 'second'))
    dinv = inverse(d)
    removed = multiply(multiply(a, dinv), a)
    r = [[second[i][j]-removed[i][j] for j in range(3)] for i in range(3)]
    g = F(data['N']-2*data['s'])
    schur = [[a[i][j]-r[i][j]/g for j in range(3)] for i in range(3)]
    require(g > 0 and schur_psd(schur) == 3, 'strict sufficient physical comparison')
    trace = sum(multiply(inverse(schur), d)[i][i] for i in range(3))
    delta = 1/trace
    require(delta > 0 and schur_psd([[schur[i][j]-delta*d[i][j]
                                    for j in range(3)] for i in range(3)]) == 3,
            'rational reciprocal-trace physical floor')
    b2 = sum(multiply(dinv, r)[i][i] for i in range(3))
    require(b2 >= 0, 'nonnegative whole residual norm bound')
    mu = min(g/2, delta/(1+2*b2/(g*g)))
    kappa = min(F(1, 8), mu/(4*(16*data['s']+1)))
    trade = kappa/24
    require(orbits.floor(data, kappa, trade, 3*mu/4) == 23,
            'exact finite invariant cap check of new rational formula')
    return {'q':q,'k':k,'N':data['N'],'delta':delta,'mu':mu,
            'kappa':kappa,'trade':trade,'nonempty_cap_floor':3*mu/4,
            'projected_unit_gap':3*mu/(4*(data['N']-data['s']))}


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(x) for key, x in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(x) for x in value]
    return value
