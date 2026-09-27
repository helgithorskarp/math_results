#!/usr/bin/env python3
"""Exact finite consumer and algebra controls; the universal proof is PROOF.md."""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rat(x):
    require(type(x) in (str, int), "rationals must be strings or integers")
    return Q(x)


def integer(x, minimum):
    require(type(x) is int and x >= minimum, "invalid integer parameter")
    return x


def schedule(R, j, k):
    integer(R, 1); integer(j, 1); integer(k, 0)
    v = 2*(j+1)
    c = isqrt(v)
    c += c*c < v
    B, S = 3*R+c, 6*R
    E, F = B*S+2*B*B, B*S+4*B*B+2
    K = 3*(E+6)*(1+B*S)+12*F
    b = (3*R*K-1).bit_length()
    N = 2*(j+6*R*B+b)
    P = 2*((6*R+1)**2+R*R)+2*R+2*j+5*k+19
    Z = 31+47*R*R+2*(2*R+c)**2+5*N
    return dict(R=R, j=j, k=k, c=c, B=B, S=S, E=E, F=F,
                K=K, b=b, N=N, P=P, L_cov=2*Z+4)


def le_dyadic(x, n):
    """x<=2^-n without constructing an enormous 2^n unnecessarily."""
    require(x >= 0 and type(n) is int and n >= 0, "dyadic domain")
    if not x:
        return True
    left_bits = x.numerator.bit_length()+n
    right_bits = x.denominator.bit_length()
    if left_bits != right_bits:
        return left_bits < right_bits
    return (x.numerator << n) <= x.denominator


def sqdist(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def mean(z, weights):
    return [sum(w*x[c] for w, x in zip(weights, z)) for c in range(len(z[0]))]


def covariance(z, weights):
    center = mean(z, weights)
    return [[sum(w*(x[a]-center[a])*(x[b]-center[b])
                 for w, x in zip(weights, z)) for b in range(3)] for a in range(3)]


def decode(data):
    require(type(data) is dict and set(data) ==
            {"source", "target", "weights", "variance", "R", "j", "k"}, "input fields")
    src, dst, raw = data["source"], data["target"], data["weights"]
    require(all(type(z) is list for z in (src, dst, raw)), "input lists")
    require(len(src) == len(dst) == len(raw) and len(raw) > 0, "atom counts")
    def points(z):
        require(all(type(x) is list and len(x) == 3 for x in z), "R3 points")
        return [[rat(v) for v in x] for x in z]
    src, dst, weights = points(src), points(dst), [rat(w) for w in raw]
    require(all(w >= 0 for w in weights) and sum(weights) == 1, "probability weights")
    s = rat(data["variance"])
    require(s > 0, "positive variance")
    p = schedule(data["R"], data["j"], data["k"])
    active = [i for i, w in enumerate(weights) if w]
    return ([src[i] for i in active], [dst[i] for i in active],
            [weights[i] for i in active], s, p)


def consume(data):
    x, y, weights, s, p = decode(data)
    center = mean(x, weights)
    radius2 = max(sqdist(z, center) for z in x)
    require(radius2 <= p["R"]**2*s, "actual centered source radius exceeds R")
    D = Q(0)
    for i in range(len(x)):
        for j in range(len(x)):
            loss = sqdist(x[i], x[j])-sqdist(y[i], y[j])
            require(loss >= 0, "expanding active pair")
            D += weights[i]*weights[j]*loss
    cx, cy = covariance(x, weights), covariance(y, weights)
    require(D == 2*sum(cx[i][i]-cy[i][i] for i in range(3)), "ordered loss identity")
    d = D/s
    status = ("SUPPORT_ISOMETRY" if d == 0 else
              "SIGNED_ABOVE_CUTOFF" if le_dyadic(d, p["N"]) else "UNRESOLVED")
    result = {"status": status, "active_atoms": len(x), "ordered_normalized_loss": str(d),
              "source_radius_squared_over_s": str(radius2/s), "schedule": p,
              "target_peak_lower_bound": str(max(Q(0), 1-sum(cy[i][i] for i in range(3))/(2*s))),
              "proof_status": "analytic author proof; independent review pending"}
    if status == "SIGNED_ABOVE_CUTOFF":
        result["hinge_claim"] = "H(u)>=0 for u>=2^-j"
        result["middle_claim"] = "H(u)>=d*2^-P for 2^-j<=u<=m-2^-k"
    return result


def simplex_flap(exponent):
    e = Q(1, 2**exponent)
    u = [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]
    x = [[Q(v,2) for v in z] for z in u]
    y = copy.deepcopy(x)
    for i in range(4):
        for j in range(4):
            if i != j:
                x.append([Q(b-a,2) for a,b in zip(u[i],u[j])])
                y.append([Q(b+a,2) for a,b in zip(u[i],u[j])])
    return {"source": [[str(v) for v in z] for z in x],
            "target": [[str(v) for v in z] for z in y],
            "weights": [str(1-e)]+[str(e/15)]*15,
            "variance": 1, "R": 3, "j": 3, "k": 2}


def rank(rows):
    a = [[Q(v) for v in row] for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        at = next((i for i in range(pivot,len(a)) if a[i][col]), None)
        if at is None:
            continue
        a[pivot], a[at] = a[at], a[pivot]
        div = a[pivot][col]
        a[pivot] = [v/div for v in a[pivot]]
        for i in range(len(a)):
            if i != pivot:
                mul = a[i][col]
                a[i] = [v-mul*w for v,w in zip(a[i],a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


# Tiny Laurent-polynomial algebra for a formal radial derivative identity.
# Variables (h,r,p,c,l,b); d/dr h=h(c-2l), d/dr r=1, d/dr p=b.
def add(*terms):
    out = {}
    for t in terms:
        for powers, v in t.items():
            out[powers] = out.get(powers,Q(0))+v
    return {key:v for key,v in out.items() if v}


def mon(coefficient=1, **exponents):
    return {tuple(exponents.get(v,0) for v in "hrpclb"): Q(coefficient)}


def mul(a,b):
    out = {}
    for p,x in a.items():
        for q,y in b.items():
            key = tuple(i+j for i,j in zip(p,q))
            out[key] = out.get(key,Q(0))+x*y
    return {key:v for key,v in out.items() if v}


def radial_derivative(a):
    rules = [add(mon(h=1,c=1),mon(-2,h=1,l=1)),mon(),mon(b=1),{}, {}, {}]
    terms = []
    for powers, coefficient in a.items():
        for i, power in enumerate(powers):
            if power:
                q = list(powers); q[i] -= 1
                terms.append(mul({tuple(q):coefficient*power},rules[i]))
    return add(*terms)


def pin_check():
    rows = json.loads((HERE/"DEPENDENCIES.json").read_text())
    for row in rows:
        p = (HERE/row["path"]).resolve()
        require(p.is_relative_to(HERE.parent), "dependency outside probability tree")
        require(hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"], "dependency hash mismatch")
    return len(rows)


def self_check():
    count = pin_check()
    fixture = json.loads((HERE/"INPUT.json").read_text())
    require(fixture == simplex_flap(487), "fixture mismatch")
    result = consume(fixture)
    require(result["status"] == "SIGNED_ABOVE_CUTOFF", "guard failure")
    require((result["schedule"]["N"],result["schedule"]["P"]) == (482,781), "calibration schedules")
    x,y,weights,s,p = decode(fixture)
    losses = [[sqdist(a,b)-sqdist(c,d) for b,d in zip(x,y)] for a,c in zip(x,y)]
    # Polynomial coefficients in epsilon: each weight is a_i+b_i epsilon.
    a = [Q(1)]+[Q(0)]*15
    b = [Q(-1)]+[Q(1,15)]*15
    coefficients = [sum(losses[i][j]*term(i,j) for i in range(16) for j in range(16))
                    for term in (lambda i,j:a[i]*a[j],lambda i,j:a[i]*b[j]+b[i]*a[j],lambda i,j:b[i]*b[j])]
    require(coefficients == [0,Q(8,5),0], "all-epsilon loss polynomial")
    for z, isotropic in ((x,Q(3,5)),(y,Q(1,3))):
        ma,mb = mean(z,a),mean(z,b)
        require(ma == [Q(1,2)]*3 and mb == [Q(-8,15)]*3, "all-epsilon means")
        for i in range(3):
            for j in range(3):
                covariance_coefficients = [sum(a[r]*z[r][i]*z[r][j] for r in range(16))-ma[i]*ma[j],
                    sum(b[r]*z[r][i]*z[r][j] for r in range(16))-ma[i]*mb[j]-mb[i]*ma[j], -mb[i]*mb[j]]
                require(covariance_coefficients == [0,isotropic*(i==j)+Q(4,15),-Q(64,225)], "covariance polynomial")
    require(max(max(row) for row in losses) == 8, "maximum pair loss")
    require(max(sqdist(v,w) for v in x for w in x) == 8, "source diameter")
    paired = [v+w for v,w in zip(x,y)]
    ranks = [rank([[a-b for a,b in zip(row,z[0])] for row in z[1:]]) for z in (x,y,paired)]
    require(ranks == [3,3,6], "affine ranks")
    require(le_dyadic(16*Q(1,2**487),482), "whole family guard")
    require(Q(result["target_peak_lower_bound"]) > Q(3,4), "nonempty explicit band")

    lhs = mul(radial_derivative(mon(h=1,r=2,p=-1)),mon(p=-1))
    rhs = mul(mon(h=1,r=1,p=-2),add(mon(r=1,c=1),mon(-2,r=1,l=1),mon(2),mon(-1,b=1,r=1,p=-1)))
    require(lhs == rhs, "formal radial derivative identity")
    require(Q(4,3)*Q(1,8)**3*2 == Q(1,192), "physical ball and spherical constants")
    require(Q(1,192)*Q(1,2)*Q(1,32)*Q(1,2) == Q(1,3*2**13), "Abel margin constant")
    # Direct Gaussian-product/hinge moment coefficient for square replica orders.
    for root in range(2,18):
        k = root*root
        require(Q(1,4*k*k*root) == Q(root,32)*Q(8,k**3), "replica 32 pi^3 normalization")
    schedules = 0
    for R in range(1,9):
        for j in (1,2,3,6,12):
            row = schedule(R,j,2)
            require((row["c"]-1)**2 < 2*(j+1) <= row["c"]**2, "ceil sqrt")
            require(2**(row["b"]-1) < 3*R*row["K"] <= 2**row["b"], "ceil logarithm")
            eta = Q(3*R,4*2**row["b"])
            require(eta*row["K"] <= Q(1,4) and eta*row["E"] <= 1, "small-loss to transverse guard")
            require(row["K"] == 3*(row["E"]+6)*(1+row["B"]*row["S"])+12*row["F"], "error budget")
            schedules += 1

    controls = []
    def control(data, expected, name):
        require(consume(data)["status"] == expected, name)
        controls.append(name)
    equal = copy.deepcopy(fixture); equal["weights"] = ["1/16"]*16
    control(equal,"UNRESOLVED","outside sufficient guard")
    iso = copy.deepcopy(fixture); iso["target"] = iso["source"]
    control(iso,"SUPPORT_ISOMETRY","zero loss")
    scaled = copy.deepcopy(fixture)
    for side in ("source","target"):
        scaled[side] = [[str(2*Q(v)) for v in z] for z in scaled[side]]
    scaled["variance"] = 4
    require(consume(scaled) == result,"variance normalization")
    controls.append("variance normalization")
    framed = copy.deepcopy(fixture)
    framed["source"] = [[str(-Q(z[1])+7),str(Q(z[2])-2),str(Q(z[0])+3)] for z in framed["source"]]
    framed["target"] = [[str(Q(z[2])-11),str(-Q(z[0])+4),str(Q(z[1])+2)] for z in framed["target"]]
    require(consume(framed) == result,"independent rigid frames")
    controls.append("independent rigid frames")
    zero = copy.deepcopy(fixture)
    zero["source"].append([0,0,0]); zero["target"].append([1000,0,0]); zero["weights"].append(0)
    require(consume(zero) == result,"inactive labels")
    controls.append("inactive labels")
    rejected = []
    for name, mutate in [
        ("negative weight",lambda z:z["weights"].__setitem__(1,"-1")),
        ("float",lambda z:z.__setitem__("variance",1.0)),
        ("zero variance",lambda z:z.__setitem__("variance",0)),
        ("bad dimension",lambda z:z["source"].__setitem__(0,[0,0])),
        ("radius",lambda z:z.__setitem__("R",1)),
        ("expansion",lambda z:z["target"].__setitem__(0,[100,0,0])),
        ("bad integer",lambda z:z.__setitem__("j",True)),
        ("unknown field",lambda z:z.__setitem__("d",0))]:
        bad = copy.deepcopy(fixture); mutate(bad)
        try:
            consume(bad)
        except (ValueError,ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError("malformed input accepted: "+name)
    damaged = copy.deepcopy(result); damaged["schedule"]["N"] -= 1
    require(damaged != consume(fixture),"damaged output comparison")
    return {"check":"COVARIANCE_FREE_SMALL_LOSS_PASS","dependencies_checked":count,
            "calibration":result,"family_loss_polynomial":[str(v) for v in coefficients],
            "family_covariance_eigenvalues_min":["(3/5) epsilon","(1/3) epsilon"],
            "affine_ranks":ranks,"schedules_checked":schedules,"replica_orders_checked":16,
            "formal_radial_derivative_terms":len(lhs),"valid_controls":controls,
            "malformed_rejections":rejected,"trust_boundary":"finite exact checks; universal analysis unformalized"}


def encoded(record):
    return (json.dumps(record,sort_keys=True,indent=2)+"\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,help="check one finite rational input")
    parser.add_argument("--record",action="store_true",help="emit recomputed canonical author record")
    args = parser.parse_args()
    if args.input:
        print(json.dumps(consume(json.loads(args.input.read_text())),sort_keys=True,indent=2))
        return
    record = self_check()
    blob = encoded(record)
    if args.record:
        sys.stdout.buffer.write(blob)
        return
    require(blob == (HERE/"EXPECTED.json").read_bytes(),"expected record mismatch")
    print(record["check"])
    print("record_sha256="+hashlib.sha256(blob).hexdigest())
    print("N=482 P=781; finite checks pass; analytic proof awaits independent review")


if __name__ == "__main__":
    try:
        main()
    except (ValueError,TypeError,KeyError,OSError,ZeroDivisionError) as exc:
        print("ERROR: "+str(exc),file=sys.stderr)
        sys.exit(1)
