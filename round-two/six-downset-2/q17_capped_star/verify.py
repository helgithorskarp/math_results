"""Source-only clean normal/optimized replay, serial fixed-45-second children."""
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
    lines = (source / 'SHA256SUMS').read_text().splitlines()
    names = []
    for line in lines:
        expected, name = line.split('  ')
        require(Path(name).name == name and name not in names, 'unique local source manifest path')
        require(hashlib.sha256((source / name).read_bytes()).hexdigest() == expected,
                'complete public source byte gate: ' + name)
        names.append(name)
    require(set(names) == {'COEFFICIENTS.json', 'EXPECTED.json', 'original.py',
                          'positive_elimination.py', 'read_positive.py', 'defects.py',
                          'measure.py', 'verify.py', 'README.md', 'PROOF.md',
                          'DEPENDENCIES.md', 'LITERATURE.md', '.gitignore'}, 'complete source closure')
    output = Path(workdir).resolve()
    require(not output.exists(), 'choose a new output directory; no output overwrite')
    (output / 'source').mkdir(parents=True)
    isolated = output / 'source'
    for name in names + ['SHA256SUMS']:
        shutil.copyfile(source / name, isolated / name)
    expected = json.loads((isolated / 'EXPECTED.json').read_bytes())
    environment = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        environment[key] = '1'
    environment['PYTHONPATH'] = ''
    receipts = []
    modes = [('normal', []), ('optimized', ['-O'])]
    for label, extra in modes:
        jobs = [('original', ['--record', str(output / (label + '-original.json'))]),
                ('defects', ['--record', str(output / (label + '-defects.json'))])]
        for endpoint in ('lower', 'upper'):
            jobs.append(('read_positive', ['--endpoint', endpoint,
                         '--record', str(output / (label + '-' + endpoint + '.json')),
                         '--full-record', str(output / (label + '-' + endpoint + '-full.json'))]))
        for script, arguments in jobs:
            endpoint = arguments[1] if script == 'read_positive' else script
            name = label + '-' + endpoint
            resource_file = output / (name + '-resource.json')
            command = [sys.executable, '-B'] + extra + [str(isolated / 'measure.py'),
                       str(resource_file), str(isolated / (script + '.py'))] + arguments
            started = time.monotonic()
            try:
                result = subprocess.run(command, cwd=isolated, env=environment, text=True,
                                        capture_output=True, timeout=45, check=False)
            except subprocess.TimeoutExpired:
                raise RuntimeError('45-second operational limit: ' + name +
                                   '; no mathematical nonexistence inference') from None
            (output / (name + '-stdout.txt')).write_text(result.stdout)
            (output / (name + '-stderr.txt')).write_text(result.stderr)
            require(result.returncode == 0, 'complete child must succeed: ' + name)
            receipts.append({'name': name, 'seconds': time.monotonic() - started,
                             'resource': json.loads(resource_file.read_bytes())})
            print(json.dumps({'completed': name, 'seconds': receipts[-1]['seconds']}), flush=True)
    for item in ('original', 'defects', 'lower', 'upper', 'lower-full', 'upper-full'):
        a = (output / ('normal-' + item + '.json')).read_bytes()
        b = (output / ('optimized-' + item + '.json')).read_bytes()
        require(a == b, 'ENTIRE normal/optimized record equality: ' + item)
        if item in expected:
            require(json.loads(a) == expected[item], 'entire compact expected result: ' + item)
    receipt = {'agent': 'six-downset-2', 'role': 'researcher', 'source_only_isolated_copy': True,
               'entire_normal_optimized_original_and_endpoint_records_equal': True,
               'entire_normal_optimized_full_proofs_equal': True,
               'semantic_defects_each_mode': 17, 'complete_children': 8,
               'guard_seconds_per_child': 45, 'native_threads': 1, 'max_concurrent_children': 1,
               'ordinary_bridges_unformalized': True, 'independently_reviewed': False,
               'resources': receipts}
    (output / 'VALIDATION.json').write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workdir', required=True)
    main(parser.parse_args().workdir)
