"""Exact reviewer check; imports no author module, certificate, or output."""
from collections import defaultdict, deque
from fractions import Fraction as Q
from functools import reduce
from itertools import combinations, permutations
from math import factorial, gcd, lcm
from pathlib import Path
import hashlib
import json
import sys

ALPHA = Q(5, 2)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def rising(m):
    value = Q(1)
    for j in range(m):
        value *= ALPHA + j
    return value


def parity(seq):
    return (-1) ** sum(seq[i] > seq[j] for i in range(len(seq))
                      for j in range(i + 1, len(seq)))


def matrix(k, correction=True):
    tuples = list(permutations(range(7), k))
    scale = {2: 35, 3: 315}[k]
    answer = []
    for x in tuples:
        row = []
        for y in tuples:
            aligned = all(x.index(a) == y.index(a) for a in set(x) & set(y))
            m = sum(a != b for a, b in zip(x, y))
            value = Q(scale, 1) / rising(m) if aligned else Q(0)
            if k == 3 and correction and set(x) == set(y):
                value += Q(63, 6) * (parity([x.index(a) for a in y]) - 1)
            require(value.denominator == 1, "matrix entry not integral")
            row.append(value.numerator)
        answer.append(row)
    require(all(answer[i][j] == answer[j][i] for i in range(len(tuples))
                for j in range(len(tuples))), "matrix not symmetric")
    return tuples, answer


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def apply(a, v):
    return [dot(row, v) for row in a]


def primitive(v):
    den = reduce(lcm, (x.denominator for x in v), 1)
    z = [int(x * den) for x in v]
    common = reduce(gcd, (abs(x) for x in z), 0)
    if not common:
        return z
    z = [x // common for x in z]
    if next(x for x in z if x) < 0:
        z = [-x for x in z]
    return z


def krylov_polynomial(a):
    """Derive a monic annihilator by an exact orthogonal cyclic basis."""
    size = len(a)
    v = [int(i == 0) for i in range(size)]
    basis, images, norms = [], [], []
    while any(v):
        require(len(basis) < 20, "Krylov safety cap: no truncated certificate")
        require(all(dot(v, u) == 0 for u in basis), "basis not orthogonal")
        basis.append(v)
        norms.append(dot(v, v))
        w = apply(a, v)
        images.append(w)
        projection = [Q(dot(u, w), n) for u, n in zip(basis, norms)]
        residual = [Q(w[i]) - sum(c * u[i] for c, u in zip(projection, basis))
                    for i in range(size)]
        v = primitive(residual)
    d = len(basis)
    h = [[dot(u, w) for w in images] for u in basis]
    require(all(h[i][j] == h[j][i] for i in range(d) for j in range(d)),
            "compressed form not symmetric")
    require(all(h[i][j] == 0 for i in range(d) for j in range(d)
                if abs(i - j) > 1), "Krylov form not tridiagonal")
    # Determinant recurrence for tI - diag(norms)^(-1) h.
    old, current = [Q(1)], [Q(1)]
    for i in range(d):
        diagonal = Q(h[i][i], norms[i])
        following = [Q(0)] * (len(current) + 1)
        for j, c in enumerate(current):
            following[j + 1] += c
            following[j] -= diagonal * c
        if i:
            cross = Q(h[i][i - 1] ** 2, norms[i] * norms[i - 1])
            for j, c in enumerate(old):
                following[j] -= cross * c
        old, current = current, following
    require(all(c.denominator == 1 for c in current), "nonintegral annihilator")
    poly = [c.numerator for c in current]
    require(len(poly) == d + 1 and poly[-1] == 1, "annihilator not monic")
    # A separate Horner evaluation checks the derived polynomial on e_0.
    value = [0] * size
    for c in reversed(poly):
        value = apply(a, value)
        value[0] += c
    require(not any(value), "derived polynomial does not annihilate seed")
    alternating = [(-1) ** (d + j) * c for j, c in enumerate(poly)]
    return {"degree": d, "coefficients_ascending": poly,
            "alternating_coefficients_nonnegative": all(c >= 0 for c in alternating),
            "seed_identity_verified": True,
            "basis_sha256": digest(basis), "largest_basis_entry_bits":
            max(abs(x).bit_length() for v in basis for x in v)}


def symmetry(tuples, a):
    """Check every entry under generators and transitivity on all indices."""
    index = {t: i for i, t in enumerate(tuples)}
    actions = []
    for swap in range(6):
        def image(x):
            return swap + 1 if x == swap else swap if x == swap + 1 else x
        action = [index[tuple(image(x) for x in t)] for t in tuples]
        require(all(a[action[i]][action[j]] == a[i][j]
                    for i in range(len(tuples)) for j in range(len(tuples))),
                "generator equivariance fails")
        actions.append(action)
    seen, queue = {0}, deque([0])
    while queue:
        i = queue.popleft()
        for action in actions:
            j = action[i]
            if j not in seen:
                seen.add(j)
                queue.append(j)
    require(len(seen) == len(tuples), "label action not transitive")
    return {"generators": len(actions), "entry_comparisons": 6 * len(tuples) ** 2,
            "seed_orbit_size": len(seen)}


def monomial(pairs):
    return tuple(sorted(tuple(sorted(e)) for e in pairs))


def matching_polynomial(k):
    answer = defaultdict(Q)
    def visit(labels, edges, loops):
        if len(edges) + len(loops) == k:
            key = monomial(edges + [(i, i) for i in loops])
            answer[key] += 1 / (Q(2) ** len(loops) * rising(len(edges)))
            return
        if not labels:
            return
        i, tail = labels[0], labels[1:]
        visit(tail, edges, loops)
        visit(tail, edges, loops + [i])
        for j in tail:
            visit([v for v in tail if v != j], edges + [(i, j)], loops)
    visit(list(range(7)), [], [])
    return dict(answer)


def trace_polynomial(k, tuples, a):
    numerator = defaultdict(int)
    for i, x in enumerate(tuples):
        for j, y in enumerate(tuples):
            numerator[monomial(list(zip(x, y)))] += a[i][j]
    divisor = 280 if k == 2 else 15120
    if k == 3:
        for triple in combinations(range(7), 3):
            for i in triple:
                j, l = (v for v in triple if v != i)
                numerator[monomial([(i, i), (j, l), (j, l)])] += 126
    return {key: Q(value, divisor) for key, value in numerator.items() if value}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest()


def run():
    folder = Path(__file__).resolve().parent
    inputs = json.loads((folder / "INPUTS.json").read_text())
    target = inputs["target_proof"]
    require(hashlib.sha256((folder / target["path"]).read_bytes()).hexdigest()
            == target["sha256"], "reviewed source changed; scope needs a fresh review")
    report = {"method": "transitive exact Krylov annihilator; no supplied eigenvalues",
              "alpha": "5/2", "matrices": []}
    for k in (2, 3):
        tuples, a = matrix(k)
        group = symmetry(tuples, a)
        certificate = krylov_polynomial(a)
        require(certificate["alternating_coefficients_nonnegative"], "PSD sign fails")
        left, right = matching_polynomial(k), trace_polynomial(k, tuples, a)
        require(left == right, "universal Gram coefficient identity fails")
        bad = [row[:] for row in a]
        bad[0][0] += 1
        try:
            symmetry(tuples, bad)
        except RuntimeError as error:
            require(str(error) == "generator equivariance fails", "wrong rejection")
        else:
            raise RuntimeError("symmetry corruption not rejected")
        report["matrices"].append({"k": k, "order": len(tuples),
            "matrix_sha256": digest(a), "symmetry": group,
            "krylov": certificate, "matching_monomials": len(left),
            "all_gram_coefficients_verified": True,
            "single_diagonal_symmetry_rejection": True})
    _, uncorrected = matrix(3, correction=False)
    negative = krylov_polynomial(uncorrected)
    require(not negative["alternating_coefficients_nonnegative"],
            "uncorrected-matrix rejection unexpectedly absent")
    report["uncorrected_matrix"] = negative
    report["rising_factorial"] = str(rising(7))
    report["status"] = "R5_SEVEN_FACTOR_INDEPENDENT_PSD_REVIEW_PASS"
    return report


if __name__ == "__main__":
    result = run()
    expected = Path(__file__).with_name("EXPECTED.json")
    if sys.argv[1:] == ["--record"]:
        require(not expected.exists(), "refuse to replace existing expected record")
        expected.write_text(json.dumps(result, indent=2) + "\n")
    else:
        require(not sys.argv[1:], "usage: independent_check.py [--record]")
        require(result == json.loads(expected.read_text()), "frozen record mismatch")
    print(result["status"])
    print("record_sha256", digest(result))
    print("matrix_orders", [x["order"] for x in result["matrices"]],
          "cyclic_dimensions", [x["krylov"]["degree"] for x in result["matrices"]])
