#!/usr/bin/env python3
"""Exact independent gate for the two-anchor dominated-Moser connector."""
from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent

# A row (a,b,c,d) means ((a+b*sqrt(33))/12,
#                        (c*sqrt(3)+d*sqrt(11))/12).
ROWS = (
    (0, 0, 0, 0),
    (12, 0, 0, 0),
    (6, 0, 6, 0),
    (18, 0, 6, 0),
    (10, 0, 0, 2),
    (5, -1, 5, 1),
    (15, -1, 5, 3),
)


class L:
    """An element a+b*sqrt(33), with exact rational coefficients."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)

    def __add__(self, other):
        other = as_l(other)
        return L(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return L(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_l(other))

    def __rsub__(self, other):
        return as_l(other) - self

    def __mul__(self, other):
        other = as_l(other)
        return L(self.a * other.a + 33 * self.b * other.b,
                 self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __eq__(self, other):
        try:
            other = as_l(other)
        except (TypeError, ValueError):
            return False
        return self.a == other.a and self.b == other.b

    def serial(self):
        return [qstr(self.a), qstr(self.b)]


def as_l(value):
    return value if isinstance(value, L) else L(value)


def qstr(value):
    return (str(value.numerator) if value.denominator == 1
            else f"{value.numerator}/{value.denominator}")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def distance2(row, other):
    a, b, c, d = (row[i] - other[i] for i in range(4))
    return L(Q(a * a + 33 * b * b + 3 * c * c + 11 * d * d, 144),
             Q(2 * (a * b + c * d), 144))


def circumcircle_denominator(side_squares):
    """Return 16 times triangle area squared from three squared sides."""
    a, b, c = side_squares
    return 2 * (a * b + b * c + c * a) - a * a - b * b - c * c


def colour(edges, colours):
    adj = [set() for _ in ROWS]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    word = [-1] * len(ROWS)

    def dfs(done):
        if done == len(ROWS):
            return tuple(word)
        uncoloured = [v for v in range(len(ROWS)) if word[v] < 0]
        vertex = max(uncoloured,
                     key=lambda v: (len({word[w] for w in adj[v] if word[w] >= 0}),
                                    len(adj[v]), -v))
        forbidden = {word[w] for w in adj[vertex] if word[w] >= 0}
        for value in range(colours):
            if value not in forbidden:
                word[vertex] = value
                answer = dfs(done + 1)
                if answer is not None:
                    return answer
        word[vertex] = -1
        return None

    return dfs(0)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def analyse(rows=ROWS):
    need(len(rows) == 7 and len(set(rows)) == 7, "seven distinct rows required")
    pairs = {(a, b): distance2(rows[a], rows[b])
             for a, b in itertools.combinations(range(7), 2)}
    edges = tuple(pair for pair, square in pairs.items() if square == 1)
    need(len(edges) == 11, "not the displayed Moser spindle")
    three = colour(edges, 3)
    four = colour(edges, 4)
    need(three is None and four is not None, "Moser chromatic check failed")
    need(all(four[a] != four[b] for a, b in edges), "bad four-colour witness")

    centre_triples = {v: [] for v in range(7)}
    collinear = 0
    qualifying = 0
    for triple in itertools.combinations(range(7), 3):
        a, b, c = triple
        side_squares = (pairs[min(a, b), max(a, b)],
                        pairs[min(b, c), max(b, c)],
                        pairs[min(a, c), max(a, c)])
        area16 = circumcircle_denominator(side_squares)
        if area16 == 0:
            collinear += 1
            continue
        # For a nondegenerate triangle, R^2=abc/(16 area^2).
        if side_squares[0] * side_squares[1] * side_squares[2] != area16:
            continue
        qualifying += 1
        possible = [v for v in range(7)
                    if all(v != u and pairs[min(u, v), max(u, v)] == 1
                           for u in triple)]
        need(len(possible) == 1, "unit circumcentre not uniquely identified")
        centre_triples[possible[0]].append(list(triple))

    neighbourhoods = []
    for v in range(7):
        if centre_triples[v]:
            neighbours = sorted(w for w in range(7)
                                if w != v and pairs[min(v, w), max(v, w)] == 1)
            need(len(neighbours) >= 3, "bad high-incidence centre")
            neighbourhoods.append({
                "centre_vertex": v,
                "neighbours": neighbours,
                "defining_triples": centre_triples[v],
            })
    need(qualifying == sum(len(row["defining_triples"]) for row in neighbourhoods),
         "qualifying triple accounting failed")

    covers = []
    largest = 0
    largest_pairs = []
    for first, second in itertools.combinations(neighbourhoods, 2):
        union = sorted(set(first["neighbours"]) | set(second["neighbours"]))
        size = len(union)
        if size > largest:
            largest, largest_pairs = size, []
        if size == largest:
            largest_pairs.append([first["centre_vertex"], second["centre_vertex"]])
        if size == 7:
            covers.append([first["centre_vertex"], second["centre_vertex"]])

    result = {
        "schema": "hn-e457-dominated-moser-gate-v1",
        "exact_field": "Q(sqrt(33)) distance arithmetic",
        "moser_vertices": 7,
        "moser_edges": len(edges),
        "moser_edge_list": [list(edge) for edge in edges],
        "moser_three_colourable": three is not None,
        "moser_four_colouring": list(four),
        "vertex_row_sha256": digest(rows),
        "edge_sha256": digest(edges),
        "triples_checked": 35,
        "collinear_triples": collinear,
        "unit_circumcentre_triples": qualifying,
        "centres_with_at_least_three_unit_neighbours": len(neighbourhoods),
        "centres_are_spindle_vertices": True,
        "maximum_unit_neighbours_of_one_centre": max(len(x["neighbours"])
                                                       for x in neighbourhoods),
        "centre_neighbourhoods": neighbourhoods,
        "centre_pairs_checked": len(neighbourhoods) * (len(neighbourhoods) - 1) // 2,
        "maximum_two_centre_neighbourhood_union": largest,
        "pairs_attaining_maximum_union": largest_pairs,
        "two_centre_covers": covers,
        "target_terminal_distance": "8/3",
        "architecture_feasible": bool(covers),
        "outside_E457_field_stage_reached": False,
        "record_candidate": False,
    }
    expected = HERE / "expected.json"
    if expected.exists():
        need(result == json.loads(expected.read_text()), "expected result mismatch")
    return result


def main():
    print(json.dumps(analyse(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
