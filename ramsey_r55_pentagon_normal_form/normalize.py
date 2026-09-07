#!/usr/bin/env python3
"""Find a physical five-clique or transport a candidate into the frame."""
import argparse
import itertools as it
import json
from pathlib import Path


def read_graph(path):
    lines = Path(path).read_text().splitlines()
    if not lines:
        raise ValueError("empty graph")
    n, m = map(int, lines[0].split())
    if n < 27 or n > 63 or m < 0 or len(lines) != m + 1:
        raise ValueError("graph dimensions")
    a = [0] * n
    for line in lines[1:]:
        u, v = map(int, line.split())
        if not 0 <= u < v < n or a[u] >> v & 1:
            raise ValueError("invalid or duplicate edge")
        a[u] |= 1 << v; a[v] |= 1 << u
    return a


def monochromatic(a, s):
    colors = {(a[i] >> j) & 1 for i, j in it.combinations(s, 2)}
    return next(iter(colors)) if len(colors) == 1 else None


def cycle_order(a, vertices):
    s = set(vertices)
    first = min(s)
    second = min(v for v in s if a[first] >> v & 1)
    order = [first, second]
    while len(order) < 5:
        order.append(next(v for v in sorted(s - set(order)) if a[order[-1]] >> v & 1))
    if not a[order[-1]] >> first & 1:
        raise ValueError("cycle ordering failed")
    return order


def normalize(a):
    n = len(a)
    if not 27 <= n <= 63:
        raise ValueError("order outside interface")
    full = (1 << n) - 1
    for u, v in it.combinations(range(n), 2):
        color = (a[u] >> v) & 1
        common = a[u] & a[v] if color else (full ^ (1 << u) ^ a[u]) & (full ^ (1 << v) ^ a[v])
        if common.bit_count() >= 10:
            ten = [w for w in range(n) if common >> w & 1][:10]
            break
    else:
        if n >= 42:
            raise ValueError("Goodman forcing failed")
        return {"kind": "no_frame_found", "n": n, "reason": "no ten-common-neighbor pair"}
    for s in it.combinations(ten, 3):
        if monochromatic(a, s) == color:
            return {"kind": "monochromatic_five", "n": n, "color": color,
                    "vertices": [u, v, *s]}
    for s in it.combinations(ten, 5):
        if monochromatic(a, s) == 1 - color:
            return {"kind": "monochromatic_five", "n": n, "color": 1 - color,
                    "vertices": list(s)}
    for s in it.combinations(ten, 5):
        mask = sum(1 << w for w in s)
        if all((a[w] & mask).bit_count() == 2 for w in s):
            root = list(s)
            break
    else:
        raise ValueError("ten-vertex pentagon lemma failed")
    flip = 1 - color
    changed = a if not flip else [full ^ (1 << i) ^ row for i, row in enumerate(a)]
    order = [u, v] + cycle_order(changed, root)
    for _ in range(4):
        unused = sorted(set(range(n)) - set(order))
        sample = unused[:21]
        for s in it.combinations(sample, 5):
            degrees = [sum((a[i] >> j) & 1 for j in s if i != j) for i in s]
            if len(set(degrees)) != 1:
                continue
            if degrees[0] in (0, 4):
                return {"kind": "monochromatic_five", "n": n,
                        "color": int(degrees[0] == 4), "vertices": list(s)}
            if degrees[0] != 2:
                raise ValueError("regular-five parity failed")
            order += cycle_order(changed, s)
            break
        else:
            if len(sample) >= 21:
                raise ValueError("imported N5<=21 theorem failed")
            return {"kind": "no_frame_found", "n": n,
                    "reason": "no regular five-set below theorem threshold"}
    order += sorted(set(range(n)) - set(order))
    return {"kind": "pentagon_frame", "n": n, "flip": flip, "order": order}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    args = parser.parse_args()
    print(json.dumps(normalize(read_graph(args.graph)), sort_keys=True))
