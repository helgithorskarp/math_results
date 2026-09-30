#!/usr/bin/env python3
"""Direct subset controls and sanitizer replay for new sparse-cover kernel."""
from itertools import combinations
import json
from pathlib import Path
import resource
import subprocess
import time
import helpers as p

HERE = p.WORK


def call(binary, text, cap=None):
    inp = HERE / 'audit_active.input'
    out = HERE / 'audit_active.jsonl'
    inp.write_text(text)
    args = [str(binary), str(inp), str(out)]
    if cap is not None:
        args.append(str(cap))
    result = subprocess.run(args, capture_output=True, text=True, timeout=60)
    return result, out


def main():
    started = time.monotonic()
    binaries = [HERE / 'dlx', HERE / 'dlx_sanitized']
    flags = [['-O2'], ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']]
    for binary, options in zip(binaries, flags):
        subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', '-Wpedantic'] + options
                       + [str(p.BASE / 'dlx.cpp'), '-o', str(binary)], check=True)
    edges = list(combinations(range(4), 2))
    fibers = 0
    for domain in range(64):
        selected = [(i, set(e)) for i, e in enumerate(edges) if domain >> i & 1]
        lines = [f'4 {len(selected)} 2']
        lines.extend(str(i) + ' ' + ' '.join(map(str, sorted(e))) for i, e in selected)
        lines.append('16')
        expected = []
        for excluded in range(16):
            missing = {z for z in range(4) if excluded >> z & 1}
            lines.append(f'{excluded} {len(missing)} ' + ' '.join(map(str, sorted(missing))))
            good = [(i, e) for i, e in selected if not e & missing]
            answers = []
            for choice in range(1 << len(good)):
                rows = [entry for k, entry in enumerate(good) if choice >> k & 1]
                columns = [z for _, e in rows for z in e]
                if len(columns) == len(set(columns)) and set(columns) == set(range(4)) - missing:
                    answers.append(sorted(i for i, _ in rows))
            expected.append(sorted(answers))
        result, out = call(binaries[0], '\n'.join(lines) + '\n')
        if result.returncode or result.stderr:
            raise RuntimeError('subset control failed: ' + result.stderr)
        actual = [json.loads(s)['covers'] for s in out.read_text().splitlines()]
        if actual != expected:
            raise RuntimeError('direct subset control mismatch')
        fibers += 16
    # Maximum matrix capacity, and columns spanning both bitset machine words.
    active = [0, 1, 62, 63, 64, 119]
    missing = [z for z in range(120) if z not in active]
    boundary = '120 1334 6\n' + '\n'.join(str(i) + ' ' + ' '.join(map(str, active))
                                             for i in range(1334)) + '\n1\n0 114 '
    boundary += ' '.join(map(str, missing)) + '\n'
    result, out = call(binaries[1], boundary)
    if result.returncode or result.stderr or json.loads(out.read_text())['covers'] != [[i] for i in range(1334)]:
        raise RuntimeError('sanitized matrix boundary control failed: ' + result.stderr)
    valid = '2 1 2\n1 0 1\n1\n0 0\n'
    malformed = [
        '-1 0 1\n0\n', '121 0 1\n0\n', '2 1335 2\n', '2 -1 2\n',
        '2 0 0\n0\n', '2 0 7\n0\n', '2 1 2\n-1 0 1\n1\n0 0\n',
        '2 1 2\n131072 0 1\n1\n0 0\n', '2 1 2\n1 0 0\n1\n0 0\n',
        '2 1 2\n1 0 2\n1\n0 0\n', '2 1 2\n1 0 -1\n1\n0 0\n',
        '2 2 2\n1 0 1\n1 0 1\n1\n0 0\n', '2 0 2\n11856\n',
        '2 0 2\n1\n1 0\n', '2 0 2\n1\n0 3\n0 1 2\n',
        '2 0 2\n1\n0 2\n0 0\n', '2 0 2\n1\n0 1\n2\n',
        '2 1 2\n1 0\n', valid + 'extra\n']
    for text in malformed:
        result, _ = call(binaries[0], text)
        if result.returncode == 0:
            raise RuntimeError('malformed matrix accepted')
    for cap in (0, 200001):
        result, _ = call(binaries[0], valid, cap)
        if result.returncode == 0 or 'invalid node cap' not in result.stderr:
            raise RuntimeError('invalid guard accepted')
    result, _ = call(binaries[0], valid, 1)
    if result.returncode == 0 or 'INCOMPLETE' not in result.stderr:
        raise RuntimeError('node guard not visibly incomplete')
    p3_fibers = 0
    for shape in range(3):
        inp = HERE / f'p3_s{shape}.input'
        out = HERE / f'p3_dlx_s{shape}.jsonl'
        result = subprocess.run([str(binaries[1]), str(inp), str(out)],
                                capture_output=True, text=True, timeout=60)
        if result.returncode or result.stderr:
            raise RuntimeError('sanitizer p3 replay failure: ' + result.stderr)
        expected = [json.loads(s)['covers'] for s in (HERE / f'p3_s{shape}.jsonl').read_text().splitlines()]
        actual = [json.loads(s)['covers'] for s in out.read_text().splitlines()]
        if expected != actual:
            raise RuntimeError('sanitizer p3 covers differ')
        p3_fibers += len(actual)
    report = dict(agent='six-code-3', role='researcher', status='COMPLETE',
                  direct_subset_fibers=fibers, sanitized_boundary_rows=1334,
                  malformed_inputs_rejected=len(malformed), invalid_caps_rejected=2,
                  node_guard_visibly_incomplete=True, sanitized_p3_fibers=p3_fibers,
                  sanitizer_diagnostics=0, seconds=round(time.monotonic() - started, 6),
                  parent_maxrss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  child_maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
    p.write('dlx_audit.json', report)
    print(json.dumps(report))


if __name__ == '__main__':
    main()
