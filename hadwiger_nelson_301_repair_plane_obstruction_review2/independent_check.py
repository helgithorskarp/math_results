#!/usr/bin/env python3
"""Independent exact audit of the h3981 plane obstruction.

This checker imports neither reviewed implementation.  It canonically
enumerates every four-cycle of the graph, constructs quotient edges literally,
uses reverse-pivot sparse elimination at two fresh primes, and expands the
quadratic identity as a full rational Gram matrix.
"""

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import isqrt
import argparse
import json
from pathlib import Path


GRAPH_SHA256 = "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb"
CERTIFICATE_SHA256 = "728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42"
RANK_PRIMES = (1_000_003, 1_000_033)


def need(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical_cycle(cycle):
    cycle = tuple(cycle)
    reverse = tuple(reversed(cycle))
    variants = []
    for row in (cycle, reverse):
        variants.extend(row[offset:] + row[:offset] for offset in range(4))
    return min(variants)


def enumerate_four_cycles(labels, neighbors):
    cycles = set()
    for first, third in combinations(labels, 2):
        common = sorted(neighbors[first] & neighbors[third])
        for second, fourth in combinations(common, 2):
            cycles.add(canonical_cycle((first, second, third, fourth)))
    return cycles


def quotient_edges(edges, keep, remove):
    result = set()
    for first, second in edges:
        mapped_first = keep if first == remove else first
        mapped_second = keep if second == remove else second
        if mapped_first != mapped_second:
            result.add(tuple(sorted((mapped_first, mapped_second))))
    return result


def is_prime(number):
    return number >= 2 and all(number % divisor
                               for divisor in range(2, isqrt(number) + 1))


def sparse_rank(rows, prime):
    """Reverse-column sparse echelon reduction over a prime field."""
    need(is_prime(prime), f"rank modulus {prime} is prime")
    basis = {}
    for source in rows:
        row = {column: coefficient % prime
               for column, coefficient in source.items()
               if coefficient % prime}
        while row:
            pivot = max(row)
            coefficient = row[pivot]
            if pivot not in basis:
                inverse = pow(coefficient, -1, prime)
                basis[pivot] = {column: value * inverse % prime
                                for column, value in row.items()}
                break
            pivot_row = basis[pivot]
            for column, value in pivot_row.items():
                reduced = (row.get(column, 0) - coefficient * value) % prime
                if reduced:
                    row[column] = reduced
                else:
                    row.pop(column, None)
    return len(basis)


def parse_parameters(raw_rows, column_count):
    parameters = []
    for raw_row in raw_rows:
        row = {}
        previous = -1
        for column, numerator, denominator in raw_row:
            need(type(column) is int and previous < column < column_count,
                 "ordered parameter column")
            need(type(numerator) is int and numerator != 0
                 and type(denominator) is int and denominator > 0,
                 "rational parameter entry")
            value = Fraction(numerator, denominator)
            need(value.numerator == numerator and value.denominator == denominator,
                 "canonical rational parameter entry")
            row[column] = value
            previous = column
        parameters.append(row)
    return parameters


def combine_parameter_rows(equation, parameters):
    result = {}
    for vertex, coefficient in equation.items():
        for column, value in parameters[vertex].items():
            result[column] = result.get(column, Fraction()) + coefficient * value
    return {column: value for column, value in result.items() if value}


def audit(graph, certificate):
    labels = graph["labels"]
    need(labels == sorted(set(labels)) and len(labels) == 301,
         "301 canonical graph labels")
    label_set = set(labels)
    position = {label: index for index, label in enumerate(labels)}
    raw_edges = graph["edges"]
    edges = {tuple(edge) for edge in raw_edges}
    need(raw_edges == [list(edge) for edge in sorted(edges)]
         and len(edges) == 1452, "canonical 1452-edge graph")
    need(all(first < second and first in label_set and second in label_set
             for first, second in edges), "simple graph endpoints")
    need(certificate["source_sha256"] == GRAPH_SHA256,
         "certificate names the input graph")
    neighbors = {label: set() for label in labels}
    for first, second in edges:
        neighbors[first].add(second)
        neighbors[second].add(first)

    all_cycles = enumerate_four_cycles(labels, neighbors)
    need(len(all_cycles) == 2062, "independent all-four-cycle census")
    certified_cycles = []
    normalized_cycles = set()
    required_diagonals = set()
    equations = []
    for raw_cycle in certificate["cycles"]:
        cycle = tuple(raw_cycle)
        need(len(cycle) == 4 and len(set(cycle)) == 4
             and all(vertex in label_set for vertex in cycle),
             "certified four-cycle vertices")
        normalized = canonical_cycle(cycle)
        need(normalized in all_cycles and normalized not in normalized_cycles,
             "distinct literal certified four-cycle")
        normalized_cycles.add(normalized)
        certified_cycles.append(cycle)
        for offset in range(2):
            required_diagonals.add(tuple(sorted((cycle[offset],
                                                 cycle[offset + 2]))))
        equation = {}
        for offset, label in enumerate(cycle):
            equation[position[label]] = 1 if offset % 2 == 0 else -1
        equations.append(equation)
    need(len(certified_cycles) == len(normalized_cycles) == 279,
         "279 distinct mandatory cycles")
    need(len(required_diagonals) == 558,
         "two distinct diagonals per certified cycle")

    witnesses = certificate["diagonal_obstructions"]
    witness_pairs = set()
    for key in witnesses:
        fields = key.split(",")
        need(len(fields) == 2, "diagonal key fields")
        first, second = map(int, fields)
        need(first < second and first in label_set and second in label_set,
             "diagonal key endpoints")
        witness_pairs.add((first, second))
    need(witness_pairs == required_diagonals,
         "exact diagonal witness coverage")

    direct = 0
    odd_wheels = 0
    rim_lengths = {}
    quotient_pairs = set()
    quotient_edge_checks = 0
    for first, second in sorted(required_diagonals):
        witness = witnesses[f"{first},{second}"]
        if witness == {"type": "edge"}:
            need((first, second) in edges, "direct diagonal edge")
            direct += 1
            continue
        need(witness.get("type") == "odd_wheel"
             and (first, second) not in edges,
             "nonedge diagonal odd-wheel type")
        quotient_pairs.add((first, second))
        quotient = quotient_edges(edges, first, second)
        quotient_labels = label_set - {second}
        hub = witness["hub"]
        rim = witness["rim"]
        need(hub in quotient_labels and hub not in rim,
             "quotient wheel hub")
        need(len(rim) >= 3 and len(rim) % 2 == 1
             and len(set(rim)) == len(rim)
             and set(rim) <= quotient_labels,
             "simple odd quotient rim")
        for vertex in rim:
            need(tuple(sorted((hub, vertex))) in quotient,
                 "quotient wheel spoke")
            quotient_edge_checks += 1
        for left, right in zip(rim, rim[1:] + rim[:1]):
            need(tuple(sorted((left, right))) in quotient,
                 "quotient wheel rim edge")
            quotient_edge_checks += 1
        odd_wheels += 1
        rim_lengths[len(rim)] = rim_lengths.get(len(rim), 0) + 1
    need((direct, odd_wheels) == (276, 282),
         "diagonal obstruction type census")
    need(rim_lengths == {3: 266, 5: 10, 7: 6},
         "odd-wheel length census")

    anchor = certificate["translation_anchor"]
    need(anchor in position, "translation anchor label")
    equations.append({position[anchor]: 1})
    free_labels = certificate["free_labels"]
    need(len(free_labels) == len(set(free_labels)) == 55
         and set(free_labels) <= label_set, "55 free labels")
    parameters = parse_parameters(certificate["parametrization"], 55)
    need(len(parameters) == len(labels), "301 parameter rows")
    for column, label in enumerate(free_labels):
        need(parameters[position[label]] == {column: Fraction(1)},
             "free-label identity row")
    need(all(not combine_parameter_rows(row, parameters)
             for row in equations), "exact rational kernel containment")

    ranks = {prime: sparse_rank(equations, prime) for prime in RANK_PRIMES}
    need(set(ranks.values()) == {246}, "independent modular ranks")
    need(certificate["affine_rank"] == 246
         and 246 + len(free_labels) == len(labels),
         "rational rank-nullity squeeze")

    gram = [[Fraction() for _ in range(55)] for _ in range(55)]
    norm_edges = set()
    weight_sum = 0
    weights = []
    for first, second, weight in certificate["norm_weights"]:
        edge = (first, second)
        need(edge in edges and edge not in norm_edges,
             "distinct physical norm edge")
        need(type(weight) is int and weight != 0,
             "nonzero integer norm weight")
        norm_edges.add(edge)
        weights.append(weight)
        weight_sum += weight
        difference = parameters[position[first]].copy()
        for column, value in parameters[position[second]].items():
            difference[column] = difference.get(column, Fraction()) - value
        difference = {column: value for column, value in difference.items()
                      if value}
        for row, row_value in difference.items():
            for column, column_value in difference.items():
                gram[row][column] += weight * row_value * column_value
    nonzero_gram_entries = sum(value != 0 for row in gram for value in row)
    need(len(norm_edges) == 18 and nonzero_gram_entries == 0,
         "zero rational Gram identity on 18 edges")
    need(weight_sum == certificate["weight_sum"] == 708,
         "nonzero unit-length evaluation")

    return {
        "status": "INDEPENDENTLY_VERIFIED_H3981_PLANE_OBSTRUCTION",
        "vertices": len(labels),
        "edges": len(edges),
        "all_graph_four_cycles": len(all_cycles),
        "mandatory_four_cycles": len(certified_cycles),
        "diagonal_obstructions": len(required_diagonals),
        "direct_diagonal_edges": direct,
        "quotient_odd_wheels": odd_wheels,
        "quotient_wheel_edges_checked": quotient_edge_checks,
        "odd_wheel_rim_lengths": {str(length): count
                                  for length, count in sorted(rim_lengths.items())},
        "anchored_equations": len(equations),
        "independent_rank_primes": list(RANK_PRIMES),
        "independent_ranks": [ranks[prime] for prime in RANK_PRIMES],
        "coordinate_parameters": len(free_labels),
        "parameter_nonzeros": sum(map(len, parameters)),
        "norm_identity_edges": len(norm_edges),
        "norm_weight_gcd": __import__("math").gcd(*weights),
        "unit_norm_sum": weight_sum,
        "quadratic_nonzero_entries": nonzero_gram_entries,
        "graph_sha256": GRAPH_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "maps_excluded": "all plane unit-edge maps, including noninjective maps",
        "target_unit_distance_graph_established": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    need(digest(args.graph) == GRAPH_SHA256, "input graph SHA-256")
    need(digest(args.certificate) == CERTIFICATE_SHA256,
         "geometric certificate SHA-256")
    graph = json.loads(args.graph.read_text())
    certificate = json.loads(args.certificate.read_text())
    print(json.dumps(audit(graph, certificate), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
