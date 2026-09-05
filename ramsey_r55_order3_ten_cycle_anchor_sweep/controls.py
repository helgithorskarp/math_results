#!/usr/bin/env python3
"""Reject corrupt cube layers and check known graph controls."""
from pathlib import Path
import argparse
import json

import audit
from verify_graph import inspect
from verify import membership
from sweep import file_info


def run(work, base):
    work.mkdir(parents=True, exist_ok=True)
    weights = audit.load_weights()[0]
    units = [(1 + 3 * j + t) * (1 if t < w else -1) for j, w in enumerate(weights) for t in range(3)]
    original = audit.CUBE_HEADER + base.read_bytes().split(b'\n', 1)[1] + ''.join(f'{x} 0\n' for x in units).encode()
    valid = work / 'valid.cnf'
    valid.write_bytes(original)
    audit.check_cube(base, valid, 0)
    mutations = {
        'wrong_anchor_unit': original[:-6] + b'27 0\n',
        'missing_unit': original[:original.rfind(b'\n', 0, len(original) - 1) + 1],
        'changed_parent_clause': original.replace(b' 0\n', b' 1 0\n', 1),
        'wrong_header': original.replace(b'927027', b'927026', 1),
    }
    rejected = []
    for name, data in mutations.items():
        audit.require(data != original, 'mutation unchanged')
        path = work / (name + '.cnf')
        path.write_bytes(data)
        try:
            audit.check_cube(base, path, 0)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted mutation: ' + name)
    positive = inspect(audit.PARENT / 'moving30.edges')
    audit.require(positive['sha256'] == '464e148ef328230b5937ab3f8eacf833653d87e6f749424b8319784a3d256fdf'
                  and positive['ramsey'] and positive['vertices'] == 30 and positive['five_sets_inspected'] == 142506,
                  'positive control failed')
    # A complete graph is a definition-level negative control for the direct
    # graph checker and needs no external fixture or catalog.
    negative_path = work / 'negative.edges'
    negative_path.write_text('5 10\n' + ''.join(f'{u} {v}\n' for u in range(5) for v in range(u + 1, 5)))
    negative = inspect(negative_path)
    audit.require(not negative['ramsey'] and negative['monochromatic_five_set'] == list(range(5)), 'negative control failed')
    fake = work / 'fake_core'
    fake.mkdir(exist_ok=True)
    core, proof = fake / 'case_00.cnf', fake / 'case_00.drat'
    core.write_text('p cnf 28950 1\n343 0\n')
    proof.write_text('0\n')
    row = {'index': 0, 'weights': weights, 'core': file_info(core), 'proof': file_info(proof)}
    try:
        membership(base, fake, [row])
    except ValueError as error:
        audit.require('outside its parent-plus-cube formula' in str(error), 'wrong negative-core rejection')
    else:
        raise ValueError('accepted a core clause outside the case formula')
    return {'rejected_cube_mutations': rejected, 'nonmember_core_rejected': True,
            'positive_graph': positive, 'negative_graph': negative}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--base', type=Path, required=True)
    args = parser.parse_args()
    audit.require(not args.work.resolve().is_relative_to(audit.ROOT.parent), 'controls must be outside Git')
    print(json.dumps(run(args.work.resolve(), args.base.resolve()), sort_keys=True))
