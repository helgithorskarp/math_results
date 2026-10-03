"""Credited10084 initial original-domain ground replay only.
Extracted verbatim functions; no parent forest/negative corpus is loaded.
"""

from itertools import combinations
import hashlib
import importlib.util
import json
from pathlib import Path
PUBLIC=Path(__file__).resolve().parent
NUMERIC_SHA='83c79d716581cdc8f947a21d9120a001624d8179fab8935817e28326f10bb041'
DEAD=(4,5,6,7,9,10)

def need(ok, why):
    if not ok:
        raise ValueError(why)

def digest(x):
    return hashlib.sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()

def scalar(x, word):
    bits = [(x >> q) & 1 for q in range(13)]
    for a, b in word:
        bits[a], bits[b] = min(bits[a], bits[b]), max(bits[a], bits[b])
    return sum(bit << q for q, bit in enumerate(bits))

def initial_ground(prefix, early_entries):
    path = PUBLIC / 'numeric.py'
    need(hashlib.sha256(path.read_bytes()).hexdigest() == NUMERIC_SHA, 'credited numerical source changed')
    spec = importlib.util.spec_from_file_location('credited_numeric_initial_only', path)
    numeric = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(numeric)
    records, envelopes, assignments = {}, {}, 0
    for count, low in ((2, True), (2, False), (3, False)):
        original, groups = [], {}
        for ports in combinations(range(13), count):
            mask = sum(1 << q for q in ports)
            lo, hi = (mask, 0) if low else (0, mask)
            record, cube = numeric.follow(numeric.fresh_domain(lo, hi), prefix, 0)
            assignments += len(cube)
            original.append(record)
            tag = (record[2], record[3])
            groups[tag] = max(groups.get(tag, -1), record[4])
        name = f'{count}{"L" if low else "H"}'
        records[name], envelopes[name] = original, groups
    high = {q: envelopes['3H'].get((0, 6144 | (1 << q))) for q in DEAD}
    need(envelopes['2L'] == {(1 | (1 << q), 0): d for q, d in ((1, 7), (2, 7), (3, 7), (8, 6))},
         'fresh ordinary LOW ground changed')
    need(envelopes['2H'] == {(0, 6144): 9}, 'fresh held HIGH saturation changed')
    need(len(envelopes['3H']) == 6 and high == {4: 11, 5: 11, 6: 11, 7: 13, 9: 11, 10: 12},
         'fresh ordinary third-HIGH classes changed')
    checked = []
    for entry in early_entries:
        gate, w = entry['gate'], entry['witness']
        word = prefix + [gate]
        r = w['record']
        got, rows = numeric.follow(numeric.fresh_domain(*r[:2]), word, 0)
        need(got == r, 'actual early original record mismatch')
        k = 13 - (r[0] | r[1]).bit_count()
        need(k in (11, 12) and w['imported_size'] == {11: 35, 12: 39}[k], 'early bound changed')
        if w['kind'] == 'DIRECT_COST':
            need(r[4] + r[5] + w['imported_size'] > 44, 'early direct cost insufficient')
        else:
            need(w['kind'] == 'TIGHT_FREE_CUT' and r[4] + r[5] + w['imported_size'] == 44,
                 'early cut is not tight')
            q, x = w['physical_port'], w['full_Boolean_witness']
            need(all(v[q] in (0, 1) and all(v[t] <= v[q] if t < q else v[q] <= v[t]
                     for t in range(13) if t != q and v[t] in (0, 1)) for v in rows), 'early cut fails')
            actual, sorted_bit = scalar(x, word) >> q & 1, int(x.bit_count() >= 13 - q)
            need(actual == w['actual_bit'] and sorted_bit == w['sorted_bit'] and actual != sorted_bit,
                 'early scalar global rank witness fails')
        checked.append([gate, r, digest(rows)])
    return records, high, assignments, checked
