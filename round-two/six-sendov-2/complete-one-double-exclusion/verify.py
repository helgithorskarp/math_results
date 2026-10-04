"""Definition-level Fraction/Berkowitz proof computation, with no CAS dependency.

Complete original model and determinant; NEW positive-q0 binomial caps;
exact reverse tensor reconstruction and original critical-quartic coverage. Same-author validation,
not independent review. Python 3.11+; all arithmetic is exact.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, lcm
from itertools import permutations
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from record_io import emit, require, rows, partitions

ZERO = {}
ONE = {(0, 0, 0, 0): 1}


def add(*polys):
    out = {}
    for p in polys:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return {m: c for m, c in out.items() if c}


def scale(p, c):
    return {m: v * c for m, v in p.items() if v * c}


def mul(p, q, jet=False):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            if jet and m[3] + n[3] > 2:
                continue
            k = tuple(m[i] + n[i] for i in range(4))
            out[k] = out.get(k, 0) + c * d
    return {m: c for m, c in out.items() if c}


def power(p, n):
    out = ONE
    for _ in range(n):
        out = mul(out, p)
    return out


def const(c):
    return scale(ONE, F(c))


def derivative(p, axis):
    out = {}
    for m, c in p.items():
        if m[axis]:
            n = list(m)
            n[axis] -= 1
            out[tuple(n)] = c * m[axis]
    return out


def zcoeff(p, i):
    return {(*m[:3], 0): c for m, c in p.items() if m[3] == i}


def short(p):
    require(all(m[3] == 0 for m in p), "scalar coefficient has no z")
    return {m[:3]: c for m, c in p.items()}


def even(p):
    require(all(m[0] % 2 == 0 and m[3] == 0 for m in p), "complete reflection parity")
    return {(m[0] // 2, m[1], m[2]): c for m, c in p.items()}


def original_maps():
    a = {(1, 0, 0, 0): F(1)}
    D = {(0, 1, 0, 0): F(1)}
    u = {(0, 0, 1, 0): F(1)}
    z = {(0, 0, 0, 1): F(1)}
    A = mul(a, a)
    E = add(const(F(3, 64)), scale(D, F(-1, 8)))
    q = add(power(z, 4), mul(add(scale(A, 2), const(F(-1, 2))), power(z, 2)),
            scale(power(A, 2), 3), scale(A, -1), scale(E, 2))
    k = add(power(z, 4), mul(add(A, const(F(-3, 8))), power(z, 2)),
            power(A, 2), scale(A, F(-3, 8)), E)
    Q = add(mul(power(add(z, a), 2), q), scale(u, 4))
    H = add(mul(mul(z, add(z, a)), k), u)
    f = add(mul(power(add(power(z, 2), scale(A, -1)), 2), q),
            scale(mul(u, power(add(z, scale(a, -1)), 2)), 4))
    require(f == mul(power(add(z, scale(a, -1)), 2), Q), "entire original factorization")
    require(derivative(f, 3) == scale(mul(add(z, scale(a, -1)), H), 8),
            "entire original derivative factorization")
    r = add(scale(mul(z, H), 8), scale(mul(add(z, scale(a, -1)), Q), -8))
    require(max(m[3] for m in r) == 5, "entire degree-five residue numerator")
    require(zcoeff(r, 5) == ONE, "entire leading-one residue numerator")
    fc = [zcoeff(f, 8 - i) for i in range(9)]
    moments = [const(8)]
    for n in range(1, 6):
        moments.append(scale(add(*[mul(fc[i], moments[n-i]) for i in range(1, n)],
                                 scale(fc[n], n)), -1))
    require(moments[1] == moments[3] == moments[5] == ZERO, "all three zero odd moments")
    require(moments[2] == ONE, "original norm one")
    require(moments[4] == add(const(F(1, 8)), D), "entire fourth excess")
    T4 = add(scale(power(z, 4), 3), scale(mul(a, power(z, 3)), 2),
             scale(mul(add(scale(A, 2), const(F(-1, 2))), power(z, 2)), 2),
             mul(mul(a, add(scale(A, 2), const(F(-1, 2)))), z),
             scale(power(A, 2), 3), scale(A, -1), scale(E, 2))
    require(derivative(Q, 3) == scale(mul(add(z, a), T4), 2),
            "whole original critical quartic")
    tc = [scale(zcoeff(T4, 4-i), F(1, 3)) for i in range(5)]
    tp = [const(4)]
    for n in range(1, 7):
        pieces = [mul(tc[j], tp[n-j]) for j in range(1, min(n, 4)+1)]
        if n <= 4: pieces.append(scale(tc[n], n-4))
        tp.append(scale(add(*pieces), -1))
    def determinant_t(n):
        out = ZERO
        for perm in permutations(range(n)):
            sign = (-1)**sum(perm[i] > perm[j] for i in range(n) for j in range(i+1, n))
            term = const(sign)
            for i in range(n): term = mul(term, tp[i+perm[i]])
            out = add(out, term)
        return even(out)
    tminors = [determinant_t(n) for n in range(1, 5)]
    require(tminors[0] == {(0, 0, 0): F(4)}, "first whole critical Hermite minor")
    hc = [zcoeff(H, i) for i in range(7)]
    rc = [zcoeff(r, i) for i in range(6)] + [ZERO]
    gc = [scale(hc[i+1], i+1) for i in range(6)] + [ZERO]

    def bez(g):
        B = [[ZERO for _ in range(6)] for _ in range(6)]
        for i in range(1, 7):
            for j in range(i):
                v = add(mul(hc[i], g[j]), scale(mul(hc[j], g[i]), -1))
                for k2 in range(i-j):
                    B[i-1-k2][j+k2] = add(B[i-1-k2][j+k2], v)
        require(all(B[i][j] == B[j][i] for i in range(6) for j in range(6)),
                "whole Bezout symmetry")
        return B

    B0, B1 = bez(gc), bez(rc)
    L = 1
    for B in [B0, B1]:
        for line in B:
            for p in line:
                for c in p.values():
                    L = lcm(L, c.denominator)
    BB = []
    for i in range(6):
        line = []
        for j in range(6):
            p = {}
            for order, B in enumerate([B0, B1]):
                for m, c in B[i][j].items():
                    v = L * c
                    require(v.denominator == 1, "exact integer matrix clearing")
                    p[(*m[:3], order)] = v.numerator
            line.append(p)
        BB.append(line)
    # Principal-block characteristic recurrence, different from subset DP.
    char = [ONE]
    for start in range(5, -1, -1):
        n = 6-start
        tail = list(range(start+1, 6))
        tv = [ONE, scale(BB[start][start], -1)]
        if n >= 2:
            vec = [BB[i][start] for i in tail]
            for exponent in range(n-1):
                tv.append(scale(add(*[mul(BB[start][i], vec[j], True)
                                      for j, i in enumerate(tail)]), -1))
                if exponent < n-2:
                    vec = [add(*[mul(BB[i][j], vec[k], True)
                                 for k, j in enumerate(tail)]) for i in tail]
        char = [add(*[mul(tv[i-j], char[j], True)
                      for j in range(min(i, n-1)+1)]) for i in range(n+1)]
    parts = [{(*m[:3], 0): F(c, L**6) for m, c in char[6].items() if m[3] == j}
             for j in range(3)]
    require(parts[1] == parts[0], "entire sum-one mass coefficient")
    de, en = even(parts[0]), even(parts[2])
    P = even(add(scale(mul(D, parts[0]), 47), scale(parts[2], -4)))
    require(max(m[2] for m in de) == max(m[2] for m in en) == 5, "whole u degrees")
    model = {"f": rows(f), "Q": rows(Q), "H": rows(H), "r": rows(r),
             "T4": rows(T4), "T4_moments": [rows(p) for p in tp],
             "T4_Hermite_leading_minors": [rows(p) for p in tminors],
             "moments": [rows(p) for p in moments],
             "B0": [[rows(short(p)) for p in line] for line in B0],
             "B1": [[rows(short(p)) for p in line] for line in B1]}
    return model, de, en, P


def tensor_transform(poly, degrees, reverse=False):
    out = poly
    for axis, n in enumerate(degrees):
        groups = {}
        for m, c in out.items():
            base = list(m)
            i = base[axis]
            base[axis] = 0
            groups.setdefault(tuple(base), {})[i] = c
        new = {}
        for base, coefficients in groups.items():
            for k in range(n+1):
                if reverse:
                    c = comb(n, k) * sum(((-1)**(k-i)*comb(k, i)*v
                                          for i, v in coefficients.items() if i <= k), F(0))
                else:
                    c = sum((F(comb(k, i), comb(n, i))*v
                             for i, v in coefficients.items() if i <= k), F(0))
                if c:
                    m = list(base)
                    m[axis] = k
                    new[tuple(m)] = c
        out = new
    return out


def affine(poly, axis, lo, hi):
    out = {}
    for m, c in poly.items():
        for k in range(m[axis]+1):
            p = list(m)
            p[axis] = k
            p = tuple(p)
            out[p] = out.get(p, F(0)) + c*comb(m[axis], k)*lo**(m[axis]-k)*(hi-lo)**k
    return {m: c for m, c in out.items() if c}



def univariate_mul(p, q):
    out = {}
    for i, c in p.items():
        for j, d in q.items(): out[i+j] = out.get(i+j, F(0))+c*d
    return {i: c for i, c in out.items() if c}


def clear_positive_q0(P, side):
    eps, kappa = (1, 9) if side == "positive" else (-1, 16)
    A = {0: F(1, 8), 1: F(eps)}
    J = ({0: F(7, 48), 1: F(-3, 4), 2: F(-10, 3)} if side == "positive" else
         {0: F(59, 420), 1: F(-51, 35), 2: F(-4, 3)})
    # Binomial expansion is algebraically separate from CAS composition.
    # den^8*A^i*D^j*u^k expands into A^(i+8-k)*J^(8-l-m)
    # h^(2j+4k+2l+2m)*r^(l+m)*v^k with the scalar below.
    require(max(j+k for i,j,k in P) == 8, "whole joint D-u denominator degree")
    Ap = [{0: F(1)}]
    for _ in range(max(i+8-k for i,j,k in P)): Ap.append(univariate_mul(Ap[-1], A))
    Jp = [{0: F(1)}]
    for _ in range(8): Jp.append(univariate_mul(Jp[-1], J))
    cache = {}
    out = {}
    for (i,j,k), c in P.items():
        n = i+8-k
        for ell in range(j+1):
            for m in range(k+1):
                q = ell+m
                scalar = c*kappa**(8-k)*(-1)**(k+ell)*comb(j,ell)*comb(k,m)*8**(j-ell)*4**q
                key = (n,8-q)
                if key not in cache: cache[key] = univariate_mul(Ap[n], Jp[8-q])
                shift = 2*j+4*k+2*q
                for d, a in cache[key].items():
                    powers = (d+shift,q,k)
                    out[powers] = out.get(powers,F(0))+scalar*a
    out = {m:c for m,c in out.items()if c}
    require(min(m[0]for m in out) == 10, "entire h common factor")
    reduced = {(m[0]-10,m[1],m[2]):c for m,c in out.items()}
    require({(m[0]+10,m[1],m[2]):c for m,c in reduced.items()} == out,
            "entire positive-q0 factor identity")
    return {"label":side,"kappa":kappa,"denominator_power":8,"h_removed":10,
            "A":rows({(i,0,0):c for i,c in A.items()}),
            "J":rows({(i,0,0):c for i,c in J.items()}),
            "cleared":rows(out),"reduced":rows(reduced)}, reduced


def scalar_margins():
    q={}
    q["positive_A_ge_21_100"] = 2*(F(21,100)-F(1,8))**2-F(5,564)-F(1,1875)-F(4,1125)
    q["positive_A_ge_1_5"] = 8*F(3,40)**2-4*F(17,200)**4/F(104,1875)-F(5,141)
    q["positive_D_monotonic"] = 1-F(240,17)*F(3,40)**2
    q["positive_h_ge_17_250"] = 8*F(17,250)**2-F(960,17)*F(17,250)**4-F(5,141)
    q["h_low_enclosure"] = F(1,5000)-F(1,72)**2
    q["positive_J_box"] = F(7,48)-F(3,4)*F(17,250)-F(10,3)*F(17,250)**2
    for name,lo,hi in [("low",F(1,25),F(9,200)),("high",F(9,200),F(1,20))]:
        hhi,hlo = F(1,8)-lo,F(1,8)-hi
        ell = lo+(F(1,4)-lo)/3+F(18,175)
        J=ell*ell-4*hhi*hhi
        q["negative_J_"+name]=J
        q["negative_eJ_minus_h4_"+name]=(2*hlo*hlo-F(5,564))*J-hhi**4
    q["sqrt_AB_low"]=F(1,25)*F(21,100)-F(9,100)**2
    q["twice_inverse_sqrt3"]=F(7,4)**2-3
    q["sqrt_AB_high_positive_factor"]=F(1,5)-F(1,8)
    q["negative_J_min"]=F(59,420)-F(51,35)*F(3,40)-F(4,3)*F(3,40)**2
    q["negative_D_monotonic"]=1-F(8400,199)*F(3,40)**2
    q["negative_h_ge_71_1000"]=8*F(71,1000)**2-F(33600,199)*F(71,1000)**4-F(5,141)
    require(all(c>0 for c in q.values()), "all original-strip endpoint margins")
    return {k:str(c)for k,c in q.items()}


def compute():
    h={(1,0,0,0):F(1)};x={(0,1,0,0):F(1)}
    hx=mul(x,add(scale(h,2),scale(x,-1)))
    require(add(power(h,4),scale(power(hx,2),-1)) ==
            mul(power(add(h,scale(x,-1)),2),add(power(h,2),hx)),
            "whole original height numerator inequality")
    A=h;B=add(const(F(1,4)),scale(A,-1))
    require(add(mul(A,B),const(F(-1,100))) ==
            mul(add(A,const(F(-1,20))),add(const(F(1,5)),scale(A,-1))),
            "whole strict AB factor identity")
    require(add(mul(add(A,scale(B,3)),add(A,scale(B,F(4,3)))),
                scale(power(add(A,scale(B,-1)),2),-1)) ==
            mul(B,add(scale(A,F(19,3)),scale(B,3))),
            "whole positive J0 lower-bound identity")
    model,de,en,P=original_maps()
    margins=scalar_margins()
    # Entire quartic comes from the ORIGINAL Q derivative, not a table input.
    quartic={}
    for row in model["T4"]:
        a,D,u,z=row["powers"];c=F(row["coefficient"])
        require(u==0,"original critical quartic independent of shift")
        m=(a,z,0);quartic[m]=quartic.get(m,F(0))+c*F(5,141)**D*(-1)**z
    quartic={m:c for m,c in quartic.items()if c}
    require([max(m[i]for m in quartic)for i in range(3)] == [4,4,0],
            "whole negative critical quartic rectangle degree")
    leaves=[]
    for spec in partitions():
        box=quartic
        for axis,(lo,hi)in enumerate(spec["bounds"]):box=affine(box,axis,lo,hi)
        deg=[4,4,0];ctrl=tensor_transform(box,deg)
        require(tensor_transform(ctrl,deg,True)==box,"whole quartic reverse tensor identity")
        leaves.append({"label":spec["label"],"kind":"quartic","bounds":
                       [[str(lo),str(hi)]for lo,hi in spec["bounds"]],
                       "degrees":deg,"box":rows(box),"controls":rows(ctrl)})
    parents=[]
    for side,hi in [("positive",F(17,250)),("negative",F(71,1000))]:
        parent,reduced=clear_positive_q0(P,side);parents.append(parent)
        lo=F(1,72);box=affine(reduced,0,lo,hi)
        deg=[max(m[i]for m in box)for i in range(3)]
        require(deg==[31,8,5],"whole positive-q0 cap tensor degrees")
        ctrl=tensor_transform(box,deg)
        require(tensor_transform(ctrl,deg,True)==box,"whole cap reverse tensor identity")
        leaves.append({"label":side,"kind":"cap","bounds":[[str(lo),str(hi)],["0","1"],["0","1"]],
                       "degrees":deg,"box":rows(box),"controls":rows(ctrl)})
    return {"domain":"QQ[a,D,u,z]; QQ[A,D,u]; QQ[h,r,v]; characteristic zero",
            "model":model,"Delta":rows(de),"N":rows(en),"P":rows(P),
            "scalar_margins":margins,"negative_quartic":rows(quartic),
            "parents":parents,"leaves":leaves}


if __name__ == "__main__": emit(compute())
