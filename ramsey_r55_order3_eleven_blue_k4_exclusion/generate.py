#!/usr/bin/env python3
"""Explicit attachment family, core blue-K4 witnesses, and a packing certificate."""
import argparse
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

PIN = '8b6b7b1b17d4a8b62cbeff401acad021764bc55986e65cab557ed9500dad48ed'
SIG = (1, 2, 4, 8, 3, 5, 9, 6, 10, 12)
CORE_PAIRS = tuple(combinations(range(4), 2))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def blue_witness(bits):
    for phases in product(range(3), repeat=4):
        if all(bits[3*k+(phases[j]-phases[i]) % 3] == '0'
               for k, (i, j) in enumerate(CORE_PAIRS)):
            return [3*i+phases[i] for i in range(4)]
    return None


def patterns():
    out = set(range(1, 16))
    for index, sig in enumerate(SIG[4:], 4):
        for subset in range(1, 16):
            if subset & sig == 0:
                out.add((1 << index) | subset)
    require(len(out) == 33, 'analytic pattern count')
    return sorted(out)


def packing():
    rows = []
    for j in range(7):
        rows.append(' '.join(f'-1 x{6*j+k+1}' for k in range(6))+' >= -1 ;')
    for k in range(6):
        rows.append(' '.join(f'+1 x{6*j+k+1}' for j in range(7))+' >= 2 ;')
    return '* #variable= 42 #constraint= 13\n'+'\n'.join(rows)+'\n'


def run(cover_path, work):
    raw = cover_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PIN, 'inherited cover bytes')
    cover = json.loads(raw)
    excluded, retained = [], []
    for case in cover['cases']:
        witness = blue_witness(case['bits'])
        row = dict(index=case['index'], bits=case['bits'], labeled=case['labeled'])
        if witness is None:
            retained.append(row)
        else:
            row['blue_k4'] = witness
            excluded.append(row)
    classification = dict(format='r55-k11-four-blue-k4-exclusion-v1', cover_sha256=PIN,
                          excluded=excluded, retained=retained,
                          excluded_classes=len(excluded), retained_classes=len(retained),
                          excluded_labeled=sum(r['labeled'] for r in excluded),
                          retained_labeled=sum(r['labeled'] for r in retained))
    attachments = dict(format='r55-blue-triangle-fixed-attachments-v1', fixed_signatures=list(SIG),
                       complementary_variants=[0, 1, 2, 4], blue_fixed_masks=patterns(),
                       max_pair_signatures=1, requires_singleton=True)
    certificate = dict(format='nonnegative-integer-row-sum-v1', multipliers=[1]*13,
                       expected_coefficients=[0]*42, expected_rhs=5)
    work.mkdir(parents=True, exist_ok=True)
    for name, data in [('classification.json', classification), ('attachments.json', attachments),
                       ('packing_certificate.json', certificate)]:
        (work/name).write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
    (work/'packing.opb').write_text(packing())
    print(json.dumps({k: v for k, v in classification.items() if k.endswith('classes') or k.endswith('labeled')}))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--cover', type=Path, default=Path(__file__).resolve().parent.parent/'ramsey_r55_order3_eleven_four_core/cover.json')
    p.add_argument('--work', type=Path, required=True)
    a = p.parse_args()
    require(not a.work.resolve().is_relative_to(Path(__file__).resolve().parent.parent), 'run state outside Git')
    run(a.cover, a.work)
