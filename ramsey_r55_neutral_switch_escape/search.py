#!/usr/bin/env python3
"""Bounded neutral BFS; stop at the first escaping state, never continue downhill."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'ramsey_r55_cell_preserving_repair'
SEARCH_SHA = 'a32bc43f6f48a4b860fa21441dcc5203fdc014058429522ebe357f3e65ea5f31'
GRAPH_SHA = '7a832f229bb3fd97f5c3e5dceb060988fb5c5d2df074d1cb37ddbb1dcd5fc8a6'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--max-states',type=int,default=256)
    args = parser.parse_args()
    if args.work.exists() or args.max_states<1:
        raise ValueError('fresh work directory and positive state cap required')
    source = PARENT/'search.py'
    if hashlib.sha256(source.read_bytes()).hexdigest() != SEARCH_SHA:
        raise ValueError('search source provenance')
    raw = (PARENT/'GRAPH.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != GRAPH_SHA:
        raise ValueError('starting graph provenance')
    spec = importlib.util.spec_from_file_location('inherited_switches',source)
    search = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(search)
    initial = tuple(int(row,16) for row in json.loads(raw)['red_adjacency_hex'])
    target = search.score(initial)
    table = search.lifting_rows(initial)
    nodes = [initial]
    parent = [None]
    parent_move = [None]
    ids = {initial:0}
    records = []
    escape = None
    args.work.mkdir(parents=True)
    start = time.monotonic()
    for i in range(args.max_states):
        if i >= len(nodes):
            break
        rows = nodes[i]
        tt = search.profiles(rows)
        counts = Counter()
        neutral = []
        best = target
        chosen = None
        for move in search.swaps(rows):
            counts['all_switches'] += 1
            delta = search.triangle_delta(rows,move)
            score = target+sum(search.penalty(tt[v]+d,rows[v]&7)-search.penalty(tt[v],rows[v]&7) for v,d in delta.items() if v>=3)
            if score > target:
                continue
            counts['nonincreasing'] += 1
            changed = tuple(search.flip(rows,move))
            if not search.lifted(changed,table,move[:2]):
                counts['lifting_failures'] += 1
                continue
            if not search.mixed_after_switch(changed,move):
                counts['mixed_failures'] += 1
                continue
            if score == target:
                if changed not in ids:
                    ids[changed] = len(nodes)
                    nodes.append(changed)
                    parent.append(i)
                    parent_move.append(move)
                neutral.append([ids[changed],move])
                counts['neutral'] += 1
            else:
                counts['escaping'] += 1
                if score < best:
                    best,chosen = score,move
        rec = {'node':i,'counts':dict(sorted(counts.items())),'neutral':neutral,'escape_move':chosen,'escape_score':best}
        records.append(rec)
        print(json.dumps(rec,sort_keys=True),flush=True)
        if chosen is not None:
            escape = {'node':i,'move':chosen,'score':best}
        checkpoint = {'format':'r55-neutral-plateau-probe-v1','target_score':target,
                      'nodes':[[format(x,'x') for x in rows] for rows in nodes],
                      'parents':parent,'parent_moves':parent_move,'records':records,
                      'escape':escape,'processed':len(records),'discovered':len(nodes)}
        pending = args.work/'checkpoint.pending.json'
        pending.write_text(json.dumps(checkpoint,indent=2,sort_keys=True)+'\n')
        pending.replace(args.work/'checkpoint.json')
        if escape is not None:
            break
    if escape is not None:
        moves = [escape['move']]
        cursor = escape['node']
        while parent[cursor] is not None:
            moves.append(parent_move[cursor])
            cursor = parent[cursor]
        moves.reverse()
        end = list(initial)
        scores = [target]
        for move in moves:
            end = search.flip(end,move)
            scores.append(search.score(end))
        graph = {'format':'r55-triple-degree-exact-mixed-graph-v1','red_adjacency_hex':[format(x,'x') for x in end]}
        (args.work/'GRAPH.json').write_text(json.dumps(graph,indent=2)+'\n')
        (args.work/'PATH.json').write_text(json.dumps({'moves':moves,'scores':scores},indent=2)+'\n')
    summary = {'status':'ESCAPE_FOUND' if escape else 'PLATEAU_CLOSED' if len(records)==len(nodes) else 'STATE_LIMIT',
               'processed':len(records),'discovered':len(nodes),'escape':escape,
               'elapsed_seconds':round(time.monotonic()-start,6),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (args.work/'result.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))


if __name__ == '__main__':
    main()
