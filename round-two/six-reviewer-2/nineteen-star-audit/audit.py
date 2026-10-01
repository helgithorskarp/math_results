#!/usr/bin/env python3
"""Independent completion and point-isomorphism audit; no author imports."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import factorial, lcm
from pathlib import Path
import hashlib
import json
import subprocess
import time


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(data):
    return (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(data):
    return hashlib.sha256(encode(data)).hexdigest()


def bitword(points):
    return sum(1 << x for x in points)


def points(word):
    return tuple(x for x in range(17) if word & (1 << x))


def construct(lengths):
    missing = set()
    offset = 0
    for size in lengths:
        missing |= {(offset + i, offset + i) for i in range(size)}
        missing |= {(offset + i, offset + (i + 1) % size) for i in range(size)}
        offset += size
    occupied = set(product(range(5), repeat=2)) - missing
    # Deliberately use column-major point labels during construction.
    cells = sorted(occupied, key=lambda cell: (cell[1], cell[0]))
    require(len(cells) == 15, "wrong cell domain")
    raw_anchors = [frozenset([15] + [i for i, (r, c) in enumerate(cells) if r == row])
                   for row in range(5)]
    raw_anchors += [frozenset([16] + [i for i, (r, c) in enumerate(cells) if c == col])
                    for col in range(5)]
    candidates = []
    for word in combinations(range(15), 4):
        if len({cells[x][0] for x in word}) == 4 and len({cells[x][1] for x in word}) == 4:
            candidates.append(word)
    # Test the row/column condition against literal anchor pair ownership.
    forbidden = {tuple(sorted(p)) for a in raw_anchors for p in combinations(a, 2)}
    require(len(forbidden) == 60, "anchor pairs overlap")
    literal = [w for w in combinations(range(15), 4)
               if all(p not in forbidden for p in combinations(w, 2))]
    require(candidates == literal, "matching/pair candidate bridge fails")
    pairsets = [set(combinations(w, 2)) for w in candidates]
    raw_rows = [{j for j, pairs in enumerate(pairsets) if i != j and a.isdisjoint(pairs)}
                for i, a in enumerate(pairsets)]
    require(all((j in raw_rows[i]) == (i != j and len(set(a) & set(b)) <= 1)
                for i, a in enumerate(candidates) for j, b in enumerate(candidates)),
            "pair/point compatibility bridge fails")
    # Transport to the author's documented lexical convention only for comparison.
    canonical_cells = sorted(occupied)
    lookup = {cell: i for i, cell in enumerate(canonical_cells)}
    transport = tuple(lookup[cell] for cell in cells) + (15, 16)
    canonical_words = [tuple(sorted(transport[x] for x in w)) for w in candidates]
    order = sorted(range(len(candidates)), key=lambda i: canonical_words[i])
    inverse_order = {old: new for new, old in enumerate(order)}
    columns = [canonical_words[i] for i in order]
    neighbors = [{inverse_order[j] for j in raw_rows[i]} for i in order]
    anchors = [bitword(transport[x] for x in a) for a in raw_anchors]
    return {"cells": canonical_cells, "anchors": anchors, "columns": columns,
            "neighbors": neighbors, "missing": missing, "transport": transport}


def graph_text(neighbors, target):
    return "%d %d\n" % (len(neighbors), target) + "".join(
        str(len(row)) + " " + " ".join(map(str, sorted(row))) + "\n" for row in neighbors)


def native_cliques(model, executable):
    graph = model["neighbors"]
    # Degeneracy ordering is a bijective vertex permutation, not a symmetry quotient.
    remaining = set(range(len(graph)))
    order = []
    while remaining:
        v = min(remaining, key=lambda x: (len(graph[x] & remaining), x))
        order.append(v)
        remaining.remove(v)
    inverse = {v: i for i, v in enumerate(order)}
    rows = [{inverse[w] for w in graph[v]} for v in order]
    started = time.monotonic()
    p = subprocess.run([str(executable)], input=graph_text(rows, 9), capture_output=True,
                       text=True, timeout=30)
    require(p.returncode == 0, "native census failed: " + p.stderr)
    data = json.loads(p.stdout)
    require(data["status"] == "COMPLETE", "native census incomplete")
    require(not data["larger_clique"], "ten-clique exists")
    cliques = sorted(tuple(sorted(order[x] for x in q)) for q in data["cliques"])
    require(len(cliques) == len(set(cliques)), "native census duplicates")
    require(all(len(q) == 9 and len(set(q)) == 9 and
                all(b in graph[a] for a, b in combinations(q, 2)) for q in cliques),
            "native result is not a nine-clique")
    return cliques, {"nodes": data["nodes"], "seconds": time.monotonic() - started,
                     "larger_clique": data["larger_clique"]}


def graph_isomorphisms(source, target):
    """Generic adjacency/nonadjacency backtracking, with whole-side orientation.

    No cycle rotations, row permutations or column-signature algorithm.
    Each choice respects all already mapped pairs. The minimum remaining
    domain only changes order, and every possible image is explored.
    """
    require(len(source) == len(target) == 10, "bipartite graph must have ten vertices")
    output = []
    for swap in (False, True):
        mapping = {}
        used = set()

        def options(v):
            side = (v >= 5) != swap
            return [w for w in range(10) if (w >= 5) == side and w not in used
                    and len(source[v]) == len(target[w])
                    and all((a in source[v]) == (b in target[w]) for a, b in mapping.items())]

        def visit():
            if len(mapping) == 10:
                output.append(tuple(mapping[i] for i in range(10)))
                return
            unmapped = [v for v in range(10) if v not in mapping]
            domains = {v: options(v) for v in unmapped}
            v = min(unmapped, key=lambda x: (len(domains[x]), -len(source[x] & mapping.keys()), x))
            for w in domains[v]:
                mapping[v] = w
                used.add(w)
                visit()
                used.remove(w)
                del mapping[v]

        visit()
    require(len(output) == len(set(output)), "duplicate graph isomorphism")
    require(all(set(p) == set(range(10)) and
                all((b in source[a]) == (p[b] in target[p[a]])
                    for a in range(10) for b in range(10)) for p in output),
            "invalid graph isomorphism")
    return sorted(output)


def hole_graph(missing):
    rows = [set() for _ in range(10)]
    for r, c in missing:
        rows[r].add(5 + c)
        rows[5 + c].add(r)
    require(all(len(row) == 2 for row in rows), "missing-cell graph not degree two")
    return rows


def mapped_cell(mapping, r, c):
    a, b = mapping[r], mapping[5 + c]
    return (a, b - 5) if a < 5 else (b, a - 5)


def anchor_group(model):
    graph = hole_graph(model["missing"])
    lookup = {cell: i for i, cell in enumerate(model["cells"])}
    maps = []
    for p in graph_isomorphisms(graph, graph):
        maps.append(tuple(lookup[mapped_cell(p, r, c)] for r, c in model["cells"]) +
                    ((15, 16) if p[0] < 5 else (16, 15)))
    maps = sorted(maps)
    require(all(set(p) == set(range(17)) for p in maps), "anchor map not bijective")
    require(tuple(range(17)) in maps, "identity absent")
    require(all(tuple(a[b[x]] for x in range(17)) in maps for a in maps for b in maps),
            "point group not closed")
    anchor_sets = {frozenset(points(w)) for w in model["anchors"]}
    require(all({frozenset(p[x] for x in w) for w in anchor_sets} == anchor_sets for p in maps),
            "point map breaks anchors")
    return maps


def inspect(words):
    require(len(words) == 19 and len(set(words)) == 19, "not nineteen distinct words")
    require(all(type(w) is int and 0 <= w < (1 << 17) and w.bit_count() == 4 for w in words),
            "malformed quadruple")
    ownership = [pair for w in words for pair in combinations(points(w), 2)]
    require(len(ownership) == len(set(ownership)) == 114, "repeated covered pair")
    replication = [sum(x in points(w) for w in words) for x in range(17)]
    require(max(replication) <= 5, "replication exceeds five")
    deficient = {x for x, r in enumerate(replication) if r < 5}
    leave = set(combinations(range(17), 2)) - set(ownership)
    require(len(leave) == 22, "wrong leave size")
    marks = sorted((x, y) for x, y in leave if x not in deficient and y not in deficient)
    high_edges = sum(x in deficient and y in deficient for x, y in leave)
    require(high_edges - len(marks) == len(deficient) + 5, "leave degree identity fails")
    require(all(sum(x in e for e in leave) == 16 - 3 * replication[x] for x in range(17)),
            "pointwise leave degree fails")
    return {"positive_deficits": sorted(5 - replication[x] for x in deficient),
            "low_low_pairs": len(marks), "high_high_pairs": high_edges,
            "homogeneous_pairs": high_edges + len(marks)}, marks


def transformed(word, mapping):
    return bitword(mapping[x] for x in points(word))


def permutation_order(mapping):
    unused = set(range(len(mapping)))
    lengths = []
    while unused:
        start = min(unused)
        x, size = start, 0
        while True:
            unused.remove(x)
            size += 1
            x = mapping[x]
            if x == start:
                break
        lengths.append(size)
    return lcm(*lengths)


def marked_classes(cliques, model, group):
    masks = [bitword(w) for w in model["columns"]]
    lookup = {mask: i for i, mask in enumerate(masks)}
    induced = [tuple(lookup[transformed(w, p)] for w in masks) for p in group]
    universe = set(cliques)
    visited = set()
    entries = []
    for q in cliques:
        if q in visited:
            continue
        orbit = {tuple(sorted(p[i] for i in q)) for p in induced}
        require(orbit <= universe and not (orbit & visited), "orbit coverage fails")
        require(q == min(orbit), "representative not least")
        visited |= orbit
        stabilizer = sum(tuple(sorted(p[i] for i in q)) == q for p in induced)
        require(stabilizer * len(orbit) == len(group), "marked orbit-stabilizer fails")
        stats, marks = inspect(model["anchors"] + [masks[i] for i in q])
        entries.append({"clique": list(q), "orbit_size": len(orbit),
                        "anchor_stabilizer_order": stabilizer, **stats})
    require(visited == universe, "missed marked orbit")
    return entries


def normalize_maps(words, pair, model):
    u, v = pair
    rows = sorted(points(w) for w in words if w & (1 << u))
    cols = sorted(points(w) for w in words if w & (1 << v))
    require(len(rows) == len(cols) == 5, "anchor not saturated")
    positions = {}
    for x in range(17):
        if x in pair:
            continue
        rr = [i for i, w in enumerate(rows) if x in w]
        cc = [i for i, w in enumerate(cols) if x in w]
        require(len(rr) == len(cc) == 1, "anchor partition fails")
        positions[x] = rr[0], cc[0]
    require(len(set(positions.values())) == 15, "opposite partitions repeat pair")
    source = hole_graph(set(product(range(5), repeat=2)) - set(positions.values()))
    output = []
    target = hole_graph(model["missing"])
    cells = {cell: i for i, cell in enumerate(model["cells"])}
    for p in graph_isomorphisms(source, target):
        mapping = {x: cells[mapped_cell(p, r, c)] for x, (r, c) in positions.items()}
        mapping[u], mapping[v] = ((15, 16) if p[0] < 5 else (16, 15))
        require(set(mapping.values()) == set(range(17)), "normalized point map not bijective")
        pointmap = tuple(mapping[x] for x in range(17))
        moved = [transformed(w, pointmap) for w in words]
        require(set(model["anchors"]) <= set(moved), "normalized anchors absent")
        output.append(pointmap)
    return output


def normalize_mark(words, pair, models):
    choices = []
    for model_id, model in enumerate(models):
        candidates = {tuple(w): i for i, w in enumerate(model["columns"])}
        for mapping in normalize_maps(words, pair, model):
            moved = [transformed(w, mapping) for w in words]
            residual = [w for w in moved if not (w & ((1 << 15) | (1 << 16)))]
            require(len(residual) == 9, "normalized residual count fails")
            q = tuple(sorted(candidates[points(w)] for w in residual))
            choices.append((model_id, q))
    require(bool(choices), "normal form missing")
    return min(choices)


def audit(executable):
    models = [construct((5,)), construct((2, 3))]
    records, carriers, performance = [], [], []
    for lengths, model in zip(((5,), (2, 3)), models):
        cliques, measured = native_cliques(model, executable)
        group = anchor_group(model)
        masks = [bitword(w) for w in model["columns"]]
        census = Counter(encode(inspect(model["anchors"] + [masks[i] for i in q])[0])
                         for q in cliques)
        entries = marked_classes(cliques, model, group)
        adjacency = [bitword(row) for row in model["neighbors"]]
        records.append({"cycle_half_lengths": list(lengths), "candidate_count": len(masks),
                        "edge_count": sum(len(row) for row in model["neighbors"]) // 2,
                        "candidate_sha256": digest(model["columns"]), "adjacency_sha256": digest(adjacency),
                        "nine_clique_count": len(cliques), "nine_clique_sha256": digest(cliques),
                        "anchor_group_order": len(group), "marked_classes": entries,
                        "profile_census": [dict(json.loads(k), count=count) for k, count in sorted(census.items())]})
        carriers.append({"cells": model["cells"], "anchors": model["anchors"],
                         "columns": model["columns"], "adjacency": adjacency,
                         "nine_cliques": cliques, "group": group})
        performance.append(measured)
    unmarked = defaultdict(list)
    for model_id, record in enumerate(records):
        model = models[model_id]
        for entry in record["marked_classes"]:
            q = tuple(entry["clique"])
            words = model["anchors"] + [bitword(model["columns"][i]) for i in q]
            stats, marks = inspect(words)
            key = min(normalize_mark(words, pair, models) for pair in marks)
            require(key[1] in set(carriers[key[0]]["nine_cliques"]), "normalized completion not enumerated")
            unmarked[key].append([model_id, list(q)])
    classes = [{"model": key[0], "clique": list(key[1]), "marked_classes": value}
               for key, value in sorted(unmarked.items())]
    manifest = {"format": "nineteen-star-census-v1", "models": records,
                "unmarked_class_count": len(classes), "unmarked_classes": classes}
    # Explicit automorphism lifting and exact labeled counts, derived from the census.
    by_marked = {(i, tuple(e["clique"])): e for i, r in enumerate(records) for e in r["marked_classes"]}
    automorphisms = []
    weighted_total = Fraction(0)
    for entry in classes:
        key = entry["model"], tuple(entry["clique"])
        marked = by_marked[key]
        m = marked["low_low_pairs"]
        eligible_orbit = m // len(entry["marked_classes"])
        require(eligible_orbit * len(entry["marked_classes"]) == m, "eligible pair orbits inconsistent")
        full_order = marked["anchor_stabilizer_order"] * eligible_orbit
        model = models[key[0]]
        words = model["anchors"] + [bitword(model["columns"][i]) for i in key[1]]
        _, pairs = inspect(words)
        actual_group = sorted({p for pair in pairs for p in normalize_maps(words, pair, model)
                               if {transformed(w, p) for w in words} == set(words)})
        require(len(actual_group) == full_order, "direct automorphism lift disagrees")
        require(tuple(range(17)) in actual_group and all(
            tuple(a[b[x]] for x in range(17)) in actual_group
            for a in actual_group for b in actual_group), "full point group not closed")
        largest_element_order = max(permutation_order(p) for p in actual_group)
        require(largest_element_order == full_order, "noncyclic point group found")
        weighted_total += Fraction(1, full_order)
        automorphisms.append({"model":key[0], "clique":list(key[1]),
                              "eligible_pair_count":m, "eligible_pair_orbit_size":eligible_orbit,
                              "point_automorphism_order":full_order,
                              "maximum_element_order":largest_element_order,
                              "cyclic":True,
                              "point_automorphisms":[list(p) for p in actual_group]})
    normalized_labeled = sum(Fraction(row["count"], r["anchor_group_order"] * row["low_low_pairs"])
                             for r in records for row in r["profile_census"])
    require(weighted_total == normalized_labeled, "two labeled count derivations disagree")
    labeled_count = weighted_total * factorial(17)
    require(labeled_count.denominator == 1, "labeled count not integral")
    refinement = {"point_automorphism_orders": automorphisms,
                  "cyclic_point_group_distribution":dict(sorted(Counter(
                      str(e["point_automorphism_order"]) for e in automorphisms).items())),
                  "reciprocal_automorphism_sum":str(weighted_total),
                  "labeled_packings_on_fixed_seventeen_set":labeled_count.numerator,
                  "normalization_point_transports":[list(m["transport"]) for m in models]}
    return manifest, carriers, refinement, performance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path, required=True)
    parser.add_argument("--author-manifest", type=Path)
    parser.add_argument("--author-carriers", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    manifest, carriers, refinement, performance = audit(args.native.resolve())
    if args.author_manifest:
        require(json.loads(encode(manifest)) == json.loads(args.author_manifest.read_text()),
                "author manifest differs entrywise")
    if args.author_carriers:
        require(json.loads(encode(carriers)) == json.loads(args.author_carriers.read_text()),
                "author full carriers differ entrywise")
    result = {"reviewer":"six-reviewer-2", "role":"independent mathematical reviewer",
              "status":"COMPLETE", "manifest":manifest, "refinement":refinement}
    expected = Path(__file__).with_name("EXPECTED.json")
    if expected.exists():
        require(json.loads(encode(result)) == json.loads(expected.read_text()), "expected output differs")
    if args.output:
        args.output.write_bytes(encode(result))
    print(json.dumps({"status":"COMPLETE", "manifest_sha256":digest(manifest),
                      "nine_cliques":sum(r["nine_clique_count"] for r in manifest["models"]),
                      "marked_classes":sum(len(r["marked_classes"]) for r in manifest["models"]),
                      "unmarked_classes":manifest["unmarked_class_count"],
                      "refinement":{k:v for k,v in refinement.items() if k not in
                                    ("point_automorphism_orders","normalization_point_transports")},
                      "performance":performance, "seconds":time.monotonic()-started},indent=2))


if __name__ == "__main__":
    main()
