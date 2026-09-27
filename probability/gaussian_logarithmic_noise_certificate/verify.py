"""Exact finite controls for the universal written theorem, not a geometry scan."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement
import json
from math import comb, factorial
from pathlib import Path

import certificate as cert
import moments

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def pins():
    data = json.loads((ROOT / "INPUTS.json").read_text())
    for row in data:
        p = (ROOT / row["relative_path"]).resolve()
        need(p.is_file(), "missing dependency")
        need(hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"],
             "changed dependency: " + row["relative_path"])
    return len(data)


def constants():
    e = F(1, 96)
    kap = 1 - e
    c2 = 32 * e / kap
    need(c2 <= F(9, 25), "modulus c bound")
    need(kap ** -3 <= F(9, 8), "kappa bound")
    need(5 * e + c2 / 2 < F(1, 4), "exponential argument")
    need(F(25, 9) < 3 and F(44, 7) < F(64, 9), "pi radical comparisons")
    modulus = F(1, 4) * F(9, 8) * F(4, 3) * F(169, 25) * F(139, 25)
    need(modulus == F(70473, 5000) and modulus < 16, "modulus constant")
    need(32 * F(3, 16) / kap <= F(25, 4), "interior q squared")
    need(5 - 1 / kap - F(5, 2) > 1, "interior beta gap")
    need(5 * e + F(5, 2) < 3, "interior exponential")
    need(F(4, 3) - e / 2 > 1, "interior lower log")
    need(F(1, 648) > F(1, 1024), "interior rational weakening")
    # exp(3/4) upper: 1+3/4 plus a geometric tail from order two.
    need(1 + F(3, 4) + F(9, 32) / (1 - F(1, 4)) == F(17, 8), "outer exponential")
    need(sum(F(4) ** j / factorial(j) for j in range(5)) > 32, "exp4 lower")
    need(F(1, 32) * 4 < F(1, 4), "Legendre exponent squared")
    need(F(38, 64) + F(1, 64 ** 2) < 1, "Chebyshev norm induction")
    return {"modulus_upper": str(modulus), "interior_lower": "1/1024",
            "tail_modulus": 16, "polynomial_margin_exponent": "-4k-6"}


def schedule_controls():
    records = []
    for n in range(1025):
        row = cert.schedule(n)
        cert.verify_schedule(row)
        k, q = row["k"], row["taylor_order"]
        r, a = F(1, 2 ** (2 * k)), F(1, 2 ** (5 * k - 2))
        length = F(1, 4) - r
        need(0 < a < r < F(1, 4) and length >= F(1, 8), "coverage")
        need((n + 1) ** 2 * r <= F(1, 256), "degree bound")
        need((n + 1) ** 2 / length <= 1 / (32 * r), "kernel constant")
        # A rational upper bound for a^(3/2)/r^2; no floating square root.
        root_upper = F(1, 2 ** (2 * k - 1))
        need(a <= root_upper ** 2, "tail root upper")
        need(a * root_upper / r ** 2 == F(1, 2 ** (3 * k - 3)), "tail ratio")
        need(F(2, 3) * a * root_upper / r ** 2 < F(1, 2048), "tail payment")
        need(q >= 3 * F(n + 2, 8 * k), "factorial schedule")
        need(n + 1 <= 2 ** n, "coefficient count")
        need(n + 6 * n - q - 3 <= -4 * k - 8, "Taylor error exponent")
        records.append(row)
    # Edge degrees and compressed, far larger schedules; no expanded moments.
    for k in [12, 13, 16, 32, 64, 128, 1024]:
        n = 2 ** (k - 4) - 1
        cert.eligible(k, n)
        row = cert.schedule(n)
        need(row["k"] == k, "degree endpoint")
        cert.verify_schedule(row)
        try:
            cert.eligible(k, n + 1)
        except ValueError:
            pass
        else:
            raise ValueError("accepted degree past boundary")
    return {"small_schedules": len(records), "schedule_digest": sha(records),
            "large_k": [12, 13, 16, 32, 64, 128, 1024],
            "examples": [cert.schedule(2 ** (k - 4) - 1) for k in [12, 16, 32]]}


def add(p, q):
    r = [F(0)] * max(len(p), len(q))
    for i, x in enumerate(p):
        r[i] += x
    for i, x in enumerate(q):
        r[i] += x
    return r


def scale(p, x):
    return [v * x for v in p]


def mul(p, q):
    r = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return r


def val(p, x):
    s = F(0)
    for a in reversed(p):
        s = s * x + a
    return s


def integral(p, a, b):
    return sum(c * (b ** (i + 1) - a ** (i + 1)) / (i + 1)
               for i, c in enumerate(p))


def legendre(n):
    rows = [[F(1)]]
    if n:
        rows.append([F(0), F(1)])
    for j in range(1, n):
        rows.append(scale(add(scale(mul([0, 1], rows[j]), 2 * j + 1),
                              scale(rows[j - 1], -j)), F(1, j + 1)))
    return rows


def legendre_controls():
    rows = legendre(16)
    orth = 0
    rep = 0
    laplace = 0
    for i, pi in enumerate(rows):
        for j, pj in enumerate(rows):
            actual = integral(mul(pi, pj), F(-1), F(1))
            need(actual == (F(2, 2 * i + 1) if i == j else 0), "orthogonality")
            orth += 1
        # Laplace's integral, expanded as a polynomial; even cosine moments.
        rebuilt = [F(0)]
        for j in range(i // 2 + 1):
            term = [F(1)]
            for _ in range(j):
                term = mul(term, [-1, 0, 1])
            term = [F(0)] * (i - 2 * j) + term
            rebuilt = add(rebuilt, scale(term, F(comb(i, 2 * j) * comb(2 * j, j), 4 ** j)))
        while len(rebuilt) < len(pi):
            rebuilt.append(F(0))
        need(rebuilt == pi, "Laplace integral coefficient identity")
        laplace += 1
    for n in range(9):
        for degree in range(n + 1):
            p = [F(0)] * degree + [F(1)]
            for x in [F(-3, 2), F(-1), F(0), F(2, 3), F(5, 4)]:
                reproduced = sum(F(2 * j + 1, 2) * val(rows[j], x)
                                 * integral(mul(rows[j], p), F(-1), F(1))
                                 for j in range(n + 1))
                need(reproduced == x ** degree, "reproduction including outside interval")
                rep += 1
    return {"orthogonality_pairs": orth, "reproduced_monomials": rep,
            "Laplace_polynomial_identities": laplace}


def definition_scatter(points, weights, q, m):
    """Independent multiset enumeration, using only pair distances."""
    n = len(points)
    dist = [[sum((points[i][a] - points[j][a]) ** 2 for a in range(3))
             for j in range(n)] for i in range(n)]
    row = [F(0)] * (q + 1)
    multisets = 0
    for labels in combinations_with_replacement(range(n), m):
        counts = Counter(labels)
        multiplicity = factorial(m)
        weight = F(1)
        for i, c in counts.items():
            multiplicity //= factorial(c)
            weight *= weights[i] ** c
        weight *= multiplicity
        z = sum(dist[labels[i]][labels[j]] for i in range(m) for j in range(i + 1, m)) / (2 * m)
        for r in range(q + 1):
            row[r] += weight * z ** r
        multisets += 1
    need(row[0] == 1, "replica probability total")
    return row, multisets


def dyadic_enclosure(lo, hi, bits=64):
    need(lo <= hi, "ordered summary bounds")
    d = 2 ** bits
    return [str(F((lo * d).numerator // (lo * d).denominator, d)),
            str(F(-((-hi * d).numerator // (-hi * d).denominator), d))]


def gaussian_controls():
    # Existing known-positive deep-flap geometry, scaled for this calibration.
    v = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    sx = list(v)
    sy = list(v)
    for i in range(4):
        for j in range(4):
            if i != j:
                sx.append(tuple(v[j][a] - 2 * v[i][a] for a in range(3)))
                sy.append(tuple(v[j][a] + 2 * v[i][a] for a in range(3)))
    x = [tuple(F(t, 1024) for t in row) for row in sx]
    y = [tuple(F(63 * t, 64 * 1024) for t in row) for row in sy]
    epsilon = F(19, 1024 ** 2)
    p = [F(1), F(-16), F(64)]  # (8u-1)^2, max_I p=1 when k=12.
    k, q, max_m = 12, 4, 4
    need(epsilon <= F(1, 8 * k), "calibration radius")
    summary = []
    for label, weights in [
        ("uniform", [F(1, 16)] * 16),
        ("small_loss", [1 - F(15, 2 ** 40)] + [F(1, 2 ** 40)] * 15),
    ]:
        got = moments.finite_taylor_moments(x, y, weights, epsilon, q, max_m, bits=160)
        need(got["loss"] > 0, "positive actual loss")
        checked = 0
        for points, rows in [(x, got["source_scatters"]), (y, got["target_scatters"])]:
            for m in range(2, max_m + 1):
                direct, count = definition_scatter(points, weights, q, m)
                need(direct == rows[m], "marginal producer versus replica definition")
                checked += count
        lo = hi = F(0)
        for coefficient, interval in zip(p, got["intervals"]):
            a, b = moments.interval_scale(interval, coefficient)
            lo += a
            hi += b
        # Even Q has a_r-L_r in [0,d*e_r]. Retain the one-sided signs.
        elow = ehigh = F(0)
        absolute = F(0)
        for r, coefficient in enumerate(p):
            m = r + 2
            er = (m * epsilon / 2) ** q / (4 * m ** 2 * factorial(q))
            if coefficient < 0:
                elow += got["loss"] * coefficient * er
            else:
                ehigh += got["loss"] * coefficient * er
            absolute += abs(coefficient) * er
        need(absolute < F(1, 2 ** (4 * k + 8)), "actual Q4 error pays uniform margin")
        lo += elow
        hi += ehigh
        need(lo > got["loss"] / 2 ** (4 * k + 6), "actual energy enclosure")
        summary.append({"control": label, "epsilon": str(epsilon), "Q": q,
                        "loss": str(got["loss"]), "replica_multisets": checked,
                        "energy_over_loss_interval": dyadic_enclosure(lo / got["loss"], hi / got["loss"]),
                        "Taylor_error_over_loss": str(absolute),
                        "exact_coefficients_digest": sha([str(c) for c in got["coefficients"]])})
    # Actual paired affine rank six, checked by fraction Gaussian elimination.
    matrix = [[x[i][j] - x[0][j] for j in range(3)] +
              [y[i][j] - y[0][j] for j in range(3)] for i in range(1, len(x))]
    rank = 0
    for col in range(6):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][col]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        row = [v / matrix[rank][col] for v in matrix[rank]]
        matrix[rank] = row
        for i in range(rank + 1, len(matrix)):
            factor = matrix[i][col]
            matrix[i] = [a - factor * b for a, b in zip(matrix[i], row)]
        rank += 1
    need(rank == 6, "paired rank six control")
    return {"paired_rank": rank, "controls": summary}


def rejections():
    good = cert.schedule(255)
    trials = [lambda: cert.schedule(-1), lambda: cert.schedule(True),
              lambda: cert.schedule(F(1, 2)), lambda: cert.eligible(11, 0),
              lambda: cert.eligible(12, 256)]
    for field in ["minimum_variance_over_radius_squared", "taylor_order",
                  "energy_gap_over_loss_and_curvature_norm_lower_power_of_two"]:
        damaged = dict(good)
        damaged[field] += 1
        trials.append(lambda row=damaged: cert.verify_schedule(row))
    trials.extend([
        lambda: moments.finite_input([(0, 0, 0)], [(0, 0, 0)], [F(1, 2)], F(1, 96)),
        lambda: moments.finite_input([(0, 0, 0), (0, 0, 0)], [(0, 0, 0), (F(1, 100), 0, 0)], [F(1, 2)] * 2, F(1, 96)),
        lambda: moments.finite_input([(1, 0, 0)], [(0, 0, 0)], [1], F(1, 96)),
        lambda: moments.interval_scale((F(2), F(1)), F(1)),
    ])
    for trial in trials:
        try:
            trial()
        except (ValueError, TypeError):
            continue
        raise ValueError("damaged input was accepted")
    return len(trials)


def result():
    return {"status": "LOGARITHMIC_NOISE_CERTIFICATE_PASS", "dependency_pins": pins(),
            "constants": constants(), "schedules": schedule_controls(),
            "Legendre_controls": legendre_controls(), "Gaussian_controls": gaussian_controls(),
            "rejected_inputs": rejections(),
            "trust": "author written universal theorem; exact controls; not independent acceptance"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    actual = result()
    expected = ROOT / "EXPECTED.json"
    if args.write_expected:
        expected.write_text(json.dumps(actual, indent=2, sort_keys=True) + "\n")
    else:
        need(json.loads(expected.read_text()) == actual, "expected record mismatch")
    print(actual["status"])
    print("record_sha256=" + sha(actual))
