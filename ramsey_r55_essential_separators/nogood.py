#!/usr/bin/env python3
"""Emit a theorem-derived cut clause in 903 lexicographic physical variables.

Input JSON: {"a": [...], "b": [...], "cross_color": 0 or 1}.
The remaining vertices are the separator. This is one valid consequence of
the Ramsey(5,5;43) constraints, not a complete Ramsey CNF or a SAT proof trace.
"""
import json
import sys


def clause(a, b, cross_color):
    if type(cross_color) is not int or cross_color not in (0, 1):
        raise ValueError("cross_color must be 0 or 1")
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("parts must be lists")
    if any(type(v) is not int or not 0 <= v < 43 for v in a + b):
        raise ValueError("invalid vertex")
    if min(len(a), len(b)) < 2 or len(set(a + b)) != len(a + b):
        raise ValueError("parts must be disjoint, nontrivial sets")
    if 43 - len(a) - len(b) > 19:
        raise ValueError("outside the proved separator scope")
    cross = sorted((min(u, v), max(u, v)) for u in a for v in b)
    return [(1 - 2 * cross_color) * (u * (85 - u) // 2 + v - u) for u, v in cross]


if __name__ == "__main__":
    with open(sys.argv[1]) as source:
        data = json.load(source)
    literals = clause(data["a"], data["b"], data["cross_color"])
    print("c Consequence of the separator theorem; not a full Ramsey formula")
    print("p cnf 903 1")
    print(*literals, 0)
