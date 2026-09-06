"""Degree-correct physical fixtures and negative controls; no Ramsey search."""
from itertools import combinations
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json,random
import derive,extract,verify,check

ROOT=Path(__file__).resolve().parent


def need(ok,msg):
    if not ok:raise ValueError(msg)


def havel(degrees):
    d=dict(degrees);edges=set()
    while any(d.values()):
        order=sorted(d,key=lambda v:(-d[v],v));v=order[0];k=d[v];d[v]=0
        neighbors=[u for u in order[1:] if d[u]>0]
        need(0<k<=len(neighbors),'fixture sequence is not graphical')
        for u in neighbors[:k]:edges.add(tuple(sorted((u,v))));d[u]-=1
    return edges


def graph(kind,orientation,seed):
    edges={tuple(e) for e in derive.produce()[0]['core_red_edges']}
    types=[i for i,count in enumerate([4,5,4,5,4]) for _ in range(count)]
    for j in range(23):
        for bag in range(4):
            if j<22:
                i=types[j];local={i,(i+1)%5} if bag in (0,3) else {(2*i)%5,(2*(i+1))%5}
            else:local={0}
            for v in range(5):
                red=(v not in local) if bag in (0,3) else (v in local)
                if red:edges.add((5*bag+v,20+j))
    desired={v:(9 if v<22 else 10 if v<27 else 11) for v in range(20,43)}
    if kind=='blue_four':
        offset=0;right=list(range(29,43));degrees={v:11 for v in right}
        for v in range(20,29):
            for i in range(desired[v]):
                u=right[(offset+i)%14];edges.add((v,u));degrees[u]-=1
            offset+=desired[v]
        edges|=havel(degrees)
    else:edges|=havel(desired)
    if kind=='bad_star':
        for e in ((0,29),(2,20)):
            need(e in edges,'rectangle red');edges.remove(e)
        for e in ((0,20),(2,29)):
            need(e not in edges,'rectangle blue');edges.add(e)
    labels=list(range(43));random.Random(seed).shuffle(labels)
    if not orientation:edges=set(combinations(range(43),2))-edges
    return {'n':43,'core_embedding':labels[:20],'core_color':orientation,
            'red_edges':sorted([sorted((labels[u],labels[v])) for u,v in edges])}


def star_count(g):
    a,core,_=extract.read_graph(g);qs=[[],[]]
    for q in combinations(core,4):
        colors={int(a[u][v]) for u,v in combinations(q,2)}
        if len(colors)==1:qs[next(iter(colors))].append(q)
    return sum(not any(all(a[x][v]==bool(c) for v in q) for c in (0,1) for q in qs[c])
               for x in set(range(43))-set(core))


def fixtures():
    return [{'kind':kind,'graph':g,'certificate':extract.extract(g)}
            for kind in ('red_triangle','blue_four','bad_star') for orientation in (0,1)
            for g in [graph(kind,orientation,21620)]]


def main():
    counts=Counter();valid_stars=Counter()
    expected={'red_triangle':'edge_class_red_triangle','blue_four':'edge_class_blue_four','bad_star':'one_vertex_attachment'}
    for kind in expected:
        for orientation in (0,1):
            for seed in range(8):
                g=graph(kind,orientation,21620+seed);w=extract.extract(g);answer=verify.verify(g,w)
                need(answer['mechanism']==expected[kind],'decoder mechanism')
                count=star_count(g)
                need((count==23) if kind!='bad_star' else (count<23),'one-vertex feasibility control')
                counts[answer['mechanism']]+=1;valid_stars[str(count)]+=1
    transfers=0
    for degree in (19,20):
        for orientation in (0,1):
            moved=graph('red_triangle',1,21620)
            a,ids,_=extract.read_graph(moved);core_vertex=ids[0]
            outside=set(range(43))-set(ids)
            recipient=next(v for v in sorted(outside) if sum(a[v])==degree)
            choices=[x for x in sorted(outside) if x!=recipient and a[core_vertex][x] and not a[recipient][x]]
            need(len(choices)>=21-degree,'degree-class transfer fixture')
            edges={tuple(e) for e in moved['red_edges']}
            for x in choices[:21-degree]:
                edges.remove(tuple(sorted((core_vertex,x))));edges.add(tuple(sorted((recipient,x))))
            if not orientation:edges=set(combinations(range(43),2))-edges
            moved['red_edges']=[list(e) for e in sorted(edges)];moved['core_color']=orientation
            b,_,_=extract.read_graph(moved);need(sum(b[core_vertex])==degree,'low degree inside core')
            answer=verify.verify(moved,extract.extract(moved));counts[answer['mechanism']]+=1
            valid_stars[str(star_count(moved))]+=1;transfers+=1
    fs=fixtures();need(fs==json.loads((ROOT/'fixtures.json').read_text()),'fixture reproduction')
    g=fs[0]['graph'];w=fs[0]['certificate'];mutations=0
    for f in (lambda x:x.update(color=1-x['color']),lambda x:x['five'].__setitem__(1,x['five'][0]),
              lambda x:x['five'].__setitem__(0,43),lambda x:x.update(mechanism='wrong')):
        bad=deepcopy(w);f(bad)
        try:verify.verify(g,bad)
        except ValueError:mutations+=1
        else:raise ValueError('bad physical certificate accepted')
    malformed=0
    for f in (lambda x:x.update(n=42),lambda x:x.update(core_color=True),lambda x:x['red_edges'].append(x['red_edges'][0]),
              lambda x:x['core_embedding'].__setitem__(1,x['core_embedding'][0]),lambda x:x['red_edges'].pop(),
              lambda x:x['red_edges'].append([0,43])):
        bad=deepcopy(g);f(bad)
        for fn in (extract.extract,lambda x:verify.verify(x,w)):
            try:fn(bad)
            except ValueError:pass
            else:raise ValueError('bad family input accepted')
        malformed+=1
    kernel_mutations=0;kernel=json.loads((ROOT/'certificate.json').read_text())
    for f in (lambda x:x.update(ordinary_star_minimum=21),lambda x:x['farkas_multipliers'].__setitem__(5,1),
              lambda x:x['class_pair_supports'][0].update(common_blue=0),lambda x:x.update(admissible_stars=14640)):
        bad=deepcopy(kernel);f(bad)
        try:check.verify(bad)
        except ValueError:kernel_mutations+=1
        else:raise ValueError('bad kernel certificate accepted')
    return {'status':'VERIFIED_LIVE_PROFILE_PHYSICAL_CONTROLS' ,'physical43_graphs':sum(counts.values()),
            'mechanisms':dict(sorted(counts.items())),'admissible_star_counts':dict(sorted(valid_stars.items())),
            'profile_class_transfers':transfers,'kernel_mutations_rejected':kernel_mutations,'certificate_mutations_rejected':mutations,'malformed_inputs_rejected_by_both':malformed,'fixtures':len(fs)}

if __name__=='__main__':print(json.dumps(main(),indent=2))
