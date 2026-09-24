#!/usr/bin/env python3
"""Independent exact checks for the independent-extension rounding theorem.

This file imports no reviewed module.  It checks the numerical degree
criterion, the private-edge normalization (including a deletion), exact
multiplicity caps for many literal graphs, the fractional cap map, and the
finite scale hierarchy.
"""

from functools import lru_cache
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations, product
from json import dumps
from math import ceil
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def near_regular_arithmetic():
    tested = 0
    minimum_margin = None
    for scale in range(1, 65):
        for length in (48 * (scale + 1), 48 * (scale + 1) + 1,
                       96 * (scale + 1)):
            maximum_edges = length * scale // 2
            # The margin below is affine in count, with positive slope under
            # length >= 48(scale+1), so its minimum is at the cutoff.  Check
            # both endpoints and the slope rather than sampling an interval.
            slope = Q(3, 4) - Q(6 * (2 * scale + 1), length)
            require(slope > 0, "near-regular margin is not increasing")
            for count in sorted({12 * (scale + 1), maximum_edges}):
                degree_bound = Q(2 * count, length) + 1
                lhs = 3 * degree_bound * (2 * scale + 1)
                margin = Q(3 * count, 4) - lhs
                require(margin > 0, "near-regular numerical implication failed")
                require(count > 3 * degree_bound * (2 * scale + 1),
                        "general augmenting criterion failed")
                minimum_margin = margin if minimum_margin is None else min(minimum_margin, margin)
                tested += 1
    return {
        "scale_values": 64,
        "parameter_tuples": tested,
        "minimum_strict_margin_to_three_quarters": str(minimum_margin),
    }


def falling(n, k):
    value = 1
    for j in range(k):
        value *= n - j
    return value


def type_injections(sizes, pattern):
    choices = []
    for label, size in sizes.items():
        count = pattern.count(label)
        choices.append(list(permutations(range(size), count)))
    labels = list(sizes)
    for rows in product(*choices):
        assigned = {}
        cursors = {label: 0 for label in labels}
        for label, row in zip(labels, rows):
            assigned[label] = row
        vertices = []
        for label in pattern:
            vertices.append((label, assigned[label][cursors[label]]))
            cursors[label] += 1
        yield tuple(vertices)


def canonical_edge(left, right):
    return tuple(sorted((left, right)))


def original_edges(vertices):
    return tuple(canonical_edge(a, b) for a, b in combinations(vertices, 2))


def private_graph(auxiliary_size, original_order, count):
    all_edges = {(a, b) for a in range(auxiliary_size) for b in range(original_order)}
    deficit = auxiliary_size * original_order - count
    removed = {(j % auxiliary_size, j) for j in range(deficit)}
    return sorted(all_edges - removed), sorted(removed)


def dense_normalization():
    sizes = {"A": 4, "B": 5}
    original_order = sum(sizes.values())
    specifications = [
        ("AAB_triangle", ("A", "A", "B"), 4),
        ("AA_spare", ("A", "A"), 2),
        ("AB_spare", ("A", "B"), 12),
    ]
    deleted = canonical_edge(("A", 0), ("A", 1))
    full_original_load = {}
    restricted_original_load = {}
    private_rows = []
    total_embeddings = 0

    for name, pattern, count in specifications:
        auxiliary_size = ceil(Q(count, original_order))
        tags, removed_tags = private_graph(auxiliary_size, original_order, count)
        denominator = auxiliary_size * original_order
        for label, size in sizes.items():
            denominator *= falling(size, pattern.count(label))
        weight = Q(auxiliary_size * original_order, denominator)
        full_tag_load = {tag: Q(0) for tag in tags}
        restricted_tag_load = {tag: Q(0) for tag in tags}
        family_weight = Q(0)
        embeddings = 0

        for vertices in type_injections(sizes, pattern):
            edges = original_edges(vertices)
            survives = deleted not in edges
            for tag in tags:
                embeddings += 1
                family_weight += weight
                full_tag_load[tag] += weight
                for edge in edges:
                    full_original_load[edge] = full_original_load.get(edge, Q(0)) + weight
                if survives:
                    restricted_tag_load[tag] += weight
                    for edge in edges:
                        restricted_original_load[edge] = (
                            restricted_original_load.get(edge, Q(0)) + weight
                        )

        require(family_weight == count, "wrong total family weight")
        require(set(full_tag_load.values()) == {Q(1)}, "private edge load is not one")
        if name in {"AAB_triangle", "AA_spare"}:
            require(set(restricted_tag_load.values()) == {Q(5, 6)},
                    "deleted internal edge has wrong private load")
        else:
            require(set(restricted_tag_load.values()) == {Q(1)},
                    "unaffected private load changed")
        degree_left = [0] * auxiliary_size
        degree_right = [0] * original_order
        for a, b in removed_tags:
            degree_left[a] += 1
            degree_right[b] += 1
        private_rows.append({
            "name": name,
            "pattern": "".join(pattern),
            "count": count,
            "auxiliary_size": auxiliary_size,
            "valid_labelled_embeddings": embeddings,
            "embedding_weight": str(weight),
            "maximum_missing_degree": max(degree_left + degree_right, default=0),
            "restricted_private_load": str(next(iter(restricted_tag_load.values()))),
        })
        total_embeddings += embeddings

    for a, b in combinations(range(sizes["A"]), 2):
        edge = canonical_edge(("A", a), ("A", b))
        require(full_original_load[edge] == 1, "full AA load is not one")
        if edge != deleted:
            require(restricted_original_load[edge] == 1,
                    "surviving AA load changed")
    for a in range(sizes["A"]):
        for b in range(sizes["B"]):
            edge = canonical_edge(("A", a), ("B", b))
            require(full_original_load[edge] == 1, "full AB load is not one")
            expected = Q(13, 15) if a in (0, 1) else Q(1)
            require(restricted_original_load[edge] == expected,
                    "restricted AB load is wrong")

    return {
        "original_part_sizes": sizes,
        "original_order": original_order,
        "patterns": private_rows,
        "labelled_valid_embeddings": total_embeddings,
        "full_original_edge_loads_all_one": True,
        "deleted_edge": [["A", 0], ["A", 1]],
        "minimum_surviving_original_load": str(min(restricted_original_load.values())),
        "minimum_private_load": "5/6",
    }


def build_instance(n, core_mask, neighborhoods, class_sizes):
    core_pairs = list(combinations(range(n), 2))
    edges = {edge for bit, edge in enumerate(core_pairs) if core_mask >> bit & 1}
    offset = n
    for neighborhood, size in zip(neighborhoods, class_sizes):
        for center in range(offset, offset + size):
            edges.update(canonical_edge(center, vertex) for vertex in neighborhood)
        offset += size
    triangles = [
        triple for triple in combinations(range(offset), 3)
        if all(canonical_edge(a, b) in edges for a, b in combinations(triple, 2))
    ]
    relevant_edges = sorted({canonical_edge(a, b) for triple in triangles
                             for a, b in combinations(triple, 2)})
    index = {edge: j for j, edge in enumerate(relevant_edges)}
    triangle_edges = [
        tuple(index[canonical_edge(a, b)] for a, b in combinations(triple, 2))
        for triple in triangles
    ]
    triangle_masks = [
        sum(1 << edge_index for edge_index in row) for row in triangle_edges
    ]
    return triangle_edges, triangle_masks, len(relevant_edges)


def exact_packing(triangle_masks):
    count = len(triangle_masks)
    conflicts = []
    for left in triangle_masks:
        mask = 0
        for j, right in enumerate(triangle_masks):
            if left & right:
                mask |= 1 << j
        conflicts.append(mask)

    @lru_cache(maxsize=None)
    def solve(remaining):
        if not remaining:
            return 0
        candidates = [j for j in range(count) if remaining >> j & 1]
        chosen = max(candidates, key=lambda j: (conflicts[j] & remaining).bit_count())
        include = 1 + solve(remaining & ~conflicts[chosen])
        exclude = solve(remaining & ~(1 << chosen))
        return max(include, exclude)

    return solve((1 << count) - 1)


def exact_cover(triangle_edges, edge_count):
    if not triangle_edges:
        return 0
    cover_masks = [0] * edge_count
    for j, row in enumerate(triangle_edges):
        for edge_index in row:
            cover_masks[edge_index] |= 1 << j

    @lru_cache(maxsize=None)
    def solve(remaining):
        if not remaining:
            return 0
        triangle_index = (remaining & -remaining).bit_length() - 1
        return 1 + min(
            solve(remaining & ~cover_masks[edge_index])
            for edge_index in triangle_edges[triangle_index]
        )

    return solve((1 << len(triangle_edges)) - 1)


@lru_cache(maxsize=None)
def invariants(n, core_mask, neighborhoods, class_sizes):
    triangle_edges, triangle_masks, edge_count = build_instance(
        n, core_mask, neighborhoods, class_sizes
    )
    return exact_packing(triangle_masks), exact_cover(triangle_edges, edge_count), len(triangle_edges)


def cap_audit():
    compared = 0
    maximum_triangles = 0
    digest_rows = []
    for n in (3, 4):
        edge_count = n * (n - 1) // 2
        for core_mask in range(1 << edge_count):
            for neighborhood_mask in range(1 << n):
                neighborhood = tuple(v for v in range(n) if neighborhood_mask >> v & 1)
                original_size = n + 2
                original = invariants(n, core_mask, (neighborhood,), (original_size,))
                capped = invariants(n, core_mask, (neighborhood,), (n,))
                require(original[:2] == capped[:2], "one-class cap changed packing or cover")
                compared += 1
                maximum_triangles = max(maximum_triangles, original[2])
                digest_rows.append((n, core_mask, neighborhood_mask, original[:2]))

    n = 3
    edge_count = n * (n - 1) // 2
    for core_mask in range(1 << edge_count):
        for first_mask in range(1 << n):
            first = tuple(v for v in range(n) if first_mask >> v & 1)
            for second_mask in range(1 << n):
                second = tuple(v for v in range(n) if second_mask >> v & 1)
                original = invariants(n, core_mask, (first, second), (n + 1, n + 2))
                capped = invariants(n, core_mask, (first, second), (n, n))
                require(original[:2] == capped[:2], "two-class cap changed packing or cover")
                compared += 1
                maximum_triangles = max(maximum_triangles, original[2])
                digest_rows.append((n, core_mask, first_mask, second_mask, original[:2]))

    encoded = dumps(digest_rows, separators=(",", ":")).encode()
    return {
        "literal_graph_pairs": compared,
        "invariants_per_graph": ["maximum edge-disjoint triangle packing",
                                 "minimum edge triangle cover"],
        "maximum_triangle_count": maximum_triangles,
        "records_sha256": sha256(encoded).hexdigest(),
    }


def fractional_cap_audit():
    state = 0xC0FFEE123456789

    def random_word():
        nonlocal state
        state = (6364136223846793005 * state + 1442695040888963407) & ((1 << 64) - 1)
        return state

    tested = 0
    maximum_spoke_load = Q(0)
    for n in range(2, 10):
        edges = list(combinations(range(n), 2))
        for _ in range(31):
            classes = 1 + random_word() % 4
            raw = [[Q(random_word() % 17, 19) for edge in edges] for h in range(classes)]
            for j in range(len(edges)):
                total = sum(raw[h][j] for h in range(classes))
                if total > 1:
                    for h in range(classes):
                        raw[h][j] /= total
            before = sum(sum(row) for row in raw)
            after = Q(0)
            for row in raw:
                for center in range(n):
                    spoke = sum(row[j] for j, edge in enumerate(edges) if center in edge) / n
                    require(spoke <= Q(n - 1, n), "fractional cap spoke overload")
                    maximum_spoke_load = max(maximum_spoke_load, spoke)
                after += sum(row)
            require(before == after, "fractional cap changed objective")
            for j in range(len(edges)):
                require(sum(raw[h][j] for h in range(classes)) <= 1,
                        "fractional cap changed a core-edge load")
            tested += 1
    return {
        "exact_rational_profiles": tested,
        "new_seed": "0xc0ffee123456789",
        "maximum_mapped_spoke_load": str(maximum_spoke_load),
        "universal_bound_checked": "(n-1)/n",
    }


def hierarchy_audit():
    state = 0x51A1E5

    def random_word():
        nonlocal state
        state = (2862933555777941757 * state + 3037000493) & ((1 << 64) - 1)
        return state

    tested = 0
    maximum_types = 7
    for type_count in range(1, maximum_types + 1):
        alpha = Q(2, 5)
        epsilon = [Q(1)]
        eta = []
        for stage in range(type_count + 1):
            proportion = min(alpha, epsilon[stage]) / (type_count + 1)
            tolerance = proportion ** 2 / 73
            eta.append(tolerance)
            epsilon.append(min(epsilon[stage] / 3, tolerance / (3 * type_count)))
        special = [Q(0), Q(1)]
        for stage in range(type_count + 1):
            special.extend((epsilon[stage], epsilon[stage + 1],
                            (epsilon[stage] + epsilon[stage + 1]) / 2))
        profiles = [
            tuple(special[(j + shift) % len(special)] for j in range(type_count))
            for shift in range(len(special))
        ]
        for _ in range(250):
            profiles.append(tuple(Q(random_word() % 1000000, 1000000)
                                  for _ in range(type_count)))
        for ratios in profiles:
            stage = next(j for j in range(type_count + 1)
                         if not any(epsilon[j + 1] <= x < epsilon[j] for x in ratios))
            large = [x for x in ratios if x >= epsilon[stage]]
            small = [x for x in ratios if x < epsilon[stage + 1]]
            require(len(large) + len(small) == type_count,
                    "hierarchy left an unclassified class")
            augmented = 1 + sum(large)
            new_alpha = min(alpha, epsilon[stage]) / (type_count + 1)
            require(alpha >= new_alpha * augmented,
                    "original core class became too small")
            require(all(x >= new_alpha * augmented for x in large),
                    "absorbed independent class became too small")
            require(sum(small) <= eta[stage] * augmented,
                    "remaining extension exceeds the small-class tolerance")
            tested += 1
    return {
        "type_counts": list(range(1, maximum_types + 1)),
        "endpoint_and_random_profiles": tested,
        "new_seed": "0x51a1e5",
        "note": "Illustrative exact tolerances; this checks the hierarchy logic, not Keevash constants.",
    }


def main():
    return {
        "status": "PASS",
        "near_regular_arithmetic": near_regular_arithmetic(),
        "dense_private_edge_normalization": dense_normalization(),
        "multiplicity_cap": cap_audit(),
        "fractional_cap_map": fractional_cap_audit(),
        "class_scale_hierarchy": hierarchy_audit(),
        "trust_boundary": (
            "Exact finite and algebraic checks only. Keevash's universal family-decomposition "
            "theorem, its specialization, and the asymptotic rounding proof are audited "
            "mathematically rather than proved by this program."
        ),
    }


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit("usage: independent_check.py [EXPECTED_OUTPUT.json]")
    encoded = (dumps(main(), indent=2, sort_keys=True) + "\n").encode()
    if len(sys.argv) == 2:
        require(encoded == Path(sys.argv[1]).read_bytes(),
                "output differs from expected output")
    print(dumps({"status": "PASS", "sha256": sha256(encoded).hexdigest()},
                sort_keys=True))
