#!/usr/bin/env python3
"""Focused independent semantic controls and all hole-count correlation classes."""
from pathlib import Path
from copy import deepcopy
from math import gcd
import argparse, json

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def inverse(z):
    need(z['points'] == list(range(1, 103)), 'literal field-coordinate domain')
    cols = [int(s, 16) for s in z['inverse_columns_hex']]
    need(len(cols) == 102 and all(0 <= x < 1 << 102 for x in cols), 'whole inverse domain')
    for k in range(1, 103):
        row = {(k*s) % 103 for s in range(80, 87)}
        for j, col in enumerate(cols, 1):
            need(sum((col >> (r-1)) & 1 for r in row) % 2 == (k == j), 'actual right product')

def orbit_size(z):
    seed = z['syndrome_logs']
    orbit = {tuple(sorted((x+t) % 102 for x in seed)) for t in range(102)}
    need(z['orbit_size'] == len(orbit), 'actual translation orbit size')

def lift(step, unit):
    need(step > 0 and (not unit or gcd(step, 618) == 1), 'nonconstant/unit lift')

def reject(name, validator, damaged):
    try:
        validator(damaged)
    except RuntimeError:
        return name
    raise RuntimeError('semantic damage accepted: ' + name)

def main():
    p = argparse.ArgumentParser(); p.add_argument('--work', type=Path, required=True); a = p.parse_args()
    z = json.loads((a.work/'INVERSE.json').read_bytes()); inverse(z)
    records = []
    bad = deepcopy(z); bad['inverse_columns_hex'][0] = format(int(bad['inverse_columns_hex'][0],16)^1,'x')
    records.append(reject('one actual inverse bit', inverse, bad))
    bad = deepcopy(z); bad['inverse_columns_hex'].pop()
    records.append(reject('missing actual column', inverse, bad))
    bad = deepcopy(z); bad['points'][0],bad['points'][1] = bad['points'][1],bad['points'][0]
    records.append(reject('changed literal field ordering', inverse, bad))
    registry = json.loads((a.work/'GAP_ORBITS.json').read_bytes())
    short = [x for x in registry if x['orbit_size'] != 102]
    need(len(short) == 1, 'unique short orbit'); orbit_size(short[0])
    bad = deepcopy(short[0]); bad['orbit_size'] = 102
    records.append(reject('naive 102-fold short-orbit multiplicity', orbit_size, bad))
    records.append(reject('nonunit affine CRT step103', lambda s:lift(s,True),103))
    records.append(reject('zero integer AP step', lambda s:lift(s,False),0))
    lift(307,True); lift(309,False)
    witness = json.loads((a.work/'MINIMUM_PARITY_WORD.json').read_bytes())
    points = witness['candidate_points']; syndrome = set(witness['syndrome_points'])
    need(len(points) == len(set(points)) == 35 and set(points) <= set(range(1,103)), 'actual minimum parity word')
    hits = [len(set(points) & {(k*s)%103 for s in range(80,87)}) for k in range(1,103)]
    need(all(hits[k-1] % 2 == (1 ^ (k in syndrome)) for k in range(1,103)), 'entire actual minimum-word syndrome')
    masks = []; comparisons = 0
    for h in range(4):
        for delta in range(2):
            if delta > h: continue
            e = h-delta; m = 102-e; bound = 70+e
            for d in range(m+1):
                need((16-e <= d <= 86) == (abs(m-2*d) <= bound), 'every integer distance/correlation equivalence')
                comparisons += 1
            masks.append({'holes':h,'root_is_hole':delta,'other_holes':e,'compared_positions':m,'minimum_distance':16-e,'maximum_distance':86,'absolute_correlation_bound':bound})
    need(len(masks) == 7 and comparisons == 712, 'whole hole-count domain')
    print(json.dumps({'complete':True,'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','author_code_imported':False,'semantic_damages_rejected':records,'valid_unit_and_repeated_modular_lifts_accepted':True,'minimum_parity_word_whole102_syndrome_checked':True,'minimum_word_is_claimed_as_repair':False,'hole_classes':masks,'all_integer_distance_comparisons':comparisons,'short_orbit_naive_overcount':68},sort_keys=True))

if __name__ == '__main__': main()
