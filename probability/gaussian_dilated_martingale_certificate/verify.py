"""Check compact martingale records using explicit coupling masses.

The supplied-record path imports no producer code. The control runner calls
the producer, then checks its output by ordered pairs and both marginals.
"""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parent


def need(test, why):
    if not test:
        raise ValueError(why)


def scalar(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def dist2(a, b):
    return sum((x-y)**2 for x, y in zip(a, b))


def rank(rows):
    rows = [[F(v) for v in row] for row in rows]
    k = 0
    for j in range(len(rows[0])):
        i = next((i for i in range(k, len(rows)) if rows[i][j]), None)
        if i is None:
            continue
        rows[k], rows[i] = rows[i], rows[k]
        divisor = rows[k][j]
        rows[k] = [v/divisor for v in rows[k]]
        for i in range(len(rows)):
            if i != k:
                factor = rows[i][j]
                rows[i] = [v-factor*w for v, w in zip(rows[i], rows[k])]
        k += 1
        if k == len(rows):
            break
    return k


def exact_input(data):
    raw = [v for row in data["sources"]+data["targets"] for v in row]+data["weights"]
    raw += [data.get("variance", 1), data.get("dilation", 2)]
    need(all(type(v) in (int, str) for v in raw), "exact rational input")
    x, y = [[[F(v) for v in row] for row in data[key]] for key in ("sources", "targets")]
    p = list(map(F, data["weights"]))
    s, a = F(data.get("variance", 1)), F(data.get("dilation", 2))
    need(len(x) == len(y) == len(p) > 0 and all(len(row) == 3 for row in x+y), "dimensions")
    need(s > 0 and a > 1 and min(p) >= 0 and sum(p) == 1, "probability and parameters")
    keep = [i for i, w in enumerate(p) if w]
    x, y, p = [[z[i] for i in keep] for z in (x, y, p)]
    n = len(p)
    D = F(0);Q = F(0)
    for i, j in product(range(n), repeat=2):
        loss = dist2(x[i], x[j])-dist2(y[i], y[j])
        need(loss >= 0, "original contraction")
        D += p[i]*p[j]*loss
        Q += p[i]*p[j]*(loss/s)**2
    means = [[sum(p[i]*cloud[i][j] for i in range(n)) for j in range(3)] for cloud in (x, y)]
    centered = [[[row[j]-mean[j] for j in range(3)] for row in cloud]
                for cloud, mean in zip((x, y), means)]
    cov = [[sum(p[i]*p[j]*(x[i][k]-x[j][k])*(x[i][l]-x[j][l])
                for i in range(n) for j in range(n))/2 for l in range(3)] for k in range(3)]
    V = sum(cov[i][i] for i in range(3))
    B = max(sum(p[j]*dist2(x[i], x[j]) for j in range(n))-V for i in range(n))
    return centered[0], centered[1], p, s, a, cov, V, B, D, Q


def check_record(data, record):
    x, y, p, s, a, cov, V, B, D, Q = exact_input(data)
    n = len(p)
    need(record["schema"] == "dilated-martingale-v1" and record["active_sites"] == n, "schema and sites")
    for key, value in [("variance", s), ("dilation", a), ("source_scatter", V),
                       ("source_radius_squared", B), ("pair_loss", D)]:
        need(F(record[key]) == value, "record "+key)
    status = record["status"]
    need(status in ("ISOMETRIC_ZERO", "UNRESOLVED", "SIGNED_ALL_THRESHOLDS",
                    "UNRESOLVED_AT_REQUESTED_VARIANCE"), "status")
    stats = {"paired_affine_rank":rank([[1]+z+w for z, w in zip(x, y)])-1,
             "pair_loss":str(D), "normalized_loss":str(D/s),
             "Q_over_normalized_loss":str(Q/(D/s)) if D else None}
    if status == "ISOMETRIC_ZERO":
        need(D == 0, "zero-loss equality")
        return dict(stats, result="ISOMETRIC_ZERO_CHECK_PASS")
    if status == "UNRESOLVED":
        return dict(stats, result="NO_SIGN_ASSERTED")
    need(D > 0 and V > 0 and B >= V, "positive loss and scatter")
    matrix = [[F(v) for v in row] for row in record["matrix"]]
    need(len(matrix) == 3 and all(len(row) == 3 for row in matrix), "matrix dimensions")
    for i, j in product(range(3), repeat=2):
        need(sum(cov[i][k]*matrix[k][j] for k in range(3)) == (a if i == j else 0),
             "covariance inverse certificate")
    # Different representation: evaluate every mass and stream its marginals.
    rows = [F(0)]*n;cols = [F(0)]*n;means = [[F(0)]*3 for _ in range(n)]
    minimum = None;zeros = 0
    for i, j in product(range(n), repeat=2):
        kernel = 1+sum(x[i][k]*matrix[k][l]*y[j][l] for k, l in product(range(3), repeat=2))
        mass = p[i]*p[j]*kernel
        need(mass >= 0, "negative coupling mass")
        minimum = kernel if minimum is None else min(minimum, kernel)
        zeros += mass == 0
        rows[i] += mass;cols[j] += mass
        for k in range(3):
            means[j][k] += mass*x[i][k]
    for i in range(n):
        need(rows[i] == p[i], "source marginal")
    for j in range(n):
        need(cols[j] == p[j], "target marginal")
        for k in range(3):
            need(means[j][k] == p[j]*a*y[j][k],
                 "dilated conditional mean")
    need(F(record["minimum_kernel"]) == minimum, "minimum kernel")
    eta = (a-1)*V/(96*a*B)
    cutoff = 4224*a*B*B/((a-1)*V)
    floor = 2*(1-a**-2)*V
    for key, value in [("spherical_gap", eta), ("variance_cutoff", cutoff), ("pair_loss_floor", floor)]:
        need(F(record[key]) == value, "record "+key)
    need(D >= floor and cutoff >= 8*B and cutoff*eta == 44*B, "endpoint budget")
    need(record["certified_thresholds"] == "[0,infinity)"
         and record["certified_variances"] == "[variance_cutoff,infinity)", "intervals")
    need((status == "SIGNED_ALL_THRESHOLDS") == (s >= cutoff), "requested variance")
    return dict(stats, result="DILATED_MARTINGALE_RECORD_PASS", coupling_entries=n*n,
                zero_coupling_entries=zeros,
                coupled_squared_residual=str(V-a*a*sum(p[j]*scalar(y[j], y[j]) for j in range(n))))


def encode(x, y, weights, variance=25344, dilation=2):
    return {"sources":[list(map(str, z)) for z in x], "targets":[list(map(str, z)) for z in y],
            "weights":list(map(str, weights)), "variance":str(variance), "dilation":str(dilation)}


def controls():
    x = list(product([-1, 1], repeat=3))
    def folded(c):
        return [[c*abs(z[0]+z[1])/2, c*abs(z[1]+z[2])/2, c*abs(z[2]+z[0])/2] for z in x]
    base = encode(x, folded(F(1, 12)), [F(1, 8)]*8)
    boundary = encode(x, folded(F(1, 3)), [F(1, 8)]*8)
    negative = encode(x, folded(F(1, 2)), [F(1, 8)]*8)
    below = deepcopy(base);below["variance"] = "25343"
    equal = encode(x, x, [F(1, 8)]*8, variance=1)
    rare = F(1, 2**100)
    weights = [(rare if z[0] == 1 else 1-rare)/4 for z in x]
    tiny = encode(x, folded(F(1, 2**120)), weights, variance=1000000)
    plane = encode([[a,b,0] for a,b in product([-1,1], repeat=2)],
                   [[abs(a+b)/4,0,0] for a,b in product([-1,1], repeat=2)], [F(1,4)]*4)
    # Dilation of the matched map need not be a contraction.
    z = list(x)+[[F(sign,1000) if j == axis else F(0) for j in range(3)]
                 for axis, sign in product(range(3),[-1,1])]
    clipped = encode(z,[[max(F(-1,100),min(F(1,100),v)) for v in row] for row in z],
                     [F(1,14)]*14,variance=1000000)
    return {"family":base, "kernel_equality":boundary, "negative_kernel":negative,
            "below_variance":below, "isometry":equal, "tiny_mass":tiny,
            "singular":plane, "dilated_map_expands":clipped}


def checks():
    from certificate import produce
    inputs = json.loads((ROOT/"INPUTS.json").read_text())
    for v in inputs:
        need(sha256((ROOT/v["relative_path"]).read_bytes()).hexdigest() == v["sha256"], "source pin")
    need(F(9,64)-F(1,8) == F(1,64), "threshold overlap")
    need(F(4) > F(3), "e<3 implies exp(-1/2)>1/2")
    # Universal parameter budgets, evaluated without exponentials.
    schedules = 0
    for a, B, rho in product([F(3,2),F(2),F(3),F(5)],
                            [F(1,16),F(1),F(3),F(10000)],
                            [F(1,3),F(1,12),F(1,256),F(1,2**100)]):
        kappa = rho*B;c = kappa/(2*a*B);r2 = (2*c)**2*B
        bound = 1408*a*B*B/((a-1)*kappa)
        need(a*a*B*r2 == kappa*kappa and c < 1, "uniform product-kernel budget")
        for V in [3*kappa, B]:
            eta = (a-1)*V/(96*a*B)
            cutoff = 4224*a*B*B/((a-1)*V)
            need(cutoff <= bound and cutoff*eta == 44*B and cutoff > 8*B, "uniform endpoint budget")
        schedules += 1
    cases = controls();records = {};stats = {}
    for name, data in cases.items():
        records[name] = produce(data);stats[name] = check_record(data, records[name])
    for name in ["family", "kernel_equality", "tiny_mass", "dilated_map_expands"]:
        need(records[name]["status"] == "SIGNED_ALL_THRESHOLDS", "signed control")
        need(stats[name]["paired_affine_rank"] == 6, "rank-six control")
    need(stats["kernel_equality"]["zero_coupling_entries"] > 0, "zero coupling masses")
    need(records["negative_kernel"]["status"] == "UNRESOLVED", "failed sufficient kernel")
    need(records["below_variance"]["status"] == "UNRESOLVED_AT_REQUESTED_VARIANCE", "variance boundary")
    need(records["isometry"]["status"] == "ISOMETRIC_ZERO", "zero loss")
    need(records["singular"]["reason"] == "singular source covariance", "singular branch")
    z,w,_,_,a,_,_,_,_,_ = exact_input(cases["dilated_map_expands"])
    need(any(a*a*dist2(w[i],w[j]) > dist2(z[i],z[j])
             for i,j in product(range(len(z)),repeat=2)), "coupling is not the dilated deterministic map")
    # These concrete parameters lie outside three currently used middle guards.
    d = F(stats["family"]["normalized_loss"])
    need(d > F(1,2**360) and F(stats["family"]["Q_over_normalized_loss"]) > F(1,2**48), "other worked cutoffs")
    need(F(1,576*25344) > d*d/F(2**86), "outside covariance-collapse cutoff")
    # Independent orthogonal rotations preserve the law-level certificate.
    rotated = deepcopy(cases["family"])
    rotated["targets"] = [[str(F(3,5)*F(a)-F(4,5)*F(b)),str(F(4,5)*F(a)+F(3,5)*F(b)),str(c)]
                          for a,b,c in rotated["targets"]]
    rr = produce(rotated);check_record(rotated, rr)
    need(rr["status"] == "SIGNED_ALL_THRESHOLDS", "rotation")
    scaled = deepcopy(cases["family"])
    for key in ["sources", "targets"]:
        scaled[key] = [[str(3*F(v)+(5 if key == "sources" else -7)) for v in z] for z in scaled[key]]
    scaled["variance"] = str(9*F(scaled["variance"]))
    sr = produce(scaled);check_record(scaled, sr)
    need(F(sr["variance_cutoff"]) == 9*F(records["family"]["variance_cutoff"]), "scale covariance")
    need(sr["spherical_gap"] == records["family"]["spherical_gap"], "scale invariant gap")
    zero = deepcopy(cases["family"])
    zero["sources"].append(["0"]*3);zero["targets"].append(["100"]*3);zero["weights"].append("0")
    need(produce(zero) == records["family"], "zero mass removal")
    rejected = 0
    damaged = []
    for key, value in [("spherical_gap","1"),("variance_cutoff","1"),("pair_loss_floor","0"),
                       ("minimum_kernel","1"),("certified_variances","[0,infinity)")]:
        r = deepcopy(records["family"]);r[key] = value;damaged.append(r)
    r = deepcopy(records["family"]);r["matrix"][0][0] = "3";damaged.append(r)
    r = deepcopy(records["below_variance"]);r["status"] = "SIGNED_ALL_THRESHOLDS"
    for data, r in [(cases["family"],z) for z in damaged]+[(cases["below_variance"],r)]:
        try:check_record(data,r)
        except ValueError:rejected += 1
        else:raise RuntimeError("damaged certificate accepted")
    for key, value in [("dilation",1),("variance",0),("variance",1.0),
                       ("weights",["-1"]+["2/7"]*7)]:
        bad = deepcopy(cases["family"]);bad[key] = value
        try:produce(bad)
        except ValueError:rejected += 1
        else:raise RuntimeError("malformed input accepted")
    bad = encode([[0,0,0],[0,0,0]],[[0,0,0],[1,0,0]],[F(1,2)]*2)
    try:produce(bad)
    except ValueError:rejected += 1
    else:raise RuntimeError("duplicate-source expansion accepted")
    return {"status":"DILATED_MARTINGALE_UNIFORM_FAMILY_PASS", "pinned_sources":len(inputs),
            "parameter_schedules":schedules, "rejected_inputs":rejected,
            "records":records, "coupling_checks":stats,
            "rotated_record_sha256":sha256(json.dumps(rr,sort_keys=True).encode()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit",action="store_true")
    parser.add_argument("--input")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    if args.input or args.certificate:
        if not(args.input and args.certificate) or args.emit:
            parser.error("use --input and --certificate together")
        out = check_record(json.loads(Path(args.input).read_text()),json.loads(Path(args.certificate).read_text()))
        print(json.dumps(out,sort_keys=True,indent=2))
    else:
        out = checks()
        if not args.emit:
            need(out == json.loads((ROOT/"EXPECTED.json").read_text()), "expected record")
        print(json.dumps(out,sort_keys=True,indent=2))
        if not args.emit:
            print("record_sha256",sha256(json.dumps(out,sort_keys=True,separators=(",",":")).encode()).hexdigest())
