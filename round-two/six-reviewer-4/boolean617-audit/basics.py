"""Projection reduction, historical seed and finite diagnostic controls."""
import argparse
import copy
import hashlib
import json
from field import P, PROJECTIONS, bit, colors, cover, gauss, need, squares
from core import generate as core_generate, validate as core_validate
from interval import generate as interval_generate, validate as interval_validate

def foundation():
    table = gauss()
    need(table == squares(), 'Gauss / square oracle disagreement')
    starts = [a for a in range(P) if all((a+j) % P != 0 for j in range(7))]
    need(len(starts) == P-7, 'unit-step regular starts')
    need(all(len({table[(a+j) % P] for j in range(7)}) > 1 for a in starts), 'projection unit-step absence')
    rows = cover()
    need(len(rows) == 103 and sorted(map(len, rows)) == [3]+[6]*102, 'entire geometry partition')
    # A small genuinely different modulus: every nonzero-step seven-term AP
    # visits all of F7 and hits any prescribed root. The F617 classification
    # cannot be inferred merely from abstract symmetry/counts.
    p7_pairs = [(a, d) for a in range(7) for d in range(1, 7)]
    need(all(set((a+j*d) % 7 for j in range(7)) == set(range(7)) for a, d in p7_pairs), 'small-field positive control')
    # Every residue occurs in exactly seven of the P unit-step windows.
    incidences = [0]*P
    for a in range(P):
        for j in range(7):
            incidences[(a+j) % P] += 1
    need(set(incidences) == {7}, 'constant-core incidence proof control')
    return {'geometry_components': len(rows), 'geometry_sizes': {'3': 1, '6': 102},
            'projection_unit_step_starts': len(starts), 'projection_words': list(PROJECTIONS),
            'small_F7_all_pairs': len(p7_pairs), 'constant_core_min_free_columns': (P+6)//7}

def seed():
    table = gauss()
    values = [None]+[1 if n == 1 else (0 if (n-1) % P == 0 else table[(n-1) % P]) for n in range(1, 3704)]
    total = 0
    for d in range(1, 618):
        for a in range(1, 3704-6*d):
            value = values[a]
            need(any(values[a+j*d] != value for j in range(1, 7)), 'historical seed monochromatic AP')
            total += 1
    return {'historical_seed_length': len(values)-1, 'integer_APs_checked': total,
            'ascii_bits_sha256': hashlib.sha256(''.join(map(str, values[1:])).encode()).hexdigest()}

def reject(fn, data, reason):
    try:
        fn(data)
    except ValueError as error:
        need(reason in str(error), 'wrong rejection reason: '+str(error))
        return
    raise ValueError('semantic damage accepted: '+reason)

def controls():
    c = core_generate(2)
    need(core_validate(c, 2) == 125, 'valid core fixture')
    damages = []
    bad = copy.deepcopy(c); bad['witnesses'].pop()
    reject(lambda z: core_validate(z, 2), bad, 'entire truth domain'); damages.append('missing rule')
    bad = copy.deepcopy(c); bad['witnesses'][0][1] = 0
    reject(lambda z: core_validate(z, 2), bad, 'all original roots'); damages.append('ignored root hit')
    bad = copy.deepcopy(c); bad['witnesses'][0][2] = 0
    reject(lambda z: core_validate(z, 2), bad, 'field AP coordinates'); damages.append('zero step')
    bad = copy.deepcopy(c); bad['t'] = 3
    reject(lambda z: core_validate(z, 2), bad, 'geometry identity'); damages.append('wrong geometry')
    u = interval_generate(0)
    need(interval_validate(u, 0) == 21, 'valid unit fixture')
    bad = copy.deepcopy(u); bad['cases'].pop()
    reject(lambda z: interval_validate(z, 0), bad, 'physical projection coverage'); damages.append('missing physical projection')
    bad = copy.deepcopy(u); bad['cases'][0]['units'].pop()
    reject(lambda z: interval_validate(z, 0), bad, 'seven independent occurrences'); damages.append('missing free occurrence')
    bad = copy.deepcopy(u); bad['cases'][0]['units'][0][3] = (bad['cases'][0]['units'][0][3]+1) % 7
    reject(lambda z: interval_validate(z, 0), bad, 'target occurrence identity'); damages.append('wrong target slot')
    bad = copy.deepcopy(u); bad['cases'][0]['units'][0][2] = 3704
    reject(lambda z: interval_validate(z, 0), bad, 'integer AP bounds'); damages.append('outside actual interval')
    m = u['cases'][0]['units'][0][0]
    bad = copy.deepcopy(u); bad['cases'][0]['units'][0] = [m, m, P, 0]
    reject(lambda z: interval_validate(z, 0), bad, 'six fixed supports'); damages.append('support hits another original root')
    # Search only for a diagnostic invalid-color fixture, never a theorem premise.
    diagnostic = None
    table = squares()
    color = table[(u['cases'][0]['column']-u['cases'][0]['root']) % P]
    for d in range(2, 100):
        support = [m+j*d for j in range(1, 7)]
        if all(n % P not in (1, 2, 0) for n in support) and any(table[(n-u['cases'][0]['root']) % P] != 1-color for n in support):
            diagnostic = [m, m, d, 0]
            break
    need(diagnostic is not None, 'opposing color damage fixture')
    bad = copy.deepcopy(u); bad['cases'][0]['units'][0] = diagnostic
    reject(lambda z: interval_validate(z, 0), bad, 'six opposing literal colors'); damages.append('support has wrong fixed color')
    reject(lambda z: bit(2, z), [None, 0, 1], 'undefined character'); damages.append('undefined character zero')
    return {'valid_core_rules': 125, 'valid_physical_units': 21, 'semantic_damages_rejected': damages}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['foundation', 'seed', 'controls'])
    args = parser.parse_args()
    print(json.dumps(globals()[args.action](), sort_keys=True))
