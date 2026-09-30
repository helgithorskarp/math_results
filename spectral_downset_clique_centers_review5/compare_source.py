#!/usr/bin/env python3
"""Optional all-entry hash comparison with the pinned reviewed source.

This script imports author constructors. It is a bridge check, not part of
the independent proof trust boundary. Usage: python3 compare_source.py DIR.
DIR must contain the b95d1958... structural source files; see README.md.
"""
from pathlib import Path
import importlib
import json
import sys
import audit


def compare(directory):
    sys.path.insert(0, str(Path(directory).resolve()))
    clique = importlib.import_module('clique_centers')
    repair = importlib.import_module('maxrank_mixtures')
    expected = json.loads(Path(__file__).with_name('audit_expected.json').read_text())
    reports = []
    for name in ('clique_centers', 'two_centers', 'friendship'):
        for record in expected[name]:
            if name == 'clique_centers':
                r, t = record['r'], record['t']
                sets, matrix, s = clique.certificate(r, t)
                literal = audit.clique(r, t)
                masks = [sum(1 << i for i in member) for member in literal]
                parameters = [r, t]
            elif name == 'two_centers':
                t = record['t']
                sets, matrix, s = repair.two_center_certificate(t)
                literal = audit.clique(2, t)
                mapping = [t, t+1]+list(range(t))
                masks = [sum(1 << mapping[i] for i in member) for member in literal]
                parameters = [t]
            else:
                k = record['k']
                sets, matrix, s = repair.friendship_certificate(k)
                decoded = [frozenset(i for i in range(2*k+1) if word >> i & 1) for word in sets]
                literal = sorted(decoded, key=audit.order)
                masks = [sum(1 << i for i in member) for member in literal]
                parameters = [k]
            audit.need(len(sets) == len(masks) and set(sets) == set(masks), 'literal source domain mismatch')
            positions = [sets.index(word) for word in masks]
            canonical = [[matrix[i][j] for j in positions] for i in positions]
            audit.need(s == record['s'] and audit.digest(canonical) == record['matrix_sha256'], 'all-entry source hash mismatch')
            reports.append({'family': name, 'parameters': parameters, 'N': len(sets),
                            'compared_entries': len(sets)**2, 'matrix_sha256': audit.digest(canonical)})
    return {'reviewer': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
            'comparison': 'SHA-256 of every exact entry in independently normalized literal-set order',
            'author_imports': True, 'cases': reports}


if __name__ == '__main__':
    audit.need(len(sys.argv) == 2, 'expected pinned author source directory argument')
    print(json.dumps(compare(sys.argv[1]), indent=2, sort_keys=True))
