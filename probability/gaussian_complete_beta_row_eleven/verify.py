"""Exact scalar premises for the complete Gaussian beta row N=11.

Standard-library Python 3.11+. The replica theorem is written mathematics.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb, isqrt
from pathlib import Path
import argparse
import copy
import json

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def evaluate(coefficients, x):
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result*x+coefficient
    return result


def power_on_interval(coefficients, left, width):
    n=len(coefficients)-1
    return [sum((coefficients[j]*comb(j,k)*left**(j-k)*width**k
                 for j in range(k,n+1)), F(0)) for k in range(n+1)]


def to_bernstein(coefficients):
    n=len(coefficients)-1
    return [sum((coefficients[k]*F(comb(i,k),comb(n,k))
                 for k in range(i+1)),F(0)) for i in range(n+1)]


def split_midpoint(coefficients):
    level=list(coefficients)
    left=[level[0]];right=[level[-1]]
    while len(level)>1:
        level=[(a+b)/2 for a,b in zip(level,level[1:])]
        left.append(level[0]);right.append(level[-1])
    return left,list(reversed(right))


def dyadic_leaves(coefficients, depth):
    rows=[coefficients]
    for _ in range(depth):
        rows=[child for row in rows for child in split_midpoint(row)]
    return rows


def root_bounds(n, denominator):
    integer=isqrt(n*denominator*denominator)
    lower=F(integer,denominator)
    upper=lower if lower*lower==n else F(integer+1,denominator)
    require(lower*lower<=n<=upper*upper,'Invalid square-root enclosure')
    return lower,upper


def check_case(case, root_denominator):
    m=case['base'];q=case['q'];depth=case['subdivision_depth']
    require(isinstance(depth,int) and 0<=depth<=12,'Subdivision depth')
    a,b,c=map(F,[case['a'],case['b'],case['c']])
    epsilon=F(case['epsilon']);critical_upper=F(case['critical_upper'])
    require(a>0 and b>0 and c>0 and epsilon>0,'Positive certificate constants')
    require(0<critical_upper<=1,'Critical point range')
    polynomial=[]
    for ell in range(q+1):
        lo,hi=root_bounds(m+ell,root_denominator)
        polynomial.append((-1)**ell*comb(q,ell)*(hi if ell%2 else lo))
    polynomial[0]-=a;polynomial[1]+=b;polynomial[2]-=c
    seen=set()
    for item in case['monotonicity']:
        ell=item['power'];coefficient=F(item['coefficient'])
        require(isinstance(ell,int) and 0<=ell<q and ell not in seen,
                'Monotonicity power')
        require(coefficient>=0,'Negative monotonicity multiplier')
        seen.add(ell)
        polynomial[ell]-=coefficient
        polynomial[ell+1]+=coefficient*F(m+ell+1,m+ell)**3
    leaves=dyadic_leaves(to_bernstein(polynomial),depth)
    intervals=2**depth
    encoded=[];minima=[];point_controls=0
    for index,recursive in enumerate(leaves):
        local=power_on_interval(polynomial,F(index,intervals),F(1,intervals))
        direct=to_bernstein(local)
        require(direct==recursive,'Independent Bernstein algorithms differ')
        require(min(direct)>0,'Scalar minorant is not certified')
        for k in range(q+1):
            t=F(k,q)
            bern=sum((direct[i]*comb(q,i)*t**i*(1-t)**(q-i)
                      for i in range(q+1)),F(0))
            require(bern==evaluate(polynomial,(index+t)/intervals),
                    'Polynomial identity control')
            point_controls+=1
        encoded.extend(str(x) for x in direct)
        minima.append(str(min(direct)))

    # The existing retained-interaction exponent at ell=2.
    exponent=F(2*(m+1)**2,m*(m+2))
    A=a/m**3;B=b/(m+1)**3;D=c/(m+2)**3
    numerator,denominator=exponent.numerator,exponent.denominator
    # h'(r)=0 iff r^(numerator-denominator)=(B/(exponent D))^denominator.
    root_slack=(critical_upper**(numerator-denominator)
                -(B/(exponent*D))**denominator)
    require(root_slack>=0,'Critical point upper bound failed')
    young_lower=A-B*(1-1/exponent)*critical_upper
    require(young_lower>=epsilon,'Young lower bound failed')
    return {'base':m,'q':q,'j':m-2,'exponent':str(exponent),
            'intervals':intervals,'bernstein_coefficients':len(encoded),
            'global_minimum':str(min(map(F,minima))),
            'coefficients_sha256':sha256(('\n'.join(encoded)+'\n').encode()).hexdigest(),
            'critical_upper':str(critical_upper),'critical_bound_verified':True,
            'young_lower':str(young_lower),'epsilon':str(epsilon),
            'identity_controls':point_controls}


def calculate(certificate):
    require(certificate['row']==11,'Wrong beta row')
    require(certificate['root_denominator']==2**40,'Wrong root denominator')
    cases=certificate['cases']
    require([(x['base'],x['q']) for x in cases]==[(2,11),(3,10),(4,9),(5,8)],
            'Missing or mislabeled left-row obligation')
    records=[check_case(case,certificate['root_denominator']) for case in cases]
    # Normalized beta degree elevation, checked for every lower-row entry.
    elevation_controls=0
    for n in range(11):
        for j in range(n+1):
            left=F(n+1-j,n+2);right=F(j+1,n+2)
            require(left>=0 and right>=0 and left+right==1,'Elevation convexity')
            require(left*(n+2)*comb(n+1,j)==(n+1)*comb(n,j),
                    'First elevation normalization')
            require(right*(n+2)*comb(n+1,j+1)==(n+1)*comb(n,j),
                    'Second elevation normalization')
            elevation_controls+=1
    covered=[(j,11-j,'new averaged certificate' if j<4 else 'credited seven-factor theorem')
             for j in range(12)]
    require(all(q<=7 for j,q,_ in covered if j>=4),'Right-row dependency')
    return {'status':'COMPLETE_BETA_ROW_ELEVEN_PASS',
            'complete_row':11,'lower_rows':list(range(12)),
            'full_majorisation_proved':False,'formalized':False,
            'new_cases':records,'coverage':covered,
            'bernstein_coefficients':sum(x['bernstein_coefficients'] for x in records),
            'polynomial_identity_controls':sum(x['identity_controls'] for x in records),
            'degree_elevation_controls':elevation_controls}


def corruption_controls(certificate):
    corruptions=[]
    altered=copy.deepcopy(certificate);altered['cases'].pop()
    corruptions.append(altered)
    altered=copy.deepcopy(certificate);altered['cases'][0]['a']='1000000'
    corruptions.append(altered)
    altered=copy.deepcopy(certificate);altered['cases'][0]['critical_upper']='1/1000000'
    corruptions.append(altered)
    altered=copy.deepcopy(certificate);altered['cases'][0]['epsilon']='1'
    corruptions.append(altered)
    for altered in corruptions:
        try:
            calculate(altered)
        except ValueError:
            pass
        else:
            raise RuntimeError('A damaged certificate was accepted')
    return len(corruptions)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-expected',action='store_true')
    args=parser.parse_args()
    certificate=json.loads((ROOT/'CERTIFICATE.json').read_text())
    result=calculate(certificate)
    result['rejected_corruptions']=corruption_controls(certificate)
    # JSON canonicalization makes tuples in coverage compare as arrays.
    result=json.loads(json.dumps(result))
    expected=ROOT/'EXPECTED.json'
    if args.write_expected:
        expected.write_text(json.dumps(result,indent=2)+'\n')
    else:
        require(result==json.loads(expected.read_text()),'Expected record mismatch')
    print(json.dumps({key:result[key] for key in ['status','complete_row',
        'bernstein_coefficients','polynomial_identity_controls',
        'degree_elevation_controls','rejected_corruptions',
        'full_majorisation_proved']},indent=2))


if __name__=='__main__':
    main()
