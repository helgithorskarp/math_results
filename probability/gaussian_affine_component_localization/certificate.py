"""Exact support-level all-variance certificate for affine maps on boxes.

The auxiliary law is uniform volume in each box with supplied component
weights. A successful guard applies to every probability law on their union.
"""
import argparse
from fractions import Fraction as F
import itertools
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(x):
    require(type(x) in (int, str), "exact rational encoding required")
    return F(x)


def dot(x, y): return sum(a*b for a, b in zip(x, y))
def subvec(x, y): return [a-b for a, b in zip(x, y)]
def transpose(a): return [list(row) for row in zip(*a)]
def multiply(a, b): return [[dot(row, col) for col in transpose(b)] for row in a]
def vector(a, v): return [dot(row, v) for row in a]
def outer(x, y): return [[a*b for b in y] for a in x]
def scale(t, a): return [[t*z for z in row] for row in a]
def add(a, b): return [[x+y for x, y in zip(u, v)] for u, v in zip(a, b)]
def subtract(a, b): return add(a, scale(-1, b))
def identity(): return [[F(i == j) for j in range(3)] for i in range(3)]
def square_sum(a): return sum(z*z for row in a for z in row)


def determinant(a):
    n = len(a)
    if n == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]])
               for j in range(n))


def psd(a):
    require(a == transpose(a), "nonsymmetric matrix")
    return all(determinant([[a[i][j] for j in ids] for i in ids]) >= 0
               for size in (1, 2, 3) for ids in itertools.combinations(range(3), size))


def inputs(data):
    boxes = []
    for b in data["components"]:
        c, d, h = [list(map(rational, b[key])) for key in ("source_center", "target_center", "halfwidths")]
        a = [list(map(rational, row)) for row in b["matrix"]]
        p = rational(b["weight"])
        require(len(c) == len(d) == len(h) == len(a) == 3 and all(len(row) == 3 for row in a),
                "three-dimensional box/map required")
        require(p > 0 and all(t > 0 for t in h), "positive auxiliary weights and box widths required")
        require(psd(subtract(identity(), multiply(transpose(a), a))), "component matrix expands")
        boxes.append(dict(c=c, d=d, h=h, a=a, p=p))
    require(len(boxes) >= 2 and sum(b["p"] for b in boxes) == 1, "at least two probability-weighted components required")
    k, kap = [rational(data[key]) for key in ("global_covariance_floor", "component_covariance_floor")]
    require(k > 0 and kap > 0 and all(h*h/3 >= kap for b in boxes for h in b["h"]),
            "invalid covariance floor")
    return boxes, k, kap


def cross_lower(a, b):
    x, y = subvec(a["c"], b["c"]), subvec(a["d"], b["d"])
    u = subvec(x, vector(transpose(a["a"]), y))
    v = subvec(x, vector(transpose(b["a"]), y))
    mix = subtract(identity(), multiply(transpose(a["a"]), b["a"]))
    return (dot(x, x)-dot(y, y)-2*sum(h*abs(z) for h, z in zip(a["h"], u))
            -2*sum(h*abs(z) for h, z in zip(b["h"], v))
            -2*sum(a["h"][i]*b["h"][j]*abs(mix[i][j]) for i in range(3) for j in range(3)))


def produce(data):
    boxes, k, kap = inputs(data)
    cx = [sum(b["p"]*b["c"][j] for b in boxes) for j in range(3)]
    cy = [sum(b["p"]*b["d"][j] for b in boxes) for j in range(3)]
    X, Y, C = [scale(0, identity()) for _ in range(3)]
    for b in boxes:
        V = [[b["h"][i]**2/3 if i == j else F(0) for j in range(3)] for i in range(3)]
        u, v, A, p = subvec(b["c"], cx), subvec(b["d"], cy), b["a"], b["p"]
        X = add(X, scale(p, add(V, outer(u, u))))
        Y = add(Y, scale(p, add(multiply(multiply(A, V), transpose(A)), outer(v, v))))
        C = add(C, scale(p, add(multiply(V, transpose(A)), outer(u, v))))
    require(psd(subtract(X, scale(k, identity()))), "global covariance floor fails")
    gram = square_sum(X)+square_sum(Y)-2*square_sum(C)
    require(gram >= 0, "negative squared Gram norm")
    D = 2*sum(X[i][i]-Y[i][i] for i in range(3))
    diam2 = max(sum((abs(a["c"][j]-b["c"][j])+a["h"][j]+b["h"][j])**2
                    for j in range(3)) for a in boxes for b in boxes)
    delta = min(cross_lower(a, b) for i, a in enumerate(boxes) for b in boxes[:i])
    m = min(b["p"] for b in boxes)
    e = 2*gram/(k*m)
    cost = 4+78*diam2/kap
    out = dict(schema="affine-component-localization-v1", components=len(boxes),
               auxiliary_law="uniform volume in each source box with supplied component weights",
               actual_prior_unrestricted=True, diameter_squared=str(diam2),
               global_covariance_floor=str(k), component_covariance_floor=str(kap),
               component_mass_floor=str(m), squared_gram_norm=str(gram), mean_pair_loss=str(D),
               aligned_error_per_component=str(e), cross_loss_lower=str(delta),
               motion_constant=str(cost), orientation_slack=str(kap/4-e),
               cross_slack=str(delta-cost*e))
    if delta < 0:
        return dict(out, status="UNRESOLVED", reason="whole-box cross contraction not certified")
    require(D >= 0, "negative loss for a certified contraction")
    if gram == 0:
        return dict(out, status="CONGRUENT_EQUALITY", certified_variances="(0,infinity)",
                    certified_thresholds="[0,infinity)", arbitrary_ball_radii=True)
    if e > kap/4 or delta < cost*e:
        return dict(out, status="UNRESOLVED", reason="motion budget not certified")
    return dict(out, status="CERTIFIED_ALL_VARIANCE_SUPPORT", certified_variances="(0,infinity)",
                certified_thresholds="[0,infinity)", arbitrary_ball_radii=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    args = parser.parse_args()
    with open(args.input) as stream:
        result = produce(json.load(stream))
    print(json.dumps(result, sort_keys=True, indent=2))
