#!/usr/bin/env python3
"""Exact algebra checks accompanying PROOF.md; not a universal proof checker."""
from fractions import Fraction as F
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def q(A, v):
    return sum(A[i][j] * v[i] * v[j]
               for i in range(len(v)) for j in range(len(v)))


def posterior_checks():
    points = [tuple(map(F, p)) for p in
              [(0, 0, 0), (-2, 1, 3), (1, -2, 0), (3, 2, -1), (-1, -1, 2)]]
    maps = [lambda p: (p[0], p[1] / 2, p[2] / 3),
            lambda p: (abs(p[0]), abs(p[1]), p[2]),
            lambda p: (-p[1] + 2, p[0] - 3, p[2] + 1)]
    count = 0
    strictly_positive = 0
    for transform in maps:
        image = [transform(p) for p in points]
        losses = [[dot(sub(p, r), sub(p, r)) - dot(sub(y, z), sub(y, z))
                   for r, z in zip(points, image)] for p, y in zip(points, image)]
        require(all(d >= 0 for row in losses for d in row), "contraction fixture")
        for seed in range(1, 9):
            weights = [F((i + seed) ** 2 + 1) for i in range(len(points))]
            total = sum(weights)
            weights = [p / total for p in weights]
            mean_x = tuple(sum(w * p[k] for w, p in zip(weights, points)) for k in range(3))
            mean_y = tuple(sum(w * p[k] for w, p in zip(weights, image)) for k in range(3))
            covariance_trace = sum(w * (dot(x, x) - dot(y, y))
                                   for w, x, y in zip(weights, points, image))
            covariance_trace -= dot(mean_x, mean_x) - dot(mean_y, mean_y)
            ordered = sum(weights[i] * weights[j] * losses[i][j]
                          for i in range(len(points)) for j in range(len(points)))
            require(covariance_trace == ordered / 2, "posterior factor 1/2")
            require(covariance_trace >= 0, "posterior sign")
            if covariance_trace > 0:
                require(covariance_trace != ordered, "missing-factor control")
                require(-ordered / 2 < 0, "reversed-loss control")
                strictly_positive += 1
            count += 1
    return {"cases": count, "strict_cases": strictly_positive}


def gaussian_checks():
    count = 0
    for n, m in [(1, 1), (2, 3), (3, 3), (4, 2)]:
        for t in [F(1, 5), F(1, 2), F(3, 4)]:
            for a2, b2 in [(F(0), F(0)), (F(5, 3), F(7, 2)), (F(9), F(1, 7))]:
                # rho_t is N(0,t I_n) times N(0,(1-t) I_m).
                time_log_derivative = -F(n, 2) / t + F(m, 2) / (1 - t)
                time_log_derivative += a2 / (2 * t * t) - b2 / (2 * (1 - t) ** 2)
                laplacian_ratio = a2 / t ** 2 - F(n) / t
                laplacian_ratio -= b2 / (1 - t) ** 2 - F(m) / (1 - t)
                require(time_log_derivative == laplacian_ratio / 2, "Gaussian heat normalization")
                count += 1
    return count


def multiply2(p, r):
    out = {}
    for a, x in p.items():
        for b, y in r.items():
            index = tuple(i + j for i, j in zip(a, b))
            if sum(index) <= 2:
                out[index] = out.get(index, F(0)) + x * y
    return out


def second(p, i, j, d):
    index = [0] * d
    index[i] += 1
    index[j] += 1
    return p.get(tuple(index), F(0)) * (2 if i == j else 1)


def apply_operator(A, p):
    d = len(A)
    return sum(A[i][j] * second(p, i, j, d) for i in range(d) for j in range(d))


def chain_and_moment_checks():
    d = 3
    count = 0
    for seed in range(1, 19):
        A = [[F(((i + j + seed) % 7) - 3, i + j + 1)
              for j in range(d)] for i in range(d)]
        B = [[F(((i + 1) * (j + 1) + seed) % 9 - 4, seed + 1)
              for j in range(d)] for i in range(d)]
        g = [F(seed - 2 * i, i + 2) for i in range(d)]
        h = {}
        for i in range(d):
            index = [0] * d
            index[i] = 1
            h[tuple(index)] = g[i]
            for j in range(d):
                index = [0] * d
                index[i] += 1
                index[j] += 1
                index = tuple(index)
                h[index] = h.get(index, F(0)) + B[i][j] / 2
        # Taylor expansion exp(-h)/exp(-h(0)) through degree two.
        exponential = {(0,) * d: F(1)}
        for index, value in h.items():
            exponential[index] = exponential.get(index, F(0)) - value
        for index, value in multiply2(h, h).items():
            exponential[index] = exponential.get(index, F(0)) + value / 2
        require(apply_operator(A, exponential) == q(A, g) - apply_operator(A, h),
                "exponential chain rule including mixed derivatives")
        for i in range(d):
            for j in range(d):
                index = [0] * d
                index[i] += 1
                index[j] += 1
                require(apply_operator(A, {tuple(index): F(1)}) == 2 * A[i][j],
                        "quadratic moment test")
                count += 1
    return {"chain_jets": 18, "quadratic_tests": count}


def span_and_sign_checks():
    J = [[F((1 if i < 3 else -1) if i == j else 0)
          for j in range(6)] for i in range(6)]
    # A rational orthogonal output rotation. Columns of [I; O] are null.
    O = [[F(3, 5), F(-4, 5), F(0)],
         [F(4, 5), F(3, 5), F(0)], [F(0), F(0), F(-1)]]
    columns = [tuple(F(i == j) for i in range(3)) + tuple(O[i][j] for i in range(3))
               for j in range(3)]
    counts = 0
    for rank in range(4):
        for v in columns[:rank]:
            for w in columns[:rank]:
                bilinear = (q(J, tuple(a + b for a, b in zip(v, w))) - q(J, v) - q(J, w)) / 2
                require(bilinear == 0, "isometric graph compression")
                counts += 1
    # Coercive wave-harmonic h=|a+b|+|a-b|: characteristic Hessian normals
    # have Q=0, but exposed gradients include (2,0) and (0,2).
    indefinite = [[F(1), F(0)], [F(0), F(-1)]]
    require(q(indefinite, (1, 1)) == q(indefinite, (1, -1)) == 0, "wave characteristics")
    require(q(indefinite, (2, 0)) == 4 and q(indefinite, (0, 2)) == -4,
            "omitted-gradient-sign negative control")
    # h(a,b)=|a|, A=diag(0,1): Lh=0 and Q(grad h)=0, but no coercivity on R2.
    degenerate = [[F(0), F(0)], [F(0), F(1)]]
    require(q(degenerate, (1, 0)) == 0 and q(degenerate, (0, 1)) == 1,
            "omitted-essential-span negative control")
    return {"null_gram_entries": counts, "negative_controls": 2}


def constant_checks():
    cubic = 3 + F(27, 4) + F(27, 16)
    require(cubic == F(183, 16) and cubic < 12, "radial cubic error")
    require(F(4, 3) * 12 == 16, "volume error divided by pi")
    require(4 * 16 - 32 == 2 * 16, "KP strict cutoff margin")
    require(F(1, 4) / 12 == F(1, 48), "spherical lower bound at lambda0")
    require(F(4, 48) == F(1, 12) and 44 / F(1, 12) >= 8, "endpoint cutoff")
    require(8 + 6 * 2 + 6 * 4 == 44, "endpoint uniform error")
    require(F(9, 64) > F(1, 8), "endpoint threshold overlap")
    # Write ell=log(1/m_*). Tail lower bound at 2(1+ell)/omega is one.
    for omega, ell in [(F(1, 3), F(0)), (F(7, 2), F(5)), (F(2, 11), F(17, 3))]:
        require(omega / 2 * (2 * (1 + ell) / omega) - ell == 1, "cover-mass tail")
    return {"cubic_error_coefficient": str(cubic), "kp_cutoff_coefficient": 16,
            "gap_denominator": 48, "endpoint_coefficient": 44}


def main():
    result = {"status": "COMPACT_WIDTH_RIGIDITY_ALGEBRA_PASS",
              "posterior": posterior_checks(), "gaussian_density_cases": gaussian_checks(),
              "chain_and_moments": chain_and_moment_checks(),
              "span_and_sign": span_and_sign_checks(), "constants": constant_checks(),
              "trust_boundary": "Exact finite algebra only; universal statements require PROOF.md and its pinned analytic premises."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
