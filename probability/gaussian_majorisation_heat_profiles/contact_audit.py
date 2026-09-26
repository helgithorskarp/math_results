"""Exact finite controls for CONTACT_REDUCTION.md; not an analytic proof."""

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def audit():
    # Both sides have separate degrees <= (2,2,2,1) in (e,S,t,q).
    # Equality on this tensor grid therefore certifies the cleared
    # polynomial identity by univariate interpolation, one variable at a time.
    count = 0
    for e, S, t, q in product(range(3), range(3), range(3), range(2)):
        left = (e + 2*S - t)*(q*e + S) - (q*e + t)*(e + t)
        right = (S - t)*(e*(1 + 2*q) + 2*S + t)
        require(left == right, "cleared coefficient identity failed")
        count += 1

    # One concrete tail control, using log(x)<=x-1 and pi<4.
    e = S = R = F(1)
    c = F(1, 2)
    eta = e*(1-c*c)/(2*(e+S))
    theta = (1-eta)/2
    A = eta/(2*(c*c*e+S))
    B = (1-eta)*R/(c*e)
    r = F(44)
    require(r >= c*R and r >= 2*B/A, "linear-radius cutoff failed")
    log_budget_upper = 3*(1/eta-1)+1
    require(A*r*r/2 >= log_budget_upper, "exponential budget failed")
    require(r*r >= 4*(e+S)/2, "radial prefactor bound failed")

    # This scalar control is not Gaussian data. It shows why the proof
    # perturbs lambda instead of relying on the derivative at a flat zero.
    # W=-(t-1)^3-(lambda-1)+(v-1)^2; minimizing v gives v=1.
    crossings = []
    for h in [F(-1, 2), F(0), F(1, 2)]:
        t = 1+h
        lam = 1-h**3
        require(-(t-1)**3-(lam-1) == 0, "contact control failed")
        slope = -3*(t-1)**2
        require(slope < 0 if h else slope == 0, "crossing slope failed")
        crossings.append({"lambda": str(lam), "time": str(t), "slope": str(slope)})

    return {
        "status": "CONTACT_CONSTANTS_AND_SCALAR_CONTROLS_PASS",
        "cleared_polynomial_tensor_grid_checks": count,
        "tail_control": {"epsilon": str(e), "horizon": str(S),
                         "radius_bound": str(R), "lipschitz": str(c),
                         "eta": str(eta), "theta": str(theta),
                         "A": str(A), "B": str(B), "test_radius": str(r),
                         "rational_log_budget_upper": str(log_budget_upper)},
        "non_gaussian_scalar_crossing_controls": crossings,
        "scope": "Finite exact controls only; no contact flux inequality is proved."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = audit()
    if args.check is not None:
        expected = json.loads(args.check.read_text())
        require(result == expected, "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
