#!/usr/bin/env python3
"""Theo's separate definition-level replay of Sage's new simple-marker scope.

No author executable is imported. Reuse Theo's independently reviewed marker
construction, direct rectangles, extrema trees and set-based predecessor
availability; enumerate all proper intervals by sorted value sets.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import time

from check_sage_marker import available, direct_occurrences, image_of, parent_pair, record, require
from rectangle_checker import boxed_occurrences


def intervals(permutation):
    result = []
    for i in range(len(permutation)):
        for j in range(i + 2, len(permutation) + 1):
            if j - i == len(permutation):
                continue
            values = sorted(permutation[i:j])
            if values == list(range(values[0], values[-1] + 1)):
                result.append((i, j))
    return tuple(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, default=Path(__file__).resolve().parent.parent / 'author')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.author_dir
    manifest = json.loads((source / 'MANIFEST.json').read_text())
    before = {row['file']: record(source / row['file']) for row in manifest['files']}
    require(all(before[row['file']] == {key: row[key] for key in ('bytes', 'sha256')}
                for row in manifest['files']), 'Frozen Sage source changed')
    expected = json.loads((source / 'artifacts/simple_marker_controls_v1.json').read_text())
    began = time.perf_counter()
    criterion = []
    for m in range(2, 7):
        stream = hashlib.sha256()
        count = simple_count = 0
        for permutation in itertools.permutations(range(1, m + 1)):
            image = image_of(permutation)
            got = intervals(image)
            required = tuple(([ (0, 2) ] if permutation[0] == m else []) +
                             ([ (len(image) - 2, len(image)) ] if permutation[-1] == 1 else []))
            require(got == required, 'Full interval classification differs')
            stream.update((json.dumps([permutation, got], separators=(',', ':')) + '\n').encode())
            count += 1
            simple_count += not got
        row = {'m': m, 'all_inputs': count, 'simple_images': simple_count,
               'interval_stream_sha256': stream.hexdigest()}
        require(row == expected['criterion_controls'][m - 2], 'Complete criterion stream differs')
        criterion.append(row)

    extensions = []
    for m in range(1, 6):
        stream = hashlib.sha256()
        count = 0
        common_pair = None
        for permutation in itertools.permutations(range(1, m + 1)):
            padded = (1,) + tuple(x + 1 for x in permutation) + (m + 2,)
            image = image_of(padded)
            require(len(image) == 3 * m + 4 and not intervals(image), 'Simple extension domain differs')
            original = boxed_occurrences(permutation)
            padded_set = tuple(tuple(i + 1 for i in occurrence) for occurrence in original)
            lifts = tuple(tuple(3 * (i + 1) for i in occurrence) for occurrence in original)
            require(direct_occurrences(padded) == boxed_occurrences(padded) == padded_set,
                    'Padding occurrence sets differ')
            require(direct_occurrences(image) == boxed_occurrences(image) == lifts,
                    'Complete extension occurrence sets differ')
            require(tuple(x - m - 2 for x in image[::3][1:-1]) == permutation,
                    'Extension does not decode')
            pair = parent_pair(image)
            if common_pair is None:
                common_pair = pair
            require(pair == common_pair, 'Images do not share one pair')
            stream.update((json.dumps([permutation, image, lifts], separators=(',', ':')) + '\n').encode())
            count += 1
        row = {'m': m, 'all_inputs': count, 'image_length': 3 * m + 4,
               'extension_stream_sha256': stream.hexdigest()}
        require(row == expected['extension_controls'][m - 1], 'Full extension stream differs')
        extensions.append(row)

    branches = []
    for m in range(2, 13):
        assigned = set(range(2, 3 * m - 2, 3))
        common_pair = parent_pair(image_of(tuple(range(1, m + 1))))
        require(available(common_pair, assigned) == tuple(range(0, 3 * m - 2, 3)), 'Heap availability differs')
        for t in range(m - 1):
            permutation = list(range(2, m + 1))
            permutation.insert(t, 1)
            image = image_of(tuple(permutation))
            require(not intervals(image) and not boxed_occurrences(image) and not direct_occurrences(image),
                    'Viable simple avoiding witness fails')
            require(image[3 * t] == m and parent_pair(image) == common_pair, 'Witness leaves its prefix or pair')
            require(all(image[3 * i - 1] == i for i in range(1, m)), 'Common prefix not preserved')
        permutation = tuple(range(2, m + 1)) + (1,)
        bad = image_of(permutation)
        require((len(bad) - 2, len(bad)) in intervals(bad), 'Forbidden final interval is missing')
        row = {'m': m, 'available_positions': m, 'simple_viable_witnesses': m - 1}
        require(row == expected['simple_branch_controls'][m - 2], 'Simple branch controls differ')
        branches.append(row)

    # Additional controls exhaust ALL assignments after the fixed low prefix,
    # including words outside the author's band-restricted image.
    full_prefix = []
    for m in range(2, 5):
        n = 3 * m - 2
        common_pair = parent_pair(image_of(tuple(range(1, m + 1))))
        fixed = {3 * i - 1: i for i in range(1, m)}
        free = tuple(i for i in range(n) if i not in fixed)
        viable = set()
        tested = heap_compatible = simple_avoiding = 0
        for tail in itertools.permutations(range(m, n + 1)):
            permutation = [0] * n
            for i, value in fixed.items():
                permutation[i] = value
            for i, value in zip(free, tail):
                permutation[i] = value
            permutation = tuple(permutation)
            tested += 1
            if parent_pair(permutation) != common_pair:
                continue
            heap_compatible += 1
            if intervals(permutation) or boxed_occurrences(permutation):
                continue
            viable.add(permutation.index(m))
            simple_avoiding += 1
        require(viable == set(range(0, n - 3, 3)), 'Outside-band simple viability count differs')
        full_prefix.append({'m': m, 'all_prefix_assignments_tested': tested,
                            'heap_compatible': heap_compatible, 'simple_avoiding': simple_avoiding,
                            'viable_positions': sorted(viable)})
    require(before == {name: record(source / name) for name in before}, 'Author source changed during check')
    result = {'author': 'literature-researcher-1', 'checker': 'literature-researcher-4',
              'decision_message_id': 410, 'full_target_solved': False,
              'proof_sha256': before['MARKER_SIMPLE_REFINEMENT_DRAFT.md']['sha256'],
              'manifest_sha256': record(source / 'MANIFEST.json')['sha256'],
              'source_files': before, 'criterion_controls': criterion, 'extension_controls': extensions,
              'simple_branch_controls': branches, 'all_prefix_controls': full_prefix,
              'author_deterministic_fields_match': True, 'python': platform.python_version(),
              'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'processes': 1, 'native_threads': 1}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('source_files', 'criterion_controls',
                                                            'extension_controls', 'simple_branch_controls')}, indent=2))


if __name__ == '__main__':
    main()
