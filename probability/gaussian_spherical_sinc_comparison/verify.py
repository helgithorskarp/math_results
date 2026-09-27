#!/usr/bin/env python3
"""Exact finite audits; the universal theorem is proved in PROOF.md.

No solver, floating point, external package, or teammate implementation is
used. These checks are not a formalization or an independent review.
"""
from fractions import Fraction as F
from math import comb, factorial
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def require_contraction_loss(loss):
    require(loss >= 0, "expanding pair is not a contraction")


def sphere_power_difference(n, a, b, c, t, dimension=3):
    """E(c+t*sqrt(a)*U)^n-E(c+t*sqrt(b)*U)^n, U a sphere coordinate."""
    ans, moment = F(0), F(1)
    for k in range(n // 2 + 1):
        if k:
            moment *= F(2*k-1, dimension+2*k-2)
        ans += comb(n, 2*k)*c**(n-2*k)*t**(2*k)*(a**k-b**k)*moment
    return ans


def integral_of_second_derivative(n, a, b, c, t, kernel=True):
    """Direct double uniform[-1,1] moments and beta integration."""
    if n < 2:
        return F(0)
    ans, m = F(0), n-2
    for i in range(m // 2 + 1):
        for j in range((m-2*i) // 2 + 1):
            h = m-2*i-2*j
            multi = factorial(m)//(factorial(h)*factorial(2*i)*factorial(2*j))
            moment = F(1, (2*i+1)*(2*j+1))
            extra = 1 if kernel else 0
            beta = F(factorial(2*j+extra)*factorial(2*i+extra),
                     factorial(2*i+2*j+2*extra+1))
            ans += multi*c**h*a**i*b**j*moment*beta*t**(2*i+2*j+2*extra)
    return (a-b)*n*(n-1)*ans


def moment_checks():
    cases = [(F(0), F(1)), (F(1), F(0)), (F(1), F(1)),
             (F(2), F(7)), (F(9, 4), F(2, 3))]
    count = 0
    for n in range(25):
        for a, b in cases:
            for c in [F(0), F(-2, 3), F(5, 7)]:
                for t in [F(1), F(2, 5)]:
                    require(sphere_power_difference(n, a, b, c, t) ==
                            integral_of_second_derivative(n, a, b, c, t),
                            f"moment identity failed: {(n, a, b, c, t)}")
                    count += 1
    args = (2, F(3), F(1), F(0), F(1))
    actual = sphere_power_difference(*args)
    require(actual != -integral_of_second_derivative(*args), "sign control failed")
    require(actual != integral_of_second_derivative(*args, kernel=False),
            "kernel control failed")
    require(sphere_power_difference(*args, dimension=2) !=
            integral_of_second_derivative(*args), "dimension control failed")
    return count


def dot(v, w):
    return sum((a*b for a, b in zip(v, w)), F(0))


def sub(v, w):
    return tuple(a-b for a, b in zip(v, w))


def rank(rows):
    rows = [list(map(F, row)) for row in rows]
    k = 0
    for c in range(len(rows[0])):
        pivot = next((i for i in range(k, len(rows)) if rows[i][c]), None)
        if pivot is None:
            continue
        rows[k], rows[pivot] = rows[pivot], rows[k]
        d = rows[k][c]
        rows[k] = [x/d for x in rows[k]]
        for i in range(len(rows)):
            if i != k:
                d = rows[i][c]
                rows[i] = [x-d*y for x, y in zip(rows[i], rows[k])]
        k += 1
    return k


def screw_fixture():
    """Reconstruct R4's rational contraction, without its obstruction proof."""
    u = [(0, 0), (1, 0), (-1, 0), (2, 0), (-2, 0),
         (0, 1), (0, -1), (1, 1)]
    u = [tuple(map(F, v)) for v in u]

    def planar_p(v):
        return v[0]+v[1], v[1]-v[0]

    vs = set(map(planar_p, u))
    for v in u[:2]:
        pv = planar_p(v)
        for j in range(2):
            for sign in [-1, 1]:
                point = list(pv)
                point[j] += F(sign, 4)
                vs.add(tuple(point))
    v = sorted(vs)
    a = [(*z, (1+dot(z, z))/2) for z in v]
    b = [(*z, -dot(z, z)) for z in u]
    bt = [(-z[1], z[0], 1-dot(z, z)) for z in u]
    source, target = a+b, a+bt
    require(len(source) == 24 and len(set(source)) == 24, "fixture count")
    losses = []
    for i in range(24):
        for j in range(i+1, 24):
            d = dot(sub(source[i], source[j]), sub(source[i], source[j]))
            d -= dot(sub(target[i], target[j]), sub(target[i], target[j]))
            require_contraction_loss(d)
            losses.append((i, j, d))
    for i, vi in enumerate(v):
        for j, uj in enumerate(u):
            d = next(d for ii, jj, d in losses if ii == i and jj == len(v)+j)
            diff = sub(vi, planar_p(uj))
            require(d == dot(diff, diff), "cross-loss identity")
    paired = [p+q for p, q in zip(source, target)]
    paired_rank = rank([sub(z, paired[0]) for z in paired[1:]])
    require(paired_rank == 6, "fixture lost paired rank six")
    posterior_count = 0
    mean_losses = []
    for numerators in [[1]*24, list(range(1, 25)), [1+(i % 5)**2 for i in range(24)]]:
        w = [F(a, sum(numerators)) for a in numerators]
        h = [[(w[i] if i == j else 0)-w[i]*w[j] for j in range(24)]
             for i in range(24)]
        require(all(sum(row) == 0 for row in h), "Hessian row sums")
        gram = sum((dot(source[i], source[j])-dot(target[i], target[j]))*h[i][j]
                   for i in range(24) for j in range(24))
        pair = sum(d*w[i]*w[j] for i, j, d in losses)
        require(gram == pair and pair > 0, "Gram/pair sign")
        mean_losses.append(str(2*pair))
        posterior_count += 1
    # A genuine expansion is outside the theorem's hypotheses and has negative loss.
    expanding_loss = F(1)-F(4)
    try:
        require_contraction_loss(expanding_loss)
    except RuntimeError:
        pass
    else:
        raise RuntimeError("expansion was incorrectly accepted")
    equal = sum(d == 0 for _, _, d in losses)
    require(equal == 156 and len(losses)-equal == 120, "pair summary")
    return {"sites": 24, "pairs": len(losses), "equal_pairs": equal,
            "strict_pairs": len(losses)-equal, "paired_affine_rank": paired_rank,
            "posterior_gram_checks": posterior_count,
            "mean_losses": mean_losses}


def main():
    count = moment_checks()
    fixture = screw_fixture()
    # Leading coefficient: unordered pair loss = D/2; integral u(1-u)=1/6.
    require(F(1, 2)*F(1, 6) == F(1, 12), "ordered-pair normalization")
    # R-independent rescaling of the compact-ray lower bound at lambda_0=1/(2R).
    require(F(1, 4)*F(1, 12) == F(1, 48), "eventual endpoint constant")
    require(44*96 == 4224, "uniform strict-contraction endpoint constant")
    print(json.dumps({"status": "EXACT_SINC_COMPARISON_CHECKS_PASSED",
                      "moment_identities": count, "maximum_degree": 24,
                      "negative_controls": 4, "fixture": fixture,
                      "universal_proof": "PROOF.md; not inferred from these finite checks"},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
