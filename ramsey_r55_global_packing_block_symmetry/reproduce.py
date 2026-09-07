#!/usr/bin/env python3
"""Regenerate all compact checks and the normalized r7-s4-t3 formula."""
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


def invoke(script, args, output, optimized=False):
    command = [sys.executable, '-B']
    if optimized:
        command.append('-O')
    command += [str(HERE / script), *map(str, args), '--output', str(output)]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
    return json.loads(output.read_text())


def run():
    if digest(TARGET / 'SHA256SUMS') != EXPECTED_MANIFEST:
        raise ValueError('h3835 source manifest changed')
    if digest(TARGET / 'model.py') != EXPECTED_MODEL:
        raise ValueError('h3835 model changed')
    expected_controls = json.loads((HERE / 'controls.json').read_text())
    expected_audit = json.loads((HERE / 'audit.json').read_text())
    expected_interface = json.loads((HERE / 'interface-audit.json').read_text())
    with tempfile.TemporaryDirectory(prefix='r55-block-symmetry-') as raw:
        work = Path(raw); cnf = work / 'normalized.cnf'; metadata = work / 'metadata.json'
        subprocess.run([sys.executable, '-B', str(HERE / 'block_symmetry.py'),
                        '--target', str(TARGET), '--branch', '7,4,3',
                        '--cnf', str(cnf), '--metadata', str(metadata)],
                       check=True, stdout=subprocess.DEVNULL)
        generated = json.loads(metadata.read_text())
        if generated['sha256'] != expected_audit['sha256'] or digest(cnf) != expected_audit['sha256']:
            raise ValueError('formula identity')
        for optimized in (False, True):
            controls = invoke('controls.py', [], work / f'controls-{optimized}.json', optimized)
            audit = invoke('audit.py', [cnf], work / f'audit-{optimized}.json', optimized)
            interface = invoke('interface_audit.py', ['--target', TARGET],
                               work / f'interface-{optimized}.json', optimized)
            if controls != expected_controls or audit != expected_audit or interface != expected_interface:
                raise ValueError('replay record mismatch')
    result = json.loads((HERE / 'RESULT.json').read_text())
    return {'status': 'VERIFIED_GLOBAL_PACKING_BLOCK_SYMMETRY_REPLAY',
            'branches_normalized': 60, 'production_branch': [7, 4, 3],
            'cnf_sha256': expected_audit['sha256'],
            'normal_and_optimized_checks_match': True,
            'solver_status': result['solver_status'],
            'target43_found': result['target43_found'],
            'branch_excluded': result['branch_excluded']}


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True))
