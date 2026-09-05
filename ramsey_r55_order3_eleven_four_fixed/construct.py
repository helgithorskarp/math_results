#!/usr/bin/env python3
"""Four-triangle signature census and a universal ten-fixed-vertex template."""
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

COVER_SHA256 = '8b6b7b1b17d4a8b62cbeff401acad021764bc55986e65cab557ed9500dad48ed'
PAIRS = tuple(combinations(range(4), 2))
SIGNATURES = (1, 2, 4, 8, 3, 5, 9, 6, 10, 12)
OPPOSITE = ((4, 9), (5, 8), (6, 7))
VARIANTS = (0, 1, 2, 4)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def core_edge(code, a, b):
    i, s = divmod(a, 3)
    j, t = divmod(b, 3)
    return 1 if i == j else code >> (3*PAIRS.index((i, j))+(t-s) % 3) & 1


def graph(code, variant):
    edges = []
    for a, b in combinations(range(22), 2):
        if b < 12:
            red = core_edge(code, a, b)
        elif a < 12:
            red = SIGNATURES[b-12] >> (a//3) & 1
        else:
            red = not (SIGNATURES[a-12] & SIGNATURES[b-12])
            if (a-12, b-12) in OPPOSITE:
                red = red and not (variant >> OPPOSITE.index((a-12, b-12)) & 1)
        if red:
            edges.append((a, b))
    return edges


def edge_bytes(edges):
    return (f'22 {len(edges)}\n'+''.join(f'{a} {b}\n' for a, b in edges)).encode()


def signatures(code):
    red_supports, blue_witness = set(), None
    for vs in combinations(range(12), 4):
        colors = {core_edge(code, a, b) for a, b in combinations(vs, 2)}
        if colors == {1}:
            red_supports.add(sum(1 << i for i in {v//3 for v in vs}))
        elif colors == {0} and blue_witness is None:
            blue_witness = list(vs)
    allowed = [s for s in range(16) if not (s == 0 and blue_witness is not None)
               and all(s & r != r for r in red_supports)]
    return sorted(red_supports), blue_witness, allowed


def run(cover_path, work):
    raw = cover_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == COVER_SHA256, 'inherited cover hash')
    cover = json.loads(raw)
    work.mkdir(parents=True, exist_ok=True)
    graphs = work/'graphs'
    graphs.mkdir(exist_ok=True)
    rows = []
    for case in cover['cases']:
        red, blue, allowed = signatures(case['code'])
        hashes, counts = [], []
        for variant in VARIANTS:
            edges = graph(case['code'], variant)
            data = edge_bytes(edges)
            (graphs/f"core{case['index']:03d}_v{variant}.edges").write_bytes(data)
            hashes.append(hashlib.sha256(data).hexdigest())
            counts.append(len(edges))
        rows.append(dict(index=case['index'], bits=case['bits'], allowed=allowed,
                         red_k4_supports=red, blue_k4=blue,
                         edge_sha256=hashes, red_edges=counts))
    result = dict(format='r55-four-core-fixed-template-v1', cover_sha256=COVER_SHA256,
                  signatures=list(SIGNATURES), variants=list(VARIANTS), cases=rows,
                  cores=len(rows), blue_k4_cores=sum(r['blue_k4'] is not None for r in rows))
    (work/'result.json').write_text(json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n')
    print(json.dumps({k: result[k] for k in ('cores', 'blue_k4_cores')}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, default=Path(__file__).resolve().parent.parent/'ramsey_r55_order3_eleven_four_core/cover.json')
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    require(not a.work.resolve().is_relative_to(Path(__file__).resolve().parent.parent), 'generated graphs outside Git')
    run(a.cover, a.work)
