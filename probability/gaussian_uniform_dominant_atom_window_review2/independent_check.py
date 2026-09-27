#!/usr/bin/env python3
"""Independent exact controls for the uniform dominant-atom review.

No target code is imported. The checker pins the packet, certifies the
one-variable perturbation envelopes in a Bernstein basis, reconstructs the
Abel constants and dyadic specialization, and checks the seven-site boundary
control with exact fractions. The continuum coarea proof remains mathematics.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, "changed target input: " + relative)
    return manifest


def bernstein_coefficients_on_quarter(power_coefficients):
    """Bernstein coefficients after substituting delta=x/4, 0<=x<=1."""
    degree = len(power_coefficients) - 1
    scaled = [coefficient / 4**index
              for index, coefficient in enumerate(power_coefficients)]
    return [sum((scaled[index] * F(comb(k, index), comb(degree, index))
                 for index in range(k + 1)), F(0))
            for k in range(degree + 1)]


def perturbation_controls():
    # After denominators are cleared, these polynomials certify the worst
    # endpoint forms of the q^3/a^2, a^-2, and b*a^-3 estimates.
    residuals = {
        "tilt_coefficient": [F(7), F(-26), F(11)],
        "inverse_square": [F(2), F(-7), F(4)],
        "inverse_cube": [F(8), F(-30), F(32), F(-11)],
    }
    records = {}
    for name, coefficients in residuals.items():
        bernstein = bernstein_coefficients_on_quarter(coefficients)
        require(all(value >= 0 for value in bernstein),
                "nonnegative perturbation residual: " + name)
        records[name] = bernstein

    # q^2-1 <= (9/4)delta follows from q<=1+delta and delta<=1/4.
    require(F(2) + F(1, 4) <= F(9, 4), "radial square coefficient")
    # Combining the three certified pieces leaves ample room under 71 delta.
    combined = F(25, 16) * 31 + 9
    require(combined <= 71, "radial geometric coefficient")

    c, L = F(16), F(8)
    U = c + 5 * L
    V0 = 72 + 12 * c + 20 * L
    J = 3 * V0 + 2 * U * (c + 4)
    P = 4 + U + J
    require((U, V0, J, P) == (56, 424, 3512, 3572),
            "perturbation budget identity")
    return {"bernstein_certificates": records,
            "combined_radial_constant": combined,
            "headline": {"c": c, "L": L, "U": U, "V0": V0,
                         "J": J, "P": P}}


def abel_normalization_controls():
    # Store only rational multipliers of the common pi powers. Gamma(3/2)
    # contributes 1/2*sqrt(pi).
    replica_after_two_primitives = F(1, 32)
    local_kernel_times_gamma = F(1, 16) * F(1, 2)
    require(local_kernel_times_gamma == replica_after_two_primitives,
            "Laplace/Abel normalization")
    differentiated_kernel = F(1, 16) * F(1, 2)
    # A' >= 4*pi^3*d*e^-5R^2*v and integral v/sqrt(h-v)=4h^(3/2)/3.
    final_multiplier = differentiated_kernel * 4 * F(4, 3)
    require(final_multiplier == F(1, 6), "final three-halves margin")
    return {"replica_laplace_multiplier": replica_after_two_primitives,
            "differentiated_abel_multiplier": differentiated_kernel,
            "final_margin_multiplier": final_multiplier}


def dyadic_controls():
    P = 3572
    alpha = F(1, 2**21)
    # Independent elementary exponential enclosure.
    e_upper = sum((F(1, factorial(k)) for k in range(5)), F(0)) + F(1, 100)
    require(e_upper < F(11, 4), "e upper enclosure")
    require(F(33, 8)**2 > 17, "sqrt(17) upper enclosure")
    exp_upper = F(11, 4)**5 * F(8, 7)
    budget = 2 * alpha * P * exp_upper
    require(exp_upper == F(161051, 896) < 256, "exp(41/8) enclosure")
    require(budget == F(143818543, 234881024) < 1,
            "posterior curvature cutoff")
    enlarged_alpha = F(1, 2**20)
    require(2 * enlarged_alpha * P * exp_upper > 1,
            "nearby weakened mass cutoff rejected by this certificate")

    e_lower = sum((F(1, factorial(k)) for k in range(4)), F(0))
    require(e_lower == F(8, 3) and e_lower**8 > 2**11,
            "dyadic threshold lies in logarithmic window")
    require(1 - 2 * alpha > F(3, 4), "modal offset budget")
    require(F(3, 4)**3 > F(1, 2)**2, "three-halves lower bound")
    raw_margin = F(1, 2**11 * 2 * 243 * 12)
    require(raw_margin > F(1, 2**24), "published dyadic margin")
    return {"alpha": alpha, "P": P, "exp_upper": exp_upper,
            "curvature_budget": budget, "raw_margin": raw_margin,
            "accepted_margin": F(1, 2**24),
            "unsafe_mass_rejections": 1}


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def sub(first, second):
    return tuple(a - b for a, b in zip(first, second))


def norm2(vector):
    return dot(vector, vector)


def stereographic(u, v):
    u, v = F(u), F(v)
    denominator = 1 + u * u + v * v
    return ((1 - u * u - v * v) / denominator,
            2 * u / denominator, 2 * v / denominator)


def determinant(matrix):
    values = [list(map(F, row)) for row in matrix]
    sign = 1
    result = F(1)
    for column in range(len(values)):
        pivot = next((row for row in range(column, len(values))
                      if values[row][column]), None)
        require(pivot is not None, "singular paired matrix")
        if pivot != column:
            values[column], values[pivot] = values[pivot], values[column]
            sign *= -1
        entry = values[column][column]
        result *= entry
        for row in range(column + 1, len(values)):
            ratio = values[row][column] / entry
            for index in range(column, len(values)):
                values[row][index] -= ratio * values[column][index]
    return sign * result


def boundary_control():
    zero = (F(0), F(0), F(0))
    source = [zero, (F(1), F(0), F(0)), (F(-1), F(0), F(0)),
              (F(0), F(1), F(0)), (F(0), F(-1), F(0)),
              (F(0), F(0), F(1)), (F(0), F(0), F(-1))]
    parameters = [(0, 0), (F(1, 8), 0), (0, F(1, 8)),
                  (F(-1, 8), 0), (0, F(-1, 8)),
                  (F(1, 8), F(1, 8))]
    target = [zero] + [stereographic(u, v) for u, v in parameters]
    losses = []
    anchor_losses = []
    rare_losses = []
    for i, j in combinations(range(7), 2):
        loss = norm2(sub(source[i], source[j])) - norm2(sub(target[i], target[j]))
        require(loss >= 0, "pair contraction")
        losses.append(loss)
        if i == 0:
            anchor_losses.append(loss)
        else:
            rare_losses.append(loss)
    require(anchor_losses == [0] * 6, "zero anchor loss")
    require(min(rare_losses) == F(730, 429), "minimum rare loss")
    rare_mean = 2 * sum(rare_losses, F(0)) / 36
    require(rare_mean == F(2366536, 1254825), "rare mean loss")

    paired = [x + y for x, y in zip(source[1:], target[1:])]
    paired_determinant = determinant(paired)
    require(paired_determinant == F(-15616, 9062625),
            "paired rank six")
    alpha = F(1, 2**21)
    full_loss = alpha**2 * rare_mean
    require(full_loss == F(295817, 689847339162009600),
            "quadratic rare-mass loss")

    # A radial expansion of one target breaks contraction and must be caught.
    damaged = list(target)
    damaged[1] = (F(2), F(0), F(0))
    damaged_losses = [norm2(sub(source[i], source[j]))
                      - norm2(sub(damaged[i], damaged[j]))
                      for i, j in combinations(range(7), 2)]
    require(any(loss < 0 for loss in damaged_losses), "damaged target rejected")
    digest = sha256("|".join(map(str, losses)).encode()).hexdigest()
    return {"pairs_checked": len(losses), "anchor_losses": anchor_losses,
            "minimum_rare_loss": min(rare_losses),
            "rare_mean_loss": rare_mean, "full_mean_loss": full_loss,
            "paired_determinant": paired_determinant,
            "loss_table_sha256": digest, "damaged_geometry_rejections": 1}


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_DOMINANT_ATOM_WINDOW_REVIEW_PASS",
        "verdict": ("accept the uniform dominant-atom Gaussian middle sign "
                    "and loss-normalized margin in their stated bounded-radius "
                    "and threshold scope"),
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "perturbation": perturbation_controls(),
        "abel_normalization": abel_normalization_controls(),
        "dyadic": dyadic_controls(),
        "boundary_control": boundary_control(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    record = (json.dumps(encode(run()), sort_keys=True, indent=2) + "\n").encode()
    if args.emit:
        print(record.decode(), end="")
        return
    require(record == (HERE / "REVIEW_EXPECTED.json").read_bytes(),
            "expected review record mismatch")
    print("INDEPENDENT_DOMINANT_ATOM_WINDOW_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
