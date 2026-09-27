"""Exact author audit; analytic proof and acceptance are separate obligations."""
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


def rational(x):
    require(type(x) in (int, str), "not an exact rational encoding")
    return F(x)


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {k: encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def norm2(v):
    return sum(z*z for z in v)


def difference(x, y):
    return [u-v for u, v in zip(x, y)]


def checked_record(data, record):
    """No producer import: reconstruct scatter/radii from paired differences."""
    ref = data["reference"]
    p = list(map(rational, ref["weights"]))
    x = [list(map(rational, row)) for row in ref["sources"]]
    y = [list(map(rational, row)) for row in ref["targets"]]
    require(len(p) == len(x) == len(y) and p and all(w >= 0 for w in p)
            and sum(p) == 1 and all(len(v) == 3 for v in x+y), "law format")
    keep = [i for i, w in enumerate(p) if w > 0]
    p, x, y = [[values[i] for i in keep] for values in (p, x, y)]
    n = len(p)
    xx = [[difference(u, v) for v in x] for u in x]
    yy = [[difference(u, v) for v in y] for u in y]
    xc = [[sum(p[j]*xx[i][j][k] for j in range(n)) for k in range(3)]
          for i in range(n)]
    yc = [[sum(p[j]*yy[i][j][k] for j in range(n)) for k in range(3)]
          for i in range(n)]
    V = sum(p[i]*p[j]*norm2(xx[i][j]) for i in range(n)
            for j in range(n))/2
    B, s = map(rational, (data["radius_squared"], data["variance"]))
    a = rational(data["witness"]["dilation"])
    ax, ay, rx, ry = [rational(data[k]) for k in (
        "source_relative_radius", "target_relative_radius",
        "source_relative_weight_error", "target_relative_weight_error")]
    require(B > 0 and s > 0 and a > 1 and max(map(norm2, xc)) <= B,
            "reference size")
    require(min(ax, ay) >= 0 and 0 <= rx <= F(1, 2) and 0 <= ry <= F(1, 2),
            "neighborhood range")
    require(all(norm2(yy[i][j]) <= norm2(xx[i][j]) for i in range(n)
                for j in range(n)), "reference matching expands")
    kind = data["witness"]["kind"]
    if kind == "diagonal":
        pi = [[p[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    else:
        require(kind == "affine_density", "unknown witness")
        A = [list(map(rational, row)) for row in data["witness"]["matrix"]]
        require(len(A) == 3 and all(len(row) == 3 for row in A), "matrix shape")
        pi = [[p[i]*p[j]*(1+sum(xc[i][k]*A[k][l]*yc[j][l]
                  for k in range(3) for l in range(3))) for j in range(n)]
              for i in range(n)]
    require(all(v >= 0 for row in pi for v in row), "coupling positivity")
    require([sum(row) for row in pi] == p and
            [sum(pi[i][j] for i in range(n)) for j in range(n)] == p,
            "coupling marginals")
    require(all(sum(pi[i][j]*xc[i][k] for i in range(n)) == a*p[j]*yc[j][k]
                for j in range(n) for k in range(3)), "conditional barycenters")
    # The radical inequality is checked in its rational equivalent, with sign.
    cross = True
    for i in range(n):
        for j in range(i):
            A2, C2, E2 = norm2(xx[i][j]), norm2(yy[i][j]), B*(ax+ay)**2
            d = A2-C2-4*E2
            cross = cross and d >= 0 and d*d >= 16*E2*C2
    t = 1+ax
    P = ax+ay+4*t*(rx+ry)
    L = (a-1)*V/(48*a*B*t)-P
    expected = {
        "schema": "robust-martingale-localization-v1", "active_reference_sites": n,
        "witness": kind, "reference_radius_squared": str(B),
        "reference_scatter": str(V), "dilation": str(a), "radius_factor": str(t),
        "perturbation_slope_cost": str(P), "remaining_dimensionless_slope": str(L),
        "source_cloud_radius_squared": str(B*ax*ax),
        "target_cloud_radius_squared": str(B*ay*ay),
        "source_relative_weight_error": str(rx), "target_relative_weight_error": str(ry),
        "variance": str(s), "uniform_cross_label_condition": bool(cross),
        "actual_contraction_required": True, "within_cloud_contraction_is_not_inferred": True}
    if L <= 0:
        expected.update(status="UNRESOLVED", reason="no positive spherical reserve")
    else:
        eta = L/(2*t)
        cutoff = 88*B*t**3/L
        require(0 < eta < F(1, 96) and cutoff > 8*B*t*t, "endpoint dominance")
        expected.update(status=("SIGNED_CONTRACTIVE_CLOUD_FAMILY" if s >= cutoff
                               else "CERTIFIED_ONLY_FOR_LARGER_VARIANCES"),
                        spherical_gap=str(eta), variance_cutoff=str(cutoff),
                        certified_variances="[variance_cutoff,infinity)",
                        certified_thresholds="[0,infinity)")
    require(record == expected, "supplied certificate mismatch")
    return {"scatter": str(V), "slope": str(L), "status": record["status"]}


def producer(data, invalid=False):
    with tempfile.TemporaryDirectory(prefix="gaussian-cloud-audit-") as tmp:
        path = Path(tmp)/"input.json"
        path.write_text(json.dumps(encode(data)))
        flags = ["-B"]+(["-O"] if sys.flags.optimize else [])
        run = subprocess.run([sys.executable, *flags, str(HERE/"certificate.py"), str(path)],
                             text=True, capture_output=True)
    if invalid:
        require(run.returncode != 0, "malformed input was accepted")
        return
    require(run.returncode == 0, "producer failed: "+run.stderr)
    record = json.loads(run.stdout)
    checked_record(encode(data), record)
    return record


def pinned_inputs():
    repo = HERE.parents[1]
    pins = json.loads((HERE/"INPUTS.json").read_text())
    for pin in pins:
        path = (HERE/pin["relative_path"]).resolve().relative_to(repo).as_posix()
        raw = subprocess.run(["git", "show", pin["file_commit"]+":"+path], cwd=repo,
                             check=True, capture_output=True).stdout
        require(hashlib.sha256(raw).hexdigest() == pin["sha256"], "dependency byte pin")
    return len(pins)


def audit():
    data = json.loads((HERE/"TUBE_INPUT.json").read_text())
    tube = producer(data)
    require(tube == json.loads((HERE/"TUBE_CERTIFICATE.json").read_text()), "fixture drift")
    require(tube["status"] == "SIGNED_CONTRACTIVE_CLOUD_FAMILY" and
            tube["uniform_cross_label_condition"], "nonempty signed tube")
    noerr = copy.deepcopy(data)
    for k in ("source_relative_radius", "target_relative_radius",
              "source_relative_weight_error", "target_relative_weight_error"):
        noerr[k] = 0
    base = producer(noerr)
    B, V, a = F(base["reference_radius_squared"]), F(base["reference_scatter"]), F(base["dilation"])
    require(F(base["variance_cutoff"]) == 4224*a*B*B/((a-1)*V), "R2 schedule recovery")

    # Equality in the reserve guard must not produce a sign.
    boundary = copy.deepcopy(noerr)
    boundary["target_relative_radius"] = str((a-1)*V/(48*a*B))
    zero = producer(boundary)
    require(zero["remaining_dimensionless_slope"] == "0" and zero["status"] == "UNRESOLVED",
            "zero reserve incorrectly signed")
    lower = copy.deepcopy(data)
    lower["variance"] = str(F(tube["variance_cutoff"])/2)
    require(producer(lower)["status"] == "CERTIFIED_ONLY_FOR_LARGER_VARIANCES", "variance guard")

    # Separate translations and common scaling preserve all dimensionless bounds.
    scaled = copy.deepcopy(data)
    for key, shift in [("sources", [7, -11, 13]), ("targets", [-5, 17, 19])]:
        scaled["reference"][key] = [[3*F(v)+shift[k] for k, v in enumerate(row)]
                                     for row in data["reference"][key]]
    scaled["witness"]["matrix"] = [[F(v)/9 for v in row] for row in data["witness"]["matrix"]]
    scaled["radius_squared"], scaled["variance"] = 9*B, 9*F(data["variance"])
    sc = producer(scaled)
    require(sc["remaining_dimensionless_slope"] == tube["remaining_dimensionless_slope"] and
            F(sc["variance_cutoff"]) == 9*F(tube["variance_cutoff"]), "scale/translation law")

    # The entire thin-source control is a genuine contraction but has no
    # center-law martingale, even after arbitrary endpoint rotations.
    refx = [[u, v, 0] for u, v in itertools.product([-1, 1], repeat=2)]
    diagonal = dict(reference=dict(sources=refx, targets=[[F(u, 2), F(v, 2), 0]
                    for u, v, _ in refx], weights=[F(1, 4)]*4),
                    witness=dict(kind="diagonal", dilation=2), radius_squared=2,
                    variance=32768, source_relative_radius=F(1, 4096),
                    target_relative_radius=F(1, 4096), source_relative_weight_error=0,
                    target_relative_weight_error=0)
    control = producer(diagonal)
    require(control["status"] == "SIGNED_CONTRACTIVE_CLOUD_FAMILY", "thin-source reserve")
    zeta, eta0 = F(1, 2**24), F(1, 2**12)
    actualx = [[F(u), F(v), zeta*w] for u, v, w in itertools.product([-1, 1], repeat=3)]
    actualy = [[u/2, v/2, eta0*u*v+w] for u, v, w in actualx]
    for i, j in itertools.product(range(8), repeat=2):
        require(norm2(difference(actualy[i], actualy[j])) <=
                norm2(difference(actualx[i], actualx[j])), "actual contraction")
    def covariance(cloud):
        mean = [sum(v[k] for v in cloud)/len(cloud) for k in range(3)]
        return [[sum((v[k]-mean[k])*(v[l]-mean[l]) for v in cloud)/len(cloud)
                 for l in range(3)] for k in range(3)]
    require(covariance(actualx) == [[1, 0, 0], [0, 1, 0], [0, 0, zeta*zeta]] and
            covariance(actualy) == [[F(1, 4), 0, 0], [0, F(1, 4), 0],
                                    [0, 0, eta0*eta0+zeta*zeta]],
            "covariance separation")
    require(zeta*zeta < eta0*eta0+zeta*zeta < F(1, 4) and
            (eta0+zeta)**2 <= F(2, 4096**2), "cloud radii")
    # A preserved nonzero pair forces Lipschitz constant exactly one.
    dx2 = norm2(difference(actualx[0], actualx[1]))
    dy2 = norm2(difference(actualy[0], actualy[1]))
    require(0 < dx2 == dy2, "preserved pair")
    # This small control is already positive by its contracting straight path.
    # The squared-distance derivative is increasing, and is <=0 at time one.
    for i, j in itertools.product(range(8), repeat=2):
        dx, dy = difference(actualx[i], actualx[j]), difference(actualy[i], actualy[j])
        require(sum(dy[k]*(dy[k]-dx[k]) for k in range(3)) <= 0, "known straight path")
    # At the certified s=32768, the centered target radius is >1/512.
    # R8's schedule always has B>=1404 (R>=1,j>=0), hence radius<=2^-1405.
    require(F(1, 2)/32768 > F(1, 512**2), "small-target scope separation")

    # Vanishing individual mass and singular covariance remain admissible.
    tiny = copy.deepcopy(diagonal)
    p = F(1, 2**80)
    tiny["reference"] = dict(sources=[[-1, 0, 0], [1, 0, 0]],
                              targets=[[F(-1, 2), 0, 0], [F(1, 2), 0, 0]], weights=[p, 1-p])
    tiny["radius_squared"] = 4
    for k in ("source_relative_radius", "target_relative_radius"):
        tiny[k] = 0
    tiny_record = producer(tiny)
    require(tiny_record["status"] == "CERTIFIED_ONLY_FOR_LARGER_VARIANCES", "tiny weight")

    # Reject counterfeit records and malformed mathematical hypotheses.
    bad_records = []
    for key, value in [("actual_contraction_required", False), ("spherical_gap", "1"),
                       ("variance_cutoff", "1"), ("uniform_cross_label_condition", False)]:
        record = copy.deepcopy(tube); record[key] = value
        try:
            checked_record(data, record)
        except ValueError:
            bad_records.append(key)
        else:
            raise ValueError("damaged record accepted")
    bad_inputs = []
    for name in ["negative_weight", "wrong_total", "float", "radius", "rho", "dilation",
                 "coupling_moments", "coupling_positivity", "expansion", "unknown"]:
        bad = copy.deepcopy(data)
        if name == "negative_weight": bad["reference"]["weights"][0] = "-1/8"
        if name == "wrong_total": bad["reference"]["weights"][0] = "1/4"
        if name == "float": bad["variance"] = 40000.0
        if name == "radius": bad["radius_squared"] = 1
        if name == "rho": bad["target_relative_weight_error"] = "3/4"
        if name == "dilation": bad["witness"]["dilation"] = 1
        if name == "coupling_moments": bad["witness"]["matrix"][0][0] = 1
        if name == "coupling_positivity": bad["witness"]["matrix"][0][0] = 100
        if name == "expansion": bad["reference"]["targets"][0][0] = 100
        if name == "unknown": bad["witness"]["kind"] = "unverified"
        producer(bad, invalid=True); bad_inputs.append(name)
    return encode(dict(status="ROBUST_MARTINGALE_LOCALIZATION_PASS", byte_pins=pinned_inputs(),
                       tube=tube, zero_error_cutoff=base["variance_cutoff"],
                       boundary=zero["status"], thin_source_control=control,
                       source_least_eigenvalue=zeta*zeta, target_least_eigenvalue=eta0*eta0+zeta*zeta,
                       no_actual_rotated_martingale=True, outside_strong_map_guard=True,
                       actual_lipschitz_constant=1, control_has_known_straight_path=True,
                       outside_small_target_schedule_at_32768=True,
                       tiny_mass=p, tiny_mass_scatter=tiny_record["reference_scatter"],
                       scaled_cutoff=sc["variance_cutoff"], rejected_records=bad_records,
                       rejected_inputs=bad_inputs, endpoint_overlap=F(9, 64)-F(1, 8)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--input")
    parser.add_argument("--certificate")
    args = parser.parse_args()
    if args.input or args.certificate:
        require(args.input and args.certificate, "supply both input and certificate")
        result = checked_record(json.loads(Path(args.input).read_text()),
                                json.loads(Path(args.certificate).read_text()))
    else:
        result = audit()
        if not args.emit:
            require(result == json.loads((HERE/"EXPECTED.json").read_text()), "expected record drift")
    print(json.dumps(result, sort_keys=True, indent=2))
