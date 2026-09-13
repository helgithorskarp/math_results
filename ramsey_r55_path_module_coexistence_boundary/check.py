"""Independent full control audit and complete path-cover certificate checker.

The module algorithm enumerates intersections of signed neighborhoods;
the C++ audit instead enumerates subsets of each signed neighborhood.
Path words here come from permutations, not degrees and connectivity.
"""

import argparse
from functools import lru_cache
from itertools import combinations, permutations
import hashlib
import json
from math import comb
from pathlib import Path
import struct


def require(condition, message):
    if not condition:
        raise ValueError(message)


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def audit(graph_path, certificate_path, native_path):
    lines = graph_path.read_text().splitlines()
    n, m = map(int, lines[0].split())
    require(n == 43 and len(lines) == m + 1, "graph header")
    red = [0] * n
    for line in lines[1:]:
        u, v = map(int, line.split())
        require(0 <= u < v < n and not red[u] >> v & 1, "simple edge input")
        red[u] |= 1 << v
        red[v] |= 1 << u
    full = (1 << n) - 1
    blue = [full ^ red[v] ^ (1 << v) for v in range(n)]
    require(all(18 <= x.bit_count() <= 24 for x in red + blue), "degree window")
    pair_positions = list(combinations(range(5), 2))
    positions = {pair: j for j, pair in enumerate(pair_positions)}
    red_words = {
        sum(1 << positions[tuple(sorted((p[i], p[i + 1])))] for i in range(4))
        for p in permutations(range(5))
    }
    blue_words = {1023 ^ word for word in red_words}
    require(len(red_words) == len(blue_words) == 60 and
            not red_words & blue_words, "path-word construction")

    def word(q):
        return sum(((red[q[i]] >> q[j]) & 1) << k
                   for k, (i, j) in enumerate(pair_positions))

    # Actual full graph scan, with no Ramsey premise.
    defects, path_counts = [], [0, 0]
    parent = list(range(n))

    def root(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for q in combinations(range(n), 5):
        w = word(q)
        if w in (0, 1023):
            defects.append([*q, 1 if w == 1023 else 2])
        if w in red_words or w in blue_words:
            path_counts[w in blue_words] += 1
            for v in q:
                parent[root(v)] = root(q[0])
    components = {}
    for v in range(n):
        r = root(v)
        components[r] = components.get(r, 0) + 1
    require(len(defects) == 7, "control must have its seven documented defects")

    # Every intersection of any subfamily of the 86 attribute extents.
    # Once an intersection has size <2 no descendant can be relevant.
    extents = {full}
    for attribute in red + blue:
        extents.update(extent & attribute for extent in list(extents)
                       if (extent & attribute).bit_count() >= 2)
    maxima = {2: 0, 3: 0}
    witnesses = {2: None, 3: None}
    for extent in sorted(extents):
        r = b = full
        for v in vertices(extent):
            r &= red[v]
            b &= blue[v]
        if not r | b:
            continue
        score = extent.bit_count() + (r | b).bit_count()
        for minimum in (2, 3):
            if extent.bit_count() >= minimum and score > maxima[minimum]:
                maxima[minimum] = score
                witnesses[minimum] = {
                    "module": list(vertices(extent)),
                    "red_uniform": list(vertices(r)),
                    "blue_uniform": list(vertices(b)),
                }
    require(maxima[2] < 36 and maxima[3] < 28, "full deletion-module resilience")

    # Audit local consequences and an explicitly omitted Ramsey condition.
    pair_min, triple_min = n, n
    common_pair_max = 0
    triangle_common_max = [0, 0]
    triangle_violations = []
    for u, v in combinations(range(n), 2):
        pair_min = min(pair_min, ((red[u] ^ red[v]) & ~(1 << u) & ~(1 << v)).bit_count())
        color = red if red[u] >> v & 1 else blue
        common_pair_max = max(common_pair_max, (color[u] & color[v]).bit_count())
    for q in combinations(range(n), 3):
        qmask = sum(1 << v for v in q)
        r = red[q[0]] & red[q[1]] & red[q[2]]
        b = blue[q[0]] & blue[q[1]] & blue[q[2]]
        triple_min = min(triple_min, (full & ~qmask & ~(r | b)).bit_count())
        for index, color in enumerate((red, blue)):
            if all(color[u] >> v & 1 for u, v in combinations(q, 2)):
                uniform = r if index == 0 else b
                triangle_common_max[index] = max(triangle_common_max[index], uniform.bit_count())
                if uniform.bit_count() > 4:
                    triangle_violations.append({"triangle": list(q), "color": index + 1,
                                                "common_neighbors": list(vertices(uniform))})
    require(pair_min >= 8 and triple_min >= 18 and common_pair_max <= 13,
            "displayed local distinguishing and pair conditions")

    # The certificate stream has one literal five-set per required subset.
    data = certificate_path.read_bytes()
    offset = 0

    @lru_cache(maxsize=None)
    def type_of(mask):
        require(mask >= 0 and mask <= full and mask.bit_count() == 5, "witness form")
        w = word(tuple(vertices(mask)))
        return 1 if w in red_words else (2 if w in blue_words else 0)

    def cover(pool, threshold, wanted):
        nonlocal offset
        records = 0
        for subset in combinations(pool, threshold):
            require(offset + 8 <= len(data), "missing coverage record")
            witness, = struct.unpack_from("<Q", data, offset)
            offset += 8
            mask = sum(1 << v for v in subset)
            require(witness & mask == witness, "witness outside represented subset")
            kind = type_of(witness)
            require(kind != 0 and (wanted == 0 or kind == wanted), "wrong induced path")
            records += 1
        require(records == comb(len(pool), threshold), "coverage cardinality")
        return records

    global_records = [cover(range(21), 13, 0), cover(range(21, 43), 14, 0)]
    neighborhood_records = []
    for v in range(n):
        for wanted, color in ((1, red), (2, blue)):
            neighborhood_records.append(cover(list(vertices(color[v])), 18, wanted))
    require(offset == len(data), "trailing coverage records")
    native = json.loads(native_path.read_text())
    agreement = {
        "module_subset_visits": sum((1 << a.bit_count()) - 1 - a.bit_count() for a in red + blue),
        "maximum_induced_order_with_module_size_at_least_two": maxima[2],
        "maximum_induced_order_with_module_size_at_least_three": maxima[3],
        "red_paths": path_counts[0], "blue_paths": path_counts[1],
        "path_component_sizes": sorted(components.values()), "defects": defects,
        "global_cover_records": global_records,
        "neighborhood_cover_records": sum(neighborhood_records),
        "neighborhood_records_by_root_and_color": neighborhood_records,
        "total_records": offset // 8, "cover_bytes": offset,
    }
    for key, value in agreement.items():
        require(native[key] == value, "native disagreement: " + key)
    return {
        "status": "CHECKED_FULL_PATH_MODULE_COEXISTENCE_CONTROL",
        "native_agreement": agreement,
        "closed_extents_at_least_two": len(extents),
        "module_maximum_witnesses": witnesses,
        "minimum_pair_distinguishers": pair_min,
        "minimum_triple_distinguishers": triple_min,
        "maximum_same_color_pair_common_neighbors": common_pair_max,
        "maximum_same_color_triangle_common_neighbors": triangle_common_max,
        "omitted_triangle_cap_violations": triangle_violations,
        "cover_sha256": hashlib.sha256(data).hexdigest(),
        "graph_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        "all_26_sets_have_path_or_antipath": True,
        "all_neighborhood_18_sets_have_required_color_path": True,
        "all_36_plus_induced_subgraphs_prime": True,
        "all_28_plus_induced_subgraphs_have_no_proper_module_of_size_at_least_three": True,
        "good43": False,
        "disconnected_path_class_excluded": False,
        "first_gate_met": False,
        "scope": "Complete specified necessary system on one unchanged bad graph; no good43 decision",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.graph, args.cover, args.native)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])


if __name__ == "__main__":
    main()
