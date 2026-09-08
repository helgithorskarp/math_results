#!/usr/bin/env python3
"""Independent catalog and overlap audit for Discovery Net h3959.

No module from the reviewed package is imported.  The checker decodes the
complete external graph6 catalog into integer adjacency rows, rebuilds every
rooted profile, and treats the reviewed physical interface as a black box on
freshly generated regular graphs.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import subprocess
import sys


SOURCE_DIRECTORY = "ramsey_r55_regular18_overlap_exclusion"
SOURCE_MANIFEST_SHA256 = (
    "c630103de12b71b92a41fb0aba236a881f34ebf786c7921ea7cd94d5f45eefcd"
)
SOURCE_CERTIFICATE_SHA256 = (
    "06f05178890e59a3cedf2fd06c8c021e71d9f3685f7571087da25e36fb57bc6e"
)
SOURCE_RETAINED_SHA256 = (
    "4a66d825bde6e615c654d307b9567ec4fb7f1abc442ec8f068574d9407126f74"
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
    need(len(names) == len(set(names)) == 19, "source manifest cardinality")
    need(set(names) == {path.name for path in source.iterdir()
                        if path.is_file()} - {"SHA256SUMS"},
         "source manifest file set")
    need(file_sha256(source / "CERTIFICATE.json") == SOURCE_CERTIFICATE_SHA256,
         "source certificate identity")
    need(file_sha256(source / "RETAINED.g6") == SOURCE_RETAINED_SHA256,
         "source retained-list identity")
    dependency = json.loads((source / "DEPENDENCIES.json").read_text())
    need(dependency["catalog"] == {
        "url": "https://users.cecs.anu.edu.au/~bdm/data/r45_24.g6",
        "sha256": CATALOG_SHA256,
        "bytes": CATALOG_BYTES,
        "graphs": CATALOG_RECORDS,
        "trust": "Completeness imported; every record selection and all retained Ramsey memberships checked.",
    }, "catalog dependency declaration")
    need(dependency["U18"]["value"] == 85 and
         dependency["U18"]["review_height"] == 2285,
         "accepted U18 dependency")
    need(dependency["small_ramsey"] == {
        "R35": 14,
        "R45": 25,
        "source": "https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf",
    }, "small Ramsey dependency declaration")
    return names


def decode_graph6(line):
    """Decode the fixed n=24 graph6 form using one 276-bit integer."""
    need(len(line) == 47 and line[0] == ord("W"), "graph6 order/header")
    payload = 0
    for character in line[1:]:
        need(63 <= character <= 126, "graph6 alphabet")
        payload = (payload << 6) | (character - 63)
    need(payload < 1 << 276, "graph6 payload")
    rows = [0] * ORDER
    position = 275
    for upper in range(ORDER):
        for lower in range(upper):
            if payload >> position & 1:
                rows[lower] |= 1 << upper
                rows[upper] |= 1 << lower
            position -= 1
    need(position == -1, "graph6 pair coverage")
    return payload, rows


def contains_clique(rows, size):
    """Exact bitset search with a size bound; rows exclude self-loops."""
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
    return [mask ^ (1 << vertex) ^ neighbors
            for vertex, neighbors in enumerate(rows)]


def triangle_free_on(rows, chosen):
    scan = chosen
    while scan:
        bit = scan & -scan
        scan ^= bit
        vertex = bit.bit_length() - 1
        neighbors = rows[vertex] & chosen
        probe = neighbors
        while probe:
            other_bit = probe & -probe
            probe ^= other_bit
            other = other_bit.bit_length() - 1
            if rows[other] & neighbors:
                return False
    return True


def vertices(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length() - 1


def rooted_profile(rows, root):
    common = rows[root]
    common_vertices = list(vertices(common))
    degrees = [row.bit_count() for row in rows]
    within = {vertex: (rows[vertex] & common).bit_count()
              for vertex in common_vertices}
    need(triangle_free_on(rows, common), "root common graph triangle")
    p_value = sum(degrees[vertex] for vertex in common_vertices)

    # Compute Q in two algebraically equivalent ways.  The first is a sum of
    # physical edge scores; the second is the stated vertex-weight formula.
    q_edges = 0
    common_neighbor_sum = 0
    for left, right in combinations(common_vertices, 2):
        if rows[left] >> right & 1:
            shared = (rows[left] & rows[right]).bit_count()
            q_edges += degrees[left] + degrees[right] - shared
            common_neighbor_sum += shared
    q_vertices = (sum(within[vertex] * degrees[vertex]
                      for vertex in common_vertices) - common_neighbor_sum)
    need(q_edges == q_vertices, "two Q formulas")
    return (len(common_vertices), tuple(sorted(within.values()))), (p_value, q_edges)


def scan_catalog(catalog, source):
    need(catalog.stat().st_size == CATALOG_BYTES, "catalog bytes")
    need(file_sha256(catalog) == CATALOG_SHA256, "catalog identity")
    lines = catalog.read_bytes().splitlines()
    need(len(lines) == CATALOG_RECORDS, "catalog record count")

    histogram = Counter()
    retained_lines = []
    decoded = []
    for line in lines:
        payload, rows = decode_graph6(line)
        edges = payload.bit_count()
        histogram[edges] += 1
        if edges >= 128:
            retained_lines.append(line)
            decoded.append(rows)
    need(len(retained_lines) == 1027, "retained catalog count")
    need((source / "RETAINED.g6").read_bytes() ==
         b"\n".join(retained_lines) + b"\n", "complete retained sequence")

    profiles = defaultdict(list)
    ramsey_checks = 0
    for rows in decoded:
        need(not contains_clique(rows, 4), "retained K4")
        need(not contains_clique(complement(rows), 5), "retained independent five")
        ramsey_checks += 1
        for root in range(ORDER):
            bucket, profile = rooted_profile(rows, root)
            profiles[bucket].append(profile)

    need(sum(map(len, profiles.values())) == 24648, "rooted profile coverage")
    return histogram, profiles, ramsey_checks


def rebuild_certificate(histogram, groups):
    buckets = []
    rejected = [0, 0]
    first_pass_pairs = 0
    best_second_slack_after_first = None
    best_joint_margin = None
    survivors = []
    for (common_order, degree_sequence), occurrences in sorted(groups.items()):
        edge_twice = sum(degree_sequence)
        need(edge_twice % 2 == 0, "common-graph handshake")
        common_edges = edge_twice // 2
        degree_budget = common_order * (29 - common_order) + 2 * common_edges
        edge_budget = (sum(value * value for value in degree_sequence) +
                       (40 - common_order) * common_edges)
        unique_profiles = sorted(set(occurrences))
        failures = [0, 0]
        for left, right in combinations_with_replacement(unique_profiles, 2):
            first_slack = left[0] + right[0] - degree_budget
            second_slack = left[1] + right[1] - edge_budget
            joint_margin = min(first_slack, second_slack)
            if best_joint_margin is None or joint_margin > best_joint_margin:
                best_joint_margin = joint_margin
            if first_slack < 0:
                failures[0] += 1
            elif second_slack < 0:
                failures[1] += 1
                first_pass_pairs += 1
                if (best_second_slack_after_first is None or
                        second_slack > best_second_slack_after_first):
                    best_second_slack_after_first = second_slack
            else:
                survivors.append({
                    "bucket": [common_order, list(degree_sequence)],
                    "left": list(left),
                    "right": list(right),
                    "slacks": [first_slack, second_slack],
                })
        rejected[0] += failures[0]
        rejected[1] += failures[1]
        buckets.append({
            "common_order": common_order,
            "common_degree_sequence": list(degree_sequence),
            "root_count": len(occurrences),
            "profiles": [list(profile) for profile in unique_profiles],
            "degree_budget": degree_budget,
            "edge_budget": edge_budget,
            "rejected_by_first_then_second": failures,
        })
    need(not survivors, "surviving compatibility profile")
    certificate = {
        "schema": 1,
        "status": "COMPLETE_REGULAR18_AND24_GOOD43_EXCLUSION",
        "catalog_sha256": CATALOG_SHA256,
        "catalog_count": CATALOG_RECORDS,
        "edge_histogram": {str(edges): count
                           for edges, count in sorted(histogram.items())},
        "retained_count": sum(bucket["root_count"] for bucket in buckets) // 24,
        "root_count": sum(bucket["root_count"] for bucket in buckets),
        "bucket_count": len(buckets),
        "distinct_bucket_profiles": sum(len(bucket["profiles"])
                                        for bucket in buckets),
        "profile_pair_count": sum(rejected),
        "rejected_by_first_then_second": rejected,
        "buckets": buckets,
    }
    need(first_pass_pairs == rejected[1], "second-stage count")
    return certificate, best_joint_margin, best_second_slack_after_first


def pair_position(order, left, right):
    need(0 <= left < right < order, "ordered physical pair")
    return left * (2 * order - left - 1) // 2 + right - left - 1


def deterministic_permutation(case):
    return sorted(range(43), key=lambda vertex:
                  sha256(f"review-h3959:{case}:{vertex}".encode()).digest())


def connection_set(case, half_degree):
    return set(sorted(range(1, 22), key=lambda distance:
                      sha256(f"distances:{case}:{distance}".encode()).digest())
               [:half_degree])


def make_regular_graph(case, degree):
    distances = connection_set(case, degree // 2)
    permutation = deterministic_permutation(case)
    word = 0
    for left, right in combinations(range(43), 2):
        difference = min((left - right) % 43, (right - left) % 43)
        if difference in distances:
            physical = sorted((permutation[left], permutation[right]))
            word |= 1 << pair_position(43, *physical)
    return {"n": 43, "red_hex": format(word, "0226x")}


def physical_rows(graph):
    need(graph["n"] == 43 and len(graph["red_hex"]) == 226, "physical graph")
    word = int(graph["red_hex"], 16)
    need(word < 1 << 903, "physical graph high bit")
    rows = [0] * 43
    for bit, (left, right) in enumerate(combinations(range(43), 2)):
        if word >> bit & 1:
            rows[left] |= 1 << right
            rows[right] |= 1 << left
    return rows


def run_interface(source, graph, path):
    path.write_text(json.dumps(graph, sort_keys=True) + "\n")
    completed = subprocess.run(
        [sys.executable, "-B", str(source / "interface.py"), str(path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True,
    )
    need(not completed.stderr, "interface stderr")
    return json.loads(completed.stdout)


def verify_interface(source, work):
    work.mkdir(parents=True)
    probes = []
    physical_pairs = 0
    for case in range(12):
        degree = 18 if case < 6 else 24
        graph = make_regular_graph(case, degree)
        rows = physical_rows(graph)
        need(Counter(row.bit_count() for row in rows) == {degree: 43},
             "fresh graph regularity")
        output = run_interface(source, graph, work / f"regular-{case:02d}.json")
        need(output["status"] == "REJECTED_COMPLETE_REGULAR18_OR24_FAMILY" and
             output["regular_degree"] == degree, "fresh interface result")
        need(output["graph_word_sha256"] ==
             sha256(graph["red_hex"].encode("ascii")).hexdigest(),
             "physical certificate binding")
        chosen = output["vertices"]
        need(isinstance(chosen, list) and len(chosen) == len(set(chosen)) == 5,
             "physical five-set")
        need(all(type(vertex) is int and 0 <= vertex < 43 for vertex in chosen),
             "physical vertex range")
        color = output["color"]
        need(color in (0, 1), "physical color")
        for left, right in combinations(chosen, 2):
            need(bool(rows[left] >> right & 1) == bool(color),
                 "physical monochromatic pair")
            physical_pairs += 1
        probes.append({
            "case": case,
            "color": color,
            "degree": degree,
            "vertices": chosen,
        })

    irregular = make_regular_graph(100, 18)
    irregular["red_hex"] = format(int(irregular["red_hex"], 16) ^ 1, "0226x")
    outside = run_interface(source, irregular, work / "irregular.json")
    need(outside["status"] == "OUTSIDE_PROVED_REGULAR_BRANCH",
         "irregular scope boundary")
    return {
        "fresh_interface_probes": len(probes),
        "fresh_degree18_probes": sum(row["degree"] == 18 for row in probes),
        "fresh_degree24_probes": sum(row["degree"] == 24 for row in probes),
        "fresh_physical_pairs_checked": physical_pairs,
        "irregular_graph_outside_branch": True,
        "interface_transcript_sha256": sha256(json.dumps(
            probes, sort_keys=True, separators=(",", ":")
        ).encode()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    snapshot = args.snapshot.resolve()
    source = snapshot / SOURCE_DIRECTORY
    catalog = args.catalog.resolve()
    need(source.is_dir(), "reviewed source directory")
    need(not args.work.exists(), "work path must not exist")
    args.work.mkdir(parents=True)

    manifest = verify_source(source)
    histogram, groups, ramsey_checks = scan_catalog(catalog, source)
    rebuilt, best_joint_margin, best_second_slack = rebuild_certificate(
        histogram, groups)
    committed = json.loads((source / "CERTIFICATE.json").read_text())
    need(rebuilt == committed, "certificate entry-level comparison")
    interface = verify_interface(source, args.work / "interface-probes")

    # Recheck the deterministic algebra entering the 18-to-24 complement
    # reduction, apart from the imported U(18)=85 extremum itself.
    for a_edges in range(86):
        b_edges = 213 - a_edges
        need(306 - 2 * a_edges == 2 * b_edges - 120,
             "cross-edge identity")
        need(b_edges >= 128, "U18 threshold implication")

    receipt = {
        "best_joint_profile_margin": best_joint_margin,
        "best_second_slack_after_first": best_second_slack,
        "catalog_bytes": catalog.stat().st_size,
        "catalog_records": CATALOG_RECORDS,
        "catalog_sha256": file_sha256(catalog),
        "checked_retained_ramsey_graphs": ramsey_checks,
        "degree_sequence_buckets": rebuilt["bucket_count"],
        "distinct_bucket_profiles": rebuilt["distinct_bucket_profiles"],
        "edge_histogram_128_through_132": {
            str(edges): histogram[edges] for edges in range(128, 133)
        },
        "fresh_degree18_probes": interface["fresh_degree18_probes"],
        "fresh_degree24_probes": interface["fresh_degree24_probes"],
        "fresh_interface_probes": interface["fresh_interface_probes"],
        "fresh_physical_pairs_checked": interface["fresh_physical_pairs_checked"],
        "interface_transcript_sha256": interface["interface_transcript_sha256"],
        "irregular_graph_outside_branch": interface["irregular_graph_outside_branch"],
        "profile_pairs": rebuilt["profile_pair_count"],
        "rejected_by_first_then_second": rebuilt["rejected_by_first_then_second"],
        "retained_graphs": rebuilt["retained_count"],
        "rooted_graphs": rebuilt["root_count"],
        "source_certificate_sha256": file_sha256(source / "CERTIFICATE.json"),
        "source_manifest_entries": len(manifest),
        "source_manifest_sha256": file_sha256(source / "SHA256SUMS"),
        "source_retained_sha256": file_sha256(source / "RETAINED.g6"),
        "status": "INDEPENDENTLY_VERIFIED_H3959_REGULAR18_24_EXCLUSION",
        "surviving_profile_pairs": 0,
        "target_result_established": False,
        "target_solver_calls": 0,
        "u18_imported_value": 85,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
