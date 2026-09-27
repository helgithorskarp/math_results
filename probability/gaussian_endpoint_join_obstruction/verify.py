#!/usr/bin/env python3
"""Exact constant/provenance audit; the universal argument is in PROOF.md."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rat(x):
    x = F(x)
    return f"{x.numerator}/{x.denominator}"


def source_checks():
    data = json.loads((HERE / "INPUTS.json").read_text())
    require(data["schema"] == 1, "unknown provenance schema")
    seen = set()
    for row in data["inputs"]:
        path, commit = row["path"], row["commit"]
        require(path.startswith("probability/") and ".." not in path,
                "unexpected source path")
        require(len(commit) == 40 and all(c in "0123456789abcdef" for c in commit),
                "invalid commit")
        require(path not in seen, "duplicate dependency")
        seen.add(path)
        content = subprocess.run(
            ["git", "show", f"{commit}:{path}"], cwd=REPO,
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        require(hashlib.sha256(content).hexdigest() == row["sha256"],
                f"versioned dependency differs: {path}")
    return len(seen)


def build_record():
    radius, kappa = F(1, 2), F(1, 2**15)
    rigidity = 2 * radius**2 / kappa
    require(rigidity == 2**14, "rigidity constant")
    trace_floor = 3 * kappa
    delta_coefficient = 24 * trace_floor / 256
    require(delta_coefficient == F(9, 2**20), "radius-to-gap coefficient")
    require(delta_coefficient > F(1, 2**17), "strict dyadic gap bound")
    log_mass_coefficient = 256 * radius / 8
    require(log_mass_coefficient == 16, "mass coefficient")
    require(F(3) < 4, "series upper bound e<3 implies e<4")

    # m=4+t. Expanding 2m^2-(m+1)^2 gives 7+6t+t^2.
    induction = [2*4**2-5**2, 4*4-2*5, 2-1]
    require(induction == [7, 6, 1], "induction polynomial")
    require(all(c > 0 for c in induction), "induction sign on t>=0")
    require(4**2 == 2**4, "induction base")

    # Compare the upper exponent 44m+208-14 with lower 33m+34.
    gap_slope = 44 - (2*int(log_mass_coefficient) + 1)
    gap_intercept = 208 - 14 - 2*17
    shifted = [gap_intercept + 4*gap_slope, gap_slope]
    require(shifted == [204, 11], "universal exponent difference")
    require(all(c > 0 for c in shifted), "strict exponent ordering")

    # General necessary test: at a=72*kappa/S, S*a/8=9*kappa.
    require(F(72, 8) == 9, "left-endpoint exponential cancellation")
    require(F(1, 1)/rigidity == kappa/(2*radius**2),
            "necessary loss normalization")

    # R2's displayed sufficient schedule, not its analytic proof.
    coupling_loss_factor = 2 * 4224
    covariance_factor = coupling_loss_factor * 3**2
    lower_loss = covariance_factor * kappa**2
    require(coupling_loss_factor == 8448 and covariance_factor == 76032,
            "martingale schedule coefficients")
    require(lower_loss == F(297, 4194304) > F(1, 2**14),
            "martingale lower loss")
    require(44*4+208 == 384 and 384 > 14, "small-loss disjointness")

    controls = []
    for m in [4, 5, 8, 16, 64, 256, 10**6, 10**200]:
        upper, lower = 44*m+194, 33*m+34
        require(upper-lower == 11*m+160 > 0, "exponent control")
        controls.append({"m": str(m), "upper_minus_lower_exponent": str(upper-lower)})
    return {
        "schema": 1,
        "status": "ENDPOINT_JOIN_OBSTRUCTION_PASS",
        "scope": "Exact constants and provenance only; written geometric proof is unformalized.",
        "versioned_inputs": source_checks(),
        "rigidity_constant": rat(rigidity),
        "minimum_gap_coefficient_if_Q_le_256m": rat(delta_coefficient),
        "log_inverse_mass_coefficient": rat(log_mass_coefficient),
        "induction_polynomial_in_m_minus_4": induction,
        "exponent_gap_polynomial_in_m_minus_4": shifted,
        "negative_log_threshold_ratio_lower_bound_strict": 256**2,
        "martingale_necessary_normalized_loss_strict": rat(lower_loss),
        "controls": controls,
    }


def main():
    record = build_record()
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    require(record == expected, "expected record mismatch")
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(record["status"])
    print("record_sha256=" + hashlib.sha256(canonical).hexdigest())


if __name__ == "__main__":
    main()
