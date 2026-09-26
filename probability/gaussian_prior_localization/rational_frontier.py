#!/usr/bin/env python3
"""Exact rational producer and small controls; no Gaussian sign computation."""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, floor
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return sum(a * a for a in x)


def rational(x):
    require(type(x) is int or isinstance(x, F), "use integers or Fraction")
    return F(x)


def input_data(k, xs, ys, weights):
    require(type(k) is int and k >= 1, "positive integer k")
    require(len(xs) == len(ys) == len(weights), "label counts")
    require(1 <= len(xs) <= k**6, "atom budget")
    xs = [tuple(map(rational, p)) for p in xs]
    ys = [tuple(map(rational, p)) for p in ys]
    weights = list(map(rational, weights))
    require(all(len(p) == 3 for p in xs + ys), "dimension")
    require(xs[0] == ys[0] == (0, 0, 0), "anchor")
    require(all(norm2(p) <= 4 * k * k for p in xs + ys), "radius")
    require(all(w >= 0 for w in weights) and sum(weights) == 1, "weights")
    for i, j in combinations(range(len(xs)), 2):
        require(norm2(sub(ys[i], ys[j])) <= norm2(sub(xs[i], xs[j])),
                "input expansion or inconsistent collision")
    return xs, ys, weights


def check_grid(k, xs, ys, numerators):
    require(type(k) is int and k >= 1, "positive integer grid parameter")
    L, W = 256 * k**3, 4 * k**7
    require(len(xs) == len(ys) == len(numerators), "output label counts")
    require(1 <= len(xs) <= k**6, "output atom budget")
    require(all(len(p) == 3 and all(type(a) is int for a in p)
                for p in xs + ys), "integer centers")
    require(xs[0] == ys[0] == (0, 0, 0), "output anchor")
    require(all(norm2(p) <= (3 * k * L)**2 for p in xs + ys), "output radius")
    require(all(type(n) is int and n >= 0 for n in numerators)
            and sum(numerators) == W, "integer masses")
    losses = []
    expected_loss = F(0)
    for i, j in combinations(range(len(xs)), 2):
        loss = norm2(sub(xs[i], xs[j])) - norm2(sub(ys[i], ys[j]))
        require(loss >= 256 * k * k, "insufficient integer pair margin")
        losses.append(loss)
        expected_loss += F(2 * numerators[i] * numerators[j] * loss, W*W*L*L)
    positive = sum(n > 0 for n in numerators)
    if positive >= 2:
        require(expected_loss >= F(1, 2048 * k**18), "pair-loss floor")
    else:
        require(expected_loss == 0, "point-law equality")
    return {"pair_count": len(losses),
            "minimum_integer_pair_margin": min(losses) if losses else None,
            "positive_weights": positive,
            "ordered_expected_distance_loss": str(expected_loss)}


def round_instance(k, xs, ys, weights):
    """Produce the integer input contract from one exact rational point of K_k."""
    xs, ys, weights = input_data(k, xs, ys, weights)
    L, W = 256 * k**3, 4 * k**7
    r, expansion = F(1, 4*k), 1 + F(1, 8*k*k)
    reps = [0]
    for i in range(1, len(xs)):
        if all(norm2(sub(xs[i], xs[j])) > r*r for j in reps):
            reps.append(i)
    assignment = [next(t for t, j in enumerate(reps)
                       if norm2(sub(xs[i], xs[j])) <= r*r)
                  for i in range(len(xs))]
    merged = [F(0)] * len(reps)
    for i, a in enumerate(assignment):
        merged[a] += weights[i]
        require(norm2(sub(ys[i], ys[reps[a]])) <= r*r, "image merging cost")
    rounded_x = [tuple(floor(L * expansion * a + F(1, 2)) for a in xs[i])
                 for i in reps]
    rounded_y = [tuple(floor(L * a + F(1, 2)) for a in ys[i]) for i in reps]
    for t, i in enumerate(reps):
        dx = tuple(F(a, L) - expansion*b for a, b in zip(rounded_x[t], xs[i]))
        dy = tuple(F(a, L) - b for a, b in zip(rounded_y[t], ys[i]))
        require(norm2(dx) <= F(3, 4*L*L) and norm2(dy) <= F(3, 4*L*L),
                "rounding displacement")
    numerators = [floor(W*w) for w in merged]
    missing = W - sum(numerators)
    require(0 <= missing < len(reps), "largest-remainder count")
    order = sorted(range(len(reps)), key=lambda i: (-(W*merged[i]-numerators[i]), i))
    for i in order[:missing]:
        numerators[i] += 1
    errors = [abs(w-F(n,W)) for w,n in zip(merged,numerators)]
    require(all(e <= F(1,W) for e in errors), "individual weight error")
    require(sum(errors) <= F(len(reps),W) <= F(1,4*k), "weight budget")
    checked = check_grid(k, rounded_x, rounded_y, numerators)
    return {"k": k, "input_atoms": len(xs), "output_atoms": len(reps),
            "coordinate_denominator": L, "weight_denominator": W,
            "source_integer_centers": rounded_x, "target_integer_centers": rounded_y,
            "weight_numerators": numerators, "representatives": reps,
            "assignments": assignment, "weight_l1_error": str(sum(errors)),
            "hinge_transfer_bound": str(F(161,256*k)), **checked}


def rejected(action):
    try:
        action()
    except ValueError:
        return True
    return False


def report():
    k = 2
    L = 256*k**3
    rotate = lambda p: (F(3,5)*p[0]-F(4,5)*p[1],
                        F(4,5)*p[0]+F(3,5)*p[1], p[2])
    xs = [(0,0,0),(0,0,0),(F(1,L),0,0),(1,0,0),(F(101,100),0,0),(0,1,0)]
    weights = [F(1,10),0,F(1,5),F(1,4),F(1,4),F(1,5)]
    cases = [round_instance(k,xs,list(map(rotate,xs)),weights)]
    collapse_x = [(0,0,0),(F(1,7),0,0),(F(-1,7),0,0),(0,0,F(1,9))]
    collapse_y = [(0,0,0)]*4
    cases.append(round_instance(k,collapse_x,collapse_y,[0,F(1,1000),F(999,1000),0]))
    cases.append(round_instance(k,collapse_x,collapse_y,[0,F(1,10000),F(9999,10000),0]))
    cases.append(round_instance(k,[(0,0,0)]*4,[(0,0,0)]*4,[F(1,3),F(1,6),F(1,4),F(1,4)]))
    cases.append(round_instance(1,[(0,0,0)],[(0,0,0)],[1]))

    # Expanding then independently rounding a tiny isometric pair, without
    # the preliminary merge, still creates expansion. Coordinates are in
    # integer grid units here; our actual producer merges this pair.
    naive_x = (floor(1+F(1,8*k*k)+F(1,2)),0,0)
    naive_y = (floor(F(3,5)+F(1,2)),floor(F(4,5)+F(1,2)),0)
    naive_loss = norm2(naive_x)-norm2(naive_y)
    require(naive_loss == -1, "unmerged-rounding control must fail")
    tiny = [(0,0,0),(F(1,L),0,0)]
    tiny_out = round_instance(k,tiny,list(map(rotate,tiny)),[F(1,2),F(1,2)])
    require(tiny_out['output_atoms'] == 1, "tiny pair should merge")
    cases.append(tiny_out)

    bad_centers = list(cases[0]['target_integer_centers'])
    bad_centers[1] = (10*L,0,0)
    negative_controls = [
        rejected(lambda: input_data(k,[(0,0,0)]*2,[(0,0,0),(1,0,0)],[F(1,2)]*2)),
        rejected(lambda: check_grid(k,cases[0]['source_integer_centers'],bad_centers,
                                    cases[0]['weight_numerators'])),
        rejected(lambda: round_instance(k,[(0,0,0)],[(0,0,0)],[F(3,4)])),
        rejected(lambda: round_instance(k,[(0,0,0)],[(0,0,0)],[1.0]))]
    require(all(negative_controls), "a malformed input was accepted")

    budgets = []
    for t in (1,2,3,8,16):
        transfer = F(5,8*t)+F(1,256*t**3)
        require(transfer <= F(161,256*t), "transfer envelope")
        total = F(14,3*t)+F(161,256*t)
        require(total == F(4067,768*t) < F(16,3*t), "consumer budget")
        require(F(2,(4*t**7)**2 * 256*t**4) == F(1,2048*t**18), "pair-loss floor constant")
        require((1536*t**4+1)**6*(4*t**7+1) <= 2**69*t**31, "count base")
        budgets.append({"k":t,"atoms":t**6,"L":256*t**3,"W":4*t**7,
                        "largest_power":2**16*t**8,"global_error_bound":str(total)})
    coefficient_checks = 0
    for N in range(13):
        for j in range(N+1):
            exact_norm = 2*(N+1)*comb(N,j)*sum(
                (F(comb(N-j,l),(j+l+1)*(j+l+2)) for l in range(N-j+1)),F(0))
            require(exact_norm <= (N+1)*3**N, "moment-error amplification bound")
            coefficient_checks += 1
    return {"status":"RATIONAL_COMPACT_FRONTIER_CONTROLS_PASS","cases":cases,
            "unmerged_integer_loss":naive_loss,"malformed_inputs_rejected":len(negative_controls),
            "budget_controls":budgets,"coefficient_norm_controls":coefficient_checks,
            "scope":"Exact rational construction controls only; no Gaussian moment, beta sign, global enumeration or independent review."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = report()
    encoded = json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.check:
        expected = Path(__file__).with_name('RATIONAL_EXPECTED.json').read_text()
        require(encoded == expected, "expected report mismatch")
    print(result['status'],sha256(encoded.encode()).hexdigest())
    if not args.check:
        print(encoded,end='')


if __name__ == '__main__':
    main()
