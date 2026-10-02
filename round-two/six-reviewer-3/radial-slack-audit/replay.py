#!/usr/bin/env python3
"""Portable source-bound original corroboration and independent whole replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = Path(__file__).resolve().parent


def need(ok, label):
    if not ok:
        raise ValueError(label)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-directory', type=Path)
    parser.add_argument('--write-validation', type=Path)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'INPUTS.json').read_text())
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', BLIS_NUM_THREADS='1')
    with tempfile.TemporaryDirectory(prefix='radial-independent-') as directory:
        root = Path(directory)
        for row in manifest['files']:
            if args.input_directory:
                raw = (args.input_directory / row['label']).read_bytes()
            else:
                url = 'https://raw.githubusercontent.com/helgithorskarp/math_results/' + row['commit'] + '/' + row['path']
                request = urllib.request.Request(url, headers={'User-Agent': 'independent-math-review/1.0'})
                with urllib.request.urlopen(request, timeout=25) as response:
                    need(response.status == 200, 'pinned input HTTP status')
                    raw = response.read(400001)
            need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'whole pinned input ' + row['label'])
            target = root / row['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        new = root / 'round-two/six-reviewer-3/radial-slack-audit'
        new.mkdir(parents=True)
        for path in HERE.iterdir():
            if path.is_file():
                (new / path.name).write_bytes(path.read_bytes())
        original = root / 'round-two/six-sendov-3/radial-slack'
        credited = json.loads((original / 'expected.json').read_text())
        independent = json.loads((new / 'EXPECTED.json').read_text())
        initial = independent['exact_initial_normal_and_dual']
        source = credited['radial_certificate']
        pairs = [('J', 'initial_even_radial'), ('O', 'initial_odd_radial'),
                 ('individual_root_multipliers', 'initial_individual_root_multipliers')]
        need(all(initial[a] == source[b] for a, b in pairs), 'all complete shared exact initial matrices and individual multipliers')
        source_hash = hashlib.sha256(canonical(credited)).hexdigest()
        runs = []
        def child(label, script, flags=(), extra=(), accept=True):
            begin = time.monotonic()
            p = subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *extra], env=env, capture_output=True, text=True, timeout=45)
            need((p.returncode == 0) == accept, 'child status ' + label)
            if accept:
                need(not p.stderr, 'accepted child has no stderr ' + label)
            item = {'label': label, 'elapsed_seconds': round(time.monotonic() - begin, 6), 'exit': p.returncode,
                    'stdout_sha256': hashlib.sha256(p.stdout.encode()).hexdigest(), 'stderr_nonempty': bool(p.stderr)}
            runs.append(item)
            print(json.dumps(item), flush=True)
            return p.stdout
        original_outputs = []
        for flags in ((), ('-O',)):
            text = child('original-' + ('O' if flags else 'normal'), original / 'verify.py', flags)
            need(json.loads(text)['record_sha256'] == source_hash, 'whole original source fixture regenerated')
            original_outputs.append(text)
        need(original_outputs[0] == original_outputs[1], 'entire original normal/O output')
        outputs = []
        for flags in ((), ('-O',)):
            outputs.append(child('independent-' + ('O' if flags else 'normal'), new / 'verify.py', flags))
        need(outputs[0] == outputs[1], 'whole independent normal/O output')
        altered = json.loads((new / 'EXPECTED.json').read_text())
        altered['whole_original_cube']['full_eta_derivative_certificate']['individual_multiplier_eta_derivatives'][1][0] = '0'
        (root / 'altered.json').write_text(json.dumps(altered))
        (root / 'malformed.json').write_text('{')
        for flags in ((), ('-O',)):
            for name in ('missing', 'malformed', 'altered'):
                child('rejected-' + name + '-' + ('O' if flags else 'normal'), new / 'verify.py', flags, ('--fixture', str(root / (name + '.json'))), False)
        controls = independent['controls']
        result = {'actual_agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer', 'status': 'PASS',
            'python': sys.version.split()[0], 'native_threads': 1, 'child_guard_seconds': 45, 'local_math_children_serial': True,
            'inputs_verified': len(manifest['files']), 'original_full_fixture_verified_by_original': True,
            'original_full_fixture_canonical_sha256': source_hash,
            'independent_full_fixture_canonical_sha256': hashlib.sha256(canonical(independent)).hexdigest(),
            'all_shared_complete_initial_normal_matrices_and_individual_weights_equal': True, 'whole_outputs_normal_O_equal': True,
            'literal_new_checks': controls['checks'], 'mathematical_damage_cases': len(controls['mathematical_damage_rejections']),
            'distinct_mathematical_damage_types': len(set(controls['mathematical_damage_rejections'])),
            'invalid_domains_rejected': controls['invalid_domains_rejected'], 'external_fixture_rejections': 6,
            'peak_child_rss_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, 'runs': runs,
            'trust_boundary': independent['trust_boundary']}
        if args.write_validation:
            args.write_validation.write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
