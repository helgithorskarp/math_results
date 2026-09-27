"""Exact author audit; supplied-record checking imports no producer code."""
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


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(z):
    require(type(z) in (int, str), "exact rational encoding required")
    return F(z)


def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)): return [encode(v) for v in x]
    return x


def dot(x, y): return sum(a*b for a, b in zip(x, y))
def minus(x, y): return [a-b for a, b in zip(x, y)]
def mv(a, v): return [dot(row, v) for row in a]
def plus(x, y): return [a+b for a, b in zip(x, y)]
def norm2(x): return dot(x, x)


def psd(a):
    """Rational Schur elimination, rather than the producer's minors."""
    n = len(a)
    if n == 0: return True
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)): return False
    if any(a[i][i] < 0 for i in range(n)): return False
    positive = next((i for i in range(n) if a[i][i] > 0), None)
    if positive is None: return all(z == 0 for row in a for z in row)
    ids = [i for i in range(n) if i != positive]
    return psd([[a[i][j]-a[i][positive]*a[positive][j]/a[positive][positive]
                 for j in ids] for i in ids])


def analyze(data):
    boxes = []
    for b in data["components"]:
        c, d, h = [list(map(rational, b[key])) for key in
                    ("source_center", "target_center", "halfwidths")]
        a = [list(map(rational, row)) for row in b["matrix"]]
        p = rational(b["weight"])
        require(len(c) == len(d) == len(h) == len(a) == 3 and all(len(row) == 3 for row in a),
                "bad box dimension")
        require(p > 0 and min(h) > 0, "empty auxiliary component")
        slack = [[F(i == j)-sum(a[k][i]*a[k][j] for k in range(3))
                  for j in range(3)] for i in range(3)]
        require(psd(slack), "expanding linear part")
        boxes.append(dict(c=c, d=d, h=h, a=a, p=p))
    require(len(boxes) >= 2 and sum(b["p"] for b in boxes) == 1, "invalid component probabilities")
    k, kap = [rational(data[key]) for key in ("global_covariance_floor", "component_covariance_floor")]
    require(min(k, kap) > 0 and all(h*h/3 >= kap for b in boxes for h in b["h"]), "bad covariance floor")

    # Rational product quadrature is exact for the uniform box's moments
    # through coordinate degree two, including the paired Gram square.
    points, weights, corners, corner_box = [], [], [], []
    one = [(-1, F(1, 6)), (0, F(2, 3)), (1, F(1, 6))]
    for index, b in enumerate(boxes):
        for states in itertools.product(one, repeat=3):
            u = [b["h"][j]*states[j][0] for j in range(3)]
            weight = b["p"]
            for _, w in states: weight *= w
            points.append((plus(b["c"], u), plus(b["d"], mv(b["a"], u))))
            weights.append(weight)
        for signs in itertools.product((-1, 1), repeat=3):
            corners.append(plus(b["c"], [h*s for h, s in zip(b["h"], signs)]))
            corner_box.append(index)
    mx, my = [[sum(w*z[side][j] for w, z in zip(weights, points)) for j in range(3)]
              for side in (0, 1)]
    centered = [(minus(x, mx), minus(y, my)) for x, y in points]
    cov = [[sum(w*x[i]*x[j] for w, (x, _) in zip(weights, centered))
            for j in range(3)] for i in range(3)]
    require(psd([[cov[i][j]-k*F(i == j) for j in range(3)] for i in range(3)]), "global covariance fails")
    gram, D = F(0), F(0)
    for i, (x, y) in enumerate(centered):
        for j, (xx, yy) in enumerate(centered):
            weight = weights[i]*weights[j]
            gram += weight*(dot(x, xx)-dot(y, yy))**2
            D += weight*(norm2(minus(x, xx))-norm2(minus(y, yy)))
    diam2 = max(norm2(minus(x, y)) for x in corners for y in corners)

    # Subtract the two PSD quadratic terms from the actual distance loss.
    # What remains is multiaffine and attains its minimum at a corner.
    lower = None
    for i, a in enumerate(boxes):
        for b in boxes[:i]:
            for signs in itertools.product((-1, 1), repeat=6):
                u = [a["h"][j]*signs[j] for j in range(3)]
                v = [b["h"][j]*signs[j+3] for j in range(3)]
                Au, Bv = mv(a["a"], u), mv(b["a"], v)
                x, y = plus(a["c"], u), plus(b["c"], v)
                tx, ty = plus(a["d"], Au), plus(b["d"], Bv)
                remainder = (norm2(minus(x, y))-norm2(minus(tx, ty))
                             -(norm2(u)-norm2(Au))-(norm2(v)-norm2(Bv)))
                lower = remainder if lower is None else min(lower, remainder)
    return dict(boxes=boxes, k=k, kap=kap, gram=gram, D=D, diam2=diam2,
                independently_certified_cross_lower=lower, cubature_points=len(points))


def validate_record(state, record):
    boxes, k, kap = state["boxes"], state["k"], state["kap"]
    m, gram, D, diam2 = min(b["p"] for b in boxes), state["gram"], state["D"], state["diam2"]
    delta = rational(record["cross_loss_lower"])
    require(delta <= state["independently_certified_cross_lower"], "unproved cross-domain lower bound")
    e, cost = 2*gram/(k*m), 4+78*diam2/kap
    expected = dict(schema="affine-component-localization-v1", components=len(boxes),
                    auxiliary_law="uniform volume in each source box with supplied component weights",
                    actual_prior_unrestricted=True, diameter_squared=str(diam2),
                    global_covariance_floor=str(k), component_covariance_floor=str(kap),
                    component_mass_floor=str(m), squared_gram_norm=str(gram), mean_pair_loss=str(D),
                    aligned_error_per_component=str(e), cross_loss_lower=str(delta),
                    motion_constant=str(cost), orientation_slack=str(kap/4-e),
                    cross_slack=str(delta-cost*e))
    if delta < 0:
        expected.update(status="UNRESOLVED", reason="whole-box cross contraction not certified")
    elif gram == 0:
        expected.update(status="CONGRUENT_EQUALITY", certified_variances="(0,infinity)",
                        certified_thresholds="[0,infinity)", arbitrary_ball_radii=True)
    elif e > kap/4 or delta < cost*e:
        expected.update(status="UNRESOLVED", reason="motion budget not certified")
    else:
        require(D >= 0, "negative mean loss")
        expected.update(status="CERTIFIED_ALL_VARIANCE_SUPPORT", certified_variances="(0,infinity)",
                        certified_thresholds="[0,infinity)", arbitrary_ball_radii=True)
    require(record == expected, "certificate field mismatch")
    return record["status"]


def producer(data, invalid=False):
    with tempfile.TemporaryDirectory(prefix="affine-component-") as folder:
        path = Path(folder)/"input.json"; path.write_text(json.dumps(encode(data)))
        flags = ["-B"]+(["-O"] if sys.flags.optimize else [])
        result = subprocess.run([sys.executable, *flags, str(HERE/"certificate.py"), str(path)],
                                capture_output=True, text=True)
    if invalid:
        require(result.returncode != 0, "malformed data accepted"); return
    require(result.returncode == 0, result.stderr)
    return json.loads(result.stdout)


def pins():
    repo = HERE.parents[1]
    records = json.loads((HERE/"INPUTS.json").read_text())
    for entry in records:
        path = (HERE/entry["relative_path"]).resolve().relative_to(repo).as_posix()
        raw = subprocess.run(["git", "show", entry["file_commit"]+":"+path],cwd=repo,
                             check=True,capture_output=True).stdout
        require(hashlib.sha256(raw).hexdigest() == entry["sha256"], "dependency bytes changed")
    return len(records)


def audit():
    data = json.loads((HERE/"INPUT.json").read_text()); record = producer(data)
    require(record == json.loads((HERE/"CERTIFICATE.json").read_text()), "fixture changed")
    state = analyze(data); validate_record(state, record)
    require(record["status"] == "CERTIFIED_ALL_VARIANCE_SUPPORT", "fixture unresolved")
    require(state["cubature_points"] == 81, "wrong moment rule")
    for power, value in [(0, F(1)), (1, F(0)), (2, F(1, 3)), (3, F(0))]:
        require(sum(w*F(x)**power for x, w in [(-1,F(1,6)),(0,F(2,3)),(1,F(1,6))]) == value,
                "one-dimensional cubature")

    # A universal rational-circle identity, checked coefficient by coefficient.
    def mul(a,b):
        out=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):out[i+j]+=x*y
        return out
    lhs=mul([1,0,-1],[1,0,-1]);extra=mul([0,2],[0,2])
    for i,v in enumerate(extra):lhs[i]+=v
    require(lhs == mul([1,0,1],[1,0,1]), "rotation polynomial identity")
    require(74+F(25,8) < 78 and F(515,4)>128, "continuous bound constants")
    require(12*12640320 <= 2**72 and 272380*12640320 <= 128*2**36,
            "whole interval budget")
    t=F(1,2**36)
    require(state["D"] == F(4102,9)*(2*t-t*t), "mean-loss polynomial")
    require(F(record["cross_loss_lower"]) >= 128*t, "whole-box versus analytic floor")

    # Equality and independent target isometries. The covariance certificate
    # concerns the auxiliary law, not the priors of an arbitrary tested mu.
    equality=copy.deepcopy(data)
    for b in equality["components"]:
        b["target_center"]=b["source_center"][:]
        b["matrix"]=[[int(i==j) for j in range(3)] for i in range(3)]
    eq=producer(equality); validate_record(analyze(equality),eq)
    require(eq["status"] == "CONGRUENT_EQUALITY", "zero loss")
    scaled=copy.deepcopy(data)
    for b in scaled["components"]:
        b["source_center"]=[3*F(x)+z for x,z in zip(b["source_center"],[7,11,-5])]
        b["target_center"]=[3*F(x)*s+z for x,s,z in zip(b["target_center"],[-1,1,1],[-13,17,19])]
        b["halfwidths"]=[3*F(h) for h in b["halfwidths"]]
        b["matrix"]=[[F(x)*(-1 if i==0 else 1) for x in row] for i,row in enumerate(b["matrix"])]
    for key in ["global_covariance_floor","component_covariance_floor"]:scaled[key]=9*F(scaled[key])
    sr=producer(scaled); validate_record(analyze(encode(scaled)),sr)
    require(sr["motion_constant"] == record["motion_constant"] and
            F(sr["aligned_error_per_component"]) == 9*F(record["aligned_error_per_component"]) and
            F(sr["cross_slack"]) == 9*F(record["cross_slack"]), "scale/isometry law")

    # Wrong global translation of one component is a failed cross guard,
    # not an adverse Gaussian hinge. A constant map fails the small-error
    # guard despite having a separately known positive comparison.
    failed=[]
    for name in ["cross_expansion","large_error"]:
        bad=copy.deepcopy(equality)
        if name=="cross_expansion":bad["components"][0]["target_center"][0]-=100
        else:
            for b in bad["components"]:
                b["target_center"]=[0,0,0];b["matrix"]=[[0]*3 for _ in range(3)]
        result=producer(bad);validate_record(analyze(bad),result)
        require(result["status"] == "UNRESOLVED", "failed guard signed");failed.append(name)

    bad_records=[]
    for key,value in [("cross_loss_lower","1000000"),("squared_gram_norm","0"),
                      ("motion_constant","4"),("actual_prior_unrestricted",False),
                      ("arbitrary_ball_radii",False),("orientation_slack","0")]:
        bad=copy.deepcopy(record);bad[key]=value
        try:validate_record(state,bad)
        except ValueError:bad_records.append(key)
        else:raise ValueError("damaged record accepted")
    bad_inputs=[]
    for name in ["zero_weight","wrong_total","float","width","component_floor",
                 "global_floor","matrix_expansion","dimension"]:
        bad=copy.deepcopy(data)
        if name=="zero_weight":bad["components"][0]["weight"]=0
        if name=="wrong_total":bad["components"][0]["weight"]="1/2"
        if name=="float":bad["global_covariance_floor"]=0.25
        if name=="width":bad["components"][0]["halfwidths"][0]=0
        if name=="component_floor":bad["component_covariance_floor"]=1
        if name=="global_floor":bad["global_covariance_floor"]=10000
        if name=="matrix_expansion":bad["components"][0]["matrix"][0][0]=2
        if name=="dimension":bad["components"][0]["source_center"]=[0,0]
        producer(bad,invalid=True)
        try:analyze(bad)
        except (ValueError,IndexError):bad_inputs.append(name)
        else:raise ValueError("checker accepted malformed input")

    return dict(status="AFFINE_COMPONENT_LOCALIZATION_PASS",byte_pins=pins(),
                fixture=record,cubature_points=state["cubature_points"],
                independent_corner_floor=str(state["independently_certified_cross_lower"]),
                whole_interval="0<=t<=2^-36",coefficient_margin="7/8",
                unresolved_controls=failed,rejected_records=bad_records,rejected_inputs=bad_inputs,
                scale_factor=3,equality=eq["status"])


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input");parser.add_argument("--certificate");parser.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.input or args.certificate:
        require(args.input and args.certificate,"supply both input and certificate")
        state=analyze(json.loads(Path(args.input).read_text()))
        status=validate_record(state,json.loads(Path(args.certificate).read_text()))
        out=dict(status="SUPPLIED_AFFINE_COMPONENT_RECORD_PASS",mathematical_status=status)
    else:
        out=audit()
        if not args.emit:require(out==json.loads((HERE/"EXPECTED.json").read_text()),"expected output drift")
    print(json.dumps(out,sort_keys=True,indent=2))
