#!/usr/bin/env python3
"""Bounded plateau-assisted exact-score descent; no closure from a state cap."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent/'ramsey_r55_cell_preserving_repair/search.py'
INPUT = ROOT.parent/'ramsey_r55_neutral_switch_escape/GRAPH.json'
SOURCE_SHA = 'a32bc43f6f48a4b860fa21441dcc5203fdc014058429522ebe357f3e65ea5f31'
INPUT_SHA = '6ee8bb9e55165e4e742064e96149bea791152de80b244ebce297c17c86ff529c'


def save(path, value):
    pending = path.with_suffix('.pending.json')
    pending.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
    pending.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--max-processed',type=int,default=512)
    parser.add_argument('--max-plateau',type=int,default=256)
    args = parser.parse_args()
    if args.work.exists() or min(args.max_processed,args.max_plateau)<1:
        raise ValueError('fresh work directory and positive bounds required')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA or hashlib.sha256(INPUT.read_bytes()).hexdigest()!=INPUT_SHA:
        raise ValueError('dependency provenance')
    spec = importlib.util.spec_from_file_location('exact_switches',SOURCE)
    search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search)
    current = tuple(int(x,16) for x in json.loads(INPUT.read_text())['red_adjacency_hex'])
    table = search.lifting_rows(current)
    if not search.lifted(current,table,range(43)):
        raise ValueError('initial lifting failure')
    args.work.mkdir(parents=True)
    start = time.monotonic()
    total = 0
    path = {'moves':[],'scores':[search.score(current)]}
    levels = []
    status = None
    while status is None:
        base = search.score(current)
        if base == 0:
            status = 'ALL_CENTRAL_CAPS'
            break
        nodes = [current]
        ids = {current:0}
        parents = [None]
        moves = [None]
        records = []
        escape = None
        for index in range(args.max_plateau):
            if index>=len(nodes):
                status = 'PLATEAU_CLOSED'
                break
            if total>=args.max_processed:
                status = 'TOTAL_STATE_LIMIT'
                break
            rows = nodes[index]
            tt = search.profiles(rows)
            counts = Counter()
            best = base
            chosen = None
            for move in search.swaps(rows):
                counts['all_switches'] += 1
                delta = search.triangle_delta(rows,move)
                score = base+sum(search.penalty(tt[v]+d,rows[v]&7)-search.penalty(tt[v],rows[v]&7) for v,d in delta.items() if v>=3)
                if score>base:
                    continue
                counts['nonincreasing'] += 1
                changed = tuple(search.flip(rows,move))
                if not search.lifted(changed,table,move[:2]):
                    counts['lifting_failures'] += 1
                    continue
                if not search.mixed_after_switch(changed,move):
                    counts['mixed_failures'] += 1
                    continue
                if score==base:
                    counts['neutral'] += 1
                    if changed not in ids:
                        ids[changed] = len(nodes)
                        nodes.append(changed)
                        parents.append(index)
                        moves.append(move)
                else:
                    counts['escaping'] += 1
                    if score<best:
                        best,chosen = score,move
            total += 1
            record = {'node':index,'counts':dict(sorted(counts.items())),'escape_move':chosen,'escape_score':best}
            records.append(record)
            if chosen is not None:
                escape = {'node':index,'move':chosen,'score':best}
            checkpoint = {'input_sha256':INPUT_SHA,'base_score':base,'completed_levels':levels,
                          'accepted_path':path,'nodes':[[format(x,'x') for x in g] for g in nodes],
                          'parents':parents,'parent_moves':moves,'records':records,
                          'escape':escape,'total_processed':total,'current_processed':len(records),
                          'current_discovered':len(nodes),'max_processed':args.max_processed,
                          'max_plateau':args.max_plateau}
            save(args.work/'checkpoint.json',checkpoint)
            if total%16==0 or chosen is not None:
                print(json.dumps({'base':base,'processed':len(records),'discovered':len(nodes),'total':total,'escape':escape},sort_keys=True),flush=True)
            if escape is not None:
                break
        else:
            status = 'PLATEAU_CLOSED' if len(records)==len(nodes) else 'PLATEAU_STATE_LIMIT'
        level = {'score':base,'processed':len(records),'discovered':len(nodes),'escape':escape}
        levels.append(level)
        if escape is None:
            break
        segment = [escape['move']]
        cursor = escape['node']
        while parents[cursor] is not None:
            segment.append(moves[cursor])
            cursor = parents[cursor]
        segment.reverse()
        for move in segment:
            before = search.profiles(current)
            delta = search.triangle_delta(current,move)
            current = tuple(search.flip(current,move))
            after = search.profiles(current)
            if any(b+delta.get(v,0)!=a for v,(b,a) in enumerate(zip(before,after))):
                raise ValueError('local triangle update discrepancy')
            actual = search.score(current,after)
            if actual>path['scores'][-1] or not search.lifted(current,table,range(43)):
                raise ValueError('invalid accepted path')
            path['moves'].append(move)
            path['scores'].append(actual)
        save(args.work/'PATH.json',path)
        save(args.work/'GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                                   'red_adjacency_hex':[format(x,'x') for x in current]})
    save(args.work/'PATH.json',path)
    save(args.work/'GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                               'red_adjacency_hex':[format(x,'x') for x in current]})
    result = {'status':status,'levels':levels,'total_processed':total,'path_length':len(path['moves']),
              'initial_score':path['scores'][0],'final_score':path['scores'][-1],
              'elapsed_seconds':round(time.monotonic()-start,6),
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'input_sha256':INPUT_SHA,'max_processed':args.max_processed,'max_plateau':args.max_plateau}
    save(args.work/'result.json',result)
    print(json.dumps(result,sort_keys=True),flush=True)


if __name__ == '__main__':
    main()
