"""Exact author audit. Supplied-record mode imports no producer code."""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import lcm
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(value):
    require(type(value) in (int, str), "exact rational encoding required")
    return F(value)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [encode(v) for v in value]
    return value


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def minus(x, y):
    return [a-b for a, b in zip(x, y)]


def read_geometry(data):
    x, y = [[list(map(rational, row)) for row in data[key]]
            for key in ("sources", "targets")]
    p = list(map(rational, data["weights"]))
    require(p and len(x) == len(y) == len(p) and all(len(v) == 3 for v in x+y)
            and all(w >= 0 for w in p) and sum(p) == 1, "invalid weighted pair")
    keep = [i for i, w in enumerate(p) if w]
    x, y, p = [[rows[i] for i in keep] for rows in (x, y, p)]
    n = len(p)
    # Center by averaged pair differences, independently of the producer.
    x, y = [[[sum(v[k]-u[k] for u in rows)/n for k in range(3)]
             for v in rows] for rows in (x, y)]
    R0, r, rho = [rational(data[key]) for key in
                  ("reference_radius", "cloud_radius", "relative_weight_error")]
    require(R0 > 0 and r >= 0 and 0 <= rho <= F(1, 2), "invalid neighborhood")
    require(all(dot(v, v) <= R0*R0 for v in x+y), "radius does not enclose sites")
    for i, j in itertools.combinations(range(n), 2):
        dx, dy = minus(x[i], x[j]), minus(y[i], y[j])
        require(dot(dx, dx) >= dot(dy, dy), "reference expands")
    # Recover the ordered mean pair loss from two marginal covariances.
    def scatter(rows):
        mean = [sum(p[i]*rows[i][k] for i in range(n)) for k in range(3)]
        return sum(p[i]*dot(rows[i], rows[i]) for i in range(n))-dot(mean, mean)
    D0 = 2*(scatter(x)-scatter(y))
    M = data["mesh"]
    B = data.get("rounding_bits", max(32, 4*M.bit_length()) if type(M) is int else 0)
    require(type(M) is int and M >= 1 and type(B) is int and B >= 1, "invalid mesh")
    return x, y, p, R0, r, rho, D0, M, B


def chart_sum(x, y, R0, M, B, direct=False):
    """Pair antipodal charts; optionally integrate cell values as Fractions."""
    pts = [[z/R0 for z in v] for v in x+y]
    den = lcm(*(z.denominator for v in pts for z in v))
    pts = [tuple(int(den*z) for z in v) for v in pts]
    xx, yy = pts[:len(x)], pts[len(x):]
    scale, total, negatives = 2**B, 0, 0
    exact = F(0)
    for axis in range(3):
        for a, b in itertools.product(range(1-M, M, 2), repeat=2):
            z = [a, b]
            z.insert(axis, M)
            denominator = den*sum(t*t for t in z)**2
            for sign in (1, -1):
                v = tuple(sign*t for t in z)
                gap = max(dot(row, v) for row in xx)-max(dot(row, v) for row in yy)
                numerator = 4*M*gap
                quotient, remainder = divmod(scale*numerator, denominator)
                require(0 <= remainder < denominator, "wrong rounding direction")
                total += quotient
                negatives += int(numerator < 0)
                if direct:
                    # Evaluate the chart integrand with rational coordinates,
                    # rather than the producer's integer cell formula.
                    vq = [F(t, M) for t in v]
                    cx = [[F(t, den) for t in row] for row in xx]
                    cy = [[F(t, den) for t in row] for row in yy]
                    g = max(dot(row, vq) for row in cx)-max(dot(row, vq) for row in cy)
                    exact += F(4, M*M)*g/dot(vq, vq)**2
    if direct:
        require(F(total, scale) <= exact <= F(total, scale)+F(6*M*M, scale),
                "cell formula or floor aggregate mismatch")
    return total, negatives


def expected_record(data):
    x, y, p, R0, r, rho, D0, M, B = read_geometry(data)
    total, _ = chart_sum(x, y, R0, M, B)
    I = F(total, 2**B)-F(480, M)
    w = R0*I/16 if I > 0 else None
    R, d = R0+r, (1-rho)**2*D0-16*R0*r-8*r*r
    q = (1-rho)*min(p)
    k = 0
    while 2**k*q < 1:
        k += 1
    out = dict(schema="support-cap-localization-v1", active_sites=len(p),
               width=dict(mesh=M, rounding_bits=B, face_cells=6*M*M,
                          normalized_floor_sum=total, normalized_integral_lower=str(I),
                          reference_width_lower=None if w is None else str(w)),
               reference_radius=str(R0), reference_loss=str(D0), cloud_radius=str(r),
               relative_weight_error=str(rho), actual_radius=str(R), actual_loss_lower=str(d),
               aggregate_mass_lower=str(q), mass_exponent=k,
               actual_cloud_contraction_required=True, common_label_weights_required=True,
               analytical_premise="universal spherical comparison6494 and endpoint6032/6048")
    if w is None:
        return dict(out, status="UNRESOLVED", reason="width not certified at this mesh")
    b = w-2*r
    out["tail_slope_lower"] = str(b)
    if min(b, d) <= 0:
        return dict(out, status="UNRESOLVED", reason="nonpositive width or loss reserve")
    z = R*(k+1)/b
    N = max(1, z.numerator//z.denominator+int(z.denominator != 1))
    require(d <= 4*R*R and N*b >= R*(k+1), "invalid schedule")
    return dict(out, status="CERTIFIED_UNIFORM_EVENTUAL_FAMILY", tail_join=N,
                variance_cutoff=dict(prefactor=str(2112*R**4/d), power_of_two=8*N),
                certified_thresholds="[0,infinity)",
                certified_variances="[prefactor*2^power_of_two,infinity)")


def checked_record(data, record):
    expected = expected_record(data)
    require(record == expected, "supplied record mismatch")
    return expected


def producer(data, invalid=False):
    with tempfile.TemporaryDirectory(prefix="support-cap-audit-") as folder:
        path = Path(folder)/"input.json"
        path.write_text(json.dumps(encode(data)))
        flags = ["-B"]+(["-O"] if sys.flags.optimize else [])
        run = subprocess.run([sys.executable, *flags, str(HERE/"certificate.py"), str(path)],
                             capture_output=True, text=True)
    if invalid:
        require(run.returncode != 0, "malformed input accepted")
        return
    require(run.returncode == 0, "producer failed: "+run.stderr)
    return json.loads(run.stdout)


def pinned_inputs():
    repo = HERE.parents[1]
    pins = json.loads((HERE/"INPUTS.json").read_text())
    for pin in pins:
        relative = (HERE/pin["relative_path"]).resolve().relative_to(repo).as_posix()
        raw = subprocess.run(["git", "show", pin["file_commit"]+":"+relative],
                             cwd=repo, check=True, capture_output=True).stdout
        require(hashlib.sha256(raw).hexdigest() == pin["sha256"], "dependency byte pin")
    return len(pins)


def audit():
    data = json.loads((HERE/"INPUT.json").read_text())
    record = producer(data)
    require(record == json.loads((HERE/"CERTIFICATE.json").read_text()), "fixture drift")
    checked_record(data, record)
    require(record["status"] == "CERTIFIED_UNIFORM_EVENTUAL_FAMILY", "fixture not certified")
    x, y, p, R0, _, _, _, _, _ = read_geometry(data)

    # Nonzero negative cells expose truncation-toward-zero bugs. The pair
    # below is a quarter-turn isometry, with g(theta) of both signs.
    xx, yy = [[F(-1), F(0), F(0)], [F(1), F(0), F(0)]], \
             [[F(0), F(-1), F(0)], [F(0), F(1), F(0)]]
    coarse = []
    for M in (1, 2, 3, 4, 8):
        for B in (1, 7, 16):
            total, negatives = chart_sum(xx, yy, F(1), M, B, direct=True)
            require(total <= 0 and negatives > 0, "signed cells were not exercised")
            coarse.append((M, B, total, negatives))

    # Small known width: the segment [-e1,e1] versus a point has delta=1/2.
    segment = dict(sources=xx, targets=[[0, 0, 0], [0, 0, 0]], weights=["1/2", "1/2"],
                   reference_radius=1, cloud_radius=0, relative_weight_error=0, mesh=128)
    seg = producer(segment)
    checked_record(encode(segment), seg)
    require(0 < F(seg["width"]["reference_width_lower"]) <= F(1, 2), "known width bound")

    # Geometry normalization: independent translations, a cube isometry, and
    # common dilation preserve normalized grid and multiply the cutoff by nine.
    scaled = copy.deepcopy(segment)
    for key, shift in (("sources", [7, -3, 11]), ("targets", [-5, 13, 17])):
        scaled[key] = [[-3*F(v[2])+shift[0], 3*F(v[0])+shift[1], 3*F(v[1])+shift[2]]
                       for v in scaled[key]]
    scaled["reference_radius"] = 3
    sc = producer(scaled)
    checked_record(encode(scaled), sc)
    require(sc["width"]["normalized_floor_sum"] == seg["width"]["normalized_floor_sum"]
            and sc["tail_join"] == seg["tail_join"]
            and F(sc["variance_cutoff"]["prefactor"]) == 9*F(seg["variance_cutoff"]["prefactor"]),
            "translation/scale/cube-isometry law")

    tiny = copy.deepcopy(segment)
    tiny["weights"] = [F(1, 2**80), 1-F(1, 2**80)]
    tiny_record = producer(tiny)
    checked_record(encode(tiny), tiny_record)
    require(tiny_record["mass_exponent"] == 80 and
            tiny_record["status"] == "CERTIFIED_UNIFORM_EVENTUAL_FAMILY", "tiny aggregate mass")

    unresolved = []
    for name in ("coarse", "isometry", "loss_reserve", "width_reserve"):
        case = copy.deepcopy(segment)
        if name == "coarse": case["mesh"] = 1
        if name == "isometry": case["targets"] = copy.deepcopy(case["sources"])
        if name == "loss_reserve":
            case["cloud_radius"] = F(1, 24)
            case["relative_weight_error"] = F(5, 12)
        if name == "width_reserve":
            case["cloud_radius"] = F(seg["width"]["reference_width_lower"])/2
        result = producer(case)
        checked_record(encode(case), result)
        require(result["status"] == "UNRESOLVED", "zero or negative reserve signed")
        if name == "loss_reserve":
            require(result["actual_loss_lower"] == "0" and F(result["tail_slope_lower"]) > 0,
                    "exact zero-loss reserve not exercised")
        if name == "width_reserve":
            require(result["tail_slope_lower"] == "0", "exact zero-width reserve not exercised")
        unresolved.append(name)

    # A zero-mass site outside the enclosing ball must have no effect.
    zero = copy.deepcopy(segment)
    zero["sources"].append([100, 0, 0]); zero["targets"].append([-100, 0, 0])
    zero["weights"].append(0)
    require(producer(zero) == seg, "zero-mass support was retained")

    # The calibration has Lip=1, a covariance obstruction to center-law
    # martingale witnesses, and an already known contracting straight path.
    def cov(rows):
        means = [sum(p[i]*rows[i][j] for i in range(len(p))) for j in range(3)]
        return [[sum(p[i]*(rows[i][j]-means[j])*(rows[i][k]-means[k])
                     for i in range(len(p))) for k in range(3)] for j in range(3)]
    zeta, eta = F(1, 2**24), F(1, 2**12)
    require(cov(x) == [[1, 0, 0], [0, 1, 0], [0, 0, zeta*zeta]] and
            cov(y) == [[F(1, 4), 0, 0], [0, F(1, 4), 0], [0, 0, eta*eta+zeta*zeta]],
            "calibration covariance")
    require(zeta*zeta < eta*eta+zeta*zeta < F(1, 4), "least eigenvalue ordering")
    a, b = minus(x[0], x[1]), minus(y[0], y[1])
    require(dot(a, a) == dot(b, b) > 0, "preserved pair")
    for i, j in itertools.combinations(range(len(p)), 2):
        a, b = minus(x[i], x[j]), minus(y[i], y[j])
        require(dot(b, minus(b, a)) <= 0, "known straight-motion control")

    bad_records = []
    # Replay mutations on the modest segment mesh, using full record checking.
    for name in ("rounding", "width", "cutoff", "contraction", "weights"):
        bad = copy.deepcopy(seg)
        if name == "rounding": bad["width"]["normalized_floor_sum"] += 1
        if name == "width": bad["width"]["reference_width_lower"] = "1"
        if name == "cutoff": bad["variance_cutoff"]["power_of_two"] = 0
        if name == "contraction": bad["actual_cloud_contraction_required"] = False
        if name == "weights": bad["common_label_weights_required"] = False
        try:
            checked_record(encode(segment), bad)
        except ValueError:
            bad_records.append(name)
        else:
            raise ValueError("damaged certificate accepted")
    bad_inputs = []
    for name in ("negative_weight", "wrong_total", "float", "radius", "rho", "expansion",
                 "negative_cloud", "mesh", "bits", "dimension"):
        bad = copy.deepcopy(segment); bad["mesh"] = 1
        if name == "negative_weight": bad["weights"][0] = "-1/2"
        if name == "wrong_total": bad["weights"][0] = 1
        if name == "float": bad["reference_radius"] = 1.0
        if name == "radius": bad["reference_radius"] = "1/2"
        if name == "rho": bad["relative_weight_error"] = "3/4"
        if name == "expansion": bad["targets"][0][0] = 100
        if name == "negative_cloud": bad["cloud_radius"] = -1
        if name == "mesh": bad["mesh"] = True
        if name == "bits": bad["rounding_bits"] = 0
        if name == "dimension": bad["sources"][0] = [0, 0]
        producer(bad, invalid=True); bad_inputs.append(name)

    return encode(dict(status="SUPPORT_CAP_LOCALIZATION_PASS", byte_pins=pinned_inputs(),
                       fixture=record, coarse_signed_cell_checks=coarse,
                       segment_width_lower=seg["width"]["reference_width_lower"],
                       scaling_factor=9, tiny_mass_exponent=tiny_record["mass_exponent"],
                       unresolved=unresolved, zero_mass_site_removed=True,
                       lipschitz_constant=1, center_law_martingale_obstruction=True,
                       control_has_known_straight_motion=True,
                       rejected_records=bad_records, rejected_inputs=bad_inputs,
                       endpoint_overlap=F(9, 64)-F(1, 8)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--input")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    if args.input or args.certificate:
        require(args.input and args.certificate, "supply input and certificate together")
        record = checked_record(json.loads(Path(args.input).read_text()),
                                json.loads(Path(args.certificate).read_text()))
        result = dict(status="SUPPLIED_SUPPORT_CAP_RECORD_PASS", record=record)
    else:
        result = audit()
        if not args.emit:
            require(result == json.loads((HERE/"EXPECTED.json").read_text()), "expected output drift")
    print(json.dumps(result, sort_keys=True, indent=2))
