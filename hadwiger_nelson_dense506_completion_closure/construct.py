#!/usr/bin/env python3
"""Construct the complete extension by singleton propagation and forest colouring."""
from collections import Counter, deque
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIOR = ROOT / 'hadwiger_nelson_dense506_two_point_extension'
PINS = {
    'points': '3bcfcab7e411f6adff3426ceb1cfff97718d634fe41a0e7a71982a57995c4c45',
    'neighbors': '7c71b32a5807e4e9baab0c17953c9e2ba688e7e0d290caa9be6e23b752f564af',
    'candidate_edges': '7912eb1140ca9a570128233517073becd52380fe3840f7cc126bc85a7493f27e',
    'available_masks': '3521c2b5b0fa8942608728d88416688ca8b5a1d207aad59d2fd79d41be27bdb6',
}
GEOMETRY_PIN = 'ce68ab6130082828fbd4e709586ae9dd53273c41e0cb4bfe3aad0278d08faddd'
HOST_COLOR_PIN = '010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4'


def digest(x):
    return sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_import(name, path, pin):
    require(sha256(path.read_bytes()).hexdigest() == pin, 'source pin: ' + str(path))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_colors(path, n):
    raw = path.read_bytes()
    require(len(raw) == n + 1 and raw[-1:] == b'\n', 'colour row length')
    require(set(raw[:-1]) <= set(b'0123'), 'colour domain')
    return [x - ord('0') for x in raw[:-1]]


def load(work):
    data = json.loads((work / 'candidates.json').read_text())
    for field, pin in PINS.items():
        require(digest(data[field]) == pin, 'candidate pin: ' + field)
    require(sha256((PRIOR / 'host_colors.txt').read_bytes()).hexdigest() == HOST_COLOR_PIN,
            'host colour pin')
    return data, read_colors(PRIOR / 'host_colors.txt', 506)


def check_colors(colors, masks, edges):
    require(len(colors) == len(masks), 'colour/list length')
    require(all(type(c) is int and c in range(4) and (m >> c) & 1
                for c, m in zip(colors, masks)), 'colour outside list')
    require(all(colors[i] != colors[j] for i, j in edges), 'monochromatic edge')


def extend_lists(masks, edges):
    """A sufficient algorithm: reject contradictions or a cyclic residual."""
    masks = list(masks)
    original = masks[:]
    n = len(masks)
    require(all(type(m) is int and 0 < m < 16 for m in masks), 'invalid list')
    adjacency = [[] for _ in masks]
    seen_edges = set()
    for i, j in edges:
        require(type(i) is int and type(j) is int and 0 <= i < j < n,
                'invalid edge')
        require((i, j) not in seen_edges, 'duplicate edge')
        seen_edges.add((i, j))
        adjacency[i].append(j)
        adjacency[j].append(i)
    for row in adjacency:
        row.sort()
    initial = sum(m.bit_count() == 1 for m in masks)
    queue = deque(i for i, m in enumerate(masks) if m.bit_count() == 1)
    forced = set()
    trace = []
    while queue:
        i = queue.popleft()
        if i in forced:
            continue
        forced.add(i)
        require(masks[i].bit_count() == 1, 'invalid propagation source')
        for j in adjacency[i]:
            if masks[j] & masks[i]:
                before = masks[j]
                masks[j] &= ~masks[i]
                trace.append((i, j, before, masks[j]))
                require(masks[j], 'propagation contradiction')
                if masks[j].bit_count() == 1:
                    queue.append(j)
    residual = {i for i, m in enumerate(masks) if m.bit_count() > 1}
    residual_edges = sorted((i, j) for i, j in edges if i in residual and j in residual)
    colors = [m.bit_length() - 1 if m.bit_count() == 1 else -1 for m in masks]
    visited = set()
    components = []
    for root in sorted(residual):
        if root in visited:
            continue
        visited.add(root)
        queue = deque([(root, -1)])
        component = []
        while queue:
            i, parent = queue.popleft()
            component.append(i)
            colors[i] = next(c for c in range(4) if (masks[i] >> c) & 1
                             and (parent == -1 or c != colors[parent]))
            for j in adjacency[i]:
                if j not in residual or j == parent:
                    continue
                require(j not in visited, 'cyclic residual')
                visited.add(j)
                queue.append((j, i))
        components.append(sorted(component))
    check_colors(colors, original, edges)
    summary = {
        'initial_singletons': initial,
        'propagated_singletons': len(forced) - initial,
        'final_singletons': len(forced),
        'colour_removals': len(trace),
        'propagation_trace_sha256': digest(trace),
        'post_propagation_list_histogram': dict(sorted(Counter(m.bit_count() for m in masks).items())),
        'residual_vertices': len(residual),
        'residual_edges': residual_edges,
        'residual_components': len(components),
        'residual_component_order_histogram': dict(sorted(Counter(map(len, components)).items())),
        'residual_components_sha256': digest(components),
    }
    return colors, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    data, host = load(args.work)
    candidate, _ = extend_lists(data['available_masks'], data['candidate_edges'])
    print(''.join(map(str, host + candidate)))


if __name__ == '__main__':
    main()
