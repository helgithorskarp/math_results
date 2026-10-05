#!/usr/bin/env python3
"""Independent labeled reverse search and exact replay of the native certificate."""

from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
from check_quinn_reverse_join import shape, perfect, value_legal_gaps, admissible, representative
from check_quinn_reciprocal_join import barrier
from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def record(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def named_perfect(lo, length):
    if not length:
        return ()
    root = lo + length // 2
    return root, named_perfect(lo, length // 2), named_perfect(root + 1, length // 2)


def erase_names(tree):
    return () if not tree else (erase_names(tree[1]), erase_names(tree[2]))


def names(tree):
    return () if not tree else names(tree[1]) + (tree[0],) + names(tree[2])


def named_merges(left, right):
    left_off, right_off = [], []
    cursor = left
    while cursor:
        left_off.append((cursor[0], cursor[1]))
        cursor = cursor[2]
    cursor = right
    while cursor:
        right_off.append((cursor[0], cursor[2]))
        cursor = cursor[1]
    for positions in itertools.combinations(range(len(left_off) + len(right_off)), len(left_off)):
        positions = set(positions)
        letters = ''.join('L' if i in positions else 'R'
                          for i in range(len(left_off) + len(right_off)))
        a, b = len(left_off), len(right_off)
        merged = ()
        for letter in reversed(letters):
            if letter == 'L':
                a -= 1
                root, sibling = left_off[a]
                merged = root, sibling, merged
            else:
                b -= 1
                root, sibling = right_off[b]
                merged = root, merged, sibling
        yield letters, merged


def reverse_fixture():
    # Original position IDs, fixed relative leaf priorities, free internal ranks.
    required = {0: 6, 2: 1, 4: 5, 6: 2, 8: 8, 10: 3, 12: 7, 14: 4}
    start = named_perfect(0, 15)
    pending = deque([start])
    visited = {start}
    branches = geometry_controls = 0
    by_size = {}
    stream = hashlib.sha256()
    while pending:
        tree = pending.popleft()
        require(tree, 'Unexpected complete fixture history')
        present = names(tree)
        require(tuple(sorted(present)) == present, 'Merge changed relative original positions')
        by_size[len(present)] = by_size.get(len(present), 0) + 1
        root, left, right = tree
        known = [required[node] for node in present if node in required]
        if root in required and required[root] != max(known):
            continue
        cut = len(names(left))
        candidates = set()
        for letters, parent in named_merges(left, right):
            require(parent not in candidates, 'Named merge collision')
            candidates.add(parent)
            old_shape = erase_names(parent)
            old_values = representative(old_shape)
            legal = cut in value_legal_gaps(old_values)
            require(legal == admissible(letters), 'Named merge legality disagrees with value geometry')
            geometry_controls += 1
            if not legal:
                continue
            require(names(parent) == tuple(node for node in present if node != root),
                    'Reverse transition lost or reordered an original node')
            branches += 1
            stream.update((json.dumps([tree, letters, parent], separators=(',', ':')) + '\n').encode())
            if parent not in visited:
                visited.add(parent)
                pending.append(parent)
        require(len(visited) <= 50000, 'Independent search cap: incomplete')
    return {'complete_nonexistence': True, 'states_visited': len(visited),
            'merge_branches': branches, 'all_merge_geometry_controls': geometry_controls,
            'states_by_remaining_nodes': {str(k): v for k, v in sorted(by_size.items())},
            'ordered_transition_stream_sha256': stream.hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path,
                        default=Path(__file__).resolve().parent / 'received/quinn_leaf_band_v1')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'Preserve earlier output; choose a new version')
    barrier()
    root = Path(__file__).resolve().parent
    source = args.author_dir
    manifest = json.loads((source / 'MANIFEST.json').read_text())
    before = {name: record(source / name) for name in manifest['files']}
    require(before == manifest['files'], 'Frozen author files changed')
    for name, digest in manifest['dependencies'].items():
        require(record(source / name)['sha256'] == digest, 'Frozen named dependency changed')
    began = time.perf_counter()
    fiber = tuple(p for p in itertools.permutations(range(1, 8))
                  if shape(p) == perfect(3) and not boxed_occurrences(p))
    tokens = (source / 'balanced_fiber_h3.txt').read_text().split()
    received = tuple(tuple(map(int, tokens[2 + 7 * i:2 + 7 * (i + 1)])) for i in range(int(tokens[1])))
    require(tokens[0] == '7' and received == fiber and len(fiber) == 43,
            'Native input not the complete correct perfect avoidance fiber')
    reverse = reverse_fixture()
    expected_reverse = json.loads((source / 'leaf_band_first_fixture_v1.json').read_text())
    require(reverse['states_visited'] == expected_reverse['states_visited'] == 2661 and
            reverse['merge_branches'] == expected_reverse['merge_branches'] == 4784,
            'Independent complete reverse certificate differs')
    expected_native = json.loads((source / 'leaf_band_literal_checker_v1.json').read_text())
    with tempfile.TemporaryDirectory(prefix='theo-leaf-band-review-', dir='/tmp') as temporary:
        temporary = Path(temporary)
        executable = temporary / 'leaf_band'
        flags = ['-std=c++20', '-O2', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wshadow']
        command = ['g++', *flags, str(source / 'leaf_band_literal_checker_v1.cpp'), '-o', str(executable)]
        compiled = subprocess.run(command, text=True, capture_output=True, timeout=60)
        (root / 'quinn-leaf-band-compiler.stdout.txt').write_text(compiled.stdout)
        (root / 'quinn-leaf-band-compiler.stderr.txt').write_text(compiled.stderr)
        require(compiled.returncode == 0, 'Native compile failed')
        barrier()
        output = temporary / 'native.json'
        start_native = time.perf_counter()
        native = subprocess.run([str(executable), str(source / 'balanced_fiber_h3.txt'), str(output)],
                                text=True, capture_output=True, timeout=60)
        seconds_native = time.perf_counter() - start_native
        (root / 'quinn-leaf-band-native.stdout.txt').write_text(native.stdout)
        (root / 'quinn-leaf-band-native.stderr.txt').write_text(native.stderr)
        require(native.returncode == 0, 'Native replay failed/incomplete')
        data = json.loads(output.read_text())
        require(data == expected_native, 'Every native certificate field must match')
        (root / 'quinn-leaf-band-native-replay.json').write_bytes(output.read_bytes())
    # Independently checked498 table must also agree in every old field.
    old = json.loads((root / 'received/quinn_reverse_join_v1/balanced_join_cpp_h3.json').read_text())
    require(all(data[k] == value for k, value in old.items()), 'Old complete pair-table fields changed')
    require(data['candidate_joins_checked'] == 43 ** 2 * math.comb(14, 7) == 6345768 and
            data['sum_valid_joins'] == 790086 and data['valid_target_leaf_band_completions'] == 0,
            'Native cardinality/property certificate differs')
    require(before == {name: record(source / name) for name in before}, 'Frozen author bytes changed during replay')
    report = {'author': 'literature-researcher-3', 'checker': 'literature-researcher-4',
              'decision_message_id': 410, 'full_target_solved': False,
              'manifest_sha256': record(source / 'MANIFEST.json')['sha256'], 'source_files': before,
              'complete_native_input_fiber_independently_reconstructed': True,
              'input_fiber_size': len(fiber), 'independent_reverse_fixture': reverse,
              'every_native_certificate_field_reproduced': True,
              'every_previously_checked498_pair_table_field_unchanged': True,
              'native_target_completions': data['valid_target_leaf_band_completions'],
              'native_candidate_joins': data['candidate_joins_checked'],
              'native_valid_joins': data['sum_valid_joins'], 'native_seconds': seconds_native,
              'native_compiler_flags': flags, 'native_warning_output_empty': not compiled.stderr,
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'reviewer_peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'compiler_and_native_child_peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'intensive_jobs_at_once': 1, 'native_threads': 1,
              'reviewed_at_utc': datetime.now(timezone.utc).isoformat()}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'source_files'}, indent=2))


if __name__ == '__main__':
    main()
