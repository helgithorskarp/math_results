"""Definition-level Fraction/Berkowitz proof computation, with no CAS dependency.

Complete original model and determinant; binomial cap expansion; de Casteljau
subdivision; exact reverse tensor reconstruction. Same-author validation,
not independent review. Python 3.11+; all arithmetic is exact.
"""
from pathlib import Path
from fractions import Fraction as F
from math import comb, lcm
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from record_io import emit, require, rows

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
    model = {"f": rows(f), "H": rows(H), "r": rows(r),
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


def bisect_q(controls, degrees):
    n = degrees[0]
    groups = {}
    for (i, j, k), c in controls.items():
        groups.setdefault((j, k), {})[i] = c
    left, right = {}, {}
    for (j, k), coefficients in groups.items():
        line = [coefficients.get(i, F(0)) for i in range(n+1)]
        L, R = [line[0]], [line[-1]]
        for _ in range(n):
            line = [(line[i]+line[i+1])/2 for i in range(len(line)-1)]
            L.append(line[0])
            R.append(line[-1])
        R.reverse()
        for i in range(n+1):
            if L[i]: left[(i, j, k)] = L[i]
            if R[i]: right[(i, j, k)] = R[i]
    return left, right


def clear_cap(P, kappa):
    # Binomial expansion independent of the CAS polynomial composition.
    out = {}
    for (i, j, k), c in P.items():
        n = i+5-k
        scalar = c*(2*kappa)**(5-k)*24**j*6**(3*k)
        for r in range(n+1):
            ca = comb(n, r)*F(1, 8)**(n-r)
            for b in range(6-k):
                cb = comb(5-k, b)*3**(5-k-b)*5**b
                for e in range(3*k+1):
                    m = (10+2*j+4*k+r, r+2*b+2*e, k)
                    out[m] = out.get(m, F(0))+scalar*ca*cb*comb(3*k, e)*(-1)**e
    out = {m: c for m, c in out.items() if c}
    require(min(m[0] for m in out) == 20, "exact q common factor")
    shifted = {(m[0]-20, m[1], m[2]): c for m, c in out.items()}
    groups = {}
    for (i, j, k), c in shifted.items():
        groups.setdefault((i, k), {})[j] = c
    reduced = {}
    for (i, k), poly in groups.items():
        remainder = dict(poly)
        while remainder and max(remainder) >= 4:
            degree = max(remainder)
            c = remainder[degree]
            reduced[(i, degree-4, k)] = c
            for d, v in [(0, 1), (2, -2), (4, 1)]:
                ix = degree-4+d
                remainder[ix] = remainder.get(ix, F(0))-c*v
                if not remainder[ix]: del remainder[ix]
        require(not remainder, "whole (1-t^2)^2 exact division")
    reconstructed = {}
    for (i, j, k), c in reduced.items():
        for d, v in [(0, 1), (2, -2), (4, 1)]:
            m = (i+20, j+d, k)
            reconstructed[m] = reconstructed.get(m, F(0))+c*v
    require({m: c for m, c in reconstructed.items() if c} == out, "entire cap factor identity")
    return out, reduced


def compute():
    y, k = {(1, 0, 0, 0): 1}, {(0, 1, 0, 0): 1}
    l = add(ONE, scale(k, -1), power(k, 2))
    g = add(ONE, scale(y, -1), scale(k, -1))
    w = add(y, power(k, 2))
    require(add(power(l, 2), scale(mul(w, g), -4)) == power(add(w, scale(g, -1)), 2),
            "entire root-gap square identity")
    require(add(ONE, scale(power(l, 2), -1)) ==
            mul(mul(k, add(ONE, scale(k, -1))), add(const(2), scale(k, -1), power(k, 2))),
            "entire root-gap endpoint identity")
    model, de, en, P = original_maps()
    qlo, qhi = F(1, 133), F(1, 26)
    mid = (qlo+qhi)/2
    require(qlo*qlo < F(1, 17496) and qhi*qhi > F(5, 3384), "rational full D-band enclosure")
    require(24*qhi*qhi < F(1, 25) and F(5, 141) < F(1, 25), "negative cap root-distance license")
    require(F(5, 6)/F(5, 141) == F(47, 2), "six-full-mass Cauchy band")
    parents, leaves = [], []
    for label, kappa, tlo, thi in [("negative", 32, F(-1), F(0)),
                                   ("positive", 64, F(0), F(1))]:
        cleared, reduced = clear_cap(P, kappa)
        box = affine(affine(reduced, 0, qlo, qhi), 1, tlo, thi)
        deg = [max(m[i] for m in box) for i in range(3)]
        require(deg == [12, 28, 5], "entire reduced tensor degrees")
        ctrl = tensor_transform(box, deg)
        require(tensor_transform(ctrl, deg, True) == box, "entire parent tensor reverse identity")
        parents.append({"label": label, "kappa": kappa,
                        "cleared": rows(cleared), "reduced": rows(reduced)})
        sub = [(label, qlo, qhi, box, ctrl)] if label == "negative" else [
            ("positive-left", qlo, mid, affine(box, 0, F(0), F(1, 2)), bisect_q(ctrl, deg)[0]),
            ("positive-right", mid, qhi, affine(box, 0, F(1, 2), F(1)), bisect_q(ctrl, deg)[1])]
        for name, lo, hi, b, c in sub:
            require(tensor_transform(c, deg, True) == b, "entire leaf reverse identity")
            leaves.append({"label": name, "kappa": kappa, "q_bounds": [str(lo), str(hi)],
                           "t_bounds": [str(tlo), str(thi)], "degrees": deg,
                           "box": rows(b), "controls": rows(c)})
    return {"domain": "QQ[a,D,u,z]; QQ[A,D,u]; QQ[q,t,v]; characteristic zero",
            "model": model, "Delta": rows(de), "N": rows(en), "P": rows(P),
            "parents": parents, "leaves": leaves}


if __name__ == "__main__":
    emit(compute())
