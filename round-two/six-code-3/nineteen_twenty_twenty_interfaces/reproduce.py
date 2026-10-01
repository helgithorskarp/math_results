"""Sequential cold reproduction of the sharp restricted 67-word maximum.

Only a complete run proves the finite obligations. A timeout, guard or
nonzero child exit leaves an incomplete run. --reuse-primary and
--resume-replay reuse explicitly identified local execution evidence;
the default regenerates and checks all mathematical domains.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
RELEASE = ['-std=c++17', '-O2', '-Wall', '-Wextra', '-Wpedantic',
           '-Wconversion', '-Wshadow']
SANITIZED = ['-std=c++17', '-O1', '-g', '-fno-omit-frame-pointer',
             '-fsanitize=address,undefined', '-Wall', '-Wextra',
             '-Wpedantic', '-Wconversion', '-Wshadow']


def check(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def baseline():
    path = HERE.parent / 'three_nineteen_uncovered_triples' / 'baseline69.txt'
    raw = path.read_bytes()
    checksum = hashlib.sha256(raw).hexdigest()
    check(checksum == 'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d',
          'published baseline input changed')
    lines = raw.decode().split()
    check(len(lines) == 69 and all(len(s) == 18 and set(s) <= {'0', '1'} for s in lines),
          'baseline binary domain')
    words = [frozenset(i for i, bit in enumerate(s) if bit == '1') for s in lines]
    check(len(set(words)) == 69 and all(len(w) == 5 for w in words), 'baseline weights')
    triples = [frozenset(t) for w in words for t in combinations(sorted(w), 3)]
    check(len(triples) == len(set(triples)) == 690, 'baseline packing')
    degrees = [sum(p in w for w in words) for p in range(18)]
    distances = Counter(len(a ^ b) for a, b in combinations(words, 2))
    check(dict(distances) == {6: 1264, 8: 637, 10: 445}, 'baseline distance census')
    check(dict(Counter(degrees)) == {12: 1, 18: 2, 19: 3, 20: 12}, 'baseline degree census')
    targets = []
    for x in range(18):
        if degrees[x] != 19:
            continue
        for y, z in combinations([p for p in range(18) if degrees[p] == 20], 2):
            pairs = [sum({a, b} <= w for w in words) for a, b in ((x, y), (x, z), (y, z))]
            if pairs == [5, 5, 4] and not any({x, y, z} <= w for w in words):
                targets.append([x, y, z])
    check(not targets, 'known baseline contradicts proposed restricted theorem')
    return {'status': 'EXACT_KNOWN_BASELINE_VALIDATION', 'words': 69,
            'sha256': checksum, 'distance_census': dict(sorted(distances.items())),
            'degree_census': dict(sorted(Counter(degrees).items())), 'target_triples': targets}


def run(args):
    begun = time.monotonic()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    build = work / 'build'
    build.mkdir(exist_ok=True)
    env = {**os.environ, 'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1',
           'MKL_NUM_THREADS': '1', 'ASAN_OPTIONS': 'detect_leaks=1',
           'UBSAN_OPTIONS': 'halt_on_error=1'}
    stages = []
    # A new attempt cannot leave a prior completion file as its status.
    (work / 'reproduction-complete.json').unlink(missing_ok=True)

    def progress():
        record = {'status': 'REPRODUCTION_IN_PROGRESS', 'agent': 'six-code-3',
                  'role': 'researcher', 'stages': stages,
                  'seconds': time.monotonic() - begun}
        (work / 'reproduction-progress.json').write_bytes(encode(record))

    progress()

    def child(label, command, timeout, output_json=False):
        start = time.monotonic()
        result = subprocess.run([str(s) for s in command], capture_output=True,
                                text=True, env=env, timeout=timeout)
        (work / f'driver-{label}.log').write_text(result.stdout + result.stderr)
        check(result.returncode == 0, 'INCOMPLETE ' + label + '; no exclusion: ' + result.stderr[-1000:])
        row = {'stage': label, 'status': 'COMPLETE', 'seconds': time.monotonic() - start}
        if output_json:
            row['result'] = json.loads(result.stdout.strip().splitlines()[-1])
        stages.append(row)
        progress()
        print(json.dumps(row), flush=True)
        return row

    def compile_engine(name, supplied, flags, suffix):
        if supplied is not None:
            path = supplied.resolve()
            check(path.is_file(), 'missing explicitly supplied executable')
            return path
        path = build / (name + suffix)
        child('compile-' + name + suffix,
              ['g++', *flags, HERE / (name + '_server.cpp'), '-o', path], 60)
        return path

    color = compile_engine('color', args.color_executable, RELEASE, '')
    pivot = compile_engine('pivot', args.pivot_executable, RELEASE, '')
    python = sys.executable
    if not args.reuse_primary:
        for case in range(46):
            child('primary-' + str(case), [python, HERE / 'produce.py', '--case', case,
                  '--work', work, '--executable', color], 70, True)
    child('primary-summary', [python, HERE / 'produce.py', '--summary', '--work', work], 60, True)
    check((work / 'summary.json').read_bytes() == (HERE / 'expected.json').read_bytes(),
          'cold primary expected manifest mismatch')
    command = [python, HERE / 'replay.py', '--work', work, '--executable', pivot]
    if args.resume_replay:
        command.append('--resume')
    # This aggregate stage contains separately guarded <=60-second children.
    # No per-query, per-case or per-chunk guard is increased.
    child('independent-census', command, None, True)
    for optimized in (False, True):
        py = [python, '-O'] if optimized else [python]
        label = 'optimized' if optimized else 'normal'
        child('capacity-' + label, [*py, HERE / 'verify_residual.py', '--work', work,
              '--certificate', HERE / 'residual.json'], 60, True)
        child('witness-' + label, [*py, HERE / 'verify_witness.py'], 60, True)
    child('capacity-controls', [python, '-O', HERE / 'capacity_controls.py'], 60, True)
    for name, executable in (('color', color), ('pivot', pivot)):
        child('native-controls-' + name, [python, '-O', HERE / 'controls.py',
              '--executable', executable], 60, True)
    # Three whole cases, each independently guarded at 60 seconds.
    child('python-port', [python, HERE / 'check_python_port.py', '--work', work], 190, True)
    for name in ('color', 'pivot'):
        executable = compile_engine(name, None, SANITIZED, '-sanitized')
        child('sanitized-witness-fiber-' + name,
              [python, HERE / 'sanitize_fiber.py', '--work', work,
               '--executable', executable], 60, True)
    stages.append({'stage': 'known-baseline', 'status': 'COMPLETE', 'result': baseline()})
    result = {'status': 'COMPLETE_ALL_REQUESTED_STAGES', 'agent': 'six-code-3',
              'role': 'researcher', 'seconds': time.monotonic() - begun,
              'peak_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'reuse_primary': args.reuse_primary, 'resume_replay': args.resume_replay,
              'stages': stages, 'summary_sha256': hashlib.sha256((work / 'summary.json').read_bytes()).hexdigest(),
              'certificate_sha256': hashlib.sha256((HERE / 'residual.json').read_bytes()).hexdigest(),
              'witness_sha256': hashlib.sha256((HERE / 'witness67.json').read_bytes()).hexdigest(),
              'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(HERE.iterdir())
                                if p.is_file() and p.suffix in ('.py', '.cpp')},
              'proof_status': 'Author exact restricted result; ordinary bridges unformalized; new peer review pending.'}
    (work / 'reproduction-complete.json').write_bytes(encode(result))
    print(json.dumps({k: v for k, v in result.items() if k != 'stages'}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--reuse-primary', action='store_true')
    parser.add_argument('--resume-replay', action='store_true')
    parser.add_argument('--color-executable', type=Path)
    parser.add_argument('--pivot-executable', type=Path)
    run(parser.parse_args())
