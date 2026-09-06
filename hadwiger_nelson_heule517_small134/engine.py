#!/usr/bin/env python3
"""Frozen eight-omission survivor generator; prior graph and positive witnesses."""
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('small133_engine', HERE.parent/'hadwiger_nelson_heule517_small_pilot/engine.py')
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


def initial(data):
    rows = json.loads((E.HERE/'certificate.json').read_text())['rows']
    assert len(rows) == 206
    for row in rows: E.checked(row, data)
    return rows


def survivors(rows, small):
    forced = {r['D'][0] for r in rows if len(r['D']) == 1}
    free = sorted(set(small)-forced)
    assert len(forced) == 119 and len(free) == 23
    pos = {v:i for i,v in enumerate(free)}
    masks = [sum(1 << pos[v] for v in r['D']) for r in rows if not set(r['D']) & forced]
    out = []; count = 0
    for indices in combinations(range(len(free)), 8):
        count += 1
        omitted = sum(1 << i for i in indices)
        if not any(omitted & m == m for m in masks):
            out.append([free[i] for i in indices])
    assert count == 490314 and len(out) == 195
    return out
