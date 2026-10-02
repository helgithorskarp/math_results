"""Optional complete shared-field comparison, without importing author code."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import json
import signal
import sys

spec=importlib.util.spec_from_file_location('own_check',Path(__file__).with_name('check.py'))
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
P,vars,zero=c.P,c.vars,c.zero


def decode(entries, n=2):
    return P(n,{tuple(row[:-1]):Q(row[-1]) for row in entries})


def own_decode(entries,n):
    return P(n,{tuple(e):Q(z) for e,z in entries})


def run(fixture):
    mine=c.run();a,b,z=vars(3);S,T=vars(2)
    d=own_decode(mine['cubic']['mass_denominator'],3)
    tr=own_decode(mine['cubic']['Newton_squared_trace'],3)
    num=1024*z*z*d*d+2*b*b*tr
    den=b*b*d*d
    author=fixture['interior']
    zero(decode(author['eta_common_denominator']).sub([a,b])-den,'whole original cubic denominator')
    for k,entries in enumerate(author['eta_coefficient_numerators']):
        mycoeff=P(2,{(e[0],e[1]):v for e,v in num.d.items() if e[2]==k})
        zero(decode(entries)-mycoeff,'whole original cubic numerator '+str(k))
    for name,key in [('F','derivative_factor_F'),('G','derivative_factor_G')]:
        zero(decode(author['polynomials'][name]).sub([a,b])-own_decode(mine['cubic'][key],3),'whole original derivative factor '+name)
    col=mine['collision_boundary'];d=own_decode(col['mass_denominator'],2);tr=own_decode(col['Newton_squared_trace'],2)
    den=(S+2*T)**2*d*d;num=1024*T*T*d*d+2*(S+2*T)**2*tr
    R=decode(fixture['collision']['R']);K=9*S*S-4*S+4-32*T;V=3*S*S-4*S+4-8*T
    zero(decode(fixture['collision']['common_mass_denominator'])-den,'whole original collision denominator')
    zero((4*(S+2)**2*den-num)*(S+2*T)**2*K-2*R*den,'whole original collision ratio')
    zero(6*(S+2*T)**2*V*K-R-decode(fixture['collision']['W24']),'whole original collision gap numerator')
    zero(decode(fixture['collision']['P'])-own_decode(col['gap_polynomial'],2),'whole original gap polynomial')
    for original,mine_patch in zip(fixture['gap_positivity']['lower_patches'],col['rectangles']):
        if original['rectangle']!=mine_patch['box']:raise ValueError('original rectangle differs')
        flat=[[i,j,v] for i,row in enumerate(original['coefficients']) for j,v in enumerate(row)]
        actual=[[ij[0],ij[1],v] for ij,v in mine_patch['coefficients']]
        if flat!=actual:raise ValueError('whole original rectangle entries differ')
    if len(fixture['gap_positivity']['lower_patches'])!=7:raise ValueError('incomplete original cover')
    if len(fixture['gap_positivity']['upper_power_coefficients'])!=5:raise ValueError('incomplete upper ray')
    for p,q in zip(fixture['gap_positivity']['upper_power_coefficients'],col['upper_polynomials']):
        zero(decode(p)-own_decode(q,1).sub([S]),'whole original upper polynomial')
    return {'status':'PASS','full_lower_Bernstein_entries':245,'full_upper_polynomials':5,
            'whole_cubic_numerators':3,'whole_cubic_denominators':1,'whole_derivative_factors':2,
            'whole_collision_ratio_gap_and_denominator':4}


if __name__=='__main__':
    signal.alarm(45)
    print(json.dumps(run(json.loads(Path(sys.argv[1]).read_text()))))
