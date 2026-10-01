"""Exact anchored nine-clique census; no prior executable is imported."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
MAX_NODES = 2000000
MAX_SECONDS = 20


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def build(lengths):
    missing = set()
    offset = 0
    for size in lengths:
        for i in range(size):
            missing.update([(offset+i, offset+i),
                            (offset+i, offset+(i+1) % size)])
        offset += size
    cells = sorted(set(product(range(5), repeat=2)) - missing)
    index = {cell: i for i, cell in enumerate(cells)}
    anchors = [sum(1 << i for i, (r, c) in enumerate(cells) if r == j)
               | (1 << 15) for j in range(5)]
    anchors += [sum(1 << i for i, (r, c) in enumerate(cells) if c == j)
                | (1 << 16) for j in range(5)]
    # Candidate enumeration is by row selection and column injection.
    columns = []
    for rows in combinations(range(5), 4):
        for cols in permutations(range(5), 4):
            if all((r, c) in index for r, c in zip(rows, cols)):
                columns.append(tuple(sorted(index[r, c] for r, c in zip(rows, cols))))
    columns = sorted(columns)
    require(len(columns) == len(set(columns)), "duplicate candidate")
    masks = [sum(1 << i for i in q) for q in columns]
    adjacency = [sum(1 << j for j, b in enumerate(masks)
                     if i != j and (a & b).bit_count() <= 1)
                 for i, a in enumerate(masks)]
    return cells, anchors, columns, masks, adjacency


def enumerate_cliques(adjacency, target, node_cap=MAX_NODES, seconds=MAX_SECONDS):
    require(type(target) is int and target > 0, "invalid target")
    require(type(node_cap) is int and 0 < node_cap <= MAX_NODES, "invalid node guard")
    require(0 < seconds <= MAX_SECONDS, "invalid time guard")
    started = time.monotonic()
    nodes = 0
    found = []

    def visit(available, chosen):
        nonlocal nodes
        nodes += 1
        if nodes > node_cap or time.monotonic()-started > seconds:
            raise RuntimeError("INCOMPLETE: clique census guard")
        need = target-len(chosen)
        if need == 0:
            found.append(tuple(sorted(chosen)))
            return
        if available.bit_count() < need:
            return
        left = available
        order, bounds = [], []
        color = 0
        while left:
            color += 1
            possible = left
            while possible:
                bit = possible & -possible
                v = bit.bit_length()-1
                order.append(v)
                bounds.append(color)
                left &= ~bit
                possible &= ~bit
                possible &= ~adjacency[v]
        for v, bound in zip(reversed(order), reversed(bounds)):
            if bound < need:
                break
            visit(available & adjacency[v], chosen+(v,))
            available &= ~(1 << v)

    visit((1 << len(adjacency))-1, ())
    require(len(found) == len(set(found)), "duplicate clique")
    return sorted(found), nodes


def statistics(words):
    require(len(words) == len(set(words)) == 19, "nineteen distinct words required")
    require(all(type(w) is int and 0 <= w < 1 << 17 and w.bit_count() == 4
                for w in words), "invalid word")
    require(all((a & b).bit_count() <= 1 for a, b in combinations(words, 2)),
            "repeated pair")
    replication = [sum((b >> i) & 1 for b in words) for i in range(17)]
    require(max(replication) <= 5, "replication exceeds five")
    high = {i for i, r in enumerate(replication) if r < 5}
    leave = [(i, j) for i, j in combinations(range(17), 2)
             if not any((b >> i) & 1 and (b >> j) & 1 for b in words)]
    e = sum(i in high and j in high for i, j in leave)
    m = sum(i not in high and j not in high for i, j in leave)
    require(len(leave) == 22 and e-m == len(high)+5, "leave accounting")
    return {"positive_deficits": sorted(5-r for r in replication if r < 5),
            "low_low_pairs": m, "high_high_pairs": e,
            "homogeneous_pairs": e+m}


def anchor_group(cells):
    index = {cell: i for i, cell in enumerate(cells)}
    output = set()
    five_maps = list(permutations(range(5)))
    for rows in five_maps:
        for cols in five_maps:
            moved = [(rows[r], cols[c]) for r, c in cells]
            if all(cell in index for cell in moved):
                output.add(tuple(index[cell] for cell in moved)+(15, 16))
            moved = [(cols[c], rows[r]) for r, c in cells]
            if all(cell in index for cell in moved):
                output.add(tuple(index[cell] for cell in moved)+(16, 15))
    return sorted(output)


def transform(mask, mapping):
    return sum(1 << mapping[i] for i in range(17) if (mask >> i) & 1)


def marked_orbits(cliques, model, group):
    cells, anchors, columns, masks, adjacency = model
    index = {mask: i for i, mask in enumerate(masks)}
    induced = [tuple(index[transform(mask, mapping)] for mask in masks)
               for mapping in group]
    require(all({transform(w, p) for w in anchors} == set(anchors) for p in group),
            "anchor map does not preserve anchors")
    remaining = set(cliques)
    universe = set(cliques)
    output = []
    while remaining:
        q = min(remaining)
        orbit = {tuple(sorted(mapping[v] for v in q)) for mapping in induced}
        require(orbit <= universe and orbit <= remaining, "invalid orbit partition")
        remaining.difference_update(orbit)
        output.append({"clique": list(q), "orbit_size": len(orbit),
                       "anchor_stabilizer_order": len(group)//len(orbit),
                       **statistics(anchors+[masks[i] for i in q])})
    return output


def normalize_second_mark(words, u, v, models):
    """All actual maps from a new anchor pair to the two normal forms."""
    rows = sorted(b for b in words if (b >> u) & 1)
    cols = sorted(b for b in words if (b >> v) & 1)
    require(len(rows) == len(cols) == 5, "invalid new anchor")
    positions = {}
    for x in range(17):
        if x not in (u, v):
            positions[x] = (next(i for i, b in enumerate(rows) if (b >> x) & 1),
                            next(i for i, b in enumerate(cols) if (b >> x) & 1))
    require(len(set(positions.values())) == 15, "nonbinary anchor matrix")
    five_maps = list(permutations(range(5)))
    possible = []
    for model_id, model in enumerate(models):
        cells, anchors, columns, masks, adjacency = model
        cell_index = {cell: i for i, cell in enumerate(cells)}
        mask_index = {mask: i for i, mask in enumerate(masks)}
        for rowmap in five_maps:
            for colmap in five_maps:
                for swap in (False, True):
                    moved = {x: ((colmap[c], rowmap[r]) if swap else
                                  (rowmap[r], colmap[c])) for x, (r, c) in positions.items()}
                    if set(moved.values()) != set(cells):
                        continue
                    mapping = {x: cell_index[cell] for x, cell in moved.items()}
                    q = tuple(sorted(mask_index[sum(1 << mapping[x] for x in positions
                                                     if (w >> x) & 1)]
                                     for w in words if not ((w >> u) & 1 or (w >> v) & 1)))
                    require(len(q) == 9, "normalized residual count")
                    possible.append((model_id, q))
    require(bool(possible), "normal form missing")
    return min(possible)


def produce():
    models = [build((5,)), build((2, 3))]
    records, carriers, performance = [], [], []
    for lengths, model in zip(((5,), (2, 3)), models):
        started = time.monotonic()
        cells, anchors, columns, masks, adjacency = model
        cliques, nodes = enumerate_cliques(adjacency, 9)
        group = anchor_group(cells)
        orbits = marked_orbits(cliques, model, group)
        census = Counter(canonical(statistics(anchors+[masks[i] for i in q]))
                         for q in cliques)
        records.append({"cycle_half_lengths": list(lengths), "candidate_count": len(columns),
                        "edge_count": sum(a.bit_count() for a in adjacency)//2,
                        "candidate_sha256": digest(columns), "adjacency_sha256": digest(adjacency),
                        "nine_clique_count": len(cliques), "nine_clique_sha256": digest(cliques),
                        "anchor_group_order": len(group), "marked_classes": orbits,
                        "profile_census": [dict(json.loads(key), count=count)
                                           for key, count in sorted(census.items())]})
        carriers.append({"cells": cells, "anchors": anchors, "columns": columns,
                         "adjacency": adjacency, "nine_cliques": cliques, "group": group})
        performance.append({"nodes": nodes, "seconds": time.monotonic()-started})
    unmarked = {}
    for model_id, record in enumerate(records):
        cells, anchors, columns, masks, adjacency = models[model_id]
        for entry in record["marked_classes"]:
            q = tuple(entry["clique"])
            if entry["low_low_pairs"] == 1:
                key = (model_id, q)
            else:
                words = anchors+[masks[i] for i in q]
                replication = [sum((w >> x) & 1 for w in words) for x in range(17)]
                pairs = [(u, v) for u, v in combinations(range(17), 2)
                         if replication[u] == replication[v] == 5
                         and not any((w >> u) & 1 and (w >> v) & 1 for w in words)]
                require(len(pairs) == entry["low_low_pairs"], "eligible marking count")
                key = min(normalize_second_mark(words, u, v, models) for u, v in pairs)
            unmarked.setdefault(key, []).append([model_id, list(q)])
    classes = [{"model": key[0], "clique": list(key[1]), "marked_classes": value}
               for key, value in sorted(unmarked.items())]
    return {"format": "nineteen-star-census-v1", "models": records,
            "unmarked_class_count": len(classes), "unmarked_classes": classes}, carriers, performance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--work", type=Path)
    args = parser.parse_args()
    result, carriers, performance = produce()
    if args.write:
        (HERE/"expected.json").write_bytes(canonical(result))
    else:
        require(canonical(result) == (HERE/"expected.json").read_bytes(), "manifest differs")
    if args.work:
        args.work.mkdir(parents=True, exist_ok=True)
        (args.work/"producer-carriers.json").write_bytes(canonical(carriers))
    print(json.dumps({"status": "COMPLETE", "cliques": sum(x["nine_clique_count"] for x in result["models"]),
                      "marked_classes": sum(len(x["marked_classes"]) for x in result["models"]),
                      "unmarked_classes": result["unmarked_class_count"],
                      "manifest_sha256": digest(result), "performance": performance}, sort_keys=True))


if __name__ == "__main__":
    main()
