#!/usr/bin/env python3
"""Reject an unsupported core clause even after updating its byte hash."""
from pathlib import Path
import argparse
import copy
import json
import tempfile

import certificate
import extension_model as ext


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True, type=Path)
    parser.add_argument('--certificates', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    ext.parent.require(not args.work.resolve().is_relative_to(ext.ROOT.parent), 'controls outside Git')
    certificate.preflight()
    manifest = json.loads(args.manifest.read_text())
    certificate.partition(manifest['sweep'])
    entries = copy.deepcopy(manifest['cases'])
    accepted = certificate.membership(args.base, args.certificates, entries)
    args.work.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='support-control-', dir=args.work) as name:
        mutant = Path(name)
        first = entries[0]['index']
        changed = f'case_{first:02}.cnf'
        for entry in entries:
            for suffix in ('cnf', 'drat'):
                filename = f"case_{entry['index']:02}.{suffix}"
                if filename != changed:
                    (mutant / filename).symlink_to((args.certificates / filename).resolve())
        lines = (args.certificates / changed).read_text().splitlines()
        header = lines[0].split()
        lines[0] = f'p cnf 28974 {int(header[3])+1}'
        lines.append('0')  # The empty clause is not a parent or layer axiom.
        (mutant / changed).write_text('\n'.join(lines)+'\n')
        entries[0]['core'] = ext.parent.file_info(mutant / changed)
        try:
            certificate.membership(args.base, mutant, entries)
        except ValueError as error:
            ext.parent.require(str(error) == 'core clause outside its case formula', 'wrong rejection stage')
            rejection = str(error)
        else:
            raise ValueError('unsupported empty core axiom was accepted')
    result = {'accepted_support': accepted, 'unsupported_core_axiom_rejected': rejection,
              'mutated_core_hash_was_updated': True}
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
