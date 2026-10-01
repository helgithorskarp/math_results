#!/usr/bin/env python3
"""Literal subset, malformed-input, guard, fixture and sanitizer controls."""
from itertools import combinations
import json
import os
import resource
import subprocess
import time

from paths import BASE, WORK
from verify import literal_fixture


def call(binary, text, cap=None):
    inp, out = WORK / 'control.input', WORK / 'control.jsonl'
    inp.write_text(text)
    args = [str(binary), str(inp), str(out)] + ([] if cap is None else [str(cap)])
    result = subprocess.run(args, capture_output=True, text=True, timeout=20)
    return result, out


def main():
    started = time.monotonic()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ[name] = '1'
    kernels = [WORK / name for name in ('fullcover', 'dlx')]
    sanitized = []
    for name, source in (('fullcover', 'bitset.cpp'), ('dlx', 'dlx.cpp')):
        binary = WORK / (name + '_sanitized')
        subprocess.run(['g++', '-std=c++17', '-O1', '-g', '-Wall', '-Wextra', '-Wpedantic',
                        '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
                        str(BASE / source), '-o', str(binary)], check=True)
        sanitized.append(binary)
    edges = list(combinations(range(4), 2))
    fibers = 0
    for domain in range(64):
        rows = [(i, set(pair)) for i, pair in enumerate(edges) if domain >> i & 1]
        lines = [f'4 {len(rows)} 2'] + [str(i) + ' ' + ' '.join(map(str, sorted(pair))) for i, pair in rows]
        lines.append('16')
        expected = []
        for missing in range(16):
            excluded = {z for z in range(4) if missing >> z & 1}
            lines.append(f'{missing} {len(excluded)} ' + ' '.join(map(str, sorted(excluded))))
            available = [(i, pair) for i, pair in rows if not pair & excluded]
            answers = []
            for bits in range(1 << len(available)):
                chosen = [q for j, q in enumerate(available) if bits >> j & 1]
                columns = [z for _, pair in chosen for z in pair]
                if len(columns) == len(set(columns)) and set(columns) == set(range(4)) - excluded:
                    answers.append(sorted(i for i, _ in chosen))
            expected.append(sorted(answers))
        for kernel in kernels:
            result, out = call(kernel, '\n'.join(lines) + '\n')
            if result.returncode or result.stderr or [json.loads(line)['covers'] for line in out.read_text().splitlines()] != expected:
                raise RuntimeError('literal subset control differs')
            fibers += 16
    good = '2 1 2\n1 0 1\n1\n0 0\n'
    malformed = ['-1 0 1\n0\n', '121 0 1\n0\n', '2 1335 2\n', '2 -1 2\n',
                 '2 0 0\n0\n', '2 0 7\n0\n', '2 1 2\n-1 0 1\n1\n0 0\n',
                 '2 1 2\n131072 0 1\n1\n0 0\n', '2 1 2\n1 0 0\n1\n0 0\n',
                 '2 1 2\n1 0 2\n1\n0 0\n', '2 1 2\n1 0 -1\n1\n0 0\n',
                 '2 2 2\n1 0 1\n1 0 1\n1\n0 0\n', '2 0 2\n11856\n',
                 '2 0 2\n1\n1 0\n', '2 0 2\n1\n0 3\n0 1 2\n',
                 '2 0 2\n1\n0 2\n0 0\n', '2 0 2\n1\n0 1\n2\n',
                 '2 1 2\n1 0\n', good + 'extra\n']
    for kernel in kernels:
        for bad in malformed:
            result, _ = call(kernel, bad)
            if result.returncode == 0:
                raise RuntimeError('malformed native matrix accepted')
        for cap in (0, 200001):
            result, _ = call(kernel, good, cap)
            if result.returncode == 0 or 'invalid node cap' not in result.stderr:
                raise RuntimeError('invalid cap accepted')
        result, _ = call(kernel, good, 1)
        if result.returncode == 0 or 'INCOMPLETE' not in result.stderr:
            raise RuntimeError('guard not visibly incomplete')
    active = (0, 1, 62, 63, 64, 119)
    forbidden = tuple(z for z in range(120) if z not in active)
    boundary = '120 1334 6\n' + '\n'.join(str(i) + ' ' + ' '.join(map(str, active)) for i in range(1334))
    boundary += '\n1\n0 114 ' + ' '.join(map(str, forbidden)) + '\n'
    for kernel in sanitized:
        result, out = call(kernel, boundary)
        if result.returncode or result.stderr or json.loads(out.read_text())['covers'] != [[i] for i in range(1334)]:
            raise RuntimeError('sanitized capacity boundary failed: ' + result.stderr)
        for stem in ('hub_2_0_fullcover', 'twice_5_0'):
            inp = WORK / (stem + '.input')
            out = WORK / ('sanitized_' + stem + '.jsonl')
            result = subprocess.run([str(kernel), str(inp), str(out)], capture_output=True, text=True, timeout=20)
            reference = WORK / (stem.replace('_fullcover', '') + '_fullcover.jsonl')
            if result.returncode or result.stderr or json.loads(out.read_text())['covers'] != json.loads(reference.read_text())['covers']:
                raise RuntimeError('sanitized real-fiber replay differs: ' + result.stderr)
    expected = json.loads((BASE / 'expected.json').read_text())
    corrupt = 0
    for family in expected['packing_families']:
        for orbit in family['orbits']:
            bad = list(orbit['representative'])
            bad[0] = bad[1]
            try:
                literal_fixture(bad)
            except RuntimeError:
                corrupt += 1
            else:
                raise RuntimeError('corrupted packing fixture accepted')
    report = dict(agent='six-code-3', role='researcher', status='COMPLETE',
                  literal_subset_fibers=fibers, malformed_matrices_rejected=2 * len(malformed),
                  invalid_caps_rejected=4, visible_incomplete_caps=2,
                  sanitized_boundary_rows=1334, sanitized_real_fibers=4,
                  sanitizer_diagnostics=0, corrupted_fixtures_rejected=corrupt,
                  seconds=round(time.monotonic() - started, 6),
                  parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    (WORK / 'controls.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
