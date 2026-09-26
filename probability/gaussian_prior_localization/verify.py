"""Exact finite algebra controls for the written localization proof.

These checks do not prove minimax, analyticity, or the open conjecture.
The finite-cell examples below are not Gaussian contraction examples.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from math import factorial
from pathlib import Path

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def double_factorial(n):
    value = 1
    while n > 0:
        value *= n; n -= 2
    return value

def sphere_moment(alpha):
    if any(a % 2 for a in alpha):
        return F(0)
    numerator = 1
    for a in alpha:
        numerator *= double_factorial(a-1)
    return F(numerator, double_factorial(sum(alpha)+1))

def moment(points, alpha):
    result = F(0)
    for point in points:
        term = F(1)
        for x, a in zip(point, alpha):
            term *= x**a
        result += term / len(points)
    return result

def signed_kernel_coefficients(points, degree):
    require(all(sum(x*x for x in p) == 1 for p in points), 'unit sphere fixture')
    rows = []
    for k in range(degree+1):
        tensor = F(0)
        for a in range(k+1):
            for b in range(k-a+1):
                alpha = (a, b, k-a-b)
                m = moment(points, alpha) - sphere_moment(alpha)
                multi = factorial(k)
                for j in alpha:
                    multi //= factorial(j)
                tensor += multi*m*m
        # Independently integrate the rotational cross terms. A coordinate
        # of uniform surface probability on S2 is uniform on [-1,1].
        direct = sum(F(sum(x*y for x,y in zip(p,q)))**k
                     for p,q in product(points, repeat=2))/len(points)**2
        direct -= F(1, k+1) if k % 2 == 0 else F(0)
        require(tensor == direct and tensor >= 0, 'positive kernel energy identity')
        rows.append(str(tensor))
    return rows

def finite_cell_controls():
    # Select one unit-volume cell, allowing relaxation 0<=psi<=1, sum psi<=1.
    # Convexity and a displayed saddle pair give exact values for every prior.
    cases = [
        {'target':((F(1), F(0)), (F(0), F(1))),
         'source_A':(F(1,2), F(1,2)), 'prior':(F(1,2), F(1,2)),
         'selector':(F(1,2), F(1,2)), 'value':F(0)},
        {'target':((F(3,5),F(3,10),F(1,10)), (F(1,5),F(3,10),F(1,2))),
         'source_A':(F(2,5),F(2,5)), 'prior':(F(3,8),F(5,8)),
         'selector':(F(1,2),F(0),F(1,2)), 'value':F(-1,20)}]
    results = []
    for case in cases:
        G, a, w, psi, value = [case[k] for k in ('target','source_A','prior','selector','value')]
        require(sum(w)==sum(psi)==1 and min(w)>=0 and min(psi)>=0, 'feasible saddle')
        require(all(sum(row)==1 and min(row)>=0 for row in G), 'probability cells')
        q = [sum(p*g for p,g in zip(psi,row))-z for row,z in zip(G,a)]
        target = [sum(w[i]*G[i][j] for i in range(len(w))) for j in range(len(psi))]
        primal = max(target)-sum(x*y for x,y in zip(w,a))
        require(primal == min(q) == value, 'exact primal dual agreement')
        require(all(q[i]==value for i in range(len(w)) if w[i]>0), 'contact condition')
        pure = max(min(G[i][j]-a[i] for i in range(len(w))) for j in range(len(psi)))
        require(pure < value, 'tied finite levels require randomization')
        results.append({'value':str(value), 'best_pure_selector':str(pure),
                        'prior':list(map(str,w)), 'selector':list(map(str,psi))})
    return results

def audit():
    # Coefficients of (z^2+3)sinh(z)-3z cosh(z), by two formulas.
    coefficients = []
    for k in range(41):
        direct = F(3, factorial(2*k+1))-F(3, factorial(2*k))
        if k:
            direct += F(1, factorial(2*k-1))
        formula = F(4*k*(k-1), factorial(2*k+1))
        require(direct == formula and (direct>0 if k>=2 else direct==0), 'hyperbolic coefficient')
        coefficients.append(str(direct))
    axes = [tuple(F(sign) if i==axis else F(0) for i in range(3))
            for axis in range(3) for sign in (-1,1)]
    axis_rows = signed_kernel_coefficients(axes, 16)
    require(axis_rows[4] == '2/15' and all(axis_rows[k]=='0' for k in range(4)),
            'first nonuniform octahedral tensor')
    single_rows = signed_kernel_coefficients([(F(1),F(0),F(0))], 16)
    require(single_rows[1]=='1', 'Dirac measure is not uniform surface measure')
    # Negative fixture must not pass a finite fragment of the radial proof.
    invalid_rejected = False
    try:
        require(coefficients[2] == '0', 'altered strict hyperbolic coefficient')
    except RuntimeError:
        invalid_rejected = True
    require(invalid_rejected, 'negative algebra control')
    return {'status':'GAUSSIAN_PRIOR_LOCALIZATION_EXACT_CONTROLS_PASS',
            'full_conjecture_resolved':False,
            'hyperbolic_coefficients_checked':len(coefficients),
            'sphere_tensor_degrees_checked':16,
            'octahedral_signed_kernel_coefficients':axis_rows,
            'dirac_signed_kernel_coefficients':single_rows,
            'finite_cell_saddles_not_gaussian_data':finite_cell_controls(),
            'negative_algebra_control_rejected':invalid_rejected}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    p.add_argument('--write', type=Path)
    a = p.parse_args(); result = audit()
    raw = (json.dumps(result, indent=2, sort_keys=True)+'\n').encode()
    if a.check:
        require(json.loads(Path(__file__).with_name('EXPECTED.json').read_text()) == result,
                'published exact expected output')
    if a.write:
        a.write.write_bytes(raw)
    print(result['status'], sha256(raw).hexdigest())

if __name__ == '__main__':
    main()
