#!/usr/bin/env python3
"""Independent finite audit of Discovery Net h3947.

This checker imports no Python module from the reviewed package.  It rebuilds
C5[C5], re-derives the inner and outer covering argument, validates every
committed factored-certificate witness, and treats the reviewed physical
interface as a black box on newly generated relabeled full graphs.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys


SOURCE_DIRECTORY = "ramsey_r55_pentagon_product_extension_obstruction"
SOURCE_MANIFEST_SHA256 = (
    "6d0030e88916f14a6bf0881d7904a8a4f97d67ebe8035155bf62c94ee4449e6b"
)
SOURCE_CERTIFICATE_SHA256 = (
    "907194bb2f37c86211ca673ba79243bfc74fe5b0651358d94233b9f261030d5e"
)
EQUALITY_WITNESS = "ramsey_r55_path_complement_core_exclusion/WITNESSES.json"
EQUALITY_WITNESS_SHA256 = (
    "16e65ab9efef324cb3daa789bf12d745efcbb19ed74914c93098c7ce901ceb70"
)
ALL5 = (1 << 5) - 1


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest(source):
    manifest = source / "SHA256SUMS"
    need(file_sha256(manifest) == SOURCE_MANIFEST_SHA256,
         "source manifest identity")
    names = []
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        need(name not in names and Path(name).name == name, "manifest path")
        need(file_sha256(source / name) == digest, "source hash " + name)
        names.append(name)
    need(len(names) == len(set(names)) == 21, "source manifest cardinality")
    need(set(names) == {path.name for path in source.iterdir()
                        if path.is_file()} - {"SHA256SUMS"},
         "source manifest file set")
    return names


def cycle_edge(u, v):
    return (u - v) % 5 in (1, 4)


def product_edge(u, v):
    outer_u, inner_u = divmod(u, 5)
    outer_v, inner_v = divmod(v, 5)
    if outer_u == outer_v:
        return cycle_edge(inner_u, inner_v)
    return cycle_edge(outer_u, outer_v)


def adjacency_from_predicate(order, predicate):
    rows = [0] * order
    for u, v in combinations(range(order), 2):
        if predicate(u, v):
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def graph_word(rows):
    word = 0
    for bit, (u, v) in enumerate(combinations(range(len(rows)), 2)):
        if rows[u] >> v & 1:
            word |= 1 << bit
    return word


def verify_core(snapshot, source):
    rows = adjacency_from_predicate(25, product_edge)
    literal = json.loads((source / "CORE.json").read_text())
    word = graph_word(rows)
    need(literal == {
        "bit_order": "low bits for lexicographic unordered pairs",
        "description": "C5[C5]: vertex5*i+j is inner vertex j of outer block i",
        "n": 25,
        "red_edges": 150,
        "red_hex": format(word, "075x"),
    }, "literal core commitment")
    need(sum(row.bit_count() for row in rows) // 2 == 150, "core edges")
    need(Counter(row.bit_count() for row in rows) == {12: 25}, "core degrees")

    five_sets = 0
    monochromatic = 0
    for vertices in combinations(range(25), 5):
        red_pairs = sum(bool(rows[u] >> v & 1)
                        for u, v in combinations(vertices, 2))
        monochromatic += red_pairs in (0, 10)
        five_sets += 1
    need(five_sets == 53130 and monochromatic == 0, "core good25 property")

    witness_path = snapshot / EQUALITY_WITNESS
    need(file_sha256(witness_path) == EQUALITY_WITNESS_SHA256,
         "accepted h3931 witness identity")
    witnesses = json.loads(witness_path.read_text())
    equality = [row for row in witnesses["graphs"]
                if (row["n"], row["omega"], row["alpha"]) == (25, 4, 4)]
    need(len(equality) == 1 and equality[0]["red_bits_hex"] == literal["red_hex"],
         "h3931 equality word")
    return rows, literal["red_hex"], five_sets


def inner_record(word):
    red_vertices = {i for i in range(5) if word >> i & 1}
    blue_vertices = set(range(5)) - red_vertices
    red_pairs = [list(pair) for pair in combinations(range(5), 2)
                 if set(pair) <= red_vertices and cycle_edge(*pair)]
    blue_pairs = [list(pair) for pair in combinations(range(5), 2)
                  if set(pair) <= blue_vertices and not cycle_edge(*pair)]
    tag = int(bool(red_pairs)) | (2 * int(bool(blue_pairs)))
    need(tag, "unmarked inner attachment")
    return {
        "word": word,
        "tag": tag,
        "red_pairs": red_pairs,
        "blue_pairs": blue_pairs,
    }


def is_literal_witness(color, blocks, words, pairs, core_rows):
    red = color == "red"
    vertices = [25]
    for block, pair in zip(blocks, pairs):
        vertices.extend(5 * block + inner for inner in pair)
    if len(vertices) != len(set(vertices)) or len(vertices) != 5:
        return False
    for u, v in combinations(vertices, 2):
        if u == 25 or v == 25:
            z = v if u == 25 else u
            block_index = blocks.index(z // 5)
            edge = bool(words[block_index] >> (z % 5) & 1)
        else:
            edge = bool(core_rows[u] >> v & 1)
        if edge != red:
            return False
    return True


def verify_cover(source, core_rows):
    certificate_path = source / "CERTIFICATE.json"
    need(file_sha256(certificate_path) == SOURCE_CERTIFICATE_SHA256,
         "certificate identity")
    certificate = json.loads(certificate_path.read_text())
    need(certificate["format"] == "pentagon-product-extension-v1",
         "certificate format")

    independent_inner = [inner_record(word) for word in range(32)]
    groups = {tag: [] for tag in (1, 2, 3)}
    source_inner = certificate["inner"]
    need(len(source_inner) == 32, "source inner cardinality")
    for ours, committed in zip(independent_inner, source_inner):
        need(committed["word"] == ours["word"] and
             committed["tag"] == ours["tag"], "source inner tag")
        for color in ("red", "blue"):
            choices = ours[color + "_pairs"]
            selected = committed[color + "_pair"]
            need(selected is None if not choices else selected in choices,
                 "source inner pair")
        groups[ours["tag"]].append(ours["word"])
    tag_counts = {str(tag): len(words) for tag, words in groups.items()}
    need(tag_counts == certificate["tag_counts"] == {"1": 11, "2": 11, "3": 10},
         "tag counts")

    # A tag assignment is equivalently a pair of mark masks whose union is
    # all five outer vertices.  Check directly that none can avoid both an
    # adjacent red pair and a nonadjacent blue pair.
    mark_covers = 0
    avoiding = 0
    for red_mask in range(32):
        for blue_mask in range(32):
            if red_mask | blue_mask != ALL5:
                continue
            mark_covers += 1
            red_obstruction = any((red_mask >> i & 1) and (red_mask >> j & 1)
                                  and cycle_edge(i, j)
                                  for i, j in combinations(range(5), 2))
            blue_obstruction = any((blue_mask >> i & 1) and (blue_mask >> j & 1)
                                   and not cycle_edge(i, j)
                                   for i, j in combinations(range(5), 2))
            avoiding += not red_obstruction and not blue_obstruction
    need(mark_covers == 243 and avoiding == 0, "outer covering theorem")

    rows_by_tags = {tuple(row["tags"]): row for row in certificate["outer"]}
    need(len(certificate["outer"]) == len(rows_by_tags) == 243,
         "source outer cardinality")
    need(set(rows_by_tags) == set(product((1, 2, 3), repeat=5)),
         "source outer coverage")
    attachment_coverage = 0
    physical_checks = 0
    source_color_weights = Counter()
    independent_blue_first_classes = Counter()
    for tags in product((1, 2, 3), repeat=5):
        row = rows_by_tags[tags]
        color = row["color"]
        blocks = row["blocks"]
        need(color in ("red", "blue") and
             isinstance(blocks, list) and blocks == sorted(set(blocks)) and
             len(blocks) == 2, "source outer row shape")
        flag = 1 if color == "red" else 2
        i, j = blocks
        need(tags[i] & flag and tags[j] & flag, "source marked blocks")
        need(cycle_edge(i, j) == (color == "red"), "source outer pair color")
        weight = 1
        for tag in tags:
            weight *= len(groups[tag])
        need(row["attachment_count"] == weight, "source class weight")
        attachment_coverage += weight
        source_color_weights[color] += weight

        own = None
        # Deliberately prefer blue, unlike the reviewed producer.
        for own_color, own_flag, wanted_edge in (("blue", 2, False),
                                                  ("red", 1, True)):
            candidates = [list(pair) for pair in combinations(range(5), 2)
                          if tags[pair[0]] & own_flag and
                          tags[pair[1]] & own_flag and
                          cycle_edge(*pair) == wanted_edge]
            if candidates:
                own = (own_color, candidates[0])
                break
        need(own is not None, "independent outer witness")
        independent_blue_first_classes[own[0]] += 1

        pair_key = color + "_pair"
        for word_i, word_j in product(groups[tags[i]], groups[tags[j]]):
            selected = [source_inner[word_i][pair_key],
                        source_inner[word_j][pair_key]]
            need(is_literal_witness(color, blocks, [word_i, word_j], selected,
                                    core_rows), "committed physical witness")
            physical_checks += 1

    need(attachment_coverage == certificate["attachment_count"] == 1 << 25,
         "all attachment words")
    need(physical_checks == 27015, "selected physical check count")
    need(certificate["free_43_edges"] == 903 - 300 == 603,
         "free physical pair count")
    need(certificate["fixed_ordered_core_family_count"] == 1 << 603,
         "fixed-core family cardinality")
    need(certificate["status"] == "COMPLETE_CORE_EXTENSION_FAMILY_EXCLUDED",
         "certificate status")
    return {
        "attachment_words_covered": attachment_coverage,
        "independent_blue_first_classes": dict(sorted(independent_blue_first_classes.items())),
        "mark_cover_assignments": mark_covers,
        "mark_avoiding_assignments": avoiding,
        "selected_two_block_physical_checks": physical_checks,
        "source_color_weights": dict(sorted(source_color_weights.items())),
        "source_outer_classes": len(rows_by_tags),
        "tag_counts": tag_counts,
    }


def pair_position(order, u, v):
    need(0 <= u < v < order, "ordered pair")
    return u * (2 * order - u - 1) // 2 + v - u - 1


def deterministic_permutation(case):
    return sorted(range(43), key=lambda vertex:
                  sha256(f"review-h3947:{case}:{vertex}".encode()).digest())


def make_physical_request(case):
    permutation = deterministic_permutation(case)
    complement = bool(case & 1)
    value = 0
    for u, v in combinations(range(43), 2):
        if v < 25:
            edge = product_edge(u, v)
        else:
            digest = sha256(f"tail:{case}:{u}:{v}".encode()).digest()
            edge = bool(digest[0] & 1)
        edge ^= complement
        if edge:
            a, b = sorted((permutation[u], permutation[v]))
            value |= 1 << pair_position(43, a, b)
    core_vertices = [permutation[i] for i in range(24, -1, -1)]
    graph = {"n": 43, "red_hex": format(value, "0226x")}
    return {"graph": graph, "core_vertices": core_vertices}, permutation


def graph_rows_from_hex(graph):
    need(graph["n"] == 43 and len(graph["red_hex"]) == 226, "physical graph")
    word = int(graph["red_hex"], 16)
    need(word < 1 << 903, "physical high bit")
    rows = [0] * 43
    for bit, (u, v) in enumerate(combinations(range(43), 2)):
        if word >> bit & 1:
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return rows


def run_interface(source, request, request_path):
    request_path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n")
    completed = subprocess.run(
        [sys.executable, "-B", str(source / "interface.py"), str(request_path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True,
    )
    need(not completed.stderr, "interface stderr")
    return json.loads(completed.stdout)


def verify_physical_certificate(graph, certificate, rows):
    need(certificate["format"] == "physical-monochromatic-five-v1" and
         certificate["n"] == 43, "physical certificate format")
    need(certificate["red_hex_sha256"] ==
         sha256(graph["red_hex"].encode("ascii")).hexdigest(),
         "physical graph binding")
    vertices = certificate["vertices"]
    need(isinstance(vertices, list) and vertices == sorted(set(vertices)) and
         len(vertices) == 5, "physical five vertices")
    red = certificate["color"] == "red"
    need(certificate["color"] in ("red", "blue"), "physical color")
    for u, v in combinations(vertices, 2):
        need(bool(rows[u] >> v & 1) == red, "physical monochromatic pair")
    return 10


def probe_interface(source, work):
    work.mkdir(parents=True)
    probes = 12
    pair_checks = 0
    distinguisher_checks = 0
    transcript = []
    for case in range(probes):
        request, permutation = make_physical_request(case)
        output = run_interface(source, request, work / f"request-{case:02d}.json")
        need(output["status"] == "REJECTED_COMPLETE_CORE_EXTENSION_FAMILY",
             "valid relabeled core rejected")
        mapping = output["ordered_core"]
        need(len(mapping) == len(set(mapping)) == 25 and
             set(mapping) == set(permutation[:25]), "recognized core vertex set")
        rows = graph_rows_from_hex(request["graph"])
        for i, j in combinations(range(25), 2):
            need(bool(rows[mapping[i]] >> mapping[j] & 1) == product_edge(i, j),
                 "recognized core mapping")
            mask = sum(1 << vertex for vertex in mapping)
            distinguished = ((rows[mapping[i]] ^ rows[mapping[j]]) & mask &
                             ~((1 << mapping[i]) | (1 << mapping[j]))).bit_count()
            need(distinguished == (2 if i // 5 == j // 5 else 14),
                 "recognizer distinguisher invariant")
            distinguisher_checks += 1
        need(output["outside_vertex"] == min(set(range(43)) - set(mapping)),
             "selected outside vertex")
        pair_checks += verify_physical_certificate(
            request["graph"], output["certificate"], rows)
        transcript.append({
            "case": case,
            "color": output["certificate"]["color"],
            "complement": bool(case & 1),
            "outside": output["outside_vertex"],
            "vertices": output["certificate"]["vertices"],
        })

    changed, permutation = make_physical_request(100)
    value = int(changed["graph"]["red_hex"], 16)
    u, v = sorted((permutation[0], permutation[1]))
    changed["graph"]["red_hex"] = format(
        value ^ (1 << pair_position(43, u, v)), "0226x")
    changed_output = run_interface(source, changed, work / "changed-core.json")
    need(changed_output["status"] == "OUTSIDE_SPECIFIED_CORE_FAMILY",
         "changed core boundary")
    return {
        "changed_core_outside_family": True,
        "fresh_complemented_probes": probes // 2,
        "fresh_interface_probes": probes,
        "fresh_physical_pairs_checked": pair_checks,
        "recognizer_distinguishers_checked": distinguisher_checks,
        "transcript_sha256": sha256(json.dumps(
            transcript, sort_keys=True, separators=(",", ":")
        ).encode()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    snapshot = args.snapshot.resolve()
    source = snapshot / SOURCE_DIRECTORY
    need(source.is_dir(), "reviewed source directory")
    need(not args.work.exists(), "work path must not exist")
    args.work.mkdir(parents=True)

    manifest = verify_manifest(source)
    core_rows, core_hex, five_sets = verify_core(snapshot, source)
    cover = verify_cover(source, core_rows)
    physical = probe_interface(source, args.work / "physical-probes")
    result = {
        "attachment_words_covered": cover["attachment_words_covered"],
        "changed_core_outside_family": physical["changed_core_outside_family"],
        "core_degree_12_vertices": sum(row.bit_count() == 12 for row in core_rows),
        "core_five_sets_checked": five_sets,
        "core_red_edges": sum(row.bit_count() for row in core_rows) // 2,
        "core_word_sha256": sha256(core_hex.encode("ascii")).hexdigest(),
        "fixed_ordered_core_family_count": 1 << 603,
        "free_physical_edges": 603,
        "fresh_complemented_probes": physical["fresh_complemented_probes"],
        "fresh_interface_probes": physical["fresh_interface_probes"],
        "fresh_physical_pairs_checked": physical["fresh_physical_pairs_checked"],
        "h3931_equality_witness_matches": True,
        "independent_blue_first_classes": cover["independent_blue_first_classes"],
        "inner_tag_counts": cover["tag_counts"],
        "mark_avoiding_assignments": cover["mark_avoiding_assignments"],
        "mark_cover_assignments": cover["mark_cover_assignments"],
        "recognizer_distinguishers_checked": physical["recognizer_distinguishers_checked"],
        "selected_two_block_physical_checks": cover["selected_two_block_physical_checks"],
        "source_certificate_sha256": file_sha256(source / "CERTIFICATE.json"),
        "source_color_weights": cover["source_color_weights"],
        "source_manifest_entries": len(manifest),
        "source_manifest_sha256": file_sha256(source / "SHA256SUMS"),
        "source_outer_classes": cover["source_outer_classes"],
        "status": "INDEPENDENTLY_VERIFIED_H3947_EXTENSION_OBSTRUCTION",
        "target_solver_calls": 0,
        "transcript_sha256": physical["transcript_sha256"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
