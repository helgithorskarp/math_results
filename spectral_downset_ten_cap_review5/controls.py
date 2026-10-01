"""Meaningful malformed-certificate and hand-checkable arithmetic controls."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
from exact import determinant,inverse,require
from audit import audit

def controls(c):
    cases=[]
    def add(name,change):
        d=deepcopy(c);change(d);cases.append((name,d))
    add('wrong_n',lambda d:d.update(n=9))
    add('wrong_N',lambda d:d.update(N=1014))
    add('wrong_star',lambda d:d.update(s=503))
    add('layer_reversal',lambda d:d.update(layers=d['layers'][::-1]))
    add('inexact_integer',lambda d:d['lower_numerator'][0].__setitem__(0,15482237.0))
    add('boolean_integer',lambda d:d['upper_numerator'][0].__setitem__(0,True))
    add('zero_denominator',lambda d:d.update(common_denominator=0))
    add('wrong_matrix_dimension',lambda d:d['upper_numerator'].pop())
    add('asymmetry',lambda d:d['lower_numerator'][0].__setitem__(1,0))
    add('indefinite_symmetric',lambda d:d['lower_numerator'][0].__setitem__(0,-1))
    add('support_list_missing',lambda d:d['cancelled_unordered_layer_pairs'].pop())
    def cancellation(d):
        d['upper_numerator'][0][1]+=1;d['upper_numerator'][1][0]+=1
    add('lost_two_three_cancellation',cancellation)
    add('wrong_scalar',lambda d:d.update(weighted_mass_lower_bound='1'))
    add('inexact_rational',lambda d:d.update(weighted_mass_lower_bound='0.0044'))
    add('wrong_simple_bound',lambda d:d.update(simple_strict_lower_bound='1/1000'))
    def swapped(d):d['lower_numerator'],d['upper_numerator']=d['upper_numerator'],d['lower_numerator']
    add('swapped_duals',swapped)
    for name,d in cases:
        try:audit(d,literal=False)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):pass
        else:raise ValueError('invalid certificate accepted: '+name)
    for a,b,c0,d in product(range(-1,2),repeat=4):
        require(determinant([[a,b],[c0,d]])==a*d-b*c0,'literal2x2 determinant')
    require(determinant([[0,1],[1,0]])==-1,'row permutation sign')
    require(determinant([[1,2],[2,4]])==0,'singular determinant')
    require(determinant([])==1,'empty determinant')
    for a in [[[1]],[[2,1],[1,2]],[[4,1,0],[1,3,1],[0,1,2]]]:
        inv=inverse(a)
        require(all(sum(a[i][k]*inv[k][j] for k in range(len(a)))==int(i==j) for i in range(len(a)) for j in range(len(a))),'adjugate identity control')
    try:inverse([[1,2],[2,4]])
    except ValueError:pass
    else:raise ValueError('singular inverse accepted')
    # The refinement arithmetic must retain the 511 scale and ordered factor two.
    r=audit(c,literal=False)
    tau=F(r['tau_trace_YW']);beta=F(r['weighted_mass_lower_bound'])
    require(F(r['ordinary_H_cap_gap_strict_floor'])==beta/(511*tau) and F(r['ordinary_H_cap_gap_strict_floor'])!=beta/tau,'M/L scaling control')
    gmax=F(r['max_extra_coefficient'])
    require(F(r['extra_unordered_abs_M_mass_strict_floor'])==beta/(2*511*gmax) and F(r['extra_unordered_abs_M_mass_strict_floor'])!=beta/(511*gmax),'unordered support mass control')
    return {'rejected_certificates':[name for name,_ in cases],'literal2x2_determinants':81,'adjugate_controls':3,'singular_inverse_rejected':True,'M_L_and_ordered_scales_checked':True}
