#!/usr/bin/env python3
"""Physical fixed-word audit, independent of the producer's profile filtering."""
from collections import Counter
from itertools import product
from pathlib import Path
import copy
import importlib.util

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('physical_attachment_audit', ROOT.parent / 'ramsey_r55_order3_eleven_core194_attachments/audit.py')
physical = importlib.util.module_from_spec(spec); spec.loader.exec_module(physical)
need = physical.need


def expected():
    hist = Counter(); permutations = set(); raw = 0
    ids = physical.primary()
    for word in product(range(3), repeat=8):
        raw += 1
        # Six RR moving triangles, one BR moving triangle, blue empty pair/core.
        red_u = 18 + sum(t != 2 for t in word)
        red_v = 21 + sum(t != 1 for t in word)
        if red_u not in range(18, 25) or red_v not in range(18, 25):
            continue
        counts = tuple(word.count(t) for t in range(3)); hist[counts] += 1
        order = sorted(range(8), key=lambda i: word[i]); p = list(range(43))
        for new, old in enumerate(order): p[35 + old] = 35 + new
        physical.check_permutation(p, ids)
        transported = [None] * 8
        for old, t in enumerate(word): transported[p[35 + old] - 35] = t
        need(transported == sorted(word), 'fixed contact sorting')
        permutations.add(tuple(p))
    need(raw == 6561 and sum(hist.values()) == 252, 'full fixed-word census')
    rows = []
    for (x,y,z), weight in sorted(hist.items()):
        counts = [6,0,1,x,y,z]
        rows.append(dict(counts=counts, red_degrees=[18+x+y,21+x+z],
            labeled_assignments=14*weight, units=physical.normalized_units(counts, True)))
    need(len(rows) == 3, 'three complete fixed profiles')
    return rows, dict(fixed_words=raw, allowed_fixed_words=sum(hist.values()),
        normalized_profiles=len(rows), distinct_sorting_permutations=len(permutations),
        physical_units_checked=30*len(rows), labeled_full_star_weight=14*sum(hist.values()))


def verify(rows, wanted):
    need(rows == wanted, 'complete entrywise physical three-profile certificate')


def controls(rows, wanted):
    rejected=[]
    for name in ('missing_profile','duplicate_profile','wrong_fixed_count','wrong_moving_count',
                 'wrong_degree','wrong_weight','wrong_fixed_unit','wrong_moving_unit'):
        bad=copy.deepcopy(rows)
        if name=='missing_profile': bad.pop()
        elif name=='duplicate_profile': bad.append(copy.deepcopy(bad[0]))
        elif name=='wrong_fixed_count': bad[0]['counts'][3]+=1
        elif name=='wrong_moving_count': bad[0]['counts'][0]-=1
        elif name=='wrong_degree': bad[0]['red_degrees'][0]-=1
        elif name=='wrong_weight': bad[0]['labeled_assignments']+=1
        elif name=='wrong_fixed_unit': bad[0]['units'][-1]*=-1
        elif name=='wrong_moving_unit': bad[0]['units'][0]*=-1
        try: verify(bad,wanted)
        except ValueError: rejected.append(name)
        else: raise ValueError('accepted '+name)
    return rejected
