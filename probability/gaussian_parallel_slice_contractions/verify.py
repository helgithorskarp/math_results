"""Exact finite controls for PROOF.md; no continuum theorem is inferred by sampling.

CPython 3.11+, standard library. All checks survive optimized Python.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sign(x):
    return (x > 0) - (x < 0)


def surd_sign(a, b, d):
    """Exact sign of a+b*sqrt(d), for rational d>=0."""
    a, b, d = Q(a), Q(b), Q(d)
    require(d >= 0, "Negative radicand")
    if not b or not d:
        return sign(a)
    if not a:
        return sign(b)
    if sign(a) == sign(b):
        return sign(a)
    return sign(a) * sign(a * a - b * b * d)


def sqdist(x, y):
    require(len(x) == len(y), "Dimension mismatch")
    return sum(((a - b) ** 2 for a, b in zip(x, y)), Q(0))


def finite_slice_certificate(sources, targets, a_values):
    """Check Section 3.1 when the caller supplies exact rational level budgets.

    This verifies the full criterion for such data, not arbitrary algebraic
    radicals or the existence of favorable source/target frames.
    """
    require(len(sources) == len(targets) > 0, "Finite endpoint counts")
    require(all(len(p) == 3 for p in sources + targets), "Finite endpoint dimension")
    require(all(isinstance(v, (int, Q)) for p in sources + targets for v in p)
            and all(isinstance(a, (int, Q)) for a in a_values), "Nonrational certificate")
    heights = {}
    for p, q in zip(sources, targets):
        require(p[2] not in heights or heights[p[2]] == q[2], "Inconsistent target level")
        heights[p[2]] = q[2]
    levels = sorted(heights)
    require(len(a_values) == len(levels) and a_values[0] == 0, "Finite budget levels")
    budgets = dict(zip(levels, a_values))
    for lo, hi in zip(levels, levels[1:]):
        dz, dt = hi - lo, heights[hi] - heights[lo]
        da = budgets[hi] - budgets[lo]
        require(abs(dt) <= dz, "Scalar height is not short")
        require(da >= 0 and da * da == dz * dz - dt * dt, "Incorrect level budget")
    for i, j in combinations(range(len(sources)), 2):
        p, q = sources[i], sources[j]
        v, w = targets[i], targets[j]
        require(sqdist(v[:2], w[:2]) <= sqdist(p[:2], q[:2])
                + (budgets[p[2]] - budgets[q[2]]) ** 2, "Transverse finite guard")
        require(sqdist(v, w) <= sqdist(p, q), "Finite endpoint contraction")
    return len(sources) * (len(sources) - 1) // 2


@dataclass(frozen=True)
class Profile:
    name: str
    breaks: tuple
    slopes: tuple
    unused: tuple

    def __post_init__(self):
        require(len(self.breaks) == len(self.slopes) + 1, "Profile lengths")
        require(len(self.slopes) == len(self.unused), "Unused-speed lengths")
        require(self.breaks[0] == -1 and self.breaks[-1] == 1, "Profile domain")
        require(all(a < b for a, b in zip(self.breaks, self.breaks[1:])),
                "Unordered profile")
        require(all(w >= 0 and s * s + w * w == 1
                    for s, w in zip(self.slopes, self.unused)),
                "Invalid Pythagorean speed")

    def integral(self, z, which):
        require(-1 <= z <= 1, "Height outside domain")
        require(which in ("h", "A", "H"), "Unknown primitive")
        lo, hi = sorted((Q(0), z))
        coefficients = (self.slopes if which == "h" else self.unused
                        if which == "A" else tuple(abs(s) for s in self.slopes))
        total = sum((max(Q(0), min(hi, b) - max(lo, a)) * c
                     for a, b, c in zip(self.breaks, self.breaks[1:], coefficients)), Q(0))
        return total if z >= 0 else -total

    def partition(self, w, z, subdivisions):
        require(w <= z and subdivisions >= 1, "Partition input")
        cuts = [w] + [a for a in self.breaks if w < a < z] + [z]
        if w == z:
            return [w]
        out = [w]
        for a, b in zip(cuts, cuts[1:]):
            out.extend(a + (b - a) * Q(j, subdivisions)
                       for j in range(1, subdivisions + 1))
        return out


def planar(v):
    require(len(v) == 3, "Planar map requires three arguments")
    a, b, c = v
    return ((a * a + b * b + c * c) / 8,
            (a * b + a * c + b * c) / 8)


def transverse(profile, p):
    return planar((p[0], p[1], profile.integral(p[2], "A")))


def target(profile, p):
    return transverse(profile, p) + (profile.integral(p[2], "h"),)


def allocation(profile, p, q, subdivisions):
    """Check the actual allocated path, and its algebraic segment budgets."""
    if p[2] > q[2]:
        p, q = q, p
    w, z = p[2], q[2]
    cuts = profile.partition(w, z, subdivisions)
    lengths = [profile.integral(b, "A") - profile.integral(a, "A")
               for a, b in zip(cuts, cuts[1:])]
    for a, b, ell in zip(cuts, cuts[1:], lengths):
        dh = profile.integral(b, "h") - profile.integral(a, "h")
        require(ell >= 0 and ell * ell == (b - a) ** 2 - dh * dh,
                "Cell unused length")
    total = sum(lengths, Q(0))
    require(total == profile.integral(z, "A") - profile.integral(w, "A"),
            "Refined total unused length")
    du2 = sqdist(p[:2], q[:2])
    if not total:
        require(transverse(profile, (q[0], q[1], w)) == transverse(profile, q),
                "Zero-length vertical constancy")
        require(sqdist(transverse(profile, p), transverse(profile, q)) <= du2,
                "Zero-length horizontal bound")
        return 0, 1
    previous, partial = p, Q(0)
    for a, z_i, ell in zip(cuts, cuts[1:], lengths):
        partial += ell
        u_i = tuple(p[j] + partial * (q[j] - p[j]) / total for j in range(2))
        current = u_i + (z_i,)
        require(all(-1 <= x <= 1 for x in current), "Path outside prism")
        df2 = sqdist(transverse(profile, current), transverse(profile, previous))
        horizontal = sqdist(current[:2], previous[:2])
        require(df2 <= horizontal + ell * ell, "Allocated segment inequality")
        require(horizontal + ell * ell == (ell / total) ** 2 * (du2 + total * total),
                "Proportional allocation identity")
        require(sqdist(target(profile, current), target(profile, previous))
                <= sqdist(current, previous), "Actual allocated step not short")
        previous = current
    require(previous == q, "Allocation endpoint")
    return len(lengths), 0


def phase_data(profile, p, q, t):
    """Two-slope fixture: exact L*C and L^2, each a+b*sqrt(d)."""
    w, z = sorted((p[2], q[2]))
    left = max(Q(0), min(z, Q(0)) - w) if w < 0 else Q(0)
    right = max(Q(0), z - max(w, Q(0))) if z > 0 else Q(0)
    s0, s1 = profile.slopes
    o0, o1 = profile.unused
    q0, q1 = 1 - t + t * s0 * s0, 1 - t + t * s1 * s1
    require(q0 > 0 and q1 > 0, "Derivative clock singular")
    d = q0 * q1
    lc_a = left * left * o0 * o0 + right * right * o1 * o1
    lc_b = left * right * (o0 * o0 * q1 + o1 * o1 * q0) / d
    length_a = left * left * q0 + right * right * q1
    length_b = 2 * left * right
    return lc_a, lc_b, length_a, length_b, d


def rejects(call):
    try:
        call()
    except ValueError:
        return True
    return False


def run():
    fixture = Profile("nonlinear_fold", (Q(-1), Q(0), Q(1)),
                      (Q(-3, 5), Q(5, 13)), (Q(4, 5), Q(12, 13)))
    plateau = Profile("unit_and_zero_slopes", (Q(-1), Q(-1, 3), Q(1, 3), Q(1)),
                      (Q(1), Q(0), Q(-1)), (Q(0), Q(1), Q(0)))
    zero_unused = Profile("all_unused_length_zero", (Q(-1), Q(0), Q(1)),
                          (Q(-1), Q(1)), (Q(0), Q(0)))
    profiles = (fixture, plateau, zero_unused)
    points = list(product((Q(-1), Q(0), Q(1)), repeat=2))
    points = [u + (z,) for u in points
              for z in (Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1))]
    times = (Q(0), Q(1, 5), Q(1, 3), Q(1, 2), Q(3, 4), Q(9, 10), Q(1))
    fold_times = (Q(0), Q(1, 5), Q(1, 2), Q(4, 5), Q(1))
    counts = dict(endpoint_pairs=0, transverse_pairs=0, allocation_segments=0,
                  zero_total_allocations=0, phase_derivatives=0, cauchy_controls=0,
                  phase_endpoint_controls=0, fold_controls=0, surd_controls=0,
                  finite_extension_certificates=0, finite_extension_pairs=0)
    surds = [(0, 1, 2, 1), (0, -1, 2, -1), (Q(3, 2), -1, 2, 1),
             (-Q(3, 2), 1, 2, -1), (1, -1, 2, -1), (-1, 1, 2, 1),
             (2, -1, 4, 0), (-2, 1, 4, 0), (0, 8, 0, 0)]
    for a, b, d, expected in surds:
        require(surd_sign(a, b, d) == expected, "Surd sign control")
        counts["surd_controls"] += 1
    for profile in profiles:
        for p, q in combinations(points, 2):
            tp, tq = target(profile, p), target(profile, q)
            require(sqdist(tp, tq) <= sqdist(p, q), "Fixture endpoint pair")
            counts["endpoint_pairs"] += 1
            fp, fq = tp[:2], tq[:2]
            du2, df2 = sqdist(p[:2], q[:2]), sqdist(fp, fq)
            da = profile.integral(p[2], "A") - profile.integral(q[2], "A")
            require(df2 <= du2 + da * da, "Transverse bound")
            counts["transverse_pairs"] += 1
            for sub in (1, 2, 4):
                segments, zeros = allocation(profile, p, q, sub)
                counts["allocation_segments"] += segments
                counts["zero_total_allocations"] += zeros
            hp, hq = profile.integral(p[2], "h"), profile.integral(q[2], "h")
            xp, xq = profile.integral(p[2], "H"), profile.integral(q[2], "H")
            require((hp - hq) ** 2 <= (xp - xq) ** 2, "Unfolded height quotient")
            previous = None
            for s in fold_times:
                axial = (1 - s) * (xp - xq) + s * (hp - hq)
                aux_square = s * (1 - s) * ((xp - hp) - (xq - hq)) ** 2
                value = df2 + axial * axial + aux_square
                require(value == df2 + (1 - s) * (xp - xq) ** 2 + s * (hp - hq) ** 2,
                        "Leapfrog pair identity")
                require(previous is None or value <= previous, "Fold not monotone")
                previous = value
                counts["fold_controls"] += 1
            require(previous == sqdist(tp, tq), "Fold endpoint")
            if profile is fixture:
                for t in times:
                    la, lb, sa, sb, d = phase_data(profile, p, q, t)
                    require(surd_sign(la - (df2 - du2), lb, d) >= 0,
                            "First-phase derivative sign")
                    require(surd_sign(la - da * da, lb, d) >= 0, "Cauchy slack")
                    counts["phase_derivatives"] += 1
                    counts["cauchy_controls"] += 1
                    if t in (0, 1):
                        wanted = sqdist(p, q) if t == 0 else df2 + (xp - xq) ** 2
                        require(surd_sign((1 - t) * du2 + t * df2 + sa - wanted, sb, d) == 0,
                                "First-phase endpoint identity")
                        counts["phase_endpoint_controls"] += 1

    # Written whole-cube bounds; finite controls reconstruct their exact constants.
    g_bound = 6 * Q(1, 4) ** 2
    t_bound = g_bound + Q(3, 5) ** 2
    require(g_bound == Q(3, 8) and t_bound == Q(147, 200) < 1, "Global fixture bound")
    hessian_determinants = []
    for c in fixture.unused:
        diagonal = (Q(1, 4), Q(1, 4), c * c / 4)
        require(all(a > 0 for a in diagonal), "Hessian definiteness")
        hessian_determinants.append(str(diagonal[0] * diagonal[1] * diagonal[2]))

    rejected = []
    for name, call in [
        ("negative_surd_radicand", lambda: surd_sign(1, 1, -1)),
        ("invalid_profile_speed", lambda: Profile("bad", (Q(-1), Q(1)), (Q(1),), (Q(1),))),
        ("unordered_profile", lambda: Profile("bad", (Q(-1), Q(1, 2), Q(0), Q(1)),
                                               (Q(0),) * 3, (Q(1),) * 3)),
        ("wrong_planar_dimension", lambda: planar((Q(1), Q(2))))]:
        require(rejects(call), "Malformed control accepted: " + name)
        rejected.append(name)
    # sqrt(1-h'^2) cannot be replaced by 1-|h'|.
    require(Q(4, 5) ** 2 > (1 - Q(3, 5)) ** 2, "Wrong axial length not excluded")
    rejected.append("linear_instead_of_pythagorean_unused_length")
    # Two vertical endpoints are short, but h(z)=|z| would force constant f.
    require(sqdist((-1, 0, 1), (1, 0, 1)) == sqdist((0, 0, -1), (0, 0, 1)) == 4,
            "Finite-only control is not contractive")
    zero_budget = zero_unused.integral(Q(1), "A") - zero_unused.integral(Q(-1), "A")
    require(sqdist((-1, 0), (1, 0)) > zero_budget * zero_budget,
            "Finite-only nonexistent zero-length extension")
    rejected.append("finite_endpoints_substituted_for_whole_prism")
    # f(z)=(4z/5,0), h(z)=3|z|/5: a raw linear height clock increases distance.
    raw_derivative = 4 * Q(4, 5) ** 2 - 8 * (1 - Q(9, 10))
    require(raw_derivative == Q(44, 25) > 0, "Wrong height clock not excluded")
    rejected.append("raw_linear_height_clock")
    p, q = (Q(0),) * 3, (Q(1),) * 3
    bad_q = tuple(8 * a for a in transverse(fixture, q)) + (fixture.integral(q[2], "h"),)
    require(sqdist(target(fixture, p), bad_q) > sqdist(p, q), "Inflated fixture accepted")
    rejected.append("inflated_nonlinear_map")

    # Finite consumer: nonlinear data, a saturated fold with repeated transformed
    # sites, and the one-level boundary. No G-extension is computed numerically.
    fixture_heights = sorted({p[2] for p in points})
    anchor = fixture.integral(fixture_heights[0], "A")
    finite_cases = [
        (points, [target(fixture, p) for p in points],
         [fixture.integral(z, "A") - anchor for z in fixture_heights]),
        ([(0, 0, -1), (1, 0, 0), (0, 0, 1)],
         [(0, 0, 1), (1, 0, 0), (0, 0, 1)], [0, 0, 0]),
        ([(0, 0, 2), (2, 0, 2)], [(0, 0, 3), (1, 0, 3)], [0])]
    for xs, ys, aa in finite_cases:
        counts["finite_extension_pairs"] += finite_slice_certificate(xs, ys, aa)
        counts["finite_extension_certificates"] += 1
    # These three endpoint assignments are an isometry, but cannot extend with
    # scalar output height in these particular frames: both level budgets vanish.
    isometry_x = [(0, 0, -1), (0, 1, 0), (0, 0, 1)]
    isometry_y = [(-1, 0, 1), (0, 0, 0), (1, 0, 1)]
    require(all(sqdist(isometry_x[i], isometry_x[j]) == sqdist(isometry_y[i], isometry_y[j])
                for i, j in combinations(range(3), 2)), "Finite control not isometric")
    for name, call in [
        ("finite_scalar_height_inconsistent", lambda: finite_slice_certificate(
            [(0, 0, 0), (2, 0, 0)], [(0, 0, 0), (0, 0, 1)], [0])),
        ("finite_scalar_slope_too_large", lambda: finite_slice_certificate(
            [(0, 0, 0), (0, 0, 1)], [(0, 0, 0), (0, 0, 2)], [0, 0])),
        ("finite_budget_mismatched", lambda: finite_slice_certificate(
            [(0, 0, 0), (0, 0, 1)], [(0, 0, 0), (0, 0, Q(3, 5))], [0, Q(3, 4)])),
        ("finite_isometry_wrong_prescribed_frames", lambda: finite_slice_certificate(
            isometry_x, isometry_y, [0, 0, 0])),
        ("finite_float_in_exact_certificate", lambda: finite_slice_certificate(
            [(0, 0, 0)], [(0.0, 0, 0)], [0]))]:
        require(rejects(call), "Finite malformed control accepted: " + name)
        rejected.append(name)

    record = dict(status="NONLINEAR_PARALLEL_SLICE_EXACT_CONTROLS_PASS",
                  profiles=[p.name for p in profiles], points_per_profile=len(points),
                  counts=counts, global_G_frobenius_square=str(g_bound),
                  global_T_frobenius_square=str(t_bound),
                  positive_hessian_determinants=hessian_determinants,
                  rejected_controls=rejected,
                  trust_boundary="Exact finite algebra and nonlinear fixtures; dyadic convergence, universal geometry, C1 reparametrization and classical transfers are written proofs.")
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    record["record_sha256"] = hashlib.sha256(canonical).hexdigest()
    return record


if __name__ == "__main__":
    output = run()
    expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
    require(output == expected, "Expected record mismatch")
    print(json.dumps(output, indent=2))
