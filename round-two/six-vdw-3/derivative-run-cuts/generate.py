#!/usr/bin/env python3
"""Exact derivative-distance fiber of the published separable cut model."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

BASE_SHA = '21bba5e30eae728ded9cc45a6a75c5522c644fd411980bc5c9310e96b19e637f'


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def counter(inputs, target, start):
    """Fully defined unary prefix count, truncated at target+1."""
    demand(0 < target < len(inputs), 'counter target must be interior')
    variables = start
    cells, clauses = {}, set()

    def minus(literal):
        return not literal if isinstance(literal, bool) else -literal

    def add(*literals):
        if any(literal is True for literal in literals):
            return
        row = {literal for literal in literals if literal is not False}
        if any(-literal in row for literal in row):
            return
        demand(bool(row), 'unexpected empty clause')
        clauses.add(tuple(sorted(row, key=abs)))

    for i, x in enumerate(inputs, 1):
        for k in range(1, min(i, target+1)+1):
            variables += 1
            z = cells[i, k] = variables
            a = cells.get((i-1, k), False)
            b = True if k == 1 else cells[i-1, k-1]
            # z <=> a OR (x AND b).
            add(minus(a), z)
            add(-x, minus(b), z)
            add(-z, a, x)
            add(-z, a, b)
    add(cells[len(inputs), target])
    add(-cells[len(inputs), target+1])
    return variables, clauses


def model(q, distance, base_path):
    demand(hashlib.sha256(base_path.read_bytes()).hexdigest() == BASE_SHA,
           'published base generator has changed')
    spec = importlib.util.spec_from_file_location('published_cut_generator', base_path)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    text, base_metadata = base.model(q)
    demand(0 < distance < q and distance % 2 == 0, 'distance must be even and interior')
    clauses = {tuple(map(int, row.split()[:-1])) for row in text.splitlines()[1:]}
    labels = {pair: i+1 for i, pair in enumerate(itertools.combinations(range(q), 2))}
    edge = lambda x, y: labels[tuple(sorted((x, y)))]
    derivative = [edge(x, (x+3) % q) for x in range(q)]
    demand(len(set(derivative)) == q, 'derivative edge repetition')
    zeros = distance > q//2
    target = q-distance if zeros else distance
    inputs = [-x if zeros else x for x in derivative]
    variables, extra = counter(inputs, target, base_metadata['variables'])
    clauses.update(extra)
    # Translate a minority derivative entry to zero. u(0)=0 is already
    # implicit in the anchor-cut representation, with no extra bit fixed.
    clauses.add((-edge(0, 3) if zeros else edge(0, 3),))
    text = f'p cnf {variables} {len(clauses)}\n'
    text += ''.join(' '.join(map(str, row))+' 0\n' for row in sorted(clauses))
    metadata = {'q': q, 'distance': distance, 'counted_color': 0 if zeros else 1,
                'counter_target': target, 'variables': variables,
                'base_variables': base_metadata['variables'],
                'counter_variables': variables-base_metadata['variables'],
                'clauses': len(clauses), 'model_sha256': hashlib.sha256(text.encode()).hexdigest()}
    return text, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--q', type=int, default=103)
    parser.add_argument('--distance', type=int, required=True)
    parser.add_argument('--base-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    text, metadata = model(args.q, args.distance, args.base_source)
    args.output.write_text(text, encoding='ascii')
    print(json.dumps(metadata, sort_keys=True))


if __name__ == '__main__':
    main()
