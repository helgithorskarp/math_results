#!/usr/bin/env python3
"""Finite sufficient guards and exact algebra supporting PROOF.md."""
import copy
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rat(x):
    require(type(x) in (int, str), "Use integers or rational strings")
    return Q(x)


def vector(x):
    require(isinstance(x, list) and len(x) == 3, "Expected a 3-vector")
    return tuple(map(rat, x))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), Q(0))


def norm(x):
    return dot(x, x)


def rank(rows):
    a = [list(row) for row in rows]
    if not a:
        return 0
    r = 0
    for k in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][k]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][k]
        a[r] = [x/v for x in a[r]]
        for i in range(len(a)):
            if i != r:
                v = a[i][k]
                a[i] = [x-v*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def affine_rank(points):
    return rank([sub(p, points[0]) for p in points[1:]])


def variance(points, w):
    mean = tuple(sum((wi*x[k] for wi, x in zip(w, points)), Q(0))
                 for k in range(len(points[0])))
    return sum((wi*norm(x) for wi, x in zip(w, points)), Q(0))-norm(mean)


def losses(p, q, w):
    values = [(i, j, norm(sub(p[i], p[j]))-norm(sub(q[i], q[j])))
              for i in range(len(p)) for j in range(i)]
    d = sum((2*w[i]*w[j]*v for i, j, v in values), Q(0))
    require(d == 2*(variance(p, w)-variance(q, w)), "Loss/variance mismatch")
    return values, d


def exponents(R, j, k):
    bn, bm = 40*R*R+9*R+38, 66*R*R+2*R+18
    nn = lambda ell: bn+3*j+8*ell
    nm = lambda ell: bm+4*j+5*ell
    nc = max(nn(k+1), nm(k+1))+k+2*R*R+2*R+1
    return {"norm": nn(k), "motion": nm(k), "chain": nc,
            "whole_curve_coefficient": max(bn+8,bm+5)+2*R*R+2*R+1}


def certify(data):
    require(isinstance(data, dict) and set(data) ==
            {"source", "weights", "source_anchor", "variance", "R", "j", "k", "stages"},
            "Unexpected input fields")
    require(isinstance(data["source"], list) and isinstance(data["weights"], list)
            and isinstance(data["stages"], list), "Expected lists")
    source = list(map(vector, data["source"]))
    w = list(map(rat, data["weights"]))
    require(len(source) == len(w) > 0 and all(x > 0 for x in w) and sum(w) == 1,
            "Invalid probability law")
    anchor = vector(data["source_anchor"])
    s = rat(data["variance"])
    R, j, k = data["R"], data["j"], data["k"]
    require(s > 0 and type(R) is int and R >= 1, "Invalid variance or radius")
    require(type(j) is int and j >= 0 and type(k) is int and k >= 0, "Invalid threshold bits")
    if any(norm(sub(x, anchor)) > s*R*R for x in source):
        return {"status": "UNRESOLVED", "reason": "source radius"}
    current, total, steps = source, Q(0), []
    for index, step in enumerate(data["stages"]):
        require(isinstance(step, dict) and "kind" in step, "Invalid stage")
        kind = step["kind"]
        require(kind in ("norm", "straight", "orthogonal_lift"), "Unknown stage kind")
        fields = {"kind", "target"} | ({"source_anchor", "target_anchor"} if kind == "norm" else set())
        require(set(step) == fields and isinstance(step["target"], list), "Invalid stage fields")
        target = list(map(vector, step["target"]))
        require(len(target) == len(source), "Label count changed")
        pairs, d = losses(current, target, w)
        reason = None
        if any(v < 0 for _, _, v in pairs):
            reason = "pair expansion"
        elif kind == "norm":
            a, b = vector(step["source_anchor"]), vector(step["target_anchor"])
            if any(norm(sub(x, a)) != norm(sub(y, b)) for x, y in zip(current, target)):
                reason = "anchor equality"
            elif any(norm(sub(x, a)) > s*R*R for x in current):
                reason = "anchor radius"
        elif kind == "straight":
            if any(dot(sub(target[i], target[t]),
                       sub(sub(target[i], target[t]), sub(current[i], current[t]))) > 0
                   for i, t, _ in pairs):
                reason = "straight motion end derivative"
        elif affine_rank(current)+affine_rank(target) > 5:
            reason = "orthogonal lift dimension"
        if reason:
            return {"status": "UNRESOLVED", "stage": index, "reason": reason}
        steps.append({"kind": kind, "ordered_loss": str(d),
                      "source_rank": affine_rank(current), "target_rank": affine_rank(target),
                      "tight_pairs": sum(v == 0 for _, _, v in pairs)})
        total += d
        current = target
    final_pairs, final_loss = losses(source, current, w)
    require(total == final_loss, "Loss did not telescope")
    bits = exponents(R, j, k)
    lower_peak = max(Q(1, 2**(R*R)), 1-variance(current, w)/(2*s))
    low, high = Q(1, 2**j), lower_peak-Q(1, 2**k)
    return {"status": "STRICT_CHAIN_MARGIN" if total else "ISOMETRY",
            "sites": len(w), "stages": steps, "stage_count": len(steps),
            "endpoint_pairs": len(final_pairs), "endpoint_tight_pairs": sum(v == 0 for _, _, v in final_pairs),
            "paired_affine_rank": affine_rank([p+q for p, q in zip(source, current)]),
            "ordered_loss": str(total), "normalized_loss": str(total/s),
            "exponents": bits, "margin": {"prefactor": str(total/s), "power_of_two": -bits["chain"]},
            "conditional_band": {"h_over_C_lower": str(low), "distance_below_target_peak_over_C": str(Q(1, 2**k))},
            "explicit_band": {"lower": str(low), "upper": str(high), "nonempty": low <= high},
            "target_peak_over_C_lower": str(lower_peak),
            "scope": "Finite sufficient geometry guard plus analytic Theorem B; no Gaussian sign quadrature"}


def pin_sources():
    data = json.loads((HERE/"DEPENDENCIES.json").read_text())
    for x in data:
        require(hashlib.sha256((HERE/x["path"]).read_bytes()).hexdigest() == x["sha256"], "Dependency pin mismatch")
    return len(data)


def audit(base):
    record = certify(base)
    require(record["paired_affine_rank"] == 6 and record["ordered_loss"] == "167/36", "Fixture invariant")
    require(record["exponents"] == {"norm": 241, "motion": 308, "chain": 328,
                                    "whole_curve_coefficient": 304}, "Fixture exponent")
    p = list(map(vector, base["stages"][0]["target"]))
    q = list(map(vector, base["stages"][1]["target"]))
    posterior_cases = 0
    for c, s in [(Q(1), Q(0)), (Q(3,5), Q(4,5)), (Q(5,13), Q(12,13)),
                 (Q(8,17), Q(15,17)), (Q(0), Q(1))]:
        require(c*c+s*s == 1, "Circle parameter")
        z = [(c*x[0], c*x[1])+tuple(s*y for y in yy) for x, yy in zip(p, q)]
        v = [(-s*x[0], -s*x[1])+tuple(c*y for y in yy) for x, yy in zip(p, q)]
        for seed in range(1, 11):
            w = [Q(1+(seed*(i+1)) % 13) for i in range(len(p))]
            mass = sum(w); w = [x/mass for x in w]
            ell = sum((w[i]*w[t]*(-2)*dot(sub(z[i],z[t]),sub(v[i],v[t]))
                       for i in range(len(p)) for t in range(len(p))), Q(0))
            _, d = losses(p, q, w)
            require(ell == 2*c*s*d and ell >= 0, "Motion loss rate")
            ez = [sum(wi*x[a] for wi, x in zip(w,z)) for a in range(5)]
            ev = [sum(wi*x[a] for wi, x in zip(w,v)) for a in range(5)]
            div = sum(wi*dot(x,y) for wi,x,y in zip(w,z,v))-dot(ez,ev)
            require(div == -ell/4, "Posterior divergence factor")
            posterior_cases += 1
    pressure_cases = 0
    for c in (Q(1,7), Q(2,3), Q(5,2)):
        for m in range(1, 17):
            inverse = m*c**(1-m)
            gaussian_integral = c**(m-1)/m
            require(inverse*gaussian_integral == 1, "Two-coordinate cancellation")
            require((m-1)*inverse == m*(m-1)*c**(1-m), "Pressure polynomial")
            pressure_cases += 1
    suffix_cases = 0
    for length in range(1, 7):
        for loss in itertools.product((Q(0), Q(1,3), Q(4,3)), repeat=length):
            for budget in (Q(1,7), Q(1), Q(7,3)):
                # Traverse backward independently of the forward suffix definition.
                remaining, eligible = Q(0), Q(0)
                for d in reversed(loss):
                    if remaining <= budget:
                        eligible += d
                    remaining += d
                require(eligible >= min(sum(loss), budget), "Suffix budget lost a crossing step")
                suffix_cases += 1
    subdivision = []
    for count in (1,2,4,8,16):
        data = copy.deepcopy(base)
        data["stages"] = []
        for i in range(1, count+1):
            scale = 1-Q(i,2*count)
            data["stages"].append({"kind":"straight", "target":
                [[str(scale*rat(x)) for x in row] for row in base["source"]]})
        got = certify(data)
        require(got["ordered_loss"] == "7/2" and got["exponents"] == record["exponents"], "Subdivision changed budget")
        subdivision.append(count)
    small_loss = []
    for bit in (1,10,40):
        t = Q(1,2**bit); data = copy.deepcopy(base)
        data["stages"] = [{"kind":"straight", "target":
            [[str((1-t)*rat(x)) for x in row] for row in base["source"]]}]
        got = certify(data)
        require(Q(got["ordered_loss"]) == Q(14,3)*(2*t-t*t), "Small-loss polynomial")
        require(got["margin"]["power_of_two"] == -328, "Small loss changed coefficient")
        small_loss.append({"t":"2^-"+str(bit),"loss":got["ordered_loss"]})
    empty = copy.deepcopy(base); empty["stages"] = []
    require(certify(empty)["status"] == "ISOMETRY", "Empty chain")
    cutoff_cases = 0
    for R in range(1, 7):
        for q in (Q(0), Q(1,3), Q(2), Q(9), Q(32)):
            # q stands for sqrt(2 log(2/tau)); the residual is a square.
            require(32*R*R+2*q*q-(4*R+q)**2 == (4*R-q)**2 >= 0,
                    "Logarithmic radial cutoff square")
            cutoff_cases += 1
    # Independent rigid frames at each stage preserve the norm and lift
    # certificates. They need not preserve a particular straight motion.
    frame_cases = 0
    for seed in range(1, 7):
        def frame(row, stage):
            a = list(map(rat, row))
            return [str((-1)**(seed+i+stage)*a[(i+stage+seed) % 3]
                        + Q(seed*(i+1)-stage, stage+1)) for i in range(3)]
        data = copy.deepcopy(base)
        data["source"] = [frame(x, 0) for x in base["source"]]
        data["source_anchor"] = frame(base["source_anchor"], 0)
        for i, step in enumerate(data["stages"]):
            original = base["stages"][i]
            step["target"] = [frame(x, i+1) for x in original["target"]]
            if step["kind"] == "norm":
                step["source_anchor"] = frame(original["source_anchor"], i)
                step["target_anchor"] = frame(original["target_anchor"], i+1)
        require(certify(data) == record, "Independent frames changed certificate")
        frame_cases += 1
    negatives = 0
    bad = copy.deepcopy(base)
    bad["stages"][0]["target"] = [[row[0],row[1],0] for row in base["source"]]
    require(certify(bad)["reason"] == "anchor equality", "Projection falsely norm-preserving"); negatives += 1
    for kind, matrix, reason in [
        ("straight",lambda x:[-rat(x[1]),rat(x[0]),rat(x[2])],"straight motion end derivative"),
        ("orthogonal_lift",lambda x:[rat(v)/2 for v in x],"orthogonal lift dimension"),
        ("straight",lambda x:[2*rat(v) for v in x],"pair expansion")]:
        bad = copy.deepcopy(base)
        bad["stages"] = [{"kind":kind,"target":[list(map(str,matrix(x))) for x in base["source"]]}]
        require(certify(bad)["reason"] == reason, "Failed guard accepted"); negatives += 1
    bad = copy.deepcopy(base); bad["R"] = 1
    require(certify(bad)["reason"] == "source radius", "Radius guard"); negatives += 1
    for field,value in [("variance",0),("R",True),("j",-1),("weights",[1]*18),
                        ("source_anchor",[0,0]),("variance",0.5),("stages",[{"kind":"unverified"}])]:
        bad=copy.deepcopy(base);bad[field]=value
        try:
            certify(bad)
        except (ValueError,ZeroDivisionError):
            negatives += 1
        else:
            raise ValueError("Malformed input accepted")
    return {"status":"MOTION_CHAIN_STRICTNESS_CONTROLS_PASS","calibration":record,
            "posterior_rate_cases":posterior_cases,"pressure_transform_cases":pressure_cases,
            "suffix_budget_cases":suffix_cases,"subdivision_counts":subdivision,
            "small_loss_controls":small_loss,"independent_frame_cases":frame_cases,
            "radial_cutoff_cases":cutoff_cases,
            "negative_controls":negatives,"content_pins":pin_sources(),
            "trust_boundary":"Exact finite author controls; analytic pressure, limits and openness are written proofs"}


def main():
    if len(sys.argv)==2:
        out=certify(json.loads(Path(sys.argv[1]).read_text()))
    else:
        require(len(sys.argv)==1,"Usage: verify.py [INPUT.json]")
        out=audit(json.loads((HERE/"INPUT.json").read_text()))
        require(out==json.loads((HERE/"EXPECTED.json").read_text()),"Expected record mismatch")
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
