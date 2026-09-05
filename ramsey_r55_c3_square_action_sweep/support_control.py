#!/usr/bin/env python3
"""Exercise core support rejection with a syntactically valid extra axiom."""
from pathlib import Path
import argparse
import json
import tempfile
import certificates
import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', required=True, type=Path)
    parser.add_argument('--core', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    model.require(not args.work.resolve().is_relative_to(model.ROOT.parent), 'controls outside Git')
    with args.full.open() as stream:
        header = stream.readline().split()
    model.require(header[:2] == ['p', 'cnf'], 'full header')
    nv = int(header[2])
    accepted = certificates.support(args.full, args.core, nv)
    lines = args.core.read_text().splitlines()
    lines[0] = f'p cnf {nv} {len(lines)}'
    lines.append('0')
    args.work.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='support-', dir=args.work) as directory:
        bad = Path(directory) / 'bad.cnf'
        bad.write_text('\n'.join(lines)+'\n')
        try:
            certificates.support(args.full, bad, nv)
        except ValueError as error:
            model.require(str(error) == 'unsupported core axiom', 'wrong rejection stage')
            rejection = str(error)
        else:
            raise ValueError('unsupported axiom accepted')
    report = {'accepted_support': accepted, 'unsupported_axiom_rejected': rejection}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, sort_keys=True))
