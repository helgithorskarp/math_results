"""Check an all-threshold family certificate without importing its producer.

Supplied-record mode verifies inequalities; conservative nonminimal schedules
are allowed. The default suite is an author check, not independent review.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def need(ok, label):
    if not ok:
        raise ValueError(label)


def rat(x):
    need(type(x) in (int, str), "rational encoding")
    return F(x)


def nat(x, minimum=0):
    need(type(x) is int and x >= minimum, "integer domain")
    return x


def vec(v):
    need(type(v) is list and len(v) == 3, "vector shape")
    return tuple(map(rat, v))


def inner(x, y):
    return sum(a*b for a, b in zip(x, y))


def difference(x, y):
    return tuple(a-b for a, b in zip(x, y))


def encode(v):
    if isinstance(v, F):
        return str(v)
    if isinstance(v, (tuple, list)):
        return [encode(t) for t in v]
    if isinstance(v, dict):
        return {k: encode(t) for k, t in v.items()}
    return v


def check(data, cert):
    need(data["schema"] == "anchored-cloud-family-input-v1", "input schema")
    need(cert["schema"] == "anchored-cloud-family-certificate-v1", "record schema")
    need(cert["status"] == "CERTIFIED_UNIFORM_ALL_THRESHOLD_FAMILY", "record status")
    raw = [[vec(z) for z in data[key]] for key in ("source", "target")]
    anc = list(map(vec, data["anchors"]))
    need(len(anc) == 2 and len(raw[0]) == len(raw[1]) >= 2, "label/anchor shape")
    p, q = [[difference(z, anc[e]) for z in raw[e]] for e in (0, 1)]
    n = len(p)
    R, ell = nat(data["radius"], 1), nat(data["mass_exponent"])
    S = rat(data["variance_ratio"])
    need(S >= 1 and n <= (1 << ell), "variance or empty prior domain")
    for x, y in zip(p, q):
        need(inner(x, x) == inner(y, y) <= R**2, "anchor/radius")
    # Use the Gram form, rather than the producer's squared differences.
    losses = {(i, j): 2*(inner(q[i], q[j])-inner(p[i], p[j]))
              for i, j in itertools.combinations(range(n), 2)}
    need(all(t >= 0 for t in losses.values()), "pair expansion")
    sp, sq = [tuple(sum(row[k] for row in rows) for k in range(3)) for rows in (p, q)]
    # Equal anchored norms cancel the two diagonal trace terms.
    ordered_uniform_sum = 2*(inner(sq, sq)-inner(sp, sp))
    need(ordered_uniform_sum == 2*sum(losses.values()), "ordered loss normalization")
    d0 = ordered_uniform_sum / F(1 << (2*ell))
    need(0 < rat(cert["uniform_loss_floor"]) <= d0, "loss floor")
    a = nat(cert["normalized_loss_exponent"])
    need(F(1, 1 << a) <= rat(cert["uniform_loss_floor"])/S, "normalized loss guard")
    need(cert["labels"] == n and cert["unordered_pairs"] == len(losses)
         and cert["strict_pairs"] == sum(t > 0 for t in losses.values()), "pair counts")

    wc, wr = data["width_witness"], cert["width"]
    need(wc["kind"] == "nested-hulls-rational-cap-v1", "width witness kind")
    bary = [[rat(z) for z in row] for row in wc["target_in_source_hull"]]
    need(len(bary) == n, "hull row count")
    for row, y in zip(bary, q):
        need(len(row) == n and all(t >= 0 for t in row) and sum(row) == 1, "hull simplex")
        # Check a zero weighted residual, not a reconstructed target vector.
        need(all(sum(row[i]*(p[i][k]-y[k]) for i in range(n)) == 0 for k in range(3)),
             "hull residual")
    axis = vec(wc["cap_axis"])
    c, r = rat(wc["cap_cosine"]), rat(wc["cap_sine_upper"])
    nat(wc.get("perpendicular_bits", 16))
    star = nat(wc["source_witness"])
    need(star < n and inner(axis, axis) == 1 and 0 <= c < 1 and r >= 0
         and r*r+c*c >= 1, "cap domain")
    b = list(map(rat, wr["perpendicular_upper"]))
    need(len(b) == n and all(t >= 0 for t in b), "perpendicular bound shape")
    gamma, w = rat(wr["cap_gap_lower"]), rat(wr["lower"])
    need(gamma > 0 and 0 < w <= min(F(2*R), (1-c)*gamma/2), "width lower bound")
    for y, bound in zip(q, b):
        v = difference(p[star], y)
        axial = inner(axis, v)
        residual = tuple(v[i]-axial*axis[i] for i in range(3))
        need(axial >= 0 and inner(residual, residual) <= bound*bound, "cap transverse bound")
        need(c*axial-r*bound >= gamma, "cap support margin")

    z = cert["schedule"]
    A, Q0 = rat(z["tail_A"]), rat(z["tail_Q"])
    j, k, N, M, bw, B = [nat(z[key]) for key in
                        ("j", "k", "N", "M", "width_exponent", "budget_exponent")]
    need(A >= 6*(R+1)**2+2*S*(ell+1) and Q0 >= 8*A/w, "tail radius schedule")
    need(j >= Q0*Q0, "tail-to-middle crossing")
    need(k >= a+9*R*R+4, "peak separation")
    need(N >= 40*R*R+9*R+38+3*j+8*k, "middle coefficient")
    need(M >= a+N and F(1, 1 << bw) <= w/2, "middle loss or width exponent")
    # Crucially, 2**B and 2**M are never formed.
    need(B >= max(M+1, k, ell+1, 1, bw), "all-threshold error budget")
    conclusion = {
        "variance_interval": ["1", str(S)],
        "threshold_interval": "[0,infinity)",
        "prior_region": "v_i >= 2^-mass_exponent; sum v_i=1",
        "error_guard": "2*cloud_radius + l1(u-v) + l1(z-v) <= 2^-budget_exponent",
        "middle_gap_exponent": M+1,
        "actual_contraction_required": False,
        "diffuse_clouds_allowed": True,
        "independent_review": "PENDING",
    }
    need(cert["conclusion"] == conclusion, "conclusion overreach")
    source_diameter2 = max(inner(difference(x,y), difference(x,y)) for x in p for y in p)
    target_diameter2 = max(inner(difference(x,y), difference(x,y)) for x in q for y in q)
    return encode({"labels": n, "strict_pairs": sum(t > 0 for t in losses.values()),
                   "uniform_loss_floor": d0, "width_lower": w,
                   "budget_exponent": B, "variance_interval": [F(1), S],
                   "source_diameter_squared": source_diameter2,
                   "target_diameter_squared": target_diameter2,
                   "same_reference_strict_homothety_MGF_buffer_excluded":
                       target_diameter2 == source_diameter2 > 0})


def dependency_checks():
    pins = json.loads((HERE/"DEPENDENCIES.json").read_text())
    for pin in pins:
        content = (HERE/pin["path"]).read_bytes()
        need(hashlib.sha256(content).hexdigest() == pin["sha256"], "dependency changed: "+pin["path"])
    return len(pins)


def bad_case(data, record, label, change, which="record"):
    d, r = copy.deepcopy(data), copy.deepcopy(record)
    change(r if which == "record" else d)
    try:
        check(d, r)
    except (ValueError, KeyError, TypeError, ZeroDivisionError, IndexError):
        return label
    raise ValueError("damaged certificate accepted: "+label)


def suite(data, record):
    summary = check(data, record)
    bad = []
    for key in ("j", "k", "N", "M", "budget_exponent"):
        bad.append(bad_case(data, record, "understated_"+key,
                   lambda r, key=key: r["schedule"].__setitem__(key, r["schedule"][key]-1)))
    changes = [
        ("false_loss_floor", lambda r: r.__setitem__("uniform_loss_floor", "1")),
        ("false_width", lambda r: r["width"].__setitem__("lower", "1/2")),
        ("undersized_transverse_bound", lambda r: r["width"]["perpendicular_upper"].__setitem__(1, 0)),
        ("false_cap_gap", lambda r: r["width"].__setitem__("cap_gap_lower", "1")),
        ("false_variance_scope", lambda r: r["conclusion"].__setitem__("variance_interval", ["0", "infinity"])),
    ]
    for label, change in changes:
        bad.append(bad_case(data, record, label, change))
    inputs = [
        ("float_input", lambda d: d["source"][1].__setitem__(0, 1.0)),
        ("empty_prior_region", lambda d: d.__setitem__("mass_exponent", 2)),
        ("invalid_variance", lambda d: d.__setitem__("variance_ratio", "1/2")),
        ("anchor_mismatch", lambda d: d["target"][5].__setitem__(2, "1/2")),
        ("expanding_reference", lambda d: d["target"].__setitem__(3, [-1,0,0])),
        ("incorrect_hull_witness", lambda d: d["width_witness"]["target_in_source_hull"].__setitem__(6, [0,0,0,0,0,0,1])),
        ("nonunit_cap_axis", lambda d: d["width_witness"].__setitem__("cap_axis", [0,0,-2])),
        ("invalid_cap_sine", lambda d: d["width_witness"].__setitem__("cap_sine_upper", "1/2")),
        ("zero_loss", lambda d: d.__setitem__("target", copy.deepcopy(d["source"]))),
    ]
    for label, change in inputs:
        bad.append(bad_case(data, record, label, change, "input"))

    # A distinct direct covariance evaluation checks (9) at every vertex of
    # the prior polytope and a nonvertex. Universal validity is termwise,
    # not an inference from this finite calibration.
    p, q = [[vec(t) for t in data[key]] for key in ("source", "target")]
    n, m = len(p), F(1, 1 << data["mass_exponent"])
    priors = [[m+(1-n*m if i == j else 0) for i in range(n)] for j in range(n)]
    priors.append([F(1,n)]*n)
    cov_losses = []
    for prior in priors:
        def var(rows):
            mean = tuple(sum(v*x[k] for v,x in zip(prior,rows)) for k in range(3))
            return sum(v*inner(x,x) for v,x in zip(prior,rows))-inner(mean,mean)
        loss = 2*(var(p)-var(q))
        need(loss >= rat(record["uniform_loss_floor"]), "covariance calibration")
        cov_losses.append(str(loss))

    # Translation invariance is checked with independent endpoint translations.
    translated = copy.deepcopy(data)
    shifts = [(F(1,3),F(-2,7),F(5,11)), (F(-3,5),F(4,9),F(-1,13))]
    for e, key in enumerate(("source", "target")):
        translated[key] = [[str(rat(row[k])+shifts[e][k]) for k in range(3)] for row in data[key]]
        translated["anchors"][e] = [str(rat(data["anchors"][e][k])+shifts[e][k]) for k in range(3)]
    need(check(translated, record) == summary, "independent anchor translation")

    parameter_controls = []
    with tempfile.TemporaryDirectory(prefix="anchored-family-") as temp:
        for factor, variance, mass_bits in [(F(1,4),F(1),3), (F(1,2),F(3,2),4),
                                            (F(2),F(8),4), (F(3,2),F(16),5)]:
            d = copy.deepcopy(data)
            for key in ("source", "target", "anchors"):
                d[key] = [[str(factor*rat(t)) for t in row] for row in data[key]]
            d["radius"] = max(1, -(-factor.numerator//factor.denominator))
            d["variance_ratio"] = str(variance)
            d["mass_exponent"] = mass_bits
            inp = Path(temp)/"input.json"
            inp.write_text(json.dumps(d))
            produced = json.loads(subprocess.check_output(
                [sys.executable, "-B", str(HERE/"certificate.py"), str(inp)]))
            checked = check(d, produced)
            parameter_controls.append({"scale": str(factor), "variance_max": str(variance),
                                       "mass_exponent": mass_bits,
                                       "budget_exponent": checked["budget_exponent"]})

    # Check the producer entry point as a subprocess, not by importing it.
    output = subprocess.check_output([sys.executable, "-B", str(HERE/"certificate.py"), str(HERE/"INPUT.json")])
    need(json.loads(output) == record, "producer/record disagreement")
    need(output == (HERE/"CERTIFICATE.json").read_bytes(), "canonical producer bytes")
    return {"status": "EFFECTIVE_ANCHORED_FAMILY_EXACT_CONTROLS_PASS",
            "certificate_sha256": hashlib.sha256(output).hexdigest(),
            "family": summary, "dependency_pins": dependency_checks(),
            "negative_controls": bad, "covariance_prior_controls": cov_losses,
            "parameter_controls": parameter_controls,
            "independent_endpoint_translation": "PASS",
            "integer_inequality_checker_imports_producer": False,
            "dyadic_budget_denominator_materialized": False,
            "trust_boundary": "Written analytic proof and imported kernel/peak/tail lemmas; author controls, not peer review."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--certificate", type=Path)
    args = parser.parse_args()
    need((args.input is None) == (args.certificate is None), "supply both input and certificate")
    inp = args.input if args.input is not None else HERE/"INPUT.json"
    rec = args.certificate if args.certificate is not None else HERE/"CERTIFICATE.json"
    data, record = json.loads(inp.read_text()), json.loads(rec.read_text())
    result = ({"status": "UNIFORM_ALL_THRESHOLD_CERTIFICATE_VERIFIED", "family": check(data, record),
               "dependency_pins": dependency_checks()} if args.input is not None else suite(data, record))
    print(json.dumps(result, sort_keys=True, indent=2))
