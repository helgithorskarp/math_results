"""Canonical exact serialization only; neither mathematical engine reads fixtures."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import argparse
import json
from math import prod


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rows(poly):
    return [{"powers": list(m), "coefficient": str(F(c.numerator, c.denominator))}
            for m, c in sorted(poly.items(), reverse=True) if c]


def canonical(record):
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode()


def summarize(record):
    boxes = []
    for leaf in record["leaves"]:
        deg = leaf["degrees"]
        d = {tuple(r["powers"]): F(r["coefficient"]) for r in leaf["controls"]}
        expected = prod(n + 1 for n in deg)
        values = [d.get((i, j, k), F(0))
                  for i in range(deg[0] + 1)
                  for j in range(deg[1] + 1)
                  for k in range(deg[2] + 1)]
        require(len(values) == expected and len(d) == expected,
                "complete strict Bernstein tensor")
        require(min(values) > 0, "entire Bernstein tensor strictly positive")
        boxes.append({"label": leaf["label"], "kappa": leaf["kappa"],
                      "q_bounds": leaf["q_bounds"], "t_bounds": leaf["t_bounds"],
                      "degrees": deg, "entries": expected,
                      "minimum": str(min(values)), "zero": 0, "negative": 0,
                      "whole_box_sha256": sha256(canonical(leaf)).hexdigest()})
    require([b["label"] for b in boxes] ==
            ["negative", "positive-left", "positive-right"], "three-box coverage")
    require(sum(b["entries"] for b in boxes) == 6786, "full tensor count")
    return {"actual_agent": "six-sendov-2", "role": "researcher",
            "claim": "outer real-q0 original-one-double C < 47/2; exact original extrema license",
            "domain": record["domain"],
            "whole_math_bytes": len(canonical(record)),
            "whole_math_sha256": sha256(canonical(record)).hexdigest(),
            "maps": {k: {"terms": len(record[k])} for k in ["Delta", "N", "P"]},
            "removed_positive_factor": "q^10 (t^2-1)^2",
            "whole_original_moments_and_derivative": True,
            "whole_critical_quartic_and_four_Hermite_minors": True,
            "positive_q0_thin_strip_identities": True,
            "whole_determinant_coefficients_and_mass_sum": True,
            "whole_cap_clearing_and_factor_identity": True,
            "whole_tensor_reverse_reconstruction": True,
            "boxes": boxes, "all_6786_controls_strictly_positive": True,
            "ordinary_bridges_unformalized": True,
            "independent_peer_review_claimed": False,
            "full_complex_first_power_claimed": False}


def emit(record):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--whole", type=Path, help="write bulky transient record outside source")
    parser.add_argument("--expected", type=Path, help="compare compact fixture after calculation")
    parser.add_argument("--check", type=Path, help="compare every coefficient of an external record")
    args = parser.parse_args()
    summary = summarize(record)
    data = canonical(record)
    if args.check:
        candidate = args.check.read_bytes()
        require(candidate == data, "entire external mathematical record mismatch")
    if args.expected:
        require(json.loads(args.expected.read_text()) == summary, "complete expected record mismatch")
    if args.whole:
        source = Path(__file__).resolve().parent
        require(not args.whole.resolve().is_relative_to(source), "do not write bulky record in source")
        args.whole.write_bytes(data)
    print(json.dumps(summary, sort_keys=True, indent=2))
