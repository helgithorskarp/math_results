"""Regenerate all twelve CNFs and compare exact production hashes.

This checks formula/source integrity, not UNSAT; use prove.py for that.
"""
import hashlib
import json
from pathlib import Path
import tempfile

import generate_cnf


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'manifest.json').read_text())
    generator = hashlib.sha256((root / 'generate_cnf.py').read_bytes()).hexdigest()
    if generator != manifest['generator_sha256']:
        raise ValueError('Generator hash differs from audited source')
    records = {row['case']: row for row in manifest['cases']}
    if len(records) != len(manifest['cases']) or set(records) != set(generate_cnf.CASES):
        raise ValueError('Manifest does not cover exactly all twelve cases')
    for name, expected in records.items():
        formula, pool = generate_cnf.case_formula(name)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'case.cnf'
            formula.to_file(str(path))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if (digest != expected['cnf_sha256'] or pool.top != expected['variables']
                or len(formula.clauses) != expected['clauses']):
            raise ValueError('Formula mismatch: ' + name)
    print(json.dumps({'cases': len(records), 'status': 'ALL CNF HASHES MATCH'}))


if __name__ == '__main__':
    main()
