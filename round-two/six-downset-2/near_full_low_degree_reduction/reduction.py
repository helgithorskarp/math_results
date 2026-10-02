"""All-order near-cube low-degree cap reduction; six-downset-2, researcher.

The universal proof is PROOF.md; finite identity controls are validation.
All arithmetic here is rational. The independent complete reference model
and PSD engines retain the credits of the public 9592/9556/9521/9017 packets.
"""
from fractions import Fraction as Q
from math import comb


def need(condition, message):
    if not condition:
        raise ValueError(message)


def binomial(a, b):
    need(type(a) is int and a >= 0, "Nonnegative binomial upper index")
    return comb(a, b) if 0 <= b <= a else 0


def domain(n, k):
    need(type(n) is int and n >= 6, "Original near-cube n>=6")
    need(type(k) is int and 1 <= k <= n-2, "Integer cutoff 1..n-2")
    d = n//2
    q = min(d, max(k, 3 if n % 2 == 0 else 2))
    return n-2, 2**n-n-1, 2**(n-1)-n, d, q


def supported(n):
    return [(a, b) for a in range(1, n-1)
            for b in range(a, min(n-2, n-a)+1)]


def dimensions(n, k):
    r, N, s, d, q = domain(n, k)
    pairs = supported(n)
    free = [p for p in pairs if p[0] >= 2]
    excluded = [p for p in free if p[0] > k and sum(p) < n]
    t = max(d-k, 0)
    closed_excluded = t*(t-1) if n % 2 == 0 else t*t
    need(len(pairs) == n*n//4-1 and len(free) == (n-2)**2//4,
         "All supported and star-only free coordinates")
    need(len(excluded) == closed_excluded, "Closed excluded-coordinate count")
    return {"n": n, "k": k, "q": q, "supported": len(pairs),
            "star_rank": r, "free": len(free), "excluded": len(excluded),
            "active": len(free)-len(excluded),
            "lower_degrees": list(range(q+1)),
            "upper_degrees": list(range(min(k, d)+1))}


def table(n):
    return [[Q(0)]*(n-1) for _ in range(n-1)]


def validate(n, k, beta):
    r, N, s, d, q = domain(n, k)
    need(len(beta) == r+1 and all(len(row) == r+1 for row in beta),
         "Complete beta shape")
    for a in range(r+1):
        for b in range(r+1):
            v = beta[a][b]
            need(type(v) is Q and v == beta[b][a], "Exact symmetric coordinates")
            if min(a, b) == 0 or a+b > n or (min(a, b) > k and a+b < n):
                need(v == 0, "Supported S_k table")


def complete_stars(n, values):
    """Credited9365 star completion, implemented directly with its identity."""
    r, N, s, d, q = domain(n, 1)
    free = [p for p in supported(n) if p[0] >= 2]
    need(len(values) == len(free) and all(type(v) is Q for v in values),
         "Entire exact star-only free face")
    beta = table(n)
    for (a, b), v in zip(free, values):
        beta[a][b] = beta[b][a] = v
    for a in range(2, r+1):
        beta[1][a] = beta[a][1] = (Q((n-a)*s)-sum(
            b*beta[a][b]*binomial(n-a, b) for b in range(2, r+1)))/(n-a)
    beta[1][1] = (Q((n-1)*s)-sum(
        b*beta[1][b]*binomial(n-1, b) for b in range(2, r+1)))/(n-1)
    need(all(sum(b*beta[a][b]*binomial(n-a, b) for b in range(1, r+1))
             == (n-a)*s for a in range(1, r+1)), "Every original star moment")
    return beta


def quotient(n, j, beta):
    """Independent full coefficient formula; G is the physical norm metric."""
    r, N, s, d, q = domain(n, 1)
    need(type(j) is int and 0 <= j <= d, "Entire harmonic degree domain")
    aa = list(range(max(1, j), min(r, n-j)+1))
    g = [comb(n-2*j, a-j) for a in aa]
    K, U = [], []
    for a in aa:
        row_k, row_u = [], []
        for b in aa:
            z = (-1)**j*beta[a][b]*binomial(n-a-j, b-j)
            const = Q(comb(n, b)) if j == 0 else Q(0)
            v = Q(s*int(a == b))-const+z
            row_k.append(v)
            row_u.append(Q(N*int(a == b))-const-v)
        K.append(row_k)
        U.append(row_u)
    return aa, g, K, U


def parent(n, j):
    """Parent degree and rational orthogonal signs for omitted sectors."""
    if n % 2 == 0:
        return 2+(j % 2), lambda a: 1
    return 2, lambda a: -1 if j % 2 and 2*a > n else 1


def transfer(n, k, beta):
    """Entry-level control of EVERY omitted physical block, without radicals.

    On each surviving complementary pair both low and high metrics have
    equal two entries. Consequently the orthonormal block entries equal
    the rational quotient entries. Every other off-diagonal entry is zero.
    This checks both facts rather than treating an unweighted quotient as
    the physical form in general.
    """
    validate(n, k, beta)
    r, N, s, d, q = domain(n, k)
    positions, degrees, midpoint_parities = 0, [], []
    for j in range(q+1, d+1):
        aa, g, K, U = quotient(n, j, beta)
        ell, signs = parent(n, j)
        bb, low_g, low_K, low_U = quotient(n, ell, beta)
        ids = [bb.index(a) for a in aa]
        need(ell <= q and all(a > k for a in aa), "Retained parent and support")
        for i, a in enumerate(aa):
            for t, b in enumerate(aa):
                ii, tt = ids[i], ids[t]
                diagonal = int(i == t)
                z = Q((-1)**j)*beta[a][b] if a+b == n else Q(0)
                need(K[i][t] == Q(s*diagonal)+z
                     and U[i][t] == Q((N-s)*diagonal)-z,
                     "Complete complementary-only higher block")
                if a != b and (K[i][t] or U[i][t]):
                    need(a+b == n and g[i] == g[t] and low_g[ii] == low_g[tt],
                         "Both physical metrics have equal complementary norms")
                need(K[i][t] == signs(a)*signs(b)*low_K[ii][tt]
                     and U[i][t] == signs(a)*signs(b)*low_U[ii][tt],
                     "Entire signed physical principal-submatrix identity")
                positions += 2
        if n % 2 == 0:
            midpoint_parities.append(j % 2)
        degrees.append([j, ell, len(aa)])
    return {"n": n, "k": k, "q": q, "positions": positions,
            "omitted_degree_parent_order": degrees,
            "middle_parities": sorted(set(midpoint_parities))}
