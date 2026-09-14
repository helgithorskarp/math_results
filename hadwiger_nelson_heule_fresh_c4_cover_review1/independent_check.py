#!/usr/bin/env python3
"""Clean-room exact audit of the Heule H510 plus fresh four-cycle cover.

No executable code from the reviewed package is imported.  Squared distances
are computed in two representations: squarefree-radicand products and the
recursive tower Q(sqrt(3))(sqrt(5))(sqrt(11)).
"""

from __future__ import annotations

import argparse
import base64
import json
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_heule_fresh_c4_cover"
UNION = ROOT / "hadwiger_nelson_parts509_heule_union_minimum" / "union_510.json"
FRESH = ROOT / "hadwiger_nelson_heule510_completion_frontier" / "fresh_candidates.json"
CERTIFICATE = TARGET / "certificate.json"
TARGET_EXPECTED = TARGET / "expected.json"
EXPECTED = HERE / "EXPECTED.json"

IDS = (1239, 1370, 1522, 1371)
N_OLD = 510
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ONE = (F(1),) + (F(0),) * 7
PINS = {
    "union": "19d360e5d460ecf1abc6d8e0084046de5e33a05c6c9ff1dff7d26d4ba5e298d9",
    "fresh": "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
    "certificate": "474b98e268ef39e3844619350aa526ce160c889849f1b25e90789c05bbfb52f7",
    "target_expected": "8c6887a6dbdfec2414f6c5be97b175083c15841303ea15e8105e2e52520992c1",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def parse_point(row):
    need(isinstance(row, list) and len(row) == 2, "point axes")
    need(all(isinstance(axis, list) and len(axis) == 8 for axis in row), "point basis")
    return tuple(tuple(F(value) for value in axis) for axis in row)


def flat_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def squarefree_product(left, right):
    out = {radicand: F(0) for radicand in RADICANDS}
    for radicand_left, coefficient_left in zip(RADICANDS, left):
        if not coefficient_left:
            continue
        for radicand_right, coefficient_right in zip(RADICANDS, right):
            if not coefficient_right:
                continue
            common = gcd(radicand_left, radicand_right)
            squarefree = radicand_left * radicand_right // (common * common)
            out[squarefree] += common * coefficient_left * coefficient_right
    return tuple(out[radicand] for radicand in RADICANDS)


def squarefree_norm2(left, right):
    result = (F(0),) * 8
    for axis in range(2):
        difference = tuple(a - b for a, b in zip(left[axis], right[axis]))
        result = flat_add(result, squarefree_product(difference, difference))
    return result


# Recursive tower arithmetic.  Q(sqrt(3)) elements are rational pairs; the
# next two pair layers adjoin sqrt(5) and sqrt(11), respectively.
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


def from_tower(value):
    return (value[0][0][0], value[0][0][1], value[0][1][0], value[0][1][1],
            value[1][0][0], value[1][0][1], value[1][1][0], value[1][1][1])


def tower_norm2(left, right):
    result = to_tower((F(0),) * 8)
    for axis in range(2):
        difference = to_tower(tuple(a - b for a, b in zip(left[axis], right[axis])))
        result = tower_add(result, tower_mul(difference, difference))
    return from_tower(result)


def exact_graph(points):
    edges = []
    metric_agreements = 0
    for left, right in combinations(range(len(points)), 2):
        first = squarefree_norm2(points[left], points[right])
        second = tower_norm2(points[left], points[right])
        need(first == second, f"metric disagreement at {left},{right}")
        need(first != (F(0),) * 8, f"point collision at {left},{right}")
        metric_agreements += 1
        if first == ONE:
            edges.append((left, right))
    return tuple(edges), metric_agreements


def rational_text(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def point_hash(points) -> str:
    text = "".join(" ".join(rational_text(value) for axis in point for value in axis) + "\n"
                   for point in points)
    return sha256(text.encode("ascii")).hexdigest()


def edge_hash(edges) -> str:
    text = "".join(f"{left} {right}\n" for left, right in edges)
    return sha256(text.encode("ascii")).hexdigest()


def decode_word(text, length):
    need(isinstance(text, str), "packed word type")
    raw = base64.b64decode(text, validate=True)
    need(len(raw) == (length + 3) // 4, "packed word length")
    if length % 4:
        need(raw[-1] >> (2 * (length % 4)) == 0, "noncanonical packed padding")
    return tuple((raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(length))


def pack_word(colours):
    raw = bytearray((len(colours) + 3) // 4)
    for index, colour in enumerate(colours):
        need(0 <= colour <= 3, "colour outside range")
        raw[index // 4] |= colour << (2 * (index % 4))
    return base64.b64encode(raw).decode("ascii")


def word_stream_hash(words):
    stream = sha256()
    for omitted, colours in enumerate(words):
        row = "".join("." if index == omitted else str(colour)
                      for index, colour in enumerate(colours))
        stream.update(f"{omitted} {row}\n".encode("ascii"))
    return stream.hexdigest()


def load_inputs():
    paths = {"union": UNION, "fresh": FRESH, "certificate": CERTIFICATE,
             "target_expected": TARGET_EXPECTED}
    for name, path in paths.items():
        need(digest(path) == PINS[name], f"input digest: {name}")
    return tuple(json.loads(paths[name].read_text())
                 for name in ("union", "fresh", "certificate", "target_expected"))


def rejected_decode(text, length):
    try:
        decode_word(text, length)
    except (ValueError, TypeError, base64.binascii.Error):
        return True
    return False


def audit():
    union, fresh_rows, certificate, target_expected = load_inputs()
    need(len(union.get("points", [])) == len(union.get("provenance", [])) == 553,
         "union table shape")
    old = tuple(parse_point(point) for point, provenance
                in zip(union["points"], union["provenance"]) if "510" in provenance)
    need(len(old) == len(set(old)) == N_OLD, "H510 source points")
    need(isinstance(fresh_rows, list) and len(fresh_rows) == 122, "fresh table size")
    fresh = {row.get("centre_index"): row for row in fresh_rows}
    need(len(fresh) == len(fresh_rows), "repeated fresh identifier")
    selected_rows = tuple(fresh[index] for index in IDS)
    selected = tuple(parse_point(row["coordinates"]) for row in selected_rows)
    points = old + selected
    need(len(points) == len(set(points)) == 514, "parent point collision")

    edges, agreements = exact_graph(points)
    old_edges = tuple(edge for edge in edges if edge[1] < N_OLD)
    need(len(edges) == 2525 and len(old_edges) == 2504, "edge census")
    attachments = []
    for offset, row in enumerate(selected_rows):
        vertex = N_OLD + offset
        got = sorted(left for left, right in edges if right == vertex and left < N_OLD)
        need(got == row.get("neighbors"), f"fresh neighbours: {IDS[offset]}")
        need(len(got) == row.get("degree"), f"fresh degree: {IDS[offset]}")
        attachments.append(got)
    fresh_edges = tuple((left - N_OLD, right - N_OLD)
                        for left, right in edges if left >= N_OLD)
    need(fresh_edges == ((0, 1), (0, 3), (1, 2), (2, 3)), "fresh induced C4")
    need(all(sum(vertex in edge for edge in fresh_edges) == 2 for vertex in range(4)),
         "fresh graph is not 2-regular")

    need(certificate.get("schema") == 1, "certificate schema")
    need(certificate.get("centre_ids") == list(IDS), "certificate centre order")
    need(certificate.get("vertices") == 514 and certificate.get("edges") == 2525,
         "certificate graph census")
    packed = certificate.get("packed_singleton_words")
    need(isinstance(packed, list) and len(packed) == N_OLD, "singleton word count")
    words = tuple(decode_word(text, len(points)) for text in packed)
    need(word_stream_hash(words) == certificate.get("word_stream_sha256"), "word stream hash")
    edge_checks = 0
    colour_usage = []
    for omitted, colours in enumerate(words):
        need(colours[N_OLD] == 0, f"fresh normalization: {omitted}")
        for left, right in edges:
            if omitted in (left, right):
                continue
            need(colours[left] != colours[right], f"monochromatic edge: {omitted},{left},{right}")
            edge_checks += 1
        colour_usage.append(len(set(colours[index] for index in range(len(points)) if index != omitted)))
    need(edge_checks == 1_282_725, "retained-edge inequality count")

    # Independent malformed-witness controls.
    left, right = next(edge for edge in edges if 0 not in edge)
    damaged = list(words[0])
    damaged[right] = damaged[left]
    need(any(damaged[a] == damaged[b] for a, b in edges if 0 not in (a, b)),
         "damaged proper word was not rejected")
    raw = bytearray(base64.b64decode(packed[0]))
    raw[-1] |= 0x10
    padding_rejected = rejected_decode(base64.b64encode(raw).decode("ascii"), len(points))
    truncation_rejected = rejected_decode(base64.b64encode(base64.b64decode(packed[0])[:-1]).decode("ascii"), len(points))
    need(padding_rejected and truncation_rejected, "malformed packing accepted")

    expected_projection = {
        "centre_ids": list(IDS),
        "edge_inequalities_checked": edge_checks,
        "edge_sha256": edge_hash(edges),
        "edges": len(edges),
        "every_at_most_509_subgraph_four_colourable": True,
        "fresh_edges_local": [list(edge) for edge in fresh_edges],
        "non_four_signal": False,
        "old_attachment_degrees": [len(row) for row in attachments],
        "old_attachment_union": len(set().union(*map(set, attachments))),
        "record_improved": False,
        "scope": "the fixed exact H510 plus centres 1239,1370,1522,1371 parent",
        "singleton_colourings": len(words),
        "status": "PASS",
        "vertices": len(points),
        "word_stream_sha256": word_stream_hash(words),
    }
    need(expected_projection == target_expected, "target expected output differs")
    need(len(points) - 509 > len(IDS), "pigeonhole coverage premise")

    return {
        "status": "PASS",
        "imports_target_code": False,
        "input_sha256": {
            "union": digest(UNION),
            "fresh": digest(FRESH),
            "certificate": digest(CERTIFICATE),
            "target_expected": digest(TARGET_EXPECTED),
        },
        "parent": {
            "vertices": len(points),
            "edges": len(edges),
            "old_vertices": len(old),
            "old_edges": len(old_edges),
            "pair_checks": len(points) * (len(points) - 1) // 2,
            "two_metric_agreements": agreements,
            "point_sha256": point_hash(points),
            "edge_sha256": edge_hash(edges),
            "centre_ids": list(IDS),
            "old_attachment_degrees": [len(row) for row in attachments],
            "old_attachment_sets": attachments,
            "old_attachment_union": len(set().union(*map(set, attachments))),
            "fresh_edges_local": [list(edge) for edge in fresh_edges],
        },
        "certificate": {
            "singleton_colourings": len(words),
            "edge_inequalities_checked": edge_checks,
            "word_stream_sha256": word_stream_hash(words),
            "all_words_use_four_colours": all(count == 4 for count in colour_usage),
            "damaged_word_rejected": True,
            "padding_rejected": padding_rejected,
            "truncation_rejected": truncation_rejected,
        },
        "logical_scope": {
            "closure_order": 509,
            "parent_vertices": 514,
            "fresh_vertices": 4,
            "old_vertices": 510,
            "minimum_omissions_at_closure_order": 5,
            "reason": "every at-most-509 vertex set omits at least one of the 510 old vertices",
            "every_at_most_509_subgraph_four_colourable": True,
            "record_improvement": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check_expected:
        need(result == json.loads(EXPECTED.read_text()), "independent output differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
