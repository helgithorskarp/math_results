#!/usr/bin/env python3
"""Independent exact checks for the direct Gaussian-hinge quadrature oracle.

This checker imports no author module.  Its exponential enclosure uses the
reciprocal of a positive Taylor sum with a geometric remainder, and its
piecewise-linear maximum uses suffix sums rather than the author's sweep.
All arithmetic relevant to certification is integer or Fraction arithmetic.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache, reduce
from hashlib import sha256
from itertools import product
import json
from math import isqrt, lcm
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_prior_localization"
PINNED = {
    "DIRECT_HINGE.md": "b6abfa8a14481aa834869403f80c424c7d9f62b75a62e5db6890d1278c4867ea",
    "direct_hinge.py": "94e9ee5f643a6d98bf18983eda3a13f5b8513f2f6e06753ad133ad046d2e5bb9",
    "DIRECT_EXPECTED.json": "59719bb341bf695d8b7a43a64d95cb80e298e7a3564a9296016b2f8682b1c75a",
    "DIRECT_FIXTURES.json": "85fd2fd4ba63434f5ad0612b34fab148b166bde63641a0543aa457d4a87b6d70",
    "DIRECT_INPUTS.json": "fee6da66e87dcbd379e40da9c6288254c8b54e5b1805e118829343097303ca68",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest_bytes(path):
    return sha256(path.read_bytes()).hexdigest()


def digest_json(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(data).hexdigest()


def ceilq(x):
    return -((-x.numerator) // x.denominator)


def rat(x):
    require(isinstance(x, (int, str)) and not isinstance(x, bool),
            "rational must be an integer or string")
    return Q(x)


@lru_cache(maxsize=10000)
def reciprocal_taylor_exp(q, bits):
    """Enclose exp(-q) by dyadic integers, via bounds on positive exp(q)."""
    require(isinstance(q, Q) and q >= 0 and bits >= 16,
            "bad exponential request")
    scale = 1 << bits
    if q == 0:
        return scale, scale
    term = total = Q(1)
    n = 0
    while True:
        n += 1
        term *= q / n
        total += term
        # The remaining positive tail begins with term_(n+1).  Every later
        # ratio is at most q/(n+2), so this is a rigorous geometric majorant.
        if Q(n + 2) > q:
            nxt = term * q / (n + 1)
            ratio = q / (n + 2)
            exp_low = total
            exp_high = total + nxt / (1 - ratio)
            lo = (Q(scale) / exp_high).__floor__()
            hi = ceilq(Q(scale) / exp_low)
            if hi - lo <= 2:
                require(Q(lo, scale) <= 1 / exp_high <= 1 / exp_low <= Q(hi, scale),
                        "reciprocal exponential enclosure failed")
                return lo, hi


def atan_alternating(x, bits):
    """Exact alternating-series enclosure for atan(x), 0 <= x <= 1/2."""
    require(0 <= x <= Q(1, 2), "atan input outside review range")
    total, power, n = Q(0), x, 0
    while True:
        total += power / (2 * n + 1)
        following = -power * x * x
        remainder = following / (2 * n + 3)
        if abs(remainder) < Q(1, 1 << bits):
            return min(total, total + remainder), max(total, total + remainder)
        power, n = following, n + 1


def sqrt_dyadic(x, bits):
    require(x >= 0, "negative square root")
    scale = 1 << bits
    floor_scaled_square = x.numerator * scale * scale // x.denominator
    a = isqrt(floor_scaled_square)
    lo = Q(a, scale)
    hi = lo if lo * lo == x else Q(a + 1, scale)
    require(lo * lo <= x <= hi * hi, "sqrt enclosure failed")
    return lo, hi


@lru_cache(maxsize=20)
def gaussian_constant(bits):
    """Bound (2*pi)^(-3/2) using pi/4=atan(1/2)+atan(1/3)."""
    a0, a1 = atan_alternating(Q(1, 2), bits + 24)
    b0, b1 = atan_alternating(Q(1, 3), bits + 24)
    pi_lo, pi_hi = 4 * (a0 + b0), 4 * (a1 + b1)
    require(Q(3) < pi_lo < pi_hi < Q(22, 7), "independent pi interval")
    c_lo = sqrt_dyadic(1 / (2 * pi_hi) ** 3, bits + 12)[0]
    c_hi = sqrt_dyadic(1 / (2 * pi_lo) ** 3, bits + 12)[1]
    require(Q(1, 16) < c_lo <= c_hi < Q(1, 8), "Gaussian constant range")
    require(c_hi - c_lo <= Q(1, 1 << (bits + 8)),
            "Gaussian constant interval too wide")
    return c_lo, c_hi


def parse_instance(obj, require_contraction):
    xs = [tuple(rat(a) for a in row) for row in obj["source"]]
    ys = [tuple(rat(a) for a in row) for row in obj["target"]]
    ws = [rat(w) for w in obj["weights"]]
    require(len(xs) == len(ys) == len(ws) > 0, "inconsistent labels")
    require(all(len(v) == 3 for v in xs + ys), "not three dimensional")
    require(all(w >= 0 for w in ws) and sum(ws) == 1, "not a probability")
    losses = []
    for i in range(len(xs)):
        for j in range(i):
            source = sum((a - b) ** 2 for a, b in zip(xs[i], xs[j]))
            target = sum((a - b) ** 2 for a, b in zip(ys[i], ys[j]))
            losses.append(source - target)
    contracted = all(v >= 0 for v in losses)
    require(contracted or not require_contraction, "noncontraction rejected")
    # Translate the two laws independently, as allowed by the hinge profile.
    xs = [tuple(a - b for a, b in zip(x, xs[0])) for x in xs]
    ys = [tuple(a - b for a, b in zip(y, ys[0])) for y in ys]
    denominator = reduce(lcm, (w.denominator for w in ws), 1)
    xgroups, ygroups = Counter(), Counter()
    for x, y, w in zip(xs, ys, ws):
        mass = int(w * denominator)
        if mass:
            xgroups[x] += mass
            ygroups[y] += mass
    radius = max(abs(a) for v in list(xgroups) + list(ygroups) for a in v)
    return xgroups, ygroups, denominator, radius, contracted, losses


def density_histograms(groups, denominator, h, half_grid, bits):
    """Rebuild all normalized-density intervals with an independent exp bound."""
    scale = 1 << bits
    coords = [h * j for j in range(-half_grid, half_grid + 1)]
    tables = {}
    for center in groups:
        for a in center:
            tables.setdefault(a, [reciprocal_taylor_exp((z - a) ** 2 / 2, bits)
                                  for z in coords])
    atoms = [(mass, *(tables[a] for a in center))
             for center, mass in groups.items()]
    low_hist, high_hist = Counter(), Counter()
    max_width = 0
    divisor = denominator * scale * scale
    size = len(coords)
    for i in range(size):
        for j in range(size):
            for k in range(size):
                low = sum(m * tx[i][0] * ty[j][0] * tz[k][0]
                          for m, tx, ty, tz in atoms)
                high = sum(m * tx[i][1] * ty[j][1] * tz[k][1]
                           for m, tx, ty, tz in atoms)
                lo = low // divisor
                hi = min(scale, (high + divisor - 1) // divisor)
                require(0 <= lo <= hi <= scale, "density interval invalid")
                max_width = max(max_width, hi - lo)
                low_hist[lo] += 1
                high_hist[hi] += 1
    require(sum(low_hist.values()) == sum(high_hist.values()) == size ** 3,
            "lattice coverage incomplete")
    return low_hist, high_hist, max_width


def profile_max_suffix(source, target):
    """Exact all-knot maximum from active suffix counts and sums."""
    require(sum(source.values()) == sum(target.values()), "grid counts differ")
    knots = sorted({0, *source, *target})
    source_sum = sum(v * n for v, n in source.items())
    target_sum = sum(v * n for v, n in target.items())
    source_count = sum(source.values())
    target_count = sum(target.values())
    best, arg = None, None
    for t in knots:
        value = source_sum - t * source_count - target_sum + t * target_count
        if best is None or value > best:
            best, arg = value, t
        ns, nt = source.get(t, 0), target.get(t, 0)
        source_sum -= t * ns
        target_sum -= t * nt
        source_count -= ns
        target_count -= nt
    require(best is not None and best >= 0, "profile maximum missing")
    return best, arg


def independent_error(h, tail_radius, bits):
    growth = 1 + h * h / 8
    quadrature = h * h * (1 + growth + growth * growth) / 4
    q = tail_radius * tail_radius / 2
    elo, ehi = reciprocal_taylor_exp(q, bits + 16)
    del elo
    tail = 3 * growth * growth * Q(ehi, 1 << (bits + 16)) / tail_radius
    return quadrature, tail


def enclose(obj, h, requested_tail, bits, require_contraction):
    xg, yg, denominator, radius, contracted, losses = parse_instance(
        obj, require_contraction)
    half_grid = ceilq((radius + requested_tail) / h)
    actual_tail = half_grid * h - radius
    xl, xu, xwidth = density_histograms(xg, denominator, h, half_grid, bits)
    yl, yu, ywidth = density_histograms(yg, denominator, h, half_grid, bits)
    low_num, low_arg = profile_max_suffix(xl, yu)
    high_num, high_arg = profile_max_suffix(xu, yl)
    c_lo, c_hi = gaussian_constant(bits)
    factor = h ** 3 / (1 << bits)
    discrete_low = c_lo * factor * low_num
    discrete_high = c_hi * factor * high_num
    quadrature, tail = independent_error(h, actual_tail, bits)
    error = quadrature + tail
    lower = max(Q(0), discrete_low - error)
    upper = min(Q(1), discrete_high + error)
    require(lower <= upper and discrete_low <= discrete_high,
            "defect interval reversed")
    return {
        "contraction": contracted,
        "minimum_pair_loss": str(min(losses)) if losses else "0",
        "step": str(h),
        "tail_radius": str(actual_tail),
        "bits": bits,
        "half_grid": half_grid,
        "lattice_sites_per_endpoint": (2 * half_grid + 1) ** 3,
        "lower": str(lower),
        "upper": str(upper),
        "lattice_defect_interval": [str(discrete_low), str(discrete_high)],
        "quadrature_pair_error": str(quadrature),
        "tail_error": str(tail),
        "max_density_width_units": [xwidth, ywidth],
        "maximizing_threshold_units": [low_arg, high_arg],
    }


def matrix_rank(rows):
    rows = [list(map(Q, row)) for row in rows]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        value = rows[rank][column]
        rows[rank] = [x / value for x in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][column]:
                value = rows[i][column]
                rows[i] = [x - value * y for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank


def ceil_log2(x):
    p = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while Q(1 << p) < x:
        p += 1
    while p and Q(1 << (p - 1)) >= x:
        p -= 1
    return p


def budget(k):
    root = isqrt(k)
    root += root * root < k
    ell = (k - 1).bit_length()
    troot = isqrt(ell + 2)
    troot += troot * troot < ell + 2
    h, tail = Q(1, 4 * root), 2 * troot
    half_grid = ceilq((3 * k + tail) / h)
    volume = ((2 * half_grid + 1) * h) ** 3
    bits = max(16, ceil_log2(100 * k * (2 * volume + 1)))
    return {"k": k, "step": str(h), "tail_radius": tail,
            "half_grid": half_grid,
            "lattice_sites_per_endpoint": (2 * half_grid + 1) ** 3,
            "bits": bits, "interval_width_upper": str(Q(21, 100 * k)),
            "localization_rounding_error": str(Q(865, 256 * k))}


def direct_profile_controls():
    count = 0
    for source in product(range(3), repeat=3):
        for target in product(range(3), repeat=3):
            a, arg = profile_max_suffix(Counter(source), Counter(target))
            direct = {t: sum(max(x - t, 0) for x in source)
                      - sum(max(x - t, 0) for x in target)
                      for t in {0, *source, *target}}
            require(a == max(direct.values()) and direct[arg] == a,
                    "suffix profile differs from definition")
            count += 1
    return count


def frontier_fixture_controls(obj):
    """Independently verify that the positive control lies in R^c_1."""
    k, atom_bound, coordinate_denominator, weight_denominator = 1, 39, 256, 156
    xs = [tuple(rat(a) for a in row) for row in obj["source"]]
    ys = [tuple(rat(a) for a in row) for row in obj["target"]]
    ws = [rat(w) for w in obj["weights"]]
    require(len(xs) <= atom_bound and xs[0] == ys[0] == (0, 0, 0),
            "frontier label or anchor condition failed")
    xints = [tuple(int(a * coordinate_denominator) for a in row) for row in xs]
    yints = [tuple(int(a * coordinate_denominator) for a in row) for row in ys]
    require(all(Q(a, coordinate_denominator) == b
                for integer, rational in zip(xints + yints, xs + ys)
                for a, b in zip(integer, rational)), "frontier coordinate lattice failed")
    masses = [int(w * weight_denominator) for w in ws]
    require(all(Q(a, weight_denominator) == b for a, b in zip(masses, ws))
            and all(a >= 0 for a in masses) and sum(masses) == weight_denominator,
            "frontier weight lattice failed")
    radius_squared = max(sum(a * a for a in row) for row in xints + yints)
    require(radius_squared <= (3 * k * coordinate_denominator) ** 2,
            "frontier radius failed")
    losses = []
    for i in range(len(xints)):
        for j in range(i):
            source = sum((a - b) ** 2 for a, b in zip(xints[i], xints[j]))
            target = sum((a - b) ** 2 for a, b in zip(yints[i], yints[j]))
            losses.append(source - target)
    require(min(losses) >= 256 * k * k, "frontier integer margin failed")
    paired_rank = matrix_rank([x + y for x, y in zip(xs, ys)])
    require(paired_rank == 6, "frontier control lacks paired rank six")
    return {
        "k": k,
        "atom_bound": atom_bound,
        "labels": len(xs),
        "coordinate_denominator": coordinate_denominator,
        "weight_denominator": weight_denominator,
        "integer_masses": masses,
        "maximum_integer_radius_squared": radius_squared,
        "minimum_integer_pair_loss": min(losses),
        "paired_rank": paired_rank,
    }


def run():
    for name, expected in PINNED.items():
        require(digest_bytes(TARGET / name) == expected, "changed target: " + name)
    fixtures = json.loads((TARGET / "DIRECT_FIXTURES.json").read_text())
    author = json.loads((TARGET / "DIRECT_EXPECTED.json").read_text())
    author_rows = {(item["name"], row["step"]): row
                   for item in author["fixtures"] for row in item["rows"]}

    growth = Q(129, 128)
    require((1 + growth + growth * growth) / 64 < Q(1, 20),
            "uniform quadrature coefficient")
    require(3 * growth * growth / 64 < Q(1, 20),
            "uniform tail coefficient")
    require(Q(865, 256) + Q(21, 100) == Q(22969, 6400),
            "global interval coefficient")
    require(Q(1, 2) + Q(865, 2048) == Q(1889, 2048),
            "epsilon consequence coefficient")

    reports = []
    frontier_control = None
    for item in fixtures:
        obj = item["instance"]
        if item["name"] == "rational_frontier_full_rank_control":
            frontier_control = frontier_fixture_controls(obj)
        rows = []
        for step in item["steps"]:
            row = enclose(obj, rat(step), rat(item["tail"]), item["bits"],
                          item["require_contraction"])
            other = author_rows[(item["name"], step)]
            a0, a1 = map(Q, row["lattice_defect_interval"])
            b0, b1 = map(Q, other["lattice_defect_interval"])
            require(max(a0, b0) <= min(a1, b1),
                    "independent and author lattice intervals are disjoint")
            row["author_lattice_interval_overlap"] = True
            rows.append(row)
        if item["name"] == "rational_frontier_full_rank_control":
            require(all(Q(rows[i + 1]["upper"]) < Q(rows[i]["upper"])
                        for i in range(len(rows) - 1)), "upper bounds not decreasing")
            require(Q(rows[-1]["upper"]) < Q(3, 250), "fine upper bound not below .012")
        else:
            require(not rows[-1]["contraction"], "negative control became contraction")
            require(Q(rows[-1]["lower"]) > Q(4, 25), "adverse lower bound not above .16")
            try:
                parse_instance(obj, True)
            except RuntimeError as error:
                require(str(error) == "noncontraction rejected", "wrong rejection")
            else:
                raise RuntimeError("noncontraction accepted without override")
        reports.append({"name": item["name"], "rows": rows})

    samples = [1, 2, 7, 16, 64, 1024, 1000000]
    schedules = [budget(k) for k in samples]
    require(schedules == author["controls"]["budgets"], "budget schedules differ")
    result = {
        "status": "INDEPENDENT_DIRECT_HINGE_REVIEW_PASS",
        "method": "reciprocal positive Taylor remainder and suffix-sum profile maxima",
        "target_source_commit": "2e0d74152db80935259c25142da0e42d37ff0399",
        "pinned_files": PINNED,
        "analytic_constants": {
            "quadrature_schedule_strict": True,
            "tail_schedule_strict": True,
            "global_width_coefficient": "22969/6400",
            "epsilon_coefficient": "1889/2048",
        },
        "profile_definition_controls": direct_profile_controls(),
        "frontier_fixture_control": frontier_control,
        "budget_schedules": schedules,
        "fixtures": reports,
    }
    return result


if __name__ == "__main__":
    require(sys.argv[1:] in ([], ["--json"]), "usage: independent_check.py [--json]")
    report = run()
    expected_path = HERE / "EXPECTED.json"
    summary = {
        "status": report["status"],
        "record_sha256": digest_json(report),
        "fixture_rows": sum(len(x["rows"]) for x in report["fixtures"]),
    }
    if expected_path.exists():
        require(summary == json.loads(expected_path.read_text()), "expected record mismatch")
    if sys.argv[1:] == ["--json"]:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(summary["status"])
        print("record_sha256", summary["record_sha256"])
        print("fixture_rows", summary["fixture_rows"])
