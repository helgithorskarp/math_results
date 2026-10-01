#!/usr/bin/env python3
"""Optional exact certificate regeneration: SymPy 1.14.0 over Q(n).

The standard-library checker uses a separate principal-determinant route.
Boundary tables are frozen rational witnesses discovered numerically and
verified exactly; regeneration of them is unnecessary for this proof.
"""
import argparse
import json
from pathlib import Path
from math import comb, factorial
import sympy as sp
from sympy.polys.matrices import DomainMatrix

from matrices import parts


def choose(x,k):
    return sp.prod([x-i for i in range(k)])*sp.Rational(1,factorial(k))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check',type=Path)
    args = parser.parse_args()
    if sp.__version__ != '1.14.0':
        raise ValueError('Regeneration requires SymPy 1.14.0')
    n,u = sp.symbols('n u')
    s = sp.expand(sum(choose(n-1,k) for k in range(5)))
    m = sp.expand(sum(choose(n,k) for k in range(1,6)))
    D = 120*sp.prod(n-i for i in range(2,10))
    beta = sp.zeros(5)
    for (a,b),(p,factors) in parts(n).items():
        beta[a-1,b-1] = beta[b-1,a-1] = p/sp.prod(n-i for i in factors)
    equations = [sum(beta[a-1,b-1]*choose(n-a-1,b-1) for b in range(1,6))-s for a in range(1,6)]
    equations += [sum(beta[a-1,b-1]*choose(n-a,b) for b in range(1,6))-(m-s) for a in range(1,6)]
    if any(sp.cancel(v) != 0 for v in equations):
        raise ValueError('Exact affine residual')
    pairs = [(a,b) for a in range(1,6) for b in range(a,6)]
    vs = sp.symbols(' '.join(f'b{a}{b}' for a,b in pairs))
    free_beta = sp.zeros(5)
    for (a,b),v in zip(pairs,vs):
        free_beta[a-1,b-1] = free_beta[b-1,a-1] = v
    eq = [sum(free_beta[a-1,b-1]*choose(n-a-1,b-1) for b in range(1,6))-s for a in range(1,6)]
    eq += [sum(free_beta[a-1,b-1]*choose(n-a,b) for b in range(1,6))-(m-s) for a in range(1,6)]
    eq += [free_beta[a-1,b-1] for a in range(1,4) for b in range(a,4)]
    sol = list(sp.linsolve(eq,vs))
    if len(sol) != 1 or any(sp.cancel(v-beta[a-1,b-1]) != 0 for (a,b),v in zip(pairs,sol[0])):
        raise ValueError('Sparse affine formula uniqueness')
    output = {}
    for j in range(6):
        layers = list(range(max(1,j),6))
        K = sp.Matrix([[s*int(a == b)+(-1)**j*beta[a-1,b-1]*choose(n-a-j,b-j)-
                        (choose(n,b) if j == 0 else 0) for b in layers] for a in layers])
        H = K.applyfunc(lambda v:sp.cancel(v*D).expand())
        dm = DomainMatrix.from_Matrix(H)
        char = [dm.domain.to_sympy(v) for v in dm.charpoly()]
        e = [sp.factor(sp.cancel((-1)**k*v/D**k)) for k,v in enumerate(char)]
        d = len(layers)-(2 if j == 0 else 1 if j == 1 else 0)
        if any(v != 0 for v in e[d+1:]):
            raise ValueError('Characteristic kernel')
        for k in range(1,d+1):
            low = sum((-1)**(k-l)*comb(d-l,k-l)*e[l] for l in range(k+1))
            high = sum((-1)**l*comb(d-l,k-l)*m**(k-l)*e[l] for l in range(k+1))
            for label,v in [(f'lower_{j}_{k}',low),(f'upper_{j}_{k}',high)]:
                p,q = sp.fraction(sp.factor(sp.cancel(v)))
                p = list(reversed(sp.Poly(p.subs(n,u+12),u).all_coeffs()))
                q = list(reversed(sp.Poly(q.subs(n,u+12),u).all_coeffs()))
                if any(x < 0 or not x.is_Integer for x in p+q) or p[0] <= 0 or q[0] <= 0:
                    raise ValueError('Coefficient sign certificate: '+label)
                output[label] = {'shift':12,'numerator_ascending':[int(x) for x in p],
                                 'denominator_ascending':[int(x) for x in q]}
    if args.check and output != json.loads(args.check.read_text()):
        raise ValueError('Frozen certificate mismatch')
    if args.output:
        args.output.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'ok':True,'affine_equations':10,'sparse_zero_choices':6,
                      'infinite_spectral_margins':len(output),'shift':12}))


if __name__ == '__main__':
    main()
