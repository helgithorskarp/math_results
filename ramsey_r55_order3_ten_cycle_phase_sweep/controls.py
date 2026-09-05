#!/usr/bin/env python3
"""Full-graph normalization controls and adversarial formula checks."""
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import random
import shutil

import audit
import model


def full_normalization():
    rng = random.Random(55031006)
    ids = audit.pair_ids()
    sigma = [3*(v//3)+(v+1) % 3 if v < 30 else v for v in range(43)]
    perms = [p for p in permutations(range(4))
             if {frozenset((p[0], p[1])), frozenset((p[2], p[3]))} == model.MATCHING]
    tested = 0
    for orbit in model.classes():
        for phase in orbit['members']:
            core = audit.literal_graph(phase)
            values = {v: bool(rng.randrange(2)) for v in set(ids.values())}
            # Every minority mixed row gets p in 1..4, in arbitrary column order.
            for i in range(4):
                ones = set(rng.sample(range(4, 10), rng.randrange(1, 5)))
                for j in range(4, 10):
                    positions = set(rng.sample(range(3), 1 if j in ones else 2))
                    for t in range(3):
                        values[ids[3*i, 3*j+t]] = t in positions
            graph = {e: (core[e] if e[1] < 12 else
                         values[ids[e]] if e in ids else e[0]//3 < 4)
                     for e in combinations(range(43), 2)}
            candidates = [(p, sign) for p in perms for sign in (-1, 1)
                          if model.relabel(phase, p, sign) == tuple(orbit['phase'])]
            for perm, sign in candidates:
                blue = rng.sample(range(4, 10), 6)
                order = list(perm) + blue
                mapping = [3*i+(sign*t) % 3 for i in order for t in range(3)] + rng.sample(range(30, 43), 13)

                def color(u, v):
                    return graph[tuple(sorted((mapping[u], mapping[v])))]

                for j in range(1, 10):
                    block = mapping[3*j:3*j+3]
                    for shift in range(3):
                        mapping[3*j:3*j+3] = block[shift:]+block[:shift]
                        word = [color(0, 3*j+t) for t in range(3)]
                        if word == sorted(word, reverse=True):
                            break
                    else:
                        raise ValueError('missing whole-graph phase normalization')
                blue_order = sorted(range(4, 10), key=lambda j: sum(color(0, 3*j+t) for t in range(3)))
                blocks = [mapping[3*j:3*j+3] for j in blue_order]
                mapping[12:30] = [v for b in blocks for v in b]
                fixed_order = sorted(range(30, 43), key=lambda v: tuple(color(3*i, v) for i in range(10)))
                mapping[30:] = [mapping[v] for v in fixed_order]
                model.require(sorted(mapping) == list(range(43)), 'full mapping not a permutation')
                for v in range(43):
                    other = mapping[v] if v >= 30 else 3*(mapping[v]//3)+(mapping[v]+sign) % 3
                    model.require(mapping[sigma[v]] == other, 'not a whole-action normalizer')
                model.require(all(color(a, b) == color(sigma[a], sigma[b])
                                  for a, b in combinations(range(43), 2)), 'whole invariance lost')
                desired = audit.literal_graph(orbit['phase'])
                model.require(all(color(*e) == desired[e] for e in desired), 'wrong representative core')
                model.require(all(color(3*i, 3*i+1) == (i < 4) for i in range(10)), 'internal colors lost')
                words = [[int(color(0, 3*j+t)) for t in range(3)] for j in range(1, 10)]
                model.require(all(w == sorted(w, reverse=True) for w in words), 'anchor phases lost')
                weights = [sum(w) for w in words]
                model.require(weights in [model.weights()[a] for a in model.ANCHORS], 'wrong anchor cube')
                signatures = [tuple(color(3*i, v) for i in range(10)) for v in range(30, 43)]
                model.require(signatures == sorted(signatures), 'fixed signatures unsorted')
                tested += 1
    return tested


def rejection_controls(base, work):
    work.mkdir(parents=True, exist_ok=True)
    case = model.cases()[0]
    valid = work / 'valid.cnf'
    model.generate(base, valid, case)
    audit.check_formula(base, valid, case)
    data = valid.read_bytes()
    header, body = data.split(b'\n', 1)
    tail_start = len(data)-sum(len((' '.join(map(str,c))+' 0\n').encode()) for c in model.tail(case))
    prefix, tail = data[:tail_start], data[tail_start:]
    lines = tail.splitlines(keepends=True)
    flipped = lines.copy()
    value = int(flipped[-1].split()[0])
    flipped[-1] = f'{-value} 0\n'.encode()
    weakened = lines.copy()
    # Replace a global mixed-block clause, preserving the declared clause count.
    weakened[30] = b'1 -1 0\n'
    corruptions = {
        'wrong_phase_unit': prefix+b''.join(flipped),
        'missing_unit': prefix+b''.join(lines[:-1]),
        'global_constraint_removed': prefix+b''.join(weakened),
        'wrong_variable_header': b'p cnf 28950 927334\n'+body,
        'parent_clause_modified': header+b'\n1 -1 0\n'+body.split(b'\n', 1)[1],
    }
    rejected = []
    for name, content in corruptions.items():
        path = work / (name+'.cnf')
        path.write_bytes(content)
        try:
            audit.check_formula(base, path, case)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('accepted corrupted formula: '+name)
    return rejected


def corrupt_core_control(base, work):
    import certificates
    manifest = json.loads((model.ROOT / 'certificate_manifest.json').read_text())
    row = dict(manifest['cases'][0])
    i = row['index']
    work.mkdir(parents=True, exist_ok=True)
    source = model.ROOT / 'certificates'
    for suffix in ('.cnf', '.drat'):
        shutil.copyfile(source / f'case_{i:02}{suffix}', work / f'case_{i:02}{suffix}')
    core = work / f'case_{i:02}.cnf'
    lines = core.read_text().splitlines()
    header = lines[0].split()
    header[3] = str(int(header[3])+1)
    lines[0] = ' '.join(header)
    lines.append('28974 0')
    core.write_text('\n'.join(lines)+'\n')
    row['core'] = model.file_info(core)  # matching hash cannot legitimize a false input clause
    try:
        certificates.membership(base, work, [row])
    except ValueError as error:
        model.require('outside its own formula' in str(error), 'wrong corruption rejection')
    else:
        raise ValueError('accepted fake core input')
    return 'unjustified_auxiliary_unit_rejected_despite_matching_hash'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    model.require(not args.work.resolve().is_relative_to(model.ROOT.parent), 'controls outside Git')
    result = {'full_graph_normalizations': full_normalization(),
              'rejected_corruptions': rejection_controls(args.base, args.work),
              'core_membership_control': corrupt_core_control(args.base, args.work / 'bad_core')}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, sort_keys=True))
