#!/usr/bin/env python3
"""Independent exact controls for the regularized-contact margin review.

No target module is imported.  This pins the reviewed bytes and checks the
tail-loss decomposition, profile-mixture interface, scaling, and cutoff
exponents with standard-library rational arithmetic.  It is not Gaussian
quadrature and does not reprove the credited bounded-input theorem.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, f"changed target input: {relative}")
    return manifest


def exponent_controls():
    """Rebuild the growth bounds without importing the author's checker."""
    rounded = (9, 69, 72, 91, 34, 169, 181)
    raw = ((8, 2), (68, 1), (71, 3), (90, 8),
           (34, -1), (168, 3), (180, 6))
    schedules = []
    inequalities = 0
    for length, bits, extra in product(
            (1, 2, 7, 31, 200), (20, 21, 60, 1000), (0, 1, 8191)):
        minimum = 2 ** 20 * (length * length + bits + 1)
        m = minimum + extra
        q = F(m, 8192)
        require(q >= 2816, "minimum q")
        require(length * length <= q / 128, "radius schedule")
        require(bits + 1 <= q / 128, "noise schedule")

        # These are twice the two Gaussian exponents after e<4.
        require(8 * length * length + F(m, 32768) <= q,
                "tau exponent")
        require(32 * length * length + F(9 * m, 32768) <= 4 * q,
                "w exponent")

        for (slope, offset), coefficient in zip(raw, rounded):
            require(slope * q + offset <= coefficient * q,
                    "rounded cutoff exponent")
            require(coefficient * q <= 256 * q, "common cutoff weakening")
            inequalities += 2

        require(1 - m <= -F(m, 32), "conditional loss below cutoff")
        require(3 * m - 16 * q >= 7, "tail below retained margin")
        require(16 * q == F(m, 512), "final margin exponent")
        inequalities += 5
        schedules.append((length, bits, m, str(q)))

    # MGF identities: 2^(3/2)<3 and 3*2^(5/2)<17.
    require(2 ** 3 < 3 ** 2, "Gaussian tail probability constant")
    require(9 * 2 ** 5 < 17 ** 2, "Gaussian tail second-moment constant")
    require(17 * F(1, 16) < F(3, 2), "conditional covariance floor")
    require(64 * 16 <= 2 ** 16, "tail polynomial base")
    return {
        "parameter_schedules": len(schedules),
        "cutoff_and_tail_inequalities": inequalities,
        "rounded_cutoff_coefficients": list(rounded),
        "first_schedule": list(schedules[0]),
        "last_schedule": list(schedules[-1]),
        "gaussian_constant_checks": 4,
    }


def dot(first, second):
    return sum((x * y for x, y in zip(first, second)), F(0))


def sub(first, second):
    return tuple(x - y for x, y in zip(first, second))


def scale(amount, vector):
    return tuple(amount * x for x in vector)


def finite_tail_loss_controls():
    """Use diagonal contractions, distinct from the target's fold fixtures."""
    latent = [
        (F(1, 4), F(1, 4), F(1, 4)),
        (F(1, 4), F(-1, 4), F(-1, 4)),
        (F(-1, 4), F(1, 4), F(-1, 4)),
        (F(-1, 4), F(-1, 4), F(1, 4)),
    ]
    directions = [
        (F(1), F(0), F(0)), (F(-1), F(0), F(0)),
        (F(0), F(1), F(0)), (F(0), F(-1), F(0)),
        (F(0), F(0), F(1)), (F(0), F(0), F(-1)),
    ]
    cases = ordered_pairs = retained = scaling_checks = 0
    for tail_mass, outer, sigma in product(
            (F(1, 32), F(1, 128), F(1, 1024)),
            (F(2), F(5)),
            (F(1, 7), F(1, 11))):
        data = []
        for u in latent:
            for radius, mass, core in ((F(1), 1 - tail_mass, True),
                                       (outer, tail_mass, False)):
                for direction in directions:
                    x = tuple(a + sigma * radius * z for a, z in zip(u, direction))
                    # A global diagonal contraction, rather than the target fold.
                    y = (x[0] / 2, F(3, 4) * x[1], x[2])
                    data.append((x, y, F(mass, 24), core))
        require(sum((weight for _, _, weight, _ in data), F(0)) == 1,
                "finite probability")
        require(all(sum((weight * x[j] for x, _, weight, _ in data), F(0)) == 0
                    for j in range(3)), "full centering")
        require(all(sum((weight * x[j] for x, _, weight, core in data if core), F(0)) == 0
                    for j in range(3)), "conditional centering")

        total = core_core = discarded = F(0)
        for x, y, weight, core in data:
            for xp, yp, other_weight, other_core in data:
                source_difference, target_difference = sub(x, xp), sub(y, yp)
                loss = dot(source_difference, source_difference) - dot(
                    target_difference, target_difference)
                require(loss >= 0, "diagonal map expands a pair")
                weighted = weight * other_weight * loss
                total += weighted
                if core and other_core:
                    core_core += weighted
                else:
                    discarded += weighted
                for factor in (F(2, 3), F(7, 5)):
                    normalized = (dot(scale(factor, source_difference),
                                      scale(factor, source_difference))
                                  - dot(scale(factor, target_difference),
                                        scale(factor, target_difference))) / factor ** 2
                    require(normalized == loss, "variance scaling")
                    scaling_checks += 1
                ordered_pairs += 1

        conditional_loss = core_core / (1 - tail_mass) ** 2
        require(total == (1 - tail_mass) ** 2 * conditional_loss + discarded,
                "exact loss decomposition")
        moment = sum((weight * dot(x, x) for x, _, weight, _ in data), F(0))
        tail_moment = sum((weight * dot(x, x)
                           for x, _, weight, core in data if not core), F(0))
        require(discarded <= 2 * tail_moment + 2 * tail_mass * moment,
                "union tail-moment bound")
        if discarded <= total / 2 and tail_mass <= F(1, 8):
            require(total / 2 <= conditional_loss <= 2 * total,
                    "relative conditional loss retention")
            retained += 1
        cases += 1
    require(retained == cases, "all finite fixtures should retain loss")
    return {
        "finite_conditional_laws": cases,
        "ordered_pair_controls": ordered_pairs,
        "variance_scaling_controls": scaling_checks,
        "relative_loss_retention_cases": retained,
    }


def top_profile(values, count):
    return sum(sorted(values, reverse=True)[:count], F(0))


def profile_mixture_controls():
    """Exact finite-space analogue of the volume-sensitive L-infinity step."""
    source_core = [F(1, 7)] * 7
    target_core = [F(2, 7), F(2, 7), F(2, 7), F(1, 7), F(0), F(0), F(0)]
    tail_base = [F(i, 21) for i in range(7)]
    cap = F(2, 7)
    require(sum(source_core) == sum(target_core) == sum(tail_base) == 1,
            "discrete density masses")
    checks = 0
    for tail_mass, source_shift, target_shift in product(
            (F(1, 64), F(1, 256), F(1, 4096)), range(7), range(7)):
        source_tail = tail_base[source_shift:] + tail_base[:source_shift]
        target_tail = tail_base[target_shift:] + tail_base[:target_shift]
        source = [(1 - tail_mass) * x + tail_mass * y
                  for x, y in zip(source_core, source_tail)]
        target = [(1 - tail_mass) * x + tail_mass * y
                  for x, y in zip(target_core, target_tail)]
        for count in range(1, 8):
            source_error = abs(top_profile(source, count)
                               - top_profile(source_core, count))
            target_error = abs(top_profile(target, count)
                               - top_profile(target_core, count))
            require(source_error <= tail_mass * cap * count,
                    "source profile sup-norm stability")
            require(target_error <= tail_mass * cap * count,
                    "target profile sup-norm stability")
            core_gap = top_profile(target_core, count) - top_profile(source_core, count)
            full_gap = top_profile(target, count) - top_profile(source, count)
            require(full_gap >= core_gap - 2 * tail_mass * cap * count,
                    "two-profile mixture restoration")
            checks += 3
    return {"exact_profile_mixture_checks": checks, "universe_points": 7}


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_REGULARIZED_CONTACT_MARGIN_REVIEW_PASS",
        "scope": ("Pinned source, independent cutoff growth, tail-loss retention, "
                  "profile-mixture stability, and scaling controls; Gaussian analysis "
                  "and the accepted bounded-input theorem remain written mathematics."),
        "source_commit": manifest["source_commit"],
        "graph_artifact": manifest["graph_artifact"],
        "exponent_controls": exponent_controls(),
        "tail_loss_controls": finite_tail_loss_controls(),
        "profile_controls": profile_mixture_controls(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    encoded = (json.dumps(run(), indent=2, sort_keys=True) + "\n").encode()
    expected = HERE / "EXPECTED.json"
    if args.write_expected:
        require(not expected.exists(), "refusing to overwrite expected record")
        expected.write_bytes(encoded)
    else:
        require(expected.read_bytes() == encoded, "expected record differs")
    print("INDEPENDENT_REGULARIZED_CONTACT_MARGIN_REVIEW_PASS")
    print("record_sha256=" + sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
