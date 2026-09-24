"""Generate the finite C5 certificate. Python 3.10+, standard library only."""
from itertools import product
from pathlib import Path
import json

# Protected vertices have masks 1,...,7; free vertices have labels 7 and 8.
# This explicit list is intentionally not shared with the verifier.
EDGES = ((0, 1), (0, 3), (0, 5), (1, 3), (1, 4), (2, 3))
HOST = EDGES + tuple((v, f) for v in range(7) for f in (7, 8)) + ((7, 8),)


def adjacency(edges):
    out = [set() for _ in range(9)]
    for a, b in edges:
        out[a].add(b)
        out[b].add(a)
    return out


def five_cycle_map(neighbors):
    colors = [-1] * 9

    def search():
        left = [i for i in range(9) if colors[i] < 0]
        if not left:
            return True
        v = max(left, key=lambda i: (sum(colors[j] >= 0 for j in neighbors[i]),
                                    len(neighbors[i]), -i))
        choices = set(range(5)) if any(c >= 0 for c in colors) else {0}
        for j in neighbors[v]:
            if colors[j] >= 0:
                choices.intersection_update({(colors[j] - 1) % 5,
                                             (colors[j] + 1) % 5})
        for c in sorted(choices):
            colors[v] = c
            if search():
                return True
        colors[v] = -1
        return False

    if not search():
        raise RuntimeError("A maximal template has no C5 map")
    return colors


def generate():
    records = []
    for h in range(64):
        base = [e for i, e in enumerate(EDGES) if (h >> i) & 1]
        for roles in product(range(3), repeat=7):
            edges = base + [(v, 6 + r) for v, r in enumerate(roles) if r]
            edges.append((7, 8))
            neighbors = adjacency(edges)
            if any(neighbors[a] & neighbors[b] for a, b in edges):
                continue
            if any(b not in neighbors[a] and not (neighbors[a] & neighbors[b])
                   for a, b in HOST):
                continue
            u = sum(1 << v for v, r in enumerate(roles) if r == 1)
            w = sum(1 << v for v, r in enumerate(roles) if r == 2)
            records.append([h, u, w, five_cycle_map(neighbors)])
    records.sort(key=lambda r: tuple(r[:3]))
    return records


if __name__ == "__main__":
    records = generate()
    destination = Path(__file__).with_name("templates.json")
    destination.write_text(json.dumps(records, separators=(",", ":")) + "\n")
    print(json.dumps({"templates": len(records), "file": destination.name}))
