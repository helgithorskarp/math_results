from fractions import Fraction as Q
from algebra import F,C

def require(ok,label):
 if not ok: raise ValueError(label)

def equal(a,b,label):
 require(a==b,label)

def cube_coordinates(v):
    """Recover and check all 12 coordinates in the subfield Q[c]."""
    columns = [F(1), C, C*C]
    a = [[x.v[j] for x in columns]+[v.v[j]] for j in range(12)]
    row = 0
    for k in range(3):
        p = next(j for j in range(row, 12) if a[j][k])
        a[row], a[p] = a[p], a[row]
        d = a[row][k]
        a[row] = [x/d for x in a[row]]
        for j in range(12):
            if j != row and a[j][k]:
                d = a[j][k]
                a[j] = [x-d*y for x, y in zip(a[j], a[row])]
        row += 1
    q = [a[k][3] for k in range(3)]
    equal(sum((columns[k]*q[k] for k in range(3)), F()), v,
          'complete cubic-subfield reconstruction')
    return q


def physical_interval():
    lo, hi = Q(15, 16), Q(47, 50)
    f = lambda t: 8*t**3-6*t-1
    require(f(lo) < 0 < f(hi) and lo > Q(1, 2), 'initial root bracket')
    for _ in range(48):
        mid = (lo+hi)/2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, hi


def bound(v):
    q = cube_coordinates(v)
    lo, hi = physical_interval()
    a = b = Q(0)
    for j, x in enumerate(q):
        u, t = x*lo**j, x*hi**j
        a += min(u, t)
        b += max(u, t)
    return a, b


def ratio(q):
    return [q.numerator, q.denominator]
