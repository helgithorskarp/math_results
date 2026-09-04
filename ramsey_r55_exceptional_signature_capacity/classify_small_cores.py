#!/usr/bin/env python3
"""Exact marginal signature-capacity sieve, at most six exceptional vertices.

Standard-library Python; deterministic stdout, no file writes or solver.
Survivors satisfy only necessary marginal bounds, not full feasibility.
"""

import argparse
from collections import Counter
import csv
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'ramsey_r55_exceptional_degree_sieve/PROFILES.tsv'
INPUT_HASH = 'a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa'
B = {18:220, 19:221, 20:220, 21:220, 22:221, 23:223, 24:223}
MAX_EXCEPTIONAL = 6
FIELDS = ('counts_18_to_24', 'M', 'k', 'split_count', 'raw_cores',
          'weighted', 'core5', 'total_capacity', 'red_capacity',
          'blue_capacity', 'pass', 'first_mask')


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def input_rows():
    require(sha256(INPUT.read_bytes()).hexdigest() == INPUT_HASH, 'input hash')
    with INPUT.open() as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    require(len(rows) == 104, '104 input rows')
    survivors = [row for row in rows if row['status'] == 'feasible']
    require(len(survivors) == 88, '88 aggregate survivors')
    for row in survivors:
        counts = tuple(map(int, row['counts_18_to_24'].split(',')))
        ds = tuple(d for d, n in zip(range(18,25), counts) if d != 21 for _ in range(n))
        yield row, ds


def signature_caps(adj, ds, M):
    k = len(ds)
    full, n = (1 << k)-1, 43-k
    omega, alpha, weight = ([0]*(1 << k) for _ in range(3))
    for x in range(1, 1 << k):
        bit = x & -x
        i, rest = bit.bit_length()-1, x ^ bit
        omega[x] = max(omega[rest], 1+omega[rest & adj[i]])
        alpha[x] = max(alpha[rest], 1+alpha[rest & ~adj[i]])
        weight[x] = weight[rest]+ds[i]-21
    if max(omega[full], alpha[full]) >= 5:
        return None
    answer = {}
    for x in range(1 << k):
        if weight[x] > M-220:
            continue
        r, s = omega[x], alpha[full ^ x]
        if max(r,s) >= 4:
            continue
        answer[x] = min(n, comb(8-r-s, 4-r)-1)
    return answer


def screen(adj, ds, M):
    caps = signature_caps(adj, ds, M)
    if caps is None:
        return {'reason':'core5'}
    n = 43-len(ds)
    available = sum(caps.values())
    if available < n:
        return {'reason':'total_capacity', 'available':available, 'required':n}
    for i, d in enumerate(ds):
        red_demand = d-adj[i].bit_count()
        require(0 <= red_demand <= n, 'exceptional-to-central degree range')
        red_cap = sum(c for x,c in caps.items() if x >> i & 1)
        if red_cap < red_demand:
            return {'reason':'red_capacity', 'vertex':i, 'available':red_cap, 'required':red_demand}
        blue_cap = sum(c for x,c in caps.items() if not (x >> i & 1))
        if blue_cap < n-red_demand:
            return {'reason':'blue_capacity', 'vertex':i, 'available':blue_cap, 'required':n-red_demand}
    return {'reason':'pass'}


def census(ds, M):
    k = len(ds)
    edges = list(combinations(range(k),2))
    eps = [d-21 for d in ds]
    lower = sum(d*e for d,e in zip(ds,eps))-(43-k)*(M-220)
    hist, blocks, first = Counter(), [], None
    for mask in range(1 << len(edges)):
        adj, sums = [0]*k, [0]*k
        for bit, (i,j) in enumerate(edges):
            if mask >> bit & 1:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
                sums[i] += eps[j]
                sums[j] += eps[i]
        if any(s > M-B[d] for s,d in zip(sums,ds)) or sum(sums) < lower:
            continue
        hist['weighted'] += 1
        result = screen(adj,ds,M)
        hist[result['reason']] += 1
        if result['reason'] == 'pass':
            if first is None:
                first = mask
        else:
            blocks.append({'red_mask':mask, **result})
    return hist, first, blocks


def compute():
    table, rejections, totals = [], [], Counter()
    removed_splits = 0
    for row, ds in input_rows():
        if len(ds) > MAX_EXCEPTIONAL:
            continue
        M, k = int(row['M']), len(ds)
        hist, first, blocks = census(ds,M)
        record = {'counts_18_to_24':row['counts_18_to_24'], 'M':M, 'k':k,
                  'split_count':int(row['split_count']), 'raw_cores':1 << comb(k,2),
                  'first_mask':first if first is not None else '-'}
        record.update({name:hist[name] for name in FIELDS[5:-1]})
        table.append(record)
        totals.update(hist)
        totals['raw_cores'] += record['raw_cores']
        if first is None:
            removed_splits += record['split_count']
            rejections.append({'counts_18_to_24':list(map(int,row['counts_18_to_24'].split(','))),
                               'M':M, 'exceptional_degrees':list(ds),
                               'removed_splits':record['split_count'],
                               'weighted_cores':hist['weighted'], 'obstructions':blocks})
    require(len(table) == 32 and len(rejections) == 7 and removed_splits == 14, 'classification totals')
    require(totals == Counter(raw_cores=209443, weighted=5114, core5=159,
                             red_capacity=5, blue_capacity=13, **{'pass':4937}), totals)
    document = {'format':'r55-signature-capacity-v1', 'input_sha256':INPUT_HASH,
                'max_exceptional':MAX_EXCEPTIONAL, 'tested_global_profiles':32,
                'untested_larger_global_profiles':56, 'excluded_global_profiles':7,
                'excluded_split_profiles':14, 'remaining_global_profiles':81,
                'remaining_split_profiles':307, 'stage_totals':dict(sorted(totals.items())),
                'scope':'marginal necessary-condition screen, not signature or graph feasibility',
                'rejections':rejections}
    return table, document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='emit the compact rejection certificate')
    args = parser.parse_args()
    table, document = compute()
    if args.json:
        print(json.dumps(document,indent=2,sort_keys=True))
    else:
        print('\t'.join(FIELDS))
        for row in table:
            print('\t'.join(str(row[field]) for field in FIELDS))


if __name__ == '__main__':
    main()
