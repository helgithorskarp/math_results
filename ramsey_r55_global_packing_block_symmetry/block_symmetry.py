#!/usr/bin/env python3
"""Add sound identical-block lex normalization to an h3835 branch formula."""
from collections import OrderedDict
from pathlib import Path
import argparse
import hashlib
import json
import sys


def lex_geq(xs, ys, first_aux):
    """CNF for the unsigned bit vector xs >= ys; inputs are MSB first."""
    if len(xs) != len(ys) or not xs:
        raise ValueError('equal nonempty bit vectors required')
    clauses = []
    prefix_equal = 1  # h3835's forced-true variable
    next_aux = first_aux
    for i, (x, y) in enumerate(zip(xs, ys)):
        clauses.append((-prefix_equal, x, -y))
        if i + 1 < len(xs):
            updated = next_aux
            next_aux += 1
            # updated <-> prefix_equal and (x == y)
            clauses.extend([
                (-updated, prefix_equal),
                (-updated, -x, y),
                (-updated, x, -y),
                (-prefix_equal, -x, -y, updated),
                (-prefix_equal, x, y, updated),
            ])
            prefix_equal = updated
    return clauses, next_aux


def added_clauses(packing):
    root = packing.blocks[0]
    groups = OrderedDict()
    for index, kind in enumerate(packing.types[1:], 1):
        groups.setdefault(kind, []).append(index)

    def key_bits(block_index):
        # Child vertices are already sorted by their integer root signatures.
        # Compare signature bits high to low, then vertices left to right.
        return tuple(
            packing.variables[root[row], vertex]
            for vertex in packing.blocks[block_index]
            for row in range(3, -1, -1)
        )

    clauses = []
    next_aux = 848
    comparisons = []
    for kind, indices in groups.items():
        for left, right in zip(indices, indices[1:]):
            current, next_aux = lex_geq(key_bits(left), key_bits(right), next_aux)
            clauses.extend(current)
            comparisons.append({'kind': kind, 'left_block': left,
                                'right_block': right,
                                'key_bits': len(key_bits(left)),
                                'clauses': len(current)})
    return clauses, next_aux - 1, comparisons


def generate(branch, target, output):
    sys.path.insert(0, str(target))
    import model
    packing = model.Packing(branch)
    added, variables, comparisons = added_clauses(packing)
    base_count = sum(1 for _ in packing.clauses())
    output = Path(output)
    if output.exists():
        raise ValueError('refusing to overwrite CNF')
    digest = hashlib.sha256()
    histogram = {}
    count = 0
    with output.open('wb') as stream:
        header = f'p cnf {variables} {base_count + len(added)}\n'.encode()
        stream.write(header); digest.update(header)
        for clause in packing.clauses():
            line = (' '.join(map(str, clause)) + ' 0\n').encode()
            stream.write(line); digest.update(line); count += 1
            histogram[len(clause)] = histogram.get(len(clause), 0) + 1
        for clause in added:
            line = (' '.join(map(str, clause)) + ' 0\n').encode()
            stream.write(line); digest.update(line); count += 1
            histogram[len(clause)] = histogram.get(len(clause), 0) + 1
    if count != base_count + len(added):
        raise ValueError('clause count')
    return {'status': 'GENERATED_IDENTICAL_BLOCK_NORMALIZED_FORMULA',
            'branch': branch, 'variables': variables, 'clauses': count,
            'base_clauses': base_count, 'symmetry_clauses': len(added),
            'auxiliary_prefix_variables': variables - 847,
            'comparisons': comparisons, 'bytes': output.stat().st_size,
            'sha256': digest.hexdigest(),
            'clause_lengths': dict(sorted(histogram.items()))}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--branch', required=True)
    parser.add_argument('--cnf', type=Path, required=True)
    parser.add_argument('--metadata', type=Path)
    args = parser.parse_args()
    result = generate(list(map(int, args.branch.split(','))), args.target, args.cnf)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.metadata:
        args.metadata.write_text(text)
    print(text, end='')
