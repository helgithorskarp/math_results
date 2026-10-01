#!/usr/bin/env python3
"""Independent fixture/coverage audit and recursive circuit certificate checker."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import resource
import subprocess
import time

ROOT = Path(__file__).resolve().parent


def scalar_parent(gates, n):
    for a, b in gates:
        if not 0 <= a < b < n:
            raise ValueError('invalid comparator')
    for mask in range(1 << n):
        v = [(mask >> i) & 1 for i in range(n)]
        for a, b in gates:
            if v[a] > v[b]:
                v[a], v[b] = v[b], v[a]
        if any(v[i] > v[i + 1] for i in range(n - 1)):
            raise RuntimeError('parent does not sort')


def normalized_projection(gates, n, survivors, choices):
    deleted = [i for i in range(n) if i not in survivors]
    tags = [('wire', survivors.index(i)) if i in survivors else
            ('high' if choices[deleted.index(i)] else 'low', 0)
            for i in range(n)]
    result = []
    order = {'low': 0, 'wire': 1, 'high': 2}
    for a, b in gates:
        x, y = tags[a], tags[b]
        if x[0] == y[0] == 'wire':
            result.append(tuple(sorted((x[1], y[1]))))
            # Normalize immediately rather than generating an oriented word.
            if x[1] > y[1]:
                tags[a], tags[b] = y, x
        elif order[x[0]] > order[y[0]]:
            tags[a], tags[b] = y, x
    if [j for kind, j in tags if kind == 'wire'] != list(range(len(survivors))):
        raise RuntimeError('nonidentity final wire frame')
    return tuple(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', type=Path, default=ROOT.parents[2] / 'scratch' / 'projection-deletion-barrier')
    parser.add_argument('--full', action='store_true',
                        help='also check all 8192 inputs instead of only the certificate')
    parser.add_argument('--sanitize', action='store_true')
    args = parser.parse_args()
    work = args.work_dir
    work.mkdir(parents=True, exist_ok=True)
    doc = json.loads((ROOT / 'parents.json').read_text())
    certificate = json.loads((ROOT / 'certificate.json').read_text())
    unique = set()
    histograms = {}
    original_inputs = 0
    for parent in doc['parents']:
        n, gates = parent['n'], parent['gates']
        if len(gates) != parent['m']:
            raise RuntimeError('parent size mismatch')
        scalar_parent(gates, n)
        original_inputs += 1 << n
        histogram = collections.Counter()
        # Independently enumerate the surviving set rather than deleted sets.
        for survivors in itertools.combinations(range(n), 13):
            survivors = list(survivors)
            for choices in itertools.product((False, True), repeat=n - 13):
                projected = normalized_projection(gates, n, survivors, choices)
                histogram[str(len(projected))] += 1
                if len(projected) <= 46:
                    unique.add(projected)
        histograms[parent['name']] = dict(histogram)
    if histograms != certificate['projection_counts']:
        raise RuntimeError('projection coverage mismatch')
    seeds = sorted(unique)
    text = str(len(seeds)) + '\n' + ''.join(
        '13 ' + str(len(net)) + '\n' + ''.join(f'{a} {b}\n' for a, b in net)
        for net in seeds)
    if hashlib.sha256(text.encode()).hexdigest() != certificate['seeds_sha256']:
        raise RuntimeError('entry-level projected-seed mismatch')
    path = work / 'independent_seeds.txt'
    path.write_text(text)
    w = certificate['witnesses']
    if not w or len(set(w)) != len(w) or any(type(x) is not int or not 0 <= x < 8192 for x in w):
        raise RuntimeError('malformed witness list')
    witness_file = work / 'witnesses.txt'
    witness_file.write_text(str(len(w)) + '\n' + ''.join(f'{x}\n' for x in w))
    if len(seeds) != certificate['seeds']:
        raise RuntimeError('seed count mismatch')
    expected44 = sum(45 if len(net) == 45 else 46 * 45 // 2 for net in seeds)
    expected45 = sum(46 for net in seeds if len(net) == 46)
    if expected44 != certificate['candidates44'] or expected45 != certificate['candidates45']:
        raise RuntimeError('deletion coverage count mismatch')
    if certificate['sorters44'] != 0 or certificate['sorters45'] != 0:
        raise RuntimeError('certificate is not an exclusion')
    flags = ['-std=c++20', '-O3', '-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wshadow']
    if args.sanitize:
        flags = ['-std=c++20', '-O1', '-g', '-Wall', '-Wextra', '-Wpedantic',
                 '-Wconversion', '-Wshadow', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
    checker = work / ('check_circuit_sanitized' if args.sanitize else 'check_circuit')
    subprocess.run(['g++'] + flags + [str(ROOT / 'check_circuit.cpp'), '-o', str(checker)], check=True)
    started = time.monotonic()
    run = subprocess.run([str(checker), str(path), str(witness_file), '0'],
                         check=True, capture_output=True, text=True)
    print(run.stdout, end='')
    if f'size44={expected44} size45={expected45}' not in run.stdout:
        raise RuntimeError('checker count mismatch')
    if args.full:
        run = subprocess.run([str(checker), str(path), str(witness_file), '1'],
                             check=True, capture_output=True, text=True)
        print(run.stdout, end='')
        if f'minimum44_failures={certificate["minimum_failed_inputs"]}' not in run.stdout:
            raise RuntimeError('full-input minimum mismatch')
    print('PARENTS_SCALAR_CHECKED', original_inputs,
          'PROJECTED_SEEDS_ENTRY_MATCH', len(seeds))
    print('checker_seconds', round(time.monotonic() - started, 3),
          'max_child_rss_kib', resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)


if __name__ == '__main__':
    main()
