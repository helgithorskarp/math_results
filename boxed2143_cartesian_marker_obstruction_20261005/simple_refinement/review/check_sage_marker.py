#!/usr/bin/env python3
"""Different-researcher controls of Sage's frozen uniform marker obstruction."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time

from rectangle_checker import boxed_occurrences


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def direct_occurrences(p):
    return tuple((a, b, c, d) for a, b, c, d in itertools.combinations(range(len(p)), 4)
                 if p[b] < p[a] < p[d] < p[c] and
                 not any(p[b] < p[j] < p[c] for j in range(a + 1, d) if j not in (b, c)))


def image_of(sigma):
    m = len(sigma)
    free = tuple(m - 1 + x for x in sigma)
    lows = tuple(range(1, m))
    highs = tuple(range(2 * m, 3 * m - 1))
    return tuple(x for triple in zip(free[:-1], highs, lows) for x in triple) + free[-1:]


def parent_pair(p):
    result = []
    for largest in (False, True):
        parents = [-1] * len(p)
        stack = [(0, len(p), -1)]
        while stack:
            lo, hi, parent = stack.pop()
            if lo == hi:
                continue
            root = (max if largest else min)(range(lo, hi), key=p.__getitem__)
            parents[root] = parent
            stack.extend(((lo, root, root), (root + 1, hi, root)))
        result.append(tuple(parents))
    return tuple(result)


def available(pair, assigned):
    incoming = [set() for _ in pair[0]]
    for child, parent in enumerate(pair[0]):
        if parent != -1:
            incoming[child].add(parent)
    for child, parent in enumerate(pair[1]):
        if parent != -1:
            incoming[parent].add(child)
    return tuple(i for i, before in enumerate(incoming) if i not in assigned and before <= assigned)


def extreme_violation(p):
    pair = parent_pair(p)
    chosen = set()
    for rank in range(1, len(p) + 1):
        choices = available(pair, chosen)
        position = p.index(rank)
        require(position in choices, 'Invalid heap assignment')
        if position not in (choices[0], choices[-1]):
            return rank, position, choices
        chosen.add(position)
    return None


def record(path):
    data = path.read_bytes()
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, default=Path(
        '/scratch/research-team-colloquium-sol61-20261005/workspaces/literature-researcher-1/boxed2143_sage_20261005/review_packet_v1'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    root = args.author_dir
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    before = {r['file']: record(root / r['file']) for r in manifest['files']}
    require(all(before[r['file']] == {'sha256': r['sha256'], 'bytes': r['bytes']} for r in manifest['files']),
            'Frozen Sage packet changed')
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location('sage_marker_reviewed', root / 'verify_marker_construction.py')
    require(spec is not None and spec.loader is not None, 'Cannot load marker functions')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    began = time.perf_counter()
    expected = json.loads((root / 'artifacts/marker_controls_m6_branch12.json').read_text())
    base_rows = []
    total = 0
    for m in range(1, 7):
        digest = hashlib.sha256()
        count = 0
        for sigma in itertools.permutations(range(1, m + 1)):
            image = image_of(sigma)
            require(tuple(sorted(image)) == tuple(range(1, 3 * m - 1)), 'Image is not a permutation')
            require(image == author.marker_map(sigma), 'Author map mismatch')
            old = boxed_occurrences(sigma)
            lifts = tuple(tuple(3 * i for i in indices) for indices in old)
            require(direct_occurrences(image) == boxed_occurrences(image) == lifts,
                    'Occurrence bijection mismatch')
            pair = parent_pair(image)
            require(pair == author.formula_pair(m), 'Tree formula mismatch')
            require(tuple(x - m + 1 for x in image[::3]) == sigma, 'Decode mismatch')
            digest.update(json.dumps([sigma, image, lifts, pair], separators=(',', ':')).encode() + b'\n')
            count += 1
        require(count == math.factorial(m), 'Incomplete base enumeration')
        row = {'m': m, 'image_length': 3 * m - 2, 'permutations_checked': count,
               'ordered_entry_sha256': digest.hexdigest()}
        require(row == expected['exhaustive_base_controls'][m - 1], 'Author base stream mismatch')
        base_rows.append(row)
        total += count

    branches = []
    for m in range(2, 13):
        witnesses = []
        assigned = set(range(2, 3 * m - 2, 3))
        for t in range(m):
            sigma_list = list(range(2, m + 1))
            sigma_list.insert(t, 1)
            sigma = tuple(sigma_list)
            image = image_of(sigma)
            pair = parent_pair(image)
            require(available(pair, assigned) == tuple(range(0, 3 * m - 2, 3)), 'Availability mismatch')
            require(pair == author.formula_pair(m), 'Viable witness left common pair')
            require(not direct_occurrences(image) and not boxed_occurrences(image), 'Witness does not avoid')
            require(image[3 * t] == m and all(image[3 * i - 1] == i for i in range(1, m)),
                    'Rank or common prefix mismatch')
            witnesses.append(image)
        row = {'m': m, 'number_of_viable_witnesses': len(witnesses),
               'witness_stream_sha256': hashlib.sha256(json.dumps(witnesses, separators=(',', ':')).encode()).hexdigest()}
        require(all(row[k] == expected['viable_position_controls'][m - 2][k] for k in row),
                'Author witness stream mismatch')
        branches.append(row)

    exhausted = 0
    for n in range(7):
        count = 0
        for p in itertools.permutations(range(1, n + 1)):
            count += 1
            if not boxed_occurrences(p):
                require(extreme_violation(p) is None, 'Earlier extreme-rule counterexample')
        require(count == math.factorial(n), 'Incomplete minimality control')
        exhausted += count
    bad = (4, 1, 6, 3, 7, 2, 5)
    require(not direct_occurrences(bad) and not boxed_occurrences(bad), 'H1 witness contains boxed pattern')
    require(extreme_violation(bad) == (3, 3, (0, 3, 6)), 'H1 witness choices mismatch')
    require({name: record(root / name) for name in before} == before, 'Source changed during replay')
    report = {'author': 'literature-researcher-1', 'checker': 'literature-researcher-4',
              'decision_message_id': 410, 'full_target_solved': False,
              'proof_sha256': before['MARKER_OBSTRUCTION_DRAFT.md']['sha256'],
              'manifest_sha256': record(root / 'MANIFEST.json')['sha256'], 'source_files': before,
              'complete_base_inputs': total, 'base_rows': base_rows, 'branch_rows': branches,
              'smaller_H1_lengths_exhausted': list(range(7)), 'smaller_H1_permutations': exhausted,
              'H1_witness': bad, 'H1_violation_rank_position_choices': (3, 3, (0, 3, 6)),
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_files', 'base_rows', 'branch_rows')}, indent=2))


if __name__ == '__main__':
    main()
