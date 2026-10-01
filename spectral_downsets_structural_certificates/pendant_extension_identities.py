#!/usr/bin/env python3
"""Cleared rational identities and shifted sign certificates, not interpolation."""
from fractions import Fraction as F
from hashlib import sha256
import json
from strict_deletion_identities import R, variable


def certificates():
    n,b,z = [variable(i) for i in range(3)]
    a = 1-1/(n*b); beta = 1-1/b; chi = 1+n/b
    tau = 1+1/b; h = 1+1/n; q = 1-n/b
    checks = []
    def identity(name,lhs,rhs):
        if (lhs-rhs).a: raise ValueError('Rational clearing failed: '+name)
        checks.append(name)
    identity('alpha_numerator', n*b*a, n*b-1)
    identity('beta_numerator', b*beta, b-1)
    identity('chi_numerator', b*chi, b+n)
    identity('tau_numerator', b*tau, b+1)
    identity('h_numerator', n*h, n+1)
    identity('q_numerator', b*q, b-n)
    identity('old_B_diagonal', beta*n+chi, n+1)
    identity('old_S_row', n+1+a*b+h, n+b+2)
    identity('old_B_row', a*n+beta*b+chi+tau+q, n+b+2)
    identity('new_S_row', n+1+b*tau, n+b+2)
    identity('new_B_row', n*h+b*q+n+1, n+b+2)
    identity('old_B_new_star', a*n+tau, n+1)
    identity('standard_S_margin', n+1-a*n, 1+1/b)
    identity('standard_B_margin', chi+(beta-a)*b, 1/n+n/b)
    identity('negative_B_multiplier', beta-a, -(n-1)/(n*b))
    identity('constant_minor', n*n-1, (n-1)*(n+1))
    epsilon = 1/(2*(z+1))
    identity('mixture_upper_margin', (1-epsilon)-epsilon*z, R(F(1,2)))
    identity('empty_off_diagonal_margin', epsilon*(z+1), R(F(1,2)))
    # Independently counted deleted-edge quotient for one triangle plus pendants.
    p = variable(0); D = p*p+4*p+1
    g11 = 4*p/(p+1); g12 = -3*(p-1)/(p+1)
    g21 = -12/(p+1); g22 = 12/(p+1)
    identity('deleted_cross_cross_count', p+2-p+2*(p-1)/(p+1), g11)
    identity('deleted_cross_other_count', -(p-1)+(p-1)*(p-2)/(p+1), g12)
    identity('deleted_other_cross_count', -4+4*(p-2)/(p+1), g21)
    identity('deleted_other_other_count', p+2-2*(p-2)+(p-2)*(p-3)/(p+1), g22)
    identity('one_triangle_delta', 2*p+7-(p+3)*(p+2)/(p+1), D/(p+1))
    den = p**4+12*p**3+46*p*p+72*p+49
    identity('deleted_quotient_determinant', (D+4*p)*(D+12)-36*(p-1), den)
    u1 = (p+1)*(p+2)*(p+5); u2 = (p+1)*(p*p+8*p+13)
    identity('quotient_inverse_first', (D+4*p)*u1-3*(p-1)*u2, (p+1)*den)
    identity('quotient_inverse_second', -12*u1+(D+12)*u2, (p+1)*den)
    num = 2*p*(p+2)*(p+3)*(p+5)
    identity('weighted_inherited_scalar', p*(p+3)*den-D*(4*p*(p+2)*(p+5)+p*(p-1)*(p*p+8*p+13)), 2*num)
    identity('inherited_gap_numerator', num-den, p**4+8*p**3+16*p*p-12*p-49)

    U,V = variable(0),variable(1); nn=U+3; bb=nn+V
    raw = {
        'alpha_numerator': nn*bb-1, 'beta_numerator':bb-1,
        'chi_numerator':bb+nn, 'tau_numerator':bb+1,
        'h_numerator':nn+1, 'standard_B_margin_numerator':bb+nn*nn,
        'constant_minor':nn*nn-1, 'negative_multiplier_absolute_numerator':nn-1,
        'one_triangle_inherited_gap':(U+2)**4+8*(U+2)**3+16*(U+2)**2-12*(U+2)-49,
    }
    records={}
    for name,P in raw.items():
        if P.b != {(0,0,0):F(1)} or not P.a or not P.a.get((0,0,0)):
            raise ValueError('Polynomial or strict constant term missing')
        if any(c<=0 or c.denominator!=1 for c in P.a.values()):
            raise ValueError('Positive coefficient failed: '+name)
        records[name]=[[*e,int(c)] for e,c in sorted(P.a.items())]
    payload=dict(identities=checks,positive_coefficients=records,
                 q_nonnegative_numerator=[[0,1,0,1]],q_zero_allowed=True)
    payload['canonical_sha256']=sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return payload


if __name__=='__main__': print(json.dumps(certificates(),sort_keys=True,indent=2))
