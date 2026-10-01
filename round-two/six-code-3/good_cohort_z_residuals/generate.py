"""Deterministic positive colors; search failure is never an exclusion.

Bit masks and greedy DSATUR, at most64 fixed seeded priority orders per
new interface. The two previously published seed colorings are credited inputs.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

BRIDGE_PIN='9239f6cfcb413ff8a76eddf172ebd62abdec46aec7c8c87c788c2370e856d1d2'
SEED_PIN='521f0b322523a340c302fa5f4ea86fd3803a73e3665194e8cff556c0d0635ff6'

def need(test,message):
    if not test:
        raise ValueError(message)

def color(adjacency,priority):
    colors=[-1]*len(adjacency)
    seen=[0]*len(adjacency)
    todo=set(range(len(adjacency)))
    degree=[a.bit_count() for a in adjacency]
    while todo:
        v=max(todo,key=lambda i:(seen[i].bit_count(),degree[i],priority[i]))
        c=0
        while seen[v]>>c&1:
            c+=1
        colors[v]=c
        todo.remove(v)
        neighbors=adjacency[v]
        while neighbors:
            bit=neighbors&-neighbors
            seen[bit.bit_length()-1]|=1<<c
            neighbors^=bit
    return colors

def generate(bridge,seeds):
    rows=bridge['raw_positive_maps']
    need(len(rows)==34,'incomplete raw carrier input')
    entries=[]
    for index,row in enumerate(rows):
        begin=time.monotonic()
        core=row['word_masks']
        centers={17,row['first'][1][2]}
        candidates=[sum(1<<p for p in q) for q in itertools.combinations(sorted(set(range(18))-centers),5)]
        candidates=[m for m in candidates if all((m&w).bit_count()<=2 for w in core)]
        adjacency=[0]*len(candidates)
        edges=0
        for i,j in itertools.combinations(range(len(candidates)),2):
            if (candidates[i]&candidates[j]).bit_count()<=2:
                adjacency[i]|=1<<j
                adjacency[j]|=1<<i
                edges+=1
        matching=[s for s in seeds['seeds'] if s['core_masks']==core]
        if matching:
            need(len(matching)==1,'ambiguous credited seed')
            best=matching[0]['colors']
        else:
            best=color(adjacency,[-i for i in range(len(candidates))])
            for trial in range(64):
                if max(best)<28:
                    break
                need(time.monotonic()-begin<=5,'INCOMPLETE5s product search guard')
                priority=list(range(len(candidates)))
                random.Random(20261001+1000*index+trial).shuffle(priority)
                colors=color(adjacency,priority)
                if max(colors)<max(best):
                    best=colors
        need(time.monotonic()-begin<=5,'INCOMPLETE5s product guard')
        need(len(best)==len(candidates),'color domain differs')
        need(all(best[i]!=best[j] for i,j in itertools.combinations(range(len(candidates)),2)
                 if adjacency[i]>>j&1),'improper generated positive color')
        capacity=max(best)+1
        entries.append(dict(index=index,product_index=row['product_index'],candidate_count=len(candidates),
                            edges=edges,candidate_sha256=hashlib.sha256(json.dumps(candidates,separators=(',',':')).encode()).hexdigest(),
                            colors=best,capacity=capacity,upper_bound=36+capacity,
                            triangle_count=len(row['triangle_points']),first_fixture=row['first'][0]))
    return dict(agent='six-code-3',role='researcher',
                scope='Every34 raw good-cohort/Z normalized union, without local covered-triangle premise; complete carrier imported from9045. Proper-color upper bounds only; no sharpness or lambda_xu=3 conclusion.',
                entries=entries)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--bridge',required=True)
    parser.add_argument('--seeds',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    raw=Path(args.bridge).read_bytes()
    seed_raw=Path(args.seeds).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==BRIDGE_PIN,'raw carrier pin differs')
    need(hashlib.sha256(seed_raw).hexdigest()==SEED_PIN,'credited seed pin differs')
    result=generate(json.loads(raw),json.loads(seed_raw))
    Path(args.output).write_text(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps(dict(status='GENERATED_POSITIVE_CERTIFICATE',interfaces=len(result['entries']),
                         maximum_upper_bound=max(r['upper_bound'] for r in result['entries']))))

if __name__=='__main__':
    main()
