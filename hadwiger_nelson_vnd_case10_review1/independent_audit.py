#!/usr/bin/env python3
"""Independent exact geometry, strict-edge, and CNF audit for h3927.

No reviewed Python module is imported.  The coordinate archive is parsed by a
small recursive-descent evaluator, then specialized at a new finite-field
prime for the separate C++ all-pairs sieve.
"""

import argparse
import hashlib
import json
import re
import struct
from fractions import Fraction
from itertools import combinations
from math import isqrt
from pathlib import Path


ORDER = 64513
EDGE_COUNT = 542472
DENOMINATOR = 96
RADICANDS = (1, 2, 3, 6, 5, 10, 15, 30)
REVIEW_PRIME = 1000000271
REVIEW_ROOTS = (1, 677183386, 590934106, 0, 838613109, 0, 0, 0)
UPSTREAM_HASHES = {
    "source_graph.dimacs": "8e447a54c4093b3961cf6e28b5f97eb61ef34a127d719d8a8edab800c49566d1",
    "source_graph.zip": "b9f43e78fb16fea8001eafa8e549af2a20703519400481cbeba6f7f19dbc7d67",
    "source_notebook.ipynb": "7ade1ab6b32764ee8af9a721a3aaa30d54694636a4bdf0eb15e56cec5cafe06c",
    "source_vtx_README.md": "935d0b3d9b097378672ef1688f0baf3f1d1317cf32ab086f27175e315c134502",
    "source_rotation.txt": "a227b42a7e03799e67c8dfaa8d12b99f69019ad822f75499035a54e76bcf6531",
}
POINTS_SHA256 = "3a0113198dde91dbb99544b9d67f5aecc96b2de165c4b3db3a1715274d53fa66"
EDGES_SHA256 = "1cf734ec5d06549e8cf944d2ebdb709bf3e59f098e906f3d090a595929824c91"
CNF_SHA256 = "aa4305ebd561a52e89fe77738deee93c53f0c062a7715b879a51d0ada69b3bef"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def zero():
    return (Fraction(0),) * 8


def scalar(value):
    return (Fraction(value),) + (Fraction(0),) * 7


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def negate(value):
    return tuple(-x for x in value)


def multiply(left, right):
    answer = [Fraction(0) for _ in range(8)]
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if b:
                answer[i ^ j] += a * b * RADICANDS[i & j]
    return tuple(answer)


def divide(left, right):
    nonzero = [(i, x) for i, x in enumerate(right) if x]
    need(len(nonzero) == 1, "division by non-monomial")
    index, coefficient = nonzero[0]
    inverse = [Fraction(0) for _ in range(8)]
    inverse[index] = 1 / (coefficient * RADICANDS[index])
    return multiply(left, tuple(inverse))


def square_root(value):
    need(not any(value[1:]) and value[0] > 0, "nonpositive/nonrational square root")
    number = value[0]
    for index, radicand in enumerate(RADICANDS):
        quotient = number / radicand
        numerator = isqrt(quotient.numerator)
        denominator = isqrt(quotient.denominator)
        if (numerator * numerator == quotient.numerator and
                denominator * denominator == quotient.denominator):
            answer = [Fraction(0) for _ in range(8)]
            answer[index] = Fraction(numerator, denominator)
            return tuple(answer)
    raise ValueError("square root outside Q(sqrt2,sqrt3,sqrt5)")


class ExpressionParser:
    TOKEN = re.compile(r"\s*(Sqrt|[0-9]+|[-+*/(),\[\]])")

    def __init__(self, text):
        self.tokens = []
        position = 0
        while position < len(text):
            match = self.TOKEN.match(text, position)
            if match is None and text[position:].isspace():
                break
            need(match is not None, "coordinate token at " + text[position:position + 20])
            self.tokens.append(match.group(1))
            position = match.end()
        self.position = 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self, wanted=None):
        token = self.peek()
        need(token is not None and (wanted is None or token == wanted),
             "expected token " + str(wanted))
        self.position += 1
        return token

    def expression(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            operator = self.take()
            right = self.term()
            value = add(value, right if operator == "+" else negate(right))
        return value

    def term(self):
        value = self.factor()
        while self.peek() in ("*", "/"):
            operator = self.take()
            right = self.factor()
            value = multiply(value, right) if operator == "*" else divide(value, right)
        return value

    def factor(self):
        token = self.peek()
        if token in ("+", "-"):
            self.take()
            value = self.factor()
            return value if token == "+" else negate(value)
        if token == "(":
            self.take("(")
            value = self.expression()
            self.take(")")
            return value
        if token == "Sqrt":
            self.take("Sqrt")
            self.take("[")
            value = self.expression()
            self.take("]")
            return square_root(value)
        need(token is not None and token.isdigit(), "coordinate atom")
        self.take()
        return scalar(int(token))

    def parse(self):
        value = self.expression()
        need(self.peek() is None, "trailing coordinate syntax")
        return value


def coordinate_records(path):
    text = path.read_text()
    records = []
    position = 0
    while position < len(text):
        while position < len(text) and text[position].isspace():
            position += 1
        if position == len(text):
            break
        need(text[position] == "{", "coordinate opening brace")
        end = text.find("}", position + 1)
        need(end >= 0 and "{" not in text[position + 1:end], "coordinate braces")
        body = text[position + 1:end]
        depth = 0
        separator = None
        for index, character in enumerate(body):
            if character in "([":
                depth += 1
            elif character in ")]":
                depth -= 1
                need(depth >= 0, "coordinate delimiter nesting")
            elif character == "," and depth == 0:
                need(separator is None, "multiple coordinate separators")
                separator = index
        need(depth == 0 and separator is not None, "coordinate separator")
        x = ExpressionParser(body[:separator]).parse()
        y = ExpressionParser(body[separator + 1:]).parse()
        row = []
        for coefficient in x + y:
            scaled = coefficient * DENOMINATOR
            need(scaled.denominator == 1, "coordinate denominator")
            row.append(scaled.numerator)
        records.append(row)
        position = end + 1
    return records


def raw_edges(path):
    edges = []
    with path.open() as stream:
        need(stream.readline().split() == ["p", "edge", str(ORDER), str(EDGE_COUNT)],
             "raw graph header")
        for line in stream:
            fields = line.split()
            need(len(fields) == 3 and fields[0] == "e", "raw edge syntax")
            u, v = sorted((int(fields[1]) - 1, int(fields[2]) - 1))
            need(0 <= u < v < ORDER, "raw edge label")
            edges.append((u, v))
    need(len(edges) == EDGE_COUNT and len(set(edges)) == EDGE_COUNT,
         "raw edge count/uniqueness")
    return sorted(edges)


def squared_distance(left, right):
    answer = [0] * 8
    for offset in (0, 8):
        difference = [left[offset + i] - right[offset + i] for i in range(8)]
        for i, a in enumerate(difference):
            if not a:
                continue
            for j, b in enumerate(difference):
                if b:
                    answer[i ^ j] += a * b * RADICANDS[i & j]
    return tuple(answer)


def prime_check(number):
    need(number % 2, "even review prime")
    divisor = 3
    while divisor * divisor <= number:
        need(number % divisor, "composite review prime")
        divisor += 2


def residue_basis():
    prime_check(REVIEW_PRIME)
    need(2 * (REVIEW_PRIME - 1) ** 2 < 1 << 63,
         "review sieve signed-overflow bound")
    s2, s3, s5 = REVIEW_ROOTS[1], REVIEW_ROOTS[2], REVIEW_ROOTS[4]
    need(s2 * s2 % REVIEW_PRIME == 2, "review sqrt2")
    need(s3 * s3 % REVIEW_PRIME == 3, "review sqrt3")
    need(s5 * s5 % REVIEW_PRIME == 5, "review sqrt5")
    return (1, s2, s3, s2 * s3 % REVIEW_PRIME, s5,
            s2 * s5 % REVIEW_PRIME, s3 * s5 % REVIEW_PRIME,
            s2 * s3 * s5 % REVIEW_PRIME)


def prepare(source_work, review_work):
    for name, wanted in UPSTREAM_HASHES.items():
        need(digest(source_work / name) == wanted, "upstream identity " + name)
    parsed = coordinate_records(source_work / "source_graph.vtx")
    need(len(parsed) == ORDER and len({tuple(row) for row in parsed}) == ORDER,
         "parsed point order/distinctness")
    source_points = json.loads((source_work / "exact_points.json").read_text())
    need(source_points["denominator"] == DENOMINATOR and
         source_points["basis_radicands"] == list(RADICANDS), "source point metadata")
    need(parsed == source_points["points"], "independent parser/source point mismatch")
    packed_points = json.dumps(parsed, separators=(",", ":")).encode()
    need(hashlib.sha256(packed_points).hexdigest() == POINTS_SHA256,
         "point-vector identity")

    edges = raw_edges(source_work / "source_graph.dimacs")
    source_edges = json.loads((source_work / "exact_edges.json").read_text())
    need([list(edge) for edge in edges] == source_edges, "raw/source edge mismatch")
    packed_edges = json.dumps(source_edges, separators=(",", ":")).encode()
    need(hashlib.sha256(packed_edges).hexdigest() == EDGES_SHA256,
         "edge-vector identity")
    wanted_norm = (DENOMINATOR * DENOMINATOR,) + (0,) * 7
    direction_classes = set()
    for u, v in edges:
        difference = tuple(a - b for a, b in zip(parsed[u], parsed[v]))
        direction_classes.add(min(difference, tuple(-x for x in difference)))
        need(squared_distance(parsed[u], parsed[v]) == wanted_norm,
             "declared nonunit edge")

    basis = residue_basis()
    residue_path = review_work / "review_residues.tsv"
    with residue_path.open("w") as stream:
        stream.write(f"{ORDER} {REVIEW_PRIME} {DENOMINATOR}\n")
        for point in parsed:
            x = sum(point[i] * basis[i] for i in range(8)) % REVIEW_PRIME
            y = sum(point[8 + i] * basis[i] for i in range(8)) % REVIEW_PRIME
            stream.write(f"{x} {y}\n")
    result = {
        "status": "INDEPENDENT_VND_COORDINATES_PREPARED",
        "vertices": len(parsed),
        "declared_edges": len(edges),
        "all_declared_edges_exactly_unit": True,
        "distinct_points": len(parsed),
        "coordinate_denominator": DENOMINATOR,
        "direction_classes": len(direction_classes),
        "points_sha256": POINTS_SHA256,
        "edges_sha256": EDGES_SHA256,
        "review_prime": REVIEW_PRIME,
        "review_residues_sha256": digest(residue_path),
    }
    return result


def audit_cnf(source_work, edges):
    triangle = (0, 1, 5)
    need(set(combinations(triangle, 2)) <= set(edges), "palette triangle")
    clauses = ORDER + 4 * EDGE_COUNT + 3
    count = 0
    with (source_work / "gate.cnf").open() as stream:
        need(stream.readline().split() ==
             ["p", "cnf", str(4 * ORDER), str(clauses)], "CNF header")

        def take(expected):
            nonlocal count
            got = tuple(map(int, stream.readline().split()))
            need(got == tuple(expected) + (0,), "CNF clause " + str(count))
            count += 1

        for vertex in range(ORDER):
            take(4 * vertex + 1 + color for color in range(4))
        for u, v in edges:
            for color in range(4):
                take((-(4 * u + color + 1), -(4 * v + color + 1)))
        for color, vertex in enumerate(triangle):
            take((4 * vertex + color + 1,))
        need(stream.read() == "" and count == clauses, "CNF trailing data/count")
    need(digest(source_work / "gate.cnf") == CNF_SHA256, "CNF byte identity")
    return clauses


def finish(source_work, review_work):
    report = json.loads((review_work / "review_sieve.json").read_text())
    need(report == {
        "vertices": ORDER,
        "pairs": ORDER * (ORDER - 1) // 2,
        "survivors": EDGE_COUNT,
        "prime": REVIEW_PRIME,
    }, "review sieve report")
    raw = (review_work / "review_sieve.bin").read_bytes()
    need(len(raw) == 8 * EDGE_COUNT, "review survivor bytes")
    survivors = list(struct.iter_unpack("<II", raw))
    need(survivors == sorted(set(survivors)), "review survivor order/uniqueness")
    edges = raw_edges(source_work / "source_graph.dimacs")
    need(survivors == edges, "independent strict edge census")
    clauses = audit_cnf(source_work, edges)
    return {
        "status": "INDEPENDENT_VND_STRICT_GRAPH_AND_CNF_VERIFIED",
        "vertices": ORDER,
        "all_pairs_audited": ORDER * (ORDER - 1) // 2,
        "strict_unit_edges": len(survivors),
        "independent_sieve_prime": REVIEW_PRIME,
        "independent_sieve_false_positives": 0,
        "survivor_sha256": digest(review_work / "review_sieve.bin"),
        "variables": 4 * ORDER,
        "clauses": clauses,
        "CNF_sha256": CNF_SHA256,
        "palette_triangle": list((0, 1, 5)),
        "at_most_one_clauses_needed": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("prepare", "finish"))
    parser.add_argument("source_work", type=Path)
    parser.add_argument("review_work", type=Path)
    args = parser.parse_args()
    args.review_work.mkdir(parents=True, exist_ok=True)
    result = (prepare(args.source_work.resolve(), args.review_work.resolve())
              if args.mode == "prepare" else
              finish(args.source_work.resolve(), args.review_work.resolve()))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
