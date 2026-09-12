#!/usr/bin/env python3
"""Produce the exact deficit-three overlap and excess-six certificates.

Only the Python standard library is used.  The complete dense order-24
Ramsey-neighborhood reduction is imported through the hash-pinned parent
certificate and its retained graph6 stream.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations
import json
from pathlib import Path


PARENT_CERTIFICATE_SHA256 = (
    "06f05178890e59a3cedf2fd06c8c021e71d9f3685f7571087da25e36fb57bc6e"
)
PARENT_RETAINED_SHA256 = (
    "4a66d825bde6e615c654d307b9567ec4fb7f1abc442ec8f068574d9407126f74"
)
EXCEPTIONAL_DEGREES = (3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4)
EXCEPTIONAL_PROFILE = (120, 358)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def partitions(total, least=1):
    if total == 0:
        yield ()
        return
    for part in range(least, total + 1):
        for rest in partitions(total - part, part):
            yield (part,) + rest


def decode_graph6(line):
    """Decode the fixed order-24 short graph6 form into adjacency sets."""
    need(len(line) == 47 and line[0] == ord("W"), "graph6 header/order")
    need(all(63 <= byte <= 126 for byte in line), "graph6 alphabet")
    adjacency = [set() for _ in range(24)]
    position = 0
    for high in range(1, 24):
        for low in range(high):
            if (line[1 + position // 6] - 63) >> (5 - position % 6) & 1:
                adjacency[low].add(high)
                adjacency[high].add(low)
            position += 1
    need(position == 276, "graph6 pair coverage")
    return adjacency


def rooted_record(adjacency, root):
    common = tuple(sorted(adjacency[root]))
    common_set = set(common)
    common_degree = {vertex: len(adjacency[vertex] & common_set)
                     for vertex in common}
    profile_p = sum(len(adjacency[vertex]) for vertex in common)
    profile_q = 0
    for left, right in combinations(common, 2):
        if right in adjacency[left]:
            profile_q += (len(adjacency[left]) + len(adjacency[right])
                          - len(adjacency[left] & adjacency[right]))
    return {
        "common": common,
        "common_degree": common_degree,
        "degree_sequence": tuple(sorted(common_degree.values())),
        "profile": (profile_p, profile_q),
    }


def common_isomorphisms(left_adjacency, left, right_adjacency, right):
    """Enumerate every degree-preserving isomorphism left C -> right C."""
    left_by_degree = defaultdict(list)
    right_by_degree = defaultdict(list)
    for vertex in left["common"]:
        left_by_degree[left["common_degree"][vertex]].append(vertex)
    for vertex in right["common"]:
        right_by_degree[right["common_degree"][vertex]].append(vertex)
    need(set(left_by_degree) == set(right_by_degree), "degree colors")
    degrees = sorted(left_by_degree)

    def extend(index, mapping):
        if index == len(degrees):
            for u, v in combinations(left["common"], 2):
                if ((v in left_adjacency[u]) !=
                        (mapping[v] in right_adjacency[mapping[u]])):
                    return
            yield dict(mapping)
            return
        degree = degrees[index]
        sources = left_by_degree[degree]
        targets = right_by_degree[degree]
        for image in permutations(targets):
            mapping.update(zip(sources, image))
            yield from extend(index + 1, mapping)
            for source in sources:
                del mapping[source]

    yield from extend(0, {})


def overlap_certificate(parent_certificate, retained_path):
    parent = json.loads(Path(parent_certificate).read_text())
    need(parent["distinct_bucket_profiles"] == 527, "parent profiles")
    need(parent["profile_pair_count"] == 6669, "parent pair count")

    tolerance = 3
    rejected = [0, 0]
    coarse_survivors = []
    for bucket_index, bucket in enumerate(parent["buckets"]):
        common_order = bucket["common_order"]
        degrees = bucket["common_degree_sequence"]
        common_edges = sum(degrees) // 2
        first = common_order * (29 - common_order) + 2 * common_edges
        second = (sum(degree * degree for degree in degrees)
                  + (40 - common_order) * common_edges)
        need((first, second) ==
             (bucket["degree_budget"], bucket["edge_budget"]),
             "parent budget")
        for left, right in combinations_with_replacement(bucket["profiles"], 2):
            if left[0] + right[0] + tolerance < first:
                rejected[0] += 1
            elif left[1] + right[1] + tolerance * max(degrees) < second:
                rejected[1] += 1
            else:
                coarse_survivors.append({
                    "bucket_index": bucket_index,
                    "common_order": common_order,
                    "common_degree_sequence": degrees,
                    "left_profile": left,
                    "right_profile": right,
                    "first_margin": first - left[0] - right[0],
                    "second_margin": second - left[1] - right[1],
                    "maximum_common_degree": max(degrees),
                })
    need(rejected == [5354, 1314], "deficit-three coarse counts")
    need(len(coarse_survivors) == 1, "unique coarse survivor")
    survivor = coarse_survivors[0]
    need(tuple(survivor["common_degree_sequence"]) == EXCEPTIONAL_DEGREES,
         "exceptional degree sequence")
    need(tuple(survivor["left_profile"]) == EXCEPTIONAL_PROFILE and
         tuple(survivor["right_profile"]) == EXCEPTIONAL_PROFILE,
         "exceptional profile")

    occurrences = []
    for retained_index, line in enumerate(Path(retained_path).read_bytes().splitlines()):
        adjacency = decode_graph6(line)
        for root in range(24):
            record = rooted_record(adjacency, root)
            if (record["degree_sequence"] == EXCEPTIONAL_DEGREES and
                    record["profile"] == EXCEPTIONAL_PROFILE):
                occurrences.append({
                    "retained_index": retained_index,
                    "root": root,
                    "adjacency": adjacency,
                    "record": record,
                })
    need(len(occurrences) == 6, "exceptional rooted occurrence count")

    deficit_matrix = []
    isomorphism_matrix = []
    for left in occurrences:
        deficit_row = []
        isomorphism_row = []
        for right in occurrences:
            maps = list(common_isomorphisms(
                left["adjacency"], left["record"],
                right["adjacency"], right["record"]))
            need(len(maps) == 1, "unique common-graph isomorphism")
            mapping = maps[0]
            required = 0
            base_rows = []
            for vertex in left["record"]["common"]:
                image = mapping[vertex]
                base = (24 - len(left["adjacency"][vertex])
                        - len(right["adjacency"][image])
                        + left["record"]["common_degree"][vertex])
                need(base >= 0, "nonnegative undepleted C-to-T degree")
                required += max(0, base - 6)
                base_rows.append(base)
            deficit_row.append(required)
            isomorphism_row.append({
                "isomorphisms": 1,
                "undepleted_C_to_T_degrees": sorted(base_rows),
            })
        deficit_matrix.append(deficit_row)
        isomorphism_matrix.append(isomorphism_row)
    need(min(map(min, deficit_matrix)) == 4, "exception needs deficit four")

    public_occurrences = [{
        "retained_index": item["retained_index"],
        "root": item["root"],
        "common_vertices": list(item["record"]["common"]),
        "common_full_degrees": [
            len(item["adjacency"][vertex]) for vertex in item["record"]["common"]
        ],
        "common_internal_degrees": [
            item["record"]["common_degree"][vertex]
            for vertex in item["record"]["common"]
        ],
    } for item in occurrences]
    return {
        "allowed_common_deficit": tolerance,
        "coarse_profile_pairs": 6669,
        "rejected_by_first_then_second": rejected,
        "coarse_survivors": coarse_survivors,
        "exceptional_rooted_occurrences": public_occurrences,
        "exceptional_ordered_pair_required_deficit": deficit_matrix,
        "exceptional_ordered_pair_isomorphism_data": isomorphism_matrix,
        "minimum_required_common_deficit": min(map(min, deficit_matrix)),
    }


def contains_five_clique(vertices, edges):
    edge_set = set(edges)
    for five in combinations(vertices, 5):
        if all(tuple(sorted(pair)) in edge_set for pair in combinations(five, 2)):
            return True
    return False


def incidence_certificate():
    summaries = []
    internal_graphs_checked = 0
    for excesses in partitions(6):
        exceptional = len(excesses)
        normal = 43 - exceptional
        pairs = list(combinations(range(exceptional), 2))
        baseline = sum(value * (18 + value) for value in excesses)
        maximum_loss = -1
        maximizing_graphs = 0
        admissible_graphs = 0
        for mask in range(1 << len(pairs)):
            edges = [pair for index, pair in enumerate(pairs) if mask >> index & 1]
            internal_graphs_checked += 1
            if contains_five_clique(range(exceptional), edges):
                continue
            admissible_graphs += 1
            loss = sum(excesses[left] + excesses[right] for left, right in edges)
            if loss > maximum_loss:
                maximum_loss = loss
                maximizing_graphs = 1
            elif loss == maximum_loss:
                maximizing_graphs += 1
        lower = baseline - maximum_loss

        # If at most four normal vertices have weighted Z-degree at least 3,
        # the local lemma makes them a clique.  For h=4, each exceptional
        # vertex can meet at most three members of that clique.
        upper_by_h = []
        for high in range(5):
            high_contribution = high * 6 if high <= 3 else 3 * 6
            upper_by_h.append(2 * (normal - high) + high_contribution)
        need(lower > max(upper_by_h), "five qualifying vertices forced")
        summaries.append({
            "positive_excesses": list(excesses),
            "exceptional_vertices": exceptional,
            "normal_vertices": normal,
            "internal_graphs_checked": 1 << len(pairs),
            "K5_free_internal_graphs": admissible_graphs,
            "weighted_incidence_baseline": baseline,
            "maximum_internal_weighted_loss": maximum_loss,
            "maximizing_internal_graphs": maximizing_graphs,
            "weighted_incidence_lower": lower,
            "upper_if_qualifying_count_is_0_to_4": upper_by_h,
            "minimum_gap": lower - max(upper_by_h),
        })
    need(len(summaries) == 11, "partitions of six")
    return summaries, internal_graphs_checked


def produce(parent):
    parent = Path(parent)
    parent_certificate = parent / "CERTIFICATE.json"
    retained = parent / "RETAINED.g6"
    need(digest(parent_certificate) == PARENT_CERTIFICATE_SHA256,
         "parent certificate identity")
    need(digest(retained) == PARENT_RETAINED_SHA256,
         "parent retained identity")
    overlap = overlap_certificate(parent_certificate, retained)
    incidence, internal_graphs = incidence_certificate()
    return {
        "schema": "ramsey-r55-global-degree-excess6-v1",
        "status": "CERTIFIED_GLOBAL_GOOD43_EDGE_WINDOW_391_512",
        "order": 43,
        "degree_window_imported": [18, 24],
        "previous_edge_window_imported": [390, 513],
        "strengthened_edge_window": [391, 512],
        "total_degree_excess_decided_per_color": 6,
        "parent_certificate_sha256": PARENT_CERTIFICATE_SHA256,
        "parent_retained_sha256": PARENT_RETAINED_SHA256,
        "overlap": overlap,
        "degree_excess_partitions": incidence,
        "internal_exception_graphs_checked": internal_graphs,
        "good43_found": False,
        "ramsey_bound_improved": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    certificate = produce(arguments.parent)
    text = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(text)
    else:
        print(text, end="")
