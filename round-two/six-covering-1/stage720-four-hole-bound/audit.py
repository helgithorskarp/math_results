"""Parse and compare every entry of the independent literal C++ replay."""
from argparse import ArgumentParser
import hashlib
import json
import os
from pathlib import Path
import subprocess

from check import HERE, GROUPS, need, validate_shape


def run(command, **kwargs):
    p = subprocess.run(command, text=True, capture_output=True, timeout=20, **kwargs)
    need(p.returncode == 0, 'child failed: ' + p.stderr[:1500])
    need(not p.stderr.strip(), 'child warnings/diagnostics: ' + p.stderr[:1500])
    return p.stdout


def binary(build, sanitized=False):
    flags = ['-std=c++17', '-Wall', '-Wextra', '-Wpedantic']
    flags += (['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer'] if sanitized else ['-O2'])
    key = hashlib.sha256((HERE / 'audit.cpp').read_bytes() + str(flags).encode()).hexdigest()[:16]
    build.mkdir(parents=True, exist_ok=True)
    destination = build / ('audit-' + key)
    if not destination.exists():
        run(['g++', *flags, str(HERE / 'audit.cpp'), '-o', str(destination)])
    return str(destination)


def main():
    ap = ArgumentParser()
    ap.add_argument('--build-dir', type=Path, required=True)
    ap.add_argument('--certificate', type=Path, default=HERE / 'certificate.json')
    ap.add_argument('--output', type=Path)
    ap.add_argument('--sanitized-controls', action='store_true')
    a = ap.parse_args()
    c = json.loads(a.certificate.read_text())
    validate_shape(c)
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[key] = '1'
    b = binary(a.build_dir, a.sanitized_controls)
    if a.sanitized_controls:
        output = run([b, 'controls'], env=env)
        need(output == 'CONTROLS 1713600 518400\n', 'sanitized literal control counters')
        result = {'sanitized_literal_phase_point_controls': 1713600,
                  'sanitized_pair_point_controls': 518400}
    else:
        lines = iter(run([b], env=env).splitlines())
        need(next(lines) == 'SPLIT 370 160', 'literal physical split')
        raw, entries = [], []
        for group, table in zip(GROUPS, c['gain_tables']):
            fields = next(lines).split()
            need(fields[0] == 'GROUP' and int(fields[1]) == len(group) and
                 list(map(int, fields[2:2 + len(group)])) == list(group), 'literal ORIGINAL inventory')
            visits, size = map(int, fields[2 + len(group):])
            gains = [list(map(int, next(lines).split())) for _ in range(size)]
            need(visits == table['raw_phase_tuples'] and gains == table['gain_pairs'],
                 'literal full ORIGINAL phase-gain table differs')
            raw.append(visits); entries.append(size)
        header = next(lines).split()
        need(header[0] == 'DP', 'literal DP marker')
        dp = [list(map(int, next(lines).split())) for _ in range(int(header[1]))]
        need(dp == c['envelope']['final_best_even_by_compulsory_sum'], 'literal full DP table differs')
        need(next(lines) == 'BOUND 61 99', 'literal conditional bound')
        need(next(lines, None) is None, 'unexpected audit output')
        result = {'literal_all_original_phase_tuples_by_group': raw,
                  'full_gain_pair_entries_by_group': entries,
                  'full_dp_entries_compared': len(dp), 'maximum_even_incidence_sum': 61,
                  'minimum_actual_even_holes': 99}
        need(result == json.loads((HERE / 'audit-expected.json').read_text()), 'frozen literal audit counters')
    if a.output:
        a.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
