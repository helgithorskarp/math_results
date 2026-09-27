#!/usr/bin/env python3
"""Independent exact audit of the deep-flap Gaussian cell.

The radial certificate is recomputed without importing target code.  Unlike
the target's alternating exponential series, this checker uses the elementary
binomial enclosure

    (1-x/2^k)^(2^k) <= exp(-x) <= (1+x/2^k)^(-2^k).

All powers and reciprocals are rounded outwards with Python integers.
"""

from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
from json import dumps, loads
from math import ceil, exp, floor, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_deep_flap_cell"
PINS = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "CELL.json": "0128192ba0572151cfbbf7611d627d2177e1f25628f1424ef99d99ddbc59e4d0",
    "EXPECTED.json": "f00fd3bd6b973ab64a141275927e8222199f130c619d7d3955490f04fca69c41",
    "PROOF.md": "4e8b8ebd680cb0b7fc831757ea4f0d500559445c609431ff61c31df5ebc60c87",
    "README.md": "9cc26ac8335f015ff7f6e800127b409c40037bb855b2bd62c5af30dacc00d331",
    "SOURCES.md": "e3cf925f1454448e0109d9cdb69652b34bf660fdec8d89ad55dd1e510297e04a",
    "middle.py": "62a6c825bd3fc05e87bfeaa93c9b7dc47c6c9e7d8f81f20d16162996280d4706",
    "radial.py": "c031213d07894d1029098caa293babd38e7cca655d1cfc728b6f3d91880c5ed2",
    "verify.py": "6520e0b8012514c2d428def37cbc2038bb3f47572837b5f746be5f2cfb596c9f",
}

D = 44
Q = 1 << D
RB = 20
RQ = 1 << RB
EP = D + RB + 1
BITS = 52
EXPQ = 1 << BITS
BINOMIAL_POWER = 38
WORK_BITS = 96
WORKQ = 1 << WORK_BITS
EPS = F(1, 1024)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def sqrt_bounds(x, bits=60):
    require(x >= 0, "negative square root")
    den = 1 << bits
    a = isqrt(x.numerator * den * den // x.denominator)
    lo = F(a, den)
    hi = lo if lo * lo == x else F(a + 1, den)
    require(lo * lo <= x <= hi * hi, "square-root enclosure failed")
    return lo, hi


def vectors():
    obj = loads((TARGET / "CELL.json").read_text())
    x = [tuple(F(a) for a in row) for row in obj["source_centers"]]
    y = [tuple(F(a) for a in row) for row in obj["target_centers"]]
    return obj, x, y


def norm2(x):
    return sum(a * a for a in x)


def dist2(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    result = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(result, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[result], a[pivot] = a[pivot], a[result]
        z = a[result][col]
        a[result] = [v / z for v in a[result]]
        for j in range(len(a)):
            if j != result and a[j][col]:
                z = a[j][col]
                a[j] = [u - z * v for u, v in zip(a[j], a[result])]
        result += 1
    return result


def geometry(x, y):
    losses = [dist2(x[i], x[j]) - dist2(y[i], y[j])
              for i, j in combinations(range(16), 2)]
    source_sep = min(dist2(x[i], x[j]) for i, j in combinations(range(16), 2))
    target_sep = min(dist2(y[i], y[j]) for i, j in combinations(range(16), 2))
    require(min(losses) == F(127, 2048), "reference loss mismatch")
    floor_loss = min(losses) - 4 * EPS * (2 * F(9, 4) + 2 * F(27, 16))
    require(floor_loss == F(1, 32), "cell contraction floor mismatch")
    rows = [tuple(a - b for a, b in zip(x[i] + y[i], x[0] + y[0]))
            for i in range(1, 16)]
    require(rank(rows) == 6, "paired-rank mismatch")
    symmetries = 0
    for perm in permutations(range(3)):
        for signs in product((-1, 1), repeat=3):
            if signs[0] * signs[1] * signs[2] != 1:
                continue
            for points in (x, y):
                transformed = Counter(tuple(signs[k] * p[perm[k]] for k in range(3))
                                      for p in points)
                require(transformed == Counter(points), "reference symmetry failed")
            symmetries += 1
    require(symmetries == 24, "symmetry count mismatch")
    undamped_y = [tuple(F(64, 63) * a for a in p) for p in y]
    midpoint_witnesses = 0
    for p in undamped_y:
        require(any(tuple((a + b) / 2 for a, b in zip(x[i], x[j])) == p
                    for i in range(16) for j in range(i, 16)),
                "target midpoint witness missing")
        midpoint_witnesses += 1
    return {
        "minimum_pair_loss": str(min(losses)),
        "cell_pair_loss_floor": str(floor_loss),
        "minimum_source_squared_separation": str(source_sep),
        "minimum_target_squared_separation": str(target_sep),
        "paired_rank": 6,
        "reference_symmetries": symmetries,
        "target_midpoint_witnesses": midpoint_witnesses,
    }


def power_down(value, squarings):
    """Floor-fixed-point value^(2^squarings), at denominator WORKQ."""
    for _ in range(squarings):
        value = value * value // WORKQ
    return value


def exp_neg_binomial(num, power):
    """Outward BITS-bit bounds for exp(-num/2^power), num >= 0."""
    require(num >= 0 and power >= 0, "invalid exponential input")
    if num == 0:
        return EXPQ, EXPQ
    k = BINOMIAL_POWER
    den = 1 << (power + k)
    require(num < den, "binomial base was not positive")
    scaled = num * WORKQ
    minus = WORKQ - ceil_fraction(F(scaled, den))
    plus = WORKQ + scaled // den
    require(0 < minus < WORKQ <= plus, "invalid binomial bases")
    lo_work = power_down(minus, k)
    denominator_lower = power_down(plus, k)
    require(denominator_lower > 0, "fixed-point denominator underflow")
    hi_work = (WORKQ * WORKQ + denominator_lower - 1) // denominator_lower
    scale = 1 << (WORK_BITS - BITS)
    lo = lo_work // scale
    hi = (hi_work + scale - 1) // scale
    require(0 <= lo <= hi <= EXPQ, "binomial exponential enclosure failed")
    return lo, hi


def exp_signed(num, power=EP):
    if num <= 0:
        return exp_neg_binomial(-num, power)
    lo, hi = exp_neg_binomial(num, power)
    require(lo > 0, "positive exponential reciprocal underflow")
    return EXPQ * EXPQ // hi, (EXPQ * EXPQ + lo - 1) // lo


def exp_neg_taylor(x):
    """Independent rational enclosure used only to test the binomial code."""
    require(x >= 0, "negative Taylor input")
    if x == 0:
        return F(1), F(1)
    total = term = F(1)
    n = 0
    while True:
        n += 1
        term *= x / n
        total += term
        next_term = term * x / (n + 1)
        ratio = x / (n + 2)
        if ratio < 1:
            exp_upper = total + next_term / (1 - ratio)
            lo, hi = 1 / exp_upper, 1 / total
            if hi - lo < F(1, 1 << (BITS + 8)):
                return lo, hi
        require(n < 1000, "Taylor control did not terminate")


def patches(n, x, y):
    answer = []
    sqrt_two = sqrt_bounds(F(2), 64)[1]
    for i in range(n):
        for j in range(i, n):
            u, v = F(2 * i + 1, 2 * n), F(2 * j + 1, 2 * n)
            inv_lo, inv_hi = sqrt_bounds(1 / (1 + u * u + v * v), 60)
            corner = 1 + F(i, n) ** 2 + F(j, n) ** 2
            direction_radius = sqrt_two / (2 * n) * sqrt_bounds(1 / corner, 60)[1]
            lower_corner = 1 + F(i + 1, n) ** 2 + F(j + 1, n) ** 2
            jl = sqrt_bounds(1 / lower_corner ** 3, 60)[0]
            ju = sqrt_bounds(1 / corner ** 3, 60)[1]
            area = F(1, n * n * (1 if i < j else 2))
            for parity in (1, -1):
                records = []
                for points, lower in ((x, True), (y, False)):
                    dots, norms = [], []
                    for p in points:
                        ns = norm2(p)
                        radius = sqrt_bounds(ns, 60)[1]
                        numerator = parity * p[0] * u + p[1] * v + p[2]
                        dc_lo = numerator * (inv_lo if numerator >= 0 else inv_hi)
                        dc_hi = numerator * (inv_hi if numerator >= 0 else inv_lo)
                        if lower:
                            d = dc_lo - radius * direction_radius - EPS
                            ns_bound = ns + 2 * radius * EPS + EPS * EPS
                            dots.append(floor(d * Q))
                            norms.append(ceil_fraction(ns_bound * Q))
                        else:
                            d = dc_hi + radius * direction_radius + EPS
                            ns_bound = ns - 2 * radius * EPS
                            dots.append(ceil_fraction(d * Q))
                            norms.append(floor(ns_bound * Q))
                    records.append((dots, norms))
                answer.append({"area": area, "jl": jl, "ju": ju,
                               "source": records[0], "target": records[1]})
    require(len(answer) == n * (n + 1), "angular patch count mismatch")
    return answer


def propose_root(s, record, lower):
    dots, norms = record
    ff = [(d / Q, q / (2 * Q)) for d, q in zip(dots, norms)]
    sf = float(s)
    left, right = max(2.25, sf - 5.0), sf + 4.0
    require(sum(exp(sf * sf / 2 - left * left / 2 + left * d - q)
                for d, q in ff) > 16, "proposal did not start inside")
    require(sum(exp(sf * sf / 2 - right * right / 2 + right * d - q)
                for d, q in ff) < 16, "proposal did not end outside")
    for _ in range(34):
        mid = (left + right) / 2
        value = sum(exp(sf * sf / 2 - mid * mid / 2 + mid * d - q)
                    for d, q in ff)
        if value > 16:
            left = mid
        else:
            right = mid
    return floor(left * RQ) - 32 if lower else ceil(right * RQ) + 32


def check_root(s, record, root, lower):
    require(root > F(9, 4) * RQ, "root outside monotone radial region")
    dots, norms = record
    scaled_threshold = s * s / 2 * (1 << EP)
    require(scaled_threshold.denominator == 1, "non-dyadic threshold")
    base = int(scaled_threshold) - root * root * (1 << (D - RB))
    total = 0
    widths = 0
    for dot, norm in zip(dots, norms):
        exponent = base + 2 * root * dot - norm * (1 << RB)
        lo, hi = exp_signed(exponent)
        total += lo if lower else hi
        widths += hi - lo
    slack = total - 16 * EXPQ if lower else 16 * EXPQ - total
    require(slack > 0, "independent radial bracket failed")
    return slack, widths


def radial_band(n, step, start, stop, x, y):
    ps = patches(n, x, y)
    windows = int((stop - start) / step)
    require(start + windows * step == stop, "radial band has a gap")
    previous = None
    minimum = None
    worst = None
    min_slack = None
    max_interval_width = 0
    roots = 0
    for k in range(windows + 1):
        s = start + k * step
        source, target = [], []
        for patch in ps:
            a = propose_root(s, patch["source"], True)
            b = propose_root(s, patch["target"], False)
            for record, root, lower in ((patch["source"], a, True),
                                        (patch["target"], b, False)):
                slack, width = check_root(s, record, root, lower)
                min_slack = slack if min_slack is None else min(min_slack, slack)
                max_interval_width = max(max_interval_width, width)
                roots += 1
            source.append(a)
            target.append(b)
        if previous is not None:
            total = F(0)
            for patch, a, b in zip(ps, previous, target):
                difference = F(a ** 3 - b ** 3, RQ ** 3)
                total += 8 * patch["area"] * difference * (
                    patch["jl"] if difference >= 0 else patch["ju"])
            require(total > F(1, 2), "independent signed volume bound failed")
            if minimum is None or total < minimum:
                minimum, worst = total, s - step
        previous = source
    return {
        "n": n,
        "start": str(start),
        "stop": str(stop),
        "step": str(step),
        "patches": len(ps),
        "windows": windows,
        "verified_roots": roots,
        "minimum_root_slack_units": min_slack,
        "maximum_summed_exp_interval_width_units": max_interval_width,
        "minimum_volume_lower": str(minimum),
        "worst_S": str(worst),
    }


def analytic_and_record_controls(x, y):
    expected = loads((TARGET / "EXPECTED.json").read_text())
    tail = expected["analytic_tail"]
    delta_record = F(tail["mean_support_lower"])
    error = F(tail["far_error_at_64"])
    require(delta_record > F(1, 4) and error < F(21, 100), "recorded far-tail margin failed")
    ps = patches(12, x, y)
    total = F(0)
    for patch in ps:
        gap = max(0, max(patch["source"][0]) - max(patch["target"][0]))
        total += patch["area"] * patch["jl"] * F(gap, Q)
    delta = F(21, 11) * total
    require(delta > F(1, 4), "independent mean-support bound failed")
    middle = expected["middle"]
    require(F(middle["cell_adverse_upper"]) < -F(1, 128), "middle margin failed")
    require(F(middle["source_peak_upper"]) < F(9, 32), "peak margin failed")
    require(F(49, 8) > 6 and F(1, 512) > 0, "threshold ordering failed")
    for band in expected["radial_bands"]:
        require(F(band["volume_lower"]) > F(1, 2), "recorded radial margin failed")
    return {
        "independent_mean_support_lower": str(delta),
        "recorded_mean_support_lower": str(delta_record),
        "far_error_at_64": str(error),
        "middle_adverse_upper": middle["cell_adverse_upper"],
        "source_peak_upper": middle["source_peak_upper"],
        "threshold_ranges": ["[0,1/512]", "[1/512,9/32]", "[9/32,infinity)"],
    }


def binomial_controls(x, y):
    controls = 0
    for power in (0, 3, 12, 40, 65):
        for num in (0, 1, 2, 7, 31, 127):
            lo, hi = exp_neg_binomial(num, power)
            require(0 <= lo <= hi <= EXPQ, "exponential control failed")
            tl, th = exp_neg_taylor(F(num, 1 << power))
            require(F(lo, EXPQ) <= th and tl <= F(hi, EXPQ),
                    "binomial and Taylor enclosures are disjoint")
            controls += 1
    # Mutation control: reversing an outward endpoint must be detected.
    lo, hi = exp_neg_binomial(1, 0)
    try:
        require(hi < lo, "deliberate reversed interval")
    except ValueError:
        rejected = 1
    else:
        raise ValueError("reversed interval mutation passed")
    patch = patches(12, x, y)[0]
    for record, lower, direction in ((patch["source"], True, 1),
                                     (patch["target"], False, -1)):
        root = propose_root(F(6), record, lower) + direction * RQ // 4
        try:
            check_root(F(6), record, root, lower)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("corrupted radial endpoint passed")
    return controls, rejected


def main():
    for name, digest in PINS.items():
        require(sha256((TARGET / name).read_bytes()).hexdigest() == digest,
                "target pin mismatch: " + name)
    obj, x, y = vectors()
    require(obj["coordinate_parameters"] == 96 and
            obj["anchored_coordinate_parameters"] == 90,
            "cell dimension mismatch")
    controls, rejected = binomial_controls(x, y)
    result = {
        "status": "DEEP_FLAP_CELL_INDEPENDENT_ACCEPT",
        "source_pins": len(PINS),
        "geometry": geometry(x, y),
        "binomial_exponential_controls": controls,
        "intentional_rejections": rejected,
        "analytic_and_record_controls": analytic_and_record_controls(x, y),
        "radial_bands": [
            radial_band(24, F(1, 16), F(7, 2), F(6), x, y),
            radial_band(12, F(1, 8), F(6), F(64), x, y),
        ],
    }
    require(result == loads((HERE / "EXPECTED.json").read_text()),
            "independent expected record mismatch")
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
