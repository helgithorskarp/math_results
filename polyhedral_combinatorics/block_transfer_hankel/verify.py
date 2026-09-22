"""Exact auxiliary audit for the weighted block-transfer theorem.

Python 3.11+, standard library. The universal proof is in PROOF.md.
Direct transfer moments and Newton determinants are independent of the
Jacobi recurrence; uncompressed block states check the Ehrhart application.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from math import comb, prod, isqrt
from pathlib import Path
import json
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def scalar(x, p=None):
    x = F(x)
    if p is None:
        return x
    return x.numerator * pow(x.denominator % p, -1, p) % p


def divide(x, y, p=None):
    require(y != 0, "division by zero")
    return scalar(x / y) if p is None else x * pow(y, -1, p) % p


def trim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def add(a, b, p=None):
    c = [scalar(0, p)] * max(len(a), len(b))
    for i in range(len(c)):
        c[i] = scalar((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0), p)
    return trim(c)


def scale(a, c, p=None):
    return trim([scalar(x * c, p) for x in a])


def sub(a, b, p=None):
    return add(a, scale(b, -1, p), p)


def multiply(a, b, p=None):
    c = [scalar(0, p)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = scalar(c[i + j] + x * y, p)
    return trim(c)


def remainder(a, b, p=None):
    a = trim(a[:])
    while a != [0] and len(a) >= len(b):
        k = len(a) - len(b)
        a = sub(a, [0] * k + scale(b, divide(a[-1], b[-1], p), p), p)
    return a


def gcd_degree(a, b, p=None):
    while b != [0]:
        a, b = b, remainder(a, b, p)
    return len(a) - 1


def mm(a, b, p=None):
    return [[scalar(sum(x * y for x, y in zip(row, col)), p)
             for col in zip(*b)] for row in a]


def identity(n, p=None):
    return [[scalar(i == j, p) for j in range(n)] for i in range(n)]


def determinant(a, p=None):
    a = [[scalar(x, p) for x in row] for row in a]
    n, ans = len(a), scalar(1, p)
    for i in range(n):
        pivot = next((j for j in range(i, n) if a[j][i]), None)
        if pivot is None:
            return scalar(0, p)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            ans = scalar(-ans, p)
        ans = scalar(ans * a[i][i], p)
        for j in range(i + 1, n):
            t = divide(a[j][i], a[i][i], p)
            for k in range(i, n):
                a[j][k] = scalar(a[j][k] - t * a[i][k], p)
    return ans


def transfer(w):
    n = len(w)
    return [[w[j] if i + j < n else 0 for j in range(n)] for i in range(n)]


def moments(w, count, p=None):
    n, v, ans = len(w), [scalar(1, p)] * len(w), []
    for _ in range(count):
        ans.append(scalar(sum(x * y for x, y in zip(w, v)), p))
        v = [scalar(sum(w[j] * v[j] for j in range(n - i)), p) for i in range(n)]
    return ans


def newton_denominator(w):
    """det(I-yC) from literal powers/traces of C, in characteristic zero."""
    c, power, traces, q = transfer(w), identity(len(w)), [0], [F(1)]
    for k in range(1, len(w) + 1):
        power = mm(power, c)
        traces.append(sum(power[i][i] for i in range(len(w))))
        q.append(-sum(q[k - j] * traces[j] for j in range(1, k + 1)) / k)
    return q


def zigzag(n):
    return [j // 2 if j % 2 == 0 else n - 1 - j // 2 for j in range(n)]


def validate(w, p=None):
    require(len(w) >= 1, "nonempty weight vector")
    if p is not None:
        require(p >= 2 and all(p % d for d in range(2, isqrt(p) + 1)), "prime field")
    w = [scalar(x, p) for x in w]
    require(all(w), "nonzero weights")
    return w


def jacobi_data(w, p=None):
    w = validate(w, p)
    n, v = len(w), zigzag(len(w))
    alpha = divide(scalar((-1) ** (n - 1), p), w[v[-1]], p)
    beta = [scalar(0, p)] + [divide(scalar(1, p), scalar(w[v[j - 1]] * w[v[j]], p), p)
                            for j in range(1, n)]
    polynomials = [[scalar(1, p)]]
    for k in range(1, n + 1):
        diagonal = alpha if k == n else scalar(0, p)
        current = multiply([-diagonal, 1], polynomials[-1], p)
        if k > 1:
            current = sub(current, scale(polynomials[-2], beta[k - 1], p), p)
        polynomials.append(current)
    return alpha, beta, polynomials


def recover(q, p=None):
    """Recover nonzero ordered weights from a valid normalized denominator.

    Parity splitting and backwards continuants are classical inverse-Jacobi
    operations (Holtz 2005); this implementation uses beta=codiagonal^2.
    No division by 2 or numerical eigenvalue computation is used.
    """
    q = trim([scalar(x, p) for x in q])
    n = len(q) - 1
    require(n >= 1 and q[0] == 1, "normalized positive-degree denominator")
    current = scale(q, divide(scalar(1, p), q[-1], p), p)
    alpha = scalar(-current[-2], p)
    require(alpha != 0, "nonzero terminal diagonal")
    beta = [scalar(0, p)] * n
    if n > 1:
        opposite = [c if j % 2 != n % 2 else scalar(0, p)
                    for j, c in enumerate(current)]
        previous = scale(opposite, divide(scalar(-1, p), alpha, p), p)
        require(len(previous) == n and previous[-1] == 1, "parity split")
        for k in range(n, 1, -1):
            diagonal = alpha if k == n else 0
            r = sub(multiply([-diagonal, 1], previous, p), current, p)
            require(len(r) == k - 1 and r[-1] != 0, "nonzero codiagonal product")
            beta[k - 1] = r[-1]
            nxt = scale(r, divide(scalar(1, p), r[-1], p), p)
            require(all(c == 0 for j, c in enumerate(nxt) if j % 2 != (k - 2) % 2), "continuant parity")
            current, previous = previous, nxt
        require(current == [0, 1] and previous == [1], "continuant endpoint")
    v, w = zigzag(n), [scalar(0, p)] * n
    w[v[-1]] = divide(scalar((-1) ** (n - 1), p), alpha, p)
    for j in range(n - 1, 0, -1):
        w[v[j - 1]] = divide(scalar(1, p), scalar(beta[j] * w[v[j]], p), p)
    return w


def audit_vector(raw, p=None):
    w = validate(raw, p)
    n, v = len(w), zigzag(len(w))
    a = moments(w, 3 * n + 4, p)
    q = [scalar(c, p) for c in newton_denominator(list(map(F, raw)))]
    alpha, beta, polys = jacobi_data(w, p)
    q2 = scale(polys[-1], divide(scalar(1, p), polys[-1][0], p), p)
    require(q == q2, "Newton/Jacobi determinant disagreement")
    require(recover(q, p) == w, "ordered weight reconstruction")
    # Verify the inverse matrix in the original coordinates, without radicals.
    signs = [(-1) ** (j * (j - 1) // 2) for j in range(n)]
    inv = [[scalar(0, p) for _ in range(n)] for _ in range(n)]
    inv[v[-1]][v[-1]] = alpha
    for j in range(1, n):
        for k, l in ((j - 1, j), (j, j - 1)):
            inv[v[k]][v[l]] = divide(scalar(signs[k] * signs[l], p), w[v[k]], p)
    require(mm(transfer(w), inv, p) == identity(n, p), "inverse path matrix")
    d = scalar((-1) ** (n * (n - 1) // 2) * prod(w), p)
    base = scalar(prod(w[i] ** (2 * j + 1) for j, i in enumerate(v)), p)
    for s in range(4):
        actual = determinant([[a[s + i + j] for j in range(n)] for i in range(n)], p)
        require(actual == scalar(d ** s * base, p), "shifted Hankel product")
    numerator = [scalar(sum(q[j] * a[k - j] for j in range(k + 1)), p) for k in range(n)]
    require(gcd_degree(trim(numerator), q, p) == 0, "uncancelled denominator")
    require(numerator[-1] == scalar(-q[-1], p), "numerator leading coefficient")
    for k in range(n, len(a)):
        require(scalar(sum(q[j] * a[k - j] for j in range(n + 1)), p) == 0, "moment recurrence")
    if p is None and all(x > 0 for x in w):
        for k in range(1, n + 1):
            require(determinant([[a[i + j] for j in range(k)] for i in range(k)]) > 0, "positive Hankel minors")
    return (tuple(map(str, raw)), p, tuple(map(str, q)), str(base))


def audit_blocks():
    tested = 0
    for width in range(1, 4):
        for capacity in range(5):
            states = [s for s in product(range(capacity + 1), repeat=width) if sum(s) <= capacity]
            heights = [sum(s) for s in states]
            dp = [1] * len(states)
            w = [comb(j + width - 1, width - 1) for j in range(capacity + 1)]
            a = moments(w, 7)
            for k in range(7):
                require(sum(dp) == a[k], "uncompressed coordinate-state enumeration")
                tested += 1
                dp = [sum(dp[j] for j in range(len(states)) if heights[i] + heights[j] <= capacity)
                      for i in range(len(states))]
    return tested


def main():
    digest = sha256()
    rational = finite = 0
    for n in range(1, 6):
        for w in product((1, 2, 3), repeat=n):
            digest.update(repr(audit_vector(w)).encode())
            rational += 1
    for n in range(1, 9):
        for w in ([F(j + 1, j + 2) for j in range(n)],
                  [(-1) ** j * (j + 2) for j in range(n)],
                  [comb(j + 2, 2) for j in range(n)]):
            digest.update(repr(audit_vector(w)).encode())
            rational += 1
    for p, max_n in ((2, 6), (3, 5), (5, 3)):
        for n in range(1, max_n + 1):
            for w in product(range(1, p), repeat=n):
                digest.update(repr(audit_vector(w, p)).encode())
                finite += 1
    zeros = 0
    for raw in ([0], [1, 0], [0, 2, 3], [1, 2, 0, 4]):
        a, n = moments(raw, 2 * len(raw) + 2), len(raw)
        require(determinant([[a[i + j] for j in range(n)] for i in range(n)]) == 0, "zero-weight boundary")
        zeros += 1
    rejected = 0
    for raw, p in (([], None), ([0], None), ([1, 0, 2], None), ([1, 2], 4), ([1, 3], 3)):
        try:
            validate(raw, p)
        except ValueError:
            rejected += 1
    require(rejected == 5, "invalid inputs")
    # Mutation control compares a supplied denominator with its prescribed weights.
    q = newton_denominator([F(1), F(2), F(3)])
    q[1] += 1
    require(q != scale(jacobi_data([1, 2, 3])[2][-1], 1 / jacobi_data([1, 2, 3])[2][-1][0]), "wrong denominator control")
    result = dict(rational_weight_vectors=rational, finite_field_vectors=finite,
                  shifts_per_vector=4, coordinate_state_comparisons=audit_blocks(),
                  zero_weight_controls=zeros, invalid_inputs_rejected=rejected,
                  modified_denominator_detected=True, entry_digest=digest.hexdigest())
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if sys.argv[1:] == ["--check"]:
        require(encoded == Path(__file__).with_name("expected.json").read_text(), "expected output")
        print("PASS: Hankel products, minimal denominators, Jacobi recovery, and block counts")
    else:
        require(not sys.argv[1:], "usage: verify.py [--check]")
        print(encoded, end="")


if __name__ == "__main__":
    main()
