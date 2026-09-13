#!/usr/bin/env python3
"""Definition-level audit of the homogeneous A5 binomial-pencil theorem.

No target or ancestor module is imported.  The checker reconstructs F4,
Eisenstein row classes, all A5 norm polynomials, the pencil/anchor interface,
collision quotients, strict unit graphs, and positional colourings.  It also
counts every square-free fibre after eliminating x (the target eliminates y),
using reviewer-written quotient-field arithmetic.
"""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from itertools import combinations, product
import hashlib
import json
from math import gcd, prod
from pathlib import Path

import sympy as sp
from flint import fmpq, fmpq_poly


UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
DIGITS = ((0, 0), (1, 0), (0, 1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def f4_mul(a, b):
    """Multiply bit-polynomials modulo t^2+t+1."""
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def f4_normalize(vector):
    pivot = next(x for x in vector if x)
    inverse = next(x for x in (1, 2, 3) if f4_mul(x, pivot) == 1)
    return tuple(f4_mul(inverse, x) for x in vector)


def f4_affine_canonical(vector, constant):
    pivot = next(x for x in vector if x)
    inverse = next(x for x in (1, 2, 3) if f4_mul(x, pivot) == 1)
    return tuple(f4_mul(inverse, x) for x in vector), f4_mul(inverse, constant)


def f4_subspaces():
    points = sorted({f4_normalize(v) for v in product(range(4), repeat=4) if any(v)})
    require(len(points) == 85, "P3(F4) point count")
    spaces = set()
    for left, right in combinations(points, 2):
        line = frozenset(
            f4_normalize(tuple(f4_mul(a, x) ^ f4_mul(b, y)
                               for x, y in zip(left, right)))
            for a, b in ((1, 0), (0, 1), (1, 1), (1, 2), (1, 3))
        )
        if len(line) == 5:
            spaces.add(line)
    require(len(spaces) == 357, "Gaussian-binomial two-space count")
    allowed = {space for space in spaces
               if min(sum(bool(x) for x in row) for row in space) >= 2}
    three = {space for space in allowed
             if any(not any(row[k] for row in space) for k in range(4))}
    no_binomial = {space for space in allowed
                   if all(sum(bool(x) for x in row) >= 3 for row in space)}
    binomial = allowed - three - no_binomial
    require((len(allowed), len(three), len(no_binomial), len(binomial)) == (279, 36, 54, 189),
            "complete disjoint homogeneous-pencil classification")
    profiles = Counter(tuple(sorted(sum(bool(x) for x in row) for row in space))
                       for space in binomial)
    require(profiles == Counter({(2, 3, 3, 4, 4): 162, (2, 2, 4, 4, 4): 27}),
            "binomial support profiles")
    return spaces, allowed, three, no_binomial, sorted(tuple(sorted(s)) for s in binomial)


def eisenstein_mul(left, right):
    """Multiply a+b*omega with omega^2=omega-1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def row_canonical(row):
    return min(tuple(eisenstein_mul(unit, x) for x in row) for unit in UNITS)


def poly_add(left, right, scale=1):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, 0) + scale * coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def poly_mul(left, right):
    out = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            key = i + k, j + ell
            out[key] = out.get(key, 0) + a * b
    return {key: value for key, value in out.items() if value}


def poly_scale(poly, scalar):
    return {key: scalar * value for key, value in poly.items() if scalar * value}


def primitive(poly):
    if not poly:
        return ()
    divisor = 0
    for coefficient in poly.values():
        divisor = gcd(divisor, coefficient)
    if poly[max(poly)] < 0:
        divisor = -divisor
    return tuple((i, j, coefficient // divisor)
                 for (i, j), coefficient in sorted(poly.items()))


def z_powers():
    one = {(0, 0): 1}
    x = {(1, 0): 1}
    y = {(0, 1): 1}
    powers = [(one, {})]
    for _ in range(4):
        real, imag = powers[-1]
        powers.append((poly_add(poly_mul(real, x), poly_mul(imag, y), -3),
                       poly_add(poly_mul(real, y), poly_mul(imag, x))))
    return powers


Z_POWERS = z_powers()


def norm_event(row):
    """Return primitive polynomial 4*(|sum row[k] z^k|^2-1)."""
    real, imag = {}, {}
    for (a, b), (zr, zi) in zip(row, Z_POWERS):
        real = poly_add(real, poly_add(poly_scale(zr, 2 * a + b),
                                      poly_scale(zi, -3 * b)))
        imag = poly_add(imag, poly_add(poly_scale(zi, 2 * a + b),
                                      poly_scale(zr, b)))
    squared = poly_add(poly_mul(real, real), poly_mul(imag, imag), 3)
    return primitive(poly_add(squared, {(0, 0): 4}, -1))


def make_inventory():
    exact_digits = ((0, 0),) + UNITS
    rows = sorted({row_canonical(row) for row in product(exact_digits, repeat=5)
                   if any(x != (0, 0) for x in row)})
    require(len(rows) == 2801, "Eisenstein row quotient")
    circle = primitive({(2, 0): 1, (0, 2): 3, (0, 0): -1})
    events = []
    for row in rows:
        support = [i for i, x in enumerate(row) if x != (0, 0)]
        raw = norm_event(row)
        event = (None if support[0] == 0 else circle) if len(support) == 1 else raw
        events.append((raw, event))
    factors = sorted({event for raw, event in events if event is not None})
    require(len(factors) == 2797, "distinct A5 event factors")
    require(digest(factors) == "85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9",
            "independent factor-inventory hash")
    factor_id = {factor: i for i, factor in enumerate(factors)}
    buckets = defaultdict(list)
    for row, (raw, event) in zip(rows, events):
        if event is None or sum(x != (0, 0) for x in row) == 1:
            continue
        residue = lambda pair: (pair[0] % 2) + 2 * (pair[1] % 2)
        signature = f4_affine_canonical(tuple(residue(pair) for pair in row[1:]),
                                        residue(row[0]))
        buckets[signature].append(factor_id[event])
    for key in buckets:
        buckets[key].sort()
    require(len(buckets) == 336, "homogeneous nonmonomial event buckets")
    return rows, events, factors, buckets


def load_pencils(path):
    raw = json.loads(Path(path).read_text())
    pencils = []
    for index, records in raw:
        pencil = tuple(tuple(row) for row, constant in records)
        require(all(constant == 0 for row, constant in records), "homogeneous supplied pencil")
        pencils.append((index, pencil))
    require([index for index, pencil in pencils] == list(range(189)), "canonical pencil indices")
    require(len({pencil for index, pencil in pencils}) == 189, "supplied pencil uniqueness")
    return pencils


def pair_envelope(pencils, buckets):
    selected = []
    for index, pencil in pencils:
        domains = sorted((buckets[(row, 0)] for row in pencil),
                         key=lambda values: (len(values), values))
        profile = sorted(map(len, domains))
        require(profile in ([2, 4, 4, 8, 8], [2, 2, 8, 8, 8]), "lift-bucket profile")
        pairs = sorted({tuple(sorted(pair)) for pair in product(*domains[:2])})
        selected.append((index, domains, pairs))
    pairs = sorted({pair for index, domains, pp in selected for pair in pp})
    require(len(pairs) == 1404, "anchor-pair envelope")
    return selected, pairs


def flint_poly(values):
    return fmpq_poly([fmpq(str(value)) for value in values])


def evaluator(component):
    q, x, y = (flint_poly(component[key]) for key in ("q", "x", "y"))
    x %= q
    y %= q
    one, zero = fmpq_poly([1]), fmpq_poly([])
    xp, yp = [one], [one]
    for _ in range(8):
        xp.append(xp[-1] * x % q)
        yp.append(yp[-1] * y % q)
    monomials = {(i, j): xp[i] * yp[j] % q for i in range(9) for j in range(9 - i)}

    def vanishes(sparse):
        total = zero
        for i, j, coefficient in sparse:
            total += coefficient * monomials[i, j]
        return total % q == zero
    return vanishes


def real_roots(component):
    s = sp.Symbol("s")
    q = sp.Poly(sum(sp.Rational(value) * s**i
                    for i, value in enumerate(component["q"])), s, domain=sp.QQ)
    require(q.is_irreducible, "component polynomial irreducibility")
    return int(q.count_roots(-sp.oo, sp.oo))


def field_pair_mul(left, right, q):
    a, b = left
    c, d = right
    return ((a * c - 3 * b * d) % q, (a * d + b * c) % q)


def physical_points(component):
    q = flint_poly(component["q"])
    x, y = flint_poly(component["x"]) % q, flint_poly(component["y"]) % q
    zero, one = fmpq_poly([]), fmpq_poly([1])
    half = fmpq_poly([fmpq(1, 2)])
    powers = [(one, zero)]
    for _ in range(4):
        powers.append(field_pair_mul(powers[-1], (x, y), q))
    digit_values = ((zero, zero), (one, zero), (half, half))
    terms = [[field_pair_mul(digit, power, q) for digit in digit_values]
             for power in powers]
    points, lookup, labels = [], {}, []
    for word in product(range(3), repeat=5):
        real, imag = zero, zero
        for position, digit in enumerate(word):
            real += terms[position][digit][0]
            imag += terms[position][digit][1]
        key = (tuple(str(c) for c in real.coeffs()), tuple(str(c) for c in imag.coeffs()))
        if key not in lookup:
            lookup[key] = len(points)
            points.append((real, imag))
        labels.append(lookup[key])
    return points, labels


def row_edgegroups():
    words = list(product(range(3), repeat=5))
    groups = defaultdict(list)
    for right in range(len(words)):
        for left in range(right):
            row = row_canonical(tuple((DIGITS[a][0] - DIGITS[b][0],
                                       DIGITS[a][1] - DIGITS[b][1])
                                      for a, b in zip(words[left], words[right])))
            groups[row].append((left, right))
    require(sum(map(len, groups.values())) == 29403 and len(groups) == 2801,
            "complete label-pair partition")
    return groups


def component_audit(component, factors, raw_by_row, edgegroups):
    field = {key: component[key] for key in ("q", "x", "y")}
    require(component["key"] == digest(field), "component key")
    degree = len(component["q"]) - 1
    q = flint_poly(component["q"])
    x, y = flint_poly(component["x"]) % q, flint_poly(component["y"]) % q
    parameter = fmpq_poly([0, 1])
    u = (x + 2 * y) % q
    require((degree == 1 and component["q"] == ["0", "1"]
             and len(component["x"]) == len(component["y"]) == 1)
            or (degree > 1 and (u == parameter or (u.degree() <= 0 and y == parameter))),
            "canonical separating coordinate")
    nreal = real_roots(component)
    require(component["real_embeddings"] == nreal, "real-root count")
    ev = evaluator(component)
    active = [i for i, factor in enumerate(factors) if ev(factor)]
    require(component["active_curves"] == active, "active-curve list")
    result = {"key": component["key"], "nreal": nreal, "degree": degree, "active": len(active)}
    if not nreal:
        return result
    points, labels = physical_points(component)
    require(component["point_count"] == len(points), "physical point count")
    require(component["label_map_sha256"] == digest(labels), "collision quotient hash")
    edges = set()
    for row, pairs in edgegroups.items():
        if not ev(raw_by_row[row]):
            continue
        for left, right in pairs:
            a, b = labels[left], labels[right]
            require(a != b, "collapsed unit loop")
            edges.add(tuple(sorted((a, b))))
    edge_list = [list(edge) for edge in sorted(edges)]
    require(component["edge_count"] == len(edge_list), "strict unit-edge count")
    require(component["edge_sha256"] == digest(edge_list), "strict unit-edge hash")
    weights = component["colour_weights"]
    require(len(weights) == 5 and weights[0] == 1
            and all(type(w) is int and w in (0, 1, 2) for w in weights),
            "positional colour weights")
    colours = [None] * len(points)
    for word, vertex in zip(product(range(3), repeat=5), labels):
        colour = sum(w * digit for w, digit in zip(weights, word)) % 3
        require(colours[vertex] is None or colours[vertex] == colour,
                "colour descends through collision")
        colours[vertex] = colour
    require(all(colours[a] != colours[b] for a, b in edges), "proper physical colouring")
    triangle = [labels[index] for index in (0, 81, 162)]
    require(len(set(triangle)) == 3
            and all(tuple(sorted((a, b))) in edges for a, b in combinations(triangle, 2)),
            "universal physical triangle")
    circle = primitive({(2, 0): 1, (0, 2): 3, (0, 0): -1})
    result.update(vertices=len(points), edges=len(edge_list), weights=weights,
                  unit_circle=ev(circle))
    return result


AUDIT_DATA = None


def initialize_component_workers(factors, raw_by_row, edgegroups):
    global AUDIT_DATA
    AUDIT_DATA = factors, raw_by_row, edgegroups


def component_task(component):
    return component_audit(component, *AUDIT_DATA)


def primitive_qx(poly, x):
    _, integer = sp.Poly(poly, x, domain=sp.QQ).clear_denoms(convert=True)
    _, integer = integer.primitive()
    if integer.LC() < 0:
        integer = -integer
    return sp.Poly(integer, x, domain=sp.QQ)


class QuotientField:
    """Tiny exact Q[x]/(q) implementation; coefficient lists are ascending."""
    def __init__(self, q):
        raw = [Fraction(q.nth(i)) for i in range(q.degree() + 1)]
        lead = raw[-1]
        self.q = tuple(value / lead for value in raw)
        self.degree = len(self.q) - 1
        self.zero = ()
        self.one = (Fraction(1),)
        self.x = self.reduce((Fraction(0), Fraction(1)))

    @staticmethod
    def trim(values):
        values = list(values)
        while values and not values[-1]:
            values.pop()
        return tuple(values)

    def reduce(self, values):
        out = list(values)
        while len(out) > self.degree:
            coefficient = out[-1]
            power = len(out) - 1 - self.degree
            if coefficient:
                for i, value in enumerate(self.q):
                    out[power + i] -= coefficient * value
            out.pop()
        return self.trim(out)

    def add(self, left, right):
        n = max(len(left), len(right))
        return self.trim([(left[i] if i < len(left) else 0)
                          + (right[i] if i < len(right) else 0) for i in range(n)])

    def neg(self, value):
        return tuple(-x for x in value)

    def sub(self, left, right):
        return self.add(left, self.neg(right))

    def mul(self, left, right):
        if not left or not right:
            return ()
        out = [Fraction(0)] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                out[i + j] += a * b
        return self.reduce(out)

    @staticmethod
    def qdivmod(left, right):
        left = list(QuotientField.trim(left))
        right = QuotientField.trim(right)
        require(right, "division by zero polynomial")
        quotient = [Fraction(0)] * max(0, len(left) - len(right) + 1)
        while len(left) >= len(right):
            shift = len(left) - len(right)
            scale = left[-1] / right[-1]
            quotient[shift] = scale
            for i, value in enumerate(right):
                left[shift + i] -= scale * value
            left = list(QuotientField.trim(left))
        return QuotientField.trim(quotient), QuotientField.trim(left)

    def inv(self, value):
        r0, r1 = self.q, self.trim(value)
        s0, s1 = (), (Fraction(1),)
        while r1:
            quotient, remainder = self.qdivmod(r0, r1)
            r0, r1 = r1, remainder
            product_qs = [Fraction(0)] * max(0, len(quotient) + len(s1) - 1)
            for i, a in enumerate(quotient):
                for j, b in enumerate(s1):
                    product_qs[i + j] += a * b
            s0, s1 = s1, self.qdivmod(
                self.trim([(s0[i] if i < len(s0) else 0)
                           - (product_qs[i] if i < len(product_qs) else 0)
                           for i in range(max(len(s0), len(product_qs)))]), self.q)[1]
        require(len(r0) == 1, "nonunit quotient-field coefficient")
        return self.reduce(tuple(value / r0[0] for value in s0))

    def pow_x(self, exponent):
        out, base = self.one, self.x
        while exponent:
            if exponent & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exponent >>= 1
        return out


def kpoly_trim(poly):
    poly = list(poly)
    while poly and not poly[-1]:
        poly.pop()
    return poly


def kpoly_monic(poly, field):
    poly = kpoly_trim(poly)
    if not poly:
        return []
    inverse = field.inv(poly[-1])
    return [field.mul(value, inverse) for value in poly]


def kpoly_remainder(left, right, field):
    left, right = kpoly_trim(left), kpoly_trim(right)
    require(right, "zero K[y] divisor")
    inverse = field.inv(right[-1])
    while len(left) >= len(right):
        scale = field.mul(left[-1], inverse)
        shift = len(left) - len(right)
        for i, value in enumerate(right):
            left[shift + i] = field.sub(left[shift + i], field.mul(scale, value))
        left = kpoly_trim(left)
    return left


def kpoly_gcd(left, right, field):
    left, right = kpoly_trim(left), kpoly_trim(right)
    while right:
        left, right = right, kpoly_remainder(left, right, field)
    return kpoly_monic(left, field)


def sparse_fiber(sparse, field):
    degree_y = max(j for i, j, coefficient in sparse)
    out = [field.zero] * (degree_y + 1)
    powers = [field.one]
    for _ in range(max(i for i, j, coefficient in sparse)):
        powers.append(field.mul(powers[-1], field.x))
    for i, j, coefficient in sparse:
        out[j] = field.add(out[j], tuple(coefficient * value for value in powers[i]))
    return kpoly_trim(out)


def component_projection_zero(component, coordinate, coefficients):
    field_q = sp.Poly(sum(sp.Rational(value) * sp.Symbol("s")**i
                          for i, value in enumerate(component["q"])), sp.Symbol("s"), domain=sp.QQ)
    field = QuotientField(field_q)
    projected = tuple(Fraction(value) for value in component[coordinate])
    total = field.zero
    for value in reversed(coefficients):
        total = field.add(field.mul(total, projected), (Fraction(value),))
    return not total


def fiber_task(task):
    pair, left, right, components = task
    x, y = sp.symbols("x y")
    f = sum(c * x**i * y**j for i, j, c in left)
    g = sum(c * x**i * y**j for i, j, c in right)
    resultant = sp.Poly(sp.resultant(f, g, x), y, domain=sp.QQ)
    require(not resultant.is_zero, "finite reverse resultant")
    records, assigned, nonlinear = [], set(), 0
    for q0, exponent in sp.factor_list(resultant)[1]:
        qy = primitive_qx(q0, y)
        field = QuotientField(qy)
        swapped_left = tuple((j, i, coefficient) for i, j, coefficient in left)
        swapped_right = tuple((j, i, coefficient) for i, j, coefficient in right)
        h = kpoly_gcd(sparse_fiber(swapped_left, field),
                      sparse_fiber(swapped_right, field), field)
        require(h, "whole horizontal component")
        derivative = [tuple(i * value for value in h[i]) for i in range(1, len(h))]
        repeated = kpoly_gcd(h, derivative, field)
        square_free_degree = (len(h) - 1) - (len(repeated) - 1)
        if qy.degree() > 1 and len(h) > 2:
            nonlinear += 1
        coefficients = [str(qy.nth(i)) for i in range(qy.degree() + 1)]
        keys, count = [], 0
        for component in components:
            if not component_projection_zero(component, "y", coefficients):
                continue
            require(component["key"] not in assigned, "unique x projection factor")
            ev = evaluator(component)
            require(ev(left) and ev(right), "claimed point solves original anchors")
            assigned.add(component["key"])
            keys.append(component["key"])
            count += len(component["q"]) - 1
        require(count == qy.degree() * square_free_degree,
                "complete independent square-free fibre coverage")
        records.append([coefficients, len(h) - 1, square_free_degree, sorted(keys)])
    require(assigned == {component["key"] for component in components},
            "every supplied component has a projection fibre")
    return {"pair": list(pair), "projection": "y", "fibers": records,
            "nonlinear_nonrational_fibers": nonlinear}


def run(pencil_path, certificate_path, jobs=1):
    spaces, allowed, three, no_binomial, independent = f4_subspaces()
    supplied = load_pencils(pencil_path)
    require(sorted(pencil for index, pencil in supplied) == independent,
            "entrywise independent binomial-pencil classification")
    rows, events, factors, buckets = make_inventory()
    selected, pairs = pair_envelope(supplied, buckets)
    lifts = [prod(len(buckets[(row, 0)]) for row in pencil) for index, pencil in supplied]
    require(set(lifts) == {2048} and sum(lifts) == 387072, "complete raw-lift count")

    certificate = json.loads(Path(certificate_path).read_text())
    require(certificate["schema"] == "hn-four-power-binomial-pencils-v1", "certificate schema")
    require(certificate["curve_inventory_sha256"] == digest(factors), "certificate inventory pin")
    supplied_json = [[index, [[list(row), 0] for row in pencil]] for index, pencil in supplied]
    require(certificate["pencil_interface_sha256"] == digest(supplied_json),
            "certificate pencil-interface pin")
    require([tuple(record["pair"]) for record in certificate["pairs"]] == pairs,
            "complete anchor-pair list")
    records = {component["key"]: component for component in certificate["components"]}
    require(len(records) == len(certificate["components"]), "distinct component records")
    require(all(set(record["components"]) <= set(records) for record in certificate["pairs"]),
            "pair component keys")
    require({key for record in certificate["pairs"] for key in record["components"]} == set(records),
            "every component has pair incidence")

    tasks = []
    for pair, claimed in zip(pairs, certificate["pairs"]):
        a, b = pair
        tasks.append((pair, factors[a], factors[b], [records[key] for key in claimed["components"]]))
    require(1 <= jobs <= 8, "bounded worker count")
    with ProcessPoolExecutor(max_workers=jobs) as pool:
        fiber_transcript = list(pool.map(fiber_task, tasks, chunksize=1))
    raw_by_row = {row: raw for row, (raw, event) in zip(rows, events)}
    edgegroups = row_edgegroups()
    ordered = [records[key] for key in sorted(records)]
    with ProcessPoolExecutor(max_workers=jobs, initializer=initialize_component_workers,
                             initargs=(factors, raw_by_row, edgegroups)) as pool:
        results = list(pool.map(component_task, ordered, chunksize=1))

    by_pair = {tuple(record["pair"]): record["components"] for record in certificate["pairs"]}
    concurrency_transcript = []
    for index, domains, pencil_pairs in selected:
        for pair in pencil_pairs:
            for key in by_pair[pair]:
                active = set(records[key]["active_curves"])
                require(pair[0] in active and pair[1] in active, "anchor substitution")
                sections = [[curve for curve in domain if curve in active] for domain in domains]
                require(not all(sections), "full five-section concurrence")
                concurrency_transcript.append([index, list(pair), key, sections])
    require(digest(concurrency_transcript) == "6a2a1f4a8e546a0bd31349eefba392dcb3f9adf7c3a6ebfef44ebd3b9b257f68",
            "concurrency transcript")
    require(digest(results) == "acffb2697a478bc822b50e372e864c13a073e56b49168806598d531215dd89fa",
            "physical transcript")

    graph_hist, active_hist, degree_hist, weight_hist = Counter(), Counter(), Counter(), Counter()
    for result in results:
        if result["nreal"]:
            n = result["nreal"]
            graph_hist[f'{result["vertices"]}v_{result["edges"]}e'] += n
            active_hist[str(result["active"])] += n
            degree_hist[str(result["degree"])] += n
            weight_hist["".join(map(str, result["weights"]))] += n
    output = {
        "status": "PASS",
        "projective_points": 85,
        "rank_two_subspaces": len(spaces),
        "homogeneous_nonmonomial_pencils": len(allowed),
        "three_position_pencils": len(three),
        "four_position_no_binomial_pencils": len(no_binomial),
        "four_position_binomial_pencils": len(supplied),
        "raw_lifts": sum(lifts),
        "factor_inventory_sha256": digest(factors),
        "anchor_pairs": len(pairs),
        "components": len(records),
        "component_pair_incidence": sum(len(record["components"]) for record in certificate["pairs"]),
        "real_components": sum(result["nreal"] > 0 for result in results),
        "real_parameters": sum(result["nreal"] for result in results),
        "reverse_nonlinear_nonrational_fibers": sum(row["nonlinear_nonrational_fibers"]
                                                     for row in fiber_transcript),
        "reverse_pairs_with_nonlinear_nonrational_fibers": sum(
            row["nonlinear_nonrational_fibers"] > 0 for row in fiber_transcript),
        "reverse_fiber_transcript_sha256": digest(fiber_transcript),
        "concurrency_transcript_sha256": digest(concurrency_transcript),
        "physical_transcript_sha256": digest(results),
        "graph_histogram": dict(sorted(graph_hist.items())),
        "active_histogram": dict(sorted(active_hist.items())),
        "degree_histogram": dict(sorted(degree_hist.items())),
        "weight_histogram": dict(sorted(weight_hist.items())),
    }
    require((output["components"], output["component_pair_incidence"]) == (1539, 2956),
            "component totals")
    require((output["real_components"], output["real_parameters"]) == (1469, 4320),
            "real totals")
    return output


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--pencils", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.pencils, args.certificate, args.jobs)
    if args.check_expected:
        require(result == json.loads(Path(__file__).with_name("EXPECTED.json").read_text()),
                "expected independent result")
    print(json.dumps(result, sort_keys=True, indent=2))
