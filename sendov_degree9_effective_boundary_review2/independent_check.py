"""Independent exact evidence for six-reviewer-2's effective-annulus audit.

Python 3.11 standard library. Polynomial identities are checked by mixed
finite differences, rather than the target's sparse symbolic expansion.
No target contribution is imported; analytic implications are written proofs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import sys


def compositions(total, size=8):
    if size == 1:
        yield (total,)
        return
    for first in range(total+1):
        for rest in compositions(total-first, size-1):
            yield (first,)+rest


def elementary(values, degree=3):
    result = [1]+[0]*degree
    for x in values:
        for k in range(degree, 0, -1):
            result[k] += x*result[k-1]
    return result


def mixed_difference(fun, alpha):
    """Delta^alpha f(0); integer input and exact integer output."""
    total = 0
    for beta in product(*(range(a+1) for a in alpha)):
        weight = (-1)**(sum(alpha)-sum(beta))
        for a, b in zip(alpha, beta):
            weight *= comb(a, b)
        total += weight*fun(beta)
    return total


def newton_left(values, multiplier=21):
    _, e, L, M = elementary(values)
    return 12*L*L-multiplier*e*M


@lru_cache(maxsize=None)
def newton_right(values):
    result = 0
    for i, j in combinations(range(8), 2):
        outside = [values[k] for k in range(8) if k not in (i, j)]
        bracket = sum(x*x for x in outside)
        bracket += sum(x*y for x, y in combinations(outside, 2))
        result += (values[i]-values[j])**2*bracket
    return result


def newton_coefficients(multiplier=21):
    left = lru_cache(maxsize=None)(lambda v: newton_left(v, multiplier))
    coefficients = {}
    type_counts = {}
    for alpha in compositions(4):
        denominator = 1
        for a in alpha:
            denominator *= factorial(a)
        lhs = F(mixed_difference(left, alpha), denominator)
        rhs = F(mixed_difference(newton_right, alpha), denominator)
        pattern = tuple(sorted((a for a in alpha if a), reverse=True))
        expected = {(4,): 0, (3, 1): 0, (2, 2): 12,
                    (2, 1, 1): 3, (1, 1, 1, 1): -12}[pattern]
        if lhs != rhs or lhs != expected:
            raise ValueError('Newton identity coefficient mismatch')
        coefficients[alpha] = int(lhs)
        key = ','.join(map(str, pattern))
        type_counts[key] = type_counts.get(key, 0)+1
    return coefficients, type_counts


def polynomial_zero(fun, degree):
    """Full falling-factorial basis audit; degree bound is inspected in code."""
    cached = lru_cache(maxsize=None)(fun)
    count = 0
    for total in range(degree+1):
        for alpha in compositions(total):
            if mixed_difference(cached, alpha):
                raise ValueError('polynomial identity mismatch')
            count += 1
    return count


def real_symmetric_relation(ts):
    # Integral coordinates represent 2U_j=1+2it_j; no floating complex numbers.
    es = [(1, 0)]+[(0, 0)]*3
    for t in ts:
        for k in range(3, 0, -1):
            a, b = es[k-1]
            c, d = es[k]
            es[k] = (c+a-2*t*b, d+b+2*t*a)
    return es[3][0]-6*es[2][0]+112


def shifted_e2(xs):
    _, er, Lr = elementary([2*x+1 for x in xs], 2)
    Lx = elementary(xs, 2)[2]
    return Lr-7*er+28-4*Lx


def shifted_e3(xs):
    _, er, Lr, Mr = elementary([2*x+1 for x in xs])
    Mx = elementary(xs)[3]
    return Mr-6*Lr+21*er-56-8*Mx


def variance_identity(xs):
    _, e, L = elementary(xs, 2)
    return 8*sum(x*x for x in xs)-8*e*e+16*L


def add(a, b):
    out = [F(0)]*max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] += x
    for i, x in enumerate(b):
        out[i] += x
    return out


def multiply(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def power(a, n):
    out = [F(1)]
    for _ in range(n):
        out = multiply(out, a)
    return out


def require(condition, label):
    if not condition:
        raise ValueError(label)


def threshold(T):
    margins = (F(1, 16)-72*T, F(1, 14)-182*T)
    require(min(margins)>F(1, 20), 'local slope threshold')
    return margins


def rejected(fun):
    try:
        fun()
    except ValueError:
        return
    raise AssertionError('mutation accepted')


def certificate():
    coefficients, types = newton_coefficients()
    identity_counts = {
        'real_reciprocal_saturation': polynomial_zero(real_symmetric_relation, 3),
        'shifted_e2': polynomial_zero(shifted_e2, 2),
        'shifted_e3': polynomial_zero(shifted_e3, 3),
        'variance': polynomial_zero(variance_identity, 2),
    }
    rejected(lambda: newton_coefficients(22))
    rejected(lambda: polynomial_zero(lambda v: real_symmetric_relation(v)+1, 3))
    rejected(lambda: threshold(F(1, 1000)))

    h, eta, gamma = F(1, 100), F(1, 10**6), F(1, 160)
    cauchy = sum(F(comb(8, k), (k+1)*7**k) for k in range(1, 9))
    require(cauchy == F(41980912, 51883209) < 1, 'reciprocal Cauchy bound')
    require(64/F(99, 100)<65, 'negative real-root defect')
    require(8*65+8*65+F(1, 40)<1100, 'total projected defect')
    require(7*65+F(1, 40)<456, 'individual projected defect')
    require(1016/F(99, 100)<1030, 'real reciprocal lower bound')
    require((1030+F(1, 20))/8<140 and F(1030, 8)<130, 'angular and mean bounds')
    require((1+h)**8<2 and 16/(1-h)**2<17, 'polar pointwise bounds')
    # Direct exact integration of the complete finite binomial polynomial H.
    H = [F(0)]
    bmu = [F(0), F(2), 2*gamma-1, -gamma]
    for k in range(9):
        term = multiply(power([F(1), -F(1)], 8-k), power(bmu, k))
        H = add(H, [F(comb(8, k), k+1)*x for x in term])
    require(H[:3] == [F(1), F(0), F(16, 3)+8*gamma], 'integrated coefficients')
    tail = sum(abs(x)*h**(k-3) for k, x in enumerate(H) if k>=3)
    require(tail<128, 'uniform integrated remainder on [0,1/100]')
    vcap = (1+F(3, 2)*gamma+24*eta+37500*eta*eta)/(1-30*eta)
    require(vcap<F(5, 4), 'finite variance gap')
    projection2, projection3 = 7*9*1100, 21*81*1100
    phase2, phase3 = 2*7*5*1100, 3*21*25*1100
    saturation_error = 4*(projection3+3*projection2)+phase3+4*phase2+F(35, 4)*1100
    require(saturation_error == 10366125 < 11000000, 'saturation budget')
    Llow = F(7, 16)*(4-1100*eta)**2-5
    Lhigh = F(7, 16)*(4+eta/20)**2
    require(Llow>1 and Lhigh<8, 'saturation branch selection')
    require(F(7, 4)*1100*8+8*11000000<90000000, 'Newton loss bound')
    require(F(7, 64)*(F(2, 5)+eta/400)<1, 'variance mean correction')
    q_energy_coefficient = 8*(23000000+130**2*eta+280)
    require(q_energy_coefficient<190000000, 'reciprocal energy')
    require(16*eta+8*190000000<1600000000, 'critical energy')
    margins = threshold(F(1, 10000))
    require(F(8)-F(1, 20)>6, 'relaxed eta estimate')
    require(F(8, 3)+F(16, 3)*h<=3, 'eta <= 3T')
    require(F(3, 40)>F(1, 20), 'strict local contradiction')
    require(F(1600000000, 10**18)<F(1, 10000)**2, 'explicit annulus')

    # Constants in the abstract variance-gap lemma, uniformly on tau <= 1/100.
    require(F(7, 16)*(4+h)**2<8, 'abstract L upper bound')
    require(F(7, 4)*(4+h)<8, 'abstract saturation error coefficient')
    require(F(7, 64)*(8+h)<=1, 'abstract variance correction')
    require(4-F(7, 8)>=3, 'tau <= rho/4 gives L >= 3rho')
    table = [{'powers': list(k), 'coefficient': value}
             for k, value in sorted(coefficients.items())]
    coefficient_hash = hashlib.sha256(json.dumps(table, separators=(',', ':')).encode()).hexdigest()
    return {
        'reviewer': 'six-reviewer-2',
        'method': 'mixed finite differences and exact integrated binomial polynomial',
        'newton_degree_four_coefficients': len(coefficients),
        'newton_nonzero_coefficients': sum(v!=0 for v in coefficients.values()),
        'newton_monomial_type_counts': types,
        'newton_coefficient_table_sha256': coefficient_hash,
        'other_polynomial_basis_checks': identity_counts,
        'cauchy_radius_sum': str(cauchy),
        'integrated_remainder_bound_at_1_over_100': str(tail),
        'variance_cap_at_eta_1e_minus_6': str(vcap),
        'saturation_error_coefficient': str(saturation_error),
        'reciprocal_energy_coefficient': str(q_energy_coefficient),
        'local_slope_margins_at_T_1_over_10000': [str(m) for m in margins],
        'abstract_variance_gap_bound': 'v <= tau + (7*tau+4*epsilon)/(6*rho)',
        'rejected_mutations': 3,
    }


def main():
    encoded = json.dumps(certificate(), sort_keys=True, indent=2)+'\n'
    if sys.argv[1:] == ['--json']:
        print(encoded, end='')
        return
    if sys.argv[1:]:
        raise SystemExit('usage: independent_check.py [--json]')
    if encoded != Path(__file__).with_name('expected.json').read_text():
        raise SystemExit('certificate mismatch')
    print('PASS: 330 Newton coefficients; 420 other polynomial-basis checks; exact finite bounds; 3 mutations rejected.')
    print('certificate SHA256: '+hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == '__main__':
    main()
