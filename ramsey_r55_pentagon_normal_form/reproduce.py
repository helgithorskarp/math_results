#!/usr/bin/env python3
"""Rebuild and audit the complete CNF and controls in a fresh external directory."""
import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def reproduce(scratch):
    scratch = scratch.resolve()
    if scratch.is_relative_to(HERE.parent):
        raise ValueError('use scratch space outside the repository')
    scratch.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    timings = []

    def run(name, *args, optimized=False, expected=None, output=None):
        before = time.monotonic()
        command = [sys.executable, '-B'] + (['-O'] if optimized else [])
        command += [str(HERE / name)] + [str(a) for a in args]
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        report = json.loads(process.stdout)
        if expected is not None and report != json.loads((HERE / expected).read_text()):
            raise ValueError('expected result differs: ' + name)
        if output:
            (scratch / output).write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
        timings.append({'script': name, 'optimized': optimized,
                        'seconds': round(time.monotonic() - before, 6)})
        return report

    cnf = scratch / 'frame43.cnf'
    run('encode.py', cnf, expected='expected_encode.json', output='encode.json')
    for optimized in (False, True):
        suffix = 'optimized' if optimized else 'normal'
        run('check_cnf.py', cnf, optimized=optimized, expected='expected_cnf.json',
            output='audit_' + suffix + '.json')
        run('controls.py', optimized=optimized, expected='controls_expected.json',
            output='controls_' + suffix + '.json')
        for name in ('control42', 'control43'):
            run('normalize.py', HERE / (name + '.edges'), optimized=optimized,
                expected=name + '_certificate.json', output=name + '_' + suffix + '.json')
            run('verify.py', HERE / (name + '.edges'), scratch / (name + '_' + suffix + '.json'),
                optimized=optimized, expected=name + '_transport.json',
                output=name + '_transport_' + suffix + '.json')
    moved, bits, decoded = (scratch / name for name in ('normalized43.edges', 'seed43.bits', 'decoded43.edges'))
    run('export.py', HERE / 'control43.edges', HERE / 'control43_certificate.json', moved, bits,
        output='export.json')
    run('decode.py', bits, decoded, output='decode.json')
    if moved.read_bytes() != decoded.read_bytes():
        raise ValueError('physical export/decode round trip')
    physical = run('verify_graph.py', decoded, expected='control43_counts.json', output='decoded_counts.json')
    evaluated = run('evaluate.py', cnf, bits, expected='expected_seed_evaluation.json', output='seed_evaluation.json')
    if evaluated['violated_clauses'] != physical['red_five_sets'] + physical['blue_five_sets']:
        raise ValueError('physical/Boolean defect mismatch')
    report = {'status': 'COMPLETE_GLOBAL_FRAME_REPRODUCED', 'python': platform.python_version(),
              'formula_sha256': json.loads((HERE / 'expected_cnf.json').read_text())['sha256'],
              'solver_invoked': False, 'target_found': False,
              'imported_N5_computation_reproduced': False,
              'seed_physical_defects': evaluated['violated_clauses'],
              'seconds': round(time.monotonic() - started, 6), 'timings': timings}
    (scratch / 'reproduction.json').write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('fresh_scratch_directory', type=Path)
    args = parser.parse_args()
    print(json.dumps(reproduce(args.fresh_scratch_directory), sort_keys=True))
