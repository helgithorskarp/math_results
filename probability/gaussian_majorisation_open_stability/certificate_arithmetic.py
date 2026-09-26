#!/usr/bin/env python3
"""Exact arithmetic consumer for CERTIFICATE_INTERFACE.md.

Inputs must already enclose the stated normalized Gaussian quantities.
The --check command audits arithmetic only; it proves no unknown Gaussian pair.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from math import comb
from pathlib import Path


def rational(value):
    if type(value) not in (int, str, Fraction):
        raise TypeError('Use exact integers, rational strings or Fraction; no floats')
    return Fraction(value)


def degree(n):
    if type(n) is not int or n < 0:
        raise ValueError('Degree must be a nonnegative integer')
    return n


@dataclass(frozen=True)
class Interval:
    lo: Fraction
    hi: Fraction

    def __post_init__(self):
        object.__setattr__(self, 'lo', rational(self.lo))
        object.__setattr__(self, 'hi', rational(self.hi))
        if self.lo > self.hi:
            raise ValueError('Reversed interval')

    @staticmethod
    def point(x):
        return Interval(x, x)

    def plus(self, other):
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def scale(self, c):
        c = rational(c)
        a, b = c*self.lo, c*self.hi
        return Interval(min(a, b), max(a, b))


def hinge_moment(m, source_power, target_power):
    """Return a_(m-2) from intervals for A_m(f), A_m(g), not raw powers."""
    if type(m) is not int or m < 2:
        raise ValueError('Power must be an integer at least two')
    return target_power.plus(source_power.scale(-1)).scale(Fraction(1, m*(m-1)))


def beta_interval(n, k, hinge_moments):
    """Signed interval evaluation of I2; caller supplies a_0,...,a_n."""
    degree(n)
    if type(k) is not int or not 0 <= k <= n:
        raise ValueError('Beta index outside degree')
    if len(hinge_moments) < n+1:
        raise ValueError('Incomplete hinge-moment list')
    total = Interval.point(0)
    for ell in range(n-k+1):
        c = (n+1)*comb(n, k)*(-1)**ell*comb(n-k, ell)
        total = total.plus(hinge_moments[k+ell].scale(c))
    return total


def selected_indices(n, tau, cutoff):
    degree(n)
    tau, cutoff = rational(tau), rational(cutoff)
    if not 0 < tau < cutoff < 1:
        raise ValueError('Need 0 < tau < cutoff < 1')
    low = (n+2)*tau - 2
    high = (n+2)*cutoff
    start = max(0, -((-low.numerator)//low.denominator))
    stop = min(n, high.numerator//high.denominator)
    return tuple(range(start, stop+1))


def beta_tail_bound(n, k, lower_cut):
    """Return exact mean, variance and Cantelli upper bound for P(V<d)."""
    degree(n)
    if type(k) is not int or not 0 <= k <= n:
        raise ValueError('Beta index outside degree')
    d = rational(lower_cut)
    if not 0 < d < 1:
        raise ValueError('Need 0 < lower_cut < 1')
    t = Fraction(k+1, n+2)
    v = t*(1-t)/(n+3)
    p = Fraction(1) if t <= d else v/(v+(t-d)**2)
    return t, v, p


def universal_local_constant(lower_cut):
    """The mass-one layer-cake bound K=1/d; no support enclosure required."""
    d = rational(lower_cut)
    if not 0 < d < 1:
        raise ValueError('Need 0 < lower_cut < 1')
    return 1/d


def holder_pass(n, beta_lower, holder_constant, transport_error=0):
    degree(n)
    low = rational(beta_lower)-rational(transport_error)
    L, eta = rational(holder_constant), rational(transport_error)
    if L < 0 or eta < 0:
        raise ValueError('Constants and error budgets must be nonnegative')
    d2 = Fraction(1, 4*(n+3))+Fraction(1, (n+2)**2)
    return low > 0 and low**4 > L**4*d2


def local_pass(n, k, beta_lower, lipschitz_constant, lower_cut, transport_error=0):
    K = (universal_local_constant(lower_cut) if lipschitz_constant is None
         else rational(lipschitz_constant))
    eta = rational(transport_error)
    if K < 0 or eta < 0:
        raise ValueError('Constants and error budgets must be nonnegative')
    _, v, p = beta_tail_bound(n, k, lower_cut)
    residual = rational(beta_lower)-eta-p
    return residual > 0 and residual**2 > K**2*(v+Fraction(1, (n+2)**2))


def source_peak_pass(m, absolute_moment_upper, cutoff):
    """Check I5. Requires a proved upper bound on A_m(f), not a difference."""
    if type(m) is not int or m < 2:
        raise ValueError('Power must be an integer at least two')
    upper, b = rational(absolute_moment_upper), rational(cutoff)
    if upper < 0 or not 0 < b <= 1:
        raise ValueError('Invalid peak inputs')
    return m**3*upper**2 <= b**(2*m)


def grid_arithmetic(n, tau, cutoff, lower_cut, lipschitz_constant,
                    beta_lowers, transport_error=0, holder_constant=None):
    """Check all selected strict margins, not the external analytic premises.

    beta_lowers is a mapping k -> rigorous reference lower bound. Missing
    selected indices raise; a failed margin is inconclusive for majorisation.
    """
    tau, d = rational(tau), rational(lower_cut)
    if not 0 < d < tau:
        raise ValueError('Need 0 < lower_cut < tau')
    if lipschitz_constant is None:
        lipschitz_constant = universal_local_constant(d)
    if rational(lipschitz_constant) < 0 or rational(transport_error) < 0:
        raise ValueError('Constants and error budgets must be nonnegative')
    if holder_constant is not None and rational(holder_constant) < 0:
        raise ValueError('Holder constant must be nonnegative')
    indices = selected_indices(n, tau, cutoff)
    if any(k not in beta_lowers for k in indices):
        raise ValueError('Missing selected beta index')
    local, old, failed = [], [], []
    for k in indices:
        if local_pass(n, k, beta_lowers[k], lipschitz_constant, d, transport_error):
            local.append(k)
        elif holder_constant is not None and holder_pass(
                n, beta_lowers[k], holder_constant, transport_error):
            old.append(k)
        else:
            failed.append(k)
    return {'arithmetic_pass': not failed, 'selected_count': len(indices),
            'local_indices': local, 'holder_indices': old, 'failed_indices': failed,
            'analytic_premises_verified': False}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rejects(operation):
    try:
        operation()
    except (ValueError, TypeError):
        return True
    return False


def polynomial_beta(coefficients, n, k):
    # Independent rising-factorial beta moments, without signed differences.
    result, rising = Fraction(0), Fraction(1)
    for power, coefficient in enumerate(coefficients):
        if power:
            rising *= Fraction(k+power, n+power+1)
        result += coefficient*rising
    return result


def audit():
    count_beta = 0
    for coefficients in ((0, 1, -1), (0, Fraction(-1, 2), Fraction(3, 2), -1)):
        for n in range(13):
            moments = [Interval.point(sum(Fraction(c, j+power+1)
                        for power, c in enumerate(coefficients))) for j in range(n+1)]
            for k in range(n+1):
                observed = beta_interval(n, k, moments)
                expected = polynomial_beta(coefficients, n, k)
                require(observed == Interval.point(expected), 'Beta normalization mismatch')
                count_beta += 1
    normalization = hinge_moment(3, Interval.point(Fraction(1, 4)),
                                 Interval.point(Fraction(1, 2)))
    require(normalization == Interval.point(Fraction(1, 24)), 'Power normalization mismatch')

    count_vertices = 0
    for n in range(5):
        intervals = [Interval(Fraction(j-2, 20), Fraction(j+3, 20)) for j in range(n+1)]
        for k in range(n+1):
            result = beta_interval(n, k, intervals)
            values = []
            for vertex in product(*[(a.lo, a.hi) for a in intervals]):
                value = sum((n+1)*comb(n,k)*(-1)**ell*comb(n-k,ell)*vertex[k+ell]
                            for ell in range(n-k+1))
                values.append(value)
                count_vertices += 1
            require(result == Interval(min(values), max(values)), 'Signed interval extremum mismatch')

    count_tails = 0
    for n in range(13):
        for k in range(n+1):
            for d in (Fraction(1,16), Fraction(1,4), Fraction(1,2)):
                exact = sum(Fraction(comb(n+1,j))*d**j*(1-d)**(n+1-j)
                            for j in range(k+1,n+2))
                _, _, bound = beta_tail_bound(n,k,d)
                require(0 <= exact <= bound <= 1, 'Cantelli does not enclose beta tail')
                count_tails += 1

    count_selections = 0
    for n in range(33):
        for tau, cutoff in ((Fraction(1,4),Fraction(3,4)),
                            (Fraction(1,100),Fraction(9,10)),
                            (Fraction(4,9),Fraction(5,9))):
            expected = tuple(k for k in range(n+1) if
                         tau-Fraction(1,n+2) <= Fraction(k+1,n+2) <= cutoff+Fraction(1,n+2))
            require(selected_indices(n,tau,cutoff) == expected, 'Selected index mismatch')
            require(bool(expected), 'Selected set unexpectedly empty')
            count_selections += 1

    # H(u)=u(1-u) is a polynomial arithmetic control, not a Gaussian claim.
    n, tau, cutoff, d = 64, Fraction(1,4), Fraction(3,4), Fraction(1,16)
    beta = {k: Fraction((k+1)*(n-k+1),(n+2)*(n+3)) for k in range(n+1)}
    toy = grid_arithmetic(n,tau,cutoff,d,1,beta)
    transported = grid_arithmetic(n,tau,cutoff,d,1,beta, Fraction(1,100))
    old_count = sum(holder_pass(n,beta[k],1) for k in selected_indices(n,tau,cutoff))
    require(universal_local_constant(d) == 16, 'Universal mass modulus mismatch')
    for k in selected_indices(n,tau,cutoff):
        require(local_pass(n,k,beta[k],None,d) == local_pass(n,k,beta[k],16,d),
                'Automatic modulus differs from explicit mass bound')
    require(toy['arithmetic_pass'] and transported['arithmetic_pass'], 'Polynomial control failed')
    require(old_count == 0, 'Expected Holder/local contrast changed')
    corrupted = dict(beta)
    corrupted[toy['local_indices'][0]] = Fraction(0)
    require(not grid_arithmetic(n,tau,cutoff,d,1,corrupted)['arithmetic_pass'],
            'Bad beta sign was accepted')
    missing = dict(beta)
    del missing[toy['local_indices'][0]]
    require(rejects(lambda: grid_arithmetic(n,tau,cutoff,d,1,missing)), 'Missing beta accepted')
    _, _, p = beta_tail_bound(1,0,Fraction(1,16))
    require(not local_pass(1,0,p,0,Fraction(1,16)), 'Strict local boundary accepted')
    require(not holder_pass(1,0,0), 'Strict Holder boundary accepted')

    replica = sum(Fraction(comb(4,j), 16*2**(j*(4-j))) for j in range(5))
    require(replica == Fraction(27,128), 'Gaussian replica control mismatch')
    direct = Fraction(0)
    for sites in product((-1,1), repeat=4):
        squared_sum = sum((sites[a]-sites[b])**2 for a in range(4) for b in range(a+1,4))
        require(squared_sum % 4 == 0, 'Replica exponent is not integral')
        direct += Fraction(1, 16*2**(squared_sum//4))
    require(direct == replica, 'Direct tuple replica normalization mismatch')
    absolute_moment = replica/8
    require(source_peak_pass(4,absolute_moment,Fraction(7,10)), 'Gaussian peak cap failed')
    require(not source_peak_pass(4,absolute_moment,Fraction(2,3)), 'Insufficient cap accepted')
    bad_inputs = (
        lambda: Interval(1,0), lambda: Interval(0.1,1),
        lambda: selected_indices(-1,tau,cutoff),
        lambda: selected_indices(2,tau,tau),
        lambda: hinge_moment(1,Interval.point(0),Interval.point(0)),
        lambda: beta_interval(2,3,[Interval.point(0)]*3),
        lambda: beta_interval(2,0,[Interval.point(0)]*2),
        lambda: beta_tail_bound(2,0,0),
        lambda: source_peak_pass(4,-1,Fraction(7,10)),
        lambda: local_pass(2,0,1,-1,d),
        lambda: holder_pass(2,1,1,-1),
        lambda: grid_arithmetic(n,tau,cutoff,tau,1,beta))
    require(all(rejects(operation) for operation in bad_inputs), 'Malformed input accepted')
    return {'schema':'gaussian-certificate-interface-audit-v1',
        'arithmetic_only':True, 'unknown_gaussian_comparison_certified':False,
        'beta_identity_cases':count_beta, 'interval_vertices_checked':count_vertices,
        'exact_beta_tail_controls':count_tails, 'selected_index_controls':count_selections,
        'normalization_a1':'1/24',
        'universal_mass_modulus':'16 at d=1/16',
        'automatic_modulus_controls':toy['selected_count'],
        'polynomial_control':{'hinge':'u(1-u); not asserted Gaussian', 'degree':n,
            'selected_count':toy['selected_count'], 'local_pass':toy['arithmetic_pass'],
            'holder_passing_indices':old_count,'transport_budget':'1/100',
            'transported_local_pass':transported['arithmetic_pass']},
        'gaussian_peak_control':{'law':'(delta_-e1+delta_e1)/2','variance':'1/(2 log 2)',
            'power':4,'direct_replica_tuples':16,'replica':'27/128','absolute_normalized_moment':'27/1024',
            'certified_peak_cap':'7/10','insufficient_fourth_moment_cap':'2/3'},
        'corrupted_beta_rejected':True,'missing_index_rejected':True,
        'strict_boundary_controls':2,'malformed_input_controls':len(bad_inputs),
        'analytic_premises_verified':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    result = audit()
    raw = (json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    path = Path(__file__).with_name('INTERFACE_EXPECTED.json')
    if args.write_expected:
        path.write_bytes(raw)
    else:
        require(path.read_bytes() == raw, 'Expected audit record differs')
    print('FINITE_CERTIFICATE_INTERFACE_ARITHMETIC_PASS '+sha256(raw).hexdigest())


if __name__ == '__main__':
    main()
