"""Independent exact controls for the strict norm-preserving theorem.

This checker imports no target module.  It uses a four-site rational
norm-preserving contraction unrelated to the author's calibration, and
recomputes the ordered loss, posterior comparison, positive-kernel exponent
bounds, radial-crossing constants, dyadic exponent, scaling, and the support-
net budget used by the openness corollary.  The measure-theoretic arguments
remain a human-audited proof boundary, not a consequence of these tests.
"""

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TARGET_COMMIT = "2106c12535f7ed647e8127ef17c14f899233d5e1"


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


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def minus(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def variance(points, weights):
    mean = tuple(sum((w * x[i] for w, x in zip(weights, points)), Q(0))
                 for i in range(3))
    return sum((w * norm2(x) for w, x in zip(weights, points)), Q(0)) - norm2(mean)


def ordered_loss(source, target, weights):
    return sum(
        (weights[i] * weights[j]
         * (norm2(minus(source[i], source[j]))
            - norm2(minus(target[i], target[j])))
         for i in range(len(weights)) for j in range(len(weights))),
        Q(0),
    )


def contraction_fixture():
    # Four equatorial source points.  The rational unit target points are
    # neither a collapse nor a rigid image, and every pair loss is nonnegative.
    source = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(-1), Q(0), Q(0)),
        (Q(0), Q(-1), Q(0)),
    )
    target = (
        (Q(1), Q(0), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(1), Q(0)),
        (Q(3, 5), Q(4, 5), Q(0)),
    )
    weights = (Q(1, 10), Q(1, 5), Q(3, 10), Q(2, 5))
    require(sum(weights, Q(0)) == 1, "weights")
    require(all(norm2(p) == norm2(q) == 1 for p, q in zip(source, target)),
            "anchor norms")
    pair_losses = []
    for i, j in itertools.combinations(range(len(weights)), 2):
        delta = norm2(minus(source[i], source[j])) - norm2(minus(target[i], target[j]))
        require(delta >= 0, "fixture is not short")
        pair_losses.append(delta)
    loss = ordered_loss(source, target, weights)
    require(loss == 2 * (variance(source, weights) - variance(target, weights)),
            "ordered loss/variance identity")
    require(loss > 0 and any(delta == 0 for delta in pair_losses),
            "fixture needs strict and tight pairs")
    return source, target, weights, pair_losses, loss


def posterior_controls(source, target, weights, base_loss):
    checked = 0
    for n in range(1, 42):
        likelihood = tuple(Q(1 + ((n + 2) * (i + 5)) % 23, 24)
                           for i in range(len(weights)))
        require(all(0 < ell <= 1 for ell in likelihood), "likelihood range")
        normalizer = sum((w * ell for w, ell in zip(weights, likelihood)), Q(0))
        posterior = tuple(w * ell / normalizer for w, ell in zip(weights, likelihood))
        beta = min(likelihood)
        # Since normalizer <= 1, d pi/d mu >= beta.  Applying this at both
        # endpoints of the ordered pair integral gives the squared floor.
        require(ordered_loss(source, target, posterior) >= beta * beta * base_loss,
                "posterior loss floor")
        checked += 1
    return checked


def kernel_controls(source, target):
    directions = (
        (Q(1), Q(0), Q(0)),
        (Q(3, 5), Q(4, 5), Q(0)),
        (Q(0), Q(5, 13), Q(12, 13)),
        (Q(-4, 5), Q(0), Q(3, 5)),
    )
    require(all(norm2(direction) == 1 for direction in directions),
            "nonunit kernel direction")
    checked = 0
    for theta, eta in itertools.product(directions, repeat=2):
        for u in (Q(0), Q(1, 9), Q(3, 5), Q(1)):
            for rho in (Q(1, 13), Q(3, 2), Q(9)):
                exponents = []
                for p, q in zip(source, target):
                    interpolation = (1 - u) * dot(theta, p) + u * dot(eta, q)
                    exponent = -rho * rho / 2 - norm2(p) / 2 + rho * interpolation
                    require(exponent <= 0, "kernel exceeds Gaussian normalization")
                    require(abs(-rho + interpolation) <= rho + 1,
                            "radial derivative bound")
                    require(abs(dot(eta, q) - dot(theta, p)) <= 2,
                            "time derivative bound")
                    exponents.append(exponent)
                for i, j in itertools.combinations(range(len(source)), 2):
                    require(exponents[i] + exponents[j] >= -(rho + 1) ** 2,
                            "kernel pair floor")
                checked += 1
    return checked


def antiderivative_u_weight(u):
    return u * u / 2 - u * u * u / 3


def schedule_controls():
    checked = 0
    minimum_exponent = None
    maximum_exponent = None
    for radius in range(1, 8):
        for j in range(7):
            for k in range(7):
                tau = Q(1, 2 ** j)
                epsilon = Q(1, 2 ** k)
                b_radius = radius + 1
                length = radius + 2 / tau
                width = length + radius
                a0 = epsilon / (16 * b_radius * radius)
                b0 = epsilon / (8 * b_radius * radius)

                require(2 * b_radius * radius * a0 == epsilon / 8,
                        "u-endpoint budget")
                require(b_radius * radius * b0 == epsilon / 8,
                        "angular endpoint budget")
                u_integral = (antiderivative_u_weight(1 - a0 / 2)
                              - antiderivative_u_weight(1 - a0))
                require(u_integral >= a0 * a0 / 8, "restricted time mass")
                require(tau * tau / (tau * tau + 2) <= tau / 2,
                        "far-end radial tail")

                # The rational factors in the real-parameter coefficient,
                # before pi*C and exp(-W^2), reproduce 2^-26 exactly.
                product = (4 * (epsilon / 4) ** 4 * Q(1, 2)
                           * (a0 * a0 / 8) * (b0 * b0 / 4) / width)
                target_product = (epsilon ** 8
                                  / (2 ** 26 * b_radius ** 4
                                     * radius ** 4 * width))
                require(product == target_product, "crossing prefactor")

                require(b_radius ** 4 * radius ** 4 <= 2 ** (4 + 8 * radius),
                        "radius dyadic bound")
                require(width.denominator == 1 and width <= 2 ** int(width),
                        "width dyadic bound")
                exponent = 2 * int(width) ** 2 + int(width) + 8 * radius + 8 * k + 33
                decomposed = (2 * int(width) ** 2 + int(width) + 8 * radius
                              + 8 * k + 3 + 26 + 4)
                require(exponent == decomposed, "dyadic exponent accounting")
                minimum_exponent = exponent if minimum_exponent is None else min(minimum_exponent, exponent)
                maximum_exponent = exponent if maximum_exponent is None else max(maximum_exponent, exponent)
                checked += 1
    return checked, minimum_exponent, maximum_exponent


def openness_controls():
    checked = 0
    for delta in (Q(1, 10), Q(1, 3), Q(3, 2), Q(7, 3)):
        eta = delta / 16
        for epsilon in (Q(0), eta / 3, eta / 2, eta):
            # Net support functions lose at most 2 eta; two transported
            # clouds lose another 2(eta+epsilon).
            retained = delta - 2 * eta - 2 * (eta + epsilon)
            require(retained >= delta / 2, "support-net gap not retained")
            checked += 1
    return checked


def scale_controls(source, target, weights, base_loss):
    checked = 0
    for scale in (Q(1, 3), Q(1, 2), Q(2), Q(5)):
        scaled_source = tuple(tuple(scale * coordinate for coordinate in p) for p in source)
        scaled_target = tuple(tuple(scale * coordinate for coordinate in q) for q in target)
        scaled_loss = ordered_loss(scaled_source, scaled_target, weights)
        variance = scale * scale
        require(scaled_loss == variance * base_loss, "spatial loss scaling")
        require(scaled_loss / variance == base_loss, "D/s invariance")
        checked += 1
    return checked


def audit():
    pin_count = pins()
    source, target, weights, pair_losses, loss = contraction_fixture()
    posterior_cases = posterior_controls(source, target, weights, loss)
    kernel_cases = kernel_controls(source, target)
    schedule_cases, exponent_min, exponent_max = schedule_controls()
    openness_cases = openness_controls()
    scale_cases = scale_controls(source, target, weights, loss)

    state = {
        "ordered_loss": str(loss),
        "pair_losses": [str(value) for value in pair_losses],
        "weights": [str(value) for value in weights],
        "schedule_exponent_range": [exponent_min, exponent_max],
    }
    state_hash = hashlib.sha256(
        json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "status": "INDEPENDENT_STRICT_GAUSSIAN_REVIEW_PASS",
        "target_commit": TARGET_COMMIT,
        "source_pins": pin_count,
        "fixture_sites": len(weights),
        "fixture_pairs": len(pair_losses),
        "fixture_tight_pairs": pair_losses.count(0),
        "fixture_ordered_loss": str(loss),
        "posterior_cases": posterior_cases,
        "kernel_cases": kernel_cases,
        "schedule_cases": schedule_cases,
        "schedule_exponent_range": [exponent_min, exponent_max],
        "openness_budget_cases": openness_cases,
        "scale_cases": scale_cases,
        "exact_state_sha256": state_hash,
        "trust_boundary": "Exact finite controls plus independent human audit; not formalization",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
