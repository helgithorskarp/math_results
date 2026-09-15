#!/usr/bin/env python3
"""Clean-room audit of the exact-507 H510 obstruction.

This checker imports no submitted Python module.  It reconstructs the strict
H510 graph from the pinned multiquadratic coordinates, rechecks the twenty
rank bases at a different prime, and independently enumerates every relevant
collision partition.  Its dense-quadruple enumeration uses a triangle/C4
decomposition rather than the submitted edge/triple bitset search.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
N = 510
FULL = (1 << 20) - 1
RANK_PRIME = 1_000_000_009
RADICAL_PRIMES = (3, 5, 11)
KERNEL_COORDINATE_COLUMNS = (0, 2, 5, 7, 9, 11, 12, 14)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_pinned():
    pins = json.loads((HERE / "inputs.json").read_text())
    loaded = {}
    for relative, digest in pins.items():
        path = (HERE / relative).resolve()
        raw = path.read_bytes()
        require(sha256(raw).hexdigest() == digest, "input hash: " + relative)
        loaded[relative] = json.loads(raw) if path.suffix == ".json" else raw
    return loaded


def radical_product_factor(a, b):
    shared = a & b
    factor = 1
    for bit, prime in enumerate(RADICAL_PRIMES):
        if shared & (1 << bit):
            factor *= prime
    return a ^ b, factor


def squared_distance(p, q):
    """Square a multiquadratic vector in the bit-mask radical basis."""
    result = [Fraction(0) for _ in range(8)]
    for axis in range(2):
        difference = [p[axis][i] - q[axis][i] for i in range(8)]
        support = [(i, value) for i, value in enumerate(difference) if value]
        for i, a in support:
            for j, b in support:
                radical, factor = radical_product_factor(i, j)
                result[radical] += factor * a * b
    return tuple(result)


def canonical_point(raw):
    require(len(raw) == 2 and all(len(axis) == 8 for axis in raw), "coordinate shape")
    return tuple(tuple(Fraction(value) for value in axis) for axis in raw)


def load_graph(loaded):
    aligned_key = "../hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json"
    union_key = "../hadwiger_nelson_parts509_heule_union_minimum/union_510.json"
    aligned = loaded[aligned_key]
    union = loaded[union_key]
    require(aligned.get("vtx") == "510.vtx", "H510 source name")
    points = [canonical_point(point) for point in aligned["aligned_H"]]
    require(len(points) == len(set(points)) == N, "H510 point census")
    kernel_rows = []
    for point in points:
        flattened = point[0] + point[1]
        require(all(flattened[index] == 0 for index in range(16) if index not in KERNEL_COORDINATE_COLUMNS),
                "coordinate kernel support")
        kernel_rows.append(tuple(flattened[index] for index in KERNEL_COORDINATE_COLUMNS))

    strict_edges = []
    for u in range(N):
        for v in range(u + 1, N):
            if squared_distance(points[u], points[v]) == (Fraction(1),) + (Fraction(0),) * 7:
                strict_edges.append((u, v))
    require(len(strict_edges) == 2504, "strict H510 unit-pair census")

    union_points = [canonical_point(point) for point in union["points"]]
    lookup = {point: i for i, point in enumerate(union_points)}
    require(len(lookup) == len(union_points) == 553, "union point census")
    h_to_union = [lookup[point] for point in points]
    require(len(set(h_to_union)) == N, "H510 alignment injectivity")
    back = {vertex: label for label, vertex in enumerate(h_to_union)}
    inherited = sorted(
        (min(back[u], back[v]), max(back[u], back[v]))
        for u, v in union["edges"]
        if u in back and v in back
    )
    require(inherited == strict_edges, "strict graph/source-union alignment")

    adjacency = [set() for _ in range(N)]
    adjacency_bits = [0] * N
    for u, v in strict_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        adjacency_bits[u] |= 1 << v
        adjacency_bits[v] |= 1 << u
    return strict_edges, adjacency, adjacency_bits, kernel_rows


def graph_rhombi(adjacency):
    rhombi = []
    opposite_row = {}
    for a, b in combinations(range(N), 2):
        common = sorted(adjacency[a] & adjacency[b])
        require(len(common) <= 2, "source contains K2,3")
        if len(common) == 2 and (a, b) < tuple(common):
            row = len(rhombi)
            c, d = common
            rhombi.append((a, b, c, d))
            opposite_row[(a, b)] = row
            opposite_row[(c, d)] = row
    require(len(rhombi) == 3953 and len(opposite_row) == 7906, "rhombus census")
    return rhombi, opposite_row


def modular_rank(row_ids, rhombi, prime):
    """Sparse forward-pivot elimination, unlike the parent's reverse pivots."""
    basis = {}
    for row_id in row_ids:
        a, b, c, d = rhombi[row_id]
        row = {a: 1, b: 1, c: prime - 1, d: prime - 1}
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = pow(row[pivot], -1, prime)
                basis[pivot] = {j: value * inverse % prime for j, value in row.items()}
                break
            factor = row[pivot]
            for j, value in basis[pivot].items():
                new = (row.get(j, 0) - factor * value) % prime
                if new:
                    row[j] = new
                else:
                    row.pop(j, None)
    return len(basis)


def fraction_mod(value, prime):
    return value.numerator * pow(value.denominator, -1, prime) % prime


def dense_modular_rank(rows, prime):
    basis = {}
    for raw in rows:
        row = [fraction_mod(value, prime) for value in raw]
        for pivot in sorted(basis):
            factor = row[pivot]
            if factor:
                row = [(a - factor * b) % prime for a, b in zip(row, basis[pivot])]
        pivots = [index for index, value in enumerate(row) if value]
        if pivots:
            pivot = min(pivots)
            inverse = pow(row[pivot], -1, prime)
            basis[pivot] = [value * inverse % prime for value in row]
    return len(basis)


def check_prime(p):
    require(p >= 2, "rank prime")
    for divisor in range(2, isqrt(p) + 1):
        require(p % divisor != 0, "rank modulus is composite")


def basis_masks(certificate, rhombi, kernel_rows):
    check_prime(RANK_PRIME)
    for a, b, c, d in rhombi:
        require(
            all(kernel_rows[a][column] + kernel_rows[b][column]
                == kernel_rows[c][column] + kernel_rows[d][column]
                for column in range(8)),
            "exact rhombus kernel",
        )
    augmented = [(Fraction(1), *row) for row in kernel_rows]
    require(dense_modular_rank(augmented, RANK_PRIME) == 9, "kernel-column independence")
    bases = certificate["bases"]
    require(len(bases) == 20, "basis count")
    base_sets = []
    for basis in bases:
        require(len(basis) == len(set(basis)) == 501, "basis cardinality")
        require(all(type(row) is int and 0 <= row < len(rhombi) for row in basis), "basis row")
        require(modular_rank(basis, rhombi, RANK_PRIME) == 501, "basis rank")
        base_sets.append(set(basis))
    masks = [
        sum(1 << index for index, basis in enumerate(base_sets) if row in basis)
        for row in range(len(rhombi))
    ]
    require(all(mask != FULL for mask in masks), "one-row full cover")
    return masks


def row_covers(masks):
    containing = [[] for _ in range(20)]
    for row, mask in enumerate(masks):
        for bit in range(20):
            if mask & (1 << bit):
                containing[bit].append(row)

    cache = {}

    def eligible(missing):
        if missing not in cache:
            if missing == 0:
                answer = tuple(range(len(masks)))
            else:
                bits = [bit for bit in range(20) if missing & (1 << bit)]
                seed = min(bits, key=lambda bit: len(containing[bit]))
                answer = tuple(row for row in containing[seed] if masks[row] & missing == missing)
            cache[missing] = answer
        return cache[missing]

    two = []
    triples = []
    for first in range(len(masks)):
        for second in range(first + 1, len(masks)):
            union = masks[first] | masks[second]
            if union == FULL:
                two.append((first, second))
            missing = FULL ^ union
            for third in eligible(missing):
                if third > second:
                    triples.append((first, second, third))
    require(len(two) == 2, "two-row cover census")
    require(len(triples) == 8486, "three-row cover census")
    return two, triples, eligible


def group_partition(pairs):
    parent = list(range(N))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in pairs:
        a, b = find(u), find(v)
        if a != b:
            parent[b] = a
    groups = {}
    for vertex in range(N):
        groups.setdefault(find(vertex), []).append(vertex)
    return tuple(sorted(tuple(group) for group in groups.values() if len(group) > 1))


def collision_loss(groups):
    return sum(len(group) - 1 for group in groups)


def canonical_groups(groups):
    answer = tuple(sorted(tuple(sorted(group)) for group in groups if len(group) > 1))
    require(collision_loss(answer) == 3, "collision deficit")
    flat = [vertex for group in answer for vertex in group]
    require(len(flat) == len(set(flat)), "overlapping fibres")
    return answer


def invalid_mask(groups, opposite_row, masks):
    answer = 0
    for group in groups:
        for pair in combinations(group, 2):
            row = opposite_row.get(tuple(sorted(pair)))
            if row is not None:
                answer |= masks[row]
    return answer


def quotient_graph(edges, groups):
    owner = list(range(N))
    for group in groups:
        representative = min(group)
        for vertex in group:
            owner[vertex] = representative
    labels = sorted(set(owner))
    index = {label: i for i, label in enumerate(labels)}
    source_groups = [[] for _ in labels]
    for vertex, label in enumerate(owner):
        source_groups[index[label]].append(vertex)
    adjacency = [0] * len(labels)
    for u, v in edges:
        a, b = index[owner[u]], index[owner[v]]
        if a == b:
            return None, source_groups, (u, v), []
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    merged = [index[min(group)] for group in groups]
    return adjacency, source_groups, None, sorted(set(merged))


def first_new_k23(adjacency, merged):
    """Lexicographically first K2,3 involving a merged class.

    The source has no K2,3.  Thus a new witness has a merged class as a centre
    or a leaf.  Bitsets make both possibilities an independently implemented
    complete search.
    """
    centre_pairs = set()
    size = len(adjacency)
    for merged_vertex in merged:
        for other in range(size):
            if other != merged_vertex:
                centre_pairs.add(tuple(sorted((merged_vertex, other))))
        neighbours = [v for v in range(size) if adjacency[merged_vertex] & (1 << v)]
        centre_pairs.update(combinations(neighbours, 2))
    for a, b in sorted(centre_pairs):
        common_bits = adjacency[a] & adjacency[b]
        if common_bits.bit_count() >= 3:
            common = []
            while common_bits and len(common) < 3:
                low = common_bits & -common_bits
                common.append(low.bit_length() - 1)
                common_bits ^= low
            return (a, b, *common)
    return None


def assess(edges, groups):
    adjacency, source_groups, collapsed, merged = quotient_graph(edges, groups)
    if collapsed is not None:
        return "edge", collapsed
    witness = first_new_k23(adjacency, merged)
    if witness is None:
        return "open", None
    return "k23", tuple(tuple(source_groups[v]) for v in witness)


def repair_source_pairs(edges, groups):
    adjacency, source_groups, collapsed, merged = quotient_graph(edges, groups)
    require(collapsed is None, "repair base edge collapse")
    witness = first_new_k23(adjacency, merged)
    require(witness is not None, "rank-covering base without K2,3")
    a, b, x, y, z = witness
    critical = ((a, b), (x, y), (x, z), (y, z))
    pairs = set()
    for first, second in critical:
        for u in source_groups[first]:
            for v in source_groups[second]:
                pairs.add(tuple(sorted((u, v))))
    return sorted(pairs), witness


def independent(groups, adjacency):
    return all(v not in adjacency[u] for group in groups for u, v in combinations(group, 2))


def three_pair_family(edges, adjacency, rhombi, masks, two_covers, three_covers):
    candidates = set()
    for rows in three_covers:
        sides = [(rhombi[row][:2], rhombi[row][2:]) for row in rows]
        for choice in range(8):
            pairs = tuple(sides[i][(choice >> i) & 1] for i in range(3))
            if len({vertex for pair in pairs for vertex in pair}) == 6:
                candidates.add(canonical_groups(pairs))

    for first, second in two_covers:
        for doubled, single in ((first, second), (second, first)):
            for pair in (rhombi[single][:2], rhombi[single][2:]):
                pairs = (rhombi[doubled][:2], rhombi[doubled][2:], pair)
                if len({vertex for item in pairs for vertex in item}) == 6:
                    candidates.add(canonical_groups(pairs))

    persistent_last_pairs = 0
    repair_last_pairs = 0
    for first, second in two_covers:
        sides = ((rhombi[first][:2], rhombi[first][2:]), (rhombi[second][:2], rhombi[second][2:]))
        for choice in range(4):
            base = group_partition((sides[0][choice & 1], sides[1][(choice >> 1) & 1]))
            if collision_loss(base) != 2 or sorted(map(len, base)) != [2, 2]:
                continue
            require(independent(base, adjacency), "exceptional base edge")
            repairs, witness = repair_source_pairs(edges, base)
            repair_set = set(repairs)
            used = {vertex for group in base for vertex in group}
            for u in range(N):
                if u in used:
                    continue
                for v in range(u + 1, N):
                    if v in used or v in adjacency[u]:
                        continue
                    if (u, v) in repair_set:
                        repair_last_pairs += 1
                        candidates.add(canonical_groups((*base, (u, v))))
                    else:
                        # The displayed five quotient classes stay distinct;
                        # hence this same witness survives the last merger.
                        persistent_last_pairs += 1
    return sorted(candidates), persistent_last_pairs, repair_last_pairs


def opposition_triples(adjacency, opposite_row):
    opposite_pairs = sorted(opposite_row)
    for pair in opposite_pairs:
        u, v = pair
        for w in range(N):
            if w == u or w == v or w in adjacency[u] or w in adjacency[v]:
                continue
            triple = tuple(sorted((u, v, w)))
            internal = [edge for edge in combinations(triple, 2) if edge in opposite_row]
            # An opposition pair need not be a source nonedge.  Canonicalize
            # only among pairs from which this triple is actually generated:
            # the third vertex must be nonadjacent to both endpoints.  Using
            # the first internal pair unconditionally would lose the 36
            # immediate edge-collapse candidates seen in the source census.
            generating = []
            for candidate in internal:
                third = next(vertex for vertex in triple if vertex not in candidate)
                if third not in adjacency[candidate[0]] and third not in adjacency[candidate[1]]:
                    generating.append(candidate)
            if pair == min(generating):
                yield triple


def triple_pair_family(edges, adjacency, rhombi, opposite_row, masks, eligible):
    candidates = set()
    full_triples = []
    triple_count = 0
    for triple in opposition_triples(adjacency, opposite_row):
        triple_count += 1
        mask = 0
        for pair in combinations(triple, 2):
            row = opposite_row.get(pair)
            if row is not None:
                mask |= masks[row]
        if mask == FULL:
            full_triples.append(triple)
            continue
        missing = FULL ^ mask
        for row in eligible(missing):
            for pair in (rhombi[row][:2], rhombi[row][2:]):
                if not set(triple).intersection(pair):
                    candidates.add(canonical_groups((triple, pair)))

    require(len(full_triples) == 4, "full-defect triple census")
    persistent_last_pairs = 0
    repair_last_pairs = 0
    for triple in full_triples:
        repairs, witness = repair_source_pairs(edges, (triple,))
        repair_set = set(repairs)
        used = set(triple)
        for u in range(N):
            if u in used:
                continue
            for v in range(u + 1, N):
                if v in used or v in adjacency[u]:
                    continue
                if (u, v) in repair_set:
                    repair_last_pairs += 1
                    candidates.add(canonical_groups((triple, (u, v))))
                else:
                    persistent_last_pairs += 1
    return sorted(candidates), sorted(full_triples), triple_count, persistent_last_pairs, repair_last_pairs


def opposition_triangles(opposition_bits):
    triangles = []
    for a in range(N):
        later_b = opposition_bits[a] & ~((1 << (a + 1)) - 1)
        while later_b:
            low = later_b & -later_b
            b = low.bit_length() - 1
            later_b ^= low
            common = opposition_bits[a] & opposition_bits[b] & ~((1 << (b + 1)) - 1)
            while common:
                low_c = common & -common
                c = low_c.bit_length() - 1
                common ^= low_c
                triangles.append((a, b, c))
    return triangles


def dense_quadruples(adjacency_bits, opposite_row, masks):
    """Enumerate independent four-sets with >=4 opposition edges.

    Such an induced four-vertex opposition graph either has a triangle, or is
    triangle-free and therefore (by Mantel at n=4) exactly K2,2.  We assign a
    set in the first class to its lexicographically first triangle and a C4 to
    its lexicographically first opposite nonedge pair, avoiding a giant set of
    1.9 million tuples.
    """
    opposition_bits = [0] * N
    for u, v in opposite_row:
        opposition_bits[u] |= 1 << v
        opposition_bits[v] |= 1 << u
    triangles = opposition_triangles(opposition_bits)
    require(len(triangles) == 31582, "opposition triangle census")

    count = 0
    retained = set()
    all_mask = (1 << N) - 1

    for triangle in triangles:
        a, b, c = triangle
        possible = (opposition_bits[a] | opposition_bits[b] | opposition_bits[c])
        possible &= all_mask ^ ((1 << a) | (1 << b) | (1 << c))
        while possible:
            low = possible & -possible
            x = low.bit_length() - 1
            possible ^= low
            quad = tuple(sorted((a, b, c, x)))
            internal_triangles = [
                triple for triple in combinations(quad, 3)
                if all(opposite in opposite_row for opposite in combinations(triple, 2))
            ]
            if triangle != min(internal_triangles):
                continue
            if any(adjacency_bits[u] & (1 << v) for u, v in combinations(quad, 2)):
                continue
            count += 1
            mask = 0
            for pair in combinations(quad, 2):
                row = opposite_row.get(pair)
                if row is not None:
                    mask |= masks[row]
            require(sum(pair in opposite_row for pair in combinations(quad, 2)) >= 4, "triangle dense quad")
            if mask == FULL:
                retained.add(canonical_groups((quad,)))

    for a in range(N):
        for b in range(a + 1, N):
            if (a, b) in opposite_row:
                continue
            common_bits = opposition_bits[a] & opposition_bits[b]
            common = []
            while common_bits:
                low = common_bits & -common_bits
                common.append(low.bit_length() - 1)
                common_bits ^= low
            for c, d in combinations(common, 2):
                if (min(c, d), max(c, d)) in opposite_row:
                    continue
                first_pair = (a, b)
                second_pair = (min(c, d), max(c, d))
                if first_pair >= second_pair:
                    continue
                quad = tuple(sorted((a, b, c, d)))
                require(len(set(quad)) == 4, "C4 vertex collision")
                if any(adjacency_bits[u] & (1 << v) for u, v in combinations(quad, 2)):
                    continue
                count += 1
                mask = 0
                for pair in combinations(quad, 2):
                    row = opposite_row.get(pair)
                    if row is not None:
                        mask |= masks[row]
                require(sum(pair in opposite_row for pair in combinations(quad, 2)) == 4, "induced C4")
                if mask == FULL:
                    retained.add(canonical_groups((quad,)))
    return retained, count, len(triangles)


def quadruple_family(adjacency, adjacency_bits, rhombi, opposite_row, masks,
                     two_covers, three_covers, full_triples):
    candidates = set()
    for rows in three_covers:
        sides = [(rhombi[row][:2], rhombi[row][2:]) for row in rows]
        for choice in range(8):
            vertices = tuple(sorted({vertex for i in range(3) for vertex in sides[i][(choice >> i) & 1]}))
            if len(vertices) == 4 and independent((vertices,), adjacency):
                candidates.add(canonical_groups((vertices,)))
    for first, second in two_covers:
        sides = ((rhombi[first][:2], rhombi[first][2:]), (rhombi[second][:2], rhombi[second][2:]))
        for choice in range(4):
            vertices = tuple(sorted(set(sides[0][choice & 1]) | set(sides[1][(choice >> 1) & 1])))
            if len(vertices) == 4 and independent((vertices,), adjacency):
                candidates.add(canonical_groups((vertices,)))
    for triple in full_triples:
        for vertex in range(N):
            if vertex not in triple and all(vertex not in adjacency[u] for u in triple):
                candidates.add(canonical_groups((tuple(sorted((*triple, vertex))),)))

    dense, dense_count, triangle_count = dense_quadruples(adjacency_bits, opposite_row, masks)
    candidates.update(dense)
    return sorted(candidates), dense_count, triangle_count


def family_result(name, partitions, edges, opposite_row, masks):
    outcomes = Counter()
    digest = sha256()
    for groups in partitions:
        require(invalid_mask(groups, opposite_row, masks) == FULL, name + " rank mask")
        status, witness = assess(edges, groups)
        require(status in ("edge", "k23"), name + " open partition")
        outcomes[status] += 1
        digest.update((json.dumps(groups, separators=(",", ":")) + "\n").encode())
    return {
        "candidates": len(partitions),
        **dict(sorted(outcomes.items())),
        "partition_sha256": digest.hexdigest(),
    }


def orientation_result(certificate, edges):
    cover = set()
    rejected = Counter()
    rejected_digest = sha256()
    survivors = 0
    for leaf in certificate["orientation_cover"]:
        signs = tuple(leaf["signs"])
        require(len(signs) <= 12 and all(sign in (-1, 1) for sign in signs), "orientation prefix")
        for tail in product((-1, 1), repeat=12 - len(signs)):
            word = signs + tail
            require(word not in cover, "orientation-prefix overlap")
            cover.add(word)
        if leaf.get("survivor") is True:
            require(len(signs) == 12, "partial survivor")
            survivors += 1
            continue
        groups = canonical_groups(group_partition(leaf["pairs"]))
        status, witness = assess(edges, groups)
        require(status in ("edge", "k23"), "orientation obstruction")
        rejected[status] += 1
        rejected_digest.update((json.dumps(groups, separators=(",", ":")) + "\n").encode())
    require(len(cover) == 4096 and survivors == 2 and sum(rejected.values()) == 34, "orientation cover")
    return {
        "covered_words": len(cover),
        "rejected_prefixes": sum(rejected.values()),
        "survivors": survivors,
        "obstructions": dict(sorted(rejected.items())),
        "forced_partition_sha256": rejected_digest.hexdigest(),
    }


def verify():
    loaded = load_pinned()
    certificate = loaded["../hadwiger_nelson_heule510_plane_realizations/certificate.json"]
    edges, adjacency, adjacency_bits, kernel_rows = load_graph(loaded)
    rhombi, opposite_row = graph_rhombi(adjacency)
    masks = basis_masks(certificate, rhombi, kernel_rows)
    two_covers, three_covers, eligible = row_covers(masks)

    three_pairs, pair_persistent, pair_repairs = three_pair_family(
        edges, adjacency, rhombi, masks, two_covers, three_covers
    )
    triple_pair, full_triples, opposition_triple_count, triple_persistent, triple_repairs = triple_pair_family(
        edges, adjacency, rhombi, opposite_row, masks, eligible
    )
    quadruples, dense_count, opposition_triangle_count = quadruple_family(
        adjacency, adjacency_bits, rhombi, opposite_row, masks,
        two_covers, three_covers, full_triples
    )

    result = {
        "status": "INDEPENDENTLY_REPRODUCED_NO_EXACT_507_IMAGE_H510_MAP",
        "source_vertices": N,
        "strict_source_unit_pairs": len(edges),
        "rhombi": len(rhombi),
        "rank_prime": RANK_PRIME,
        "rank_bases": len(certificate["bases"]),
        "rank_per_basis": 501,
        "two_row_covers": [list(pair) for pair in two_covers],
        "three_row_covers": len(three_covers),
        "opposition_triples_examined": opposition_triple_count,
        "full_defect_triples": [list(triple) for triple in full_triples],
        "opposition_triangles": opposition_triangle_count,
        "dense_quadruples_examined": dense_count,
        "arbitrary_last_pair_accounting": {
            "three_pairs_persistent_k23": pair_persistent,
            "three_pairs_possible_repairs": pair_repairs,
            "triple_pair_persistent_k23": triple_persistent,
            "triple_pair_possible_repairs": triple_repairs,
        },
        "rank_defect_families": {
            "three_pairs": family_result("three_pairs", three_pairs, edges, opposite_row, masks),
            "triple_pair": family_result("triple_pair", triple_pair, edges, opposite_row, masks),
            "quadruple": family_result("quadruple", quadruples, edges, opposite_row, masks),
        },
        "full_rank_orientation": orientation_result(certificate, edges),
        "exact_507_image_realization_exists": False,
        "record_improvement": False,
        "solver_required": False,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.check_expected:
        expected = json.loads((HERE / "expected.json").read_text())
        require(result == expected, "expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
