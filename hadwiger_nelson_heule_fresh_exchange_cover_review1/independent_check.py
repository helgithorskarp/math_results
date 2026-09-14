#!/usr/bin/env python3
"""Clean-room exact audit of the two Heule fresh-centre exchange covers.

No executable code from the reviewed package is imported.  The two exact
metric implementations below use, respectively, squarefree-radicand products
and a recursive tower Q(sqrt(3))(sqrt(5))(sqrt(11)).
"""

from __future__ import annotations

import argparse
import base64
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path


UNION_SHA256 = "19d360e5d460ecf1abc6d8e0084046de5e33a05c6c9ff1dff7d26d4ba5e298d9"
FRESH_SHA256 = "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317"
CERTIFICATE_SHA256 = "f5ca4de28bf9739598310d61af69ff5748a7b1690e1a1aa7b59ef8d50cfb73b6"
TARGET_EXPECTED_SHA256 = "6e11689b5331196853aa2361ec3199c6e1bd418cc5c74d3c0542574d2404c375"
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ONE_FLAT = (F(1),) + (F(0),) * 7


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_point(row):
    need(isinstance(row, list) and len(row) == 2, "point axes")
    need(all(isinstance(axis, list) and len(axis) == 8 for axis in row), "point basis")
    return tuple(tuple(F(value) for value in axis) for axis in row)


def flat_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def radicand_product(left, right):
    """Multiply basis expansions through squarefree radicand identities."""
    out = {radicand: F(0) for radicand in RADICANDS}
    for r, a in zip(RADICANDS, left):
        if not a:
            continue
        for s, b in zip(RADICANDS, right):
            if not b:
                continue
            common = gcd(r, s)
            out[r * s // (common * common)] += common * a * b
    return tuple(out[radicand] for radicand in RADICANDS)


def radicand_norm2(left, right):
    answer = (F(0),) * 8
    for axis in range(2):
        difference = tuple(a - b for a, b in zip(left[axis], right[axis]))
        answer = flat_add(answer, radicand_product(difference, difference))
    return answer


# A second implementation using the recursive tower
# Q(sqrt(3))(sqrt(5))(sqrt(11)).  A Q(sqrt(3)) element is a pair of Fractions;
# higher elements are pairs over the previous level.
def q3_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def q3_scale(value, scalar):
    return value[0] * scalar, value[1] * scalar


def q3_mul(left, right):
    return (left[0] * right[0] + 3 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def q35_add(left, right):
    return q3_add(left[0], right[0]), q3_add(left[1], right[1])


def q35_scale(value, scalar):
    return q3_scale(value[0], scalar), q3_scale(value[1], scalar)


def q35_mul(left, right):
    return (q3_add(q3_mul(left[0], right[0]), q3_scale(q3_mul(left[1], right[1]), 5)),
            q3_add(q3_mul(left[0], right[1]), q3_mul(left[1], right[0])))


def tower_add(left, right):
    return q35_add(left[0], right[0]), q35_add(left[1], right[1])


def tower_mul(left, right):
    return (q35_add(q35_mul(left[0], right[0]), q35_scale(q35_mul(left[1], right[1]), 11)),
            q35_add(q35_mul(left[0], right[1]), q35_mul(left[1], right[0])))


def to_tower(value):
    return (((value[0], value[1]), (value[2], value[3])),
            ((value[4], value[5]), (value[6], value[7])))


def tower_flat(value):
    return (value[0][0][0], value[0][0][1], value[0][1][0], value[0][1][1],
            value[1][0][0], value[1][0][1], value[1][1][0], value[1][1][1])


def tower_norm2(left, right):
    zero = to_tower((F(0),) * 8)
    answer = zero
    for axis in range(2):
        difference = to_tower(tuple(a - b for a, b in zip(left[axis], right[axis])))
        answer = tower_add(answer, tower_mul(difference, difference))
    return tower_flat(answer)


def exact_graph(points, prefix_size=0, prefix_edges=()):
    """Rebuild a graph, optionally reusing an already audited point prefix."""
    need(0 <= prefix_size <= len(points), "graph prefix size")
    edges = list(prefix_edges)
    agreements = prefix_size * (prefix_size - 1) // 2
    pairs = ((left, right) for right in range(max(1, prefix_size), len(points))
             for left in range(right)) if prefix_size else combinations(range(len(points)), 2)
    for left, right in pairs:
        first = radicand_norm2(points[left], points[right])
        second = tower_norm2(points[left], points[right])
        need(first == second, f"metric disagreement at {left},{right}")
        agreements += 1
        if first == ONE_FLAT:
            edges.append((left, right))
    edges.sort()
    return tuple(edges), agreements


def rational_text(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def point_hash(points) -> str:
    rows = []
    for point in points:
        rows.append(" ".join(rational_text(value) for axis in point for value in axis))
    return sha256(("\n".join(rows) + "\n").encode("ascii")).hexdigest()


def edge_hash(edges) -> str:
    packed = "".join(f"{left} {right}\n" for left, right in edges).encode("ascii")
    return sha256(packed).hexdigest()


def decode_word(text, length):
    need(isinstance(text, str), "packed word type")
    raw = base64.b64decode(text, validate=True)
    need(len(raw) == (length + 3) // 4, "packed word length")
    if length % 4:
        need(raw[-1] >> (2 * (length % 4)) == 0, "noncanonical unused packed bits")
    return tuple((raw[index // 4] >> (2 * (index % 4))) & 3
                 for index in range(length))


def colour_checks(edges, colours, omitted):
    return sum(1 for left, right in edges
               if omitted not in (left, right) and colours[left] != colours[right])


def proper_after_omission(edges, colours, omitted):
    return all(omitted in (left, right) or colours[left] != colours[right]
               for left, right in edges)


def word_hash(words):
    stream = sha256()
    for omitted, colours in enumerate(words):
        row = "".join("." if index == omitted else str(colour)
                      for index, colour in enumerate(colours))
        stream.update(f"{omitted} {row}\n".encode("ascii"))
    return stream.hexdigest()


def load_inputs(union_path, fresh_path, certificate_path, expected_path):
    pins = {
        "union": (union_path, UNION_SHA256),
        "fresh": (fresh_path, FRESH_SHA256),
        "certificate": (certificate_path, CERTIFICATE_SHA256),
        "target_expected": (expected_path, TARGET_EXPECTED_SHA256),
    }
    for name, (path, digest) in pins.items():
        need(file_sha(path) == digest, f"input digest: {name}")
    return tuple(json.loads(path.read_text()) for path, _ in pins.values())


def source_points(union, fresh_rows):
    need(len(union.get("points", [])) == len(union.get("provenance", [])) == 553,
         "union table shape")
    old = tuple(parse_point(point) for point, provenance
                in zip(union["points"], union["provenance"])
                if "510" in provenance)
    need(len(old) == len(set(old)) == 510, "H510 source points")
    need(isinstance(fresh_rows, list) and len(fresh_rows) == 122, "fresh table size")
    fresh = {row.get("centre_index"): row for row in fresh_rows}
    need(len(fresh) == 122, "fresh centre identifiers")
    return old, fresh


def audit_support(spec, old, old_edges, fresh, target_spec):
    ids = spec.get("centre_ids")
    need(ids in ([319], [1074, 1269]), "support identifier")
    need(ids == target_spec.get("centre_ids"), "target support order")
    rows = [fresh[identifier] for identifier in ids]
    points = old + tuple(parse_point(row["coordinates"]) for row in rows)
    need(len(points) == len(set(points)) == 510 + len(ids), "support distinctness")
    edges, agreements = exact_graph(points, len(old), old_edges)
    need(len(edges) == spec.get("edges") == target_spec.get("edges"), "edge census")
    old_edges = tuple(edge for edge in edges if edge[1] < 510)
    need(len(old_edges) == 2504, "old edge census")

    attachments = []
    fresh_edges = []
    for offset, row in enumerate(rows):
        vertex = 510 + offset
        old_neighbours = sorted(left if right == vertex else right
                                for left, right in edges
                                if vertex in (left, right) and min(left, right) < 510)
        need(old_neighbours == row.get("neighbors"), f"old neighbours of {ids[offset]}")
        need(len(old_neighbours) == row.get("degree"), f"old degree of {ids[offset]}")
        attachments.append(old_neighbours)
    for left, right in edges:
        if left >= 510:
            fresh_edges.append((ids[left - 510], ids[right - 510]))
    need(fresh_edges == ([] if len(ids) == 1 else [(1074, 1269)]), "fresh mutual edges")

    packed_words = spec.get("packed_singleton_words")
    need(isinstance(packed_words, list) and len(packed_words) == 510, "word count")
    words = tuple(decode_word(text, len(points)) for text in packed_words)
    stream_digest = word_hash(words)
    need(stream_digest == spec.get("word_stream_sha256"), "certificate word digest")
    need(stream_digest == target_spec.get("word_stream_sha256"), "target word digest")
    checks = 0
    for omitted, colours in enumerate(words):
        need(proper_after_omission(edges, colours, omitted),
             f"monochromatic retained edge for omission {omitted}")
        checks += colour_checks(edges, colours, omitted)
    need(checks == target_spec.get("edge_inequalities_checked"), "colour check count")

    # A direct corruption control, independent of the target controls.
    left, right = next(edge for edge in edges if 0 not in edge)
    damaged = list(words[0])
    damaged[left] = damaged[right]
    need(not proper_after_omission(edges, damaged, 0), "damaged word accepted")

    # The submitted statement stops at 508.  In fact any set of at most 509
    # vertices misses one of the 510 old vertices and is contained in the
    # corresponding certified deletion graph.
    need(len(old) == 510, "old-vertex pigeonhole premise")
    return {
        "centre_ids": ids,
        "vertices": len(points),
        "edges": len(edges),
        "old_edges": len(old_edges),
        "fresh_edges": [list(edge) for edge in fresh_edges],
        "old_attachment_degrees": [len(row) for row in attachments],
        "old_attachment_sets": attachments,
        "pair_checks": len(points) * (len(points) - 1) // 2,
        "two_metric_agreements": agreements,
        "point_sha256": point_hash(points),
        "edge_sha256": edge_hash(edges),
        "singleton_colourings": len(words),
        "edge_inequalities_checked": checks,
        "word_stream_sha256": stream_digest,
        "noncanonical_packed_words": 0,
        "damaged_word_rejected": True,
        "every_at_most_508_subgraph_four_colourable": True,
        "stronger_every_at_most_509_subgraph_four_colourable": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--union", type=Path, required=True)
    parser.add_argument("--fresh", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--target-expected", type=Path, required=True)
    args = parser.parse_args()
    union, fresh_rows, certificate, target_expected = load_inputs(
        args.union, args.fresh, args.certificate, args.target_expected)
    need(certificate.get("schema") == 1, "certificate schema")
    old, fresh = source_points(union, fresh_rows)
    old_edges, old_agreements = exact_graph(old)
    need(len(old_edges) == 2504, "H510 edge census")
    specs = certificate.get("supports")
    targets = target_expected.get("supports")
    need(isinstance(specs, list) and isinstance(targets, list)
         and len(specs) == len(targets) == 2, "support tables")
    supports = [audit_support(spec, old, old_edges, fresh, target)
                for spec, target in zip(specs, targets)]
    need(sum(row["edge_inequalities_checked"] for row in supports)
         == target_expected.get("total_edge_inequalities_checked"), "total colour checks")
    result = {
        "status": "PASS",
        "imports_target_code": False,
        "input_sha256": {
            "union": file_sha(args.union),
            "fresh": file_sha(args.fresh),
            "certificate": file_sha(args.certificate),
            "target_expected": file_sha(args.target_expected),
        },
        "old_graph": {
            "vertices": len(old),
            "edges": len(old_edges),
            "pair_checks": len(old) * (len(old) - 1) // 2,
            "two_metric_agreements": old_agreements,
            "point_sha256": point_hash(old),
            "edge_sha256": edge_hash(old_edges),
        },
        "supports": supports,
        "totals": {
            "support_pair_checks": sum(row["pair_checks"] for row in supports),
            "support_two_metric_agreements": sum(row["two_metric_agreements"] for row in supports),
            "singleton_colourings": sum(row["singleton_colourings"] for row in supports),
            "edge_inequalities_checked": sum(row["edge_inequalities_checked"] for row in supports),
            "damaged_words_rejected": sum(row["damaged_word_rejected"] for row in supports),
        },
        "logical_scope": {
            "submitted_order_bound": 508,
            "independently_justified_order_bound": 509,
            "reason": "any set of at most 509 vertices omits one of the 510 old vertices",
            "record_improvement": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
