#!/usr/bin/env python3
"""Small exhaustive enumeration/cover controls and malformed-word checks."""
from pathlib import Path
import argparse
import itertools
import json
import random
import subprocess
import verify


def main(work):
    work.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent
    for name in ('enumerate_esu', 'spanning_trees', 'transversal'):
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic',
                        str(root / (name + '.cpp')), '-o', str(work / name)], check=True)
    rng = random.Random(20260913055)
    qualified = 0
    for case in range(12):
        n = 9 + case % 4
        adj = [set() for _ in range(n)]
        for a in range(n):
            for b in range(a):
                if rng.randrange(5) < 2:
                    adj[a].add(b)
                    adj[b].add(a)
        degrees = [rng.randrange(5) for _ in range(n)]
        inp = work / 'small-graph.txt'
        with inp.open('w') as stream:
            stream.write(f'{n} {n} 1\n')
            for v in range(n):
                stream.write(' '.join(map(str, [v, degrees[v], 0, 0, len(adj[v]),
                                                *sorted(adj[v])])) + '\n')
        esu = subprocess.run([str(work / 'enumerate_esu'), str(inp), str(work / 'esu')],
                             check=True, capture_output=True, text=True)
        subprocess.run([str(work / 'spanning_trees'), str(inp), str(work / 'tree')],
                       check=True, capture_output=True, text=True)
        for size in range(1, 6):
            expected = set()
            for group in itertools.combinations(range(n), size):
                selected = set(group)
                seen = {group[0]}
                while True:
                    updated = seen | {u for v in seen for u in adj[v] & selected}
                    if updated == seen:
                        break
                    seen = updated
                if seen == selected and all(degrees[v] + len(adj[v] & selected) >= 4
                                             for v in group):
                    expected.add(group)
            qualified += len(expected)
            if size < 5:
                got = [tuple(map(int, s.split()))
                       for s in (work / f'esu-{size}.txt').read_text().splitlines()]
                verify.require(len(got) == len(set(got)) and set(got) == expected,
                               'ESU/brute mismatch')
            else:
                row = next(s.split() for s in esu.stdout.splitlines() if s.startswith('5 '))
                verify.require(int(row[2]) == len(expected), 'five-set census mismatch')
            if size in (3, 4):
                got = {tuple(map(int, s.split()))
                       for s in (work / f'tree-{size}.txt').read_text().splitlines()}
                verify.require(got == expected, 'tree/brute mismatch')

    feasible_cases = 0
    for case in range(80):
        width = 2 + case % 9
        h, p = 3 + case % 5, case % 4
        masks = [rng.randrange(1 << width) for _ in range(h + p)]
        weights = [1] * h + [2] * p
        target = (1 << width) - 1
        expected = False
        for selected in range(1 << len(masks)):
            if sum(weights[j] for j in range(len(masks)) if selected >> j & 1) > 5:
                continue
            union = 0
            for j, mask in enumerate(masks):
                if selected >> j & 1:
                    union |= mask
            if union == target:
                expected = True
                break
        inp = work / 'small-cover.txt'
        inp.write_text(f'{width} {h} {p}\n' + ''.join(f'{m} 0\n' for m in masks))
        result = subprocess.run([str(work / 'transversal'), str(inp)],
                                text=True, capture_output=True)
        verify.require(result.returncode in (0, 10), 'C++ cover execution')
        verify.require((result.returncode == 10) == expected, 'C++ cover/brute mismatch')
        actual, _ = verify.weighted_cover(masks, weights, width, 5)
        verify.require(actual == expected, 'Python cover/brute mismatch')
        feasible_cases += expected
    verify.require(0 < feasible_cases < 80, 'both positive and negative cases required')
    edges, base = [(0, 1), (1, 2)], {0}
    verify.validate_words(['012'], edges, base, 3)
    rejected = 0
    for word in ('002', '.12', '052', '01'):
        try:
            verify.validate_words([word], edges, base, 3)
        except ValueError:
            rejected += 1
    verify.require(rejected == 4, 'malformed word accepted')
    result = {'status': 'PASS', 'exhaustive_graphs': 12,
              'qualified_connected_sets': qualified, 'exhaustive_cover_instances': 80,
              'feasible_cover_controls': feasible_cases, 'invalid_words_rejected': rejected}
    (work / 'controls.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    main(args.work.resolve())
