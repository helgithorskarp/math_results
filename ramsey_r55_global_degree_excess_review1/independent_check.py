#!/usr/bin/env python3
"""Independent bitset audit of the h4009 global edge-window certificate.

No module from the reviewed package is imported.  The official graph6
catalog is decoded into integer adjacency rows, every dense rooted profile
is reconstructed, and the new deficit-two and global-incidence arguments
are checked independently.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


SOURCE_DIRECTORY = "ramsey_r55_global_degree_excess"
SOURCE_MANIFEST_SHA256 = (
    "a6298b2c49798871a0e88876c1665939290710e538d5effe104d0d4900f882d6"
)
SOURCE_CERTIFICATE_SHA256 = (
    "d030ea15e9529f3dcf6fdefb03f3f64e8eff75cf23aa9359152cce23338c06fe"
)
CATALOG_SHA256 = (
    "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"
)
CATALOG_BYTES = 16_913_568
CATALOG_RECORDS = 352_366
ORDER = 24
ALL24 = (1 << ORDER) - 1


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_source(source):
    manifest = source / "SHA256SUMS"
    need(file_sha256(manifest) == SOURCE_MANIFEST_SHA256,
         "source manifest identity")
    names = []
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        need(Path(name).name == name and name not in names, "manifest path")
        need(file_sha256(source / name) == digest, "source hash " + name)
        names.append(name)
    actual = {path.name for path in source.iterdir() if path.is_file()}
    need(len(names) == 16 and set(names) == actual - {"SHA256SUMS"},
         "source manifest file set")
    need(file_sha256(source / "CERTIFICATE.json") == SOURCE_CERTIFICATE_SHA256,
         "source certificate identity")
    dependencies = json.loads((source / "DEPENDENCIES.json").read_text())
    need(dependencies["catalog_sha256"] == CATALOG_SHA256,
         "catalog dependency identity")
    need(dependencies["imported_mathematics"] == [
        "R(3,5) <= 14",
        "R(4,5) <= 25",
        "Maximum edges in a (4,5;18) graph is at most 85",
        "Completeness of the 352366-record (4,5;24) catalog",
    ], "imported mathematics declaration")
    need(dependencies["parent_files"] == {
        "CERTIFICATE.json":
            "06f05178890e59a3cedf2fd06c8c021e71d9f3685f7571087da25e36fb57bc6e",
        "PROOF.md":
            "bf02881567a64839178aac64e4f292338fccb3fce8b004f03f85011cb265d8bb",
        "RETAINED.g6":
            "4a66d825bde6e615c654d307b9567ec4fb7f1abc442ec8f068574d9407126f74",
    }, "accepted parent dependencies")
    return names


def decode_graph6(line):
    """Decode the fixed order-24 graph6 form without source helpers."""
    need(len(line) == 47 and line[0] == ord("W"), "graph6 order/header")
    payload = 0
    for character in line[1:]:
        need(63 <= character <= 126, "graph6 alphabet")
        payload = (payload << 6) | (character - 63)
    rows = [0] * ORDER
    position = 275
    for high in range(ORDER):
        for low in range(high):
            if payload >> position & 1:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            position -= 1
    need(position == -1, "graph6 pair coverage")
    return payload, rows


def vertices(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length() - 1


def contains_clique(rows, size):
    def search(candidates, left):
        if left == 0:
            return True
        while candidates.bit_count() >= left:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if search(candidates & rows[vertex], left - 1):
                return True
        return False

    return search((1 << len(rows)) - 1, size)


def complement(rows):
    mask = (1 << len(rows)) - 1
    return [mask ^ (1 << vertex) ^ row
            for vertex, row in enumerate(rows)]


def rooted_profile(rows, root):
    common = rows[root]
    chosen = list(vertices(common))
    full_degrees = [row.bit_count() for row in rows]
    common_degrees = [(rows[vertex] & common).bit_count()
                      for vertex in chosen]

    # The common graph must be triangle-free.  Each physical common edge
    # contributes deg(w)+deg(z)-codeg(w,z) to Q.
    q_value = 0
    common_edges = 0
    for left, right in combinations(chosen, 2):
        if rows[left] >> right & 1:
            need(not (rows[left] & rows[right] & common),
                 "common graph triangle")
            common_edges += 1
            q_value += (full_degrees[left] + full_degrees[right]
                        - (rows[left] & rows[right]).bit_count())
    need(2 * common_edges == sum(common_degrees),
         "common graph handshake")
    p_value = sum(full_degrees[vertex] for vertex in chosen)
    return ((len(chosen), tuple(sorted(common_degrees))),
            (p_value, q_value))


def scan_catalog(catalog):
    need(catalog.stat().st_size == CATALOG_BYTES, "catalog bytes")
    need(file_sha256(catalog) == CATALOG_SHA256, "catalog identity")
    lines = catalog.read_bytes().splitlines()
    need(len(lines) == CATALOG_RECORDS, "catalog record count")
    groups = defaultdict(list)
    retained = 0
    ramsey_memberships = 0
    for line in lines:
        payload, rows = decode_graph6(line)
        if payload.bit_count() < 128:
            continue
        retained += 1
        need(not contains_clique(rows, 4), "retained graph contains K4")
        need(not contains_clique(complement(rows), 5),
             "retained graph contains independent five-set")
        ramsey_memberships += 1
        for root in range(ORDER):
            bucket, profile = rooted_profile(rows, root)
            groups[bucket].append(profile)
    need(retained == ramsey_memberships == 1027, "dense catalog coverage")
    need(sum(map(len, groups.values())) == 24_648, "root coverage")
    return groups, retained


def robust_overlap_summary(groups):
    buckets = []
    rejected = [0, 0]
    worst_first_margin = None
    worst_second_margin = None
    for (common_order, degree_sequence), occurrences in sorted(groups.items()):
        profiles = sorted(set(occurrences))
        edge_twice = sum(degree_sequence)
        need(edge_twice % 2 == 0, "degree-sequence parity")
        common_edges = edge_twice // 2
        first_rhs = common_order * (29 - common_order) + 2 * common_edges
        second_rhs = (sum(degree * degree for degree in degree_sequence)
                      + (40 - common_order) * common_edges)
        failures = [0, 0]
        for left, right in combinations_with_replacement(profiles, 2):
            first_margin = first_rhs - left[0] - right[0]
            if first_margin > 2:
                failures[0] += 1
                if worst_first_margin is None or first_margin < worst_first_margin:
                    worst_first_margin = first_margin
                continue
            second_margin = second_rhs - left[1] - right[1]
            need(second_margin > 2 * max(degree_sequence),
                 "profile pair survives deficit-two slack")
            failures[1] += 1
            residual = second_margin - 2 * max(degree_sequence)
            if worst_second_margin is None or residual < worst_second_margin:
                worst_second_margin = residual
        rejected[0] += failures[0]
        rejected[1] += failures[1]
        buckets.append({
            "common_order": common_order,
            "common_degree_sequence": list(degree_sequence),
            "profiles": len(profiles),
            "rejected_by_first_then_second": failures,
        })
    need(len(groups) == 39, "bucket count")
    need(sum(len(set(values)) for values in groups.values()) == 527,
         "distinct profile count")
    need(rejected == [5708, 961], "robust rejection totals")
    return buckets, rejected, worst_first_margin, worst_second_margin


def excess_histograms():
    histograms = []
    for multiplicities in product(range(5), repeat=4):
        excesses = tuple(value for value in range(1, 5)
                         for _ in range(multiplicities[value - 1]))
        if sum(excesses) in (2, 4):
            histograms.append(excesses)
    return sorted(histograms, key=lambda values: (sum(values), values))


def global_incidence_summary():
    summaries = []
    internal_graphs = 0
    for excesses in excess_histograms():
        total = sum(excesses)
        exceptional = len(excesses)
        normal = 43 - exceptional
        possible_edges = list(combinations(range(exceptional), 2))
        baseline = sum(value * (18 + value) for value in excesses)
        minimum = None
        for mask in range(1 << len(possible_edges)):
            loss = sum(excesses[left] + excesses[right]
                       for index, (left, right) in enumerate(possible_edges)
                       if mask >> index & 1)
            incidence = baseline - loss
            minimum = incidence if minimum is None else min(minimum, incidence)
            internal_graphs += 1
        formula = ((19 - exceptional) * total
                   + sum(value * value for value in excesses))
        need(minimum == formula, "weighted incidence formula")
        threshold = total // 2
        qualifying = next(
            count for count in range(normal + 1)
            if count * total + (normal - count) * (threshold - 1) >= minimum
        )
        need(qualifying >= 5, "insufficient qualifying vertices")
        summaries.append({
            "total_excess": total,
            "positive_excesses": list(excesses),
            "normal_vertices": normal,
            "qualifying_threshold": threshold,
            "weighted_incidence_lower": minimum,
            "qualifying_count_lower": qualifying,
        })
    need(len(summaries) == 7 and internal_graphs == 80,
         "exceptional graph coverage")
    return summaries, internal_graphs


def expected_certificate(groups):
    buckets, rejected, first_margin, second_margin = robust_overlap_summary(groups)
    incidence, internal_graphs = global_incidence_summary()
    certificate = {
        "buckets": buckets,
        "catalog_profiles": 527,
        "edge_window": [390, 513],
        "irregular_profiles": incidence,
        "maximum_allowed_common_excess": 2,
        "n": 43,
        "new_irregular_degree_multisets_per_color": 7,
        "profile_pairs": sum(rejected),
        "q10_children_decided": 0,
        "regular_zero_excess_case": "all 43 vertices qualify",
        "rejected_by_first_then_second": rejected,
        "rooted_catalog_records": 24_648,
        "status": "CERTIFIED_GLOBAL_GOOD43_EDGE_WINDOW",
        "target_found": False,
        "whole_packing_tasks_decided": 0,
    }
    return certificate, internal_graphs, first_margin, second_margin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_root", type=Path)
    parser.add_argument("catalog", type=Path)
    args = parser.parse_args()
    source = args.snapshot_root.resolve() / SOURCE_DIRECTORY
    catalog = args.catalog.resolve()
    need(source.is_dir() and catalog.is_file(), "input paths")
    manifest_entries = verify_source(source)
    groups, retained = scan_catalog(catalog)
    rebuilt, internal_graphs, first_margin, second_margin = expected_certificate(groups)
    saved = json.loads((source / "CERTIFICATE.json").read_text())
    need(rebuilt == saved, "complete reviewed certificate")
    receipt = {
        "catalog_records": CATALOG_RECORDS,
        "edge_window": [390, 513],
        "exceptional_graphs": internal_graphs,
        "irregular_degree_multisets": 7,
        "manifest_entries": len(manifest_entries),
        "profile_pairs": 6669,
        "rejected_by_first_then_second": [5708, 961],
        "retained_graphs": retained,
        "root_occurrences": sum(map(len, groups.values())),
        "root_profiles": sum(len(set(values)) for values in groups.values()),
        "smallest_first_stage_exclusion_margin": first_margin,
        "smallest_second_stage_residual_margin": second_margin,
        "status": "INDEPENDENTLY_VERIFIED_GLOBAL_EDGE_WINDOW",
        "surviving_profile_pairs": 0,
        "target_result_established": False,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
