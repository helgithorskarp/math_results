"""Regenerate and independently audit the exact formula; never run a solver."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'ramsey_r55_maximal_block_order'
SOURCE_MANIFEST = '452b38de607c4bfecd9f6addbf363b47b1400c8c63eaee954d68466648f534e6'
TASK = 'bo1-q7-r7-c000000'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def source_identity():
    raw = (SOURCE / 'SHA256SUMS').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_MANIFEST, 'ordered source manifest')
    entries = raw.decode().splitlines()
    require(len(entries) == 17, 'ordered source entry count')
    for line in entries:
        wanted, name = line.split('  ', 1)
        require(digest(SOURCE / name) == wanted, 'ordered source identity: ' + name)
    return len(entries)


def package_identity():
    count = 0
    for line in (HERE / 'SHA256SUMS').read_text().splitlines():
        wanted, name = line.split('  ', 1)
        require(digest(HERE / name) == wanted, 'package identity: ' + name)
        count += 1
    return count


def command(optimized, script, *arguments):
    result = [sys.executable]
    if optimized:
        result.append('-O')
    result.extend(['-B', str(script), *map(str, arguments)])
    return result


def run(cache):
    start = time.monotonic()
    source_entries = source_identity()
    expected = json.loads((HERE / 'FORMULA_AUDIT.json').read_text())
    expected_controls = json.loads((HERE / 'MODEL_CONTROLS.json').read_text())
    with tempfile.TemporaryDirectory(prefix='r55-bo1-q7r7-') as raw:
        work = Path(raw)
        cnf = work / 'formula.cnf'
        generated = subprocess.run(
            command(False, SOURCE / 'ordered.py', cache, '--task', TASK,
                    '--triangles', '--cnf', cnf),
            check=True, text=True, stdout=subprocess.PIPE).stdout
        require(json.loads(generated) == expected, 'generated formula record')
        require(digest(cnf) == expected['sha256'], 'generated formula bytes')
        audits = []
        model_controls = []
        for optimized in (False, True):
            checked = subprocess.run(
                command(optimized, SOURCE / 'check_order.py', '--cache', cache,
                        '--task', TASK, '--triangles', '--cnf', cnf),
                check=True, text=True, stdout=subprocess.PIPE).stdout
            record = json.loads(checked)
            require(record == expected, 'independent literal audit')
            audits.append(record)
            models = subprocess.run(
                command(optimized, SOURCE / 'check_models.py', cache),
                check=True, text=True, stdout=subprocess.PIPE).stdout
            control = json.loads(models)
            require(control == expected_controls, 'complete-model controls')
            model_controls.append(control)
    return {
        'status': 'VERIFIED_ORDERED_TRIANGLE_Q7R7_UNKNOWN_BOUNDARY_REPLAY',
        'source_manifest_entries': source_entries,
        'package_manifest_entries': package_identity(),
        'normal_and_optimized_literal_audits_match': audits[0] == audits[1],
        'normal_and_optimized_model_controls_match': model_controls[0] == model_controls[1],
        'formula_sha256': expected['sha256'],
        'solver_status': json.loads((HERE / 'RESULT.json').read_text())['solver_status'],
        'solver_calls': 0,
        'seconds': time.monotonic() - start,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cache', type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.cache), sort_keys=True))
