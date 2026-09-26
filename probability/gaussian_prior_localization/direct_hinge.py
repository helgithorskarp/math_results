#!/usr/bin/env python3
"""Exact interval quadrature of the whole Gaussian hinge profile in R^3.

Standard-library CPython 3.11+. See DIRECT_HINGE.md for the analytic error.
No floating arithmetic, sampled thresholds, or moment expansion is used.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import isqrt, lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rat(x):
    need(isinstance(x, (int, str)) and not isinstance(x, bool),
         "rational inputs must be integers or strings")
    return F(x)


def ceilq(x):
    return -((-x.numerator) // x.denominator)


def ceil_log2(x):
    need(x > 0, "positive logarithm input required")
    p = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while F(1 << p) < x:
        p += 1
    while p and F(1 << (p - 1)) >= x:
        p -= 1
    return p


@lru_cache(maxsize=100000)
def exp_neg(q, bits):
    """Enclose exp(-q) by integers divided by 2**bits; width <=2 units."""
    need(q >= 0 and isinstance(bits, int) and bits >= 8,
         "invalid exponential request")
    Q = 1 << bits
    if not q:
        return Q, Q
    r, squarings = q, 0
    while r > F(1, 8):
        r /= 2
        squarings += 1
    work = bits + 2 * squarings + 16
    S = 1 << work
    total, term, n = F(1), F(1), 0
    while True:
        # Even partial sum is upper; the following odd sum is lower.
        nxt = -term * r / (n + 1)
        if n % 2 == 0 and abs(nxt) <= F(1, 16 * S):
            low, high = total + nxt, total
            break
        total += nxt
        term = nxt
        n += 1
    lo, hi = (low * S).__floor__(), ceilq(high * S)
    for _ in range(squarings):
        lo = lo * lo // S
        hi = min(S, (hi * hi + S - 1) // S)
    shift = 1 << (work - bits)
    lo, hi = lo // shift, min(Q, (hi + shift - 1) // shift)
    need(0 <= lo <= hi <= Q and hi - lo <= 2,
         "exponential enclosure width invariant failed")
    return lo, hi


def atan_bounds(x, bits):
    total, term, n = F(0), x, 0
    while True:
        total += term / (2 * n + 1)
        next_term = -term * x * x
        rem = next_term / (2 * n + 3)
        if abs(rem) < F(1, 1 << bits):
            return min(total, total + rem), max(total, total + rem)
        term, n = next_term, n + 1


def sqrt_bounds(x, bits):
    need(x >= 0, "negative square root")
    Q = 1 << bits
    a = isqrt(x.numerator * Q * Q // x.denominator)
    lo = F(a, Q)
    hi = lo if lo * lo == x else F(a + 1, Q)
    need(lo * lo <= x <= hi * hi, "square-root enclosure failure")
    return lo, hi


@lru_cache(maxsize=100)
def gaussian_constant(bits):
    """Enclose C=(2*pi)^(-3/2) with rational Machin/square-root bounds."""
    a, b = atan_bounds(F(1, 5), bits + 20)
    c, d = atan_bounds(F(1, 239), bits + 20)
    plo, phi = 16 * a - 4 * d, 16 * b - 4 * c
    need(F(3) < plo <= phi < F(22, 7), "Machin pi bounds failed")
    low = sqrt_bounds(1 / (2 * phi) ** 3, bits + 10)[0]
    high = sqrt_bounds(1 / (2 * plo) ** 3, bits + 10)[1]
    need(F(1, 16) < low <= high < F(1, 8), "Gaussian constant bounds")
    need(high - low <= F(1, 1 << (bits + 8)), "constant width")
    return low, high


def read_instance(obj, require_contraction=True):
    need(isinstance(obj, dict), "instance must be an object")
    need("variance" not in obj or rat(obj["variance"]) == 1,
         "this executable requires variance one; rescale first")
    xs = [tuple(rat(v) for v in row) for row in obj["source"]]
    ys = [tuple(rat(v) for v in row) for row in obj["target"]]
    ws = [rat(w) for w in obj["weights"]]
    need(len(xs) == len(ys) == len(ws) > 0, "inconsistent labels")
    need(all(len(v) == 3 for v in xs + ys), "dimension must be three")
    need(all(w >= 0 for w in ws) and sum(ws) == 1, "probability weights")
    pairs = []
    for i in range(len(xs)):
        for j in range(i):
            loss = sum((a - b) ** 2 for a, b in zip(xs[i], xs[j]))
            loss -= sum((a - b) ** 2 for a, b in zip(ys[i], ys[j]))
            pairs.append(loss)
    contracted = all(loss >= 0 for loss in pairs)
    need(not require_contraction or contracted, "input is not a contraction")
    # Separate translations preserve the exact continuous hinge profiles.
    xs = [tuple(a - b for a, b in zip(v, xs[0])) for v in xs]
    ys = [tuple(a - b for a, b in zip(v, ys[0])) for v in ys]
    W = lcm(*(w.denominator for w in ws))
    masses = [int(w * W) for w in ws]
    xgroups, ygroups = Counter(), Counter()
    for x, y, w in zip(xs, ys, masses):
        if w:
            xgroups[x] += w
            ygroups[y] += w
    R = max(abs(a) for v in list(xgroups) + list(ygroups) for a in v)
    return xgroups, ygroups, W, R, contracted


def density_histograms(groups, W, h, M, bits):
    """Interval values of p/C on every lattice site in [-Mh,Mh]^3."""
    Q = 1 << bits
    size = 2 * M + 1
    coords = [h * j for j in range(-M, M + 1)]
    tables = {}
    for v in groups:
        for a in v:
            if a not in tables:
                tables[a] = [exp_neg((z - a) ** 2 / 2, bits) for z in coords]
    atoms = [(mass, *(tables[a] for a in v)) for v, mass in groups.items()]
    low_hist, high_hist = Counter(), Counter()
    divisor = W * Q * Q
    width_sum, max_width = 0, 0
    stream = sha256()
    for i in range(size):
        for j in range(size):
            factors = [(mass * tx[i][0] * ty[j][0],
                        mass * tx[i][1] * ty[j][1], tz)
                       for mass, tx, ty, tz in atoms]
            for k in range(size):
                a = sum(lo * tz[k][0] for lo, hi, tz in factors)
                b = sum(hi * tz[k][1] for lo, hi, tz in factors)
                lo = a // divisor
                hi = min(Q, (b + divisor - 1) // divisor)
                need(0 <= lo <= hi <= Q and hi - lo <= 8,
                     "mixture value interval invariant failed")
                low_hist[lo] += 1
                high_hist[hi] += 1
                width_sum += hi - lo
                max_width = max(max_width, hi - lo)
                stream.update(f"{lo},{hi}\n".encode())
    need(sum(low_hist.values()) == sum(high_hist.values()) == size ** 3,
         "lattice coverage failed")
    return low_hist, high_hist, width_sum, max_width, stream.hexdigest()


def profile_max(source, target):
    """Exact max_t sum(a-t)_+ - sum(b-t)_+ at ALL knots, including zero."""
    need(all(isinstance(a, int) and a >= 0 and n > 0
             for hist in (source, target) for a, n in hist.items()),
         "invalid histogram")
    need(sum(source.values()) == sum(target.values()), "unequal grid counts")
    value = sum(a * n for a, n in source.items()) - sum(a * n for a, n in target.items())
    best, arg = value, 0
    slope, prev = 0, 0
    for knot in sorted(source.keys() | target.keys()):
        value += slope * (knot - prev)
        if value > best:
            best, arg = value, knot
        slope += source.get(knot, 0) - target.get(knot, 0)
        prev = knot
    need(value == 0 and slope == 0, "profile sweep endpoint failure")
    return best, arg


def matrix_rank(rows):
    rows = [list(map(F, row)) for row in rows]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((j for j in range(rank, len(rows)) if rows[j][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        v = rows[rank][col]
        rows[rank] = [a / v for a in rows[rank]]
        for j in range(rank + 1, len(rows)):
            v = rows[j][col]
            rows[j] = [a - v * b for a, b in zip(rows[j], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def quadrature_error(h, T, bits=48):
    need(h > 0 and T > 0, "positive step and tail radius required")
    G = 1 + h * h / 8
    two_endpoint = h * h * (1 + G + G * G) / 4
    q = T * T / 2
    ehi = min(F(exp_neg(q, bits)[1], 1 << bits), F(1, 1 << (q.__floor__())))
    tail = 3 * G * G * ehi / T
    return two_endpoint, tail


def enclose(obj, h, tail_radius, bits=40, require_contraction=True):
    xg, yg, W, R, contracted = read_instance(obj, require_contraction)
    need(h > 0 and tail_radius >= 1 and isinstance(bits, int) and bits >= 16,
         "invalid grid parameters")
    M = ceilq((R + tail_radius) / h)
    T = M * h - R
    xl, xu, xwidth, xmaxw, xhash = density_histograms(xg, W, h, M, bits)
    yl, yu, ywidth, ymaxw, yhash = density_histograms(yg, W, h, M, bits)
    low_num, low_arg = profile_max(xl, yu)
    high_num, high_arg = profile_max(xu, yl)
    cl, cu = gaussian_constant(bits)
    scale = h ** 3 / (1 << bits)
    qlow, qhigh = cl * scale * low_num, cu * scale * high_num
    quad, tail = quadrature_error(h, T, bits + 10)
    error = quad + tail
    lower, upper = max(F(0), qlow - error), min(F(1), qhigh + error)
    need(lower <= upper and qlow <= qhigh, "reversed defect enclosure")
    eval_width = qhigh - qlow
    need(eval_width <= cu * scale * (xwidth + ywidth)
         + (cu - cl) * scale * low_num, "interval profile width failed")
    mass_intervals = []
    for lh, uh in [(xl, xu), (yl, yu)]:
        ml = cl * scale * sum(a * n for a, n in lh.items())
        mu = cu * scale * sum(a * n for a, n in uh.items())
        need(ml - quad / 2 <= 1 <= mu + quad / 2 + tail,
             "grid mass conflicts with the independent unit-mass value")
        mass_intervals.append([str(ml), str(mu)])
    return {
        "contraction": contracted, "variance": 1,
        "source_groups": len(xg), "target_groups": len(yg),
        "step": str(h), "tail_radius": str(T), "bits": bits,
        "half_grid": M, "lattice_sites_per_endpoint": (2 * M + 1) ** 3,
        "lower": str(lower), "upper": str(upper),
        "quadrature_pair_error": str(quad), "tail_error": str(tail),
        "lattice_defect_interval": [str(qlow), str(qhigh)],
        "maximizing_lower_threshold_over_C": str(F(low_arg, 1 << bits)),
        "maximizing_upper_threshold_over_C": str(F(high_arg, 1 << bits)),
        "fixed_point_profile_maxima": [low_num, high_num],
        "density_interval_width_sums": [xwidth, ywidth],
        "finite_lattice_mass_intervals": mass_intervals,
        "max_density_interval_width_units": [xmaxw, ymaxw],
        "value_stream_sha256": [xhash, yhash],
    }


def frontier_budget(k):
    need(isinstance(k, int) and not isinstance(k, bool) and k >= 1,
         "positive integer k required")
    root = isqrt(k)
    if root * root < k:
        root += 1
    ell = (k - 1).bit_length()
    troot = isqrt(ell + 2)
    if troot * troot < ell + 2:
        troot += 1
    h, T = F(1, 4 * root), 2 * troot
    M = ceilq((3 * k + T) / h)
    V = (2 * M * h + h) ** 3
    bits = max(16, ceil_log2(100 * k * (2 * V + 1)))
    return {"k": k, "step": str(h), "tail_radius": T,
            "half_grid": M, "lattice_sites_per_endpoint": (2 * M + 1) ** 3,
            "bits": bits, "interval_width_upper": str(F(21, 100 * k)),
            "localization_rounding_error": str(F(865, 256 * k))}


def gaussian_hinge_controls():
    """A separate radial integral checks actual Gaussian hinges at three levels."""
    h, M, bits = F(1, 2), 10, 40
    lo, hi, *_ = density_histograms(Counter({(F(0),) * 3: 1}), 1, h, M, bits)
    cl, cu = gaussian_constant(bits)
    a, b = atan_bounds(F(1, 5), 70)
    c, d = atan_bounds(F(1, 239), 70)
    pl, pu = 16 * a - 4 * d, 16 * b - 4 * c
    invroot_l = sqrt_bounds(1 / pu, 64)[0]
    invroot_u = sqrt_bounds(1 / pl, 64)[1]
    rows = []
    for t in [F(1, 4), F(1), F(4)]:
        term, etotal, ftotal = F(1), F(1), F(1, 3)
        for n in range(1, 61):
            term *= -t / n
            etotal += term
            ftotal += term / (2 * n + 3)
        nextterm = -term * t / 61
        el, eu = etotal + nextterm, etotal
        fl, fu = ftotal + nextterm / 125, ftotal
        bracket_l, bracket_u = fl - eu / 3, fu - el / 3
        need(0 < bracket_l <= bracket_u, "radial hinge bracket")
        tl, tu = sqrt_bounds(t, 64)
        analytic_l = 4 * t * tl * invroot_l * bracket_l
        analytic_u = 4 * t * tu * invroot_u * bracket_u
        lattice_l = cl * h ** 3 * sum(n * max(F(v, 1 << bits) - eu, 0)
                                       for v, n in lo.items())
        lattice_u = cu * h ** 3 * sum(n * max(F(v, 1 << bits) - el, 0)
                                       for v, n in hi.items())
        err = max(abs(analytic_l - lattice_u), abs(analytic_u - lattice_l))
        quad, tail = quadrature_error(h, M * h, bits)
        need(err <= quad / 2 + tail and err < F(1, 100),
             "Gaussian hinge disagrees with independent radial integral")
        rows.append({"t": str(t), "certified_error_below": "1/100"})
    return rows


def controls():
    # Independent definition-level profile maxima, rather than another sweep.
    cases = 0
    lists = list(product(range(4), repeat=3))
    for a in lists:
        for b in lists:
            got, arg = profile_max(Counter(a), Counter(b))
            knots = {0, *a, *b}
            vals = {t: sum(max(x - t, 0) for x in a)
                    - sum(max(x - t, 0) for x in b) for t in knots}
            need(got == max(vals.values()) and vals[arg] == got,
                 "profile sweep differs from definition")
            cases += 1
    # Two valid implementations: reduced fixed point vs direct alternating sums.
    ecases = 0
    for q in [F(i, 8) for i in range(65)] + [F(100), F(10000)]:
        lo, hi = exp_neg(q, 32)
        if q <= 8:
            term, total = F(1), F(1)
            for n in range(1, 101):
                term *= -q / n
                total += term
            next_total = total + term * (-q) / 101
            need(F(lo, 1 << 32) <= next_total <= total <= F(hi, 1 << 32),
                 "exponential disagrees with independent Taylor enclosure")
        ecases += 1
    need(exp_neg(F(0), 32) == (1 << 32, 1 << 32), "exp zero")
    # Translation, permutation, zero-weight and collision normalization.
    base = {"source": [[0, 0, 0], [1, 0, 0]],
            "target": [[0, 0, 0], ["1/2", 0, 0]], "weights": ["1/2", "1/2"]}
    expanded = {"source": [[2, 3, 4], [3, 3, 4], [99, 0, 0]],
                "target": [[-2, 1, 0], ["-3/2", 1, 0], [0, 0, 0]],
                "weights": ["1/2", "1/2", 0]}
    a = read_instance(base)
    # Zero labels can violate irrelevant distances; the public parser deliberately
    # validates all declared labels, so remove them for this normalization check.
    expanded["source"].pop(); expanded["target"].pop(); expanded["weights"].pop()
    b = read_instance(expanded)
    need(a == b, "separate-translation invariance failed")
    # A split atom and a zero-mass duplicate have the same normalized law.
    split = {"source": [[0, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 0]],
             "target": [[0, 0, 0], ["1/2", 0, 0], ["1/2", 0, 0], [0, 0, 0]],
             "weights": ["1/2", "1/4", "1/4", 0]}
    xg, yg, W, R, contracted = read_instance(split)
    need({x: F(w, W) for x, w in xg.items()} == {x: F(w, a[2]) for x, w in a[0].items()}
         and {x: F(w, W) for x, w in yg.items()} == {x: F(w, a[2]) for x, w in a[1].items()},
         "split-atom normalization failed")
    peano = 0
    for d in range(2, 12):
        direct = F(1, 2) - F(1, d + 1)
        kernel = F(d * (d - 1), 2) * (F(1, d) - F(1, d + 1))
        need(direct == kernel, "polynomial Peano identity")
        peano += 1
    for i in range(33):
        a0 = F(i, 32)
        direct = (1 - a0) / 2 - (1 - a0) ** 2 / 2
        need(direct == a0 * (1 - a0) / 2 <= F(1, 8), "hinge Peano identity")
        peano += 1
    rejected = 0
    invalid = [lambda: exp_neg(F(-1), 32), lambda: exp_neg(F(1), 2),
               lambda: frontier_budget(0), lambda: frontier_budget(True),
               lambda: rat(0.1), lambda: profile_max(Counter({1: 2}), Counter({1: 1})),
               lambda: read_instance({**base, "weights": [1, 1]}),
               lambda: read_instance({**base, "target": [[0, 0, 0], [2, 0, 0]]}),
               lambda: read_instance({**base, "variance": 2}),
               lambda: read_instance({**base, "source": [[0, 0], [1, 0]]})]
    for f in invalid:
        try:
            f()
        except (ValueError, KeyError):
            rejected += 1
        else:
            raise ValueError("malformed input was not rejected")
    # Exact coefficient used for the all-k bound, not just a sample of k.
    G = F(129, 128)
    need((1 + G + G * G) / 64 < F(1, 20), "quadrature schedule coefficient")
    need(3 * G * G / 64 < F(1, 20), "tail schedule coefficient")
    budgets = [frontier_budget(k) for k in [1, 2, 7, 16, 64, 1024, 1000000]]
    return {"direct_profile_comparisons": cases, "exponential_enclosures": ecases,
            "peano_controls": peano, "gaussian_hinge_controls": gaussian_hinge_controls(),
            "rejected_inputs": rejected, "budgets": budgets,
            "C_interval": [str(v) for v in gaussian_constant(40)]}


def run_all():
    fixtures = json.loads((HERE / "DIRECT_FIXTURES.json").read_text())
    inputs = json.loads((HERE / "DIRECT_INPUTS.json").read_text())
    for name, record in inputs.items():
        need(sha256((HERE.parents[1] / name).read_bytes()).hexdigest() == record["sha256"],
             "changed pinned source: " + name)
    report = {"status": "DIRECT_HINGE_CERTIFICATES_PASS", "controls": controls(),
              "pinned_inputs": len(inputs), "fixtures": []}
    for item in fixtures:
        if item["name"] == "rational_frontier_full_rank_control":
            obj = item["instance"]
            xs = [tuple(map(rat, v)) for v in obj["source"]]
            ys = [tuple(map(rat, v)) for v in obj["target"]]
            ws = list(map(rat, obj["weights"]))
            rank = matrix_rank([x + y for x, y in zip(xs, ys)])
            need(rank == 6 and len(ws) <= 39 and xs[0] == ys[0] == (0, 0, 0),
                 "rank-six k=1 frontier geometry")
            need(all((a * 256).denominator == 1 for v in xs + ys for a in v)
                 and all((w * 156).denominator == 1 for w in ws),
                 "k=1 coordinate/mass denominators")
            need(all(sum(a * a for a in v) <= 9 for v in xs + ys), "frontier radius")
            losses = [sum((a - b) ** 2 for a, b in zip(xs[i], xs[j]))
                      - sum((a - b) ** 2 for a, b in zip(ys[i], ys[j]))
                      for i in range(len(xs)) for j in range(i)]
            need(min(losses) * 256 ** 2 >= 256, "frontier integer pair margin")
        rows = []
        for step in item["steps"]:
            row = enclose(item["instance"], rat(step), rat(item["tail"]),
                          item["bits"], item["require_contraction"])
            need(row["contraction"] == item["require_contraction"],
                 "fixture admissibility mismatch")
            rows.append(row)
        if item["name"] == "rational_frontier_full_rank_control":
            need(all(F(rows[i + 1]["upper"]) < F(rows[i]["upper"])
                     for i in range(len(rows) - 1)), "defect bounds did not decrease")
            need(F(rows[-1]["upper"]) < F(3, 250), "fine control exceeds 0.012")
        if item["name"] == "deliberately_noncontracting_sign_control":
            need(F(rows[-1]["lower"]) > F(4, 25), "positive-defect control failed")
        report["fixtures"].append({"name": item["name"], "rows": rows})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--controls", action="store_true")
    modes.add_argument("--input", type=Path)
    modes.add_argument("--budget", type=int)
    parser.add_argument("--step", default="1/8")
    parser.add_argument("--tail", default="4")
    parser.add_argument("--bits", type=int, default=40)
    parser.add_argument("--allow-noncontraction", action="store_true")
    parser.add_argument("--expected", type=Path, default=HERE / "DIRECT_EXPECTED.json")
    args = parser.parse_args()
    if args.input:
        result = enclose(json.loads(args.input.read_text()), rat(args.step),
                         rat(args.tail), args.bits, not args.allow_noncontraction)
    elif args.budget is not None:
        result = frontier_budget(args.budget)
    elif args.controls:
        result = controls()
    else:
        result = run_all()
        encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.write:
            args.expected.write_text(encoded)
        else:
            need(json.loads(args.expected.read_text()) == result,
                 "expected certificate mismatch")
        print(json.dumps({"status": result["status"],
                          "record_sha256": sha256(encoded.encode()).hexdigest()}))
        return
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
