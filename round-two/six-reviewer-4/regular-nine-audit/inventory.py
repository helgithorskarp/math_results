"""Independent physical-pair orbit and incidence enumeration; no target imports."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def canonical(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def adjacency(word, cycles):
    n = 3 * cycles
    out = [0] * n
    pairs = list(it.combinations(range(cycles), 2))
    for u, v in it.combinations(range(n), 2):
        i, t = divmod(u, 3)
        j, z = divmod(v, 3)
        bit = i if i == j else cycles + 3 * pairs.index((i, j)) + (z - t) % 3
        if (word >> bit) & 1:
            out[u] |= 1 << v
            out[v] |= 1 << u
    return out


def relabel_word(rows, permutation, offsets, multiplier):
    image = [3 * permutation[i] + (multiplier * t + offsets[i]) % 3
             for i in range(3) for t in range(3)]
    # Decode transformed physical pairs rather than transform mask indices.
    pairs = list(it.combinations(range(3), 2))
    word = 0
    for u, v in it.combinations(range(9), 2):
        if (rows[u] >> v) & 1:
            a, b = sorted((image[u], image[v]))
            i, t = divmod(a, 3)
            j, z = divmod(b, 3)
            bit = i if i == j else 3 + 3 * pairs.index((i, j)) + (z - t) % 3
            word |= 1 << bit
    return word


def local_data(word):
    rows = adjacency(word, 3)
    degrees = [row.bit_count() for row in rows]
    if sorted(degrees[::3]) != [2, 3, 3]:
        return None, "degree"
    margins = [8 - d for d in degrees]
    bounds = {(u, v): (2 if (rows[u] >> v) & 1 else 3)
              - (rows[u] & rows[v]).bit_count()
              for u, v in it.combinations(range(9), 2)}
    if any(b < max(0, margins[u] + margins[v] - 12)
           for (u, v), b in bounds.items()):
        return None, "pair"
    for size in range(3, 10):
        for subset in it.combinations(range(9), size):
            q, r = divmod(sum(margins[u] for u in subset), 12)
            minimum = 12 * q * (q - 1) // 2 + r * q
            if sum(bounds[u, v] for u, v in it.combinations(subset, 2)) < minimum:
                return None, "subset"
    return (rows, margins, bounds), "keep"


def shift(mask):
    return sum(1 << (3 * i + (t + 1) % 3)
               for i in range(3) for t in range(3) if (mask >> (3 * i + t)) & 1)


def generate():
    counters = {key: 0 for key in ("degree", "pair", "subset", "keep")}
    survivors = {}
    for word in range(1 << 12):
        data, reason = local_data(word)
        counters[reason] += 1
        if data is not None:
            survivors[word] = data
    classes = {}
    for word, (rows, _, _) in survivors.items():
        transports = {relabel_word(rows, p, o, a)
                      for p in it.permutations(range(3))
                      for o in it.product(range(3), repeat=3) for a in (1, 2)}
        if not transports <= survivors.keys():
            raise ValueError("local transport left the complete surviving domain")
        rep = min(transports)
        classes.setdefault(rep, []).append(word)
    # Construct from all physical FOUR-subsets. A column's translation orbit
    # has length three: a fixed subset would have size divisible by three.
    columns = [sum(1 << u for u in c) for c in it.combinations(range(9), 4)]
    column_types = sorted({min(m, shift(m), shift(shift(m))) for m in columns})
    if len(column_types) * 3 != len(columns):
        raise ValueError("unexpected shorter column orbit")
    pairs = list(it.combinations(range(9), 2))
    profiles = []
    for first in column_types:
        triple = [first, shift(first), shift(shift(first))]
        row = [sum((m >> u) & 1 for m in triple) for u in range(9)]
        intersections = [sum(((m >> u) & 1) * ((m >> v) & 1) for m in triple)
                         for u, v in pairs]
        profiles.append((triple, row, intersections))
    frames = []
    per_local = []
    for rep in sorted(classes):
        _, margins, bounds = survivors[rep]
        margin_matches = 0
        start = len(frames)
        for chosen in it.combinations_with_replacement(range(len(profiles)), 4):
            selected = [profiles[i] for i in chosen]
            if any(sum(p[1][u] for p in selected) != margins[u] for u in range(9)):
                continue
            margin_matches += 1
            if any(sum(p[2][k] for p in selected) > bounds[pair]
                   for k, pair in enumerate(pairs)):
                continue
            frames.append({"local_word": rep,
                           "column_first_masks": [column_types[i] for i in chosen],
                           "columns": [m for p in selected for m in p[0]]})
        per_local.append({"local_word": rep, "labeled_words": classes[rep],
                          "multisets": 148995, "margin_matches": margin_matches,
                          "frames": len(frames) - start})
    return {"scope": "nine-regular C3 type 3^7 1 ordinary colored books",
            "local_words_tested": 1 << 12, "local_filters": counters,
            "column_foursets": columns, "column_type_representatives": column_types,
            "local_classes": per_local, "frames": frames}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    record = generate()
    raw = canonical(record)
    (args.work / "inventory.json").write_bytes(raw)
    with (args.work / "frames.txt").open("w") as out:
        for frame in record["frames"]:
            out.write(" ".join(map(str, [frame["local_word"]] + frame["columns"])) + "\n")
    print(json.dumps({"inventory_sha256": hashlib.sha256(raw).hexdigest(),
                      "bytes": len(raw), "local_filters": record["local_filters"],
                      "classes": [{k: v for k, v in c.items() if k != "labeled_words"}
                                  for c in record["local_classes"]],
                      "frames": len(record["frames"])}, sort_keys=True))


if __name__ == "__main__":
    main()
