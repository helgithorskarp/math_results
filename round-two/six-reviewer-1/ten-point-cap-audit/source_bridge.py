#!/usr/bin/env python3
"""Compare the independent literal construction with the pinned author source.

This optional check imports author code and is explicitly separate from audit.py.
Pass the spectral_downset_multiple_pair_caps directory at the pinned commit.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import audit


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('author_directory', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    root = args.author_directory
    files = sorted(p.name for p in root.iterdir() if p.is_file())
    hashes = {name: sha256((root / name).read_bytes()).hexdigest() for name in files}
    author_matrices = load_module('matrices', root / 'matrices.py')
    author_blocks = load_module('blocks', root / 'blocks.py')
    result, (D, L, forms) = audit.audit()
    z = {2: F(519, 25), 3: F(107, 50), 4: F(111, 50), 5: F(11, 5)}
    delta = {3: F(11, 25), 4: F(6, 25)}
    members, matrix = author_matrices.construct(10, z, F(47, 50), delta)
    original_index = {A: i for i, A in enumerate(members)}
    audit.require(set(members) == set(D), 'same exact original vertices')
    audit.require(all(F(L[i][j], 100) == matrix[original_index[A]][original_index[B]]
                      for i, A in enumerate(D) for j, B in enumerate(D)),
                  'all original entries agree with closed author formula')
    blocks, _ = author_blocks.blocks(10, z, F(47, 50), delta)
    mapping = {'constant_lower': ('Q0', 1), 'constant_upper': ('U0', 1),
               'point_lower': ('Q1', 2), 'point_upper': ('U1', 2),
               'coupled_lower': ('C', 4), 'coupled_upper': ('U', 4)}
    for name, (author_name, factor) in mapping.items():
        a, b = forms[name], blocks[author_name]
        audit.require(a == [[factor * x for x in row] for row in b],
                      'literal reduced form agrees with author normalization: ' + name)
    out = {'reviewer': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
           'author_commit': 'c8faaa8296979c886916db72f4eaeed16874f589',
           'author_directory': 'spectral_downset_multiple_pair_caps',
           'author_file_sha256': hashes, 'all_original_entries_compared': len(D) ** 2,
           'six_forms_compared': mapping,
           'independent_matrix_sha256': result['full_scaled_matrix_sha256'],
           'trust_boundary': 'Optional bridge imports pinned author construction and block code; audit.py itself imports no author code.'}
    raw = json.dumps(out, indent=2) + '\n'
    if args.check:
        audit.require(raw == args.check.read_text(), 'bridge expected output mismatch')
    print(raw, end='')


if __name__ == '__main__':
    main()
