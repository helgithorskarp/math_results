#!/usr/bin/env python3
"""Exact K5-count switch updates and bounded strict target-obstruction descent."""
import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent/'ramsey_r55_cell_preserving_repair/search.py'
COMPONENT = ROOT.parent/'ramsey_r55_neutral_component_barrier/COMPONENT.json'
SOURCE_SHA = 'a32bc43f6f48a4b860fa21441dcc5203fdc014058429522ebe357f3e65ea5f31'
COMPONENT_SHA = 'c366bf0ea4a392c5cf4b1a5789229c5aa74abfb08bd604fe636575ce9e960a2d'


def complement(rows):
    universe = (1 << len(rows))-1
    return tuple(universe^row^(1 << u) for u,row in enumerate(rows))


def triangles_in(rows, mask):
    total = 0
    while mask:
        bit = mask & -mask
        mask ^= bit
        u = bit.bit_length()-1
        possible = mask&rows[u]
        while possible:
            bit = possible & -possible
            possible ^= bit
            v = bit.bit_length()-1
            total += (possible&rows[v]).bit_count()
    return total


def k5_change(rows, move, blue=None):
    a,b,c,d = move
    if len(set(move))!=4 or not(rows[a] >> c & 1 and rows[b] >> d & 1) or rows[a] >> d & 1 or rows[b] >> c & 1:
        raise ValueError('alternating four-vertex switch required')
    outside = ((1 << len(rows))-1)^sum(1 << v for v in move)
    A,B,C,D = (rows[v]&outside for v in move)
    red = (triangles_in(rows,A&D)+triangles_in(rows,B&C)
           -triangles_in(rows,A&C)-triangles_in(rows,B&D))
    blue = complement(rows) if blue is None else blue
    A,B,C,D = (outside^mask for mask in (A,B,C,D))
    other = (triangles_in(blue,A&C)+triangles_in(blue,B&D)
             -triangles_in(blue,A&D)-triangles_in(blue,B&C))
    return red,other


def clique_count(rows, size, candidates=None):
    if size==0:
        return 1
    if candidates is None:
        candidates = (1 << len(rows))-1
    if size==1:
        return candidates.bit_count()
    result = 0
    while candidates.bit_count()>=size:
        bit = candidates & -candidates
        candidates ^= bit
        v = bit.bit_length()-1
        result += clique_count(rows,size-1,candidates&rows[v])
    return result


def counts(rows):
    return clique_count(rows,5),clique_count(complement(rows),5)


def save(path, value):
    pending = path.with_suffix('.pending.json')
    pending.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
    pending.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--max-steps',type=int,default=128)
    args = parser.parse_args()
    if args.work.exists() or args.max_steps<1:
        raise ValueError('fresh work directory and positive step bound required')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA or hashlib.sha256(COMPONENT.read_bytes()).hexdigest()!=COMPONENT_SHA:
        raise ValueError('input provenance')
    initial = json.loads(COMPONENT.read_text())['graphs'][2]
    rows = tuple(int(x,16) for x in initial)
    spec = importlib.util.spec_from_file_location('retained_switch_gates',SOURCE)
    search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search)
    table = search.lifting_rows(rows)
    values = counts(rows)
    if values!=(238,212) or not search.lifted(rows,table,range(43)):
        raise ValueError('initial graph invariants')
    path = {'component_start_index':2,'moves':[],'color_counts':[values],'phi':[search.score(rows)]}
    records = []
    args.work.mkdir(parents=True)
    start = time.monotonic()
    status = 'STEP_LIMIT'
    for step in range(args.max_steps):
        blue = complement(rows)
        tt = search.profiles(rows)
        phi = search.score(rows,tt)
        best = None
        chosen = None
        census = Counter()
        for move in search.swaps(rows):
            census['all_switches'] += 1
            changed = tuple(search.flip(rows,move))
            if not search.lifted(changed,table,move[:2]):
                census['lifting_failures'] += 1
                continue
            if not search.mixed_after_switch(changed,move):
                census['mixed_failures'] += 1
                continue
            census['admissible'] += 1
            delta = k5_change(rows,move,blue)
            if sum(delta)>=0:
                continue
            census['k5_decreasing'] += 1
            local = search.triangle_delta(rows,move)
            next_phi = phi+sum(search.penalty(tt[v]+d,rows[v]&7)-search.penalty(tt[v],rows[v]&7) for v,d in local.items() if v>=3)
            rank = (sum(values)+sum(delta),next_phi,move)
            if best is None or rank<best:
                best,chosen = rank,move
        record = {'step':step,'before_color_counts':values,'before_phi':phi,
                  'move':chosen,'rank':best,'census':dict(sorted(census.items()))}
        records.append(record)
        if chosen is None:
            status = 'NO_K5_DECREASING_SWITCH'
            print(json.dumps(record,sort_keys=True),flush=True)
            break
        predicted = k5_change(rows,chosen,blue)
        rows = tuple(search.flip(rows,chosen))
        exact = counts(rows)
        if exact!=tuple(x+d for x,d in zip(values,predicted)) or sum(exact)>=sum(values):
            raise ValueError('full K5 reconstruction disagrees with update')
        values = exact
        if search.score(rows)!=best[1] or not search.lifted(rows,table,range(43)):
            raise ValueError('accepted path invariant discrepancy')
        path['moves'].append(chosen)
        path['color_counts'].append(values)
        path['phi'].append(best[1])
        save(args.work/'PATH.json',path)
        save(args.work/'GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                                    'red_adjacency_hex':[format(x,'x') for x in rows]})
        save(args.work/'checkpoint.json',{'input_component_sha256':COMPONENT_SHA,'max_steps':args.max_steps,
                                         'records':records,'path':path,'current_graph':[format(x,'x') for x in rows]})
        print(json.dumps({'step':step,'move':chosen,'counts':values,'total':sum(values),'phi':best[1]},sort_keys=True),flush=True)
        if sum(values)==0:
            status = 'ZERO_K5_REQUIRES_FULL_AUDIT'
            break
    result = {'status':status,'steps':len(path['moves']),'initial_color_counts':path['color_counts'][0],
              'final_color_counts':values,'final_phi':search.score(rows),'records':records,
              'max_steps':args.max_steps,'elapsed_seconds':round(time.monotonic()-start,6),
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'component_sha256':COMPONENT_SHA}
    save(args.work/'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},sort_keys=True))


if __name__=='__main__':
    main()
