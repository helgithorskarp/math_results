#!/usr/bin/env python3
"""Exact finite two-large/seven-small family and inherited positive witnesses."""
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('small134', HERE.parent/'hadwiger_nelson_heule517_small134/engine.py')
Q = importlib.util.module_from_spec(spec); spec.loader.exec_module(Q)
E = Q.E


def inputs():
    data = E.inputs(); initial = Q.initial(data)
    cert = json.loads((Q.HERE/'certificate.json').read_text())
    small = [(initial if k == 'initial' else cert['new_rows'])[i] for k,i in cert['final_rows']]
    rows = []
    for i,row in enumerate(data['prior_rows']):
        colour = E.P.decode(row, data); assert list(E.P.check_colouring(colour, data['edges'])) == row['D']
        rows.append(dict(kind='prior', index=i, D=row['D']))
    for i,row in enumerate(small):
        E.checked(row, data); rows.append(dict(kind='small134', index=i, D=row['D']))
    data['small_rows'] = small
    return data, rows


def decode(row, data):
    if row['kind'] == 'prior': return E.P.decode(data['prior_rows'][row['index']], data)
    if row['kind'] == 'small134': return E.full_colour(data['small_rows'][row['index']], data)
    assert row['kind'] == 'native'; return row['colouring']


def family(data, rows):
    S = set(data['small']); L = set(data['large'])
    small_rows = [r for r in rows if r['kind'] == 'small134']
    forced = {r['D'][0] for r in small_rows if len(r['D']) == 1}
    free = sorted(S-forced); pos = {v:i for i,v in enumerate(free)}
    cuts = [sum(1 << pos[v] for v in r['D']) for r in small_rows if not set(r['D']) & forced]
    states = []; count = 0
    for indices in combinations(range(len(free)), 7):
        count += 1; mask = sum(1 << i for i in indices)
        if any(mask & d == d for d in cuts): continue
        O = {free[i] for i in indices}; forbidden = set()
        for row in rows:
            D = set(row['D']); dl = D & L
            if dl and D & S <= O:
                assert len(dl) == 1; forbidden.update(dl)
        eligible = sorted(L-forbidden)
        states.append(dict(small_omitted=sorted(O), mask=sum(1 << v for v in O),
                           remaining={517*u+v for u,v in combinations(eligible, 2)}))
    assert count == 170544 and len(states) == 167
    assert sum(len(s['remaining']) for s in states) == 870215
    return states


def apply_cut(states, row, small):
    D = set(row['D']); ds = sum(1 << v for v in D & small); dl = sorted(D-small)
    assert len(dl) <= 2
    for state in states:
        if state['mask'] & ds != ds: continue
        if not dl: state['remaining'].clear()
        elif len(dl) == 1:
            v = dl[0]; state['remaining'] = {x for x in state['remaining'] if v not in divmod(x,517)}
        else: state['remaining'].discard(517*dl[0]+dl[1])
