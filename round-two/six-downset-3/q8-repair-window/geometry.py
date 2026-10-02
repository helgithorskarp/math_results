"""Exact real repair window from complete physical Schur blocks."""
from fractions import Fraction as F
from math import gcd,lcm,isqrt
import json,sys
import inputs
from claims import POLY
from literal import require

def window(lower,upper):
    ue,uo,le,lo=[[[F(x) for x in row] for row in block] for block in upper['even_odd_blocks']+lower['even_odd_blocks']]
    a,b,c=ue[0][0],ue[0][1],ue[1][1]
    require(a>0 and c>0 and b<0 and b*b>a*c,'even original upper condition')
    coeff=[4,4*b,b*b-a*c];den=lcm(*(x.denominator if isinstance(x,F) else 1 for x in coeff));ints=[int(x*den) for x in coeff]
    g=gcd(*ints);ints=[x//g for x in ints];A,B,C=ints
    require(tuple(ints)==POLY,'declared polynomial differs from original physical forms')
    D=B*B-4*A*C;root=isqrt(D)
    require(A>0 and B<0 and C>0 and D>0 and root*root<D<(root+1)**2,'irrational positive real endpoints')
    def poly(t):return A*t*t+B*t+C
    # Simple exact rational ordering, no decimal/floating point premise.
    require(poly(F(1,4))>0 and poly(F(3,8))<0 and poly(F(6))<0 and poly(F(8))>0,
            'two separated exact endpoint isolators')
    vertex=F(-B,2*A);require(F(3,8)<vertex<6,'unique ordered root positions')
    m=le[0][0];mp=lo[0][0]
    require(le==[[m,m],[m,m]] and lo==[[mp,-mp],[-mp,mp]],'lower scalar forms')
    require(8<min(m,mp),'lower window contains complete upper window')
    ao,bo,co=uo[0][0],uo[0][1],uo[1][1]
    require(ao==co>0 and ao>abs(bo) and ao>abs(bo-16),'odd upper PD on entire [0,8]')
    # Convexity of |bo-2t| gives odd positive throughout this enclosure.
    return {'q':8,'k':3,'kappa':'0','N':89,'primitive_cap_polynomial':ints,'discriminant':D,
            'irrational_endpoint_formula':'(-B +/- sqrt(D))/(2A)',
            'lower_endpoint_isolator':['1/4','3/8'],'upper_endpoint_isolator':['6','8'],
            'lower_repair_limits':[str(m),str(mp)],'odd_upper_strict_on':['0','8'],
            'feasibility':'exactly the closed interval between the two irrational roots',
            'whole_lower_rank_all_feasible':87,'whole_upper_rank_interior':88,'whole_upper_rank_endpoints':87,
            'scope':'original q8,k3,kappa0 slice; endpoint duals separately close the all-kappa repair projection'}
