"""Explicit rational core for the precisely stated sufficient deletion region."""
import bootstrap
from fractions import Fraction as F
from itertools import combinations
from model import formula
from floor import cap_parameters
from exact import require


def parameter(q, k):
    require(type(q) is type(k) is int and q >= 4 and 1 <= k <= q,
            'require literal integers q>=4 and 1<=k<=q')


def scalar(q, k, require_cap=True):
    parameter(q, k)
    n, s, chi, gamma = cap_parameters(F(q), k)
    require(n.denominator == 1, 'nonintegral family size')
    if require_cap:
        require(chi > 0, 'sufficient cap condition chi>0 is not met; no H nonexistence conclusion')
    return {'q': q, 'k': k, 'N': int(n), 's': int(s), 'chi': chi, 'gamma': gamma,
            't': min(F(1, 48), gamma/4) if chi > 0 else None}


def literal_base(q):
    parameter(q, 1)
    domain = [0]+sorted(sum(1 << i for i in t) for size in [1, 2, 3]
                        for t in combinations(range(q+3), size)
                        if size < 3 or sum(i < 3 for i in t) >= 2)
    weights = {key: F(v) for key, v in formula(F(q)).items()}
    typ = lambda a: ((a & 7).bit_count(), (a >> 3).bit_count())
    s = 3*q+4
    c = [[F(s-1) if a == b else F(-1) if a & b else weights[tuple(sorted((typ(a), typ(b))))]-1
          for b in domain[1:]] for a in domain[1:]]
    families = [[F(int(a >> i & 1)) for a in domain[1:]] for i in range(3)]
    families.append([F(int(a.bit_count() == 3 or (a.bit_count() == 2 and a & 7 == a))) for a in domain[1:]])
    return domain, c, families


def restricted(q, k):
    parameter(q, k)
    domain, old, families = literal_base(q)
    deleted = {6 | (1 << i) for i in range(3, 3+k)}
    keep = [i for i, a in enumerate(domain[1:]) if a not in deleted]
    remaining = [0]+[domain[i+1] for i in keep]
    c = [[old[i][j] for j in keep] for i in keep]
    fam = [[v[i] for i in keep] for v in families]
    return remaining, c, fam, (domain, old, families, keep)


def trade(domain):
    n = len(domain)-1
    index = {a: i for i, a in enumerate(domain[1:])}
    r = [[F(0)]*n for _ in range(n)]
    for a, b, v in [(1, 2, 1), (1, 4, 1), (2, 5, -1), (4, 3, -1)]:
        require(a in index and b in index and not a & b, 'four-edge trade domain/support differs')
        i, j = index[a], index[b]
        r[i][j] = r[j][i] = F(v)
    def point(a):
        return [F(int(x == a)) for x in domain[1:]]
    a, b, c, ab, ac = map(point, [1, 2, 4, 3, 5])
    ell = [[x-y+z for x, y, z in zip(b, a, ac)], [x-y+z for x, y, z in zip(c, a, ab)]]
    positive = [[x+y-z for x, y, z in zip(b, a, ac)], [x+y-z for x, y, z in zip(c, a, ab)]]
    require(all(r[i][j] == sum((v[i]*v[j]-w[i]*w[j])/2 for v, w in zip(positive, ell))
                for i in range(n) for j in range(n)), 'four-edge PSD split differs')
    return r, ell, positive


def construct(q, k):
    info = scalar(q, k)
    domain, core, families, _ = restricted(q, k)
    r, _, _ = trade(domain)
    repaired = [[core[i][j]+info['t']*r[i][j] for j in range(len(core))] for i in range(len(core))]
    return info, domain, families[0], repaired


def template_rayleigh(q, k):
    info = scalar(q, k, require_cap=False)
    q0 = F(q); c = F(1, 2)
    alpha = q0*(q0+1)/2+3*(q0+1)/(3*q0+5)
    h = 1/(3*q0+5)
    return info['N']-1-c*alpha+2*k*c*h-k*(info['s']-k)
