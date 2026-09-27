#!/usr/bin/env python3
"""Exact controls for the written polynomial hinge-margin theorem."""
import argparse
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, why):
    if not ok:
        raise ValueError(why)


def rat(x):
    require(isinstance(x, (int, str)) and not isinstance(x, bool),
            "rational inputs must be integers or fraction strings")
    return Q(x)


def integer(x, low=0):
    require(type(x) is int and x >= low, "invalid integer")
    return x


def norm2(x):
    return sum(v*v for v in x)


def sub(x, y):
    return [a-b for a, b in zip(x, y)]


def exponent(R):
    integer(R, 1)
    return 40*R*R+9*R+38


def band_exponent(R, j, k):
    return exponent(R)+3*integer(j)+8*integer(k)


def old_exponent(R, j, k):
    integer(R, 1)
    integer(j)
    integer(k)
    W = 2*R+2**(j+1)
    return 2*W*W+W+8*R+8*k+33


def beta_margin(N, k, p):
    integer(N)
    integer(k)
    require(k <= N and 0 < p <= 1, "invalid beta parameters")
    S = sum(Q(comb(N-k, r))*(1-p)**(N-k-r)*p**r
            * Q(factorial(k+3)*factorial(r+8), factorial(k+r+12))
            for r in range(N-k+1))
    return (N+1)*comb(N, k)*p**(k+12)*S


def beta_integral_direct(N, k, p):
    # Integrate the expanded monomials of
    # u^(k+3) (1-u)^(N-k) (p-u)^8 on [0,p].
    S = Q(0)
    for a in range(N-k+1):
        for b in range(9):
            z = k+4+a+b
            S += Q((-1)**(a+b)*comb(N-k, a)*comb(8, b), z) * p**(8-b+z)
    return (N+1)*comb(N, k)*S


def loss(points, images, weights):
    return sum(weights[i]*weights[j]
               *(norm2(sub(points[i], points[j]))-norm2(sub(images[i], images[j])))
               for i in range(len(weights)) for j in range(len(weights)))


def row_error(N, q, radius_squared):
    return (Q(N+1, 4*factorial(q))*(radius_squared/2)**q
            * max(comb(N, k)*sum(comb(N-k, z)*(k+z+2)**(q-2)
                                 for z in range(N-k+1)) for k in range(N+1)))


def certify(raw, row=8):
    integer(row)
    P = [[rat(a) for a in v] for v in raw["source"]]
    Qs = [[rat(a) for a in v] for v in raw["target"]]
    w = list(map(rat, raw["weights"]))
    a = list(map(rat, raw["source_anchor"]))
    b = list(map(rat, raw["target_anchor"]))
    s = rat(raw["variance"])
    R, j, k = integer(raw["R"], 1), integer(raw["j"]), integer(raw["k"])
    require(len(P) == len(Qs) == len(w) > 0, "inconsistent lengths")
    require(all(len(v) == 3 for v in P+Qs+[a, b]), "not three-dimensional")
    require(s > 0 and all(v > 0 for v in w) and sum(w) == 1, "bad law or variance")
    unresolved = []
    for x, y in zip(P, Qs):
        if norm2(sub(x, a)) != norm2(sub(y, b)):
            unresolved.append("anchor equality")
        if norm2(sub(x, a)) > R*R*s:
            unresolved.append("anchor radius")
    tight = 0
    for i in range(len(P)):
        for h in range(i):
            z = norm2(sub(P[i], P[h]))-norm2(sub(Qs[i], Qs[h]))
            if z < 0:
                unresolved.append("pair contraction")
            tight += (z == 0)
    if unresolved:
        return {"status": "UNRESOLVED", "failed": sorted(set(unresolved))}
    d = loss(P, Qs, w)/s
    p = Q(1, 2**(R*R))
    B = band_exponent(R, j, k)
    lower, upper = Q(1, 2**j), p-Q(1, 2**k)
    return {
        "status": "ISOMETRIC_ZERO" if d == 0 else "POLYNOMIAL_HINGE_MARGIN",
        "sites": len(w), "pairs": len(w)*(len(w)-1)//2, "tight_pairs": tight,
        "normalized_ordered_loss": str(d),
        "envelope": {"coefficient_power_of_two": -exponent(R),
                     "low_threshold_power": 3, "peak_gap_power": 8,
                     "certified_lower_peak_over_C": str(p)},
        "band": {"lower": str(lower), "explicit_upper": str(upper),
                 "nonempty": lower <= upper,
                 "conditional_peak_separation": str(Q(1, 2**k)),
                 "new_margin_power_of_two": -B,
                 "prior_margin_power_of_two": -old_exponent(R, j, k)},
        "beta_row": row,
        "beta_margins_divided_by_d_A": [str(beta_margin(row, z, p)) for z in range(row+1)],
        "loss_modulus_budget": {
            "premise": "K<=2^20 in the separately required small-radius regime",
            "radius_le_half_sqrt_variance_verified":
                max(norm2(sub(v, a)) for v in P) <= s/4,
            "log2_N_plus_2": 4*(B+21)+1,
            "prior_log2_N_plus_2": 4*(old_exponent(R, j, k)+21)+1},
        "scope": "Finite guards and analytic theorem; no Gaussian quadrature or all-radius relative modulus"
    }


def clone(x):
    return json.loads(json.dumps(x))


def check_record(raw, record, row=8):
    require(record == certify(raw, row), "damaged certificate")


def controls():
    raw = json.loads((HERE/"INPUT.json").read_text())
    base = certify(raw)
    require(base["status"] == "POLYNOMIAL_HINGE_MARGIN", "fixture failed")
    require(base["normalized_ordered_loss"] == "129/392", "ordered loss normalization")
    require(base["band"]["new_margin_power_of_two"] == -112, "band budget")
    require(base["band"]["prior_margin_power_of_two"] == -723, "prior budget")
    count = 0
    for N in range(13):
        for k in range(N+1):
            for p in [Q(1, 8), Q(1, 2), Q(3, 4), Q(1)]:
                actual = beta_margin(N, k, p)
                require(actual == beta_integral_direct(N, k, p) and actual > 0,
                        "positive beta integration mismatch")
                count += 1
    squares = 0
    for R in range(1, 6):
        for q in [Q(i, 3) for i in range(41)]:
            # q=sqrt(ell/2): the difference is (4R-q)^2.
            require(20*R*R+5*q*q-(2*R+2*q)**2 == (4*R-q)**2,
                    "square completion")
            squares += 1
        require((R+1)**5*R**4 <= 2**(5+9*R), "dyadic denominator")
    transformed = clone(raw)
    sa, ta = [Q(7), Q(-2), Q(1)], [Q(-3), Q(5), Q(2)]
    # Independent orthogonal frames and common factor three.
    rotP = lambda v: [rat(v[1]), -rat(v[0]), rat(v[2])]
    rotQ = lambda v: [-rat(v[2]), rat(v[1]), rat(v[0])]
    transformed["source"] = [[str(3*a+b) for a, b in zip(rotP(v), sa)] for v in raw["source"]]
    transformed["target"] = [[str(3*a+b) for a, b in zip(rotQ(v), ta)] for v in raw["target"]]
    transformed["source_anchor"] = list(map(str, sa))
    transformed["target_anchor"] = list(map(str, ta))
    transformed["variance"] = 9
    require(certify(transformed) == base, "frame/variance invariance")
    smaller = clone(raw)
    for endpoint in ["source", "target"]:
        smaller[endpoint] = [[str(rat(z)/2) for z in v] for v in raw[endpoint]]
    scaled = certify(smaller)
    require(scaled["loss_modulus_budget"]["radius_le_half_sqrt_variance_verified"],
            "small-radius calibration")
    require(Q(scaled["normalized_ordered_loss"]) == Q(129, 1568), "scaled loss")
    require(Q(1, 4)*3*3**7*Q(256, 9)*Q(196, 9) == 1016064 < 2**20,
            "modulus rational upper budget")
    margin = Q(1, 2**exponent(1))*min(beta_margin(8, k, Q(1, 2)) for k in range(9))
    cubature_q = 5
    while row_error(8, cubature_q, Q(1)) >= margin:
        cubature_q += 1
    require(cubature_q > 5 and row_error(8, cubature_q-1, Q(1)) >= margin,
            "row budget predecessor")
    families = []
    for t in [Q(1, 4), Q(1, 16), Q(1, 2**30)]:
        r = {"source": [[str(t), 0, 0], [str(-t), 0, 0]],
             "target": [[str(t), 0, 0], [str(t), 0, 0]],
             "weights": ["1/2", "1/2"],
             "source_anchor": [0, 0, 0], "target_anchor": [0, 0, 0],
             "variance": 1, "R": 1, "j": 3, "k": 2}
        c = certify(r, 0)
        require(Q(c["normalized_ordered_loss"]) == 2*t*t, "vanishing-loss family")
        require(c["band"]["new_margin_power_of_two"] == -112, "loss-independent exponent")
        families.append({"t": str(t), "loss": str(2*t*t)})
    zero = clone(raw)
    zero["target"] = clone(zero["source"])
    require(certify(zero)["status"] == "ISOMETRIC_ZERO", "zero loss")
    bad = []
    q = clone(raw); q["target"][0] = [0, 0, 0]; bad.append((q, False))
    q = clone(raw); q["source_anchor"] = [1, 0, 0]; bad.append((q, False))
    q = clone(raw); q["variance"] = "1/100"; bad.append((q, False))
    q = clone(raw); q["target"][-1] = ["-1/4", "-1/4", "-1/4"]; bad.append((q, False))
    q = clone(raw); q["weights"][0] = 0; bad.append((q, True))
    q = clone(raw); q["weights"][0] = 0.25; bad.append((q, True))
    q = clone(raw); q["R"] = True; bad.append((q, True))
    q = clone(raw); q["variance"] = -1; bad.append((q, True))
    q = clone(raw); q["target"][0] = [0, 0]; bad.append((q, True))
    q = clone(raw); q["k"] = -1; bad.append((q, True))
    for q, malformed in bad:
        try:
            c = certify(q)
            require(not malformed and c["status"] == "UNRESOLVED", "bad guard accepted")
        except ValueError:
            require(malformed, "valid failed guard raised")
    damaged = clone(base)
    damaged["band"]["new_margin_power_of_two"] = -111
    try:
        check_record(raw, damaged)
    except ValueError:
        pass
    else:
        raise ValueError("damaged record accepted")
    pins = json.loads((HERE/"INPUTS.json").read_text())
    for pin in pins:
        require(hashlib.sha256((HERE/pin["path"]).read_bytes()).hexdigest() == pin["sha256"],
                "dependency byte pin mismatch")
    schedules = []
    for j in [3, 6, 10, 20]:
        b = band_exponent(1, j, 2)
        old = old_exponent(1, j, 2)
        schedules.append({"j": j, "new_margin_bits": b, "prior_margin_bits": old,
                          "loss_modulus_log2_N_plus_2": 4*(b+21)+1,
                          "prior_loss_modulus_log2_N_plus_2": 4*(old+21)+1})
    return {"status": "POLYNOMIAL_HINGE_MARGIN_CONTROLS_PASS",
            "calibration": base, "beta_integral_comparisons": count,
            "square_controls": squares, "invariance_controls": 1,
            "vanishing_loss_controls": families, "zero_loss_controls": 1,
            "negative_controls": len(bad)+1, "source_pins": len(pins),
            "schedules": schedules,
            "small_radius_calibration": {
                "coordinate_factor": "1/2", "normalized_loss": "129/1568",
                "margin": "(129/1568)*2^-112", "K_upper": "2^20",
                "log2_N_plus_2": 533, "prior_log2_N_plus_2": 2977},
            "row_error_budget": {"row": 8, "radius_squared": "1",
                "normalized_row_margin": str(margin), "q": cubature_q,
                "coordinate_degree": 2*cubature_q,
                "atom_cap": 2*comb(2*cubature_q+3, 3)-1,
                "error": str(row_error(8, cubature_q, Q(1))),
                "scope": "Accepted same-row error only, not full-curve transfer"},
            "trust": "Exact finite author controls; written analytic proof is unformalized"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path)
    ap.add_argument("--row", type=int, default=8)
    ap.add_argument("--verify", type=Path)
    ap.add_argument("--write-expected", action="store_true")
    args = ap.parse_args()
    if args.input:
        require(not args.write_expected, "cannot write expected for external input")
        raw = json.loads(args.input.read_text())
        result = certify(raw, args.row)
        if args.verify:
            check_record(raw, json.loads(args.verify.read_text()), args.row)
    else:
        require(not args.verify, "verification requires supplied input")
        result = controls()
    output = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.write_expected:
        (HERE/"EXPECTED.json").write_text(output)
    elif not args.input:
        require(output == (HERE/"EXPECTED.json").read_text(), "expected record mismatch")
    print(output, end="")


if __name__ == "__main__":
    main()
