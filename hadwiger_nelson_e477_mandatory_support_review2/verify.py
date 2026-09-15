#!/usr/bin/env python3
"""Independent exact verifier for the strengthened E477 support bound."""

from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed"
INPUT_HASHES = {
    "certificate.json": "3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237",
    "mandatory_vertices.json": "f0cea2d38b8d43e22bf82cba23ee65fb971cd031918015c9061ee499485cac2d",
}
RADICANDS = (1, 3, 11, 33)
RINDEX = {radicand: index for index, radicand in enumerate(RADICANDS)}
ZERO = (0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def compact_hash(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def edge_line_hash(edges):
    raw = "".join(f"{left} {right}\n" for left, right in edges).encode()
    return sha256(raw).hexdigest()


def fadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def fsub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def fmul(left, right):
    output = [0, 0, 0, 0]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            common = gcd(RADICANDS[i], RADICANDS[j])
            radicand = RADICANDS[i] * RADICANDS[j] // (common * common)
            output[RINDEX[radicand]] += common * a * b
    return tuple(output)


def point(row):
    require(type(row) is list and len(row) == 4 and all(type(value) is int for value in row), "point row")
    a, b, c, d = row
    return (0, a, b, 0), (c, 0, 0, d)


def unit(left, right):
    dx = fsub(left[0], right[0])
    dy = fsub(left[1], right[1])
    return fadd(fmul(dx, dx), fmul(dy, dy)) == (36 * 36, 0, 0, 0)


def proper_source_word(word, edges, omitted=None):
    require(type(word) is str and len(word) == 477 and all(char in "0123" for char in word), "source word")
    require(all(word[u] != word[v] for u, v in edges if omitted not in (u, v)), "source word edge")


def proper_core_word(word, core_edges):
    require(type(word) is str and len(word) == 255 and all(char in "0123" for char in word), "core word")
    require(word[0] != word[1], "core terminals equal")
    require(all(word[u] != word[v] for u, v in core_edges), "core word edge")


def allowed_mask(word, vertex, core_index, adjacency):
    mask = 15
    for neighbour in adjacency[vertex]:
        if neighbour in core_index:
            mask &= ~(1 << int(word[core_index[neighbour]]))
    return mask


def extension_assignment(word, extras, core_index, adjacency):
    masks = [allowed_mask(word, vertex, core_index, adjacency) for vertex in extras]
    for colours in product(range(4), repeat=len(extras)):
        if not all(mask & (1 << colour) for mask, colour in zip(masks, colours)):
            continue
        if all(
            colours[i] != colours[j] or extras[j] not in adjacency[extras[i]]
            for i in range(len(extras))
            for j in range(i + 1, len(extras))
        ):
            return colours
    return None


def validate_certificate(certificate, core, optional, core_edges, adjacency):
    require(certificate.get("format") == "E477 mandatory-core extension colouring cover v1", "format")
    require(certificate.get("input_sha256") == INPUT_HASHES, "certificate input hashes")
    require(certificate.get("core_vertices") == core, "certificate core")
    require(certificate.get("optional_vertices") == optional, "certificate optional vertices")
    require(certificate.get("covered_optional_pairs") == len(optional) * (len(optional) - 1) // 2, "pair count")
    words = certificate.get("core_colourings")
    require(type(words) is list and len(words) == len(set(words)) > 0, "certificate word bank")
    for word in words:
        proper_core_word(word, core_edges)

    core_index = {vertex: index for index, vertex in enumerate(core)}
    coverage_lines = []
    singleton_count = 0
    for vertex in optional:
        for word_index, word in enumerate(words):
            assignment = extension_assignment(word, (vertex,), core_index, adjacency)
            if assignment is not None:
                coverage_lines.append(f"1 {vertex} {word_index} {assignment[0]}\n")
                singleton_count += 1
                break
        else:
            raise ValueError("uncovered singleton: " + str(vertex))

    pair_count = 0
    per_word_pair_coverage = [0] * len(words)
    for left, right in combinations(optional, 2):
        for word_index, word in enumerate(words):
            assignment = extension_assignment(word, (left, right), core_index, adjacency)
            if assignment is not None:
                coverage_lines.append(
                    f"2 {left} {right} {word_index} {assignment[0]} {assignment[1]}\n"
                )
                per_word_pair_coverage[word_index] += 1
                pair_count += 1
                break
        else:
            raise ValueError(f"uncovered pair: {left},{right}")
    require(all(count > 0 for count in per_word_pair_coverage), "unused certificate word")
    return {
        "certificate_core_colourings": len(words),
        "checked_singleton_extensions": singleton_count,
        "checked_pair_extensions": pair_count,
        "per_word_pair_coverage": per_word_pair_coverage,
        "coverage_assignment_sha256": sha256("".join(coverage_lines).encode()).hexdigest(),
    }


def verify(certificate=None):
    for name, expected in INPUT_HASHES.items():
        require(file_hash(SOURCE / name) == expected, "unexpected input hash: " + name)
    equal = json.loads((SOURCE / "certificate.json").read_text())["equal"]
    mandatory = json.loads((SOURCE / "mandatory_vertices.json").read_text())
    require(equal["denominator"] == 1, "source denominator")
    rows = equal["points"]
    require(len(rows) == 477, "source order")
    points = [point(row) for row in rows]
    require(len(set(points)) == 477, "repeated source point")
    edges = [pair for pair in combinations(range(477), 2) if unit(points[pair[0]], points[pair[1]])]
    require(len(edges) == 2458, "source edge census")

    require(type(mandatory) is list and len(mandatory) == 253, "deletion word count")
    deleted = [row["deleted"] for row in mandatory]
    require(deleted == sorted(set(deleted)) and not {0, 1} & set(deleted), "deletion labels")
    for row in mandatory:
        proper_source_word(row["colouring"], edges, omitted=row["deleted"])
        require(row["colouring"][0] != row["colouring"][1], "deletion terminals equal")

    core = sorted({0, 1, *deleted})
    optional = sorted(set(range(477)) - set(core))
    require(len(core) == 255 and len(optional) == 222, "support partition")
    core_index = {old: new for new, old in enumerate(core)}
    core_edges = [
        (core_index[u], core_index[v])
        for u, v in edges
        if u in core_index and v in core_index
    ]
    require(len(core_edges) == 659, "core edge census")
    adjacency = [set() for _ in range(477)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    if certificate is None:
        certificate = json.loads((HERE / "certificate.json").read_text())
    coverage = validate_certificate(certificate, core, optional, core_edges, adjacency)
    result = {
        "status": "VERIFIED_AND_STRENGTHENED",
        "source_points": len(points),
        "source_complete_unit_edges": len(edges),
        "source_edge_sha256": compact_hash([list(edge) for edge in edges]),
        "source_edge_line_sha256": edge_line_hash(edges),
        "checked_deletion_words": len(mandatory),
        "mandatory_core_points": len(core),
        "mandatory_core_complete_unit_edges": len(core_edges),
        "mandatory_core_edge_sha256": compact_hash([list(edge) for edge in core_edges]),
        "mandatory_core_edge_line_sha256": edge_line_hash(core_edges),
        "optional_source_vertices": len(optional),
        "largest_completely_covered_extension_order": len(core) + 2,
        "minimum_E477_equality_forcing_subgraph_order_at_least": len(core) + 3,
        "minimum_sole_bridge_nonfour_order_at_least": 2 * (len(core) + 3) - 1,
        "reviewed_claim_256_and_511_valid": True,
        "record_candidate": False,
        "scope": "subgraphs of fixed E477 and its classified one-overlap sole-cross-edge spindle frames only",
    }
    result.update(coverage)
    return result


def main():
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
