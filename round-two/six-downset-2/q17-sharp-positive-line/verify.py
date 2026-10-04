"""Standalone source-only cold replay; serial exact children, fixed45s guard."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main(workdir):
    source = Path(__file__).resolve().parent
    names = []
    for line in (source/'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ')
        require(Path(name).name == name and name not in names, 'unique local manifest file')
        require(hashlib.sha256((source/name).read_bytes()).hexdigest() == expected,
                'entire source byte gate: '+name)
        names.append(name)
    require(set(names) == {'COEFFICIENTS.json', 'EXPECTED.json', 'original.py',
        'positive_elimination.py', 'sparse.py', 'check_original.py', 'read_lower.py',
        'read_tree.py', 'face.py', 'defects.py', 'measure.py', 'verify.py',
        'README.md', 'PROOF.md', 'MASS-PROOF.md', 'DEPENDENCIES.md', 'LITERATURE.md', '.gitignore'},
        'complete standalone source closure')
    output = Path(workdir).resolve()
    require(not output.exists(), 'fresh output directory, no evidence overwrite')
    isolated = output/'source'; isolated.mkdir(parents=True)
    for name in names+['SHA256SUMS']:
        shutil.copyfile(source/name, isolated/name)
    expected = json.loads((isolated/'EXPECTED.json').read_bytes())
    env = os.environ.copy(); env['PYTHONPATH'] = ''
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[key] = '1'
    receipts = []
    for mode, flags in [('normal', []), ('optimized', ['-O'])]:
        jobs = [('original', 'original', []), ('face', 'face', []),
                ('tree', 'read_tree', []), ('defects', 'defects', [])]
        for label, tau in [('lower-zero', '0'), ('lower-interior', '1/128')]:
            jobs.append((label, 'read_lower', ['--tau', tau, '--full-record',
                          str(output/(mode+'-'+label+'-full.json'))]))
        for label, script, args in jobs:
            record = output/(mode+'-'+label+'.json')
            resource = output/(mode+'-'+label+'-resource.json')
            command = [sys.executable, '-B', *flags, str(isolated/'measure.py'),
                       str(resource), str(isolated/(script+'.py')), '--record', str(record), *args]
            start = time.monotonic()
            try:
                result = subprocess.run(command, cwd=isolated, env=env, text=True,
                                        capture_output=True, timeout=45, check=False)
            except subprocess.TimeoutExpired:
                raise RuntimeError('45s operational limit: '+label+
                                   '; incomplete evidence, no nonexistence inference') from None
            (output/(mode+'-'+label+'-stdout.txt')).write_text(result.stdout)
            (output/(mode+'-'+label+'-stderr.txt')).write_text(result.stderr)
            require(result.returncode == 0, 'complete child success: '+mode+'-'+label)
            receipt = {'mode': mode, 'label': label, 'seconds': time.monotonic()-start,
                       'resource': json.loads(resource.read_bytes()),
                       'whole_record_sha256': hashlib.sha256(record.read_bytes()).hexdigest()}
            receipts.append(receipt)
            if label in expected.get('record_sha256', {}):
                require(receipt['whole_record_sha256'] == expected['record_sha256'][label],
                        'whole published expected result: '+label)
            print(json.dumps({'completed': mode+'-'+label, 'seconds': receipt['seconds']}), flush=True)
    for label in ('original', 'face', 'tree', 'defects', 'lower-zero', 'lower-interior',
                  'lower-zero-full', 'lower-interior-full'):
        raw = (output/('normal-'+label+'.json')).read_bytes()
        require(raw == (output/('optimized-'+label+'.json')).read_bytes(),
                'ENTIRE normal/O record or proof equality: '+label)
        if label.endswith('-full'):
            require(hashlib.sha256(raw).hexdigest() == expected['private_validated_full_proofs'][label],
                    'entire regenerated endpoint proof equals saved author proof: '+label)
    validation = {'agent': 'six-downset-2', 'role': 'researcher', 'complete_children': 12,
                  'source_only_isolated_replay': True, 'whole_normal_O_records_and_proofs_equal': True,
                  'whole_new_lower_proofs_equal_saved_author_proofs': True,
                  'semantic_rejections_each_mode': 22, 'guard_seconds': 45,
                  'native_threads': 1, 'max_concurrent_children': 1,
                  'ordinary_bridges_unformalized': True, 'independently_reviewed': False,
                  'resources': receipts}
    (output/'VALIDATION.json').write_text(json.dumps(validation, sort_keys=True, indent=2)+'\n')
    print(json.dumps(validation))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--workdir', required=True)
    main(p.parse_args().workdir)
