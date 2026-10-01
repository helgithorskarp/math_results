"""Producer-free literal rebuild, pivoted maximal-clique census and cycle maps."""
import argparse
from collections import Counter, defaultdict
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
MAX_NODES = 2000000
MAX_SECONDS = 20


def check(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha(value):
    return hashlib.sha256(encode(value)).hexdigest()


def reconstruct(lengths):
    # Walk the edges of each alternating missing-cell cycle.
    holes = set()
    start = 0
    for size in lengths:
        for row in range(start, start+size):
            successor = start+(row-start+1) % size
            holes.add((row, row))
            holes.add((row, successor))
        start += size
    cells = sorted(set(product(range(5), repeat=2))-holes)
    check(len(cells) == 15, "wrong occupied-cell count")
    anchors = [frozenset([15]+[i for i, cell in enumerate(cells) if cell[0] == r])
               for r in range(5)]
    anchors += [frozenset([16]+[i for i, cell in enumerate(cells) if cell[1] == c])
                for c in range(5)]
    check(all(len(w) == 4 for w in anchors), "anchor size")
    covered = [frozenset(p) for w in anchors for p in combinations(sorted(w), 2)]
    check(len(covered) == len(set(covered)) == 60, "repeated anchor pair")
    forbidden = set(covered)
    columns, pairsets = [], []
    for word in combinations(range(15), 4):
        pairs = frozenset(frozenset(p) for p in combinations(word, 2))
        if not forbidden.intersection(pairs):
            columns.append(word)
            pairsets.append(pairs)
    neighbors = [set(j for j, q in enumerate(pairsets)
                     if i != j and p.isdisjoint(q)) for i, p in enumerate(pairsets)]
    # Check the whole graph using intersections, separately from pair ownership.
    for i, a in enumerate(columns):
        for j, b in enumerate(columns):
            check((j in neighbors[i]) == (i != j and len(set(a).intersection(b)) <= 1),
                  "adjacency disagreement")
    return cells, anchors, columns, neighbors, holes


def maximal_cliques(neighbors, minimum, node_cap=MAX_NODES, seconds=MAX_SECONDS):
    check(type(minimum) is int and minimum > 0, "invalid minimum")
    check(type(node_cap) is int and 0 < node_cap <= MAX_NODES, "invalid node guard")
    check(0 < seconds <= MAX_SECONDS, "invalid time guard")
    started = time.monotonic()
    nodes = 0
    result = []

    def visit(chosen, possible, previous):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap or time.monotonic()-started > seconds:
            raise RuntimeError("INCOMPLETE: literal maximal-clique guard")
        if len(chosen)+len(possible) < minimum:
            return
        if not possible:
            if not previous:
                result.append(tuple(sorted(chosen)))
            return
        pivot = max(possible | previous, key=lambda v: (len(neighbors[v] & possible), -v))
        for vertex in sorted(possible-neighbors[pivot]):
            visit(chosen+[vertex], possible & neighbors[vertex], previous & neighbors[vertex])
            possible.remove(vertex)
            previous.add(vertex)

    visit([], set(range(len(neighbors))), set())
    check(len(result) == len(set(result)), "duplicated maximal clique")
    return sorted(result), nodes


def inspect(words):
    check(len(words) == len(set(words)) == 19, "invalid packing cardinality")
    check(all(len(w) == 4 and all(type(x) is int and 0 <= x < 17 for x in w)
              for w in words), "invalid literal word")
    pairs = [frozenset(p) for w in words for p in combinations(sorted(w), 2)]
    check(len(pairs) == len(set(pairs)) == 114, "packing repeats a pair")
    replication = [sum(x in w for w in words) for x in range(17)]
    check(max(replication) <= 5, "point replication")
    high = set(x for x, r in enumerate(replication) if r < 5)
    leave = set(frozenset(p) for p in combinations(range(17), 2))-set(pairs)
    high_high = sum(p <= high for p in leave)
    low_low = sum(p.isdisjoint(high) for p in leave)
    check(len(leave) == 22 and high_high-low_low == len(high)+5, "literal leave identity")
    stats = {"positive_deficits": sorted(5-r for r in replication if r < 5),
             "low_low_pairs": low_low, "high_high_pairs": high_high,
             "homogeneous_pairs": high_high+low_low}
    marks = sorted(tuple(sorted(p)) for p in leave if p.isdisjoint(high))
    return stats, marks


def cycle_group(cells, anchors, holes):
    graph = [set() for _ in range(10)]
    for r, c in holes:
        graph[r].add(5+c)
        graph[5+c].add(r)
    check(all(len(a) == 2 for a in graph), "hole graph degree")
    unused = set(range(10))
    cycles = []
    while unused:
        root = min(unused)
        cycle = [root]
        previous, current = root, min(graph[root])
        while current != root:
            cycle.append(current)
            next_vertex = next(v for v in graph[current] if v != previous)
            previous, current = current, next_vertex
        check(set(cycle) <= unused, "bad cycle partition")
        unused.difference_update(cycle)
        cycles.append(cycle)
    check(sorted(len(c) for c in cycles) in ([10], [4, 6]), "cycle normal forms")
    choices = []
    for cycle in cycles:
        maps = []
        for sign in (-1, 1):
            for shift in range(len(cycle)):
                mapping = {v: cycle[(shift+sign*i) % len(cycle)] for i, v in enumerate(cycle)}
                swap = mapping[cycle[0]] >= 5
                check(all((mapping[v] >= 5) == ((v >= 5) != swap) for v in cycle),
                      "inconsistent cycle sides")
                maps.append((swap, mapping))
        choices.append(maps)
    index = {cell: i for i, cell in enumerate(cells)}
    group = set()
    for selections in product(*choices):
        if len({swap for swap, mapping in selections}) != 1:
            continue
        swap = selections[0][0]
        graphmap = {v: image for kind, mapping in selections for v, image in mapping.items()}
        moved = []
        for r, c in cells:
            a, b = graphmap[r], graphmap[5+c]
            moved.append(index[(b, a-5)] if swap else index[(a, b-5)])
        moved += [16, 15] if swap else [15, 16]
        group.add(tuple(moved))
    group = sorted(group)
    identity = tuple(range(17))
    check(identity in group, "group lacks identity")
    check(all(tuple(a[b[i]] for i in range(17)) in group for a in group for b in group),
          "group not closed")
    for mapping in group:
        check(set(mapping) == set(range(17)), "point map is not bijective")
        check({frozenset(mapping[x] for x in w) for w in anchors} == set(anchors),
              "point map breaks anchors")
    return group


def orbit_partition(cliques, model, group):
    cells, anchors, columns, neighbors, holes = model
    lookup = {frozenset(w): i for i, w in enumerate(columns)}
    induced = [[lookup[frozenset(mapping[x] for x in w)] for w in columns] for mapping in group]
    buckets = defaultdict(list)
    for q in cliques:
        representative = min(tuple(sorted(mapping[i] for i in q)) for mapping in induced)
        buckets[representative].append(q)
    entries = []
    for q, orbit in sorted(buckets.items()):
        stats, marks = inspect(anchors+[frozenset(columns[i]) for i in q])
        actual_images = {tuple(sorted(mapping[i] for i in q)) for mapping in induced}
        check(actual_images == set(orbit), "incomplete literal orbit")
        stabilizers = sum(tuple(sorted(mapping[i] for i in q)) == q for mapping in induced)
        check(stabilizers*len(orbit) == len(group), "orbit stabilizer identity")
        entries.append({"clique": list(q), "orbit_size": len(orbit),
                        "anchor_stabilizer_order": stabilizers, **stats})
    return entries


def canonical_mark(words, u, v, models):
    """Assign rows, then solve column domains from their actual hole signatures."""
    output = []
    for first, second in ((u, v), (v, u)):
        rows = sorted(tuple(sorted(w-{first})) for w in words if first in w)
        cols = sorted(tuple(sorted(w-{second})) for w in words if second in w)
        check(len(rows) == len(cols) == 5, "new anchor is not saturated")
        position = {x: (next(i for i, r in enumerate(rows) if x in r),
                         next(i for i, c in enumerate(cols) if x in c))
                    for x in range(17) if x not in (first, second)}
        check(len(set(position.values())) == 15, "nonbinary new anchor matrix")
        occupied = set(position.values())
        residual = [w for w in words if first not in w and second not in w]
        check(len(residual) == 9, "new anchor residual size")
        for model_id, model in enumerate(models):
            cells, anchors, columns, neighbors, holes = model
            cell_index = {cell: i for i, cell in enumerate(cells)}
            word_index = {frozenset(w): i for i, w in enumerate(columns)}
            for rowmap in permutations(range(5)):
                domains = [set(k for k in range(5)
                               if all(((r, c) in occupied) == ((rowmap[r], k) in cell_index)
                                      for r in range(5))) for c in range(5)]
                if any(not domain for domain in domains):
                    continue

                def assign(colmap, used):
                    if len(colmap) == 5:
                        pointmap = {x: cell_index[rowmap[r], colmap[c]] for x, (r, c) in position.items()}
                        q = tuple(sorted(word_index[frozenset(pointmap[x] for x in w)] for w in residual))
                        output.append((model_id, q))
                        return
                    c = len(colmap)
                    for k in sorted(domains[c]-used):
                        assign(colmap+[k], used | {k})

                assign([], set())
    check(bool(output), "unmarked normal form missing")
    return min(output)


def verify(expected=None, comparison=None):
    models = [reconstruct((5,)), reconstruct((2, 3))]
    records, carriers, performance = [], [], []
    for lengths, model in zip(((5,), (2, 3)), models):
        started = time.monotonic()
        cells, anchors, columns, neighbors, holes = model
        maximal, nodes = maximal_cliques(neighbors, 9)
        check(all(len(q) == 9 for q in maximal), "larger clique found")
        cliques = maximal
        group = cycle_group(cells, anchors, holes)
        orbits = orbit_partition(cliques, model, group)
        census = Counter(encode(inspect(anchors+[frozenset(columns[i]) for i in q])[0]) for q in cliques)
        adjacency = [sum(1 << v for v in neighbors[i]) for i in range(len(columns))]
        records.append({"cycle_half_lengths": list(lengths), "candidate_count": len(columns),
                        "edge_count": sum(len(a) for a in neighbors)//2,
                        "candidate_sha256": sha(columns), "adjacency_sha256": sha(adjacency),
                        "nine_clique_count": len(cliques), "nine_clique_sha256": sha(cliques),
                        "anchor_group_order": len(group), "marked_classes": orbits,
                        "profile_census": [dict(json.loads(key), count=count)
                                           for key, count in sorted(census.items())]})
        carriers.append({"cells": cells, "anchors": [sum(1 << x for x in w) for w in anchors],
                         "columns": columns, "adjacency": adjacency,
                         "nine_cliques": cliques, "group": group})
        performance.append({"nodes": nodes, "seconds": time.monotonic()-started})
    unmarked = defaultdict(list)
    for model_id, record in enumerate(records):
        model = models[model_id]
        cells, anchors, columns, neighbors, holes = model
        for entry in record["marked_classes"]:
            q = tuple(entry["clique"])
            words = anchors+[frozenset(columns[i]) for i in q]
            stats, pairs = inspect(words)
            # Unlike the producer, normalize every mark even in the one-mark cases.
            key = min(canonical_mark(words, u, v, models) for u, v in pairs)
            unmarked[key].append([model_id, list(q)])
    classes = [{"model": key[0], "clique": list(key[1]), "marked_classes": value}
               for key, value in sorted(unmarked.items())]
    result = {"format": "nineteen-star-census-v1", "models": records,
              "unmarked_class_count": len(classes), "unmarked_classes": classes}
    for record in records:
        for item in record["profile_census"]:
            check(item["positive_deficits"] in ([1]*9, [1]*7+[2]), "deficit profile theorem fails")
            check(item["low_low_pairs"] in (1, 2), "two-pair theorem fails")
    if expected is not None:
        check(result == expected, "complete compact classification differs")
    if comparison is not None:
        check(json.loads(encode(carriers)) == comparison, "actual finite carrier differs")
    return result, carriers, performance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    expected = json.loads((HERE/"expected.json").read_text())
    comparison = json.loads(args.compare.read_text()) if args.compare else None
    result, carriers, performance = verify(expected, comparison)
    print(json.dumps({"status": "COMPLETE", "cliques": sum(x["nine_clique_count"] for x in result["models"]),
                      "marked_classes": sum(len(x["marked_classes"]) for x in result["models"]),
                      "unmarked_classes": result["unmarked_class_count"], "all_entrywise": comparison is not None,
                      "manifest_sha256": sha(result), "performance": performance}, sort_keys=True))


if __name__ == "__main__":
    main()
