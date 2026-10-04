"""Separate exact SymPy ring/subset determinant proof computation.

Direct affine substitution on all three boxes, without native de Casteljau
or native determinant imports. Shared module provides serialization only.
Requires SymPy 1.14.0. All coefficients are QQ, characteristic zero.
"""
from pathlib import Path
from math import comb
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from record_io import emit, require, rows
import sympy as sp
from sympy.polys.rings import ring


def compute():
    require(sp.__version__ == "1.14.0", "pinned exact CAS version")
    U, y, k = ring("y,k", sp.QQ)
    require((1-k+k*k)**2-4*(y+k*k)*(1-y-k) == (y+k*k-(1-y-k))**2,
            "entire root-gap square identity")
    require(1-(1-k+k*k)**2 == k*(1-k)*(2-k+k*k), "entire root-gap endpoint identity")
    M, a, D, u, z = ring("a,D,u,z", sp.QQ)
    A, E = a*a, sp.QQ(3, 64)-D/8
    q = z**4+(2*A-sp.QQ(1, 2))*z*z+3*A*A-A+2*E
    Q = (z+a)**2*q+4*u
    f = (z-a)**2*Q
    H = f.diff(z).exquo(8*(z-a))
    require(f == (z*z-A)**2*q+4*u*(z-a)**2, "entire original factorization")
    require(H == z*(z+a)*(z**4+(A-sp.QQ(3, 8))*z*z+A*A-3*A/8+E)+u,
            "entire derivative quotient")
    r = 8*z*H-8*(z-a)*Q
    require(r.degree(z) == 5, "whole residue numerator degree")
    def zc(poly, i):
        return M.from_dict({(*m[:3], 0): c for m, c in poly.items() if m[3] == i})
    require(zc(r, 5) == M.one, "entire leading-one residue numerator")
    fc = [zc(f, 8-i) for i in range(9)]
    moments = [M(8)]
    for n in range(1, 6):
        moments.append(-sum((fc[i]*moments[n-i] for i in range(1, n)), M.zero)-n*fc[n])
    require(moments[1] == moments[3] == moments[5] == M.zero, "all original odd moments")
    require(moments[2] == M.one and moments[4] == sp.QQ(1, 8)+D, "whole original norm and excess")
    R, aa, DD, uu = ring("a,D,u", sp.QQ)
    def scalar(poly):
        require(all(m[3] == 0 for m in poly), "no z in scalar coefficient")
        return R.from_dict({m[:3]: c for m, c in poly.items()})
    hc = [scalar(zc(H, i)) for i in range(7)]
    rc = [scalar(zc(r, i)) for i in range(6)] + [R.zero]
    gc = [(i+1)*hc[i+1] for i in range(6)] + [R.zero]
    def bez(g):
        B = [[R.zero for _ in range(6)] for _ in range(6)]
        for i in range(1, 7):
            for j in range(i):
                v = hc[i]*g[j]-hc[j]*g[i]
                for k2 in range(i-j):
                    B[i-1-k2][j+k2] += v
        require(all(B[i][j] == B[j][i] for i in range(6) for j in range(6)), "whole Bezout symmetry")
        return B
    B0, B1 = bez(gc), bez(rc)
    dp = {0: (R.one, R.zero, R.zero)}
    for row in range(6):
        nxt = {}
        for mask, old in dp.items():
            for j in range(6):
                if (mask >> j) & 1: continue
                sign = -1 if (mask >> (j+1)).bit_count() % 2 else 1
                x, y2 = B0[row][j], B1[row][j]
                values = (sign*old[0]*x, sign*(old[1]*x+old[0]*y2),
                          sign*(old[2]*x+old[1]*y2))
                key = mask | (1 << j)
                previous = nxt.get(key, (R.zero, R.zero, R.zero))
                nxt[key] = tuple(previous[i]+values[i] for i in range(3))
        dp = nxt
    delta, d1, N = dp[63]
    require(d1 == delta, "entire sum-one coefficient")
    S, XA, XD, XU = ring("A,D,u", sp.QQ)
    def even(poly):
        require(all(m[0] % 2 == 0 for m in poly), "complete reflection parity")
        return S.from_dict({(m[0]//2, m[1], m[2]): c for m, c in poly.items()})
    de, en = even(delta), even(N)
    P = 47*XD*de-4*en
    require(de.degree(XU) == en.degree(XU) == 5, "whole u degrees")
    T, qv, t, v = ring("q,t,v", sp.QQ)
    A2 = sp.QQ(1, 8)+qv*t
    D2, d, ell = 24*qv*qv, 6*qv*qv*(1-t*t), 2*qv*qv*(3+5*t*t)
    qlo, qhi = sp.QQ(1, 133), sp.QQ(1, 26)
    mid = (qlo+qhi)/2
    require(qlo*qlo < sp.QQ(1, 17496) and qhi*qhi > sp.QQ(5, 3384), "whole D-band enclosure")
    require(24*qhi*qhi < sp.QQ(1, 25) and sp.QQ(5, 141) < sp.QQ(1, 25), "root-distance license")
    require(sp.QQ(5, 6)/sp.QQ(5, 141) == sp.QQ(47, 2), "six-mass Cauchy endpoint")
    def substitute(poly, index, lo, hi):
        grouped = {}
        for m, c in poly.items():
            n = list(m)
            degree = n[index]
            n[index] = 0
            grouped.setdefault(degree, T.zero)[tuple(n)] = c
        gen = [qv, t, v][index]
        ans = T.zero
        for n in range(max(grouped, default=0), -1, -1):
            ans = ans*(lo+(hi-lo)*gen)+grouped.get(n, T.zero)
        return ans
    def transform(poly, degrees, reverse=False):
        result = dict(poly.items())
        for axis, n in enumerate(degrees):
            groups = {}
            for m, c in result.items():
                base = list(m)
                i = base[axis]
                base[axis] = 0
                groups.setdefault(tuple(base), {})[i] = c
            new = {}
            for base, coefficients in groups.items():
                for k2 in range(n+1):
                    if reverse:
                        c = comb(n, k2)*sum(((-1)**(k2-i)*comb(k2, i)*c
                                            for i, c in coefficients.items() if i <= k2), sp.QQ.zero)
                    else:
                        c = sum((sp.QQ(comb(k2, i), comb(n, i))*c
                                 for i, c in coefficients.items() if i <= k2), sp.QQ.zero)
                    if c:
                        m = list(base)
                        m[axis] = k2
                        new[tuple(m)] = c
            result = new
        return T.from_dict(result)
    parents, leaves = [], []
    for label, kappa, tlo, thi in [("negative", 32, -1, 0), ("positive", 64, 0, 1)]:
        den = kappa*A2*ell
        cleared = T.zero
        for (i, j, k2), c in P.items():
            cleared += c*A2**i*D2**j*den**(5-k2)*d**(3*k2)*v**k2
        require(min(m[0] for m in cleared) == 20, "whole q factor")
        reduced = cleared.exquo(qv**20*(1-t*t)**2)
        require(cleared == reduced*qv**20*(1-t*t)**2, "entire cap factorization")
        parents.append({"label": label, "kappa": kappa,
                        "cleared": rows(cleared), "reduced": rows(reduced)})
        boxes = [("negative", qlo, qhi)] if label == "negative" else [
            ("positive-left", qlo, mid), ("positive-right", mid, qhi)]
        for name, lo, hi in boxes:
            b = substitute(substitute(reduced, 0, lo, hi), 1, sp.QQ(tlo), sp.QQ(thi))
            degrees = [b.degree(g) for g in [qv, t, v]]
            require(degrees == [12, 28, 5], "whole tensor degrees")
            c = transform(b, degrees)
            require(transform(c, degrees, True) == b, "entire reverse tensor identity")
            leaves.append({"label": name, "kappa": kappa, "q_bounds": [str(lo), str(hi)],
                           "t_bounds": [str(tlo), str(thi)], "degrees": degrees,
                           "box": rows(b), "controls": rows(c)})
    model = {"f": rows(f), "H": rows(H), "r": rows(r), "moments": [rows(p) for p in moments],
             "B0": [[rows(p) for p in line] for line in B0],
             "B1": [[rows(p) for p in line] for line in B1]}
    return {"domain": "QQ[a,D,u,z]; QQ[A,D,u]; QQ[q,t,v]; characteristic zero",
            "model": model, "Delta": rows(de), "N": rows(en), "P": rows(P),
            "parents": parents, "leaves": leaves}


if __name__ == "__main__":
    emit(compute())
