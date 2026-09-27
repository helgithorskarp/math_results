#!/usr/bin/env python3
"""Exact controls for PROOF.md; standard library, no floating-point arithmetic."""

import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def distance2(a, b, metric=None):
    d = sub(a, b)
    return sum(w*x*x for w, x in zip(metric or [1]*len(d), d))


def rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    if not rows:
        return 0
    k = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(k, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[k], rows[pivot] = rows[pivot], rows[k]
        v = rows[k][j]
        rows[k] = [x/v for x in rows[k]]
        for i in range(k+1, len(rows)):
            v = rows[i][j]
            rows[i] = [x-v*y for x, y in zip(rows[i], rows[k])]
        k += 1
    return k


# Ascending polynomial coefficient lists, with exact rational arithmetic.
def trim(p):
    p = list(map(Q, p))
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    return trim([(p[i] if i < len(p) else 0)
                 + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def neg(p):
    return [-x for x in p]


def mul(p, q):
    out = [Q(0)]*(len(p)+len(q)-1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i+j] += x*y
    return trim(out)


def deriv(p):
    return trim([i*p[i] for i in range(1, len(p))] or [0])


def tau(s):
    s = Q(s)
    return s*(3-s)/(1+s)


def endpoint(b, shift=Q(1)):
    x, y, z = b
    return (-y, x, z+shift)


def lm(a, b):
    x, y, z = b
    X, Y, Z = a
    return Z-Q(1, 2)-z-X*(x+y)-Y*y, Y*x


def lifted(p, moving, s, k, chord=False, remove_height=False):
    """Fourth coordinate is stored divided by sqrt(2); metric restores it."""
    s, k = Q(s), Q(k)
    if not moving:
        return tuple(p)+(Q(0), Q(0))
    x, y, z = p
    r = 1-s
    t = s if chord else tau(s)
    return (r*x-s*y, t*x+r*y, z+s,
            k*(y-r*x/(1+s)), Q(0) if remove_height else k)


def run():
    s, r, den, num = [0, 1], [1, -1], [1, 1], [0, 3, -1]
    identities = {
        "residual_11": add(add(mul(mul(den, den), add([1], neg(mul(r, r)))),
                              neg(mul(num, num))),
                           neg(mul([0, 2], mul(r, mul(r, r))))),
        "residual_12": add(mul(r, add(mul(s, den), neg(num))),
                           mul([0, 2], mul(r, r))),
        "residual_22": add(add(add([1], neg(mul(s, s))), neg(mul(r, r))),
                           neg(mul([0, 2], r))),
        "tau_derivative": add(add(mul(deriv(num), den), neg(mul(num, deriv(den)))),
                              neg(mul(r, [3, 1]))),
    }
    for name, polynomial in identities.items():
        require(trim(polynomial) == [0], name)
    require(tau(Q(0)) == 0 and tau(Q(1)) == 1, "endpoints")

    A = [tuple(map(Q, p)) for p in
         [(0, 0, Q(3, 2)), (1, 0, Q(3, 2)),
          (0, 1, Q(3, 2)), (0, 0, Q(5, 2))]]
    B = [tuple(map(Q, p)) for p in
         [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]]
    X = A+B
    Y = A+[endpoint(b) for b in B]
    pairs = list(combinations(range(8), 2))
    losses = [distance2(X[i], X[j])-distance2(Y[i], Y[j]) for i, j in pairs]
    require(min(losses) >= 0, "endpoint contraction")
    require(rank([sub(a, A[0]) for a in A[1:]]) == 3, "A span")
    require(rank([sub(b, B[0]) for b in B[1:]]) == 3, "B span")
    paired = [x+y for x, y in zip(X, Y)]
    require(rank([sub(p, paired[0]) for p in paired[1:]]) == 6, "paired rank")

    within_rows, all_tight_rows = [], []
    for (i, j), loss in zip(pairs, losses):
        row = sub(X[i], X[j])+tuple(-x for x in sub(Y[i], Y[j]))
        if (i < 4) == (j < 4):
            within_rows.append(row)
        if loss == 0:
            all_tight_rows.append(row)
    require(rank(within_rows) == 5, "within-cloud scalar constraints")
    require(rank(all_tight_rows) == 6, "scalar-defect exclusion")
    require(all(dot(row, (0, 0, 1, 0, 0, 1)) == 0 for row in within_rows),
            "only axial scalar null direction")

    # Pythagorean parameters give rational s and sqrt(s(1-s)).
    times = {}
    for p in range(7):
        for q in range(7):
            if p or q:
                d = p*p+q*q
                times[Q(p*p, d)] = Q(p*q, d)
    metric = (1, 1, 1, 2, 1)
    previous = None
    digest_rows = []
    for time in sorted(times):
        k = times[time]
        require(k*k == time*(1-time), "time radical")
        points = [lifted(x, i >= 4, time, k) for i, x in enumerate(X)]
        distances = [distance2(points[i], points[j], metric) for i, j in pairs]
        for n, (i, j) in enumerate(pairs):
            if i < 4 <= j:
                L, N = lm(X[i], X[j])
                require(L >= 0 and N >= 0, "domain interface")
                predicted = 2*time*L+2*tau(time)*N
            else:
                predicted = 0
            require(distance2(X[i], X[j])-distances[n] == predicted,
                    "direct five-dimensional squared distance")
        if previous is not None:
            require(all(d <= e for d, e in zip(distances, previous)), "time ordering")
        previous = distances
        digest_rows.append([str(time), [str(d) for d in distances]])
    require([lifted(x, i >= 4, 0, 0) for i, x in enumerate(X)] ==
            [x+(Q(0), Q(0)) for x in X], "source realization")
    require([lifted(x, i >= 4, 1, 0) for i, x in enumerate(X)] ==
            [y+(Q(0), Q(0)) for y in Y], "target realization")

    # Direct controls on extra interior points; the universal domain proof is (8).
    interior_B = [(Q(1, 8), Q(1, 4), Q(1, 2)), (Q(1, 3), Q(1, 3), Q(1, 6))]
    more_A = [(Q(-2), Q(1, 3), Q(2)), (Q(2), Q(3), Q(6))]
    for a in A+more_A:
        for b in B+interior_B:
            L, N = lm(a, b)
            require(L >= 0 and N >= 0, "extended domain control")

    # Exact helicity: W=M x+c. Check both constant and linear coefficients.
    Wmat = [[-1, -1, 0], [1, -1, 0], [0, 0, 0]]
    c = (0, 0, 1)
    curl = (Wmat[2][1]-Wmat[1][2], Wmat[0][2]-Wmat[2][0],
            Wmat[1][0]-Wmat[0][1])
    require(curl == (0, 0, 2), "curl")
    require(all(sum(curl[i]*Wmat[i][j] for i in range(3)) == 0
                for j in range(3)) and dot(curl, c) == 2, "helicity")

    # Adverse controls establish that dropping a hypothesis or lift term is detected.
    bad_target = A+[endpoint(b, Q(3)) for b in B]
    require(any(distance2(X[i], X[j]) < distance2(bad_target[i], bad_target[j])
                for i, j in pairs), "reject excessive translation")
    mid = [lifted(x, i >= 4, Q(1, 2), Q(1, 2), remove_height=True)
           for i, x in enumerate(X)]
    require(distance2(mid[0], mid[7], metric) < distance2(Y[0], Y[7]),
            "reject height deletion: re-expansion to endpoint")
    chord = [lifted(b, True, Q(1, 2), Q(1, 2), chord=True) for b in B]
    require(distance2(chord[0], chord[1], metric) == Q(5, 9), "bad chord control")
    bad_a = tuple(map(Q, (1, -1, Q(5, 2))))
    require(all(distance2(bad_a, b) >= distance2(bad_a, endpoint(b)) for b in B),
            "negative-N control is still endpoint-contractive")
    L, N = lm(bad_a, B[1])
    bad_loss = 2*Q(1, 5)*L+2*tau(Q(1, 5))*N
    require((L, N, bad_loss) == (1, -1, Q(-8, 15)), "negative-N motion control")

    return {
        "status": "PASS; exact construction controls, not independent review",
        "polynomial_identities": sorted(identities),
        "sites": 8,
        "endpoint_pairs": len(pairs),
        "endpoint_losses": list(map(str, losses)),
        "tight_endpoint_pairs": sum(x == 0 for x in losses),
        "paired_affine_rank": 6,
        "within_tight_scalar_rank": 5,
        "all_tight_scalar_rank": 6,
        "rational_times": len(times),
        "direct_pair_time_checks": len(times)*len(pairs),
        "trajectory_record_sha256": sha256(json.dumps(digest_rows, separators=(",", ":")).encode()).hexdigest(),
        "extended_domain_pairs": (len(A)+len(more_A))*(len(B)+len(interior_B)),
        "helicity": 2,
        "adverse_controls": {
            "excessive_translation": "rejected",
            "deleted_translation_height": "rejected by re-expansion",
            "uncompleted_chord_squared_edge": "5/9, must remain 1",
            "endpoint_contractive_negative_N_loss": str(bad_loss),
        },
        "trust_boundary": "Written universal geometry and cited classical transfers; finite exact controls do not replace them.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="compare to EXPECTED.json")
    args = parser.parse_args()
    result = run()
    if args.verify:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
