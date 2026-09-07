"""Fresh exact moments and physical checks; verifies the entire public package."""
from pathlib import Path
import hashlib
import json
import time
from audit import run
from model import physical
from verify import verify


def reproduce():
    root = Path(__file__).resolve().parent
    entries = []
    for line in (root/'SHA256SUMS').read_text(encoding='utf-8').splitlines():
        digest, name = line.split('  ', 1)
        if '/' in name or name in entries or len(digest) != 64:
            raise ValueError('invalid manifest')
        entries.append(name)
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise ValueError('source hash mismatch: '+name)
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'SHA256SUMS'}
    if set(entries) != actual:
        raise ValueError('manifest does not cover every package file')
    provenance = json.loads((root/'provenance.json').read_text(encoding='utf-8'))
    for entry in provenance['verbatim_files']:
        if hashlib.sha256((root/entry['file']).read_bytes()).hexdigest() != entry['origin_sha256']:
            raise ValueError('antecedent source changed')
    started = time.monotonic()
    result = run()
    evidence = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if evidence != (root/'expected_audit.json').read_text(encoding='utf-8'):
        raise ArithmeticError('fresh evidence differs from expected output')
    fixture = result['physical']['fixture']
    for key, name in [('parameters', 'fixture_parameters.json'), ('graph', 'fixture_graph.json'), ('certificate', 'fixture_certificate.json')]:
        if json.loads((root/name).read_text(encoding='utf-8')) != fixture[key]:
            raise ArithmeticError('fixture changed')
    if physical(fixture['parameters']) != fixture['graph']:
        raise ArithmeticError('physical fixture changed')
    verify(fixture['graph'], fixture['certificate'])
    moment = result['exact']['moments']
    print(json.dumps({'status': result['status'], 'audit_sha256': hashlib.sha256(evidence.encode()).hexdigest(),
                      'removed_lower_bound': moment['removed_lower_bound'], 'remaining_upper_bound': moment['remaining_upper_bound'],
                      'elapsed_seconds': time.monotonic()-started}, sort_keys=True))


if __name__ == '__main__':
    reproduce()
