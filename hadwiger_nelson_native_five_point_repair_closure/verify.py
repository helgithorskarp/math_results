#!/usr/bin/env python3
"""Solver-free verification of the fixed native 503-plus-five repair closure."""
from pathlib import Path
import argparse
import functools
import hashlib
import importlib.util
import itertools
import json
import subprocess
import time

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def load_host():
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    for name, expected in pins.items():
        require(hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest() == expected,
                'source hash: ' + name)
    parent = HERE.parent / 'hadwiger_nelson_native_contact_repair'
    spec = importlib.util.spec_from_file_location('native_radicals', parent / 'radical_check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    points = module.generate(False)
    edges = module.edges(points)
    require(len(points) == 3919 and len(edges) == 29125, 'host cardinalities')
    require(digest(points) == 'fa6c2aa721db1dc24bf96ea71bb0b944c50646d0f0276f3d5f47fa8b7cb766a3',
            'point order or geometry')
    require(digest(edges) == 'e6e4757bfcb92fc54f2ad57759c16653e75f920073006ef846c9ce2486f1ec3d',
            'complete unit edges')
    original = json.loads((parent / 'certificate.json').read_text())
    base = original['untruncated_fixed_503']
    require(base == sorted(set(base)) and len(base) == 503 and all(0 <= v < 3919 for v in base),
            'base IDs')
    require(sorted(original['record_map'].values()) == base, 'parent record map')
    return points, edges, set(base)


def validate_words(words, edges, base, n):
    require(isinstance(words, list) and 0 < len(words) <= 128, 'word count')
    for word in words:
        require(isinstance(word, str) and len(word) == n and set(word) <= set('0123.'),
                'partial colour domain')
        require(all(word[v] != '.' for v in base), 'a fixed point is omitted')
        require(all(word[a] != word[b] or word[a] == '.' for a, b in edges),
                'monochromatic retained edge')


class CoverTable:
    """Bit j survives precisely when item j covers every requested word."""
    def __init__(self, items, point_masks, width):
        self.full = (1 << len(items)) - 1
        rows = [bytearray((len(items) + 7) // 8) for _ in range(width)]
        for j, item in enumerate(items):
            mask = 0
            for v in item:
                mask |= point_masks[v]
            while mask:
                bit = mask & -mask
                mask -= bit
                rows[bit.bit_length() - 1][j // 8] |= 1 << (j % 8)
        self.columns = [int.from_bytes(row, 'little') for row in rows]
        self.order = sorted(range(width), key=lambda i: self.columns[i].bit_count())
        self.cache = {}

    def query(self, missing):
        if missing in self.cache:
            return self.cache[missing]
        value = self.full
        for i in self.order:
            if missing >> i & 1:
                value &= self.columns[i]
                if not value:
                    break
        self.cache[missing] = value
        return value


def weighted_cover(masks, weights, width, budget):
    """Independent weighted recursion; no split by the number of pairs."""
    hits = {k: [[j for j, mask in enumerate(masks) if weights[j] <= k and mask >> i & 1]
                for i in range(width)] for k in (1, 2)}
    order = {k: sorted(range(width), key=lambda i: len(hits[k][i])) for k in hits}

    @functools.lru_cache(None)
    def solve(remaining, capacity):
        if not remaining:
            return True
        if not capacity:
            return False
        k = min(capacity, 2)
        row = next(i for i in order[k] if remaining >> i & 1)
        for j in hits[k][row]:
            after = remaining & ~masks[j]
            if weights[j] == capacity:
                if not after:
                    return True
            elif solve(after, capacity - weights[j]):
                return True
        return False

    result = solve((1 << width) - 1, budget)
    statistics = solve.cache_info()._asdict()
    solve.cache_clear()
    return result, statistics


def verify(work, certificate, cxx='g++', sanitize=False, python_cover=True):
    started = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    points, edges, base = load_host()
    data = json.loads(certificate.read_text())
    require(data.get('format') == 'native-five-point-repair-cover-v1', 'certificate format')
    words = data['partial_words']
    validate_words(words, edges, base, len(points))
    search_counts = {}
    search_cases = json.loads((HERE / 'search_controls.json').read_text())['cases']
    seen_cases = set()
    for case in search_cases:
        selected = case['selected']
        require(selected == sorted(set(selected)) and 0 < len(selected) <= 6,
                'search selection size')
        require(set(selected) <= set(range(len(points))) - base, 'search point IDs')
        require(tuple(selected) not in seen_cases, 'duplicate search control')
        seen_cases.add(tuple(selected))
        vertices = sorted(base | set(selected))
        word = case['word']
        require(case['vertices'] == len(vertices) and len(word) == len(vertices)
                and set(word) <= set('0123'), 'search colour domain')
        colour = dict(zip(vertices, word))
        retained_edges = [(a, b) for a, b in edges if a in colour and b in colour]
        require(len(retained_edges) == case['edges'], 'search edge count')
        require(all(colour[a] != colour[b] for a, b in retained_edges), 'search colouring')
        key = str(len(vertices))
        search_counts[key] = search_counts.get(key, 0) + 1
    require(search_counts == {'508': 7, '509': 10}, 'positive sample counts')
    adj = [set() for _ in points]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    free = sorted(set(range(len(points))) - base)
    degrees = {v: len(adj[v] & base) for v in free}
    high = [v for v in free if degrees[v] >= 4]
    pairs = sorted((a, b) for a, b in edges if a in degrees and b in degrees
                   and degrees[a] >= 3 and degrees[b] >= 3)
    atoms = [(v,) for v in high] + [p for p in pairs if any(degrees[v] == 3 for v in p)]
    require((len(high), len(pairs), len(atoms)) == (585, 2549, 1823), 'atom counts')
    masks = {v: sum(1 << i for i, word in enumerate(words) if word[v] == '.') for v in free}
    all_words = (1 << len(words)) - 1

    def group_mask(group):
        value = 0
        for v in group:
            value |= masks[v]
        return value

    flags = ['-std=c++17', '-Wall', '-Wextra', '-Wpedantic']
    flags += (['-O1', '-g', '-fsanitize=undefined', '-fno-sanitize-recover=all']
              if sanitize else ['-O3'])
    for name in ('spanning_trees', 'transversal'):
        subprocess.run([cxx, *flags, str(HERE / (name + '.cpp')), '-o', str(work / name)],
                       check=True)
    tree_input = work / 'tree-input.txt'
    with tree_input.open('w') as stream:
        stream.write(f'{len(points)} {len(free)} {len(words)}\n')
        for v in free:
            neighbours = sorted(adj[v] - base)
            row = [v, degrees[v], masks[v] & ((1 << 64) - 1), masks[v] >> 64,
                   len(neighbours), *neighbours]
            stream.write(' '.join(map(str, row)) + '\n')
    result = subprocess.run([str(work / 'spanning_trees'), str(tree_input), str(work / 'tree')],
                            check=True, text=True, capture_output=True)
    (work / 'spanning-trees.log').write_text(result.stdout + result.stderr)
    require('qualified five-point spanning-tree maps 78576 1277542 1571915' in result.stdout,
            'spanning-tree map counts')
    group_counts = {}
    for size, completions in ((4, [(v,) for v in high]),
                              (3, sorted(set(itertools.combinations(high, 2)) | set(pairs)))):
        groups = [tuple(map(int, line.split()))
                  for line in (work / f'tree-{size}.txt').read_text().splitlines()]
        require(len(groups) == len(set(groups)), 'duplicate tree group')
        require(len(groups) == {3: 18965, 4: 175654}[size], 'tree group count')
        table = CoverTable(completions, masks, len(words))
        for group in groups:
            require(not table.query(all_words & ~group_mask(group)),
                    'uncovered large component and completion: ' + str(group))
        group_counts[str(size)] = {'groups': len(groups), 'completions': len(completions),
                                  'uncovered': 0}
    atom_masks = [group_mask(atom) for atom in atoms]
    cover_input = work / 'cover-input.txt'
    with cover_input.open('w') as stream:
        stream.write(f'{len(words)} {len(high)} {len(atoms) - len(high)}\n')
        for mask in atom_masks:
            stream.write(f'{mask & ((1 << 64) - 1)} {mask >> 64}\n')
    result = subprocess.run([str(work / 'transversal'), str(cover_input)],
                            check=True, text=True, capture_output=True)
    require('NO_COVER' in result.stdout, 'missing finite transversal verdict')
    (work / 'transversal.log').write_text(result.stdout + result.stderr)
    python_stats = None
    if python_cover:
        feasible, python_stats = weighted_cover(atom_masks, list(map(len, atoms)), len(words), 5)
        require(not feasible, 'independent weighted cover found a model')
    out = {'status': 'EVERY FIXED-BASE REPAIR WITH AT MOST FIVE HOST POINTS IS FOUR-COLOURABLE',
           'host_vertices': len(points), 'unit_edges': len(edges), 'fixed_vertices': len(base),
           'new_point_budget': 5, 'partial_colourings': len(words),
           'high_singletons': len(high), 'low_involving_pairs': len(atoms) - len(high),
           'large_component_checks': group_counts,
           'five_point_spanning_tree_maps': [78576, 1277542, 1571915],
           'positive_search_controls': search_counts,
           'certificate_sha256': hashlib.sha256(certificate.read_bytes()).hexdigest(),
           'python_cover_checked': python_cover, 'python_cover_statistics': python_stats,
           'sanitized': sanitize, 'seconds': time.monotonic() - started}
    (work / 'verification.json').write_text(json.dumps(out, indent=2) + '\n')
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    parser.add_argument('--cxx', default='g++')
    parser.add_argument('--sanitize', action='store_true')
    parser.add_argument('--skip-python-cover', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.work.resolve(), args.certificate, args.cxx, args.sanitize,
                            not args.skip_python_cover), indent=2))
