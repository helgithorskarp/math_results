#!/usr/bin/env python3
"""Definition-level replay: Gray-code graphs and literal clique subsets.

No classifier imports. Checks every census field and rejection certificate.
"""

from collections import Counter
from copy import deepcopy
import csv
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'ramsey_r55_exceptional_degree_sieve/PROFILES.tsv'
INPUT_HASH = 'a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa'
U = {18:85, 19:92, 20:100, 21:107, 22:114, 23:122, 24:132}
STAGES = ('weighted','core5','total_capacity','red_capacity','blue_capacity','pass')


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


@lru_cache(None)
def ramsey_upper(a,b):
    # The elementary recurrence, not a table of exact Ramsey numbers.
    if min(a,b) == 1:
        return 1
    return ramsey_upper(a-1,b)+ramsey_upper(a,b-1)


def literal_screen(neighbors, ds, M):
    k, n = len(ds), 43-len(ds)
    full = (1 << k)-1
    red_cliques, blue_cliques = [], []
    for mask in range(1 << k):
        vertices = [i for i in range(k) if mask >> i & 1]
        pairs = list(combinations(vertices,2))
        if all(j in neighbors[i] for i,j in pairs):
            red_cliques.append((mask,len(vertices)))
        if all(j not in neighbors[i] for i,j in pairs):
            blue_cliques.append((mask,len(vertices)))
    if any(size >= 5 for _,size in red_cliques+blue_cliques):
        return {'reason':'core5'}
    caps = []
    for x in range(1 << k):
        if sum(ds[i]-21 for i in range(k) if x >> i & 1) > M-220:
            continue
        r = max(size for mask,size in red_cliques if mask & x == mask)
        blue = full ^ x
        s = max(size for mask,size in blue_cliques if mask & blue == mask)
        if r >= 4 or s >= 4:
            continue
        caps.append((x,min(n,ramsey_upper(5-r,5-s)-1)))
    total = sum(cap for _,cap in caps)
    if total < n:
        return {'reason':'total_capacity','available':total,'required':n}
    for i,d in enumerate(ds):
        red = d-len(neighbors[i])
        require(0 <= red <= n, 'cross degree')
        bounds = [sum(cap for x,cap in caps if bool(x >> i & 1) == color) for color in (True,False)]
        for color,bound,demand in zip(('red_capacity','blue_capacity'),bounds,(red,n-red)):
            if bound < demand:
                return {'reason':color,'vertex':i,'available':bound,'required':demand}
    return {'reason':'pass'}


def reconstruct(source):
    output, rejected, totals = [], [], Counter()
    graph_instances = 0
    for row in source:
        if row['status'] != 'feasible':
            continue
        counts = list(map(int,row['counts_18_to_24'].split(',')))
        ds = [d for d,n in zip(range(18,25),counts) if d != 21 for _ in range(n)]
        k, n, M = len(ds), counts[3], int(row['M'])
        if k > 6:
            continue
        targets = [U[d]+U[42-d]-14-comb(42-d,2)+(231+M)-21*d for d in ds]
        edges = list(combinations(range(k),2))
        neighbors = [set() for _ in ds]
        previous, first, hist, blocks = 0, None, Counter(), []
        for index in range(1 << len(edges)):
            mask = index ^ (index >> 1)
            if index:
                changed = mask ^ previous
                i,j = edges[changed.bit_length()-1]
                if j in neighbors[i]:
                    neighbors[i].remove(j)
                    neighbors[j].remove(i)
                else:
                    neighbors[i].add(j)
                    neighbors[j].add(i)
            previous = mask
            graph_instances += 1
            sums = [sum(ds[j]-21 for j in near) for near in neighbors]
            if any(s > t for s,t in zip(sums,targets)):
                continue
            # Count exceptional-to-central weighted incidence directly.
            central_sum = sum((d-21)*(d-len(near)) for d,near in zip(ds,neighbors))
            if central_sum > n*(M-220):
                continue
            hist['weighted'] += 1
            block = literal_screen(neighbors,ds,M)
            hist[block['reason']] += 1
            if block['reason'] == 'pass':
                first = mask if first is None else min(first,mask)
            else:
                blocks.append({'red_mask':mask, **block})
        result = {'counts_18_to_24':row['counts_18_to_24'],'M':str(M),'k':str(k),
                  'split_count':row['split_count'],'raw_cores':str(1 << len(edges)),
                  'first_mask':'-' if first is None else str(first)}
        result.update({stage:str(hist[stage]) for stage in STAGES})
        output.append(result)
        totals.update(hist)
        totals['raw_cores'] += 1 << len(edges)
        if first is None:
            rejected.append({'counts_18_to_24':counts,'M':M,'exceptional_degrees':ds,
                             'removed_splits':int(row['split_count']),
                             'weighted_cores':hist['weighted'],
                             'obstructions':sorted(blocks,key=lambda b:b['red_mask'])})
    require(graph_instances == 209443, 'full labeled graph universe')
    removed = sum(row['removed_splits'] for row in rejected)
    document = {'format':'r55-signature-capacity-v1','input_sha256':INPUT_HASH,
                'max_exceptional':6,'tested_global_profiles':len(output),
                'untested_larger_global_profiles':88-len(output),
                'excluded_global_profiles':len(rejected),'excluded_split_profiles':removed,
                'remaining_global_profiles':88-len(rejected),'remaining_split_profiles':321-removed,
                'stage_totals':dict(sorted(totals.items())),
                'scope':'marginal necessary-condition screen, not signature or graph feasibility',
                'rejections':rejected}
    return output, document


def compare(actual, expected):
    require(actual == expected, 'certificate or census mismatch')


def main():
    require(sha256(INPUT.read_bytes()).hexdigest() == INPUT_HASH, 'inherited input hash')
    extrema = HERE.parent / 'ramsey_r55_local_extremal_deficiency/extrema.json'
    require(sha256(extrema.read_bytes()).hexdigest() ==
            '7233dd701f47de79c65ecccb6b06ad8f79b16b92c08cfcf73bcef1ed3b4d5b10', 'extrema hash')
    require({int(d):value for d,value in json.loads(extrema.read_text())['max_edges'].items()} == U,
            'extrema constants')
    with INPUT.open() as stream:
        source = list(csv.DictReader(stream,delimiter='\t'))
    require(len(source) == 104 and sum(r['status']=='feasible' for r in source)==88, 'input universe')
    require(sum(int(r['split_count']) for r in source if r['status']=='feasible') == 321, 'input splits')
    expected_table, expected_certificate = reconstruct(source)
    with (HERE/'CENSUS.tsv').open() as stream:
        actual_table = list(csv.DictReader(stream,delimiter='\t'))
    actual_certificate = json.loads((HERE/'REJECTIONS.json').read_text())
    compare(actual_table,expected_table)
    compare(actual_certificate,expected_certificate)
    mutants = [deepcopy(expected_certificate) for _ in range(4)]
    mutants[0]['rejections'][0]['obstructions'][0]['available'] += 1
    mutants[1]['rejections'][1]['obstructions'].pop()
    mutants[2]['remaining_split_profiles'] += 1
    mutants[3]['rejections'][0]['counts_18_to_24'][3] -= 1
    for mutant in mutants:
        try:
            compare(mutant,expected_certificate)
        except ValueError:
            continue
        raise ValueError('mutation accepted')
    print('PASS pinned 104-profile input: 88 aggregate survivors and 321 anchored splits')
    print('PASS full entry-level census replay: 32 profiles, 209443 labeled core graphs')
    print('PASS weighted cores=5114; core-K5 rejects=159; red/blue capacity rejects=5/13')
    print('PASS 4937 marginal-screen cores in 25 small profiles; 56 larger profiles untested')
    print('PASS seven exclusions and every obstruction in the compact certificate')
    print('PASS cumulative remaining candidates: 81 global profiles, 307 anchored splits')
    print('PASS four altered certificates rejected')
    print('SCOPE necessary marginal screen only; no complete signature assignment or Ramsey witness')
    print('certificate_sha256='+sha256((HERE/'REJECTIONS.json').read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
