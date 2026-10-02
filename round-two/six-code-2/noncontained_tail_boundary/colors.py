"""Bounded deterministic greedy saturation coloring, not an absence search.

Successful colors are positive certificates; inability to color with3
would not disprove a3-coloring or prove any packing-size assertion.
"""
import argparse
from collections import Counter
import hashlib
import heapq
import json
from pathlib import Path
import resource
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    need(not args.work.exists(), 'require fresh deterministic color pilot directory')
    args.work.mkdir(parents=True)
    begin = time.monotonic()
    raw = args.graph.read_bytes()
    data = json.loads(raw)
    rows = [int(x, 16) for x in data['adjacency_hex']]
    n = len(rows)
    colors, saturation = [-1] * n, [0] * n
    degree = [r.bit_count() for r in rows]
    heap = [(0, -degree[i], i, 0) for i in range(n)]
    heapq.heapify(heap)
    states = 0
    while heap:
        _, _, i, old_mask = heapq.heappop(heap)
        states += 1
        if colors[i] >= 0 or saturation[i] != old_mask:
            continue
        color = 0
        while old_mask >> color & 1:
            color += 1
        colors[i] = color
        bits = rows[i]
        while bits:
            bit = bits & -bits
            bits ^= bit
            j = bit.bit_length() - 1
            states += 1
            if colors[j] < 0:
                mask = saturation[j] | (1 << color)
                if mask != saturation[j]:
                    saturation[j] = mask
                    heapq.heappush(heap, (-mask.bit_count(), -degree[j], j, mask))
        if states % 1024 < 600:
            need(states <= 2_000_000 and time.monotonic() - begin < 60,
                 'INCOMPLETE fixed60s/two-million-state greedy color guard')
    need(all(c >= 0 for c in colors), 'incomplete positive coloring')
    for i, row in enumerate(rows):
        while row:
            bit = row & -row
            row ^= bit
            j = bit.bit_length() - 1
            need(colors[i] != colors[j], 'same-color graph edge')
    need(time.monotonic() - begin < 60 and states <= 2_000_000, 'INCOMPLETE final color guard')
    packet = {'agent': 'six-code-2', 'role': 'researcher',
        'status': 'POSITIVE_PROPER_FIXED_NONCONTAINED_Q_GRAPH_COLORING_SINGLE_PRODUCER',
        'colors': colors, 'color_count': max(colors) + 1, 'hole_words': data['hole_words'],
        'core_carrier_sha256': data['core_carrier_sha256'], 'graph_sha256': hashlib.sha256(raw).hexdigest(),
        'vertices': n, 'scope': 'Positive field on this fixed physical graph; no all-triple coverage or unsuccessful-color absence inference.'}
    b = encoded(packet)
    (args.work / 'COLORS.json').write_bytes(b)
    result = {'agent': 'six-code-2', 'role': 'researcher', 'status': packet['status'],
        'vertices': n, 'color_count': packet['color_count'], 'color_class_sizes': sorted(Counter(colors).items()),
        'states': states, 'certificate_bytes': len(b), 'certificate_sha256': hashlib.sha256(b).hexdigest(),
        'seconds': time.monotonic() - begin, 'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'initial_whole_guard_seconds': 60, 'initial_state_guard': 2_000_000,
        'independent_color_audit': 'pending; supplied graph properness checked by producer'}
    (args.work / 'SUMMARY.json').write_bytes(encoded(result))
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
