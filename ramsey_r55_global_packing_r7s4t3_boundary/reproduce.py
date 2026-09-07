#!/usr/bin/env python3
"""Regenerate and independently audit the exact h3835 r7-s4-t3 CNF."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / 'ramsey_r55_global_clique_packing'
EXPECTED_MANIFEST = '1e3cafb437e30478f3961200529cb0a7bb4d5065495f8bf47f0da7589457172e'
EXPECTED_MODEL = '620833aac2a36bd368d0111f70cd9032f613d6cb15450d4142d0c54ae6af3f41'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run():
    if digest(TARGET / 'SHA256SUMS') != EXPECTED_MANIFEST:
        raise ValueError('h3835 source manifest changed')
    if digest(TARGET / 'model.py') != EXPECTED_MODEL:
        raise ValueError('h3835 model source changed')
    expected = json.loads((HERE / 'audit.json').read_text())
    with tempfile.TemporaryDirectory(prefix='r55-r7s4t3-') as raw:
        work = Path(raw)
        cnf = work / 'branch.cnf'
        generation = subprocess.run(
            [sys.executable, '-B', str(TARGET / 'model.py'), '--branch',
             '7,4,3', '--cnf', str(cnf)], check=True, text=True,
            stdout=subprocess.PIPE).stdout
        generated = json.loads(generation)
        if generated['sha256'] != expected['sha256'] or digest(cnf) != expected['sha256']:
            raise ValueError('regenerated formula identity')
        records = []
        for optimized in (False, True):
            output = work / ('audit-O.json' if optimized else 'audit.json')
            command = [sys.executable, '-B']
            if optimized:
                command.append('-O')
            command += [str(HERE / 'audit.py'), str(cnf), '--output', str(output)]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
            record = json.loads(output.read_text())
            if record != expected:
                raise ValueError('audit replay differs')
            records.append(record)
    return {
        'status': 'VERIFIED_R7_S4_T3_UNKNOWN_BOUNDARY_REPLAY',
        'branch': [7, 4, 3],
        'cnf_sha256': expected['sha256'],
        'clauses': expected['clauses'],
        'normal_and_optimized_audits_match': records[0] == records[1],
        'solver_status': json.loads((HERE / 'RESULT.json').read_text())['solver_status'],
        'target43_found': False,
        'branch_excluded': False,
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
