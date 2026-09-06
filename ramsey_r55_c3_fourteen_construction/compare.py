#!/usr/bin/env python3
"""Fixed-winner separation from completed switching-extension families.

This is a comparison of one candidate, not a switching-class census.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

from verify import family, need, read_graph

HERE = Path(__file__).resolve().parent
CATALOG_SHA = '067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb'
CORE_SHA = '096b23f09a0e8eddc928d932f2fb7cc7e9c54e6543b2e77b0b9d8dcade158651'


def graph6(line):
    values = [ord(c)-63 for c in line]
    need(values and 1 <= values[0] <= 62 and all(0 <= v <= 63 for v in values), 'graph6 values')
    n = values[0]
    length = n*(n-1)//2
    need(len(values) == 1+(length+5)//6, 'graph6 length')
    bits = ''.join(f'{v:06b}' for v in values[1:])
    need(set(bits[length:]) <= {'0'}, 'graph6 padding')
    rows = [0]*n
    i = 0
    for v in range(n):
        for u in range(v):
            if bits[i] == '1':
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            i += 1
    return rows


def histogram(rows, vertices):
    mask = sum(1 << v for v in vertices)
    counts = [0]*(len(vertices)-1)
    for u, v in combinations(vertices, 2):
        different = ((rows[u] ^ rows[v]) & mask & ~((1 << u) | (1 << v))).bit_count()
        odd = len(vertices)-2-different if rows[u] & (1 << v) else different
        counts[odd] += 1
    return tuple(counts)


def normalize(rows, anchor):
    labels = [v for v in range(len(rows)) if v != anchor]
    out = [0]*len(labels)
    for i, u in enumerate(labels):
        for j, v in enumerate(labels):
            if i != j and (((rows[u] >> v) ^ (rows[anchor] >> u) ^ (rows[anchor] >> v)) & 1):
                out[i] |= 1 << j
    return out, labels


def run(edges, binary, work):
    work.mkdir(parents=True, exist_ok=False)
    rows = read_graph(edges)
    family(rows)  # Certifies the anchor orbit reduction used below.
    raw = (HERE/'catalog.g6').read_bytes()
    need(sha256(raw).hexdigest() == CATALOG_SHA, 'catalog identity')
    records = raw.decode().splitlines()
    need(len(records) == 328 and len(set(records)) == 328, 'literal catalog count')
    catalog_histograms = set()
    for record in records:
        parent = graph6(record)
        need(len(parent) == 42, 'catalog order')
        h = histogram(parent, list(range(42)))
        catalog_histograms.add(h)
        catalog_histograms.add(h[::-1])
    deletion_histograms = [histogram(rows, [v for v in range(43) if v != deleted]) for deleted in range(43)]
    catalog_matches = [v for v, h in enumerate(deletion_histograms) if h in catalog_histograms]
    residues = {x*x % 41 for x in range(1, 41)}
    paley = [sum(1 << v for v in range(41) if v != u and (u-v) % 41 in residues) for u in range(41)]
    ph = histogram(paley, list(range(41)))
    paley_matches = []
    pair_histograms = []
    for deleted in combinations(range(43), 2):
        h = histogram(rows, [v for v in range(43) if v not in deleted])
        pair_histograms.append(h)
        if h in (ph, ph[::-1]):
            paley_matches.append(deleted)
    raw = (HERE/'core33.edges').read_bytes()
    need(sha256(raw).hexdigest() == CORE_SHA, 'Core186 moving33 identity')
    core = [0]*33
    lines = raw.decode().splitlines()
    need(lines[0] == '33', 'moving core order')
    for line in lines[1:]:
        u, v = map(int, line.split())
        need(0 <= u < v < 33 and not core[u] & (1 << v), 'moving core pair')
        core[u] |= 1 << v
        core[v] |= 1 << u
    pattern, _ = normalize(core, 0)
    complement = [((1 << 32)-1) ^ row ^ (1 << u) for u, row in enumerate(pattern)]
    cases, descriptions = [], []
    for anchor in list(range(0, 42, 3))+[42]:
        host, labels = normalize(rows, anchor)
        for color, source in enumerate((pattern, complement)):
            index = len(cases)
            cases.append(f'{index} 42 32\n'+ ' '.join(map(str, host))+'\n'+' '.join(map(str, source))+'\n')
            descriptions.append((anchor, color, labels, host, source))
    source = work/'cases.txt'
    source.write_text(''.join(cases))
    output = work/'decisions.txt'
    start = time.monotonic()
    subprocess.run([str(binary.resolve()), str(source), str(output), '2000000'], check=True)
    seconds = time.monotonic()-start
    lines = output.read_text().splitlines()
    need(len(lines) == 30, 'complete anchor/orientation count')
    decisions = []
    for i, line in enumerate(lines):
        values = list(map(int, line.split()))
        need(len(values) >= 3 and values[0] == i and values[1] in (0, 1, 2), 'decision format')
        anchor, color, labels, host, source_rows = descriptions[i]
        status, nodes = values[1:3]
        need(nodes >= 1 and nodes <= 2000001, 'node bound')
        if status == 1:
            mapping = values[3:]
            need(len(mapping) == 32 and len(set(mapping)) == 32 and all(0 <= v < 42 for v in mapping), 'embedding map')
            need(all(((source_rows[u] >> v) & 1) == ((host[mapping[u]] >> mapping[v]) & 1)
                     for u, v in combinations(range(32), 2)), 'physical embedding')
        else:
            need(len(values) == 3, 'unexpected embedding values')
        decisions.append({'anchor': anchor, 'color_reverse': color, 'status': status, 'nodes': nodes})
    separated = not catalog_matches and not paley_matches and all(d['status'] == 0 for d in decisions)
    report = {'status': 'SEPARATION_PROVED' if separated else 'SEPARATION_NOT_ESTABLISHED',
        'graph_sha256': sha256(Path(edges).read_bytes()).hexdigest(),
        'catalog_sha256': CATALOG_SHA, 'moving_core_sha256': CORE_SHA,
        'catalog_records': 328, 'catalog_histograms_with_color_reverse': len(catalog_histograms),
        'all_42_vertex_deletions': 43, 'matching_catalog_histograms': catalog_matches,
        'all_41_vertex_deletions': 903, 'matching_Paley_histograms': paley_matches,
        'catalog_deletion_histograms_sha256': sha256(json.dumps(deletion_histograms).encode()).hexdigest(),
        'paley_deletion_histograms_sha256': sha256(json.dumps(pair_histograms).encode()).hexdigest(),
        'moving33_anchor_orientation_cases': decisions,
        'moving33_all_cases_exhausted': all(d['status'] == 0 for d in decisions),
        'total_embedding_nodes': sum(d['nodes'] for d in decisions),
        'case_input_sha256': sha256(source.read_bytes()).hexdigest(),
        'decisions_sha256': sha256(output.read_bytes()).hexdigest()}
    (work/'comparison.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    (work/'runtime.json').write_text(json.dumps({'seconds': seconds, 'binary_sha256': sha256(binary.read_bytes()).hexdigest()}, indent=2)+'\n')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('edges', type=Path)
    p.add_argument('binary', type=Path)
    p.add_argument('work', type=Path)
    a = p.parse_args()
    result = run(a.edges, a.binary, a.work)
    print(result['status'], result['total_embedding_nodes'], 'induced-search nodes')
