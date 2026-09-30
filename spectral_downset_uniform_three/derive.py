#!/usr/bin/env python3
"""Optional CAS regeneration: SymPy 1.14.0 over Q(n,t), one native thread.

This script discovers the centered formula and regenerates the small
coefficient certificate. verify.py checks it without SymPy. No numerical
optimizer, sampling, algebraic extension, or modular reconstruction is used.
"""
import argparse
import json
from pathlib import Path
import sympy as sp


def require(condition, message):
    if not condition:
        raise ValueError(message)


def normal(x):
    return sp.factor(sp.cancel(x))


def choose(x, k):
    return sp.prod(x-i for i in range(k))/sp.factorial(k)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    require(sp.__version__ == '1.14.0', 'reproduction requires SymPy 1.14.0')
    n, t, u = sp.symbols('n t u')
    variables = sp.symbols('b11 b12 b13 b22 b23 b33')
    b11, b12, b13, b22, b23, b33 = variables
    B = sp.Matrix([[b11,b12,b13],[b12,b22,b23],[b13,b23,b33]])
    N = normal(1+sum(choose(n, k) for k in (1, 2, 3)))
    s = normal(1+n-1+choose(n-1, 2))
    equations = [sum(B[a-1,b-1]*choose(n-a-1,b-1) for b in (1,2,3))-s
                 for a in (1,2,3)] + [
                 sum(B[a-1,b-1]*choose(n-a,b) for b in (1,2,3))-(N-1-s)
                 for a in (1,2,3)]
    solutions = list(sp.linsolve(equations, variables))
    require(len(solutions) == 1, 'centered solution family')
    family = [normal(x.subs(b33, t)) for x in solutions[0]]
    choice = sp.solve(family[0], t)
    require(len(choice) == 1 and normal(choice[0]-(n+1)/(n-5)) == 0,
            'b11=0 choice')
    substitution = dict(zip(variables, [normal(x.subs(t, choice[0])) for x in family]))
    require(all(normal(x.subs(substitution)) == 0 for x in equations), 'linear residual')
    beta = B.subs(substitution)
    expected = sp.Matrix([[0,-(n-4)/(n-2),(n+3)/(n-3)],
                          [-(n-4)/(n-2),2*(4*n-9)/((n-3)*(n-2)),(n+3)/(n-3)],
                          [(n+3)/(n-3),(n+3)/(n-3),(n+1)/(n-5)]])
    require(all(normal(x) == 0 for x in beta-expected), 'explicit formula agreement')
    K = []
    for j in range(4):
        layers = list(range(max(1,j),4))
        block = sp.Matrix([[s*int(a==b)-(choose(n,b) if j==0 else 0) +
                            (-1)**j*beta[a-1,b-1]*choose(n-a-j,b-j)
                            for b in layers] for a in layers]).applyfunc(normal)
        G = sp.diag(*(choose(n-2*j,a-j) for a in layers))
        require(all(normal(x) == 0 for x in G*block-(G*block).T), 'metric symmetry')
        K.append(block)
    tau = normal(sp.trace(K[1]))
    d = normal(sum(K[1].extract([i,j],[i,j]).det() for i in range(3) for j in range(i+1,3)))
    margins = {'C0_gap1': sp.trace(K[0])-1, 'U0_gap1': N-sp.trace(K[0])-1,
               'C1_shift_trace': tau-2, 'C1_shift_det': d-tau+1,
               'U1_shift_trace': 2*(N-1)-tau,
               'U1_shift_det': (N-1)**2-(N-1)*tau+d,
               'C2_shift_diag': K[2][0,0]-1, 'C2_shift_det': (K[2]-sp.eye(2)).det(),
               'U2_shift_diag': N-1-K[2][0,0],
               'U2_shift_det': ((N-1)*sp.eye(2)-K[2]).det(),
               'C3_gap1': K[3][0,0]-1, 'U3_gap1': N-K[3][0,0]-1}
    result = {'agent':'six-downset-3', 'role':'researcher', 'coefficient_domain':'Q[n]',
              'substitution':'n=6+u, u>=0', 'CAS_discovery':'SymPy '+sp.__version__, 'margins':{}}
    for name, x in margins.items():
        x = normal(x)
        num, den = sp.fraction(normal(x.subs(n, u+6)))
        a = list(reversed(sp.Poly(num, u, domain=sp.ZZ).all_coeffs()))
        b = list(reversed(sp.Poly(den, u, domain=sp.ZZ).all_coeffs()))
        require(all(v >= 0 for v in a+b) and a[0] > 0 and b[0] > 0, 'positive coefficients')
        result['margins'][name] = {'expression':str(x), 'numerator_ascending':list(map(int,a)),
                                   'denominator_ascending':list(map(int,b))}
    result['status'] = 'Exact positivity identities; soundness requires the harmonic and rank-lifting proofs in PROOF.md.'
    if args.check:
        require(result == json.loads(args.check.read_text()), 'certificate differs')
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'ok':True,'system':'SymPy '+sp.__version__,'domain':'Q(n,t)',
                      'free_parameter_choice':str(normal(choice[0])),'positive_margins':len(margins)}))


if __name__ == '__main__':
    main()
