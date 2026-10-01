"""Exact rational-function clearings and shifted polynomial sign records."""
from fractions import Fraction as F
from hashlib import sha256
import json
from strict_deletion_identities import R, variable


def certificates():
    n, b, z = [variable(i) for i in range(3)]
    alpha, beta = 1-1/(n*b), 1-1/b
    chi, tau, h, q = 1+n/b, 1+1/b, 1+1/n, 1-n/b
    identities = []

    def identity(name, lhs, rhs):
        if (lhs-rhs).a:
            raise ValueError('Cleared identity failed: '+name)
        identities.append(name)

    identity('alpha_clear', n*b*alpha, n*b-1)
    identity('beta_clear', b*beta, b-1)
    identity('new_B_diagonal', beta*n+chi, n+1)
    identity('old_S_row', n+1+alpha*b+h, n+b+2)
    identity('old_B_row', alpha*n+beta*b+chi+tau+q, n+b+2)
    identity('new_S_row', n+1+b*tau, n+b+2)
    identity('new_B_row', n*h+b*q+n+1, n+b+2)
    identity('old_B_new_star', alpha*n+tau, n+1)
    identity('history_B_diagonal', beta*(n+z)+chi, n+1+beta*z)
    identity('history_B_telescoping', (b-1)/(b+z-1)*(1-1/(b+z)), (b-1)/(b+z))
    identity('contrast_first_diagonal', (n+1)/(1+1/n), n)
    identity('contrast_second_diagonal', (n+1+(n/b-1))/(1+1/b), n)
    identity('contrast_norm_product', (1+1/n)*(1+1/b), (n+1)*(b+1)/(n*b))
    identity('cross_norm_square_gap', 2*n*b-(n+1)*(b+1), n*b-n-b-1)
    identity('contrast_half_margin', 2*b*(R(F(1, 2))-(n/b-1)), 3*b-2*n)
    # Here n,b are the original star/outside sizes and z=e_B.
    delta = z-n*(b-1)/2
    t0 = b*(n-1)-2*z
    identity('preliminary_pair_total', t0+2*delta, n-b)
    identity('preliminary_old_B_star', -1/b+1/b, R(0))
    identity('preliminary_spoke_star', -n+n, R(0))
    identity('preliminary_spoke_outside', b/b-1, R(0))
    identity('preliminary_singleton_star', R(1)-1, R(0))
    identity('preliminary_singleton_outside', n-(n-b)-b, R(0))
    identity('preliminary_old_S_row', z-1-z+1, R(0))
    identity('preliminary_old_B_outside', z+1-z-1, R(0))
    m = n+b
    identity('uniform_old_B_bound', 2*m*(n-1)+m*(b-1)+3, m*(2*n+b-3)+3)
    identity('uniform_singleton_bound', 3*b*(n-1)+b*(b-1)+m*(b-1)+m+2,
             2*b*(2*n+b-2)+2)
    identity('uniform_old_S_gap', 2*m*m+2-(2*m*(n-1)+4), 2*m*(b+1)-2)
    identity('uniform_old_B_gap', 2*m*m+2-(m*(2*n+b-3)+3), m*(b+3)-1)
    identity('uniform_singleton_gap', 2*m*m+2-(2*b*(2*n+b-2)+2), 2*n*n+4*b)
    eps = n/(2*(b+2))
    identity('repair_Schur_margin', 2/b-eps/(n-eps), 3*(b+2)/(b*(2*b+3)))
    identity('repair_lower_margin', n-eps, n*(2*b+3)/(2*(b+2)))
    # Here n is original N, b original s.
    p = 4*(n-1)*(n-1)+b+6
    identity('uniform_final_order', n+2*p, n+8*(n-1)*(n-1)+2*b+12)
    identity('pendant_density_gap', n+2*z-2*(b+z), n-2*b)

    U, V = variable(0), variable(1)
    nn, bb = U+3, U+2+V
    mm = nn+bb
    polynomials = {
        'alpha_positive': (nn*bb-1, True),
        'beta_positive': (bb-1, True),
        'cross_norm_nonnegative_gap': (nn*bb-nn-bb-1, False),
        'contrast_half_nonnegative_gap': (3*bb-2*nn, False),
        'contrast_final_lower_clear': (2*(3*nn-2)-5, True),
        'repair_positive_numerator': (3*(bb+2), True),
        'uniform_old_S_gap': (2*mm*(bb+1)-2, True),
        'uniform_old_B_gap': (mm*(bb+3)-1, True),
        'uniform_spoke_gap': (2*mm*mm-2*nn, True),
        'uniform_singleton_gap': (2*nn*nn+4*bb, True),
    }
    signs = {}
    for name, (P, strict) in polynomials.items():
        if P.b != {(0, 0, 0): F(1)} or not P.a:
            raise ValueError('Not a nonzero polynomial: '+name)
        if any(c < 0 or c.denominator != 1 for c in P.a.values()):
            raise ValueError('Coefficient sign failure: '+name)
        if strict and P.a.get((0, 0, 0), F(0)) <= 0:
            raise ValueError('Strict constant missing: '+name)
        signs[name] = dict(strict_constant_required=strict,
                          coefficients=[[*e, int(c)] for e, c in sorted(P.a.items())])
    payload = dict(agent='six-downset-1', role='researcher',
                   identities=identities, sign_certificates=signs,
                   domain='n=3+U,b=n-1+V,U,V>=0; repair n>0,b>=2')
    payload['canonical_sha256'] = sha256(json.dumps(payload, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()
    return payload


if __name__ == '__main__':
    print(json.dumps(certificates(), sort_keys=True, indent=2))
