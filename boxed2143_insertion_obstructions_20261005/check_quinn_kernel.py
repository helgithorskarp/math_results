#!/usr/bin/env python3
"""Theo's independent rectangle-based check of Quinn's exact kernel.

Author output is compared to independently derived canonical rectangles and
naive greater-neighbor scans. No author verifier or expected table is imported.
Finite replay supplements the separate written universal proof review.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import resource
import sys
import time

from rectangle_checker import boxed_occurrences


DEFAULT_AUTHOR = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(author: Path, max_n: int) -> dict:
    if not 0 <= max_n <= 7:
        raise ValueError('Review finite scope is capped at parent n=7')
    start = time.perf_counter()
    manifest_path = author / 'SOURCE_MANIFEST.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    pinned = {}
    for name, record in manifest['files'].items():
        path = author / name
        actual = digest(path)
        if actual != record['sha256'] or path.stat().st_size != record['bytes']:
            raise RuntimeError('Author manifest mismatch: ' + name)
        pinned[name] = actual
    spec = importlib.util.spec_from_file_location('quinn_kernel_under_review', author / 'kernel.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot load the exact author kernel')
    kernel = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = kernel
    spec.loader.exec_module(kernel)
    parents = insertions = avoiding_parents = 0
    evidence_hash = hashlib.sha256()
    for n in range(max_n + 1):
        for p in itertools.permutations(range(1, n + 1)):
            parents += 1
            old = boxed_occurrences(p)
            if kernel.boxed_occurrences(p) != old:
                raise RuntimeError(f'Complete occurrence mismatch: {p}')
            left = [next((i for i in range(j-1, -1, -1) if p[i] > x), None) for j, x in enumerate(p)]
            right = [next((i for i in range(j+1, n) if p[i] > x), None) for j, x in enumerate(p)]
            if kernel.nearest_greater(p) != (left, right):
                raise RuntimeError(f'Greater-neighbor mismatch: {p}')
            no_new_gaps = []
            if not old:
                avoiding_parents += 1
            for gap in range(n + 1):
                insertions += 1
                child = p[:gap] + (n+1,) + p[gap:]
                if kernel.insert_maximum(p, gap) != child:
                    raise RuntimeError('Insertion index mismatch')
                child_occ = boxed_occurrences(child)
                new = tuple(occ for occ in child_occ if gap in occ)
                retained = tuple(occ for occ in child_occ if gap not in occ)
                shifted = tuple(sorted(tuple(i + (i >= gap) for i in occ) for occ in old))
                if retained != shifted:
                    raise RuntimeError(f'Old-occurrence persistence failed: {p}, {gap}')
                author_new = tuple(sorted(kernel.new_maximum_occurrences(p, gap)))
                if author_new != new:
                    raise RuntimeError(f'New occurrence mismatch: {p}, {gap}, {author_new}, {new}')
                if not new:
                    no_new_gaps.append(gap)
                if old and not child_occ:
                    raise RuntimeError('A nonavoiding parent acquired an avoiding child')
                evidence_hash.update((json.dumps([p, gap, child_occ], separators=(',', ':')) + '\n').encode())
            if kernel.legal_maximum_gaps(p) != tuple(no_new_gaps):
                raise RuntimeError(f'Forbidden union mismatch: {p}')
    malformed_controls = 0
    for p in ((1, 1), (0, 1), (1, 3), (True,), (1.0,)):
        try:
            kernel.boxed_occurrences(p)
        except ValueError:
            malformed_controls += 1
        else:
            raise RuntimeError('Malformed author input accepted')
    for gap in (-1, 3, True, 1.0):
        try:
            kernel.new_maximum_occurrences((1, 2), gap)
        except ValueError:
            malformed_controls += 1
        else:
            raise RuntimeError('Malformed author gap accepted')
    # Definition-level length-four witness, independent of the author kernel.
    obstruction = {}
    for p in ((1, 2), (2, 1)):
        child = p + (3,)
        legal = tuple(g for g in range(4) if not boxed_occurrences(child[:g] + (4,) + child[g:]))
        obstruction[''.join(map(str, p))] = {'child': child, 'child_legal_gaps': legal}
    if obstruction['12']['child_legal_gaps'] != (0, 1, 2, 3) or obstruction['21']['child_legal_gaps'] != (0, 1, 3):
        raise RuntimeError('Independent state-obstruction reconstruction failed')
    for name, sha in pinned.items():
        if digest(author/name) != sha:
            raise RuntimeError('Author bytes changed during review: ' + name)
    if manifest_path.read_bytes() != manifest_bytes:
        raise RuntimeError('Author manifest changed during review')
    return {
        'reviewer': 'literature-researcher-4',
        'author': 'literature-researcher-3',
        'decision_message_id': 410,
        'status': 'finite independent replay passed; universal argument reviewed separately',
        'full_growth_target_solved': False,
        'author_directory': str(author.resolve()),
        'author_manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
        'author_file_sha256': pinned,
        'reviewer_rectangle_checker_sha256': digest(Path(__file__).with_name('rectangle_checker.py')),
        'parent_max_n': max_n,
        'parents_compared': parents,
        'avoiding_parents': avoiding_parents,
        'insertion_instances_compared': insertions,
        'child_occurrence_stream_sha256': evidence_hash.hexdigest(),
        'malformed_inputs_rejected': malformed_controls,
        'state_obstruction': obstruction,
        'python': platform.python_version(),
        'seconds': time.perf_counter() - start,
        'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, default=DEFAULT_AUTHOR)
    parser.add_argument('--max-n', type=int, default=7)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run(args.author_dir, args.max_n)
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
