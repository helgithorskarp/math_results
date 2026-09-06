#!/usr/bin/env python3
"""Exact three-large/six-small family from all durable positive colourings."""
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('large2_engine', HERE.parent/'hadwiger_nelson_heule517_large2_pilot/engine.py')
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
E = R.E


def inputs():
    data, rows = R.inputs()
    data['large2_rows'] = json.loads((R.HERE/'certificate.json').read_text())['rows']
    for i,row in enumerate(data['large2_rows']):
        assert list(E.P.check_colouring(row['colouring'],data['edges'])) == row['D']
        rows.append(dict(kind='large2',index=i,D=row['D']))
    assert len(rows) == 814
    minimal = []
    for row in sorted(rows,key=lambda r:(len(r['D']),r['D'])):
        if not any(set(q['D']) <= set(row['D']) for q in minimal): minimal.append(row)
    assert len(minimal) == 571
    return data, minimal


def decode(row,data):
    if row['kind'] == 'large2': return data['large2_rows'][row['index']]['colouring']
    return R.decode(row,data)


def code(triple):
    a,b,c = triple; return a*517**2+b*517+c


def uncode(value):
    a,rem = divmod(value,517**2); b,c = divmod(rem,517); return (a,b,c)


def family(data,rows):
    S = set(data['small']); L = set(data['large'])
    forced = {r['D'][0] for r in rows if len(r['D']) == 1}
    free = sorted(S-forced); assert len(forced) == 397 and len(free) == 16
    cuts = [sum(1 << v for v in r['D']) for r in rows if set(r['D']) <= S]
    states = []; count = 0
    for O in combinations(free,6):
        count += 1; om = sum(1 << v for v in O)
        if any(om & d == d for d in cuts): continue
        os = set(O); forbidden = set(); forbidden_pairs = []
        for row in rows:
            d = set(row['D']); dl = d & L
            if d & S <= os:
                if len(dl) == 1: forbidden.update(dl)
                elif len(dl) == 2: forbidden_pairs.append(dl)
                else: assert not dl
        eligible = sorted(L-forbidden)
        remaining = {code(t) for t in combinations(eligible,3) if not any(p <= set(t) for p in forbidden_pairs)}
        states.append(dict(small_omitted=list(O),mask=om,remaining=remaining))
    assert count == 8008 and len(states) == 38
    assert sum(len(s['remaining']) for s in states) == 749066
    return states


def apply_cut(states,row,small):
    D = set(row['D']); ds = sum(1 << v for v in D & small); dl = D-small
    assert len(dl) <= 3
    for state in states:
        if state['mask'] & ds == ds:
            if not dl: state['remaining'].clear()
            else: state['remaining'] = {x for x in state['remaining'] if not dl <= set(uncode(x))}
