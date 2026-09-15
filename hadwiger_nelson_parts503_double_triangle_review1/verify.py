#!/usr/bin/env python3
"""Independent exact verifier for the Parts503 double-triangle family."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

BASE = Path(__file__).resolve().parent
PRIMES = (3, 5, 11)
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
DENOMINATOR = 288
UNIT_SQUARED = DENOMINATOR * DENOMINATOR
REMOVED = (310, 313, 316, 319, 322, 325)
HOST = tuple(vertex for vertex in range(509) if vertex not in REMOVED)
MOSER_PARENT = (0, 398, 408, 459, 397, 407, 470)
LOCAL_PAIRS = tuple(combinations(range(5), 2))
INPUT_HASHES = {
    "hadwiger_nelson_parts509_fold264_438_stop/points.tsv": "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    "hadwiger_nelson_parts509_swap_closure/completion_points.json": "b82909c48ce088deb89b555f4c8fa554bba44030570fdaaf0b9b607e9552a5a6",
    "hadwiger_nelson_parts509_degree4_list_kernel/certificate.json": "d0d88c667525589539926efbec124fc697059a6606cde110e7cd53c0b7dbb4e6",
    "hadwiger_nelson_parts509_pair_closure/ambient_w3_edges.json": "960d32618cf5afd013f29b3f6e2e85cb6a35e7d6b8884a6680a657f8e6c46f92",
}

OFF_DIAGONAL = []
for left in range(8):
    for right in range(left + 1, 8):
        repeated = left & right
        factor = 2
        for bit, prime in enumerate(PRIMES):
            if repeated & (1 << bit):
                factor *= prime
        OFF_DIAGONAL.append((left, right, left ^ right, factor))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_inputs(repo):
    raw = {}
    for relative, expected in INPUT_HASHES.items():
        data = (repo / relative).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, "input hash " + relative)
        raw[relative] = data

    parent = []
    for line in raw["hadwiger_nelson_parts509_fold264_438_stop/points.tsv"].decode().splitlines():
        if line and not line.startswith("#"):
            row = tuple(3 * int(value) for value in line.split())
            require(len(row) == 16, "parent coordinate width")
            parent.append(row)

    pool_json = json.loads(raw["hadwiger_nelson_parts509_swap_closure/completion_points.json"])
    pool = []
    for record in pool_json["points"]:
        scaled = tuple(DENOMINATOR * Fraction(value) for value in record["x"] + record["y"])
        require(len(scaled) == 16 and all(value.denominator == 1 for value in scaled), "pool coordinate scale")
        pool.append(tuple(int(value) for value in scaled))

    state_json = json.loads(raw["hadwiger_nelson_parts509_degree4_list_kernel/certificate.json"])
    host_words = [record["core_coloring"] for record in state_json["states"]]
    imported_edges = [tuple(edge) for edge in json.loads(raw["hadwiger_nelson_parts509_pair_closure/ambient_w3_edges.json"])["edges"]]
    require(len(parent) == 509 and len(pool) == 1158 and len(host_words) == 22, "input cardinalities")
    require(len(parent + pool) == len(set(parent + pool)) == 1667, "ambient point distinctness")
    return parent, pool, host_words, imported_edges


def norm_coefficients(left, right):
    dx = tuple(a - b for a, b in zip(left[:8], right[:8]))
    dy = tuple(a - b for a, b in zip(left[8:], right[8:]))
    output = [0] * 8
    output[0] = sum(
        radicand * (x * x + y * y)
        for radicand, x, y in zip(RADICANDS, dx, dy)
    )
    for i, j, target, factor in OFF_DIAGONAL:
        output[target] += factor * (dx[i] * dx[j] + dy[i] * dy[j])
    return tuple(output)


def exact_unit(left, right):
    norm = norm_coefficients(left, right)
    if norm[0] != UNIT_SQUARED:
        return False, False
    return norm[1:] == (0,) * 7, True


def scan_edges(points):
    edges = []
    rational_survivors = 0
    for i, j in combinations(range(len(points)), 2):
        unit, survived = exact_unit(points[i], points[j])
        rational_survivors += survived
        if unit:
            edges.append((i, j))
    return edges, rational_survivors


def proper_word(word, edges, vertices, colours=4):
    require(len(word) == vertices and set(word) <= set("0123"[:colours]), "word format")
    require(all(word[a] != word[b] for a, b in edges), "word edge")


def enumerate_cases(pool_adjacency):
    triangles = []
    for a in range(len(pool_adjacency)):
        for b in sorted(vertex for vertex in pool_adjacency[a] if vertex > a):
            for c in sorted(vertex for vertex in pool_adjacency[a] & pool_adjacency[b] if vertex > b):
                triangles.append((a, b, c))
    cases = set()
    for first, second in combinations(triangles, 2):
        if len(set(first) & set(second)) == 1:
            cases.add(tuple(sorted(set(first) | set(second))))
    return triangles, sorted(cases)


def edge_mask(ids, pool_adjacency):
    mask = 0
    local_edges = []
    for bit, (a, b) in enumerate(LOCAL_PAIRS):
        if ids[b] in pool_adjacency[ids[a]]:
            mask |= 1 << bit
            local_edges.append((a, b))
    return mask, local_edges


def all_proper_five_words(mask, cache):
    if mask not in cache:
        active = [pair for bit, pair in enumerate(LOCAL_PAIRS) if mask & (1 << bit)]
        cache[mask] = [
            word
            for word in product(range(4), repeat=5)
            if all(word[a] != word[b] for a, b in active)
        ]
    return cache[mask]


def compatible_words(words, domains):
    return [word for word in words if all(domains[index] & (1 << colour) for index, colour in enumerate(word))]


def audit(repo, target_certificate):
    parent, pool, host_words, imported_edges = load_inputs(repo)
    ambient = parent + pool
    ambient_edges, rational_survivors = scan_edges(ambient)
    require(ambient_edges == imported_edges, "complete ambient edge stream")
    require(len(ambient_edges) == 11074, "ambient edge count")

    parent_edges = [edge for edge in ambient_edges if edge[1] < 509]
    require(len(parent_edges) == 2442, "parent edge count")
    degrees = Counter(vertex for edge in parent_edges for vertex in edge)
    require(tuple(vertex for vertex in range(509) if degrees[vertex] == 4) == REMOVED, "degree-four deletion set")
    require(not any(a in REMOVED and b in REMOVED for a, b in parent_edges), "deleted vertices independent")

    host_index = {vertex: index for index, vertex in enumerate(HOST)}
    host_edges = [
        (host_index[a], host_index[b])
        for a, b in parent_edges
        if a not in REMOVED and b not in REMOVED
    ]
    require(len(host_edges) == 2418, "host edge count")
    for word in host_words:
        proper_word(word, host_edges, 503)
    moser_local = tuple(host_index[vertex] for vertex in MOSER_PARENT)
    moser_position = {vertex: index for index, vertex in enumerate(moser_local)}
    moser_edges = [
        (moser_position[a], moser_position[b])
        for a, b in host_edges
        if a in moser_position and b in moser_position
    ]
    require(len(moser_edges) == 11, "retained Moser edge count")
    require(
        not any(
            all(word[a] != word[b] for a, b in moser_edges)
            for word in product(range(3), repeat=7)
        ),
        "retained Moser three-colour exhaustion",
    )

    pool_adjacency = [set() for _ in pool]
    host_neighbours = [set() for _ in pool]
    for a, b in ambient_edges:
        if a >= 509:
            qa, qb = a - 509, b - 509
            pool_adjacency[qa].add(qb)
            pool_adjacency[qb].add(qa)
        elif b >= 509 and a in host_index:
            host_neighbours[b - 509].add(host_index[a])

    domains = []
    for word in host_words:
        word_domains = []
        for neighbourhood in host_neighbours:
            used = sum(1 << colour for colour in {int(word[v]) for v in neighbourhood})
            word_domains.append(15 & ~used)
        domains.append(word_domains)

    triangles, cases = enumerate_cases(pool_adjacency)
    require(len(cases) == 1401, "complete double-triangle family")
    proper_cache = {}
    histogram = Counter()
    survival_counts = {}
    survival_sets = {}
    witness_sets = {}
    edge_counts = []
    case_stream = hashlib.sha256()
    witness_stream = hashlib.sha256()

    for ids in cases:
        mask, local_edges = edge_mask(ids, pool_adjacency)
        proper_words = all_proper_five_words(mask, proper_cache)
        surviving = []
        witnesses = {}
        for fixture in range(22):
            local_domains = [domains[fixture][vertex] for vertex in ids]
            compatible = compatible_words(proper_words, local_domains)
            if compatible:
                surviving.append(fixture)
                witnesses[fixture] = compatible[0]
        require(surviving, "every support has a four-colour extension")
        survival_counts[ids] = len(surviving)
        survival_sets[ids] = surviving
        witness_sets[ids] = witnesses
        histogram[len(surviving)] += 1
        contacts = sum(len(host_neighbours[vertex]) for vertex in ids)
        edge_counts.append(2418 + contacts + len(local_edges))
        record = [list(ids), mask, contacts, surviving]
        case_stream.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
        witness_record = [list(ids), [[fixture, list(witnesses[fixture])] for fixture in surviving]]
        witness_stream.update((json.dumps(witness_record, separators=(",", ":")) + "\n").encode())

    chosen = min(cases, key=lambda ids: (survival_counts[ids], ids))
    require(list(chosen) == target_certificate["selected_q3_indices"], "selected support")
    require(target_certificate["removed_original"] == list(REMOVED), "target deletion set")
    selected_mask, selected_local_edges = edge_mask(chosen, pool_adjacency)
    selected_survivors = survival_sets[chosen]
    require(selected_survivors == target_certificate["surviving_fixture_indices"], "selected survival set")

    stored_extensions = dict((fixture, tuple(word)) for fixture, word in target_certificate["surviving_fixture_extensions"])
    require(sorted(stored_extensions) == selected_survivors, "stored extension index set")
    selected_proper_words = all_proper_five_words(selected_mask, proper_cache)
    for fixture, word in stored_extensions.items():
        require(word in selected_proper_words, "stored internal word")
        require(all(domains[fixture][vertex] & (1 << word[index]) for index, vertex in enumerate(chosen)), "stored contact word")

    selected_points = [parent[vertex] for vertex in HOST] + [pool[vertex] for vertex in chosen]
    selected_edges, selected_rational_survivors = scan_edges(selected_points)
    expected_selected_edges = set(host_edges)
    expected_selected_edges.update(
        (host_vertex, 503 + index)
        for index, pool_vertex in enumerate(chosen)
        for host_vertex in host_neighbours[pool_vertex]
    )
    expected_selected_edges.update((503 + a, 503 + b) for a, b in selected_local_edges)
    require(set(selected_edges) == expected_selected_edges, "complete selected edge decomposition")
    require(len(selected_edges) == 2450, "selected edge count")

    target_word = target_certificate["four_word"]
    proper_word(target_word, selected_edges, 508)
    require(target_word[:503] == host_words[target_certificate["fixture_index"]], "target word fixture")

    candidates = []
    for fixture in selected_survivors:
        local_domains = [domains[fixture][vertex] for vertex in chosen]
        for tail in compatible_words(selected_proper_words, local_domains):
            full_word = host_words[fixture] + "".join(map(str, tail))
            difference = sum(a != b for a, b in zip(full_word, target_word))
            candidates.append((difference, full_word, fixture, tail))
    difference, fresh_word, fresh_fixture, fresh_tail = max(candidates)
    proper_word(fresh_word, selected_edges, 508)
    require(target_certificate["fresh_fixture"] == fresh_fixture, "fresh fixture regeneration")
    require(target_certificate["fresh_tail"] == list(fresh_tail), "fresh tail regeneration")
    require(target_certificate["fresh_word"] == fresh_word, "fresh full-word regeneration")

    rejected = [fixture for fixture in range(22) if fixture not in selected_survivors]
    joint_only = [
        fixture
        for fixture in rejected
        if all(domains[fixture][vertex] for vertex in chosen)
    ]
    require(joint_only == [6, 10, 11], "private-contact-only failures")
    fixture_six_lists = [
        [colour for colour in range(4) if domains[6][vertex] & (1 << colour)]
        for vertex in chosen
    ]
    require(fixture_six_lists == [[0], [1], [1], [1], [0, 3]], "fixture six domain witness")

    output = {
        "verdict": "ACCEPT_AND_STRENGTHEN_WITH_STRICT_FINITE_POOL_AND_FIXTURE_LIMITATION",
        "parent_points": 509,
        "parent_edges": 2442,
        "host_points": 503,
        "host_edges": 2418,
        "removed_original": list(REMOVED),
        "ambient_points": len(ambient),
        "ambient_pairs": len(ambient) * (len(ambient) - 1) // 2,
        "ambient_edges": len(ambient_edges),
        "rational_coefficient_survivors": rational_survivors,
        "ambient_edge_stream_entrywise_match": True,
        "pool_unit_triangles": len(triangles),
        "double_triangle_supports": len(cases),
        "all_supports_points": 508,
        "complete_edge_count_range": [min(edge_counts), max(edge_counts)],
        "fixture_survival_histogram": {str(key): value for key, value in sorted(histogram.items())},
        "minimum_surviving_fixtures": min(survival_counts.values()),
        "all_supports_four_colourable": True,
        "all_supports_chromatic_number": 4,
        "moser_parent_vertices": list(MOSER_PARENT),
        "moser_edges": len(moser_edges),
        "moser_three_colour_assignments_exhausted": 3**7,
        "case_relation_sha256": case_stream.hexdigest(),
        "positive_witness_sha256": witness_stream.hexdigest(),
        "selected_q3_indices": list(chosen),
        "selected_points": len(selected_points),
        "selected_pairs": len(selected_points) * (len(selected_points) - 1) // 2,
        "selected_edges": len(selected_edges),
        "selected_rational_coefficient_survivors": selected_rational_survivors,
        "selected_new_old_contacts": sum(len(host_neighbours[vertex]) for vertex in chosen),
        "selected_new_new_edges": len(selected_local_edges),
        "selected_surviving_fixtures": selected_survivors,
        "selected_rejected_fixtures": len(rejected),
        "selected_joint_only_fixture_rejections": joint_only,
        "selected_single_star_fixture_rejections": len(rejected) - len(joint_only),
        "fixture_six_available_lists": fixture_six_lists,
        "fresh_fixture": fresh_fixture,
        "fresh_tail": list(fresh_tail),
        "fresh_word": fresh_word,
        "fresh_word_difference_from_target": difference,
        "target_word_checked": True,
        "selected_rejects_supplied_complete_host_words": True,
        "full_unrestricted_host_relation_enumerated": False,
        "record_candidate": False,
    }
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=BASE.parent)
    parser.add_argument("--certificate", type=Path, default=BASE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=BASE / "EXPECTED.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    output = audit(args.repo.resolve(), certificate)
    if args.check_expected:
        require(output == json.loads(args.expected.read_text()), "expected theorem output")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
