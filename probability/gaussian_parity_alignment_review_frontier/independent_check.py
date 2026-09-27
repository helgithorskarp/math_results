#!/usr/bin/env python3
"""Definition-level exact checks for the parity-alignment review.

This checker imports no target code.  It uses only Python integers and
fractions and deliberately represents the orbit identity through Walsh
characters rather than the target checker's Laurent-polynomial expansion.
"""

from fractions import Fraction as Q
import hashlib
import itertools
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "probability" / "gaussian_parity_alignment"
PINS = {
    "PROOF.md": "8b6b47c15c7ccfd76d61ec9fdf2e936c8063cde02f5ac01a0a62255f2c37bf83",
    "verify.py": "d64f82c443cf0ed41d84d0e9d9e5dcf9a8b6415eb8cb07cd67e8e8638d82aaf2",
    "EXPECTED.json": "8c514711602ed3cc8ae3455490f2c0c1e5cbcece0a5f65b02eaef12d0efa9d1c",
}

SIGNS = tuple(itertools.product((-1, 1), repeat=3))
EVEN = tuple(e for e in SIGNS if e[0] * e[1] * e[2] == 1)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prod(values):
    answer = Q(1)
    for value in values:
        answer *= value
    return answer


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def norm2(x, y):
    return sum(((a - b) ** 2 for a, b in zip(x, y)), Q(0))


def scale(c, x):
    return tuple(Q(c) * a for a in x)


def cross(x, y):
    return (
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    )


def pinned_sources():
    for name, wanted in PINS.items():
        actual = hashlib.sha256((TARGET / name).read_bytes()).hexdigest()
        require(actual == wanted, f"source pin mismatch: {name}")


def walsh_spectrum(orbit):
    """Fourier coefficients of the uniform measure on a sign orbit."""
    require(len(orbit) == 4 and len(set(orbit)) == 4, "incomplete sign orbit")
    require(all(e in SIGNS for e in orbit), "non-sign orbit entry")
    spectrum = {}
    for mask in range(8):
        coefficient = sum(
            (prod(e[j] for j in range(3) if mask & (1 << j)) for e in orbit),
            Q(0),
        ) / 4
        if coefficient:
            spectrum[mask] = coefficient
    return spectrum


def character_check():
    require(walsh_spectrum(EVEN) == {0: Q(1), 7: Q(1)}, "even spectrum")
    odd = tuple(tuple(-x for x in e) for e in EVEN)
    require(walsh_spectrum(odd) == {0: Q(1), 7: Q(-1)}, "odd spectrum")
    damaged = EVEN[:-1] + ((1, 1, -1),)
    require(walsh_spectrum(damaged) != {0: Q(1), 7: Q(1)},
            "damaged orbit escaped detection")


def orbit_value(cosh_values, sinh_values, parity, reverse=False):
    """Evaluate the orbit directly from exp(+-z)=cosh(z)+-sinh(z)."""
    value = Q(0)
    for e in EVEN:
        value += prod(
            cosh_values[j]
            + (-1 if reverse else 1) * parity * e[j] * sinh_values[j]
            for j in range(3)
        )
    return value / 4


def hinge_sum(pair, threshold):
    return sum((max(value - threshold, Q(0)) for value in pair), Q(0))


def kernel_fixture(terms):
    """Check direct orbit sums against a separately formed 2x2 kernel."""
    require(terms and all(weight >= 0 for weight, _, _, _ in terms),
            "invalid fixture weights")
    source = [Q(0), Q(0)]
    aligned = [Q(0), Q(0)]
    inverse_source = [Q(0), Q(0)]
    inverse_aligned = [Q(0), Q(0)]
    C = B = D = Q(0)
    for weight, parity, cosh_values, sinh_values in terms:
        require(parity in (-1, 1), "bad parity")
        require(all(c >= b >= 0 for c, b in zip(cosh_values, sinh_values)),
                "bad hyperbolic amplitudes")
        C += weight * prod(cosh_values)
        B += weight * parity * prod(sinh_values)
        D += weight * prod(sinh_values)
        for side, reverse in enumerate((False, True)):
            source[side] += weight * orbit_value(
                cosh_values, sinh_values, parity, reverse)
            aligned[side] += weight * orbit_value(
                cosh_values, sinh_values, 1, reverse)
            inverse_source[side] += weight * orbit_value(
                cosh_values, sinh_values, parity, not reverse)
            inverse_aligned[side] += weight * orbit_value(
                cosh_values, sinh_values, 1, not reverse)

    require(source == [C + B, C - B], "direct source pair")
    require(aligned == [C + D, C - D], "direct aligned pair")
    require(inverse_source == [C - B, C + B], "inverse source pair")
    require(inverse_aligned == [C - D, C + D], "inverse aligned pair")
    require(C >= D >= abs(B), "kernel coefficient bounds")

    theta = (Q(1) + B / D) / 2 if D else Q(1, 2)
    matrix = ((theta, 1 - theta), (1 - theta, theta))
    require(all(value >= 0 for row in matrix for value in row), "kernel sign")
    require(all(sum(row) == 1 for row in matrix), "kernel row sums")
    require(all(sum(matrix[i][j] for i in range(2)) == 1 for j in range(2)),
            "kernel column sums")
    for direct_pair, endpoint_pair in (
        (source, aligned), (inverse_source, inverse_aligned)
    ):
        rebuilt = [
            sum((matrix[i][j] * endpoint_pair[j] for j in range(2)), Q(0))
            for i in range(2)
        ]
        require(rebuilt == direct_pair, "pair reconstruction")

    # Pairwise hinge comparison needs checking only at its exact breakpoints.
    for threshold in sorted(set([Q(0), *source, *aligned])):
        require(hinge_sum(source, threshold) <= hinge_sum(aligned, threshold),
                "hinge direction")
    # The clipped exponential-sum surrogate uses the opposite concavity sign.
    clipped_source = sum((min(value, Q(1)) for value in source), Q(0))
    clipped_aligned = sum((min(value, Q(1)) for value in aligned), Q(0))
    require(clipped_source >= clipped_aligned, "union clipping direction")
    # z^2 is an exact independent convex-energy control for the inverse field.
    require(sum(value * value for value in inverse_source)
            <= sum(value * value for value in inverse_aligned),
            "inverse convex-energy direction")

    bad_theta = theta + Q(1, 7)
    if D and bad_theta <= 1:
        bad = ((bad_theta, 1 - bad_theta), (1 - bad_theta, bad_theta))
        rebuilt = [sum((bad[i][j] * aligned[j] for j in range(2)), Q(0))
                   for i in range(2)]
        require(rebuilt != source, "mutated kernel accepted")


def kernel_checks():
    kernel_fixture([
        (Q(2, 7), 1, (Q(5, 2), Q(7, 3), Q(9, 4)),
         (Q(3, 2), Q(2, 3), Q(5, 4))),
        (Q(5, 7), -1, (Q(11, 4), Q(13, 5), Q(8, 3)),
         (Q(7, 4), Q(3, 5), Q(2, 3))),
    ])
    kernel_fixture([
        (Q(1, 3), 1, (Q(2), Q(3), Q(4)), (Q(0), Q(1), Q(2))),
        (Q(2, 3), -1, (Q(7, 3), Q(5, 2), Q(9, 4)),
         (Q(0), Q(1, 2), Q(3, 4))),
    ])


def parity(x):
    return 1 if prod(x) > 0 else -1


def box_check():
    corners = tuple(itertools.product((-2, -1, 1, 2), repeat=3))
    images = {x: scale(Q(parity(x), 4), x) for x in corners}
    same = opposite = 0
    for index, x in enumerate(corners):
        for y in corners[:index]:
            before = norm2(x, y)
            after = norm2(images[x], images[y])
            require(after <= before, "corner contraction")
            if parity(x) == parity(y):
                require(after == before / 16, "same-parity formula")
                same += 1
            else:
                require(before >= 4 and after <= 3, "opposite-parity bounds")
                opposite += 1
    require((same, opposite) == (992, 1024), "box-pair coverage")


def distance_map(points):
    return {
        (i, j): norm2(points[i], points[j])
        for i in range(len(points)) for j in range(i + 1, len(points))
    }


def eight_site_check():
    core = tuple(tuple(map(Q, e)) for e in EVEN)
    source = core + tuple(scale(-20, e) for e in core)
    target = core + tuple(scale(Q(58, 3), e) for e in core)
    ds = distance_map(source)
    dt = distance_map(target)
    require(all(dt[pair] <= ds[pair] for pair in ds), "endpoint contraction")
    require(sum(dt[pair] == ds[pair] for pair in ds) == 18, "tight-pair count")

    # Independently derive each outer point's two candidates from its three
    # tight face-sphere equations.  Equal face norms make the difference
    # equations homogeneous; their one-dimensional nullspace is span(v_i).
    for i, vertex in enumerate(core):
        face = tuple(core[j] for j in range(4) if j != i)
        u = tuple(face[1][k] - face[0][k] for k in range(3))
        v = tuple(face[2][k] - face[0][k] for k in range(3))
        normal = cross(u, v)
        require(dot(normal, normal) > 0, "degenerate face equations")
        ratios = [normal[k] / vertex[k] for k in range(3)]
        require(len(set(ratios)) == 1, "wrong sphere-line direction")
        require(all(dot(vertex, z) == -1 for z in face), "tetrahedral dot value")
        # |t v_i-z|^2=1163 gives 3 t^2+2 t-1160=0.
        roots = (Q(-20), Q(58, 3))
        require(sum(roots) == Q(-2, 3) and prod(roots) == Q(-1160, 3),
                "sphere quadratic roots")
        for root in roots:
            point = scale(root, vertex)
            require(all(norm2(point, z) == 1163 for z in face),
                    "sphere-root substitution")

    feasible = []
    for mask in range(16):
        points = core + tuple(
            target[4 + i] if mask & (1 << i) else source[4 + i]
            for i in range(4)
        )
        middle = distance_map(points)
        if all(dt[pair] <= middle[pair] <= ds[pair] for pair in ds):
            feasible.append(mask)
    require(feasible == [0, 15], "full interval state list")

    for i in range(4):
        for j in range(4):
            if i != j:
                mixed = norm2(source[4 + i], target[4 + j])
                require(mixed == 1548 < Q(26912, 9), "mixed-state obstruction")

    slope = (Q(58, 3) - 1) / 19
    require(slope == Q(55, 57) and 0 <= slope <= 1, "radial middle slope")
    require(1 + 19 * slope == Q(58, 3), "radial endpoint")
    require(Q(58, 3) == 20 - Q(2, 3), "radial final branch")


def main():
    pinned_sources()
    character_check()
    kernel_checks()
    box_check()
    eight_site_check()
    print("PARITY_ALIGNMENT_INDEPENDENT_ACCEPT")
    print("exact_arithmetic=fractions.Fraction")
    print("walsh_orbits=2 kernel_fixtures=2 box_pairs=2016 interval_states=16")
    print("universal_Gaussian_and_volume_limits=written_review")


if __name__ == "__main__":
    main()
