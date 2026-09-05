#!/usr/bin/env python3
"""Bounded sublevel BFS; stop on the first lower-score escape."""
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
COMPONENT = ROOT/'COMPONENT.json'
SOURCE_SHA = 'a32bc43f6f48a4b860fa21441dcc5203fdc014058429522ebe357f3e65ea5f31'
COMPONENT_SHA = 'c366bf0ea4a392c5cf4b1a5789229c5aa74abfb08bd604fe636575ce9e960a2d'


def save(path, value):
    pending = path.with_suffix('.pending.json')
    pending.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
    pending.replace(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--max-processed',type=int,default=512)
    parser.add_argument('--ceiling',type=int,default=74)
    parser.add_argument('--start-index',type=int,default=2)
    args = parser.parse_args()
    if args.work.exists() or args.max_processed<1 or args.ceiling<73:
        raise ValueError('fresh work directory, positive bound and ceiling>=73 required')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA or hashlib.sha256(COMPONENT.read_bytes()).hexdigest()!=COMPONENT_SHA:
        raise ValueError('source/input provenance')
    document = json.loads(COMPONENT.read_text())
    if not 0<=args.start_index<len(document['graphs']):
        raise ValueError('invalid component vertex')
    initial = tuple(int(x,16) for x in document['graphs'][args.start_index])
    spec = importlib.util.spec_from_file_location('sublevel_switches',SOURCE)
    search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search)
    table = search.lifting_rows(initial)
    base = search.score(initial)
    if base!=document['score'] or not search.lifted(initial,table,range(43)):
        raise ValueError('initial invariants')
    args.work.mkdir(parents=True)
    start = time.monotonic()
    nodes,parents,moves = [initial],[None],[None]
    ids = {initial:0}
    records = []
    escape = None
    for index in range(args.max_processed):
        if index>=len(nodes):
            break
        rows = nodes[index]
        tt = search.profiles(rows)
        current = search.score(rows,tt)
        best = base
        chosen = None
        counts = Counter()
        for move in search.swaps(rows):
            counts['all_switches'] += 1
            delta = search.triangle_delta(rows,move)
            score = current+sum(search.penalty(tt[v]+d,rows[v]&7)-search.penalty(tt[v],rows[v]&7) for v,d in delta.items() if v>=3)
            if score>args.ceiling:
                continue
            counts['within_ceiling'] += 1
            changed = tuple(search.flip(rows,move))
            if not search.lifted(changed,table,move[:2]):
                counts['lifting_failures'] += 1
                continue
            if not search.mixed_after_switch(changed,move):
                counts['mixed_failures'] += 1
                continue
            if score<base:
                counts['escaping'] += 1
                if score<best:
                    best,chosen = score,move
            else:
                counts['admissible_sublevel'] += 1
                if changed not in ids:
                    ids[changed] = len(nodes)
                    nodes.append(changed)
                    parents.append(index)
                    moves.append(move)
        record = {'node':index,'score':current,'counts':dict(sorted(counts.items())),
                  'escape_move':chosen,'escape_score':best}
        records.append(record)
        if chosen is not None:
            escape = {'node':index,'move':chosen,'score':best}
        save(args.work/'checkpoint.json',{'component_sha256':COMPONENT_SHA,'start_index':args.start_index,
                 'base_score':base,'ceiling':args.ceiling,'max_processed':args.max_processed,
                 'nodes':[[format(x,'x') for x in g] for g in nodes],'parents':parents,'parent_moves':moves,
                 'records':records,'processed':len(records),'discovered':len(nodes),'escape':escape})
        if index%16==0 or escape is not None:
            print(json.dumps({'processed':len(records),'discovered':len(nodes),'escape':escape},sort_keys=True),flush=True)
        if escape is not None:
            break
    path = {'component_start_index':args.start_index,'moves':[],'scores':[base],'ceiling':args.ceiling}
    final = initial
    if escape is not None:
        segment = [escape['move']]
        cursor = escape['node']
        while parents[cursor] is not None:
            segment.append(moves[cursor])
            cursor = parents[cursor]
        segment.reverse()
        for move in segment:
            before = search.profiles(final)
            delta = search.triangle_delta(final,move)
            final = tuple(search.flip(final,move))
            after = search.profiles(final)
            if any(b+delta.get(v,0)!=a for v,(b,a) in enumerate(zip(before,after))):
                raise ValueError('triangle update disagreement')
            actual = search.score(final,after)
            if actual>args.ceiling or not search.lifted(final,table,range(43)):
                raise ValueError('accepted path invariant failure')
            path['moves'].append(move)
            path['scores'].append(actual)
        save(args.work/'PATH.json',path)
        save(args.work/'GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                                    'red_adjacency_hex':[format(x,'x') for x in final]})
    result = {'status':'ESCAPE_FOUND' if escape else 'SUBLEVEL_CLOSED' if len(records)==len(nodes) else 'STATE_LIMIT',
              'processed':len(records),'discovered':len(nodes),'escape':escape,'path_scores':path['scores'],
              'start_index':args.start_index,'ceiling':args.ceiling,'max_processed':args.max_processed,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'component_sha256':COMPONENT_SHA,'elapsed_seconds':round(time.monotonic()-start,6),
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    save(args.work/'result.json',result)
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
