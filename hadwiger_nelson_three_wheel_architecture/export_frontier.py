#!/usr/bin/env python3
"""Export the exact next-phase interface locally; does not isolate or solve roots."""
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json
import verify as V
import algebra as A


def run(out):
    out.mkdir(parents=True, exist_ok=False)
    encoded = (V.HERE/'certificate.json').read_bytes()
    expected = json.loads((V.HERE/'EXPECTED.json').read_text())
    A.need(hashlib.sha256(encoded).hexdigest() == expected['certificate_sha256'], 'verified source certificate')
    cert = json.loads(encoded)
    displacements, polynomials = V.input_polynomials()
    factors, decomposition = V.factor_check(cert, polynomials)
    active = {i for i, f in enumerate(factors) if f not in (A.DX, A.DY)}
    base, pair_inventory = V.pair_inventory(displacements, decomposition)
    rows, cover = V.covering(factors, active, base, pair_inventory)
    A.need(cover == expected['finite_intersection_cover'], 'verified finite cover')
    primary = cover['primary_index']
    protect = {f: min((i for i, r in enumerate(rows) if f not in r['bad']),
                      key=lambda i: (rows[i]['bad_degree_sum'], i)) for f in sorted(rows[primary]['bad'])}
    pairs = sorted({tuple(sorted((f, g))) for f, i in protect.items() for g in rows[i]['bad']})
    nonzero = [d for d in V.D if d != (0, 0)]
    collisions = sorted({V.canonical(ds) for ds in product(nonzero, repeat=3)})
    interface = {'coefficient_order': cert['coefficient_order'], 'factors': cert['factors'],
                 'active_factor_ids': sorted(active), 'colour_words': [{'name': r['name'], 'bad_factor_ids': sorted(r['bad'])} for r in rows],
                 'primary_word_index': primary, 'protecting_word_indices': sorted(protect.items()),
                 'intersection_pairs': pairs, 'collision_displacements_in_Z_omega': collisions,
                 'collision_equation': 'd+phi(x)e+phi(y)f=0, phi(t)=(1+i sqrt3 t)/(1-i sqrt3 t)',
                 'strict_candidate_filter': 'Discard pair-alignment lines. Noncollision candidates must satisfy every one of the 13 bad-factor product equations. Physical label identifications and all strict unit edges still require exact checking.'}
    output = (json.dumps(interface, separators=(',', ':'))+'\n').encode()
    (out/'frontier.json').write_bytes(output)
    receipt = {'intersection_pairs': len(pairs), 'collision_displacement_rows': len(collisions),
               'bytes': len(output), 'sha256': hashlib.sha256(output).hexdigest(),
               'root_isolation_performed': False, 'new_chromatic_solver_calls': 0}
    (out/'RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--out', type=Path, required=True)
    run(parser.parse_args().out)
