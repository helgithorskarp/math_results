#!/usr/bin/env python3
"""Exact auxiliary checks for PROOF.md; the continuous proof remains written.

CPython >= 3.11, standard library only. No floating arithmetic, external data,
solver, or expected-output file is used to establish any check.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Quadratic:
    """An element a+b*sqrt(D), with exact rational coefficients."""

    D: int
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        require(self.D > 0, "nonpositive radicand")
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    def coerce(self, other):
        if isinstance(other, Quadratic):
            require(self.D == other.D, "incompatible quadratic fields")
            return other
        return Quadratic(self.D, F(other))

    def __add__(self, other):
        other = self.coerce(other)
        return Quadratic(self.D, self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(self.D, -self.a, -self.b)

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        return Quadratic(
            self.D,
            self.a * other.a + self.D * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        denominator = other.a * other.a - self.D * other.b * other.b
        require(denominator != 0, "zero quadratic divisor")
        return self * Quadratic(self.D, other.a / denominator, -other.b / denominator)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def sign(self):
        """Exact ordering of the selected positive real square root."""
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        difference = self.a * self.a - self.D * self.b * self.b
        return ((self.a > 0) - (self.a < 0)) * (
            (difference > 0) - (difference < 0)
        )

    def record(self):
        return {"a": str(self.a), "b": str(self.b), "radicand": self.D}


def arithmetic():
    e, delta, upper_a = F(1, 300), F(1, 50), F(31, 100)
    require(5 * 25 * 25 < 56 * 56, "sqrt(5) upper bound")
    require((F(56, 25) - 1) / 4 == upper_a, "cosine bound conversion")
    require(F(1, 2) - e > upper_a, "pentagon domain")
    require(0 < F(3, 5) + delta < 1, "positive margin comparison")
    endpoints = [F(1, 2), F(3, 5)]
    values = [c - e - upper_a - (1 - upper_a) * (c + delta) ** 2 for c in endpoints]
    require(values == [F(17, 187500), F(16073, 750000)], "margin endpoint identities")
    require(all(v > 0 for v in values), "nonpositive margin endpoint")
    require(-(1 - upper_a) < 0, "concavity")

    a = Quadratic(5, F(-1, 4), F(1, 4))
    one = Quadratic(5, 1)
    require((4 * a * a + 2 * a - 1).sign() == 0, "pentagon cosine identity")
    require(a.sign() > 0 and (one - a).sign() > 0, "cosine domain")
    critical = a / (one - a)
    require(critical == Quadratic(5, 0, F(1, 5)), "sharp exclusion threshold")
    # Coefficient comparison in c for both sides of the displayed factorization.
    left = [-a, one, -(one - a)]
    right = [-a, (one - a) + a, -(one - a)]
    require(left == right, "threshold polynomial factorization")

    # Raw role words: A=active, P=other positive, N=nonpositive.
    role_counts = {}
    six_run_counts = {2: 0, 3: 0}
    for m in (4, 5, 6):
        exceptional = []
        for word in product("APN", repeat=m):
            if word.count("A") < 3:
                continue
            adjacent_n = any(word[i] == word[(i + 1) % m] == "N" for i in range(m))
            if adjacent_n:
                require(m in (5, 6) and word.count("N") <= m - 3,
                        "nonpositive-pair role reduction")
                if m == 6:
                    lengths = []
                    for i in range(m):
                        if word[i] != "N" or word[(i - 1) % m] == "N":
                            continue
                        length = 1
                        while word[(i + length) % m] == "N":
                            length += 1
                        if length >= 2:
                            lengths.append(length)
                    require(len(lengths) == 1 and lengths[0] in (2, 3), "hexagon run cover")
                    r = lengths[0]
                    require(5 - r <= 3, "hexagon remaining-gap budget")
                    six_run_counts[r] += 1
                exceptional.append("".join(word))
        role_counts[str(m)] = exceptional
    require(role_counts["4"] == [] and len(role_counts["5"]) == 5,
            "raw exceptional role words")
    require(six_run_counts == {2: 42, 3: 6} and len(role_counts["6"]) == 48,
            "hexagon exceptional role words")
    return {
        "edge_cosine_tolerance": str(e),
        "strict_cover_cosine_margin": str(delta),
        "c_interval": [str(x) for x in endpoints],
        "cos_72_upper_bound": str(upper_a),
        "concave_margin_endpoint_lower_bounds": [str(x) for x in values],
        "critical_contact_pentagon_cosine": critical.record(),
        "exceptional_role_words": role_counts,
        "hexagon_nonpositive_run_counts": six_run_counts,
    }


def counterexample(points=None):
    D, c = 3835, F(7, 12)
    require(61 * 61 < D < 62 * 62, "radicand bracket")
    R = Quadratic(D, 0, 1)
    u, w = F(7, 18) - R / 117, F(7, 18) + R / 45
    require(u.sign() < 0 and w.sign() > 0, "concave coordinate signs")
    if points is None:
        points = {
            "V": (0, 0, 1),
            "A": (u, -w, c),
            "P": (1, -1, F(1, 2)),
            "Q": (1, 1, F(1, 2)),
            "B": (u, w, c),
        }
    require(set(points) == set("VAPQB"), "counterexample labels")
    H = (F(13, 24), F(5, 24), F(1))

    def dot(p, q):
        return sum((Quadratic(D, h) * x * y for h, x, y in zip(H, p, q)), Quadratic(D))

    for name, p in points.items():
        require(len(p) == 3 and (dot(p, p) - 1).sign() == 0, "nonunit point " + name)
        require(Quadratic(D).coerce(p[2]).sign() > 0, "hemisphere " + name)
    pairs = []
    contacts = []
    for left, right in combinations("VAPQB", 2):
        d = dot(points[left], points[right])
        comparison = (d - c).sign()
        require(comparison <= 0 and (1 - d).sign() > 0, "packing/distinctness " + left + right)
        if comparison == 0:
            contacts.append("".join(sorted(left + right)))
        pairs.append({"pair": left + right, "dot": d.record(), "contact": comparison == 0})
    require(sorted(contacts) == ["AP", "AV", "BQ", "BV", "PQ"], "contact set")

    projected = {name: tuple(Quadratic(D).coerce(x) / p[2] for x in p[:2])
                 for name, p in points.items()}

    def turn(p, q, r):
        return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

    order = "VAPQB"
    turns = []
    for i, name in enumerate(order):
        t = turn(projected[order[(i - 1) % 5]], projected[name], projected[order[(i + 1) % 5]])
        require(t.sign() == (-1 if name == "V" else 1), "turn sign " + name)
        turns.append({"vertex": name, "turn": t.record(), "sign": t.sign()})
    return {"c": str(c), "metric": [str(h) for h in H], "pairs": pairs, "turns": turns}


def controls():
    require(Quadratic(5, -2, 1).sign() == 1, "ordering control")
    require(Quadratic(5, 2, -1).sign() == -1, "ordering control")
    require(Quadratic(5, -3, 1).sign() == -1, "ordering control")
    require(Quadratic(5, 3, -1).sign() == 1, "ordering control")
    bad = {"V": (0, 0, 1), "A": (1, 0, 0), "P": (1, -1, F(1, 2)),
           "Q": (1, 1, F(1, 2)), "B": (-1, 0, 0)}
    try:
        counterexample(bad)
    except ValueError:
        pass
    else:
        raise ValueError("bad-coordinate control accepted")
    return {"quadratic_ordering_cases": 4, "bad_coordinate_rejected": True}


if __name__ == "__main__":
    result = {"status": "all exact auxiliary checks passed", "arithmetic": arithmetic(),
              "concave_five_cycle": counterexample(), "controls": controls(),
              "trust_boundary": "continuous spherical covering and face bridges remain written"}
    print(json.dumps(result, indent=2, sort_keys=True))
