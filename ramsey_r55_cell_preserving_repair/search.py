#!/usr/bin/env python3
"""Deterministic restricted-switch descent; the separate verifier certifies scope."""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent/'ramsey_r55_triple_graph_realization/GRAPH.json'
SOURCE_SHA = 'a57fc26ea50196d82537220cf057c659860f9842dd35351d33445781f019eae5'


def bits(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length()-1


def profiles(rows):
    return [sum((rows[v]&row).bit_count() for v in bits(row))//2 for row in rows]


def penalty(t, signature):
    return max(0,t-100)+max(0,101-signature.bit_count()-t)


def score(rows, tt=None):
    tt = profiles(rows) if tt is None else tt
    return sum(penalty(tt[v],rows[v]&7) for v in range(3,43))


def swaps(rows):
    """Unique four-edge supports with an opposite pair in one signature cell."""
    seen = set()
    central = ((1 << 43)-1)^7
    for a,b in combinations(range(3,43),2):
        if rows[a]&7 != rows[b]&7:
            continue
        only_a = rows[a]&~rows[b]&central&~((1 << a)|(1 << b))
        only_b = rows[b]&~rows[a]&central&~((1 << a)|(1 << b))
        for c,d in product(bits(only_a),bits(only_b)):
            support = tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))
            if support in seen:
                continue
            seen.add(support)
            yield a,b,c,d


def flip(rows, move):
    a,b,c,d = move
    result = list(rows)
    for u,v in ((a,c),(b,d),(a,d),(b,c)):
        result[u] ^= 1 << v
        result[v] ^= 1 << u
    return result


def triangle_delta(rows, move):
    a,b,c,d = move
    outside = ((1 << len(rows))-1)^sum(1 << v for v in move)
    A,B,C,D = (rows[v]&outside for v in move)
    ab,ba,dc,cd = A&~B,B&~A,D&~C,C&~D
    delta = {a:(A&dc).bit_count()-(A&cd).bit_count(),
             b:(B&cd).bit_count()-(B&dc).bit_count(),
             c:(C&ba).bit_count()-(C&ab).bit_count(),
             d:(D&ab).bit_count()-(D&ba).bit_count()}
    for u in bits((ab&dc)|(ba&cd)):
        delta[u] = 1
    for u in bits((ab&cd)|(ba&dc)):
        delta[u] = -1
    return {v:change for v,change in delta.items() if change}


@lru_cache(None)
def upper(a,b):
    if min(a,b) == 1:
        return 1
    x,y = upper(a-1,b),upper(a,b-1)
    return x+y-int(x%2 == y%2 == 0)


def lifting_rows(rows):
    table = [dict() for _ in rows]
    for word in product(range(3),repeat=3):
        A = {i for i,w in enumerate(word) if w == 1}
        B = {i for i,w in enumerate(word) if w == 2}
        if not A|B or any(not(rows[u] >> v & 1) for u,v in combinations(sorted(A),2)) or any(rows[u] >> v & 1 for u,v in combinations(sorted(B),2)):
            continue
        S = sum(1 << v for v in range(43) if v not in A|B
                and all(rows[u] >> v & 1 for u in A)
                and all(not(rows[u] >> v & 1) for u in B))
        for u in range(43):
            if u in A|B:
                continue
            mask = S&~(1 << u)
            lo,hi = table[u].get(mask,(0,mask.bit_count()))
            if all(rows[u] >> v & 1 for v in A):
                hi = min(hi,upper(4-len(A),5-len(B))-1)
            if all(not(rows[u] >> v & 1) for v in B):
                lo = max(lo,mask.bit_count()-(upper(5-len(A),4-len(B))-1))
            table[u][mask] = (lo,hi)
    return [[(mask,lo,hi) for mask,(lo,hi) in sorted(rec.items())] for rec in table]


def lifted(rows, table, vertices):
    return all(lo <= (rows[u]&mask).bit_count() <= hi for u in vertices for mask,lo,hi in table[u])


def mixed_after_switch(rows, move, root_mask=7):
    """A new mixed K5 contains a newly red/blue central edge and an E root."""
    a,b,c,d = move
    allbits = (1 << len(rows))-1
    for red,pairs in ((True,((a,d),(b,c))),(False,((a,c),(b,d)))):
        adjacency = rows if red else [allbits^row^(1 << u) for u,row in enumerate(rows)]
        for u,v in pairs:
            common = adjacency[u]&adjacency[v]
            for root in bits(common&root_mask):
                possible = common&adjacency[root]
                if any(adjacency[w]&possible for w in bits(possible)):
                    return False
    return True


def best_move(rows, table):
    tt = profiles(rows)
    initial = score(rows,tt)
    best = initial
    chosen = None
    census = Counter()
    for move in swaps(rows):
        census['all_switches'] += 1
        delta = triangle_delta(rows,move)
        newscore = initial+sum(penalty(tt[v]+d,rows[v]&7)-penalty(tt[v],rows[v]&7) for v,d in delta.items() if v>=3)
        if newscore >= initial:
            census['nondecreasing'] += 1
            continue
        census['decreasing'] += 1
        changed = flip(rows,move)
        if not lifted(changed,table,move[:2]):
            census['decreasing_lift_failure'] += 1
            continue
        if not mixed_after_switch(changed,move):
            census['decreasing_mixed_failure'] += 1
            continue
        census['decreasing_admissible'] += 1
        if newscore < best:
            best = newscore
            chosen = move
    return chosen,best,dict(sorted(census.items()))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    args = p.parse_args()
    if args.work.exists():
        raise ValueError('fresh work path required')
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise ValueError('input graph hash')
    rows = [int(row,16) for row in json.loads(raw)['red_adjacency_hex']]
    table = lifting_rows(rows)
    if not lifted(rows,table,range(43)):
        raise ValueError('invalid initial lifting rows')
    args.work.mkdir(parents=True)
    start = time.monotonic()
    record = {'input_sha256':SOURCE_SHA,'initial_score':score(rows),'steps':[]}
    while True:
        before = profiles(rows)
        chosen,newscore,census = best_move(rows,table)
        row = {'before_score':score(rows,before),'move':chosen,'after_score':newscore,'census':census}
        record['steps'].append(row)
        print(json.dumps(row,sort_keys=True),flush=True)
        if chosen is None:
            break
        predicted = triangle_delta(rows,chosen)
        rows = flip(rows,chosen)
        after = profiles(rows)
        if any(after[v]-before[v] != predicted.get(v,0) for v in range(43)):
            raise ValueError('triangle update disagreement')
        if score(rows,after) != newscore or not lifted(rows,table,range(43)):
            raise ValueError('post-move verification')
        (args.work/'progress.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        if newscore == 0:
            break
    graph = {'format':'r55-triple-degree-exact-mixed-graph-v1','red_adjacency_hex':[format(row,'x') for row in rows]}
    (args.work/'GRAPH.json').write_text(json.dumps(graph,indent=2)+'\n')
    record.update(final_score=score(rows),elapsed_seconds=round(time.monotonic()-start,6),
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  terminal='ALL_CENTRAL_CAPS' if score(rows)==0 else 'NO_STRICTLY_IMPROVING_SWITCH',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (args.work/'result.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps({key:record[key] for key in ('initial_score','final_score','terminal','elapsed_seconds','peak_rss_kib')},sort_keys=True))


if __name__ == '__main__':
    main()
