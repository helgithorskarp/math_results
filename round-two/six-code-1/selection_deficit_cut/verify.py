"""Exact definition-level validation of the ordinary selection cuts.

This is not an ambient packing enumeration or a formal proof. The theorem
imports the explicit local9249 and universal8323 premises in PROOF.md.
"""
from collections import Counter
import copy
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BASELINE_SHA = 'cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def baseline(raw):
    lines = raw.decode().splitlines()
    need(len(lines) == 69 and len(set(lines)) == 69, 'baseline word population')
    need(all(len(s) == 18 and set(s) <= {'0', '1'} and s.count('1') == 5 for s in lines),
         'baseline length, alphabet or weight')
    words = [tuple(i for i, c in enumerate(s) if c == '1') for s in lines]
    need(all(len(set(a) & set(b)) <= 2 for a, b in itertools.combinations(words, 2)),
         'baseline word collision')
    triples = [t for word in words for t in itertools.combinations(word, 3)]
    need(len(triples) == len(set(triples)) == 690, 'baseline triple ownership')
    return words


def charge_graphs():
    records = []
    total = 0
    for h in range(1, 6):
        pairs = list(itertools.combinations(range(h), 2))
        minima = {k: None for k in range(h+1)}
        for edges in itertools.combinations(pairs, h-1):
            for bits in range(1 << h):
                hubs = {i for i in range(h) if bits >> i & 1}
                k = len(hubs)
                q = sum(a in hubs or b in hubs for a, b in edges)
                if k:
                    need(q >= k-1, 'elementary hub charge fails')
                if h == 5 and k >= 2:
                    need(q >= 1, 'unit positive-hub non-singleton has zero charge')
                minima[k] = q if minima[k] is None else min(minima[k], q)
                total += 1
        records.append(dict(h=h, minima=[minima[k] for k in range(h+1)]))
    return dict(all_enlarged_graph_and_hub_placements=total, records=records,
                classification_imported=False)


def homogeneous_control(words):
    masks = [sum(1 << p for p in word) for word in words]
    degrees = Counter(p for word in words for p in word)
    pairs = Counter(t for word in words for t in itertools.combinations(word, 2))
    covered = {t for word in words for t in itertools.combinations(word, 3)}
    unowned = [sum(1 << p for p in t) for t in itertools.combinations(range(18), 3) if t not in covered]
    records = []
    counts = Counter()
    for m in range(1, 6):
        for hubs in itertools.combinations(range(18), m):
            hmask = sum(1 << p for p in hubs)
            r_h = sum(degrees[p] for p in hubs)
            p_h = sum(pairs[t] for t in itertools.combinations(hubs, 2))
            t_h = sum(t in covered for t in itertools.combinations(hubs, 3))
            actual = sum(not (t & hmask) for t in unowned)
            expected = comb(18-m, 3)-10*len(words)+6*r_h-3*p_h+t_h
            need(actual == expected, 'literal homogeneous-triple identity fails')
            js = [(word & hmask).bit_count() for word in masks]
            need(sum(js) == r_h and sum(comb(j, 2) for j in js) == p_h
                 and sum(comb(j, 3) for j in js) == t_h, 'word ownership statistics fail')
            records.append([list(hubs), r_h, p_h, t_h, actual])
            counts[m] += 1
    return dict(primary69_positive_control_only=True, hub_subsets=len(records),
                counts_by_size=dict(counts), whole_record_sha256=hashlib.sha256(encode(records)).hexdigest())


def weighted_rows():
    checked = 0
    for h in range(1, 6):
        for cuts in itertools.combinations(range(1, 5), h-1):
            endpoints = (0,)+cuts+(5,)
            delta = [b-a for a, b in zip(endpoints, endpoints[1:])]
            e = 5-h
            for bits in range(1 << h):
                k = bits.bit_count()
                g = h-k
                ss_excess = sum(d-1 for i, d in enumerate(delta) if not (bits >> i & 1))
                if e:
                    need(g <= 3*e+ss_excess, 'nonunit degree-excess capacity fails')
                    if not k:
                        need(ss_excess == e and ss_excess >= 1, 'unmarked nonunit bulk source fails')
                    else:
                        need(g <= 3, 'marked nonunit degree capacity fails')
                checked += 1
    return dict(all_ordered_positive_deficit_and_hub_placements=checked,
                exact_partition_weight=5)


def tables():
    out = []
    for m in range(1, 6):
        n = 18-m
        w = 20+10*m-5*m*m
        b = 4*n-comb(n, 3)-120*m+740
        c = 8*w-19*b
        out.append(dict(m=m, n=n, W_constant=w, B_constant=b, cut_constant=c,
                        preliminary_P_lower=(c+40)//41, final_P_lower=(None, 3, 8, 19, 34)[m-1]))
    need([r['cut_constant'] for r in out] == [48, 84, 325, 752, 1346], 'exact cut constants differ')
    for j in range(6):
        need(comb(5-j, 3) == 10-6*j+3*comb(j, 2)-comb(j, 3), 'binomial word identity fails')
    return out


def boundary(m, p):
    n = 18-m
    w = 20+10*m-5*m*m+2*p
    b = 4*n-comb(n, 3)-120*m+740+3*p
    before, after = [], []
    for t in range(comb(m, 3)+1):
        budget = b-t
        if budget < 0:
            continue
        for tau in range(budget//2+1):
            for e in range(min(4*n, budget-2*tau)+1):
                q = budget-2*tau-e
                for x in range(e//2+1):
                    if 8*e+11*q < 4*w or 11*e+8*q < 4*w+6*x:
                        continue
                    z_lower = w-2*(e+q)+2*x
                    record = dict(T=t, X=x, tau=tau, E=e, Q=q, Z_lower=z_lower)
                    before.append(record)
                    if e < 4 and z_lower > 0:
                        continue  # An actual unit singleton has four distinct neighbors.
                    after.append(record)
    return dict(m=m, P=p, necessary_arithmetic_before_unit_partner=before,
                necessary_arithmetic_after_unit_partner=after,
                actual_packings_enumerated=False)


def controls(raw):
    lines = raw.decode().splitlines()
    damaged = [lines[:-1], [lines[0]]+lines[2:]+[lines[0]],
               [lines[0]+'0']+lines[1:]]
    bad = copy.deepcopy(lines)
    i = bad[0].index('1');bad[0] = bad[0][:i]+'0'+bad[0][i+1:];damaged.append(bad)
    for rows in damaged:
        try:
            baseline(('\n'.join(rows)+'\n').encode())
        except ValueError:
            continue
        raise ValueError('damaged primary positive control accepted')
    # Enlarged unit leaves really allow q=1 at two hub marks. The proof
    # intentionally uses q>=k-1 and does not import the stronger catalog cut.
    edges = ((0, 1), (0, 2), (1, 2), (3, 4))
    need(sum(a in {3, 4} or b in {3, 4} for a, b in edges) == 1,
         'positive enlarged two-hub charge control differs')
    return dict(rejected_primary_damages=len(damaged), enlarged_q1_positive_control=True)


def compute():
    raw = (ROOT/'BASELINE69.txt').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BASELINE_SHA, 'credited primary fixture pin differs')
    words = baseline(raw)
    branches = [boundary(m, p) for m, p in ((2, 2), (3, 7), (3, 8), (4, 18), (5, 32), (5, 33))]
    three = next(r for r in branches if (r['m'], r['P']) == (3, 8))
    need(three['necessary_arithmetic_after_unit_partner'] ==
         [dict(T=0, X=0, tau=0, E=4, Q=5, Z_lower=3),
          dict(T=0, X=0, tau=0, E=5, Q=4, Z_lower=3)], 'P8 frontier differs')
    five = next(r for r in branches if (r['m'], r['P']) == (5, 33))
    need([r['E'] for r in five['necessary_arithmetic_before_unit_partner']] == [2, 3]
         and not five['necessary_arithmetic_after_unit_partner'], 'P33 partner refinement differs')
    return dict(actual_agent='six-code-1', role='researcher',
                scope='Exact arithmetic and definition-level validation of ordinary cuts; no packing census or formalized bridge.',
                charge_graphs=charge_graphs(), weighted_rows=weighted_rows(),
                tables=tables(), boundary_cases=branches,
                homogeneous_identity=homogeneous_control(words), controls=controls(raw))


def main():
    result = compute()
    expected = json.loads((ROOT/'EXPECTED.json').read_text())
    need(encode(result) == encode(expected), 'frozen exact mathematical readout differs')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
