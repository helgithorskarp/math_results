#!/usr/bin/env python3
"""Malformed-formula controls for the actual whole-file checker."""
from pathlib import Path
import argparse
import json
import tempfile

import extension_model as ext
import check_layer


def controls(base, cnf, work):
    case = ext.cases()[0]
    check_layer.check_formula(base, cnf, case)
    source = cnf.read_bytes()
    ext.parent.require(source.endswith(b'-237 0\n'), 'fixture final unit')
    header, body = source.split(b'\n', 1)
    mutations = {
        'wrong_polarity': source[:-7]+b'237 0\n',
        'wrong_cycle': source[:-7]+b'-238 0\n',
        'missing_unit': source[:-7],
        'wrong_header': b'p cnf 28974 927345\n'+body,
        'changed_parent_clause': header+b'\n'+(b'-' if body[:1] != b'-' else b'')+
                                 (body if body[:1] != b'-' else body[1:]),
    }
    work.mkdir(parents=True, exist_ok=True)
    rejected = {}
    with tempfile.TemporaryDirectory(prefix='formula-controls-', dir=work) as directory:
        bad = Path(directory) / 'bad.cnf'
        for name, data in mutations.items():
            bad.write_bytes(data)
            try:
                check_layer.check_formula(base, bad, case)
            except ValueError as error:
                rejected[name] = str(error)
            else:
                raise ValueError('accepted malformed formula: '+name)
    ext.parent.require(len(rejected) == 5, 'incomplete controls')
    return {'accepted_case_0': ext.parent.file_info(cnf), 'rejected': rejected}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True, type=Path)
    parser.add_argument('--cnf', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    ext.parent.require(not args.work.resolve().is_relative_to(ext.ROOT.parent), 'controls outside Git')
    result = controls(args.base, args.cnf, args.work)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
