#!/usr/bin/env python3
"""Audit literal edge orbits, lexicographic normalization, and every clause."""
from itertools import product
from pathlib import Path
import argparse
import json
import extension_model as ext
import audit as phase_audit


def semantic_units():
    # Reconstruct the actual permutation orbits through the parent's literal
    # checker, independently of the arithmetic variable formula in the writer.
    ids = phase_audit.pair_ids()
    selected = {(a, b) for a in range(12) for b in range(30, 33)}
    variables = {ids[e] for e in selected}
    ext.parent.require(len(selected) == 36 and len(variables) == 12, 'unit edge count')
    ext.parent.require({e for e, v in ids.items() if v in variables} == selected,
                       'a selected orbit has an unintended edge')
    result = sorted(-v for v in variables)
    ext.parent.require(result == sorted(ext.units()), 'literal units disagree with writer')
    return result


def preflight():
    manifest = json.loads((ext.ROOT / 'dependencies.json').read_text())
    for relative, digest in manifest['files'].items():
        ext.parent.require(ext.parent.file_info(ext.ROOT.parent / relative)['sha256'] == digest,
                           'dependency changed: '+relative)
    previous = phase_audit.audit()
    comparisons = 0
    for a in product((0, 1), repeat=6):
        for prefix in product((0, 1), repeat=4):
            if not any(prefix):
                continue
            for b in product((0, 1), repeat=6):
                ext.parent.require((0, 0, 0, 0)+a < prefix+b, 'fixed ordering failed')
                comparisons += 1
    units = semantic_units()
    return {'cases': ext.cases(), 'units': units, 'literal_edges_forced_blue': 36,
            'prefix_suffix_comparisons': comparisons,
            'parent_literal_relabelings': previous['literal_relabelings'],
            'parent_tail_truth_assignments': previous['truth_assignments_per_tail'],
            'base_sha256': ext.parent.BASE_SHA}


def check_formula(base, cnf, case):
    ext.parent.require(case in ext.cases(), 'case outside cover')
    ext.parent.require(ext.parent.file_info(base)['sha256'] == ext.parent.BASE_SHA, 'base digest')
    with base.open('rb') as a, cnf.open('rb') as b:
        ext.parent.require(a.readline() == ext.parent.BASE_HEADER, 'base header')
        ext.parent.require(b.readline() == b'p cnf 28974 927346\n', 'extended header')
        while block := a.read(1024*1024):
            ext.parent.require(b.read(len(block)) == block, 'modified parent clause')
        lines = b.read().decode().splitlines()
    clauses = []
    for line in lines:
        values = list(map(int, line.split()))
        ext.parent.require(values and values[-1] == 0 and all(values[:-1]), 'bad clause')
        clauses.append(tuple(sorted(values[:-1])))
    phase, _ = phase_audit.semantic_tail(case)
    expected = phase + [(v,) for v in semantic_units()]
    ext.parent.require(len(clauses) == 346 and sorted(clauses) == sorted(expected),
                       'extended tail mismatch')
    return ext.parent.file_info(cnf)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', type=Path)
    parser.add_argument('--work', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = preflight()
    if args.work:
        ext.parent.require(args.base is not None, '--work requires --base')
        result['formulas'] = [dict(case=c['index'], **check_formula(
            args.base, args.work / f"case_{c['index']:02}.cnf", c)) for c in ext.cases()]
    if args.report:
        args.report.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
