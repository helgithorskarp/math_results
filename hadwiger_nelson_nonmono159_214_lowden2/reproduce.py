#!/usr/bin/env python3
"""Rebuild the exhaustive family and verify positive coloring witnesses.

All bulky generated state stays in the explicitly supplied work directory.
An existing local coloring file can replace the SAT generation step.
"""

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / 'hadwiger_nelson_nonmono159_overlap10'


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def run(argv, output=None):
    print('running:', ' '.join(map(str, argv)), file=sys.stderr, flush=True)
    if output is None:
        subprocess.run(argv, check=True, cwd=HERE)
    else:
        with output.open('x') as f:
            subprocess.run(argv, stdout=f, check=True, cwd=HERE)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, required=True,
                        help='new directory for resumable generated state')
    parser.add_argument('--colorings', type=Path,
                        help='existing plain-text coloring file; skips SAT generation')
    parser.add_argument('--solver-python', default=sys.executable,
                        help='Python with python-sat 1.8.dev24 (generation only)')
    parser.add_argument('--jobs', type=int, default=1)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error('--jobs must be positive')
    start = time.monotonic()
    work = args.work_dir.resolve()
    colors = args.colorings.resolve() if args.colorings else work / 'colorings.txt'
    if args.colorings and not colors.is_file():
        parser.error('--colorings must name an existing file')
    work.mkdir(parents=True, exist_ok=False)
    run(['sha256sum', '-c', 'SHA256SUMS'])
    manifest = json.loads((HERE / 'GENERATED.json').read_text())
    transforms = work / 'transforms.txt'
    run([sys.executable, HERE / 'enumerate_lowden.py', HERE / 'points159.tsv',
         HERE / 'points214.tsv', transforms], work / 'census.txt')
    if (work / 'census.txt').read_bytes() != (HERE / 'CENSUS.txt').read_bytes():
        raise RuntimeError('census mismatch')
    if digest(transforms) != manifest['transforms.txt']['sha256']:
        raise RuntimeError('canonical transform set mismatch')
    if not args.colorings:
        emitter = work / 'emit_graphs'
        run(['g++', '-std=c++20', '-O3', SIBLING / 'emit_graphs.cpp', '-o', emitter])
        graphs = work / 'graphs.txt'
        run([emitter, HERE / 'points159.tsv', HERE / 'points214.tsv', transforms], graphs)
        if digest(graphs) != manifest['graphs.txt']['sha256']:
            raise RuntimeError('strict graph stream mismatch')
        run([args.solver_python, SIBLING / 'check_graph_stream.py', graphs,
             '--jobs', str(args.jobs)], colors)
    # A different valid assignment is acceptable: SAT model determinism is
    # not part of the theorem. Report the original hash match as provenance.
    print('original_coloring_hash_match=' +
          str(digest(colors) == manifest['colorings.txt']['sha256']).lower())
    verifier = work / 'verify_colorings'
    run(['g++', '-std=c++20', '-O3', HERE / 'verify_colorings.cpp', '-o', verifier])
    run([verifier, HERE / 'points159.tsv', HERE / 'points214.tsv', transforms, colors],
        work / 'verify.txt')
    if (work / 'verify.txt').read_bytes() != (HERE / 'expected_verify.txt').read_bytes():
        raise RuntimeError('verification output mismatch')
    print((work / 'verify.txt').read_text(), end='')
    print(f'elapsed_seconds={time.monotonic()-start:.3f}', file=sys.stderr)


if __name__ == '__main__':
    main()
