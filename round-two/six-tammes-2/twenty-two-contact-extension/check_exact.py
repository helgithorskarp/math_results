"""Exact scalar and contact-incidence checks; no cover generation."""
from fractions import Fraction as Q
import argparse
import json
from binding import load


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    delta, _, _ = load(args.work)
    c = delta.c
    lower, upper, j_upper = c.LO, c.HI, Q(593,1000)
    def F(t):
        return 13*t**5-t**4+6*t**3+2*t**2-3*t-1
    derivative_lower = 65*lower**4-4*j_upper**3+18*lower**2+4*lower-3
    delta.r.require(F(lower)<0<F(upper) and upper<j_upper and derivative_lower>0,
                    'unique root in J and tau strictly below frozen upper endpoint')
    margin = 2*c.RHO**2-1
    delta.r.require(margin==Q(297449,500000)>j_upper,
                    'strict two-point cap obstruction exceeds all allowed t')
    edges = c.CONTACTS
    def contact(a,b):
        return tuple(sorted((a,b))) in edges
    h_patterns = [(0,9,5,11), (5,6,0,11), (7,11,0,5)]
    for a,b,u,v in h_patterns:
        delta.r.require(len({a,b,u,v})==4 and contact(u,v)
                        and all(contact(x,y) for x in (a,b) for y in (u,v)),
                        'h identity contact-incidence premise')
    k_patterns = [(0,(6,11,5,7)), (11,(6,0,5,9)), (5,(7,0,11,9))]
    for center,chain in k_patterns:
        delta.r.require(len(set(chain))==4 and center not in chain
                        and all(contact(center,j) for j in chain)
                        and all(contact(a,b) for a,b in zip(chain,chain[1:])),
                        'k identity contact-incidence premise')
    delta.r.require((6,8) not in edges and (9,13) not in edges and len(edges)==22,
                    'deleted contacts remain inequalities')
    print(json.dumps(dict(status='CHECKED_EXACT_SCALARS_AND_CONTACT_INCIDENCE',
                          derivative_lower=str(derivative_lower),
                          root_lower_sign=-1,root_upper_sign=1,
                          cap_pair_lower_bound=str(margin),contact_count=len(edges),
                          h_incidence_patterns=len(h_patterns),k_incidence_patterns=len(k_patterns),
                          complete_cover_claimed=False,independent_review=False),indent=2))


if __name__ == '__main__':
    main()
