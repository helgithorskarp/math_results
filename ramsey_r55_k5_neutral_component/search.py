#!/usr/bin/env python3
"""Bounded single-level neutral-component census; never descend to another level."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent/'ramsey_r55_exceptional_profile_switches'
SEED = PARENT/'GRAPH.json'
SEED_SHA = '122ed044228839122d6dba6d0f1cb87480818a6a8e8b277b6e5504d2da2e2cbc'
SOURCE_SHA = '54a90b7875675db36f77b8f1712cc74bbbce21e10e5fbb31711143e7424b2b64'
LEVEL = 358


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load_parent():
    source = PARENT/'search.py'
    require(hashlib.sha256(source.read_bytes()).hexdigest()==SOURCE_SHA,'parent source pin')
    spec = importlib.util.spec_from_file_location('profile_switches',source)
    parent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(parent)
    return parent


def census(rows, parent, gate, count, table):
    values = count.counts(rows)
    require(sum(values)==LEVEL,'wrong neutral level')
    blue = count.complement(rows)
    summary,histogram = Counter(),Counter()
    entries,neutral,negative = [],[],[]
    for move in parent.swaps(rows):
        support = parent.support(move)
        changed = tuple(gate.flip(rows,move))
        quota_change = not parent.quota_preserving(rows,move)
        summary['all_switches'] += 1
        summary['quota_changing' if quota_change else 'quota_preserving'] += 1
        after = None
        if not gate.lifted(changed,table,move):
            kind = 'lifting_failure'
        elif not gate.mixed_after_switch(changed,move):
            kind = 'mixed_failure'
        else:
            kind = 'admissible'
            summary['admissible_quota_changing' if quota_change else 'admissible_quota_preserving'] += 1
            after = tuple(v+d for v,d in zip(values,count.k5_change(rows,move,blue)))
            delta = sum(after)-LEVEL
            histogram[delta] += 1
            if delta<=0:
                require(after==count.counts(changed),'nonincreasing neighbor full K5 discrepancy')
                require(gate.profiles(changed)[:3]==[92]*3 and gate.lifted(changed,table,range(43)),
                        'nonincreasing neighbor retained invariant discrepancy')
                item = {'move':move,'support':support,'color_counts':after,'changes_quotas':quota_change}
                (neutral if delta==0 else negative).append((changed,item))
        summary[kind] += 1
        entries.append((support,kind,after,quota_change))
    digest = hashlib.sha256()
    supports_digest = hashlib.sha256()
    for entry in sorted(entries):
        digest.update((json.dumps(entry,separators=(',',':'))+'\n').encode())
        supports_digest.update((json.dumps(entry[0],separators=(',',':'))+'\n').encode())
    return {'color_counts':values,'phi':gate.score(rows),'counts':dict(sorted(summary.items())),
            'admissible_K5_delta_histogram':{str(k):v for k,v in sorted(histogram.items())},
            'canonical_supports_sha256':supports_digest.hexdigest(),
            'canonical_projected_classification_sha256':digest.hexdigest()},neutral,negative


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,required=True)
    parser.add_argument('--max-states',type=int,default=128)
    parser.add_argument('--resume',action='store_true')
    args = parser.parse_args()
    require(args.max_states>0,'positive state bound required')
    require(hashlib.sha256(SEED.read_bytes()).hexdigest()==SEED_SHA,'seed pin')
    parent = load_parent()
    gate,count = parent.dependencies()
    initial = tuple(int(x,16) for x in json.loads(SEED.read_text())['red_adjacency_hex'])
    source_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    table = gate.lifting_rows(initial)
    require(count.counts(initial)==(172,186) and gate.lifted(initial,table,range(43)),'seed invariants')
    if args.resume:
        state = json.loads((args.work/'checkpoint.json').read_text())
        require(state['seed_sha256']==SEED_SHA and state['source_sha256']==source_sha
                and state['max_states']==args.max_states,'resume contract mismatch')
    else:
        require(not args.work.exists(),'fresh work directory required')
        args.work.mkdir(parents=True)
        state = {'seed_sha256':SEED_SHA,'source_sha256':source_sha,'max_states':args.max_states,
                 'level':LEVEL,'graphs':[[format(x,'x') for x in initial]],'parents':[None],
                 'parent_moves':[None],'records':[],'negative_exits':[],'elapsed_seconds':0.0}
    nodes = [tuple(int(x,16) for x in graph) for graph in state['graphs']]
    require(nodes and nodes[0]==initial and len(set(nodes))==len(nodes),'resume graphs')
    ids = {graph:i for i,graph in enumerate(nodes)}
    start = time.monotonic()
    elapsed_before = state['elapsed_seconds']
    def save_state():
        state['elapsed_seconds'] = elapsed_before+time.monotonic()-start
        count.save(args.work/'checkpoint.json',state)
    status = 'STATE_LIMIT'
    while len(state['records'])<args.max_states:
        index = len(state['records'])
        if index==len(nodes):
            status = 'NEUTRAL_COMPONENT_CLOSED'
            break
        if (args.work/'STOP').exists():
            status = 'STOPPED_AT_STATE_BOUNDARY'
            break
        record,neutral,negative = census(nodes[index],parent,gate,count,table)
        adjacent = []
        for graph,item in neutral:
            if graph not in ids:
                ids[graph] = len(nodes)
                nodes.append(graph)
                state['graphs'].append([format(x,'x') for x in graph])
                state['parents'].append(index)
                state['parent_moves'].append(item['move'])
            adjacent.append(ids[graph])
        for graph,item in negative:
            state['negative_exits'].append(dict(item,source=index))
        record.update(node=index,neutral_neighbors=sorted(adjacent),negative_exit_count=len(negative))
        state['records'].append(record)
        save_state()
        print(json.dumps({'processed':len(state['records']),'discovered':len(nodes),'node':index,
                          'neutral_neighbors':sorted(adjacent),'negative_exits':len(negative)},sort_keys=True),flush=True)
    if len(state['records'])==len(nodes):
        status = 'NEUTRAL_COMPONENT_CLOSED'
    state['status'] = status
    save_state()
    component = {'format':'r55-actual-k5-neutral-component-v1','seed_sha256':SEED_SHA,
                 'level':LEVEL,'graphs':state['graphs'],'parents':state['parents'],
                 'parent_moves':state['parent_moves']}
    count.save(args.work/'COMPONENT.json',component)
    result = {'status':status,'processed':len(state['records']),'discovered':len(nodes),
              'level':LEVEL,'records':state['records'],'negative_exits':state['negative_exits'],
              'seed_sha256':SEED_SHA,'source_sha256':source_sha,'max_states':args.max_states,
              'elapsed_seconds':round(state['elapsed_seconds'],6),
              'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    count.save(args.work/'result.json',result)
    if state['negative_exits']:
        # Preserve a best one-edge exit, but do not search its lower level.
        best = min(state['negative_exits'],key=lambda item:(sum(item['color_counts']),item['source'],item['move']))
        segment = [best['move']]
        cursor = best['source']
        while state['parents'][cursor] is not None:
            segment.append(state['parent_moves'][cursor])
            cursor = state['parents'][cursor]
        segment.reverse()
        count.save(args.work/'EXIT_PATH.json',{'seed_sha256':SEED_SHA,'moves':segment,
                                              'source_component_vertex':best['source']})
        endpoint = gate.flip(nodes[best['source']],best['move'])
        count.save(args.work/'EXIT_GRAPH.json',{'format':'r55-triple-degree-exact-mixed-graph-v1',
                                               'red_adjacency_hex':[format(x,'x') for x in endpoint]})
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','negative_exits')},sort_keys=True),flush=True)


if __name__=='__main__':
    main()
