#!/usr/bin/env python3
"""Bounded exact-K5 descent with exceptional-profile-preserving switches."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
SEED = HERE.parent/'ramsey_r55_k5_obstruction_repair/GRAPH.json'
SEED_SHA = 'c343c8ace3fb1c9dff6e90175ecdb1035989e0caf40a976a44d464a1381dc03c'
GATE_SHA = 'a32bc43f6f48a4b860fa21441dcc5203fdc014058429522ebe357f3e65ea5f31'
COUNT_SHA = '63edee70e0ffa08ec433cdd39ad16436804a1baf39daca22cfc96ae170d8314b'


def load(name, path, digest):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
        raise ValueError('dependency pin: '+str(path))
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependencies():
    gate = load('retained_gate',HERE.parent/'ramsey_r55_cell_preserving_repair/search.py',GATE_SHA)
    count = load('exact_k5_update',HERE.parent/'ramsey_r55_k5_obstruction_repair/search.py',COUNT_SHA)
    return gate,count


def bits(mask):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length()-1


def support(move):
    a,b,c,d = move
    return tuple(sorted(tuple(sorted(e)) for e in ((a,c),(b,d),(a,d),(b,c))))


def preserves(signatures):
    a,b,c,d = signatures
    return ((a^b)&(c^d))==0


def swaps(rows):
    """Every alternating C4 preserving the three exceptional local profiles."""
    seen = set()
    central = ((1 << 43)-1)^7
    for a,b in combinations(range(3,43),2):
        difference = (rows[a]^rows[b])&7
        only_a = rows[a]&~rows[b]&central&~((1 << a)|(1 << b))
        only_b = rows[b]&~rows[a]&central&~((1 << a)|(1 << b))
        for c,d in product(bits(only_a),bits(only_b)):
            if difference&(rows[c]^rows[d]):
                continue
            key = support((a,b,c,d))
            if key not in seen:
                seen.add(key)
                yield a,b,c,d


def quota_preserving(rows, move):
    a,b,c,d = (rows[v]&7 for v in move)
    return a==b or c==d


def scan(rows, gate, count, table, values):
    blue = count.complement(rows)
    tt = gate.profiles(rows)
    phi = gate.score(rows,tt)
    best = chosen = None
    census = Counter()
    histogram = Counter()
    for move in swaps(rows):
        census['all_switches'] += 1
        old = quota_preserving(rows,move)
        census['quota_preserving' if old else 'quota_changing'] += 1
        changed = tuple(gate.flip(rows,move))
        full_support = gate.lifted(changed,table,move)
        if not full_support:
            census['lifting_failures'] += 1
            if gate.lifted(changed,table,move[:2]):
                census['unsafe_first_pair_gate_false_accepts'] += 1
            continue
        if not gate.mixed_after_switch(changed,move):
            census['mixed_failures'] += 1
            continue
        census['admissible'] += 1
        census['admissible_quota_preserving' if old else 'admissible_quota_changing'] += 1
        delta = count.k5_change(rows,move,blue)
        histogram[sum(delta)] += 1
        if sum(delta)>=0:
            continue
        census['k5_decreasing'] += 1
        local = gate.triangle_delta(rows,move)
        next_phi = phi+sum(gate.penalty(tt[v]+d,rows[v]&7)-gate.penalty(tt[v],rows[v]&7)
                           for v,d in local.items() if v>=3)
        rank = (sum(values)+sum(delta),next_phi,move)
        if best is None or rank<best:
            best,chosen = rank,move
    return chosen,best,dict(sorted(census.items())),{str(k):v for k,v in sorted(histogram.items())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--max-steps',type=int,default=128)
    args = parser.parse_args()
    if args.work.exists() or args.max_steps<1:
        raise ValueError('fresh work directory and positive bound required')
    if hashlib.sha256(SEED.read_bytes()).hexdigest()!=SEED_SHA:
        raise ValueError('seed pin')
    gate,count = dependencies()
    rows = tuple(int(x,16) for x in json.loads(SEED.read_text())['red_adjacency_hex'])
    table = gate.lifting_rows(rows)
    exceptional = gate.profiles(rows)[:3]
    values = count.counts(rows)
    if values!=(198,186) or not gate.lifted(rows,table,range(43)):
        raise ValueError('seed invariants')
    path = {'seed_sha256':SEED_SHA,'moves':[],'color_counts':[values],'phi':[gate.score(rows)]}
    args.work.mkdir(parents=True)
    records = []
    start = time.monotonic()
    status = 'STEP_LIMIT'
    for step in range(args.max_steps):
        chosen,best,census,histogram = scan(rows,gate,count,table,values)
        record = {'step':step,'before_color_counts':values,'before_phi':gate.score(rows),
                  'move':chosen,'rank':best,'census':census,'admissible_K5_delta_histogram':histogram}
        records.append(record)
        if chosen is None:
            status = 'NO_K5_DECREASING_SWITCH'
        else:
            predicted = count.k5_change(rows,chosen)
            rows = tuple(gate.flip(rows,chosen))
            exact = count.counts(rows)
            if exact!=tuple(x+d for x,d in zip(values,predicted)) or sum(exact)>=sum(values):
                raise ValueError('K5 update or descent mismatch')
            values = exact
            if gate.score(rows)!=best[1] or gate.profiles(rows)[:3]!=exceptional or not gate.lifted(rows,table,range(43)):
                raise ValueError('accepted path invariant mismatch')
            path['moves'].append(chosen)
            path['color_counts'].append(values)
            path['phi'].append(best[1])
            if sum(values)==0:
                status = 'ZERO_K5_REQUIRES_FULL_AUDIT'
        count.save(args.work/'PATH.json',path)
        count.save(args.work/'GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                                          'red_adjacency_hex':[format(x,'x') for x in rows]})
        count.save(args.work/'checkpoint.json',{'seed_sha256':SEED_SHA,'max_steps':args.max_steps,
                                               'records':records,'path':path,'status':status})
        print(json.dumps(record,sort_keys=True),flush=True)
        if chosen is None or sum(values)==0:
            break
    result = {'status':status,'steps':len(path['moves']),'initial_color_counts':path['color_counts'][0],
              'final_color_counts':values,'final_phi':gate.score(rows),'records':records,
              'max_steps':args.max_steps,'elapsed_seconds':round(time.monotonic()-start,6),
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seed_sha256':SEED_SHA}
    count.save(args.work/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))


if __name__=='__main__':
    main()
