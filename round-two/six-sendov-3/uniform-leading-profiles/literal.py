"""Credited generic eight-factor fourth jet from8619/f8df996d; finite replay.
Actual six-sendov-3 / researcher. Kernel unchanged; no independent backend claim.
"""
from fractions import Fraction as F
from hashlib import sha256
import json
from arithmetic import need as require
# Gaussian-rational sparse jets: epsilon, z, seven free balanced h,
# and eight free coordinates in each of u, v, w.
NV = 33
ORDER = 4
ZERO_EXP = (0,)*NV


def gadd(a, b):
    return a[0]+b[0], a[1]+b[1]


def gmul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def pc(v=0, imag=0):
    v = F(v), F(imag)
    return {ZERO_EXP: v} if v != (0, 0) else {}


def pv(i):
    a = [0]*NV
    a[i] = 1
    return {tuple(a): (F(1), F(0))}


def padd(*ps):
    ans = {}
    for p in ps:
        for e, v in p.items():
            ans[e] = gadd(ans.get(e, (F(0), F(0))), v)
            if ans[e] == (0, 0):
                del ans[e]
    return ans


def pscale(p, real=1, imag=0):
    return {e: w for e, v in p.items()
            if (w := gmul(v, (F(real), F(imag)))) != (0, 0)}


def pmul(*ps):
    ans = pc(1)
    for p in ps:
        new = {}
        for e, v in ans.items():
            for f, w in p.items():
                if e[0]+f[0] > ORDER:
                    continue
                key = tuple(a+b for a, b in zip(e, f))
                new[key] = gadd(new.get(key, (F(0), F(0))), gmul(v, w))
                if new[key] == (0, 0):
                    del new[key]
        ans = new
    return ans


def ppow(p, n):
    return pmul(*([p]*n))


def pdiff(p, i):
    ans = {}
    for e, v in p.items():
        if e[i]:
            f = list(e)
            f[i] -= 1
            ans[tuple(f)] = gmul(v, (F(e[i]), F(0)))
    return ans


def pint(p, i):
    ans = {}
    for e, v in p.items():
        f = list(e)
        f[i] += 1
        ans[tuple(f)] = gmul(v, (F(1, f[i]), F(0)))
    return ans


def psubst(p, i, replacement):
    ans = {}
    for e, v in p.items():
        f = list(e)
        power = f[i]
        f[i] = 0
        ans = padd(ans, pmul({tuple(f): v}, ppow(replacement, power)))
    return ans


def precord(p):
    return [[list(e), str(v[0]), str(v[1])] for e, v in sorted(p.items())]


def phash(p):
    raw = json.dumps(precord(p), separators=(',', ':')).encode()
    return sha256(raw).hexdigest()
