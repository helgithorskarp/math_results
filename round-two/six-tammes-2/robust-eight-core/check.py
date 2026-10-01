"""Exact full-proof replay and transfer of every core inequality.

Author: six-tammes-2, researcher. Uses pinned, published prerequisites.
No optimizer, floating point, network, or private input enters verification.
The old integer Bernstein transfer is adapted, with attribution, from
tammes15_seven_core_omitted_point_stability/check.py. All eight rows,
both cosine strips, and the approximate-contact reduction are new here.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import lcm
import hashlib, importlib.util, json, subprocess, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRIOR_NAMES = {
    "lower": "tammes15_octagon_model2_lower_strip_exclusion",
    "upper": "tammes15_octagon_model2_extension_exclusion",
}
EPSILON = Q(1, 20000000)
DELTA = Q(1, 156250)
CONTACTS = ((0, 1), (0, 7), (1, 2), (1, 7), (2, 3), (2, 6), (2, 7),
            (3, 4), (3, 5), (3, 6), (4, 5), (5, 6), (6, 7))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def validate_config(config):
    need(config["format"] == 1, "certificate format")
    need(config["edge_cosine_tolerance"] == [1, 20000000], "fixed epsilon")
    need(config["core_dot_relaxation"] == [1, 156250], "fixed delta")
    need(config["coordinate_growth_bound"] == 128, "fixed stability bound")
    need(config["prescribed_edges"] == [list(c) for c in CONTACTS], "fixed thirteen edges")
    need(128 * EPSILON == DELTA and EPSILON <= Q(1, 10000), "tolerance bridge")


def config_and_base(kind, root):
    config = json.loads((HERE / "certificate.json").read_text())
    validate_config(config)
    base = root / PRIOR_NAMES[kind]
    files = config["prerequisites"][kind]["files_sha256"]
    for name, expected in files.items():
        need(Path(name).name == name, "canonical pinned name")
        need(hashlib.sha256((base / name).read_bytes()).hexdigest() == expected,
             "pinned prerequisite " + kind + "/" + name)
    return config, base


def stability_constants():
    """Check the rational bounds used in the written analytic reduction.

    These checks do not formalize the geometric derivation in PROOF.md.
    """
    epsilon, lo, hi = Q(1, 10000), Q(14, 25), Q(593, 1000)
    need(0 < lo - epsilon and hi < Q(3, 5), "anchor scalar interval")
    need(1 - Q(3, 5) ** 2 >= Q(4, 5) ** 2, "anchor square-root lower bound")
    need(Q(3, 5) ** 2 <= 1 - Q(3, 5) ** 2, "square-root derivative at most one")
    # Derivative of (1-s^2)^(-1/2) is at most two on [0,3/5].
    need(Q(3, 5) ** 2 <= 4 * (1 - Q(3, 5) ** 2) ** 3,
         "inverse-square-root derivative at most two")
    need(3 * 2 + Q(1, 4) * 2 <= 7, "anchor second-coordinate error")
    need(Q(1, 4) * Q(5, 4) + 7 * epsilon < Q(1, 2), "anchor coordinate bound")
    need(1 - Q(3, 5) ** 2 - Q(1, 2) ** 2 > Q(1, 2) ** 2,
         "anchor normal component above one half")
    need(Q(6, 5) + 7 < 9 and 1 + 7 + 9 == 17, "anchor error seventeen")
    need(2 + 2 * (lo - epsilon) >= Q(8, 5) ** 2, "reflection denominator")
    need(2 * Q(3, 5) / Q(8, 5) <= Q(3, 4), "reflection axial coordinate")
    need(2 - 2 * hi >= Q(4, 5) ** 2, "reflection transverse denominator")
    need(1 - Q(3, 4) ** 2 - 4 * epsilon ** 2 > Q(1, 2) ** 2,
         "reflection normal component above one half")
    need(3 + 16 * epsilon <= 4, "reflection normal-coordinate error")
    need(10 * epsilon < Q(4, 5) and 2 * (1 - hi) > Q(4, 5) ** 2,
         "same-sign branch impossible")
    need(10 + 4 + 4 <= 20, "approximate reflection error twenty")
    need(hi + DELTA < 1 and 16 * (1 - hi) * (1 - hi - DELTA) ** 2 > 1,
         "complete square chart under relaxation of all eight core rows")
    need(4 * lo ** 4 - 2 * lo ** 3 + 3 * lo ** 2 - 1 < 0
         and (-6) ** 2 - 4 * 16 * 6 < 0, "published N14 cosine exceeds fourteen twenty-fifths")
    quintic = lambda x: 13*x**5 - x**4 + 6*x**3 + 2*x**2 - 3*x - 1
    need(quintic(Q(1, 2)) < 0 < quintic(hi), "incumbent root is below upper cutoff")
    need(65*Q(1, 2)**4 - 4*Q(3, 5)**3 + 18*Q(1, 2)**2 + 4*Q(1, 2) - 3 > 0,
         "quintic increases on one-half to three-fifths")
    error = {2: 0, 6: 2, 7: 17}
    folds = ((1, 2, 7, 6), (3, 2, 6, 7), (0, 1, 7, 2),
             (5, 3, 6, 2), (4, 3, 5, 6))
    for new, a, b, old in folds:
        error[new] = 20 + error[a] + error[b] + error[old]
    need(max(error.values()) == 122 and max(error.values()) < 128,
         "all eight errors below 128 epsilon")
    return {str(k): error[k] for k in sorted(error)}


def verify_strip(kind, root, delta=DELTA):
    config, base = config_and_base(kind, root)
    sys.path.insert(0, str(base))
    spec = importlib.util.spec_from_file_location("pinned_parent_check", base / "check.py")
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    from model import box_bounds, gmetric
    data = json.loads((base / "certificate.json").read_text())
    parts = parent.verify(data, details=True)
    old, leaves, adjacency, discards = parts[:4]
    need(old == json.loads((base / "EXPECTED.json").read_text()), "complete parent receipt")
    lo, hi = parent.LO, parent.HI
    need(lo >= Q(1, 4) and hi < 1, "decreasing positive chart Gram eigenvalues")

    def denominator_bound(cell):
        lower, upper = box_bounds(tuple(cell))
        return (1 + hi) ** 3 * (1 + max(gmetric((u, v), lo)
                                            for u, v in product(*zip(lower, upper))))

    rational = parent.t_bernstein_forms(2, lo, hi)
    denominators = [lcm(*(z.denominator for p in row for z in p))
                    for row in rational]
    integer = parts[-1]
    grid = 2 ** (max(c[0] for c in leaves + [tuple(z) for z in data["refined_cells"]]) - 2)
    bernstein = []
    limits = []
    for cell, method, label in discards:
        if method != "bernstein":
            continue
        d, i, j = cell
        side = 8 * grid // 2 ** d
        u, v = -4 * grid + i * side, -4 * grid + j * side
        values = []
        for f, linear_u, linear_v, square, cross in integer[label]:
            c00 = (4 * f * grid ** 2 + 4 * linear_u * u * grid
                   + 4 * linear_v * v * grid + 4 * square * (u * u + v * v)
                   + 4 * cross * u * v)
            c10 = 2 * side * (linear_u * grid + 2 * square * u + cross * v)
            c01 = 2 * side * (linear_v * grid + 2 * square * v + cross * u)
            c20, c11 = 4 * side * side * square, side * side * cross
            for r, s in product(range(3), repeat=2):
                values.append(c00 + r * c10 + s * c01
                              + (int(r == 2) + int(s == 2)) * c20 + r * s * c11)
        margin = Q(min(values), 4 * denominators[label] * grid ** 2)
        factor = denominator_bound(cell)
        relaxed = margin - delta * factor
        need(relaxed > 0, "every relaxed Bernstein omission " + str(cell))
        limits.append(margin / factor)
        bernstein.append([list(cell), label, str(margin), str(factor), str(relaxed)])

    duals = []
    if kind == "upper":
        from certificates import Rows, verify_dual
        rows = Rows(lo, hi)
        for tag, certificates in (("single", data["single_cells"]),
                                  ("pair", data["conditioned_pairs"])):
            for cert in certificates:
                if tag == "single":
                    cells = [tuple(cert["cell"])]
                    system = rows.single(cells[0])
                else:
                    cells = list(map(tuple, cert["cells"]))
                    system = rows.pair(*cells)
                original = verify_dual(system, cert)
                factors = [denominator_bound(c) for c in cells]
                weight = sum((Q(w) * factors[k // 8]
                              for k, w in zip(cert["support"], cert["weights"])
                              if k < 8 * len(cells)), Q(0))
                relaxed = original + delta * weight
                need(relaxed < 0, "every all-core relaxed dual RHS")
                if weight:
                    limits.append(-original / weight)
                duals.append([tag, [list(c) for c in cells], str(original),
                              str(weight), str(relaxed)])

    need(str(min(limits)) == config["prerequisites"][kind]["uniform_relaxation_limit"],
         "exact minimum relaxation limit")
    return {
        "strip": kind, "closed_interval": data["interval"],
        "bernstein_discards_transferred": len(bernstein),
        "duals_transferred": len(duals),
        "minimum_relaxed_Bernstein_margin": str(min(Q(z[-1]) for z in bernstein)),
        "maximum_relaxed_dual_rhs": str(max(Q(z[-1]) for z in duals)) if duals else None,
        "uniform_relaxation_limit": str(min(limits)),
        "bernstein_transfer_sha256": digest(bernstein),
        "dual_transfer_sha256": digest(duals),
        "cover_cells": old["cover_cells"],
        "graph_sha256": old["graph_sha256"],
        "tree_sha256": old["tree_sha256"],
        "clique_search_states": old["clique_search_states"],
    }


def main():
    root = Path(sys.argv[sys.argv.index("--prerequisite-root") + 1]).resolve() \
        if "--prerequisite-root" in sys.argv else ROOT
    if "--strip" in sys.argv:
        kind = sys.argv[sys.argv.index("--strip") + 1]
        need(kind in PRIOR_NAMES, "strip name")
        print(json.dumps(verify_strip(kind, root), sort_keys=True))
        return
    strips = []
    for kind in ("lower", "upper"):
        # Separate sequential processes isolate same-named prerequisite modules.
        result = subprocess.run([sys.executable, "-B", str(HERE / "check.py"),
                                 "--strip", kind, "--prerequisite-root", str(root)],
                                text=True, capture_output=True, timeout=55, check=True)
        strips.append(json.loads(result.stdout))
    result = {
        "agent": "six-tammes-2", "role": "researcher", "status": "VERIFIED",
        "edge_cosine_tolerance": str(EPSILON), "core_dot_relaxation": str(DELTA),
        "reflection_stability_constants": stability_constants(),
        "coordinate_growth_bound": 128,
        "closed_cosine_interval": [[14, 25], [593, 1000]],
        "prescribed_edges": json.loads((HERE / "certificate.json").read_text())["prescribed_edges"],
        "strips": strips, "global_Tammes15_bounds": "unchanged",
        "independent_peer_review": "pending",
        "trust_boundary": "Pinned exact complete parent proofs, exact margin transfer, and written unformalized reflection stability.",
    }
    expected = HERE / "EXPECTED.json"
    if expected.exists():
        need(result == json.loads(expected.read_text()), "complete new receipt")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
