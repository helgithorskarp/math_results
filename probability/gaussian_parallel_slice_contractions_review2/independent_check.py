"""Independent exact controls for the nonlinear parallel-slice theorem.

This checker imports no target module.  It uses a new three-slope scalar
profile and a different nonlinear transverse map, then verifies the
partition allocation, endpoint contraction, phase derivative at both
regular boundary clocks, axial fold, finite extension criterion, and the
two-Gaussian hinge cancellation with rational arithmetic.
"""
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET_COMMIT = "43c807f9ffe40fb40b7c2a44b8441cfd55324e84"
BREAKS = (Q(-2), Q(-1, 2), Q(1, 3), Q(2))
SLOPES = (Q(7, 25), Q(-20, 29), Q(9, 41))
UNUSED = (Q(24, 25), Q(21, 29), Q(40, 41))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_bytes(commit, path):
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    ).stdout


def pins():
    records = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for record in records:
        raw = git_bytes(record["commit"], record["path"])
        require(hashlib.sha256(raw).hexdigest() == record["sha256"],
                "reviewed source drift")
    return len(records)


def sqdist(x, y):
    require(len(x) == len(y), "dimension mismatch")
    return sum((a - b) ** 2 for a, b in zip(x, y))


def primitive(z, coefficients):
    require(BREAKS[0] <= z <= BREAKS[-1], "height outside review prism")
    total = Q(0)
    for lo, hi, coefficient in zip(BREAKS, BREAKS[1:], coefficients):
        total += max(Q(0), min(z, hi) - lo) * coefficient
        if z <= hi:
            break
    return total


def h(z):
    return primitive(z, SLOPES)


def unused_height(z):
    return primitive(z, UNUSED)


def unfolded_height(z):
    return primitive(z, tuple(abs(s) for s in SLOPES))


def transverse(point):
    x, y, z = point
    a = unused_height(z)
    return ((x * x + y * y + a * a) / 32, x * y / 32)


def target(point):
    return transverse(point) + (h(point[2]),)


def cuts(w, z):
    return (w,) + tuple(b for b in BREAKS[1:-1] if w < b < z) + (z,)


def allocated_chain(p, q):
    if p[2] > q[2]:
        p, q = q, p
    axial_cuts = cuts(p[2], q[2])
    lengths = [unused_height(z) - unused_height(w)
               for w, z in zip(axial_cuts, axial_cuts[1:])]
    total = sum(lengths, Q(0))
    require(total == unused_height(q[2]) - unused_height(p[2]) and total > 0,
            "unused-length additivity")
    prior = p
    partial = Q(0)
    checked = 0
    for z, ell in zip(axial_cuts[1:], lengths):
        partial += ell
        xy = tuple(p[j] + partial * (q[j] - p[j]) / total for j in range(2))
        current = xy + (z,)
        horizontal = sqdist(current[:2], prior[:2])
        dz = current[2] - prior[2]
        dh = h(current[2]) - h(prior[2])
        require(ell * ell == dz * dz - dh * dh,
                "Pythagorean cell length")
        require(horizontal + ell * ell ==
                (ell / total) ** 2 * (sqdist(p[:2], q[:2]) + total * total),
                "allocation identity")
        require(sqdist(target(current), target(prior)) <= sqdist(current, prior),
                "allocated endpoint step expands")
        prior = current
        checked += 1
    require(prior == q, "allocation endpoint mismatch")
    return checked


def phase_terms(p, q, endpoint_time):
    if p[2] > q[2]:
        p, q = q, p
    pieces = []
    for w, z in zip(cuts(p[2], q[2]), cuts(p[2], q[2])[1:]):
        index = next(i for i, (lo, hi) in enumerate(zip(BREAKS, BREAKS[1:]))
                     if lo <= w and z <= hi)
        pieces.append((z - w, SLOPES[index], UNUSED[index]))
    if endpoint_time == 0:
        q_values = [Q(1) for _ in pieces]
    else:
        require(endpoint_time == 1, "only exact regular boundary clocks used")
        q_values = [abs(slope) for _, slope, _ in pieces]
    length = sum(delta * q for (delta, _, _), q in zip(pieces, q_values))
    conjugate = sum(delta * omega * omega / q
                    for (delta, _, omega), q in zip(pieces, q_values))
    unused = sum(delta * omega for delta, _, omega in pieces)
    return length, conjugate, unused


def audit():
    pin_count = pins()
    require(all(s * s + omega * omega == 1 and omega > 0 and s != 0
                for s, omega in zip(SLOPES, UNUSED)),
            "profile is not exact unit speed")
    a_max = unused_height(BREAKS[-1])
    require(a_max < 4, "review transverse domain escaped its bound")

    # For G(x,y,a)=((x^2+y^2+a^2)/32,xy/32), the displayed number bounds
    # the squared Frobenius norm of DG on [-1,1]^2 x [0,a_max].
    g_frobenius_bound = Q(10, 1024) + a_max * a_max / 256
    require(g_frobenius_bound < 1, "nonlinear transverse map not short")

    z_values = (Q(-2), Q(-5, 4), Q(-1, 2), Q(-1, 12),
                Q(1, 3), Q(7, 6), Q(2))
    points = [(x, y, z) for x, y in itertools.product((Q(-1), Q(0), Q(1)), repeat=2)
              for z in z_values]
    endpoint_pairs = transverse_pairs = allocation_segments = 0
    phase_derivatives = fold_controls = 0
    for p, q in itertools.combinations(points, 2):
        du2 = sqdist(p[:2], q[:2])
        df2 = sqdist(transverse(p), transverse(q))
        da = unused_height(p[2]) - unused_height(q[2])
        require(df2 <= du2 + da * da, "transverse factor expands")
        require(sqdist(target(p), target(q)) <= sqdist(p, q),
                "full endpoint expands")
        transverse_pairs += 1
        endpoint_pairs += 1
        if p[2] != q[2]:
            allocation_segments += allocated_chain(p, q)
            delta_q = df2 - du2
            for time in (0, 1):
                length, conjugate, unused = phase_terms(p, q, time)
                require(unused * unused <= length * conjugate,
                        "exact Cauchy phase control")
                require(delta_q - length * conjugate <= 0,
                        "first-phase derivative positive")
                phase_derivatives += 1
        else:
            require(df2 <= du2, "equal-level phase expands")

        dx = unfolded_height(p[2]) - unfolded_height(q[2])
        dh = h(p[2]) - h(q[2])
        require(dh * dh <= dx * dx, "height quotient is not short")
        previous = None
        for s in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
            direct = ((1 - s) * dx + s * dh) ** 2 + s * (1 - s) * (dx - dh) ** 2
            affine = (1 - s) * dx * dx + s * dh * dh
            require(direct == affine, "leapfrog identity")
            require(previous is None or affine <= previous, "axial fold expands")
            previous = affine
            fold_controls += 1

    # Reconstruct the finite prescribed-frame criterion on every grid site.
    levels = sorted(set(z_values))
    budgets = {z: unused_height(z) for z in levels}
    for lo, hi in zip(levels, levels[1:]):
        dz, dh = hi - lo, h(hi) - h(lo)
        da = budgets[hi] - budgets[lo]
        require(da * da == dz * dz - dh * dh, "finite level budget")
    finite_pairs = 0
    for p, q in itertools.combinations(points, 2):
        require(sqdist(transverse(p), transverse(q)) <=
                sqdist(p[:2], q[:2]) + (budgets[p[2]] - budgets[q[2]]) ** 2,
                "finite extension criterion")
        finite_pairs += 1

    # In two Gaussian auxiliary coordinates gamma(Y)/gamma(0) is uniform.
    # The conditional density-tail identity is therefore purely algebraic.
    cancellation_controls = 0
    for density in (Q(1, 3), Q(1), Q(5, 2)):
        for threshold in (Q(0), Q(1, 2), Q(2), Q(3)):
            tail = density * max(Q(0), 1 - threshold / density)
            require(tail == max(Q(0), density - threshold),
                    "two-Gaussian hinge cancellation")
            cancellation_controls += 1

    hessian_determinants = [omega * omega / 4096 for omega in UNUSED]
    require(all(value > 0 for value in hessian_determinants),
            "nonlinear scalar lost strict convexity")
    payload = "|".join(map(str, [a_max, g_frobenius_bound, endpoint_pairs,
                                 allocation_segments, phase_derivatives,
                                 finite_pairs]))
    return {
        "status": "INDEPENDENT_NONLINEAR_PARALLEL_SLICE_REVIEW_PASS",
        "target_commit": TARGET_COMMIT,
        "source_pins": pin_count,
        "profile_slopes": [str(x) for x in SLOPES],
        "profile_unused_speeds": [str(x) for x in UNUSED],
        "unused_height_range": str(a_max),
        "nonlinear_G_frobenius_bound": str(g_frobenius_bound),
        "points": len(points),
        "endpoint_pairs": endpoint_pairs,
        "transverse_pairs": transverse_pairs,
        "allocation_segments": allocation_segments,
        "phase_boundary_derivatives": phase_derivatives,
        "fold_controls": fold_controls,
        "finite_extension_pairs": finite_pairs,
        "gaussian_cancellation_controls": cancellation_controls,
        "positive_hessian_determinants": [str(x) for x in hessian_determinants],
        "exact_state_sha256": hashlib.sha256(payload.encode()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
