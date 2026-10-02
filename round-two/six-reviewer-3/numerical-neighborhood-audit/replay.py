#!/usr/bin/env python3
"""Serial independent checks and separately labelled unchanged-author replay."""
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OWN_SHA = '47cecc585621e301dcd117266e8b69c432aaa5a68a67b87534424a7e3637a271'
AUTHOR = ROOT / 'round-two/six-sendov-3/effective-neighborhood'


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode()


def main():
    for row in json.loads((HERE / 'INPUTS.json').read_text())['files']:
        body = (ROOT / row['path']).read_bytes()
        if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['sha256']:
            raise ValueError('source bytes changed: ' + row['path'])
    expected = json.loads((HERE / 'EXPECTED.json').read_text())
    if hashlib.sha256(canonical(expected)).hexdigest() != OWN_SHA:
        raise ValueError('frozen independent record changed')
    env = os.environ.copy()
    for key in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS']:
        env[key] = '1'
    runs = []
    def run(label, path, optimize=False, arguments=(), reject=False):
        command = [sys.executable, '-I', '-B'] + (['-O'] if optimize else []) + [str(path)] + list(arguments)
        start = time.monotonic()
        result = subprocess.run(command, env=env, text=True, capture_output=True, timeout=45)
        if (result.returncode == 0) == reject:
            raise ValueError('unexpected exit: ' + label + '\n' + result.stdout + result.stderr)
        row = {'label': label, 'mode': 'optimized' if optimize else 'normal', 'exit': result.returncode, 'elapsed_seconds': round(time.monotonic()-start, 6), 'stdout': result.stdout, 'stderr': result.stderr}
        runs.append(row)
        return result
    with tempfile.TemporaryDirectory(prefix='numerical-neighborhood-') as temporary:
        temporary = Path(temporary)
        malformed = temporary / 'malformed.json'
        malformed.write_text('{broken')
        changed = temporary / 'changed.json'
        bad = json.loads(json.dumps(expected))
        bad['proved_refinements']['coefficient_max_radius'] = 'unproved larger radius'
        changed.write_text(json.dumps(bad))
        original = json.loads((AUTHOR / 'expected.json').read_text())
        original_hash = hashlib.sha256(canonical(original)).hexdigest()
        for optimize in [False, True]:
            result = run('complete independent regenerated record', HERE / 'verify.py', optimize)
            if OWN_SHA not in result.stdout:
                raise ValueError('independent canonical record not printed')
            for name, path in [('missing', temporary / 'missing.json'), ('malformed', malformed), ('changed', changed)]:
                run('independent external fixture rejects ' + name, HERE / 'verify.py', optimize, ['--fixture', str(path)], reject=True)
            run('unchanged original checker, all original predicates and controls', AUTHOR / 'verify.py', optimize)
            regenerated = temporary / ('original-' + str(optimize) + '.json')
            run('separate whole original record regeneration', AUTHOR / 'verify.py', optimize, ['--freeze', '--fixture', str(regenerated)])
            actual = json.loads(regenerated.read_text())
            if canonical(actual) != canonical(original):
                raise ValueError('complete original record differs')
    out = {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer', 'independent_record_sha256': OWN_SHA, 'original_record_sha256': original_hash, 'full_original_fixture_comparison': True, 'input_files_hash_verified': len(json.loads((HERE / 'INPUTS.json').read_text())['files']), 'guard_seconds_per_child': 45, 'native_threads': 1, 'serial_children': True, 'peak_child_rss_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, 'runs': runs, 'trust_boundary': 'Original code is corroboration only and supplies no calculation inputs to verify.py; core frozen before original executable/expected inspection.'}
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'runs'}, sort_keys=True))


if __name__ == '__main__':
    main()
