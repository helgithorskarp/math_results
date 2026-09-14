#!/usr/bin/env python3
"""Exact verification of the native six-point insertion / old-point exchange gate."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / 'hadwiger_nelson_native_five_point_repair_closure'


def require(test, message):
    if not test:
        raise ValueError(message)


def parent_module():
    pins = json.loads((HERE / 'SOURCE_PINS.json').read_text())
    for name, expected in pins.items():
        require(hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest() == expected,
                'source pin: ' + name)
    spec = importlib.util.spec_from_file_location('five_point_parent', PARENT / 'verify.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_words(words, edges, base, n):
    require(isinstance(words, list) and 0 < len(words) <= 256, 'word count')
    for word in words:
        require(isinstance(word, str) and len(word) == n and set(word) <= set('0123.'),
                'word domain')
        require(all(word[v] != '.' for v in base), 'omitted base point')
        require(all(word[a] != word[b] or word[a] == '.' for a, b in edges),
                'monochromatic retained edge')


def group_mask(group, masks):
    result = 0
    for v in group:
        result |= masks[v]
    return result


def compile_tools(work, sanitize=False):
    flags = ['-std=c++17', '-Wall', '-Wextra', '-Wpedantic']
    flags += (['-O1', '-g', '-fsanitize=undefined', '-fno-sanitize-recover=all']
              if sanitize else ['-O3'])
    for name in ('tree_six', 'smaller_trees', 'cover_six', 'split_cover', 'connected_six'):
        subprocess.run(['g++', *flags, str(HERE / (name + '.cpp')), '-o', str(work / name)],
                       check=True)


def write_graph(path, n, free, degrees, adj, masks, width):
    fs = set(free)
    with path.open('w') as out:
        out.write(f'{n} {len(free)} {width}\n')
        for v in free:
            neighbours = sorted(adj[v] & fs)
            row = [v, degrees[v], masks[v] & ((1 << 64) - 1), masks[v] >> 64,
                   len(neighbours), *neighbours]
            out.write(' '.join(map(str, row)) + '\n')


def run(work, name, args, allowed=(0,)):
    result = subprocess.run([str(work / name), *map(str, args)], text=True, capture_output=True)
    (work / (name + '.log')).write_text(result.stdout + result.stderr)
    require(result.returncode in allowed, name + ': unexpected exit ' + str(result.returncode))
    return result


def verify(work, certificate=None, compare_esu=False, sanitize=False):
    start = time.monotonic()
    work.mkdir(parents=True, exist_ok=True)
    pv = parent_module()
    points, edges, base = pv.load_host()
    initial = json.loads((PARENT / 'certificate.json').read_text())['partial_words']
    data = json.loads((certificate or HERE / 'certificate.json').read_text())
    require(data.get('format') == 'native-six-point-cover-v1', 'certificate format')
    words = initial + data['additional_partial_words']
    require(len(initial) == 126 and len(words) == len(set(words)) == 166, 'certificate counts')
    check_words(words, edges, base, len(points))
    adj = [set() for _ in points]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    free = sorted(set(range(len(points))) - base)
    degrees = {v: len(adj[v] & base) for v in free}
    high = [(v,) for v in free if degrees[v] >= 4]
    pairs = [(a, b) for a, b in edges if a in degrees and b in degrees
             and min(degrees[a], degrees[b]) >= 3]
    atoms = high + [p for p in pairs if any(degrees[v] == 3 for v in p)]
    require((len(high), len(pairs), len(atoms)) == (585, 2549, 1823), 'component atom counts')
    masks = {v: sum(1 << i for i, word in enumerate(initial) if word[v] == '.') for v in free}
    wide_masks = {v: sum(1 << i for i, word in enumerate(words) if word[v] == '.') for v in free}
    full, wide_full = (1 << len(initial)) - 1, (1 << len(words)) - 1
    compile_tools(work, sanitize)
    inp = work / 'graph-input.txt'
    write_graph(inp, len(points), free, degrees, adj, masks, len(initial))
    six = run(work, 'tree_six', [inp])
    six_rows = [list(map(int, line.split())) for line in six.stdout.splitlines()]
    require(len(six_rows) == 6 and [r[0] for r in six_rows] == list(range(6)), 'six tree shapes')
    require(all(r[3] == 0 for r in six_rows), 'uncovered connected six-point set')
    small = run(work, 'smaller_trees', [inp, work / 'groups'])
    groups = {}
    for k, expected in ((3, 18965), (4, 175654), (5, 1856054)):
        groups[k] = [tuple(map(int, line.split()))
                     for line in (work / f'groups-{k}.txt').open()]
        require(len(groups[k]) == len(set(groups[k])) == expected, 'smaller group count')
    pair_completions = sorted(set(itertools.combinations([v for v, in high], 2)) | set(pairs))
    component_checks = []
    for k, items in ((5, high), (4, pair_completions), (3, groups[3])):
        table = pv.CoverTable(items, masks, len(initial))
        for group in groups[k]:
            require(not table.query(full & ~group_mask(group, masks)),
                    'uncovered component partition: ' + str(k))
        component_checks.append({'largest': k, 'groups': len(groups[k]),
                                 'completion_items': len(items), 'uncovered': 0})
    # A triple and a remainder consisting of singletons / pairs.
    # Branch on an omitted-colouring row which some remainder atom must hit.
    atom_masks = [group_mask(t, masks) for t in atoms]
    hits = [[a for a, m in enumerate(atom_masks) if m >> i & 1] for i in range(len(initial))]
    order = sorted(range(len(initial)), key=lambda i: len(hits[i]))
    ht = pv.CoverTable(high, masks, len(initial))
    pt = pv.CoverTable(pair_completions, masks, len(initial))
    residual = set()
    for triple in groups[3]:
        remaining = full & ~group_mask(triple, masks)
        require(remaining != 0, 'unexpected uncovered triple')
        row = next(i for i in order if remaining >> i & 1)
        for a in hits[row]:
            atom = atoms[a]
            table, items = (pt, pair_completions) if len(atom) == 1 else (ht, high)
            choices = table.query(remaining & ~atom_masks[a])
            while choices:
                bit = choices & -choices
                choices -= bit
                candidate = tuple(sorted(set(triple + atom + items[bit.bit_length() - 1])))
                # Overlapping pieces overapproximate the component partitions.
                # Smaller unions are also checked, rather than assumed impossible.
                require(group_mask(candidate, wide_masks) != wide_full,
                        'uncovered triple and small components')
                residual.add(candidate)
    require(len(residual) == 13 and all(len(t) == 6 for t in residual), 'coupled residual count')
    cases = json.loads((HERE / 'positive_cases.json').read_text())['cases']
    require({tuple(c['selected']) for c in cases} == residual and len(cases) == 13,
            'positive cases match residual sets')
    for case in cases:
        vertices = sorted(base | set(case['selected']))
        colour = dict(zip(vertices, case['word']))
        retained = [(a, b) for a, b in edges if a in colour and b in colour]
        require(len(vertices) == case['vertices'] == len(case['word']) == 509,
                'actual candidate cardinality')
        require(set(case['word']) <= set('0123') and len(retained) == case['edges'],
                'candidate domain / edge count')
        require(all(colour[a] != colour[b] for a, b in retained), 'candidate colouring')
    wide_atom_masks = [group_mask(t, wide_masks) for t in atoms]
    cover_input, split_input = work / 'cover-input.txt', work / 'split-input.txt'
    blocks = (len(words) + 63) // 64
    with cover_input.open('w') as out, split_input.open('w') as split:
        out.write(f'{len(words)} {len(atoms)} 6\n')
        split.write(f'{len(words)} {len(high)} {len(atoms) - len(high)}\n')
        for t, mask in zip(atoms, wide_atom_masks):
            row = [(mask >> (64 * i)) & ((1 << 64) - 1) for i in range(blocks)]
            out.write(' '.join(map(str, [len(t), *row])) + '\n')
            split.write(' '.join(map(str, row)) + '\n')
    cover = run(work, 'cover_six', [cover_input, work / 'cover-output.txt'])
    require((work / 'cover-output.txt').read_text().splitlines()[0] == 'UNSAT',
            'weighted six-point atom transversal')
    split = run(work, 'split_cover', [split_input], allowed=(20,))
    require('UNSAT' in split.stdout, 'independent pair-count split verdict')
    esu_stats = None
    if compare_esu:
        esu = run(work, 'connected_six', [inp, work / 'esu'])
        esu_stats = [list(map(int, row.split())) for row in esu.stdout.splitlines()]
        require(esu_stats[-1] == [6, 127004782, 21289412, 0], 'ESU six count / coverage')
        require((work / 'esu-6.txt').stat().st_size == 0, 'ESU residual output')
    out = {'status': 'EVERY B503 PLUS AT MOST SIX HOST POINTS IS FOUR-COLOURABLE',
           'old_point_exchange_to_508': 'CLOSED', 'record_improved': False,
           'host_vertices': len(points), 'unit_edges': len(edges), 'fixed_vertices': len(base),
           'partial_colourings': len(words), 'six_spanning_tree_rows': six_rows,
           'component_checks': component_checks, 'coupled_positive_cases': len(cases),
           'weighted_cover': cover.stdout.strip(), 'split_cover': split.stdout.strip(),
           'esu_statistics': esu_stats, 'sanitize': sanitize,
           'seconds': time.monotonic() - start}
    (work / 'verification.json').write_text(json.dumps(out, indent=2) + '\n')
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--certificate', type=Path)
    parser.add_argument('--compare-esu', action='store_true')
    parser.add_argument('--sanitize', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.work.resolve(), args.certificate, args.compare_esu, args.sanitize),
                     indent=2))
