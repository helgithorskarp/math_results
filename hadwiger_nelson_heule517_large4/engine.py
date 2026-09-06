#!/usr/bin/env python3
"""Exact four-large/five-small family from durable positive witnesses."""
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('large3_engine', HERE.parent/'hadwiger_nelson_heule517_large3/engine.py')
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
E = R.E


def inputs():
    data, rows = R.inputs()
    data['large3_rows'] = json.loads((R.HERE/'certificate.json').read_text())['rows']
    for i,row in enumerate(data['large3_rows']):
        assert list(E.P.check_colouring(row['colouring'],data['edges'])) == row['D']
        rows.append(dict(kind='large3',index=i,D=row['D']))
    minimal = []
    for row in sorted(rows,key=lambda r:(len(r['D']),r['D'])):
        if not any(set(q['D']) <= set(row['D']) for q in minimal): minimal.append(row)
    assert len(minimal) == 584
    return data, minimal


def decode(row,data):
    if row['kind'] == 'large3': return data['large3_rows'][row['index']]['colouring']
    return R.decode(row,data)


def code(vertices):
    n = 0
    for v in vertices: n = 517*n+v
    return n


def uncode(n):
    out = []
    for _ in range(4): n,v = divmod(n,517); out.append(v)
    assert n == 0
    return tuple(reversed(out))


def family(data,rows):
    S = set(data['small']); L = set(data['large'])
    forced = {r['D'][0] for r in rows if len(r['D']) == 1}
    free = sorted(S-forced); assert len(forced) == 467 and len(free) == 15
    cuts = [sum(1 << v for v in r['D']) for r in rows if set(r['D']) <= S]
    states = []; count = 0
    for O in combinations(free,5):
        count += 1; om = sum(1 << v for v in O)
        if any(om & d == d for d in cuts): continue
        os = set(O); forbidden = set(); bad = []
        for row in rows:
            d = set(row['D']); dl = d & L
            if d & S <= os:
                if len(dl) == 1: forbidden.update(dl)
                elif 2 <= len(dl) <= 3: bad.append(dl)
                else: assert not dl
        eligible = sorted(L-forbidden)
        remaining = {code(q) for q in combinations(eligible,4) if not any(d <= set(q) for d in bad)}
        states.append(dict(small_omitted=list(O),mask=om,remaining=remaining))
    assert count == 3003 and len(states) == 94
    assert sum(len(s['remaining']) for s in states) == 31695
    return states


def apply_cut(states,row,small):
    D = set(row['D']); ds = sum(1 << v for v in D & small); dl = D-small
    assert len(dl) <= 4
    for state in states:
        if state['mask'] & ds == ds:
            if not dl: state['remaining'].clear()
            else: state['remaining'] = {x for x in state['remaining'] if not dl <= set(uncode(x))}
