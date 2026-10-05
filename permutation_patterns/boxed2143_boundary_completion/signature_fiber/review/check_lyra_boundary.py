"""Sage's independent controls of Lyra's frozen interval-composition packet."""

from __future__ import annotations

import argparse
import functools
import hashlib
import importlib.util
import itertools
import json
import platform
import resource
import sys
import time
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def occurrences(word):
    """Sparse distinct labels; no standardization or author checker is used."""
    result = []
    for a, b, c, d in itertools.combinations(range(len(word)), 4):
        if word[b] < word[a] < word[d] < word[c]:
            selected = {a, b, c, d}
            if not any(j not in selected and word[b] < word[j] < word[c]
                       for j in range(a + 1, d)):
                result.append((a, b, c, d))
    return tuple(result)


def boundary_signature(word, ambient):
    rows = []
    for lo in range(1, ambient + 1):
        for hi in range(lo, ambient + 1):
            positions = [i for i, x in enumerate(word) if lo <= x <= hi]
            front = tuple(word[i] for i in positions[:3])
            back = tuple(word[i] for i in positions[-3:])
            rows.append((front, back))
    return tuple(rows)


@functools.lru_cache(maxsize=None)
def scaffolds(size):
    # Factorial enumeration filtered by the defining classical triple test.
    return tuple(p for p in itertools.permutations(range(size))
                 if all(not (p[i] < p[k] < p[j])
                        for i, j, k in itertools.combinations(range(size), 3)))


def interleave(old, markers):
    result = []
    for i, x in enumerate(old):
        result.append(x)
        if i < len(markers):
            result.append(markers[i])
    return tuple(result)


def brute_state(permutation, key):
    first, end, low = key
    old = tuple(2 * x - 1 for x in permutation[first:end])
    result = {}
    for rho in scaffolds(end - first - 1):
        word = interleave(old, tuple(2 * (low + x) for x in rho))
        if not occurrences(word):
            signature = boundary_signature(word, 2 * len(permutation) - 1)
            if signature not in result or word < result[signature]:
                result[signature] = word
    return result


def adjacent_everywhere(permutation, rho, first=0):
    if not rho:
        return True
    gap = rho.index(max(rho))
    old_max = permutation.index(max(permutation))
    if gap + 1 not in (old_max, old_max + 1):
        return False
    cut = gap + 1
    return (adjacent_everywhere(permutation[:cut], rho[:gap]) and
            adjacent_everywhere(permutation[cut:], rho[gap + 1:]))


def file_record(path):
    raw = path.read_bytes()
    return {'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-dir', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.author_dir.resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    before = {row['path']: file_record(root / row['path']) for row in manifest['files']}
    require(all(before[row['path']] == {'size': row['size'], 'sha256': row['sha256']}
                for row in manifest['files']), 'Author packet bytes changed')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root))
    spec = importlib.util.spec_from_file_location('reviewed_lyra_boundary', root / 'boundary_completion.py')
    require(spec is not None and spec.loader is not None, 'Cannot load author algorithm')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    began = time.perf_counter()
    stream = hashlib.sha256()
    inputs = reached = all_bands = 0
    rows = []
    for m in range(1, 6):
        row_inputs = row_reached = row_bands = 0
        for p in itertools.permutations(range(1, m + 1)):
            solver = module.BoundaryCompletion(p)
            root_states = solver.states(0, m, 1)
            require(root_states, 'Finite root nonemptiness failed; no universal assertion intended')
            original_keys = sorted(solver.memo)
            for key in original_keys:
                states = solver.memo[key]
                expected = brute_state(p, key)
                require(states == expected, f'Reached canonical map differs at {p}, {key}')
                stream.update((json.dumps([p, key, sorted(expected.items())], separators=(',', ':')) + '\n').encode())
            for first in range(m):
                for end in range(first + 1, m + 1):
                    for low in range(1, m - (end - first) + 2):
                        key = first, end, low
                        actual = solver.states(*key)
                        expected = brute_state(p, key)
                        require(actual == expected, f'Valid-band canonical map differs at {p}, {key}')
                        row_bands += 1
            for word in root_states.values():
                require(tuple((x + 1) // 2 for x in word[::2]) == p, 'Input recovery differs')
                rho = tuple(x // 2 for x in word[1::2])
                require(tuple(x - 1 for x in rho) in scaffolds(m - 1), 'Root leaves 132 grammar')
            inputs += 1
            row_inputs += 1
            reached += len(original_keys)
            row_reached += len(original_keys)
        all_bands += row_bands
        rows.append({'m': m, 'inputs': row_inputs, 'reached_maps': row_reached, 'all_valid_band_maps': row_bands})
    expected_report = json.loads((root / 'boundary_comparison_m5.json').read_text())
    require(stream.hexdigest() == expected_report['ordered_state_map_sha256'], 'Reached state stream differs')
    require(inputs == expected_report['inputs'] and reached == expected_report['subproblems_compared'],
            'Incomplete reached-map comparison')

    # Generic merge controls include actual empty sides and missing ambient labels.
    merge_solver = module.BoundaryCompletion((1, 2, 3, 4))  # ambient alphabet 1..7
    controls = avoided = rejected = 0
    instances = itertools.chain((p for n in range(1, 5)
                                 for p in itertools.permutations(range(1, 8), n)),
                                itertools.permutations(range(1, 7)))
    for word in instances:
        for cut in range(len(word)):
            left, value, right = word[:cut], word[cut], word[cut + 1:]
            if occurrences(left) or occurrences(right):
                continue
            actual = merge_solver.merge(boundary_signature(left, 7), value, boundary_signature(right, 7))
            is_avoiding = not occurrences(word)
            require((actual is not None) == is_avoiding, f'Merge soundness/completeness differs at {word}, {cut}')
            if is_avoiding:
                require(actual == boundary_signature(word, 7), 'Merged signature differs')
                avoided += 1
            else:
                rejected += 1
            controls += 1

    failure = (1, 2, 4, 5, 3)
    old = tuple(2 * x - 1 for x in failure)
    restricted = []
    for zero_rho in scaffolds(4):
        rho = tuple(x + 1 for x in zero_rho)
        if adjacent_everywhere(failure, rho):
            word = interleave(old, tuple(2 * x for x in rho))
            require(occurrences(word), 'Adjacency restriction has a valid completion')
            restricted.append({'rho': rho, 'word': word, 'complete_occurrences': occurrences(word)})
    require({row['word'] for row in restricted} == {
        (1, 2, 3, 4, 7, 6, 9, 8, 5), (1, 4, 3, 6, 7, 8, 9, 2, 5)}, 'Restricted candidate set differs')
    good = interleave(old, (6, 4, 8, 2))
    require(not occurrences(good) and (2, 1, 3, 0) in scaffolds(4), 'Full size5 witness failed')
    shorter = 0
    for m in range(1, 5):
        for p in itertools.permutations(range(1, m + 1)):
            old = tuple(2 * x - 1 for x in p)
            require(any(adjacent_everywhere(p, tuple(x + 1 for x in rho)) and
                        not occurrences(interleave(old, tuple(2 * (x + 1) for x in rho)))
                        for rho in scaffolds(m - 1)), 'Earlier adjacency failure')
            shorter += 1

    local = []
    for markers in itertools.permutations((6, 8, 10)):
        word = interleave((3, 1, 7, 5), markers)
        occ = occurrences(word)
        require(occ, 'Local band state has a completion')
        local.append({'markers': markers, 'word': word, 'complete_occurrences': occ})
    require(not occurrences((3, 1, 5)) and not occurrences(()), 'Lower/upper condition failed')
    full = (2, 1, 4, 3, 5, 6, 7)
    local_solver = module.BoundaryCompletion(full)
    require(not local_solver.states(0, 4, 3), 'Author local state nonempty')
    require(1 + (7 - 4 - 1) == 3, 'Named root split does not give band3')
    full_word = interleave(tuple(2 * x - 1 for x in full), (2, 4, 6, 8, 10, 12))
    require(not occurrences(full_word), 'Full size7 witness failed')
    require({name: file_record(root / name) for name in before} == before, 'Source changed during review')
    report = {'author': 'literature-researcher-2', 'checker': 'literature-researcher-1',
              'proof_sha256': before['BOUNDARY_INTERFACE_LEMMA.md']['sha256'],
              'author_manifest_sha256': file_record(root / 'MANIFEST.json')['sha256'],
              'source_files': before, 'full_target_solved': False,
              'input_permutations': inputs, 'reached_subproblem_maps': reached,
              'all_valid_band_maps': all_bands, 'ordered_state_map_sha256': stream.hexdigest(), 'rows': rows,
              'generic_merge_controls': controls, 'avoiding_merges': avoided, 'rejected_merges': rejected,
              'adjacent_maximum_exact_candidates': restricted, 'smaller_adjacent_inputs': shorter,
              'local_band_all_six': local, 'valid_full_size5_word': good, 'valid_full_size7_word': full_word,
              'python': platform.python_version(), 'seconds': time.perf_counter() - began,
              'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in (
        'source_files', 'adjacent_maximum_exact_candidates', 'local_band_all_six')}, indent=2))


if __name__ == '__main__':
    main()
