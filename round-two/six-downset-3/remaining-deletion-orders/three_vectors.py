"""original three-vector necessary mechanism and exact coefficients."""
from fractions import Fraction as F
from pathlib import Path
import json
import orbits
from literal import require
from dual import congruence
from exact import digest
from algebra import add, mul, scale, constant, ONE, Q, K


def scalars(q, k):
    require(type(q) is int and type(k) is int and k >= 2 and q >= 3*k,
            'new quantified mechanism: integers k>=2,q>=3k')
    N, s = (q*q+13*q+16)//2-k, 3*q+4
    gap, h, ell = N-s, F(1, 3*q+5), 5*q+4-k
    e = F(q*q+(13-6*k)*q+2*k*k-10*k+14, 2)
    A = F((2*k+1)*q+k)-F(2*k, q)
    C = F(ell*(1-k))
    T = F(q*gap)
    B = -(q-k)*s-k*(3+F(2, q))
    V = F(ell*gap-4*q*s)
    determinant = T*V-B*B
    require(T > 0 and V > 0 and determinant > 0, 'exact strictly positive two-vector block')
    a, b = (V*A-B*C)/determinant, (T*C-B*A)/determinant
    S = F(q*(q+1), 2)+3*(q+1)*h-2*k*h
    pairing, derivative = e-a*A-b*C, S-2*h*(a*q+b*(2*q-k))
    require(derivative > 0, 'new universal affine orientation')
    return {'q': q, 'k': k, 'e': e, 'A': A, 'C': C, 'T': T, 'B': B, 'V': V,
            'determinant': determinant, 'a': a, 'b': b, 'Q': pairing, 'Delta': derivative,
            'S': S, 'h': h}


def vectors(data):
    return [[F(1)]*23,
            [F(c == 1 and z+w == 1) for c, z, w in data['keys']],
            [F(bool(c & 6) and not(c in (3, 5) and z+w == 0)) for c, z, w in data['keys']]]


def check(data):
    v = scalars(data['q'], data['k'])
    columns = vectors(data)
    require(congruence(data['U0'], columns) == [[v['e'], v['A'], v['C']],
                                              [v['A'], v['T'], v['B']],
                                              [v['C'], v['B'], v['V']]], 'every three-vector original upper Gram entry')
    q, k, h = v['q'], v['k'], v['h']
    require(congruence(data['Delta'], columns) == [[v['S'], q*h, (2*q-k)*h],
                                                 [q*h, 0, 0], [(2*q-k)*h, 0, 0]],
            'every three-vector original slope entry')
    require(not any(x for row in congruence(data['R'], columns) for x in row),
            'entire three-vector space annihilates repair quadratic')
    return {key: str(value) if isinstance(value, F) else value for key, value in v.items()}


def polynomial_forms(q, k):
    """Cleared denominators; these are identities, not fitted samples."""
    g2 = add(mul(q, q), scale(q, 7), constant(8), scale(k, -2))
    s = add(scale(q, 3), constant(4))
    ell = add(scale(q, 5), constant(4), scale(k, -1))
    aq = add(mul(add(scale(k, 2), ONE), mul(q, q)), mul(k, q), scale(k, -2))
    c = mul(ell, add(ONE, scale(k, -1)))
    t2 = mul(q, g2)
    v2 = add(mul(ell, g2), scale(mul(q, s), -8))
    bq = add(mul(q, add(mul(add(q, scale(k, -1)), s), scale(k, 3))), scale(k, 2))
    det = add(mul(mul(q, q), mul(t2, v2)), scale(mul(bq, bq), -4))
    an = scale(mul(q, add(mul(v2, aq), scale(mul(bq, c), 2))), 2)
    bn = scale(add(mul(mul(q, q), mul(t2, c)), scale(mul(bq, aq), 2)), 2)
    s2 = add(mul(mul(q, add(q, ONE)), add(scale(q, 3), constant(5))),
             scale(add(q, ONE), 6), scale(k, -4))
    derivative = add(mul(s2, det), scale(add(mul(an, q), mul(bn, add(scale(q, 2), scale(k, -1)))), -4))
    return {'V2': v2, 'det_num': det, 'Delta_num': derivative, 'a_num': an, 'b_num': bn}


def run():
    # q=3k+u, k=2+x, hence x,u>=0 covers the WHOLE quantified quadrant.
    shifted = polynomial_forms(add(scale(K, 3), Q, constant(6)), add(K, constant(2)))
    certificate = {}
    for name in ('V2', 'det_num', 'Delta_num'):
        coefficients = shifted[name]
        require(coefficients.get((0, 0), F(0)) > 0 and all(x >= 0 for x in coefficients.values()),
                'entire shifted coefficient positivity: '+name)
        certificate[name] = {'coefficients': [[list(p), str(x)] for p, x in sorted(coefficients.items())],
                             'count': len(coefficients), 'digest': digest([[list(p), str(x)] for p, x in sorted(coefficients.items())])}
    calibration = []
    for q, k in ((19, 5), (24, 6), (74, 15)):
        v = scalars(q, k)
        normal = polynomial_forms({(0, 0): F(q)}, {(0, 0): F(k)})
        value = lambda name: normal[name].get((0, 0), F(0))
        require(value('V2') == 2*v['V'] and value('det_num') == 4*q*q*v['determinant']
                and value('a_num') == value('det_num')*v['a']
                and value('b_num') == value('det_num')*v['b']
                and value('Delta_num') == 2*(3*q+5)*value('det_num')*v['Delta'],
                'cleared denominators exact scalar calibration')
        calibration.append(check(orbits.forms(q, k)))
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'new universal necessary mechanism; written original counting bridge required',
              'scope': 'ALL integers k>=2,q>=3k; Q<0 excludes ALL REAL kappa,t in the ansatz',
              'certificates': certificate, 'exact_calibrations': calibration,
              'polynomial_coverage': 'every coefficient after exact q=3k+u,k=2+x substitution; finite values are calibration only'}
    result['record_sha256'] = digest(result)
    return result


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('THREE-VECTOR.json').write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'digest': result['record_sha256'], 'positive_coefficient_counts':
                      {name: value['count'] for name, value in result['certificates'].items()},
                      'calibrations': result['exact_calibrations']}, indent=2))
