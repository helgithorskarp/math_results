"""Direct multivariate-polynomial audit of the new all-core margin transfers.

Six-tammes-2, researcher. Standard library only. This uses explicit Gram
products, generic binomial Bernstein conversion, and literal substitutions.
It imports no production or prerequisite algebra/checking function. The
complete parent pair graphs/clique proofs are replayed separately by check.py;
this audit independently reconstructs the cover and all changed inequalities.
Same author, not independent mathematical peer review.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb
import hashlib, json, sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ZERO = (0, 0, 0, 0, 0)
NAMES = {"lower": "tammes15_octagon_model2_lower_strip_exclusion",
         "upper": "tammes15_octagon_model2_extension_exclusion"}
DELTA = Q(1, 156250)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def constant(c):
    return {ZERO: Q(c)} if c else {}


def variable(k):
    e = [0] * 5
    e[k] = 1
    return {tuple(e): Q(1)}


def add(*polys):
    result = {}
    for p in polys:
        for e, c in p.items():
            result[e] = result.get(e, Q(0)) + c
    return {e: c for e, c in result.items() if c}


def scale(p, c):
    return {e: a * c for e, a in p.items() if a * c}


def mul(p, q):
    result = {}
    for e, c in p.items():
        for f, d in q.items():
            g = tuple(a + b for a, b in zip(e, f))
            result[g] = result.get(g, Q(0)) + c * d
    return {e: c for e, c in result.items() if c}


def power(p, n):
    result = constant(1)
    for _ in range(n):
        result = mul(result, p)
    return result


t, u, v, U, V = [variable(i) for i in range(5)]
one = constant(1)
s = add(one, t)
D = power(s, 3)
q2s = scale(mul(t, power(s, 2)), 2)
q4s = scale(mul(power(t, 2), s), 4)
q8 = scale(power(t, 3), 8)
points = {
    0: [add(q4s, scale(D, -1)), scale(q2s, -1), add(q2s, q4s)],
    1: [q2s, scale(D, -1), q2s], 2: [D, {}, {}],
    3: [q2s, q2s, scale(D, -1)],
    4: [add(q8, q4s, scale(q2s, -1)), add(q8, scale(q4s, 2), scale(D, -1)),
        scale(add(q2s, q4s), -1)],
    5: [add(q4s, scale(D, -1)), add(q2s, q4s), scale(q2s, -1)],
    6: [{}, D, {}], 7: [{}, {}, D],
}


def metric(a, b):
    return add(mul(add(one, scale(t, -1)), add(*(mul(x, y) for x, y in zip(a, b)))),
               mul(t, mul(add(*a), add(*b))))


def chart(a, b):
    radius = add(one, mul(add(one, scale(power(t, 2), -1)),
                         add(power(a, 2), power(b, 2))),
                 scale(mul(mul(t, add(one, scale(t, -1))), mul(a, b)), 2))
    numerator = [add(radius, constant(-2), scale(mul(t, add(a, b)), -2)),
                 scale(a, 2), scale(b, 2)]
    return radius, numerator


radius, Y = chart(u, v)
other_radius, other_Y = chart(U, V)
forms = [add(metric(points[i], Y), scale(mul(mul(t, D), radius), -1))
         for i in range(8)]
other_forms = [add(metric(points[i], other_Y), scale(mul(mul(t, D), other_radius), -1))
               for i in range(8)]
pair = add(mul(radius, other_radius),
           scale(add(mul(s, add(power(add(u, scale(U, -1)), 2),
                                power(add(v, scale(V, -1)), 2))),
                     scale(mul(t, mul(add(u, scale(U, -1)),
                                     add(v, scale(V, -1)))), 2)), -2))


def beta(p, k, degree, lo, hi):
    return sum((Q(comb(p, j) * comb(k, j), comb(degree, j))
                * lo ** (p - j) * (hi - lo) ** j
                for j in range(min(p, k) + 1)), Q(0))


def cell_bounds(cell):
    d, i, j = cell
    need(type(d) is int and type(i) is int and type(j) is int
         and 0 <= d <= 12 and 0 <= i < 2 ** d and 0 <= j < 2 ** d,
         "canonical cell")
    h = Q(8, 2 ** d)
    return ((-4 + i * h, -4 + (i + 1) * h),
            (-4 + j * h, -4 + (j + 1) * h))


def evaluation(p, values):
    return sum((c * product_value(e, values) for e, c in p.items()), Q(0))


def product_value(e, values):
    result = Q(1)
    for power_, value in zip(e, values):
        result *= value ** power_
    return result


def denominator_bound(cell, lo, hi):
    axes = cell_bounds(cell)
    return (1 + hi) ** 3 * max(evaluation(radius, [lo, x, y, 0, 0])
                               for x, y in product(*axes))


def t_coefficients(lo, hi):
    # Independently convert the explicitly multiplied Fi polynomials first
    # in t, leaving the ordinary powers of u,v.
    degree = max(e[0] for p in forms for e in p)
    result = []
    for p in forms:
        rows = []
        for k in range(degree + 1):
            row = {}
            for e, c in p.items():
                key = e[1:3]
                row[key] = row.get(key, Q(0)) + c * beta(e[0], k, degree, lo, hi)
            rows.append({e: c for e, c in row.items() if c})
        result.append(rows)
    return result


def bernstein_margin(rows, cell):
    axes = cell_bounds(cell)
    tables = [{(p, k): beta(p, k, 2, *axis)
               for p in range(3) for k in range(3)} for axis in axes]
    minimum = None
    for row in rows:
        for i, j in product(range(3), repeat=2):
            value = sum((c * tables[0][p, i] * tables[1][q, j]
                         for (p, q), c in row.items()), Q(0))
            if value <= 0:
                return None
            minimum = value if minimum is None else min(minimum, value)
    return minimum


def substitute(p, axes):
    powers = {(i, 0): one for i in range(5)}
    for i in range(5):
        max_power = max((e[i] for e in p), default=0)
        for n in range(1, max_power + 1):
            powers[i, n] = mul(powers[i, n - 1], axes[i])
    result = {}
    for e, coefficient in p.items():
        term = constant(coefficient)
        for i, n in enumerate(e):
            term = mul(term, powers[i, n])
        result = add(result, term)
    return result


def affine_row(p):
    a = [Q(0)] * 5
    error = Q(0)
    for e, c in p.items():
        if sum(e) == 1:
            a[e.index(1)] += c
        elif sum(e) >= 2:
            error += abs(c)
    return a, error - p.get(ZERO, Q(0))


def dual_record(cert, tag, lo, hi):
    cells = [tuple(cert["cell"])] if tag == "single" else list(map(tuple, cert["cells"]))
    axes = [add(constant((lo + hi) / 2), scale(t, (hi - lo) / 2))]
    for cell, indices in zip(cells, ((1, 2), (3, 4))):
        for (low, high), index in zip(cell_bounds(cell), indices):
            axes.append(add(constant((low + high) / 2), scale(variable(index), (high - low) / 2)))
    nvars = len(axes)
    axes += [U, V] if nvars == 3 else []
    polynomials = forms if tag == "single" else forms + other_forms + [pair]
    rows = [affine_row(substitute(p, axes)) for p in polynomials]
    for j in range(nvars):
        for sign in (-1, 1):
            a = [Q(0)] * 5
            a[j] = sign
            rows.append((a, Q(1)))
    support, weights = cert["support"], list(map(Q, cert["weights"]))
    need(support and len(support) == len(set(support)) == len(weights), "audit dual support")
    need(all(type(k) is int and 0 <= k < len(rows) for k in support), "audit dual indices")
    need(all(w >= 0 for w in weights) and sum(weights) == 1, "audit nonnegative weights")
    need(all(sum(w * rows[k][0][j] for k, w in zip(support, weights)) == 0
             for j in range(5)), "audit literal affine cancellation")
    original = sum(w * rows[k][1] for k, w in zip(support, weights))
    need(original == Q(cert["negative_rhs"]) and original < 0, "audit original RHS")
    factors = [denominator_bound(c, lo, hi) for c in cells]
    weight = sum((w * factors[k // 8] for k, w in zip(support, weights)
                  if k < 8 * len(cells)), Q(0))
    relaxed = original + DELTA * weight
    need(relaxed < 0, "audit all-core relaxed RHS")
    return [tag, [list(c) for c in cells], str(original), str(weight), str(relaxed)]


def audit_strip(kind, root):
    config = json.loads((HERE / "certificate.json").read_text())
    base = root / NAMES[kind]
    for name, expected in config["prerequisites"][kind]["files_sha256"].items():
        need(Path(name).name == name and hashlib.sha256((base / name).read_bytes()).hexdigest() == expected,
             "audit prerequisite pin")
    data = json.loads((base / "certificate.json").read_text())
    lo, hi = [Q(*z) for z in data["interval"]]
    need(16 * (1 - hi) * (1 - hi - DELTA) ** 2 > 1, "audit relaxed chart coverage")
    # Explicit source geometry, independently of the production kernels.
    need(metric(Y, Y) == mul(radius, radius), "audit chart norm identity")
    need(add(metric(Y, other_Y), scale(mul(t, mul(radius, other_radius)), -1))
         == mul(add(one, scale(t, -1)), pair), "audit pair identity")
    for p in points.values():
        need(metric(p, p) == mul(D, D), "audit core unit identity")
    contacts = []
    for i, j in combinations(range(8), 2):
        if metric(points[i], points[j]) == mul(t, mul(D, D)):
            contacts.append([i, j])
    need(contacts == config["prescribed_edges"], "audit full thirteen-contact identities")
    tc = t_coefficients(lo, hi)
    leaves = set(map(tuple, data["remaining_cover_cells"]))
    refined = set(map(tuple, data["refined_cells"]))
    ancestors = set()
    for d, i, j in leaves | refined:
        while d:
            d, i, j = d - 1, i // 2, j // 2
            ancestors.add((d, i, j))
    need(not (leaves & ancestors) and not (leaves & refined), "audit cover frontier")
    empty = [tuple(c["cell"]) for c in data.get("single_cells", [])]
    records, found, visited = [], set(), set()

    def under(c, p):
        d, i, j = c
        e, a, b = p
        return d >= e and i // 2 ** (d - e) == a and j // 2 ** (d - e) == b

    def cover(cell):
        visited.add(cell)
        if cell in leaves:
            found.add(cell)
            return
        split = cell in ancestors or cell in refined
        if not split and any(under(cell, p) for p in empty):
            return
        if not split:
            for label, rows in enumerate(tc):
                margin = bernstein_margin(rows, cell)
                if margin is not None:
                    factor = denominator_bound(cell, lo, hi)
                    relaxed = margin - DELTA * factor
                    need(relaxed > 0, "audit relaxed cover margin")
                    records.append([list(cell), label, str(margin), str(factor), str(relaxed)])
                    return
            need(cell[0] < 5, "audit uncovered square region")
        d, i, j = cell
        for a, b in product((0, 1), repeat=2):
            cover((d + 1, 2 * i + a, 2 * j + b))

    cover((0, 0, 0))
    need(found == leaves and refined <= visited, "audit complete square cover")
    duals = [dual_record(c, tag, lo, hi)
             for tag, key in (("single", "single_cells"), ("pair", "conditioned_pairs"))
             for c in data.get(key, [])]
    result = {"strip": kind, "bernstein_discards_transferred": len(records),
              "duals_transferred": len(duals),
              "bernstein_transfer_sha256": digest(records), "dual_transfer_sha256": digest(duals)}
    primary = next(s for s in json.loads((HERE / "EXPECTED.json").read_text())["strips"]
                   if s["strip"] == kind)
    need(all(primary[k] == v for k, v in result.items()), "entry-level new transfer agreement")
    return result


def main():
    root = Path(sys.argv[sys.argv.index("--prerequisite-root") + 1]).resolve() \
        if "--prerequisite-root" in sys.argv else ROOT
    result = {"agent": "six-tammes-2", "role": "researcher", "status": "AUDIT_VERIFIED",
              "strips": [audit_strip(kind, root) for kind in ("lower", "upper")],
              "independent_peer_review": "pending"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
