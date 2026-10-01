#!/usr/bin/env python3
"""Exact author checks; the analytic/local-to-global proof is in PROOF.md.

Pure Python rational polynomial and second-order Taylor arithmetic.
No numerical roots, external algebra system, or imported research code.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(a):
    a = list(a)
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def add(a, b):
    out = [Q(0)] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] += value
    for i, value in enumerate(b):
        out[i] += value
    return trim(out)


def scale(a, scalar):
    return trim([value * scalar for value in a])


def mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, value in enumerate(a):
        for j, other in enumerate(b):
            out[i + j] += value * other
    return trim(out)


def diff(a):
    return trim([i * a[i] for i in range(1, len(a))] or [Q(0)])


def evaluate(a, value):
    out = Q(0)
    for coefficient in reversed(a):
        out = out * value + coefficient
    return out


def divrem(a, b):
    a, b = trim(a), trim(b)
    require(b != [0], 'polynomial division by zero')
    quotient = [Q(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a != [0]:
        k, coefficient = len(a) - len(b), a[-1] / b[-1]
        quotient[k] += coefficient
        a = add(a, scale([Q(0)] * k + b, -coefficient))
    return trim(quotient), trim(a)


def mod(a, b):
    return divrem(a, b)[1]


def inverse(a, modulus):
    r0, r1 = modulus, mod(a, modulus)
    s0, s1 = [Q(0)], [Q(1)]
    while r1 != [0]:
        quotient, remainder = divrem(r0, r1)
        r0, r1 = r1, remainder
        s0, s1 = s1, add(s0, scale(mul(quotient, s1), -1))
    require(len(r0) == 1 and bool(r0[0]), 'noninvertible polynomial')
    return mod(scale(s0, 1 / r0[0]), modulus)


def powers(a, order):
    n = len(a) - 1
    require(a[-1] == 1, 'Newton polynomial must be monic')
    out = [Q(n)]
    for k in range(1, order + 1):
        total = Q(0)
        for j in range(1, min(k, n) + 1):
            total += a[n - j] * (out[k - j] if j < k else Q(k))
        out.append(-total)
    return out


def trace(a, modulus):
    a = mod(a, modulus)
    return sum(c * p for c, p in zip(a, powers(modulus, len(a) - 1)))


class Poly2:
    """Polynomial in two independent variables, with no degree truncation."""
    def __init__(self, value=0):
        if isinstance(value, Poly2):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {key: Q(c) for key, c in value.items() if c}
        else:
            self.terms = {(0, 0): Q(value)} if value else {}

    def __bool__(self):
        return bool(self.terms)

    def __eq__(self, other):
        return self.terms == Poly2(other).terms

    def __add__(self, other):
        out = self.terms.copy()
        for key, c in Poly2(other).terms.items():
            out[key] = out.get(key, Q(0)) + c
        return Poly2(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly2({key: -c for key, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly2(other)

    def __rsub__(self, other):
        return Poly2(other) + -self

    def __mul__(self, other):
        out = {}
        for key, c in self.terms.items():
            for other_key, d in Poly2(other).terms.items():
                new_key = tuple(x + y for x, y in zip(key, other_key))
                out[new_key] = out.get(new_key, Q(0)) + c * d
        return Poly2(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / Q(scalar))

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'bad exponent')
        out = Poly2(1)
        for _ in range(exponent):
            out = out * self
        return out

    def derivative(self, index):
        out = {}
        for key, c in self.terms.items():
            if key[index]:
                reduced = list(key)
                reduced[index] -= 1
                out[tuple(reduced)] = c * key[index]
        return Poly2(out)

    def at(self, first, second):
        return sum(c * first**i * second**j for (i, j), c in self.terms.items())


class Jet:
    """Second-order rational Taylor polynomial in dr,dt, modulo degree three."""
    def __init__(self, value=0):
        if isinstance(value, Jet):
            self.terms = value.terms.copy()
        elif isinstance(value, dict):
            self.terms = {key: Q(c) for key, c in value.items() if c and sum(key) <= 2}
        else:
            self.terms = {(0, 0): Q(value)} if value else {}

    def __add__(self, other):
        out = self.terms.copy()
        for key, c in Jet(other).terms.items():
            out[key] = out.get(key, Q(0)) + c
        return Jet(out)

    __radd__ = __add__

    def __neg__(self):
        return Jet({key: -c for key, c in self.terms.items()})

    def __sub__(self, other):
        return self + -Jet(other)

    def __rsub__(self, other):
        return Jet(other) + -self

    def __mul__(self, other):
        out = {}
        for key, c in self.terms.items():
            for other_key, d in Jet(other).terms.items():
                new_key = tuple(x + y for x, y in zip(key, other_key))
                if sum(new_key) <= 2:
                    out[new_key] = out.get(new_key, Q(0)) + c * d
        return Jet(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        out = Jet(1)
        for _ in range(exponent):
            out = out * self
        return out

    def reciprocal(self):
        c = self.terms.get((0, 0), Q(0))
        require(bool(c), 'jet inverse has zero constant')
        n = (self - c) * (1 / c)
        return (1 - n + n * n) * (1 / c)

    def __truediv__(self, other):
        return self * Jet(other).reciprocal()

    def __rtruediv__(self, other):
        return Jet(other) * self.reciprocal()

    def coefficient(self, i, j):
        return self.terms.get((i, j), Q(0))


def profile(r, t):
    return mul(mul([-r, 0, 1], [-r, 0, 1]), [t, 0, 2*r-Q(1, 2), 0, 1])


def invariants(r, t):
    u = Q(3, 8)-r
    v = t/2+r/8-r*r/2
    X = 12*r*r-4*r+Q(1, 2)-4*t
    p = 8*r*t/v
    N, M = 1-p, X-Q(1, 8)
    eta = p*p+(2*M*M-2*M*N*u+N*N*(u*u-2*v))/(2*(u*u-4*v))
    return X, eta


def formal(b):
    return [15*(4-3*b)**3/(Q(11239424)*(2-b)*(4-b)), 0,
            -15*(4-3*b)**2/(Q(12544)*(2-b)*(4-b)), 0,
            15*(4-3*b)/(Q(448)*(2-b)), 0, -Q(1, 2), 0, Q(1)]


def L(h, b):
    sigma = [(4-3*b)/224, 0, b/8]
    return add(add(mul(sigma, diff(diff(h))),
                   scale(mul([0, 1], diff(h)), -(1+7*b/8))), scale(h, 8))


def encode(value):
    if isinstance(value, Poly2):
        return [[list(key), str(c)] for key,c in sorted(value.terms.items())]
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    if isinstance(value, dict):
        return {str(k): encode(v) for k, v in value.items()}
    return str(value)


def verify():
    records = {}
    def check(name, actual, expected):
        require(actual == expected, name+' failed')
        records[name] = encode(actual)

    r0, t0, b0, R0 = Q(11,56), Q(11,9408), -Q(8,5), -Q(112,25)
    r, t = Poly2({(1,0):1}), Poly2({(0,1):1})
    f = profile(r,t)
    u, v = Q(3,8)-r, t/2+r/8-r*r/2
    g = mul(mul([0,1],[-r,0,1]),[v,0,-u,0,1])
    check('full_two_parameter_compression_identity', scale(diff(f),Q(1,8)), g)
    check('full_two_parameter_normalized_coefficients', [f[8],f[7],f[6]], [1,0,-Q(1,2)])

    # Symbolic identity behind the two pair-weight squares, independent of r,t.
    y1,y2 = r,t
    # Compare the M², MN, N² coefficients of the two squared numerators.
    check('pair_weight_square_coefficients',
          [Poly2(1)**2+Poly2(-1)**2,2*(-y2)+2*(-1)*y1,y2*y2+y1*y1],
          [Poly2(2),-2*(y1+y2),(y1+y2)**2-2*y1*y2])
    check('squared_pair_eigenvalue_difference', (y1-y2)**2,
          (y1+y2)**2-4*y1*y2)

    f0 = [c.at(r0,t0) if isinstance(c,Poly2) else Q(c) for c in f]
    g0 = scale(diff(f0),Q(1,8))
    check('lower_endpoint_factorization', formal(b0), f0)
    check('lower_endpoint_ODE', L(f0,b0), [0])
    check('compression_squared_root_discriminant',
          (Q(3,8)-r0)**2-4*(t0/2+r0/8-r0*r0/2), Q(5,588))
    check('compression_factor_at_outer_root',
          r0*r0-(Q(3,8)-r0)*r0+t0/2+r0/8-r0*r0/2, Q(11,1176))
    check('ODE_six_diagonal_coefficients',
          [L([Q(0)]*i+[Q(1)],b0)[i] for i in range(6)],
          [Q((8-i)*(5+i),5) for i in range(6)])

    for label, rr, tt in [('endpoint',r0,t0),('real_1',Q(1,5),Q(1,1000)),
                         ('real_2',Q(3,16),Q(1,640)),
                         ('nonreal_extension',Q(1,5),Q(1,250))]:
        fp = profile(rr,tt);gp=scale(diff(fp),Q(1,8))
        rho=mod(scale(mul(fp,inverse(diff(gp),gp)),-8),gp)
        xp,ep=invariants(rr,tt)
        check(label+'_exact_residue_eta',trace(mul(rho,rho),gp),ep)
        check(label+'_root_fourth_moment',powers(fp,4)[4],xp)
        check(label+'_weight_total',trace(rho,gp),Q(1))
        check(label+'_weighted_second_moment',trace(mul(rho,[0,0,1]),gp),xp-Q(1,8))
        check(label+'_compression_fourth_trace',powers(gp,4)[4],xp/2+Q(1,32))

    rj=Jet({(0,0):r0,(1,0):1});tj=Jet({(0,0):t0,(0,1):1})
    xj,ej=invariants(rj,tj);jj=R0*xj-ej
    check('endpoint_X_eta_J',[xj.coefficient(0,0),ej.coefficient(0,0),jj.coefficient(0,0)],
          [Q(29,168),Q(5,21),-Q(177,175)])
    check('stationary_gradient',[jj.coefficient(1,0),jj.coefficient(0,1)],[0,0])
    H=[[2*jj.coefficient(2,0),jj.coefficient(1,1)],
       [jj.coefficient(1,1),2*jj.coefficient(0,2)]]
    check('rational_jet_Hessian',H,[[-Q(73344,125),-Q(1064448,125)],
                                 [-Q(1064448,125),-Q(24385536,125)]])
    det=H[0][0]*H[1][1]-H[0][1]*H[1][0]
    check('Hessian_determinant',det,Q(131096641536,3125))
    require(H[0][0]<0 and det>0,'Hessian definiteness failed')
    xgrad=[xj.coefficient(1,0),xj.coefficient(0,1)]
    response=[(-H[1][1]*xgrad[0]+H[0][1]*xgrad[1])/det,
              (H[1][0]*xgrad[0]-H[0][0]*xgrad[1])/det]
    check('stationary_branch_response',response,[Q(25,6048),-Q(25,124416)])
    xr=sum(a*b for a,b in zip(xgrad,response))
    check('constrained_X_response',xr,Q(5725,1524096))

    # Independent residue trace Gram calculation, not rational-jet differentiation.
    hs=[[c.derivative(i).at(r0,t0) if isinstance(c,Poly2) else Q(0)
         for c in f] for i in range(2)]
    invg=inverse(diff(g0),g0)
    def residual(h):
        return mod(scale(mul(L(h,b0),invg),-1),g0)
    Ts=[residual(h) for h in hs]
    gram=[[-2*trace(mul(a,b),g0) for b in Ts] for a in Ts]
    check('independent_spectral_Gram_Hessian',gram,H)
    hR=add(scale(hs[0],response[0]),scale(hs[1],response[1]))
    inner_quartic=[t0,0,2*r0-Q(1,2),0,1]
    hsplit=add(add(mul([0,1],diff(f0)),scale(f0,-8)),
               scale(mul([r0,0,1],inner_quartic),-1))
    check('split_variation_is_normalized',hsplit[6:] if len(hsplit)>6 else [],[])
    DX=-4*hsplit[4]
    check('split_X_derivative',DX,Q(5,3))
    split_slope=DX-2*trace(mul(residual(hR),residual(hsplit)),g0)
    check('boundary_gradient_slope',split_slope,Q(22,9))

    # One-variable exact Taylor derivatives of the equality polynomial at b0.
    bj=Jet({(0,0):b0,(1,0):1})
    fj=formal(bj)
    hb=sum(fj[2*i]*(r0**i) for i in range(5))
    kappa=hb.coefficient(1,0)
    hyy=sum(i*(i-1)*f0[2*i]*(r0**(i-2)) for i in range(2,5))
    check('formal_collision_derivatives',[kappa,hyy],[-Q(6655,309786624),Q(11,294)])
    check('y_cluster_discriminant_slope',-8*kappa/hyy,Q(605,131712))
    kb=-kappa/(2*r0*hyy)
    check('root_cluster_split_b_response',kb,Q(55,37632))
    kR=kb*Q(5,18)
    check('root_cluster_split_R_response',kR,Q(275,677376))
    xformal=powers(formal(bj),4)[4]
    xfr=xformal.coefficient(1,0)*Q(5,18)
    check('formal_X_response',xfr,Q(625,108864))
    gamma=(xfr-xr)/2
    check('formal_value_gap_coefficient',gamma,Q(3025,3048192))
    check('gap_gradient_consistency',gamma/kR,split_slope)

    b3=-Q(8,3);r3=Q(9,56);t3=Q(1,56)
    f3=mul(mul(mul([-r3,0,1],[-r3,0,1]),[-r3,0,1]),[-t3,0,1])
    check('further_equality_factorization',formal(b3),f3)
    check('further_equality_ODE',L(f3,b3),[0])
    weights=[Q(3,7),Q(2,7),Q(2,7),0,0,0,0]
    check('further_point_X_eta',[powers(f3,4)[4],sum(c*c for c in weights)],
          [Q(61,392),Q(17,49)])
    check('further_point_parameter',2*b3-b3*b3/2,-Q(80,9))

    # Clear all denominators in the leading-coefficient-root evaluation (28).
    B=Poly2({(1,0):1});Y=(4-3*B)
    denominator=Q(11239424)*(2-B)*(4-B)
    cleared_h=[15*Y**3, -15*Y**2*Q(896),15*Y*Q(25088)*(4-B),
               -denominator/2,denominator]
    left=sum(c*(-Y)**i*(28*B)**(4-i) for i,c in enumerate(cleared_h))
    # left = (28 b)^4 * denominator * f_b(L_b).
    right=Y**3*(7*B+8)*(5*B+8)*(3*B+8)*(B+8)*Q(28**4,7)
    check('full_collision_evaluation_identity',left,right)
    return records


def damaged_checks():
    failures=0
    damaged=profile(Q(11,56),Q(11,9408))
    damaged[6]+=Q(1,1024)
    H=[[-Q(73344,125),-Q(1064448,125)],
       [-Q(1064448,125),-Q(24385536,125)]]
    bad_response=[Q(25,6047),-Q(25,124416)]
    xgrad=[24*Q(11,56)-4,-Q(4)]
    controls=[lambda: require(powers(damaged,2)[2]==1,'damaged normalization'),
              lambda: require(all(sum(a*b for a,b in zip(row,bad_response))+c==0
                                  for row,c in zip(H,xgrad)), 'damaged response'),
              lambda: require(Q(3025,3048192)/Q(275,677376)==-Q(22,9),
                              'damaged constraint sign'),
              lambda: inverse([0],[0,1])]
    for control in controls:
        try:
            control()
        except ValueError:
            failures+=1
    require(failures==len(controls),'corruption control unexpectedly passed')
    return failures


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected',action='store_true',help='maintainer fixture update')
    args=parser.parse_args()
    records=verify()
    serialized=json.dumps(records,sort_keys=True,separators=(',',':'))
    digest=hashlib.sha256(serialized.encode()).hexdigest()
    if args.write_expected:
        args.expected.write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
    require(json.loads(args.expected.read_text())==records,'exact expected fixture differs')
    damage=damaged_checks()
    print(json.dumps({'status':'all exact checks passed','checks':len(records),
                      'damage_controls':damage,'record_sha256':digest},sort_keys=True))


if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,json.JSONDecodeError) as error:
        print('verification failed: '+str(error),file=sys.stderr)
        raise SystemExit(1)
