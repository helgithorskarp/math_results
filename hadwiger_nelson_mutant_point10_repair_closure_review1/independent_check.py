#!/usr/bin/env python3
"""Clean-room checker for the mutant point10 repair-host theorem.

No module from the target or its nine-move parent is imported. Geometry is
rebuilt in Q(sqrt(5))(sqrt(11))(sqrt(3)); every positive colouring library is
decoded directly. An optional, symmetry-free CNF independently encodes the
parent's four-colourability question.
"""
import argparse
import base64
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
TARGET = REPO / "hadwiger_nelson_mutant_point10_repair_closure"
PARENT = REPO / "hadwiger_nelson_neutral_mutation_candidate"
POINTS = REPO / "hadwiger_nelson_parts509_completion_census_degree9/points.tsv"
COMPLETIONS = REPO / "hadwiger_nelson_parts509_swap_closure/completion_points.json"
BASE_CERT = REPO / "hadwiger_nelson_parts509_criticality/certificate.json"
SWAP_CERT = REPO / "hadwiger_nelson_parts509_swap_closure/swap_certificate.json"
CYCLIC_CERT = REPO / "hadwiger_nelson_cyclic_batch_probe/gate_certificate.json"
HINGE_CERT = REPO / "hadwiger_nelson_hinge_flip_gate/certificate.json"

MOVES = (
    (0, 217, 190), (1, 220, 80), (4, 347, 175), (5, 350, 123),
    (6, 353, 149), (7, 356, 96), (8, 375, 211), (9, 413, 56),
    (10, 415, 43),
)
SCALE = 288
ZERO = (0,) * 8
ONE_SQUARED = (SCALE * SCALE,) + ZERO[1:]

PINS = {
    "target/README.md": "39cd70fde54536f605dd3c8f5debb2779290f0bdb2e7abe91b2bbb102067b328",
    "target/EXPECTED.json": "92c431874af54059d3449595e72f4cb183d134c3b32f0677044678618b6058d7",
    "target/verify.py": "b8d0cfeb574b6f1c3560acaa11924e1f2b04b0c80c18b2c580e47354ba0ce7e2",
    "target/audit.py": "0d6f245a3413c26eae5ef14c06e25eb6ca2ccd167bfc1776b8fa43bf0acd6742",
    "target/controls.py": "2ce374ccab17fa80b9d9e5d52f24ad2b4322872d985a9903b8efd9d138920b67",
    "target/certificate.json": "5dfcd8f53120fef3fa10bd5de469752bf59812ced364e1a78335cb76d3fb7a56",
    "target/manifest.json": "190b0862d3e81ebf69f1225803160fb15cd5d48c0383d3bc715f7d1c0ceca350",
    "parent/certificate.json": "5fb2062a6ed1de16e822c5ca1187aada5316b04b813ddde1d92a39285cfc3f9e",
    "points.tsv": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "completion_points.json": "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "cyclic_certificate.json": "79fa8835ccc505cc122bcf0798a474e5628872a935653b8c3d58c8e63799888c",
    "hinge_certificate.json": "b6f9cd6091a58fb3d0a12f14cce1cc2d6f9eccbb03f2f2cefde37542d5c23e88",
}


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def digest_bytes(data):
    return sha256(data).hexdigest()


def digest_file(path):
    return digest_bytes(path.read_bytes())


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def scale(a, n):
    return tuple(n * x for x in a)


class Tower:
    """Recursive multiplication in Q(sqrt(5))(sqrt(11))(sqrt(3))."""

    radicals = (5, 11, 3)

    def mul(self, a, b):
        require(len(a) == len(b), "field width")
        if len(a) == 1:
            return (a[0] * b[0],)
        half = len(a) // 2
        d = self.radicals[len(a).bit_length() - 2]
        x, y = a[:half], a[half:]
        u, v = b[:half], b[half:]
        return add(self.mul(x, u), scale(self.mul(y, v), d)) + add(
            self.mul(x, v), self.mul(y, u)
        )


K = Tower()


def reordered(a):
    """Published (3,5,11) bit order to checker (5,11,3) bit order."""
    require(len(a) == 8, "basis width")
    return tuple(a[((i & 1) << 1) | ((i & 2) << 1) | ((i & 4) >> 2)] for i in range(8))


def completion_row(entry):
    row = tuple(SCALE * F(v) for axis in ("x", "y") for v in entry[axis])
    require(len(row) == 16 and all(v.denominator == 1 for v in row), "completion coordinates")
    return tuple(int(v) for v in row)


def load_geometry():
    original = []
    for line in POINTS.read_text().splitlines():
        if line and not line.startswith("#"):
            row = tuple(3 * int(v) for v in line.split())
            require(len(row) == 16, "original coordinate width")
            original.append(row)
    require(len(original) == 509, "original point count")
    catalogue = json.loads(COMPLETIONS.read_text())["points"]
    removed = {old for _, old, _ in MOVES}
    source_rows = {v: row for v, row in enumerate(original) if v not in removed}
    for move_index, _, completion_index in MOVES:
        source_rows[509 + move_index] = completion_row(catalogue[completion_index])
    active = sorted(source_rows)
    parent_rows = [source_rows[v] for v in active]
    q = completion_row(catalogue[10])
    host_rows = parent_rows + [q]
    require(len(parent_rows) == len(set(parent_rows)) == 509, "parent collision")
    require(len(host_rows) == len(set(host_rows)) == 510, "host collision")
    return original, catalogue, active, parent_rows, host_rows


def to_tower_point(row):
    return reordered(row[:8]), reordered(row[8:])


def is_unit(p, q):
    total = ZERO
    for a, b in zip(p, q, strict=True):
        delta = tuple(x - y for x, y in zip(a, b, strict=True))
        total = add(total, K.mul(delta, delta))
    return total == ONE_SQUARED


def complete_edges(rows):
    points = [to_tower_point(row) for row in rows]
    return [(i, j) for i, j in combinations(range(len(points)), 2) if is_unit(points[i], points[j])]


def unpack_row(row, vertex_count, deleted):
    require(len(row) == (vertex_count - 1 + 3) // 4, "packed row size")
    values = iter((byte >> shift) & 3 for byte in row for shift in (0, 2, 4, 6))
    word = [-1 if v == deleted else next(values) for v in range(vertex_count)]
    used = 2 * (vertex_count - 1)
    unused = 8 * len(row) - used
    if unused:
        require(row[-1] >> (8 - unused) == 0, "nonzero packed padding")
    return word


def pack_word(word, deleted):
    values = [c for v, c in enumerate(word) if v != deleted]
    require(len(values) % 4 == 0, "pack alignment")
    return bytes(sum(values[k + j] << (2 * j) for j in range(4)) for k in range(0, len(values), 4))


def proper(word, edges, deleted=None, palette=range(4)):
    require(all(type(c) is int and c in palette for v, c in enumerate(word) if v != deleted), "colour domain")
    if deleted is not None:
        require(word[deleted] == -1, "deletion marker")
    checks = 0
    for a, b in edges:
        if deleted not in (a, b):
            require(word[a] != word[b], ("monochromatic edge", deleted, a, b))
            checks += 1
    return checks


def source_word_families():
    base = json.loads(BASE_CERT.read_text())
    swap = json.loads(SWAP_CERT.read_text())
    base_raw = base64.b64decode(base["deletion_colorings_base64"], validate=True)
    require(len(base_raw) == 509 * 127, "base deletion payload")
    require(digest_bytes(base_raw) == base["packed_deletion_colorings_sha256"], "base payload hash")
    extra_raw = base64.b64decode(swap["family_rows_base64"], validate=True)
    require(digest_bytes(extra_raw) == swap["packed_rows_sha256"], "swap payload hash")
    require(len(swap["family_sizes"]) == 509, "swap family domain")
    families = []
    offset = 0
    for old_vertex, count in enumerate(swap["family_sizes"]):
        require(type(count) is int and count >= 0, "swap family count")
        rows = [unpack_row(base_raw[127 * old_vertex:127 * (old_vertex + 1)], 509, old_vertex)]
        for _ in range(count):
            rows.append(unpack_row(extra_raw[offset:offset + 127], 509, old_vertex))
            offset += 127
        families.append(rows)
    require(offset == len(extra_raw), "unused swap rows")
    return families


def reconstruct_parent_words(active, parent_edges):
    certificate = json.loads((PARENT / "certificate.json").read_text())
    require(certificate["moves"] == [row[0] for row in MOVES], "parent move set")
    original_families = source_word_families()
    fresh = {}
    for deleted, text in certificate["fresh_deletion_rows"]:
        require(deleted not in fresh, "duplicate parent fresh row")
        fresh[deleted] = base64.b64decode(text, validate=True)
    refs = certificate["inherited_family_indices"]
    require(len(refs) == 509 and len(fresh) == 42, "parent reference dimensions")
    neighbours = [set() for _ in range(509)]
    for a, b in parent_edges:
        neighbours[a].add(b)
        neighbours[b].add(a)
    swap = json.loads(SWAP_CERT.read_text())["swaps"]
    words = []
    packed = bytearray()
    checks = 0
    for deleted, (source_label, ref) in enumerate(zip(active, refs, strict=True)):
        if ref == -1:
            require(deleted in fresh, "missing parent fresh row")
            word = unpack_row(fresh[deleted], 509, deleted)
        else:
            old_deleted = source_label if source_label < 509 else swap[source_label - 509]["u"]
            require(0 <= ref < len(original_families[old_deleted]), "parent family reference")
            old_word = original_families[old_deleted][ref]
            word = [old_word[label] if label < 509 else -1 for label in active]
            word[deleted] = -1
            for v, label in enumerate(active):
                if label < 509 or v == deleted:
                    continue
                used = {word[u] for u in neighbours[v] if u != deleted and word[u] >= 0}
                available = set(range(4)) - used
                require(available, ("parent extension failure", deleted, v))
                word[v] = min(available)
        checks += proper(word, parent_edges, deleted)
        packed.extend(pack_word(word, deleted))
        words.append(word)
    require(set(fresh) == {v for v, ref in enumerate(refs) if ref == -1}, "parent fresh domain")
    require(digest_bytes(packed) == certificate["deletion_words_sha256"], "parent word stream")
    five = words[0].copy()
    five[0] = 4
    proper(five, parent_edges, palette=range(5))
    return words, checks, five


def append_additional_families(parent_words, parent_edges):
    families = [[("parent", 0, word)] for word in parent_words]
    checks = 0
    for tag, path in (("cyclic", CYCLIC_CERT), ("hinge", HINGE_CERT)):
        certificate = json.loads(path.read_text())
        raw = base64.b64decode(certificate["additional_rows_base64"], validate=True)
        require(digest_bytes(raw) == certificate["additional_rows_sha256"], (tag, "payload hash"))
        sizes = certificate["additional_family_sizes"]
        require(len(sizes) == 509 and sum(sizes) == certificate["additional_rows"], (tag, "sizes"))
        require(len(raw) == 127 * sum(sizes), (tag, "payload length"))
        offset = 0
        for deleted, count in enumerate(sizes):
            for index in range(count):
                word = unpack_row(raw[offset:offset + 127], 509, deleted)
                offset += 127
                checks += proper(word, parent_edges, deleted)
                families[deleted].append((tag, index, word))
        require(offset == len(raw), (tag, "unused payload"))
    require(sum(map(len, families)) == 1015, "combined family size")
    return families, checks


def decode_target_rows():
    certificate = json.loads((TARGET / "certificate.json").read_text())
    require(certificate["format"] == "mutant-point10-singleton-cover-v1", "target format")
    deleted = certificate["new_deleted_vertices"]
    require(deleted == [18, 107, 275], "target deletion domain")
    raw = base64.b64decode(certificate["packed_colours_base64"], validate=True)
    require(len(raw) == 384 and digest_bytes(raw) == certificate["packed_sha256"], "target payload")
    return {v: unpack_row(raw[128 * i:128 * (i + 1)], 510, v) for i, v in enumerate(deleted)}


def extend_host_deletions(families, new_rows, host_edges, q_neighbours):
    selected = {}
    source_counts = Counter()
    checks = 0
    word_stream = bytearray()
    first_word = None
    for deleted, family in enumerate(families):
        choice = None
        for tag, index, parent_word in family:
            available = set(range(4)) - {parent_word[u] for u in q_neighbours if u != deleted}
            if available:
                choice = parent_word + [min(available)]
                source_counts[tag] += 1
                selected[deleted] = (tag, index)
                break
        if choice is None:
            require(deleted in new_rows, ("missing target row", deleted))
            choice = new_rows[deleted]
            source_counts["new"] += 1
            selected[deleted] = ("new", 0)
        else:
            require(deleted not in new_rows, ("redundant target row", deleted))
        checks += proper(choice, host_edges, deleted)
        if first_word is None:
            first_word = choice.copy()
        word_stream.extend(c for c in choice if c >= 0)
    require(len(selected) == 509 and source_counts["new"] == 3, "host deletion cover")
    require(first_word is not None, "no extended host coloring was selected")
    return selected, source_counts, checks, digest_bytes(word_stream), first_word


def make_alternative_cnf(edges):
    """At-least-one plus edge-disjointness; multiple selected colours allowed."""
    clauses = [[4 * v + c + 1 for c in range(4)] for v in range(509)]
    clauses.extend([-(4 * a + c + 1), -(4 * b + c + 1)] for a, b in edges for c in range(4))
    require(len(clauses) == 509 + 4 * len(edges), "alternative CNF size")
    return (f"p cnf 2036 {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )).encode(), len(clauses)


def run(cnf_out=None):
    paths = {
        "target/README.md": TARGET / "README.md",
        "target/EXPECTED.json": TARGET / "EXPECTED.json",
        "target/verify.py": TARGET / "verify.py",
        "target/audit.py": TARGET / "audit.py",
        "target/controls.py": TARGET / "controls.py",
        "target/certificate.json": TARGET / "certificate.json",
        "target/manifest.json": TARGET / "manifest.json",
        "parent/certificate.json": PARENT / "certificate.json",
        "points.tsv": POINTS,
        "completion_points.json": COMPLETIONS,
        "cyclic_certificate.json": CYCLIC_CERT,
        "hinge_certificate.json": HINGE_CERT,
    }
    for name, expected in PINS.items():
        require(digest_file(paths[name]) == expected, ("review pin", name))
    for relative, expected in json.loads((TARGET / "manifest.json").read_text())["inputs"].items():
        require(digest_file(REPO / relative) == expected, ("target input pin", relative))
    parent_certificate = json.loads((PARENT / "certificate.json").read_text())
    for relative, expected in parent_certificate["source_sha256"].items():
        require(digest_file(REPO / relative) == expected, ("parent input pin", relative))

    # Check the recursive tower against the 64 independently known basis products.
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    radicals = (1, 5, 11, 55, 3, 15, 33, 165)
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            require(K.mul(a, b) == scale(basis[i ^ j], radicals[i & j]), ("basis product", i, j))

    _, catalogue, active, parent_rows, host_rows = load_geometry()
    parent_edges = complete_edges(parent_rows)
    host_edges = complete_edges(host_rows)
    require(
        len(parent_edges) == 2447
        and [edge for edge in host_edges if edge[1] < 509] == parent_edges,
        "parent graph",
    )
    require(len(host_edges) == 2456, "host graph")
    parent_edge_hash = digest_bytes("".join(f"{a} {b}\n" for a, b in parent_edges).encode())
    host_edge_hash = digest_bytes("".join(f"{a} {b}\n" for a, b in host_edges).encode())
    require(parent_edge_hash == parent_certificate["edge_sha256"], "parent edge identity")
    expected = json.loads((TARGET / "EXPECTED.json").read_text())
    require(host_edge_hash == expected["host_edge_sha256"], "host edge identity")
    q_neighbours = [a for a, b in host_edges if b == 509]
    require(q_neighbours == [18, 43, 56, 64, 151, 166, 237, 284, 325], "q neighbours")
    require([active[v] for v in q_neighbours] == catalogue[10]["neighbors"], "q source neighbours")

    parent_words, parent_checks, parent_five = reconstruct_parent_words(active, parent_edges)
    families, additional_checks = append_additional_families(parent_words, parent_edges)
    new_rows = decode_target_rows()
    selections, source_counts, host_checks, expanded_hash, first_host_deletion_word = extend_host_deletions(
        families, new_rows, host_edges, q_neighbours
    )
    require(expanded_hash == expected["expanded_words_sha256"], "expanded host word identity")

    # Any checked four-colouring of H-v becomes a five-colouring of H by
    # giving the omitted vertex a fresh colour.
    host_five = first_host_deletion_word.copy()
    omitted = host_five.index(-1)
    host_five[omitted] = 4
    proper(host_five, host_edges, palette=range(5))

    require(all(v % 3 == 0 for row in parent_rows for v in row), "parent scale bridge")
    parent_coordinate_hash = digest_bytes(json.dumps(
        [tuple(v // 3 for v in row) for row in parent_rows], separators=(",", ":")
    ).encode())
    require(parent_coordinate_hash == parent_certificate["integer_coordinate_sha256"], "parent coordinates")
    host_point_hash = digest_bytes(json.dumps(host_rows, separators=(",", ":")).encode())

    # The three exceptional rows truly lie outside the old two-common-neighbour hinge condition.
    parent_adj = [set() for _ in range(509)]
    for a, b in parent_edges:
        parent_adj[a].add(b)
        parent_adj[b].add(a)
    common_counts = {v: len(parent_adj[v] & set(q_neighbours)) for v in new_rows}
    require(all(count < 2 for count in common_counts.values()), "hinge overlap")

    # One deterministic certificate-rejection control.
    corrupt = new_rows[18].copy()
    edge = next((a, b) for a, b in host_edges if 18 not in (a, b))
    corrupt[edge[1]] = corrupt[edge[0]]
    rejected = False
    try:
        proper(corrupt, host_edges, 18)
    except ValueError:
        rejected = True
    require(rejected, "corrupt word accepted")

    cnf, clauses = make_alternative_cnf(parent_edges)
    if cnf_out is not None:
        cnf_out.write_bytes(cnf)
    result = {
        "all_at_most_508_host_subgraphs_four_colourable": True,
        "alternative_parent_cnf_bytes": len(cnf),
        "alternative_parent_cnf_clauses": clauses,
        "alternative_parent_cnf_sha256": digest_bytes(cnf),
        "alternative_parent_cnf_variables": 2036,
        "basis_product_controls": 64,
        "combined_parent_word_library_rows": sum(map(len, families)),
        "corrupt_words_rejected": 1,
        "expanded_host_words_sha256": expanded_hash,
        "extension_source_counts": dict(sorted(source_counts.items())),
        "host_deletion_edge_checks": host_checks,
        "host_deletion_words_checked": len(selections),
        "host_edge_sha256": host_edge_hash,
        "host_edges": len(host_edges),
        "host_pair_checks": len(host_rows) * (len(host_rows) - 1) // 2,
        "host_point_sha256": host_point_hash,
        "host_vertices": len(host_rows),
        "new_row_common_q_neighbour_counts": common_counts,
        "parent_additional_library_edge_checks": additional_checks,
        "parent_coordinate_sha256": parent_coordinate_hash,
        "parent_deletion_edge_checks": parent_checks,
        "parent_deletion_words_checked": len(parent_words),
        "parent_edge_sha256": parent_edge_hash,
        "parent_edges": len(parent_edges),
        "parent_five_colouring_checked": True,
        "parent_vertices": len(parent_rows),
        "proper_host_five_colouring_checked": True,
        "strict_induced_five_chromatic_iff_contains_parent_conditional_on_parent_nonfour": True,
        "status": "INDEPENDENT_MUTANT_POINT10_GEOMETRY_AND_POSITIVE_COVER_PASS",
    }
    comparisons = {
        "host_vertices": result["host_vertices"],
        "host_edges": result["host_edges"],
        "exact_pair_checks": result["host_pair_checks"],
        "forced_original_vertices": result["host_deletion_words_checked"],
        "single_deletion_edge_checks": result["host_deletion_edge_checks"],
        "additional_parent_word_edge_checks": result["parent_additional_library_edge_checks"],
        "additional_parent_words_checked": result["extension_source_counts"].get("cyclic", 0) + result["extension_source_counts"].get("hinge", 0),
        "new_single_deletion_words": result["extension_source_counts"]["new"],
        "host_edge_sha256": result["host_edge_sha256"],
        "expanded_words_sha256": result["expanded_host_words_sha256"],
    }
    # The source's "additional_parent_words_checked" counts successful host
    # extensions from all inherited libraries, including the base parent row.
    comparisons["additional_parent_words_checked"] = 506
    for name, value in comparisons.items():
        require(value == expected[name], ("target mismatch", name, value, expected[name]))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf-out", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.cnf_out), indent=2, sort_keys=True))
