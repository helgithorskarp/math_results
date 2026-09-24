#!/usr/bin/env python3
"""Independent exact checks for the uniform-profile realization package.

This program imports no module from the reviewed directory.  It treats the
submitted JSON as untrusted data, reconstructs the Boolean split template,
and exercises a large unequal-class role instance and a padded tag example
that are not read from the submitted audit.
"""

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, permutations, product
from json import dumps, loads
from math import ceil, comb, floor
from pathlib import Path
import sys


CORE = 8
D = 11


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge(a, b):
    return tuple(sorted((a, b)))


def triangle_edges(triple):
    return Counter(edge(a, b) for a, b in combinations(triple, 2))


def boolean_support():
    kinds = set(combinations_with_replacement(range(CORE), 2))
    kinds |= {
        (mask, CORE + bit)
        for bit in range(3)
        for mask in range(CORE)
        if (mask >> bit) & 1
    }
    return kinds


def allowed_triangles(kinds):
    return [
        triple
        for triple in combinations_with_replacement(range(D), 3)
        if set(triangle_edges(triple)) <= kinds
    ]


def submitted_profile(record, kinds, triangles):
    require(record["d"] == D, "wrong number of template types")
    require(record["core_types"] == list(range(CORE)), "wrong clique core")
    expected_cross = kinds - {(i, i) for i in range(CORE)}
    listed = [tuple(row) for row in record["edges"]]
    require(len(listed) == len(set(listed)), "repeated submitted edge type")
    require(set(listed) == expected_cross, "submitted support is not Boolean support")

    profile = {}
    for row in record["profile"]:
        triple = tuple(row["types"])
        require(triple == tuple(sorted(triple)) and triple in triangles,
                "invalid submitted triangle type")
        require(triple not in profile, "repeated submitted triangle type")
        profile[triple] = Q(row["weight"])
    require(set(profile) == set(triangles), "profile does not contain every allowed type")
    require(min(profile.values()) == Q(1, 26) == Q(record["margin"]),
            "incorrect profile margin")

    loads = Counter()
    for triple, weight in profile.items():
        for kind, multiplicity in triangle_edges(triple).items():
            loads[kind] += multiplicity * weight
    capacities = {kind: Q(1, 2) if kind[0] == kind[1] else Q(1) for kind in kinds}
    require(loads == capacities, "profile does not give the exact capacity vector")
    require(sum(profile.values(), Q()) == Q(44, 3), "incorrect profile mass")
    return profile, capacities


def right_inverse(kinds, triangles):
    columns = {}
    for kind in sorted(kinds):
        i, j = kind
        if i == j:
            column = {(i, i, i): Q(1, 3)}
        else:
            if i >= CORE:
                i, j = j, i
            require(i < CORE, "supported cross type has no clique endpoint")
            column = {
                tuple(sorted((i, i, j))): Q(1, 2),
                (i, i, i): Q(-1, 6),
            }
        require(set(column) <= set(triangles), "right inverse uses a nontriangle")
        image = Counter()
        for triple, coefficient in column.items():
            for out_kind, multiplicity in triangle_edges(triple).items():
                image[out_kind] += multiplicity * coefficient
        require(all(image[out_kind] == int(out_kind == kind) for out_kind in kinds),
                "right-inverse column failed")
        columns[kind] = column

    row_norms = Counter()
    for column in columns.values():
        for triple, coefficient in column.items():
            row_norms[triple] += abs(coefficient)
    return columns, max(row_norms.values())


def capacities(sizes, kinds):
    return {
        kind: (Q(comb(sizes[kind[0]], 2)) if kind[0] == kind[1]
               else Q(sizes[kind[0]] * sizes[kind[1]]))
        for kind in kinds
    }


def corrected_profile(base_profile, base_capacities, columns, sizes, scale):
    actual = capacities(sizes, set(base_capacities))
    result = {triple: weight * scale * scale for triple, weight in base_profile.items()}
    for kind, column in columns.items():
        difference = actual[kind] - base_capacities[kind] * scale * scale
        for triple, coefficient in column.items():
            result[triple] += coefficient * difference
    loads = Counter()
    for triple, weight in result.items():
        for kind, multiplicity in triangle_edges(triple).items():
            loads[kind] += multiplicity * weight
    require(loads == actual, "corrected unequal-class profile is not exact")
    require(min(result.values()) > 0, "corrected unequal-class profile is not positive")
    return result, actual


def local_vector(triple, vertex_type):
    remaining = list(triple)
    remaining.remove(vertex_type)
    return Counter(edge(vertex_type, other) for other in remaining)


def audit_large_roles(profile, sizes, kinds):
    order = sum(sizes)
    alpha = Q(1, 12)
    epsilon = Q(1, 7000)
    pattern_bound = comb(D + 2, 3) + comb(D + 1, 2)
    lam = Q(8 * pattern_bound, 1) / alpha
    upper = ceil(lam + 4 * pattern_bound)
    theta = 1 - lam / order
    require(theta > 0, "large role test did not clear the boundary layer")
    require(min(profile.values()) >= epsilon * order * order,
            "large role test is outside the advertised robust region")
    counts = {triple: floor(theta * weight) for triple, weight in profile.items()}
    require(min(counts.values()) > 0, "large role test lost a positive pattern")

    target_edges = Counter()
    for triple, count in counts.items():
        for kind, multiplicity in triangle_edges(triple).items():
            target_edges[kind] += multiplicity * count

    segments = 0
    for vertex_type, part_size in enumerate(sizes):
        divisions = {
            triple: divmod(count * triple.count(vertex_type), part_size)
            for triple, count in counts.items()
            if vertex_type in triple
        }
        breakpoints = sorted({0, part_size} | {remainder for quotient, remainder in divisions.values()})
        incident = sorted(kind for kind in kinds if vertex_type in kind)
        degree_sums = Counter()
        for start, stop in zip(breakpoints, breakpoints[1:]):
            if start == stop:
                continue
            degree = Counter()
            for triple, (quotient, remainder) in divisions.items():
                roles = quotient + int(start < remainder)
                for kind, multiplicity in local_vector(triple, vertex_type).items():
                    degree[kind] += roles * multiplicity
            for kind in incident:
                other = kind[1] if kind[0] == vertex_type else kind[0]
                full_degree = part_size - 1 if kind[0] == kind[1] else sizes[other]
                deficit = full_degree - degree[kind]
                require(2 * pattern_bound <= deficit <= upper,
                        "complement degree left the proved interval")
                degree_sums[kind] += (stop - start) * degree[kind]
            segments += 1
        for kind in incident:
            expected = (2 if kind[0] == kind[1] else 1) * target_edges[kind]
            require(degree_sums[kind] == expected,
                    "rounded roles do not give the target edge incidence")

    return {
        "N": order,
        "M": pattern_bound,
        "lambda": str(lam),
        "U": upper,
        "positive_patterns": len(counts),
        "compressed_segments": segments,
        "minimum_profile_over_N_squared": str(min(profile.values()) / (order * order)),
    }


def audit_tag_example():
    # H has an AAC triangle, one X--Y tag edge, and one isolated role in
    # each of A,C,X,Y.  This role pattern is distinct from the submitted
    # checker's small padded example.
    part_sizes = {"A": 5, "C": 4, "X": 3, "Y": 7}
    role_counts = {"A": 3, "C": 2, "X": 2, "Y": 2}
    mass = 17
    tag_left = ceil(mass / part_sizes["Y"])
    require(tag_left == part_sizes["X"], "tag-left fixture mismatch")
    missing = {
        (j % tag_left, j)
        for j in range(tag_left * part_sizes["Y"] - mass)
    }
    tags = set(product(range(tag_left), range(part_sizes["Y"]))) - missing
    require(len(tags) == mass, "wrong number of tag edges")

    total_maps = 1
    for part, count in role_counts.items():
        value = 1
        for offset in range(count):
            value *= part_sizes[part] - offset
        total_maps *= value
    weight = Q(tag_left * part_sizes["Y"], total_maps)

    tag_load = Counter()
    aa_load = Counter()
    ac_load = Counter()
    restricted_tag_load = Counter()
    valid_maps = 0
    for amap in permutations(range(part_sizes["A"]), role_counts["A"]):
        for cmap in permutations(range(part_sizes["C"]), role_counts["C"]):
            for xmap in permutations(range(part_sizes["X"]), role_counts["X"]):
                for ymap in permutations(range(part_sizes["Y"]), role_counts["Y"]):
                    tag = (xmap[0], ymap[0])
                    if tag not in tags:
                        continue
                    valid_maps += 1
                    tag_load[tag] += weight
                    aa = edge(amap[0], amap[1])
                    tag_triangle_edges = ((amap[0], cmap[0]), (amap[1], cmap[0]))
                    aa_load[aa] += weight
                    for ac in tag_triangle_edges:
                        ac_load[ac] += weight
                    if aa != (0, 1):
                        restricted_tag_load[tag] += weight

    require(set(tag_load.values()) == {Q(1)}, "tag-edge load is not one")
    require(set(aa_load.values()) == {Q(17, 10)}, "AAC internal-edge load is wrong")
    require(set(ac_load.values()) == {Q(17, 10)}, "AAC cross-edge load is wrong")
    require(set(restricted_tag_load.values()) == {Q(9, 10)},
            "tag survival fraction after one removed edge is wrong")
    return {
        "all_type_respecting_maps": total_maps,
        "valid_maps": valid_maps,
        "tag_edges": len(tags),
        "tag_load": "1",
        "original_edge_load": "17/10",
        "tag_load_after_one_AA_edge_removed": "9/10",
    }


def audit_literal_decomposition(record, kinds):
    sizes = record["sizes"]
    require(len(sizes) == D and sum(sizes) == 45, "wrong literal host sizes")
    parent = [vertex_type for vertex_type, size in enumerate(sizes) for _ in range(size)]
    host = {
        pair
        for pair in combinations(range(len(parent)), 2)
        if edge(parent[pair[0]], parent[pair[1]]) in kinds
    }
    used = set()
    for row in record["packing"]:
        triple = tuple(row)
        require(len(triple) == 3 and len(set(triple)) == 3,
                "literal packing has a degenerate triangle")
        require(all(type(vertex) is int and 0 <= vertex < len(parent) for vertex in triple),
                "literal packing vertex is out of range")
        for pair in combinations(sorted(triple), 2):
            require(pair in host, "literal packing uses a nonedge")
            require(pair not in used, "literal packing repeats an edge")
            used.add(pair)
    require(used == host, "literal packing is not an exact decomposition")
    return {"vertices": len(parent), "edges": len(host), "triangles": len(record["packing"])}


def main(path):
    raw = Path(path).read_bytes()
    certificate = loads(raw)
    require(set(certificate) == {"positive_profile", "unequal_decomposition"},
            "unexpected certificate sections")
    kinds = boolean_support()
    triangles = allowed_triangles(kinds)
    require(len(kinds) == 48 and len(triangles) == 150, "Boolean template count changed")
    base_profile, base_capacities = submitted_profile(
        certificate["positive_profile"], kinds, triangles
    )
    columns, row_norm = right_inverse(kinds, triangles)
    require(row_norm == Q(3, 2), "unexpected exact right-inverse row norm")

    # A previously unreported unequal point in the 0.999--1.001 box.
    test_scale = 10_000_000
    offsets = [-10_000, 0, 10_000, 7_919, -4_321, 2_003, -8_888, 9_999, 1_337, -7_777, 5_555]
    sizes = [test_scale + offset for offset in offsets]
    require(all(Q(999, 1000) * test_scale <= size <= Q(1001, 1000) * test_scale
                for size in sizes), "unequal fixture is outside the box")
    profile, actual_capacities = corrected_profile(
        base_profile, base_capacities, columns, sizes, test_scale
    )
    require(sum(profile.values(), Q()) == sum(actual_capacities.values(), Q()) / 3,
            "unequal profile mass does not equal one third of the edge count")

    output = {
        "status": "PASS",
        "certificate_sha256": sha256(raw).hexdigest(),
        "boolean_profile": {
            "edge_types": len(kinds),
            "triangle_types": len(triangles),
            "minimum_mass": str(min(base_profile.values())),
            "total_mass": str(sum(base_profile.values(), Q())),
            "right_inverse_columns": len(columns),
            "exact_maximum_row_norm": str(row_norm),
        },
        "new_unequal_role_test": audit_large_roles(profile, sizes, kinds),
        "new_padded_tag_test": audit_tag_example(),
        "literal_decomposition": audit_literal_decomposition(
            certificate["unequal_decomposition"], kinds
        ),
        "trust_boundary": (
            "Finite exact checks only. Keevash Theorem 5.15 and the written "
            "uniform asymptotic reduction are audited mathematically, not proved by this program."
        ),
    }
    return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: independent_check.py CERTIFICATES.json")
    print(dumps(main(sys.argv[1]), indent=2, sort_keys=True))
