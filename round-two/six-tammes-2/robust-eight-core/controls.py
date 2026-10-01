"""Adverse certificate and scope controls, same author as the proof."""
from pathlib import Path
from fractions import Fraction as Q
import copy, importlib.util, json, subprocess, sys

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("robust_check", HERE / "check.py")
primary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(primary)


def rejected(action):
    try:
        action()
    except ValueError:
        return True
    raise ValueError("an adverse control was accepted")


def main():
    root = Path(sys.argv[sys.argv.index("--prerequisite-root") + 1]).resolve() \
        if "--prerequisite-root" in sys.argv else HERE.parents[2]
    config = json.loads((HERE / "certificate.json").read_text())
    primary.validate_config(config)
    cases = []
    for field, value, label in (
        ("edge_cosine_tolerance", [1, 10000000], "changed edge tolerance"),
        ("core_dot_relaxation", [1, 100000], "changed all-core relaxation"),
        ("coordinate_growth_bound", 100, "unsupported coordinate bound"),
        ("prescribed_edges", config["prescribed_edges"][:-1], "missing prescribed edge"),
    ):
        false = copy.deepcopy(config)
        false[field] = value
        rejected(lambda: primary.validate_config(false))
        cases.append(label)
    # This tests the actual margin calculation, not only a format rejection.
    script = "import sys;sys.path.insert(0,sys.argv[1]);import check;from pathlib import Path;from fractions import Fraction;check.verify_strip('upper',Path(sys.argv[2]),Fraction(1,100000))"
    result = subprocess.run([sys.executable, "-B", "-c", script, str(HERE), str(root)],
                            capture_output=True, text=True, timeout=55)
    if result.returncode == 0 or "every relaxed Bernstein omission" not in result.stderr:
        raise ValueError("larger relaxation was not rejected by its exact margin")
    cases.append("1/100000 rejected by a concrete relaxed Bernstein margin")
    # A nearby point cannot be replaced by a reflected model point while
    # silently retaining an unrelaxed inner-product inequality. Rational
    # unit vectors give an exact adverse example, with no floating input.
    x = (Q(1), Q(0), Q(0))
    model = (Q(3, 5), Q(4, 5), Q(0))
    # Rotate model toward -x by rational sine/cosine; the actual point
    # avoids x at t=3/5, while an oppositely perturbed model violates it.
    sine, cosine = Q(2 * 100000000, 100000000**2 + 1), Q(100000000**2 - 1, 100000000**2 + 1)
    actual = (cosine * model[0] - sine * model[1],
              sine * model[0] + cosine * model[1], Q(0))
    displaced_model = (cosine * model[0] + sine * model[1],
                       -sine * model[0] + cosine * model[1], Q(0))
    dot = lambda a, b: sum(c * d for c, d in zip(a, b))
    if not (dot(actual, actual) == dot(displaced_model, displaced_model) == dot(x, x) == 1
            and dot(x, actual) < Q(3, 5) < dot(x, displaced_model)
            and sum((a-b)**2 for a,b in zip(actual, displaced_model)) < Q(1,20000000)**2):
        raise ValueError("rational perturbation scope control failed")
    cases.append("nearby unit replacement requires the relaxed inequality")
    print(json.dumps({"agent": "six-tammes-2", "role": "researcher",
                      "status": "CONTROLS_VERIFIED", "controls": cases}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
