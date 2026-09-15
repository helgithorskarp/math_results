#!/usr/bin/env python3
"""Exact verifier for the fixed de Grey D31 C7-equivariant plane-map gate."""

from fractions import Fraction as F
from hashlib import sha256
import json


def graph31():
    """Return the 98-edge GraphData template, with vertices made zero-based."""
    A = tuple(range(7))
    B = tuple(range(7, 14))
    C = 14
    D = tuple(range(15, 22))
    E = tuple(range(22, 29))
    F_axis = 29
    G_axis = 30
    edges = set()

    def add(left, right):
        edges.add(tuple(sorted((left, right))))

    for j in range(7):
        add(A[j], A[(j + 1) % 7])
        for orbit in (B, D, E):
            add(A[j], orbit[(j - 1) % 7])
            add(A[j], orbit[(j + 1) % 7])
        add(B[j], D[(j - 1) % 7])
        add(B[j], D[(j + 1) % 7])
        add(B[j], C)
        add(B[j], F_axis)
        add(C, E[j])
        add(D[j], G_axis)
        add(E[j], G_axis)
    assert len(edges) == 98
    return tuple(sorted(edges)), (A, B, C, D, E, F_axis, G_axis)


def graph61(edges31, shared_axis, joined_axis):
    """Notebook construction: share vertex 31 and join vertices 30 and 61."""
    mapping = {shared_axis: shared_axis}
    next_vertex = 31
    for vertex in range(31):
        if vertex != shared_axis:
            mapping[vertex] = next_vertex
            next_vertex += 1
    edges = set(edges31)
    edges.update(tuple(sorted((mapping[a], mapping[b]))) for a, b in edges31)
    edges.add(tuple(sorted((joined_axis, mapping[joined_axis]))))
    assert next_vertex == 61 and len(edges) == 197
    return tuple(sorted(edges))


def colour(vertices, edges, colour_count):
    """Exact DSATUR backtracking with canonical introduction of colour names."""
    adjacency = [set() for _ in range(vertices)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    row = [-1] * vertices
    nodes = 0

    def rec(done):
        nonlocal nodes
        nodes += 1
        if done == vertices:
            return tuple(row)
        vertex = max(
            (v for v in range(vertices) if row[v] < 0),
            key=lambda v: (
                len({row[w] for w in adjacency[v] if row[w] >= 0}),
                len(adjacency[v]),
                -v,
            ),
        )
        forbidden = {row[w] for w in adjacency[vertex] if row[w] >= 0}
        used = {value for value in row if value >= 0}
        for value in range(min(colour_count - 1, len(used)) + 1):
            if value not in forbidden:
                row[vertex] = value
                answer = rec(done + 1)
                if answer is not None:
                    return answer
        row[vertex] = -1
        return None

    return rec(0), nodes


def polynomial_strip(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return tuple(poly)


def polynomial_divmod(dividend, divisor):
    dividend = list(map(F, dividend))
    divisor = polynomial_strip(tuple(map(F, divisor)))
    quotient = [F(0)] * max(1, len(dividend) - len(divisor) + 1)
    while len(polynomial_strip(dividend)) >= len(divisor) and any(dividend):
        dividend = list(polynomial_strip(dividend))
        shift = len(dividend) - len(divisor)
        factor = dividend[-1] / divisor[-1]
        quotient[shift] += factor
        for index, value in enumerate(divisor):
            dividend[index + shift] -= factor * value
    return polynomial_strip(quotient), polynomial_strip(dividend)


def polynomial_gcd(left, right):
    left = polynomial_strip(tuple(map(F, left)))
    right = polynomial_strip(tuple(map(F, right)))
    while any(right):
        _quotient, remainder = polynomial_divmod(left, right)
        left, right = right, remainder
    leading = left[-1]
    return tuple(value / leading for value in left)


# Q(zeta_7), in the basis 1,z,...,z^5 with Phi_7=1+...+z^6.
QZERO = (F(0),) * 6
QONE = (F(1),) + (F(0),) * 5
ZETA7 = (F(0), F(1), F(0), F(0), F(0), F(0))


def qadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def qmul(a, b):
    coefficients = [F(0)] * 11
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            coefficients[i + j] += x * y
    for degree in range(10, 5, -1):
        value = coefficients[degree]
        for offset in range(1, 7):
            coefficients[degree - offset] -= value
    return tuple(coefficients[:6])


def qpower(a, exponent):
    answer = QONE
    while exponent:
        if exponent & 1:
            answer = qmul(answer, a)
        a = qmul(a, a)
        exponent //= 2
    return answer


def qscale(value, a):
    return tuple(F(value) * x for x in a)


def qeval(poly, x):
    answer = QZERO
    for coefficient in reversed(poly):
        answer = qadd(qmul(answer, x), qscale(coefficient, QONE))
    return answer


def digest_edges(edges):
    data = "".join(f"{a + 1} {b + 1}\n" for a, b in edges).encode()
    return sha256(data).hexdigest()


def word_string(word):
    return "".join(map(str, word))


def main():
    edges31, orbits = graph31()
    A, B, C, D, E, F_axis, G_axis = orbits
    sigma = {vertex: vertex for vertex in range(31)}
    for orbit in (A, B, D, E):
        for j, vertex in enumerate(orbit):
            sigma[vertex] = orbit[(j + 1) % 7]
    assert {
        tuple(sorted((sigma[left], sigma[right]))) for left, right in edges31
    } == set(edges31)

    three, nodes3 = colour(31, edges31, 3)
    four, nodes4 = colour(31, edges31, 4)
    assert three is None and four is not None
    equality_nodes = {}
    for left, right in ((C, F_axis), (C, G_axis), (F_axis, G_axis)):
        inequality_edge = tuple(sorted((left, right)))
        word, nodes = colour(31, tuple(sorted((*edges31, inequality_edge))), 4)
        assert word is None
        equality_nodes[f"{left + 1}-{right + 1}"] = nodes

    # This is exactly the construction displayed in the source notebook:
    # two D31 copies share vertex 31; the copies of vertex 30 are joined.
    edges61 = graph61(edges31, G_axis, F_axis)
    five, nodes5 = colour(61, edges61, 5)
    assert five is not None
    assert all(five[a] != five[b] for a, b in edges61)
    # Non-four follows without a 61-vertex search: within each D31 copy the
    # three axis roles are equal, but the two vertex-30 roles are adjacent.

    # For a nontrivial C7 action in the plane, alpha=2*pi*m/7 and
    # x=2*cos(alpha). The A-cycle, axial B contacts, and A-B offsets +/-1
    # force x^2(2-x)=1. But every such x satisfies x^3+x^2-2x-1=0.
    geometric_polynomial = (F(1), F(0), F(-2), F(1))
    seventh_trace_polynomial = (F(-1), F(-2), F(1), F(1))
    gcd = polynomial_gcd(geometric_polynomial, seventh_trace_polynomial)
    assert gcd == (F(1),)
    residues = []
    for m in range(1, 7):
        x = qadd(qpower(ZETA7, m), qpower(ZETA7, 7 - m))
        assert qeval(seventh_trace_polynomial, x) == QZERO
        residue = qeval(geometric_polynomial, x)
        assert residue != QZERO
        residues.append(tuple(map(int, residue)))

    result = {
        "scope": "nontrivial C7-equivariant plane edge maps of fixed D31",
        "source_vertices": 31,
        "source_edges": len(edges31),
        "source_edge_sha256_one_based": digest_edges(edges31),
        "source_chromatic_number": 4,
        "source_three_colour_search_nodes": nodes3,
        "source_four_colour_search_nodes": nodes4,
        "source_proper_four_word": word_string(four),
        "axis_roles_one_based": [C + 1, F_axis + 1, G_axis + 1],
        "axis_pair_inequality_search_nodes": equality_nodes,
        "all_axis_pairs_forced_equal_in_four_colours": True,
        "spindle_vertices": 61,
        "spindle_edges": len(edges61),
        "spindle_chromatic_number": 5,
        "spindle_non_four_from_axis_equality": True,
        "spindle_proper_five_word": word_string(five),
        "spindle_five_colour_search_nodes": nodes5,
        "seventh_trace_polynomial_ascending": list(map(int, seventh_trace_polynomial)),
        "geometric_necessity_polynomial_ascending": list(map(int, geometric_polynomial)),
        "polynomial_gcd": list(map(int, gcd)),
        "geometric_residues_in_qzeta7": residues,
        "c7_equivariant_nonconstant_plane_map": False,
        "candidate_status": False,
        "record_progress": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
