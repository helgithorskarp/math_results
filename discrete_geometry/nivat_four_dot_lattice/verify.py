"""Exact finite corroboration; Python 3.11+, standard library only.

Finite quotients below check window languages, not infinite nonperiodicity.
The latter has a two-point geometric certificate in PROOF.md.
"""
from collections import Counter
from itertools import product
from math import gcd
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def scale(k, u):
    return (k * u[0], k * u[1])


def det(u, v):
    return u[0] * v[1] - u[1] * v[0]


def coords(z, u, v):
    d = det(u, v)
    require(d != 0, "dependent directions")
    a, b = det(z, v), det(u, z)
    if a % d or b % d:
        return None
    return (a // d, b // d)


def point(a, b, u, v):
    return add(scale(a, u), scale(b, v))


def coset_representatives(u, v):
    """Lattice quotient by exact Cramer numerators modulo determinant."""
    q = abs(det(u, v))
    require(q > 0, "dependent directions")
    reps = {}
    # q*Z^2 is contained in L by the adjugate identity.
    for x, y in product(range(q), repeat=2):
        key = (det((x, y), v) % q, det(u, (x, y)) % q)
        reps.setdefault(key, (x, y))
    require(len(reps) == q, "lattice index")
    return sorted(reps.values())


def validate(u, v, t):
    require(abs(det(u, v)) > 1, "requires proper direction lattice")
    require(coords(t, u, v) is None, "cosets must be distinct")


def on_progression(z, u):
    if det(u, z):
        return False
    i = 0 if u[0] else 1
    return z[i] % u[i] == 0


def value(z, u, v, t):
    return int(on_progression(z, u)) ^ int(on_progression(sub(z, t), v))


def period_separator(w, u, v, t):
    """For any nonzero proposed period, one of two support points refutes it."""
    require(w != (0, 0), "zero is always a period")
    if det(u, w):
        candidates = [(0, 0), u]
    else:
        candidates = [t, add(t, v)]
    for z in candidates:
        if value(z, u, v, t) != value(add(z, w), u, v, t):
            return z
    raise ValueError("geometric period separator failed")


def torus_value(z, u, v, t, N):
    """Periodized union: coset L has one u-row; coset t+L has one v-column."""
    a = coords(z, u, v)
    b = coords(sub(z, t), u, v)
    return int(a is not None and a[1] % N == 0) ^ \
        int(b is not None and b[0] % N == 0)


def quotient_language(A, u, v, t):
    """Evaluate every translation in Z^2/(N L) in physical coordinates."""
    validate(u, v, t)
    A = sorted(A)
    require(A and len(A) == len(set(A)), "window must be a nonempty set")
    span = max(max(x[i] for x in A) - min(x[i] for x in A) for i in (0, 1))
    N = span + 2
    D = [point(a, b, u, v) for a, b in A]
    result = set()
    for r in coset_representatives(u, v):
        for a, b in product(range(N), repeat=2):
            shift = add(r, point(a, b, u, v))
            mask = sum(torus_value(add(shift, z), u, v, t, N) << i
                       for i, z in enumerate(D))
            result.add(mask)
    return result


def predicted_language(A):
    """Incidence description, independent of lattice membership implementation."""
    A = sorted(A)
    rows, cols = {}, {}
    for k, (a, b) in enumerate(A):
        rows[b] = rows.get(b, 0) | (1 << k)
        cols[a] = cols.get(a, 0) | (1 << k)
    return {0} | set(rows.values()) | set(cols.values())


def statistics(A):
    rows = Counter(b for a, b in A)
    cols = Counter(a for a, b in A)
    isolated = sum(rows[b] == cols[a] == 1 for a, b in A)
    return len(rows), len(cols), isolated


def check_formula(A, language):
    r, s, i = statistics(A)
    require(len(language) == 1 + r + s - i, "window complexity formula")
    require(language == predicted_language(A), "complete pattern set")


def multiply(p, q):
    """Laurent polynomial product over F2, represented by exponent sets."""
    out = set()
    for a in p:
        for b in q:
            z = add(a, b)
            if z in out:
                out.remove(z)
            else:
                out.add(z)
    return out


def annihilates_at(p, z, u, v, t):
    return sum(value(sub(z, a), u, v, t) for a in p) % 2 == 0


def main():
    # Different indices, signs, shears, primitive and nonprimitive directions.
    bases = [((1, 0), (1, 2)), ((1, 0), (0, 3)),
             ((2, 0), (0, 2)), ((2, 1), (1, 2)),
             ((1, 2), (1, 0)), ((-1, 2), (2, 1)),
             ((2, 0), (1, 3)), ((3, -1), (1, 2))]
    fixtures = []
    for u, v in bases:
        reps = coset_representatives(u, v)
        t = next(z for z in reps if coords(z, u, v) is None)
        validate(u, v, t)
        constraints = multiply({(0, 0), u}, {(0, 0), v})
        annihilator_checks = 0
        for z in product(range(-8, 9), repeat=2):
            require(annihilates_at(constraints, z, u, v, t), "four-dot constraint")
            annihilator_checks += 1
        for w in product(range(-8, 9), repeat=2):
            if w != (0, 0):
                period_separator(w, u, v, t)
        shapes = {
            "six_site": list(product(range(3), range(2))),
            "eight_site_k24": list(product(range(4), range(2))),
            "eight_site_k33_minus_edge":
                [z for z in product(range(3), repeat=2) if z != (2, 2)],
            "isolated_points": [(0, 0), (2, 2), (4, 4)],
            "square_plus_isolated": [(0, 0), (0, 1), (1, 0), (1, 1), (3, 3)],
            "negative_coordinates": [(-3, -2), (-2, -2), (-3, 0), (-2, 0), (2, 3)],
        }
        summary = {}
        for name, A in shapes.items():
            language = quotient_language(A, u, v, t)
            check_formula(A, language)
            translated = [(a - 7, b + 4) for a, b in A]
            require(quotient_language(translated, u, v, t) == language,
                    "translation invariance")
            summary[name] = {"sites": len(A), "patterns": len(language)}
        fixtures.append({"u": u, "v": v, "t": t, "index": abs(det(u, v)),
                         "window_checks": summary, "period_separators": 288,
                         "annihilator_checks": annihilator_checks})

    # All nonempty subsets of a 3x3 grid: compare every finite quotient pattern.
    u, v, t = (1, 0), (1, 2), (0, 1)
    grid = list(product(range(3), repeat=2))
    digest = hashlib.sha256()
    quotient_windows = 0
    for mask in range(1, 1 << len(grid)):
        A = [z for i, z in enumerate(grid) if mask >> i & 1]
        language = quotient_language(A, u, v, t)
        check_formula(A, language)
        digest.update(json.dumps([A, sorted(language)], separators=(",", ":")).encode())
        quotient_windows += 1

    # Independent incidence-graph audit of the sharp six/eight-site boundaries.
    grid = list(product(range(4), range(3)))
    by_size = Counter()
    low_six = strict_eight = 0
    for mask in range(1, 1 << len(grid)):
        A = [z for i, z in enumerate(grid) if mask >> i & 1]
        language = predicted_language(A)
        check_formula(A, language)
        r, s, i = statistics(A)
        n, P = len(A), len(language)
        by_size[n] += 1
        if n <= 5:
            require(P > n, "small low-complexity window")
        if n <= 7:
            require(P >= n, "small strictly low-complexity window")
        if n == 6 and P <= n:
            require(i == 0 and sorted((r, s)) == [2, 3] and n == r * s,
                    "six-site equality classification")
            low_six += 1
        if n == 8 and P < n:
            require(i == 0 and (sorted((r, s)) == [2, 4] or (r, s) == (3, 3)),
                    "eight-site strict classification")
            strict_eight += 1

    # A full-support-lattice polynomial still inherits a bad determinant-two pair.
    directions = [(1, 0), (1, 2), (0, 1)]
    f = {(0, 0)}
    for w in directions:
        require(gcd(abs(w[0]), abs(w[1])) == 1, "nonprimitive binomial")
        f = multiply(f, {(0, 0), w})
    require(len(f) == 8 and {(0, 0), (1, 0), (0, 1)} <= f, "full support lattice")
    require(all(det(a, b) for j, a in enumerate(directions) for b in directions[j+1:]),
            "repeated binomial direction")
    for z in product(range(-10, 11), repeat=2):
        require(annihilates_at(f, z, u, v, t), "inherited annihilator")

    # Hypotheses that cannot be silently dropped.
    rejected = 0
    for a, b, c in [((1, 0), (0, 1), (1, 1)),
                    ((1, 0), (1, 2), (2, 2)),
                    ((1, 0), (2, 0), (0, 1))]:
        try:
            validate(a, b, c)
        except ValueError:
            rejected += 1
    require(rejected == 3, "invalid construction accepted")
    print(json.dumps({
        "schema": 1,
        "fixtures": fixtures,
        "complete_3x3_window_languages": quotient_windows,
        "window_language_sha256": digest.hexdigest(),
        "incidence_windows_by_size": dict(sorted(by_size.items())),
        "six_site_low_windows_in_4x3": low_six,
        "eight_site_strict_windows_in_4x3": strict_eight,
        "full_lattice_polynomial_support": sorted(f),
        "full_lattice_polynomial_annihilator_checks": 441,
        "negative_controls": rejected,
        "trust_boundary": "Infinite nonperiodicity and universal classification use the written proof; finite quotients check languages only."
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
