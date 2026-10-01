"""Optional deterministic generator of residual color/branch certificates."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time

from produce import p

ALL_CANDIDATES=[(q,sum(1 << i for i in q),set(combinations(q,3)))
                for q in combinations(range(15),5)]


def graph(core):
    forbidden=set()
    for mask in core['blocks']:
        forbidden.update(combinations([i for i in range(15) if mask & (1 << i)],3))
    candidates=[(q,mask) for q,mask,triples in ALL_CANDIDATES if triples.isdisjoint(forbidden)]
    masks=[mask for q,mask in candidates]
    adjacent=[{j for j,b in enumerate(masks) if i!=j and (a&b).bit_count()<=2}
              for i,a in enumerate(masks)]
    return candidates,adjacent


def color(adjacent):
    # Deterministic saturation-degree coloring (the standard DSATUR heuristic).
    colors=[-1]*len(adjacent)
    forbidden=[set() for _ in adjacent]
    left=set(range(len(adjacent)))
    while left:
        vertex=max(left,key=lambda i:(len(forbidden[i]),len(adjacent[i]),-i))
        chosen=0
        while chosen in forbidden[vertex]:chosen+=1
        colors[vertex]=chosen;left.remove(vertex)
        for other in adjacent[vertex]:forbidden[other].add(chosen)
    p.require(not any(colors[i]==colors[j] for i,a in enumerate(adjacent) for j in a),
              'generator produced an improper coloring')
    return colors


def tree(adjacent,limit=21):
    start=time.monotonic();nodes=0;leaves=Counter();max_depth=0
    def visit(available,need,depth):
        nonlocal nodes,max_depth
        nodes+=1;max_depth=max(max_depth,depth)
        if nodes>2000000 or time.monotonic()-start>20:
            raise RuntimeError('INCOMPLETE residual certificate guard')
        if need<=0:
            raise RuntimeError('COUNTEREXAMPLE to the proposed residual bound')
        if len(available)<need:
            leaves['size']+=1
            return {'kind':'size'}
        induced=[{j for j,u in enumerate(available) if u in adjacent[v]} for v in available]
        colors=color(induced)
        if max(colors,default=-1)+1<need:
            leaves['color']+=1
            return {'kind':'color','colors':colors}
        branches=[]
        for i,v in enumerate(available):
            future=[u for u in available[i+1:] if u in adjacent[v]]
            if len(future)>=need-1:
                branches.append([v,visit(future,need-1,depth+1)])
        leaves['branch']+=1
        return {'kind':'branch','branches':branches}
    result=visit(list(range(len(adjacent))),limit+1,0)
    return result,{'nodes':nodes,'kinds':dict(leaves),'max_depth':max_depth}



def run(work,output,limit=None):
    summary=json.loads((work/'summary.json').read_text())
    p.require(summary['status']=='COMPLETE' and len(summary['cases'])==46,'incomplete primary coverage')
    cores=[c for case in range(46) for c in json.loads((work/f'joints-{case}.json').read_text())]
    lookup={c['core_sha256']:c for c in cores}
    certificates=[];totals=Counter();ranges=[];limits=Counter();maximum_depth=0
    for core in lookup.values():
        candidates,adjacent=graph(core)
        if limit is None:
            colors=color(adjacent)
            bound=max(colors,default=-1)+1
            proof={'kind':'color','colors':colors}
            record={'kinds':{'color':1},'max_depth':0}
        else:
            bound=limit
            proof,record=tree(adjacent,limit=bound)
        certificates.append({'core_sha256':core['core_sha256'],
                             'candidate_sha256':p.digest([q for q,mask in candidates]),
                             'candidate_count':len(candidates),'limit':bound,'tree':proof})
        ranges.append(len(candidates));limits[bound]+=1
        totals.update(record['kinds']);maximum_depth=max(maximum_depth,record['max_depth'])
    result={'format':1,'status':'COMPLETE','primary_summary_sha256':p.digest(summary),
            'raw_core_count':len(cores),'distinct_core_count':len(lookup),
            'maximum_additional_bound':max(limits,default=0),'certificates':certificates}
    output.write_bytes(p.canonical(result))
    print(json.dumps({'status':'COMPLETE_RESIDUAL_GENERATOR_ONLY','raw_cores':len(cores),
                      'distinct_cores':len(lookup),'limits':dict(sorted(limits.items())),
                      'candidate_count_range':[min(ranges,default=0),max(ranges,default=0)],
                      'maximum_total_bound':45+max(limits,default=0),
                      'kinds':dict(totals),'max_depth':maximum_depth,'sha256':p.digest(result)}),flush=True)
    return result


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--work',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--limit',type=int)
    args=ap.parse_args()
    p.require(args.limit is None or type(args.limit) is int and 0<=args.limit<=45,'capacity request')
    run(args.work,args.output,args.limit)
