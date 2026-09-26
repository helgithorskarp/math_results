#!/usr/bin/env python3
"""Exact audits of the sparse interpolation bridge; standard library only."""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import permutations
from math import comb, factorial
from pathlib import Path
import json
import sys

BASE = Path(__file__).resolve().parent.parent
PIN = "60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7"
BOUND = BASE / "gaussian_majorisation_hankel_transport" / "bounds.py"
if sha256(BOUND.read_bytes()).hexdigest() != PIN:
    raise RuntimeError("interval dependency changed")
sys.path.insert(0, str(BOUND.parent))
from bounds import I, exp_negative, sqrt_integer  # noqa: E402

DIGITS = 70


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def multiply(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def evaluate(coeff, x):
    out = F(0)
    for c in reversed(coeff):
        out = out*x+c
    return out


def interpolate(nodes, power):
    n = len(nodes)
    require(len(set(nodes)) == n, "repeated interpolation node")
    require(all(0 <= x <= 1 for x in nodes), "node outside [0,1]")
    require(power >= n-1, "power below one-sided derivative range")
    dd = [x**power for x in nodes]
    out, product = [F(0)]*n, [F(1)]
    for j in range(n):
        require(0 <= dd[0] <= comb(power, j), "divided-difference bound failed")
        for k, c in enumerate(product):
            out[k] += dd[0]*c
        product = multiply(product, [-nodes[j], F(1)])
        dd = [(dd[i+1]-dd[i])/(nodes[i+j+1]-nodes[i])
              for i in range(len(dd)-1)]
    return out


def interpolation_controls():
    count, clustered = 0, 0
    for n in range(2, 8):
        families = [
            [F(i, n-1) for i in range(n)],
            [F(i+1, n+1) for i in range(n)],
            [F(1)-F(n-i, 10**6) for i in range(n)],
        ]
        for family, nodes in enumerate(families):
            for power in [n-1, n+2, 2*n+5]:
                coeff = interpolate(nodes, power)
                require(all(evaluate(coeff, x) == x**power for x in nodes),
                        "interpolation identity failed")
                budget = sum(F(2**j * comb(power, j)) for j in range(n))
                require(sum(abs(c) for c in coeff) <= budget,
                        "coefficient norm bound failed")
                simple = F(2*(2*power)**(n-1), factorial(n-1))
                require(budget <= simple, "geometric-series bound failed")
                weights = [F((-1)**i * comb(n-1, i)) for i in range(n)]
                moments = [sum(c*x**j for c,x in zip(weights,nodes))
                           for j in range(n)]
                lhs = sum(c*x**power for c,x in zip(weights,nodes))
                rhs = sum(a*b for a,b in zip(coeff,moments))
                require(lhs == rhs, "exponential extrapolation identity failed")
                count += 1
                clustered += family == 2
    return {"exact_interpolations": count, "nearly_coalescing_node_cases": clustered,
            "orders": [2,3,4,5,6,7], "minimum_cluster_spacing": "1/1000000"}


def constants():
    # e > 1+1+1/2+1/6+1/24 > 8/3.
    e_lower = sum(F(1, factorial(k)) for k in range(5))
    require(e_lower > F(8,3), "elementary e lower bound failed")
    rho3 = F(2**26) * F(3,8)**20
    step = F(256) * F(3,8)**9
    require(2**32 > 3**20, "tail-margin integer certificate failed")
    require(rho3 < F(1,4) and step < 1, "uniform tail-ratio certificate failed")
    require(F(352*32,11) == 1024, "tail/positive-window coefficient failed")
    require(F(3,4)*F(1,12)*F(1,32) == F(1,512),
            "quantitative margin coefficient failed")
    require(F(16,15)**3 < 2, "kappa inverse bound failed")
    require(F(59,15)/4 > F(3,4), "central-window beta bound failed")
    require(F(5,16)+3 < 4, "central-window exponential bound failed")
    table=[]
    for n in [3,4,8,16,64]:
        eps = F(1,24*n)
        level = (4-5*eps)**2/(32*eps*(1-eps))
        require(level >= 11*n, "variance-to-level implication failed")
        require(2-F(2*n*2+5,2)/level >= 1, "tail integral denominator failed")
        table.append({"monomials":n, "variance_over_radius_squared":24*n,
                      "L":str(level), "tail_ratio_upper":str(rho3*step**(n-3))})
    # Keep large exact powers out of the compact output at large n.
    for row in table:
        if row['monomials']>8:
            row['tail_ratio_upper']='rho3 * step^(N-3), with rho3<1/4 and step<1'
    return {"rho3_rational_upper":str(rho3), "ratio_step_upper":str(step),
            "surviving_fraction_lower":"3/4", "table":table}


def determinant(matrix):
    n=len(matrix)
    out=I.of(0)
    for perm in permutations(range(n)):
        inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=I.of((-1)**inversions)
        for i,j in enumerate(perm):
            term=(term*I.of(matrix[i][j])).rounded(DIGITS)
        out=(out+term).rounded(DIGITS)
    return out


@lru_cache(maxsize=512)
def two_atom_moment(j, variance, contraction):
    """Exact ordered-replica binomial reduction, X=+/-e1 equiprobably."""
    m=j+2
    loss=I.of(0)
    for k in range(m+1):
        exponent=F(2*k*(m-k),m)/variance
        gap=(exp_negative(-contraction*contraction*exponent,DIGITS)
             -exp_negative(-exponent,DIGITS))
        loss=(loss+F(comb(m,k),2**m)*gap).rounded(DIGITS)
    # d_m=m^(-3/2) times loss, a_(m-2)=d_m/[m(m-1)].
    return (loss/(m*m*(m-1)*sqrt_integer(m,DIGITS))).rounded(DIGITS)


def gaussian_controls():
    out=[]
    cases=[([0,1,2],72,F(0)),([0,5,24],72,F(0)),
           ([100,101,102],72,F(0)),([0,1,2],72,F(99,100)),
           ([0,5,24],72,F(99,100)),([100,101,102],72,F(99,100)),
           ([0,1,3,8],96,F(1,2))]
    for indices,s,lam in cases:
        require(s>=24*len(indices), "finite case outside hierarchy bound")
        matrix=[[two_atom_moment(i+j,F(s),lam) for j in indices] for i in indices]
        minors=[]
        for n in range(1,len(indices)+1):
            det=determinant([row[:n] for row in matrix[:n]])
            require(det.lo>0, "finite principal-block positivity inconclusive")
            minors.append(det.strings(48))
        out.append({"indices":indices,"R":"1","s":s,"lambda":str(lam),
                    "leading_principal_determinants":minors})
    # Previously published abstract log-convex counterexample: negative control only.
    seq=[F(1),F(1,2),F(1,3),F(1,4),F(19,100)]
    det=determinant([[seq[i+j] for j in range(3)] for i in range(3)])
    require(det.lo<=F(-1,2700)<=det.hi<0, "negative determinant control failed")
    return {"actual_contraction_blocks":out,"abstract_negative_control":"-1/2700",
            "warning":"Finite examples audit formulas; the universal theorem is analytic."}


def main():
    result={"status":"exact finite audits of an analytic author proof",
            "arithmetic":"Fraction and outward rational intervals; no floating point",
            "digits":DIGITS,"bounds_sha256":PIN,
            "interpolation":interpolation_controls(),"constants":constants(),
            "gaussian":gaussian_controls()}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
