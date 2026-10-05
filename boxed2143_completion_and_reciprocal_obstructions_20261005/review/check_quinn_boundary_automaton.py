#!/usr/bin/env python3
"""Independent contextual-language, quotient-collision and leaf controls."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import sys
import time

sys.dont_write_bytecode = True
from check_quinn_tree_state import naive_shape, legal_from_values, word
from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def record(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def leaf_paths(tree):
    result = []
    stack = [(tree, '')]
    while stack:
        node, path = stack.pop()
        if not node:
            result.append(path)
        else:
            stack.extend(((node[1], path + 'R'), (node[0], path + 'L')))
    return tuple(result)


def accepts(path):
    first_l = path.find('L')
    return first_l == -1 or 'RR' not in path[first_l:]


def abc_by_paths(tree):
    paths = leaf_paths(tree)
    return tuple(sum(accepts(prefix + path) for path in paths) for prefix in ('', 'L', 'LR'))


def abc_by_recurrence(tree):
    values = {(): (1, 1, 1)}
    stack = [(tree, False)]
    while stack:
        node, visited = stack.pop()
        if not node or node in values:
            continue
        if not visited:
            stack.extend(((node, True), (node[1], False), (node[0], False)))
        else:
            a, b, c = values[node[0]]
            d, e, f = values[node[1]]
            values[node] = (b + d, b + f, b)
    return values[tree]


def descending_preorder_representative(tree, n):
    result = {}
    stack = [(tree, 0)]
    rank = n
    while stack:
        node, offset = stack.pop()
        if not node:
            continue
        left_size = len(leaf_paths(node[0])) - 1
        position = offset + left_size
        result[position] = rank
        rank -= 1
        stack.extend(((node[1], position + 1), (node[0], offset)))
    require(rank == 0 and sorted(result) == list(range(n)), 'Representative construction failed')
    return tuple(result[i] for i in range(n))


def profile(p):
    n = len(p)
    children = Counter(abc_by_paths(naive_shape(p[:gap] + (n + 1,) + p[gap:]))
                       for gap in legal_from_values(p))
    return [{'ABC': list(signature), 'multiplicity': multiplicity}
            for signature, multiplicity in sorted(children.items())]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'author/boundary')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.author_dir
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    before = {name: record(root / name) for name in manifest['files']}
    require(before == manifest['files'], 'Frozen author packet changed')
    for name, digest in manifest['dependencies'].items():
        require(record(root / name)['sha256'] == digest, 'Frozen named dependency changed')
    expected = json.loads((root / 'boundary_automaton_probe_v1.json').read_text())['counterexample']
    began = time.perf_counter()
    stream = hashlib.sha256()
    complete_rows = []
    shape_count = path_count = child_count = 0
    for n in range(8):
        trees = {naive_shape(p) for p in itertools.permutations(range(1, n + 1))}
        require(len(trees) == (1, 1, 2, 5, 14, 42, 132, 429)[n], 'Shape enumeration incomplete')
        smaller_profiles = {}
        for tree in sorted(trees, key=word):
            p = descending_preorder_representative(tree, n)
            require(naive_shape(p) == tree and not boxed_occurrences(p), 'Invalid avoiding representative')
            paths = leaf_paths(tree)
            legal = tuple(i for i, path in enumerate(paths) if accepts(path))
            require(legal == legal_from_values(p), 'External language mismatch')
            signature = abc_by_paths(tree)
            require(signature == abc_by_recurrence(tree), 'Contextual recurrence mismatch')
            require(signature[0] == len(legal), 'A is not the legal-gap count')
            for gap in range(n + 1):
                child = p[:gap] + (n + 1,) + p[gap:]
                require((not boxed_occurrences(child)) == (gap in legal), 'Literal child legality mismatch')
                child_count += 1
            if n < 4:
                row = profile(p)
                require(signature not in smaller_profiles or smaller_profiles[signature] == row,
                        'Earlier quotient collision')
                smaller_profiles[signature] = row
            stream.update((json.dumps([p, word(tree), paths, legal, signature],
                                      separators=(',', ':')) + '\n').encode())
            shape_count += 1
            path_count += len(paths)
        complete_rows.append({'n': n, 'complete_shapes': len(trees)})
    first = tuple(expected['first_avoiding_representative'])
    second = tuple(expected['second_avoiding_representative'])
    for key, p in (('first', first), ('second', second)):
        require(not boxed_occurrences(p), 'Collision input is outside domain')
        require(word(naive_shape(p)) == expected[key + '_shape'], 'Collision shape mismatch')
        require(list(abc_by_paths(naive_shape(p))) == expected['ABC'], 'Collision ABC mismatch')
        require(profile(p) == expected[key + '_child_multiset'], 'Complete child multiset mismatch')
        require(list(legal_from_values(p)) == expected[key + '_legal_gaps'], 'Collision gap mismatch')
    require(profile(first) != profile(second), 'Claimed collision absent')
    perfect = ((((), ()), ((), ())), (((), ()), ((), ())))
    all_perfect = leaf_2143 = leaf_2143_boxes = 0
    for p in itertools.permutations(range(1, 8)):
        if naive_shape(p) != perfect:
            continue
        all_perfect += 1
        leaves = p[::2]
        if not (leaves[1] < leaves[0] < leaves[3] < leaves[2]):
            continue
        leaf_2143 += 1
        a, x, b, r, c, y, d = p
        certificate = (1, 2, 3, 4) if x < c else (0, 2, 4, 6)
        actual = boxed_occurrences(p)
        require(certificate in actual, 'Uniform fixed-leaf witness failed')
        leaf_2143_boxes += len(actual)
    require(all_perfect == 80 and leaf_2143 > 0, 'Perfect-tree domain enumeration failed')
    require(all(naive_shape(p) == (((), ()), ((), ())) and not boxed_occurrences(p)
                for p in ((1, 3, 2), (2, 3, 1))), 'Two-leaf witnesses failed')
    require(before == {name: record(root / name) for name in before}, 'Packet changed during replay')
    report = {'author': 'literature-researcher-3', 'checker': 'literature-researcher-4',
              'decision_message_id': 410, 'full_target_solved': False,
              'manifest_sha256': record(root / 'MANIFEST.json')['sha256'],
              'source_files': before, 'no_author_implementation_imported': True,
              'complete_shape_rows': complete_rows, 'complete_shapes': shape_count,
              'external_paths_checked': path_count, 'literal_insertion_children_checked': child_count,
              'ordered_context_stream_sha256': stream.hexdigest(),
              'same_size_ABC_collision': expected,
              'smaller_quotient_lengths_exhausted': list(range(4)),
              'perfect_size7_heap_labelings': all_perfect,
              'perfect_size7_leaf2143_completions': leaf_2143,
              'perfect_size7_leaf2143_boxes': leaf_2143_boxes,
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_files', 'same_size_ABC_collision')}, indent=2))


if __name__ == '__main__':
    main()
