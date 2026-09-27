#!/usr/bin/env python3
"""Exact controls for PROOF.md; no Gaussian integration or large replay."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

E = tuple(v for v in itertools.product((1, -1), repeat=3)
          if v[0] * v[1] * v[2] == 1)
ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def frac(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else str(q)


def product(xs):
    out = F(1)
    for x in xs:
        out *= x
    return out


def orbit(q, sigma):
    return sum((product(q[j] ** (sigma * e[j]) for j in range(3))
                for e in E), F(0)) / 4


def validate_terms(terms):
    require(bool(terms), "empty orbit list")
    for q, sigma, coefficient in terms:
        require(len(q) == 3 and all(F(x) >= 1 for x in q),
                "nonnegative log variables required")
        require(sigma in (-1, 1), "invalid parity")
        require(F(coefficient) >= 0, "negative coefficient")
    require(any(F(c) > 0 for _, _, c in terms), "zero total coefficient")


def witness(terms):
    validate_terms(terms)
    c = b = d = F(0)
    direct = [F(0), F(0)]
    aligned = [F(0), F(0)]
    for q0, sigma, coefficient in terms:
        q = tuple(map(F, q0))
        w = F(coefficient)
        ca = product((z + 1/z)/2 for z in q)
        ba = product((z - 1/z)/2 for z in q)
        c += w * ca
        b += w * sigma * ba
        d += w * ba
        for side in (0, 1):
            qq = q if side == 0 else tuple(1/z for z in q)
            direct[side] += w * orbit(qq, sigma)
            aligned[side] += w * orbit(qq, 1)
    require(d >= abs(b) and c >= d, "invalid amplitude")
    require(direct == [c+b, c-b], "source orbit expansion")
    require(aligned == [c+d, c-d], "aligned orbit expansion")
    theta = (1+b/d)/2 if d else F(1, 2)
    matrix = ((theta, 1-theta), (1-theta, theta))
    require(all(x >= 0 for row in matrix for x in row), "negative kernel")
    require(all(sum(row) == 1 for row in matrix), "row sum")
    require(all(sum(matrix[i][j] for i in range(2)) == 1
                for j in range(2)), "column sum")
    require([sum(matrix[i][j]*aligned[j] for j in range(2))
             for i in range(2)] == direct, "kernel reconstruction")

    # The pair-hinge difference is piecewise affine. Its four possible
    # density breakpoints, zero, and a point above all values suffice.
    knots = sorted(set([F(0)] + direct + aligned))
    knots.append(knots[-1]+1)
    gaps = []
    for h in knots:
        gain = sum(max(x-h, 0) for x in aligned) - sum(
            max(x-h, 0) for x in direct)
        require(gain >= 0, "negative breakpoint hinge")
        gaps.append(gain)
    return {
        "orbit_count": len(terms),
        "source_pair": list(map(frac, direct)),
        "aligned_pair": list(map(frac, aligned)),
        "theta": frac(theta),
        "breakpoint_count": len(knots),
        "maximum_breakpoint_gain": frac(max(gaps)),
        "inverse_exponent_pair": list(map(frac, reversed(direct))),
        "status": "EXACT_DOUBLY_STOCHASTIC",
    }


def laurent_identity():
    # Independent formal coefficient expansion:
    # product cosh + sigma product sinh, with q_j=exp(z_j).
    all_signs = list(itertools.product((1, -1), repeat=3))
    records = []
    for sigma in (1, -1):
        direct = {tuple(sigma*x for x in e): F(1, 4) for e in E}
        expanded = {}
        for exponent in all_signs:
            coefficient = F(1, 8) + sigma*F(product(exponent), 8)
            if coefficient:
                expanded[exponent] = coefficient
        require(direct == expanded, "formal Laurent identity")
        records.append({"parity": sigma, "nonzero_monomials": len(direct),
                        "coefficient": "1/4"})
    return records


def norm2(x, y):
    return sum((a-b)**2 for a, b in zip(x, y))


def scale(a, v):
    return tuple(F(a)*x for x in v)


def distances(points):
    return {(i, j): norm2(points[i], points[j])
            for i in range(len(points)) for j in range(i+1, len(points))}


def balanced_orbit(weights):
    require(len(weights) == 4 and all(F(w) >= 0 for w in weights),
            "invalid orbit weights")
    require(len(set(map(F, weights))) == 1, "nonuniform orbit weights")


def geometry():
    core = [tuple(map(F, e)) for e in E]
    source = core + [scale(-20, e) for e in E]
    target = core + [scale(F(58, 3), e) for e in E]
    aligned = core + [scale(20, e) for e in E]
    ds, dt, da = map(distances, (source, target, aligned))
    losses = [ds[p]-dt[p] for p in ds]
    require(min(losses) == 0, "target is not a contraction")
    require(losses.count(0) == 18, "tight pair count")
    categories = {"core": set(), "off_diagonal_cross": set(),
                  "diagonal_cross": set(), "outer": set()}
    for (i, j), d in ds.items():
        if j < 4:
            category = "core"
        elif i >= 4:
            category = "outer"
        elif i == j-4:
            category = "diagonal_cross"
        else:
            category = "off_diagonal_cross"
        categories[category].add((d, dt[(i, j)]))
    require(all(len(v) == 1 for v in categories.values()), "distance classes")

    interval = []
    rejected = []
    for mask in range(16):
        points = core + [target[i+4] if (mask >> i) & 1 else source[i+4]
                         for i in range(4)]
        dd = distances(points)
        bad = [(i, j) for (i, j) in ds
               if not dt[(i, j)] <= dd[(i, j)] <= ds[(i, j)]]
        if bad:
            pair = bad[0]
            rejected.append({"mask": mask, "pair": list(pair),
                             "distance": frac(dd[pair]),
                             "target_lower_bound": frac(dt[pair])})
        else:
            interval.append(mask)
    require(interval == [0, 15], "full finite interval")
    require(all(r["distance"] == "1548" for r in rejected), "mixed distance")
    require(len(rejected) == 14, "incomplete mask check")

    lam = 1-F(1, 2**20)
    strict_target = [scale(lam, v) for v in target]
    strict_distances = distances(strict_target)
    minimum = min(ds[p]-strict_distances[p] for p in ds)
    require(minimum > F(1, 2**18), "strict target margin")
    radial_slope = (F(58, 3)-1)/19
    require(radial_slope == F(55, 57) and 0 <= radial_slope <= 1,
            "radial profile")
    require(1+19*radial_slope == F(58, 3), "profile endpoint")
    require(all(da[p] >= dt[p] for p in ds), "radial endpoint contraction")
    expanded_pair = (0, 5)
    require(da[expanded_pair]-ds[expanded_pair] == 80,
            "alignment expansion control")

    priors = []
    for alpha in (F(0), F(1, 7), F(1, 2), F(1)):
        ws = [F(1-alpha, 4)]*4 + [F(alpha, 4)]*4
        balanced_orbit(ws[:4]); balanced_orbit(ws[4:])
        require(sum(ws) == 1, "prior normalization")
        priors.append({"alpha": frac(alpha), "core_mass_per_atom": frac(ws[0]),
                       "outer_mass_per_atom": frac(ws[4])})

    # The three prescribed face centres are noncollinear, and both
    # candidate positions satisfy every tight sphere equation.
    for i in range(4):
        face = [core[j] for j in range(4) if j != i]
        u = tuple(face[1][j]-face[0][j] for j in range(3))
        v = tuple(face[2][j]-face[0][j] for j in range(3))
        cross = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2],
                 u[0]*v[1]-u[1]*v[0])
        require(sum(x*x for x in cross) > 0, "degenerate face")
        for point in (source[i+4], target[i+4]):
            require(all(norm2(point, z) == 1163 for z in face),
                    "tight face spheres")

    return {
        "labels": 8, "pairs": len(losses), "tight_pairs": losses.count(0),
        "strict_pairs": sum(x > 0 for x in losses),
        "distance_categories": {
            k: {"source": frac(next(iter(v))[0]),
                "target": frac(next(iter(v))[1])}
            for k, v in categories.items()},
        "full_interval_masks": interval,
        "rejected_masks": [r["mask"] for r in rejected],
        "mixed_distance": "1548", "mixed_lower_bound": "26912/9",
        "mixed_deficit": frac(F(26912, 9)-1548),
        "strict_target_factor": frac(lam),
        "strict_target_minimum_pair_loss": frac(minimum),
        "radial_profile_slope": frac(radial_slope),
        "alignment_squared_distance_expansion": "80",
        "prior_controls": priors,
    }


def rejected_controls():
    damaged = [
        ("negative coefficient", lambda: witness([((2, 3, 4), 1, F(-1))])),
        ("invalid parity", lambda: witness([((2, 3, 4), 0, F(1))])),
        ("invalid exponential variable",
         lambda: witness([((0, 3, 4), 1, F(1))])),
        ("nonuniform orbit",
         lambda: balanced_orbit([F(1, 5), F(1, 5), F(1, 5), F(2, 5)])),
    ]
    result = []
    for name, operation in damaged:
        try:
            operation()
        except ValueError as exc:
            result.append({"control": name, "rejected": True, "reason": str(exc)})
        else:
            raise ValueError("damaged control accepted: "+name)
    return result


def box_application():
    points = list(itertools.product((F(-2), F(-1), F(1), F(2)), repeat=3))
    def parity(x):
        return 1 if product(x) > 0 else -1
    images = [scale(F(parity(x), 4), x) for x in points]
    same = opposite = 0
    for i, x in enumerate(points):
        for j in range(i):
            y = points[j]
            ds = norm2(x, y); dt = norm2(images[i], images[j])
            require(dt <= ds, "box map contraction")
            if parity(x) == parity(y):
                require(dt == ds/16, "same-parity scaling")
                same += 1
            else:
                require(ds >= 4 and dt <= 3, "opposite-parity bounds")
                opposite += 1
    return {"box_corner_labels": len(points), "same_parity_pairs": same,
            "opposite_parity_pairs": opposite,
            "universal_source_lower_bound": "4",
            "universal_target_upper_bound": "3",
            "scope": "Corner checks supplement the written all-box proof."}


def report():
    cases = {
        "mixed": [((2, 3, 5), 1, F(2, 7)),
                  ((3, 2, 4), -1, F(5, 7))],
        "anisotropic_three_orbits": [((F(3, 2), 2, 5), 1, F(1, 3)),
                                   ((2, F(4, 3), 3), -1, F(1, 2)),
                                   ((3, 4, F(5, 4)), 1, F(1, 6))],
        "coordinate_plane": [((1, 3, 5), 1, F(1, 3)),
                             ((1, 2, 4), -1, F(2, 3))],
        "single_positive": [((2, 3, 5), 1, F(1))],
        "single_negative": [((2, 3, 5), -1, F(1))],
        "balanced_equal_orbits": [((2, 3, 5), 1, F(1, 2)),
                                 ((2, 3, 5), -1, F(1, 2))],
    }
    witnesses = {name: witness(value) for name, value in cases.items()}
    require(F(witnesses["mixed"]["maximum_breakpoint_gain"]) > 0,
            "missing strict convexity control")
    return {
        "status": "PARITY_ALIGNMENT_EXACT_CONTROLS_PASS",
        "arithmetic": "Python arbitrary integers and fractions.Fraction",
        "laurent_identity": laurent_identity(),
        "density_pair_controls": witnesses,
        "eight_site_geometry": geometry(),
        "continuous_box_application": box_application(),
        "damaged_inputs": rejected_controls(),
        "trust_boundary": (
            "Exact algebra and sixteen finite candidates only. Universal Gaussian "
            "integration, dominated limits and the credited radial theorem remain "
            "written proofs. No quadrature, old audit replay, or independent review."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = json.dumps(report(), indent=2, sort_keys=True)+"\n"
    if args.check:
        expected = (ROOT/"EXPECTED.json").read_text()
        require(output == expected, "expected output mismatch")
        print("PARITY_ALIGNMENT_EXACT_CONTROLS_PASS")
        print("EXPECTED sha256="+hashlib.sha256(output.encode()).hexdigest())
        print("No Gaussian quadrature or large certificate replay was run.")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
