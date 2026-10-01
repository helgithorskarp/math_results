"""Exact original-face cover, profile(1,5,0), F-U contact.
six-tammes-1, researcher. Written bridges/imported7912 collar: PROOF.md.
Only the hash-guarded prior PUBLIC8180 kernel is imported.
"""
from pathlib import Path
from collections import Counter
from itertools import combinations
import hashlib, importlib.util, json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tammes15_ordinary_five_four_one_exclusion/check.py'
if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != '2d543e31857e3a64d31e9306617ac7fb3e20cd3f7605941f1d96c5306d579c86':
    raise RuntimeError('Published8180 kernel changed')
loader = importlib.util.spec_from_file_location('published8180', SOURCE)
k = importlib.util.module_from_spec(loader)
loader.loader.exec_module(k)
ANCHORS = ('F', 'U', 'X', 'R', 'S', 'Z', 'B', 'C')
CORE = (('F', 'X', 'R'), ('F', 'R', 'S'), ('F', 'S', 'Z'),
        ('F', 'Z', 'C', 'U'), ('F', 'U', 'B', 'X'), ('U', 'C', 'Y', 'B'),
        ('R', 'L', 'K', 'S'), ('R', 'X', 'P', 'L'), ('S', 'K', 'Q', 'Z'))
TABLE = {
    'X1Z1': (('E',), ('B', 'C', 'X', 'Z', 'E')),
    'X1Z2': (('E', 'G'), ('B', 'C', 'X', 'E', 'G')),
    'X2Z1': (('E', 'G'), ('B', 'C', 'Z', 'E', 'G')),
}

def schema(case):
    extra, ones = TABLE[case]
    originals = ANCHORS + extra
    names = originals + ('Y', 'L', 'K', 'P', 'Q')
    words = CORE
    if 'X' in ones:
        names += ('AX',)
        words += (('X', 'B', 'AX', 'P'),)
    else:
        words += (('X', 'B', 'P'),)
    if 'Z' in ones:
        names += ('AZ',)
        words += (('Z', 'Q', 'AZ', 'C'),)
    else:
        words += (('Z', 'Q', 'C'),)
    number = {n: i for i, n in enumerate(names)}
    if len(ones) != 5 or len(names) != 16:
        raise RuntimeError('Wrong deficient-five original-face cover')
    return {'case': case, 'names': names, 'words': words, 'number': number,
            'faces': tuple(tuple(number[n] for n in w) for w in words),
            'mode': 'full', 'maxima': {'F': 3},
            'exact': {'F': 3, 'U': 0, **{n: 1 for n in ones}},
            'distinct': (), 'initial': tuple(range(len(originals))),
            'contact_edges': ((0, 1), (1, number['B']), (1, number['C']))}

old_necessary = k.necessary
def necessary(labels, spec):
    if max(labels) + 1 > 15:
        return 'more_than_fifteen_actual_points'
    return old_necessary(labels, spec)
k.necessary = necessary

def ordinary_stars(prefix, spec):
    roles = {n: k.triangle_role(prefix, spec, n) for n in ('L', 'K')}
    names, words = spec['names'], spec['words']
    for n in ('L', 'K'):
        if roles[n] not in (0, 1, 2):
            raise RuntimeError('Unclassified ordinary strip original')
        if roles[n] != 2:
            continue
        h = 'H' + n
        names += (h,)
        if n == 'L':
            words += (('L', h, 'K'), ('L', 'P', h))
        else:
            words += (('K', h, 'Q'), ('K', 'L', h))
    full = dict(spec, names=names, words=words)
    full['number'] = {n: i for i, n in enumerate(names)}
    full['faces'] = tuple(tuple(full['number'][n] for n in w) for w in words)
    return roles, full

def serializable_spec(spec):
    return {n: spec[n] for n in ('case', 'names', 'words', 'exact', 'maxima', 'initial', 'contact_edges')}

def controls():
    results = {}
    for case in TABLE:
        s = schema(case)
        if necessary(s['initial'], s) is not None:
            raise RuntimeError('Three-T F-star positive control rejected')
        wrong = dict(s, exact=dict(s['exact'], F=4), maxima={})
        if necessary(s['initial'], wrong) != 'excess_quadrilateral_corners':
            raise RuntimeError('Wrong four-T F role was accepted')
        results[case] = {'F_three_T_positive': True, 'F_four_T_negative': True,
                         'all_five_one_T_originals_assigned_first': True, 'positions': len(s['names'])}
    return results

def run():
    trace, ledger = [], []
    totals = Counter()
    def record(stage, spec, initial=None):
        r = k.cover(spec, initial)
        trace.append({'stage':stage,'spec':serializable_spec(spec),'initial':initial,'cover':r})
        totals['covers'] += 1
        totals['nodes'] += r['nodes']
        totals[stage+'_covers'] += 1
        totals[stage+'_nodes'] += r['nodes']
        totals[stage+'_survivors'] += len(r['survivors'])
        return r
    def recurse(prefix,spec,depth=0):
        if depth > 12: raise RuntimeError('INCOMPLETE: fixed12forcingdepth')
        if k.one_T_U_obstruction(prefix,spec):
            totals['one_T_U_cuts'] += 1
            return
        forced = k.force_last_face(prefix,spec)
        if forced is None: raise RuntimeError('A contact terminal patch survives')
        for p in record('forced_last_face',forced[3],prefix)['survivors']:
            recurse(p,forced[3],depth+1)
    cs = controls()
    for case in TABLE:
        spec=schema(case);r=record('original_face',spec)
        roles_seen=Counter()
        before=totals['covers'];before_nodes=totals['nodes']
        for prefix in r['survivors']:
            if k.one_T_U_obstruction(prefix,spec):
                totals['early_one_T_U_cuts']+=1
                continue
            roles,full=ordinary_stars(prefix,spec)
            roles_seen[tuple(roles[n] for n in ('L','K'))]+=1
            for p in record('ordinary_strip_stars',full,prefix)['survivors']:
                recurse(p,full)
        ledger.append({'case':case,'base_nodes':r['nodes'],'base_survivors':len(r['survivors']),
                       'L_K_roles':{str(x):n for x,n in sorted(roles_seen.items())},
                       'extension_covers':totals['covers']-before,
                       'extension_nodes':totals['nodes']-before_nodes})
    return {'status':'CONTACT_CASE_EXCLUDED','controls':cs,'ledger':ledger,
            'counts':dict(sorted(totals.items()))},trace
