#!/usr/bin/env python3
"""Compile/run the exact enumeration and compare its compact diagnostics."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent


def run(directory):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    executable = directory/'search_two_edges'
    trace = directory/'two_edges.trace'
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
    subprocess.run(['c++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                    str(HERE/'search_two_edges.cpp'), '-o', str(executable)],
                   check=True, env=env, timeout=60)
    result = subprocess.run([str(executable), str(HERE/'core16.edges'), str(trace)],
                            check=True, capture_output=True, text=True,
                            env=env, timeout=60)
    summary = json.loads(result.stdout)
    if summary.get('complete') is not True:
        raise AssertionError('incomplete enumeration')
    summary['trace_sha256'] = sha256(trace.read_bytes()).hexdigest()
    summary['row_sizes'] = {}
    summary['qualifying_matching_pair_records'] = []
    for line in trace.read_text().splitlines():
        tag, *numbers = line.split()
        if tag == 'R':
            size = str(int(numbers[0]).bit_count())
            summary['row_sizes'][size] = summary['row_sizes'].get(size, 0)+1
        elif tag == 'P':
            summary['qualifying_matching_pair_records'].append(list(map(int, numbers)))
    summary['agent'] = 'six-books-2'
    summary['role'] = 'researcher'
    summary['scope'] = 'All cross assignments with the fixed core and exactly two internal red edges; no degree or symmetry assumption.'
    return summary, trace


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', default='scratch/books_two_edges')
    args = parser.parse_args()
    summary, trace = run(args.scratch)
    expected = json.loads((HERE/'two_edges_expected.json').read_text())
    if summary != expected:
        raise AssertionError('compact diagnostics mismatch')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
