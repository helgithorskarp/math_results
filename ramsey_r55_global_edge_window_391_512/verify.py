#!/usr/bin/env python3
"""Independent bitset verifier for the excess-six edge-window certificate.

This checker imports no producer module.  It uses bit rows, a recursive
colored-graph isomorphism search, and an independent histogram enumeration.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path


PARENT_CERTIFICATE_SHA256 = (
    "06f05178890e59a3cedf2fd06c8c021e71d9f3685f7571087da25e36fb57bc6e"
)
PARENT_RETAINED_SHA256 = (
    "4a66d825bde6e615c654d307b9567ec4fb7f1abc442ec8f068574d9407126f74"
)
SPECIAL_DEGREES = (3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4)
SPECIAL_PROFILE = (120, 358)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def decode(line):
    need(len(line) == 47 and line[0] == ord("W"), "graph6 order")
    payload = 0
    for byte in line[1:]:
        need(63 <= byte <= 126, "graph6 payload")
        payload = payload << 6 | (byte - 63)
    rows = [0] * 24
    position = 275
    for high in range(24):
        for low in range(high):
            if payload >> position & 1:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            position -= 1
    need(position == -1, "graph6 bits")
    return rows


def vertices(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length() - 1


def root_data(rows, root):
    common_mask = rows[root]
    common = tuple(vertices(common_mask))
    internal = {vertex: (rows[vertex] & common_mask).bit_count()
                for vertex in common}
    p_value = sum(rows[vertex].bit_count() for vertex in common)
    q_value = 0
    for left, right in combinations(common, 2):
        if rows[left] >> right & 1:
            q_value += (rows[left].bit_count() + rows[right].bit_count()
                        - (rows[left] & rows[right]).bit_count())
    return common, internal, tuple(sorted(internal.values())), (p_value, q_value)


def isomorphisms(left_rows, left_common, left_degree,
                 right_rows, right_common, right_degree):
    """Backtrack all isomorphisms, testing edges and nonedges immediately."""
    order = sorted(left_common,
                   key=lambda vertex: (-left_degree[vertex], vertex))
    candidates = {
        vertex: [image for image in right_common
                 if right_degree[image] == left_degree[vertex]]
        for vertex in order
    }
    mapping = {}
    used = set()

    def visit(index):
        if index == len(order):
            yield dict(mapping)
            return
        vertex = order[index]
        for image in candidates[vertex]:
            if image in used:
                continue
            if any(((left_rows[vertex] >> previous & 1) !=
                    (right_rows[image] >> mapping[previous] & 1))
                   for previous in mapping):
                continue
            mapping[vertex] = image
            used.add(image)
            yield from visit(index + 1)
            used.remove(image)
            del mapping[vertex]

    yield from visit(0)


def enumerate_histograms(total):
    output = set()
    for multiplicities in product(range(total + 1), repeat=total):
        if sum((index + 1) * count
               for index, count in enumerate(multiplicities)) != total:
            continue
        output.add(tuple(value for value, count in enumerate(multiplicities, 1)
                         for _ in range(count)))
    return sorted(output, key=lambda values: (len(values), values), reverse=True)


def has_k5(vertex_count, edge_mask, pair_index):
    for chosen in combinations(range(vertex_count), 5):
        if all(edge_mask >> pair_index[tuple(sorted(pair))] & 1
               for pair in combinations(chosen, 2)):
            return True
    return False


def reconstruct(parent_path):
    parent_path = Path(parent_path)
    parent_certificate_path = parent_path / "CERTIFICATE.json"
    retained_path = parent_path / "RETAINED.g6"
    need(file_hash(parent_certificate_path) == PARENT_CERTIFICATE_SHA256,
         "parent certificate SHA256")
    need(file_hash(retained_path) == PARENT_RETAINED_SHA256,
         "parent retained SHA256")
    parent = json.loads(parent_certificate_path.read_text())

    rejected = [0, 0]
    survivors = []
    for bucket_index, bucket in enumerate(parent["buckets"]):
        degrees = tuple(bucket["common_degree_sequence"])
        order = bucket["common_order"]
        edges = sum(degrees) // 2
        first_rhs = order * (29 - order) + 2 * edges
        second_rhs = sum(value * value for value in degrees) + (40 - order) * edges
        for left, right in combinations_with_replacement(bucket["profiles"], 2):
            first_margin = first_rhs - left[0] - right[0]
            second_margin = second_rhs - left[1] - right[1]
            if first_margin > 3:
                rejected[0] += 1
            elif second_margin > 3 * max(degrees):
                rejected[1] += 1
            else:
                survivors.append({
                    "bucket_index": bucket_index,
                    "common_order": order,
                    "common_degree_sequence": list(degrees),
                    "left_profile": left,
                    "right_profile": right,
                    "first_margin": first_margin,
                    "second_margin": second_margin,
                    "maximum_common_degree": max(degrees),
                })
    need(rejected == [5354, 1314] and len(survivors) == 1,
         "deficit-three coarse classification")

    occurrences = []
    lines = retained_path.read_bytes().splitlines()
    need(len(lines) == 1027, "retained record count")
    for retained_index, line in enumerate(lines):
        rows = decode(line)
        for root in range(24):
            common, internal, degrees, profile = root_data(rows, root)
            if degrees == SPECIAL_DEGREES and profile == SPECIAL_PROFILE:
                occurrences.append((retained_index, root, rows, common, internal))
    need(len(occurrences) == 6, "special rooted occurrences")

    public_occurrences = []
    deficit_matrix = []
    iso_data = []
    for retained_index, root, rows, common, internal in occurrences:
        public_occurrences.append({
            "retained_index": retained_index,
            "root": root,
            "common_vertices": list(common),
            "common_full_degrees": [rows[vertex].bit_count() for vertex in common],
            "common_internal_degrees": [internal[vertex] for vertex in common],
        })
    for _, _, left_rows, left_common, left_internal in occurrences:
        deficit_row = []
        iso_row = []
        for _, _, right_rows, right_common, right_internal in occurrences:
            maps = list(isomorphisms(
                left_rows, left_common, left_internal,
                right_rows, right_common, right_internal))
            need(len(maps) == 1, "asymmetric common graph")
            mapping = maps[0]
            undepleted = []
            for vertex in left_common:
                image = mapping[vertex]
                undepleted.append(
                    24 - left_rows[vertex].bit_count()
                    - right_rows[image].bit_count() + left_internal[vertex]
                )
            need(min(undepleted) >= 0, "undepleted degree nonnegative")
            deficit_row.append(sum(max(0, degree - 6) for degree in undepleted))
            iso_row.append({
                "isomorphisms": len(maps),
                "undepleted_C_to_T_degrees": sorted(undepleted),
            })
        deficit_matrix.append(deficit_row)
        iso_data.append(iso_row)
    need(min(map(min, deficit_matrix)) == 4, "physical survivor eliminated")

    overlap = {
        "allowed_common_deficit": 3,
        "coarse_profile_pairs": 6669,
        "rejected_by_first_then_second": rejected,
        "coarse_survivors": survivors,
        "exceptional_rooted_occurrences": public_occurrences,
        "exceptional_ordered_pair_required_deficit": deficit_matrix,
        "exceptional_ordered_pair_isomorphism_data": iso_data,
        "minimum_required_common_deficit": min(map(min, deficit_matrix)),
    }

    summaries = []
    internal_graphs_checked = 0
    for excesses in enumerate_histograms(6):
        z_size = len(excesses)
        normal = 43 - z_size
        pairs = list(combinations(range(z_size), 2))
        pair_index = {pair: index for index, pair in enumerate(pairs)}
        baseline = sum(value * (18 + value) for value in excesses)
        maximum_loss = -1
        maximizers = 0
        admissible = 0
        for edge_mask in range(1 << len(pairs)):
            internal_graphs_checked += 1
            if has_k5(z_size, edge_mask, pair_index):
                continue
            admissible += 1
            loss = sum(excesses[left] + excesses[right]
                       for index, (left, right) in enumerate(pairs)
                       if edge_mask >> index & 1)
            if loss > maximum_loss:
                maximum_loss = loss
                maximizers = 1
            elif loss == maximum_loss:
                maximizers += 1
        lower = baseline - maximum_loss
        upper = [2 * (normal - high) + (6 * high if high < 4 else 18)
                 for high in range(5)]
        need(lower > max(upper), "incidence forces five qualifiers")
        summaries.append({
            "positive_excesses": list(excesses),
            "exceptional_vertices": z_size,
            "normal_vertices": normal,
            "internal_graphs_checked": 1 << len(pairs),
            "K5_free_internal_graphs": admissible,
            "weighted_incidence_baseline": baseline,
            "maximum_internal_weighted_loss": maximum_loss,
            "maximizing_internal_graphs": maximizers,
            "weighted_incidence_lower": lower,
            "upper_if_qualifying_count_is_0_to_4": upper,
            "minimum_gap": lower - max(upper),
        })
    # Match the producer's ordinary nondecreasing partition order.
    summaries.sort(key=lambda item: item["positive_excesses"])

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
        "degree_excess_partitions": summaries,
        "internal_exception_graphs_checked": internal_graphs_checked,
        "good43_found": False,
        "ramsey_bound_improved": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    arguments = parser.parse_args()
    expected = reconstruct(arguments.parent)
    actual = json.loads(arguments.certificate.read_text())
    need(expected == actual, "complete certificate comparison")
    print(json.dumps({
        "status": "VERIFIED_GLOBAL_GOOD43_EDGE_WINDOW_391_512",
        "edge_window": expected["strengthened_edge_window"],
        "coarse_profile_pairs": expected["overlap"]["coarse_profile_pairs"],
        "coarse_survivors": len(expected["overlap"]["coarse_survivors"]),
        "physical_occurrences": len(
            expected["overlap"]["exceptional_rooted_occurrences"]),
        "physical_ordered_gluings": 36,
        "minimum_required_common_deficit":
            expected["overlap"]["minimum_required_common_deficit"],
        "degree_excess_partitions": len(expected["degree_excess_partitions"]),
        "internal_exception_graphs_checked":
            expected["internal_exception_graphs_checked"],
    }, sort_keys=True))
