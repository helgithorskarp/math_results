#!/usr/bin/env python3
"""Independent exact audit of the paired-rank conditional-kernel theorem.

The submitted verifier multiplies truncated power series and checks one
orthogonal certificate. This checker instead differentiates log(Phi) in
closed form, reconstructs Phi with a multivariate exponential recurrence,
tests a second nonorthogonal rank-six contraction, and checks the replica
scaling directly. It imports no submitted code or certificate.
"""

from fractions import Fraction as Q
from itertools import combinations, product
from math import factorial


DIM = 7
ZERO = (0,) * DIM


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add_vec(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub_vec(x, y):
    return tuple(a - b for a, b in zip(x, y))


def scale_vec(c, x):
    return tuple(c * a for a in x)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def dist2(x, y):
    return dot(sub_vec(x, y), sub_vec(x, y))


def multiindices(total, dimension=DIM):
    if dimension == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in multiindices(total - first, dimension - 1):
            yield (first,) + tail


def multinomial(alpha):
    out = factorial(sum(alpha))
    for a in alpha:
        out //= factorial(a)
    return out


def decrement(alpha, indices):
    out = list(alpha)
    for i in indices:
        out[i] -= 1
        if out[i] < 0:
            return None
    return tuple(out)


def all_subindices(alpha):
    for beta in product(*(range(a + 1) for a in alpha)):
        if beta != ZERO:
            yield beta


def log_phi_coefficient(alpha, point, vectors):
    """Coefficient of u^alpha in log Phi(point+u)-log Phi(point)."""
    degree = sum(alpha)
    require(degree > 0, "constant log coefficient is normalized away")
    point = tuple(Q(x) for x in point)
    norms = tuple(dot(w, w) for w in vectors)
    gram = tuple(tuple(dot(x, y) for y in vectors) for x in vectors)
    denominator = 2 + sum(point)
    bary_sum = tuple(sum(point[i] * vectors[i][j] for i in range(DIM))
                     for j in range(6))
    numerator0 = dot(bary_sum, bary_sum)

    answer = (Q(-5, 2) * Q((-1) ** (degree + 1), degree)
              * Q(multinomial(alpha), denominator ** degree))
    if degree == 1:
        answer -= Q(norms[alpha.index(1)], 2)
    answer += (Q(numerator0, 2 * denominator)
               * Q((-1) ** degree * multinomial(alpha), denominator ** degree))

    k = degree - 1
    linear_sum = Q(0)
    for i in range(DIM):
        rest = decrement(alpha, (i,))
        if rest is not None:
            linear_sum += 2 * dot(bary_sum, vectors[i]) * multinomial(rest)
    answer += Q((-1) ** k, 2 * denominator ** (k + 1)) * linear_sum

    if degree >= 2:
        k = degree - 2
        quadratic_sum = Q(0)
        for i in range(DIM):
            rest = decrement(alpha, (i, i))
            if rest is not None:
                quadratic_sum += gram[i][i] * multinomial(rest)
            for j in range(i + 1, DIM):
                rest = decrement(alpha, (i, j))
                if rest is not None:
                    quadratic_sum += 2 * gram[i][j] * multinomial(rest)
        answer += Q((-1) ** k, 2 * denominator ** (k + 1)) * quadratic_sum
    return answer


def phi_taylor(vectors, limit=4):
    """Taylor coefficients of Phi(u)/Phi(0), via exp(log Phi)."""
    logs = {}
    coefficients = {ZERO: Q(1)}
    for degree in range(1, limit + 1):
        for alpha in multiindices(degree):
            logs[alpha] = log_phi_coefficient(alpha, ZERO, vectors)
            value = Q(0)
            for beta in all_subindices(alpha):
                remainder = tuple(a - b for a, b in zip(alpha, beta))
                value += sum(beta) * logs[beta] * coefficients[remainder]
            coefficients[alpha] = value / degree
    return coefficients


def poly_add(p, q):
    out = dict(p)
    for a, value in q.items():
        out[a] = out.get(a, Q(0)) + value
        if out[a] == 0:
            del out[a]
    return out


def poly_scale(c, p):
    return {a: c * value for a, value in p.items() if c * value}


def poly_mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            exponent = tuple(i + j for i, j in zip(a, b))
            out[exponent] = out.get(exponent, Q(0)) + x * y
    return {a: value for a, value in out.items() if value}


def constant(c):
    return {ZERO: Q(c)} if c else {}


def variable(i):
    return {tuple(int(i == j) for j in range(DIM)): Q(1)}


def moment(coefficients, alpha):
    value = coefficients[alpha]
    for exponent in alpha:
        value *= factorial(exponent)
    return (-1) ** sum(alpha) * value


def square_value(polynomial, coefficients):
    square = poly_mul(polynomial, polynomial)
    return sum(value * moment(coefficients, alpha)
               for alpha, value in square.items())


def inverse(matrix):
    n = len(matrix)
    rows = [[Q(x) for x in row] + [Q(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if rows[i][col]), None)
        require(pivot is not None, "singular Gram matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x / divisor for x in rows[col]]
        for i in range(n):
            if i != col and rows[i][col]:
                multiplier = rows[i][col]
                rows[i] = [x - multiplier * y for x, y in zip(rows[i], rows[col])]
    return tuple(tuple(row[n:]) for row in rows)


def paired_vectors(source, target, base_pair):
    paired = tuple(tuple(Q(x) for x in (a + b)) for a, b in zip(source, target))
    i, j = base_pair
    centroid = scale_vec(Q(1, 2), add_vec(paired[i], paired[j]))
    return paired, tuple(sub_vec(u, centroid) for u in paired)


def certify_contraction(source, target):
    losses = []
    for i, j in combinations(range(len(source)), 2):
        loss = dist2(source[i], source[j]) - dist2(target[i], target[j])
        require(loss >= 0, "fixture is not a contraction")
        losses.append(loss)
    return losses


def special_obstruction():
    source = ((0, 0, 0), (1, 0, 0), (-1, 0, 0), (0, 1, 0),
              (0, -1, 0), (0, 0, 1), (0, 0, -1))
    target = tuple(tuple(abs(x) for x in point) for point in source)
    losses = certify_contraction(source, target)
    require(losses.count(4) == 3 and losses.count(0) == 18,
            "special loss census mismatch")
    paired, vectors = paired_vectors(source, target, (1, 2))
    differences = tuple(sub_vec(vectors[i], vectors[0]) for i in range(1, DIM))
    require(all(dot(differences[i], differences[j]) == 2 * int(i == j)
                for i in range(6) for j in range(6)), "special rank-six basis mismatch")

    p = poly_scale(Q(4), variable(0))
    for i in range(1, DIM):
        term = poly_add(constant(1), poly_add(variable(0), poly_scale(-1, variable(i))))
        p = poly_add(p, poly_scale(-1, poly_mul(term, term)))
    coefficients = phi_taylor(vectors)
    require(square_value(p, coefficients) == -1, "special negative square mismatch")
    return paired, vectors


def nonorthogonal_obstruction():
    source = ((0, 0, 0), (10, 0, 0), (0, 10, 0), (0, 0, 10),
              (10, 10, 0), (10, 0, 10), (0, 10, 10))
    target = ((0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
              (1, 0, 0), (0, 1, 0), (0, 0, 1))
    losses = certify_contraction(source, target)
    require(all(loss > 0 for loss in losses), "second fixture lacks strict loss")
    _, vectors = paired_vectors(source, target, (0, 1))
    differences = tuple(sub_vec(vectors[i], vectors[0]) for i in range(1, DIM))
    gram = tuple(tuple(dot(x, y) for y in differences) for x in differences)
    gram_inverse = inverse(gram)

    r = []
    for i, difference in enumerate(differences, start=1):
        d = Q(dot(difference, difference), 2)
        r.append(poly_add(constant(d), poly_add(variable(0), poly_scale(-1, variable(i)))))
    quadratic = {}
    for i in range(6):
        for j in range(6):
            quadratic = poly_add(quadratic,
                                 poly_scale(gram_inverse[i][j], poly_mul(r[i], r[j])))
    rg = poly_add(variable(0), poly_scale(Q(-1, 2), quadratic))
    coefficients = phi_taylor(vectors)
    require(square_value(rg, coefficients) == Q(-1, 16),
            "general Gram obstruction mismatch")
    return len(losses), len(rg)


def replicated_scatter_checks(paired, vectors):
    checks = 0
    fixtures = (
        (2, (0, 1, 0, 2, 0, 1, 0), (1, 0, 0, 0, 1, 0, 0)),
        (3, (2, 0, 1, 0, 3, 1, 2), (0, 2, 1, 1, 0, 0, 1)),
        (7, (1, 4, 2, 3, 0, 2, 5), (2, 0, 3, 0, 1, 1, 0)),
    )
    base_scatter = dist2(paired[1], paired[2]) / 2
    for n, m, r in fixtures:
        counts = [m[i] + r[i] for i in range(DIM)]
        counts[1] += n
        counts[2] += n
        cardinality = sum(counts)
        total = tuple(sum(counts[i] * paired[i][j] for i in range(DIM))
                      for j in range(6))
        scatter = (sum(counts[i] * dot(paired[i], paired[i]) for i in range(DIM))
                   - Q(dot(total, total), cardinality))
        direct_exponent = Q(scatter, 2 * n)

        weights = tuple(Q(m[i] + r[i], n) for i in range(DIM))
        weighted_sum = tuple(sum(weights[i] * vectors[i][j] for i in range(DIM))
                             for j in range(6))
        extra = (sum(weights[i] * dot(vectors[i], vectors[i]) for i in range(DIM))
                 - Q(dot(weighted_sum, weighted_sum), 2 + sum(weights)))
        require(direct_exponent == base_scatter / 2 + extra / 2,
                "replica exponent scaling mismatch")
        require(Q(cardinality, n) == 2 + sum(weights),
                "replica cardinality scaling mismatch")
        checks += 2
    return checks


def low_rank_completion_checks():
    base = ((0, 0, 0, 0, 0), (2, 0, 0, 0, 0), (0, 3, 0, 0, 0))
    remaining = ((1, 1, 1, 0, 0), (-1, 2, 0, 1, 0), (0, -2, 1, 0, 1))
    p = len(base)
    centroid = tuple(Q(sum(x[j] for x in base), p) for j in range(5))
    base_scatter = sum(dist2(x, centroid) for x in base)
    shifted = tuple(sub_vec(x, centroid) for x in remaining)
    checks = 0
    for mask in product((0, 1), repeat=len(remaining)):
        subset = [remaining[i] for i, bit in enumerate(mask) if bit]
        all_points = list(base) + subset
        mean = tuple(Q(sum(x[j] for x in all_points), len(all_points)) for j in range(5))
        direct = sum(dist2(x, mean) for x in all_points)
        chosen = [shifted[i] for i, bit in enumerate(mask) if bit]
        total = tuple(sum((x[j] for x in chosen), Q(0)) for j in range(5))
        completed = (base_scatter + sum(dot(x, x) for x in chosen)
                     - Q(dot(total, total), p + len(chosen)))
        require(direct == completed, "rank-five square completion mismatch")
        checks += 1
    return checks


def main():
    paired, vectors = special_obstruction()
    nonorthogonal = nonorthogonal_obstruction()
    replica_checks = replicated_scatter_checks(paired, vectors)
    completion_checks = low_rank_completion_checks()
    print("INDEPENDENT_CONDITIONAL_RANK_REVIEW_PASS")
    print("special negative square: -1; physical pair checks: 21")
    print("nonorthogonal strict-loss pairs/polynomial terms:", *nonorthogonal)
    print("replica scaling checks:", replica_checks)
    print("rank-five completion subsets:", completion_checks)


if __name__ == "__main__":
    main()
