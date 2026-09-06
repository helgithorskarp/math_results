"""Physical monochromatic-five extractor for the complete stated profile branch."""
from itertools import combinations
import json


def read_graph(data):
    if type(data.get('n')) is not int or data['n']!=43:raise ValueError('order 43 required')
    ids=data.get('core_embedding');orientation=data.get('core_color')
    if not isinstance(ids,list) or len(ids)!=20 or any(type(v) is not int or not 0<=v<43 for v in ids) or len(set(ids))!=20:raise ValueError('20 distinct core labels')
    if type(orientation) is not int or orientation not in (0,1):raise ValueError('core color')
    if not isinstance(data.get('red_edges'),list):raise ValueError('edge list')
    physical=[[False]*43 for _ in range(43)];seen=set()
    for e in data['red_edges']:
        if not isinstance(e,list) or len(e)!=2 or any(type(v) is not int for v in e):raise ValueError('edge syntax')
        u,v=e
        if not 0<=u<v<43 or (u,v) in seen:raise ValueError('edge identity')
        seen.add((u,v));physical[u][v]=physical[v][u]=True
    a=[[u!=v and physical[u][v]==bool(orientation) for v in range(43)] for u in range(43)]
    if sorted(map(sum,a))!=[19]*2+[20]*5+[21]*36:raise ValueError('wrong full degree profile')
    for u,v in combinations(range(20),2):
        i,j=divmod(u,5);k,l=divmod(v,5)
        expected=(j-l)%5 in (1,4) if i==k else abs(i-k)==1
        if a[ids[u]][ids[v]]!=expected:raise ValueError('wrong induced P4[C5]')
    return a,ids,orientation


def extract(data):
    a,ids,orientation=read_graph(data)
    outside=sorted(set(range(43))-set(ids))
    fours=[[],[]]
    for q in combinations(ids,4):
        cs={int(a[u][v]) for u,v in combinations(q,2)}
        if len(cs)==1:fours[next(iter(cs))].append(q)
    def witness(c,q,mechanism):
        return {'schema':1,'color':orientation if c else 1-orientation,'five':sorted(q),'mechanism':mechanism}
    for x in outside:
        for c in (0,1):
            for q in fours[c]:
                if all(a[x][v]==bool(c) for v in q):return witness(c,[x,*q],'one_vertex_attachment')
    # Every remaining star has a red-clique missed set in the first end bag.
    classes=[[] for _ in range(5)]
    types=[{ids[i],ids[(i+1)%5]} for i in range(5)]
    for x in outside:
        missed={v for v in ids[:5] if not a[x][v]}
        if len(missed)>2 or any(not a[u][v] for u,v in combinations(missed,2)):raise RuntimeError('activity theorem mismatch')
        if len(missed)==2:classes[types.index(missed)].append(x)
    if sum(map(len,classes))<22:raise RuntimeError('global degree-count mismatch')
    for i in range(5):
        bucket=sorted(classes[i]+classes[(i+1)%5])
        if len(bucket)<9:continue
        nine=bucket[:9]
        for tri in combinations(nine,3):
            if all(a[u][v] for u,v in combinations(tri,2)):
                return witness(1,[*tri,ids[(i+3)%5],ids[(i+4)%5]],'edge_class_red_triangle')
        for four in combinations(nine,4):
            if all(not a[u][v] for u,v in combinations(four,2)):
                return witness(0,[*four,ids[(i+1)%5]],'edge_class_blue_four')
        raise RuntimeError('R(3,4) theorem mismatch')
    raise RuntimeError('five-class averaging mismatch')

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('graph');args=p.parse_args()
    print(json.dumps(extract(json.load(open(args.graph))),indent=2))
