"""Replay compact checks; optionally regenerate and audit both complete encodings."""
from pathlib import Path
import argparse
import hashlib
import json
import time
import compile as compiler
import audit

HERE = Path(__file__).resolve().parent


def main(directory=None):
    start = time.monotonic()
    manifest = HERE/'SHA256SUMS'
    checked = 0
    for line in manifest.read_text().splitlines():
        wanted, name = line.split('  ', 1)
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != wanted:
            raise ValueError('source identity: '+name)
        checked += 1
    expected = json.loads((HERE/'VALIDATION.json').read_text())
    controls = audit.controls()
    if controls != expected['controls']:
        raise ValueError('compact controls disagree')
    full = []
    if directory is not None:
        directory = Path(directory); directory.mkdir(exist_ok=False)
        for factored, name in [(False, 'direct'), (True, 'factored')]:
            path = directory/(name+'.cnf')
            generation = compiler.write(path, factored)
            actual = audit.full_audit(path, factored)
            if actual != expected[name]:
                raise ValueError('independent full audit: '+name)
            for field in ('clauses', 'sha256'):
                if generation[field] != actual[field]:
                    raise ValueError('producer/auditor disagreement')
            full.append({'encoding': name, 'generation': generation, 'audit': actual})
    return {'status': 'VERIFIED_REPLAY', 'manifest_entries': checked, 'controls': controls,
            'complete_formulas_audited': len(full), 'full': full,
            'seconds': time.monotonic()-start, 'solver_calls': 0}


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--generate', type=Path); a = p.parse_args()
    print(json.dumps(main(a.generate), indent=2, sort_keys=True))
