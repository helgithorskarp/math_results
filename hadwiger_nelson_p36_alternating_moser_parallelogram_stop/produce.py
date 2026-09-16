"""Produce the frozen alternating-Moser four-P36 parallelogram certificate."""
from collections import Counter, deque
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json

# Scalar coordinates use (1,sqrt(3),sqrt(11),sqrt(33)).
ZERO4=(F(0),)*4
ONE4=(F(1),F(0),F(0),F(0))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,q): return tuple(q*x for x in a)
def mul(a,b):
    out=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            common=i&j
            out[i^j]+=x*y*(3 if common&1 else 1)*(11 if common&2 else 1)
    return tuple(out)
def p_add(p,q): return add(p[0],q[0]),add(p[1],q[1])
def p_sub(p,q): return sub(p[0],q[0]),sub(p[1],q[1])
def norm(p,q):
    x,y=p_sub(p,q); return add(mul(x,x),mul(y,y))
ZERO=(ZERO4,ZERO4)

def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()
def encode(point):
    return [[[x.numerator,x.denominator] for x in axis] for axis in point]

def patch():
    rows=[]
    for a in range(-12,13):
        for b in range(-12,13):
            if a*a+a*b+b*b<=36:
                point=((F(2*a+b,2),F(0),F(0),F(0)),(F(0),F(b,2),F(0),F(0)))
                rows.append((point,(a,b)))
    rows.sort()
    return [p for p,_ in rows],[label for _,label in rows]

def rho(point):
    x,y=point; sqrt11six=(F(0),F(0),F(1,6),F(0))
    return add(scale(x,F(5,6)),neg(mul(sqrt11six,y))),add(mul(sqrt11six,x),scale(y,F(5,6)))

def graph():
    P,labels=patch()
    v=((F(11),F(0),F(0),F(0)),(F(0),F(0),F(1),F(0)))
    w=((F(-11,2),F(0),F(0),F(-1,2)),(F(0),F(11,2),F(-1,2),F(0)))
    c=p_add(v,w)
    patches=[P,[p_add(v,rho(p)) for p in P],[p_add(c,p) for p in P],[p_add(w,rho(p)) for p in P]]
    occurrences={}
    for k,Q in enumerate(patches):
        for j,p in enumerate(Q): occurrences.setdefault(p,[]).append((k,j))
    points=sorted(occurrences); index={p:i for i,p in enumerate(points)}
    edges=[(i,j) for i,j in combinations(range(len(points)),2) if norm(points[i],points[j])==ONE4]
    patch_edges=[(i,j) for i,j in combinations(range(len(P)),2) if norm(P[i],P[j])==ONE4]
    inherited=set()
    for Q in patches:
        for i,j in patch_edges: inherited.add(tuple(sorted((index[Q[i]],index[Q[j]]))))
    collision_pairs=Counter()
    for rows in occurrences.values():
        owners=sorted({k for k,_ in rows})
        for a,b in combinations(owners,2): collision_pairs[a,b]+=1
    return P,labels,patches,points,occurrences,edges,patch_edges,inherited,collision_pairs

def tarjan(adjacency):
    n=len(adjacency); disc=[-1]*n; low=[0]*n; parent=[-1]*n
    time=0; articulations=set(); bridges=[]; components=0
    def visit(u):
        nonlocal time
        disc[u]=low[u]=time; time+=1; children=0
        for v in adjacency[u]:
            if disc[v]<0:
                parent[v]=u; children+=1; visit(v); low[u]=min(low[u],low[v])
                if parent[u]<0 and children>1: articulations.add(u)
                if parent[u]>=0 and low[v]>=disc[u]: articulations.add(u)
                if low[v]>disc[u]: bridges.append(tuple(sorted((u,v))))
            elif v!=parent[u]: low[u]=min(low[u],disc[v])
    for u in range(n):
        if disc[u]<0: components+=1; visit(u)
    return components,articulations,bridges

def build():
    P,labels,patches,points,occurrences,edges,patch_edges,inherited,collision_pairs=graph()
    adjacency=[set() for _ in points]
    for a,b in edges: adjacency[a].add(b); adjacency[b].add(a)
    components,articulations,bridges=tarjan(adjacency)
    degrees=list(map(len,adjacency)); alive=[True]*len(points); queue=deque(i for i,d in enumerate(degrees) if d<4); peel=[]
    while queue:
        u=queue.popleft()
        if not alive[u]: continue
        alive[u]=False; peel.append(u)
        for v in sorted(adjacency[u]):
            if alive[v]:
                degrees[v]-=1
                if degrees[v]==3: queue.append(v)
    index={p:i for i,p in enumerate(points)}
    word=[]
    for p in points:
        colours={(labels[j][0]-labels[j][1])%3 for _,j in occurrences[p]}
        if len(colours)!=1: raise ValueError('collision has inconsistent residue colours')
        word.append(str(colours.pop()))
    if any(word[a]==word[b] for a,b in edges): raise ValueError('residue word failed')
    source_triangle=[index[patches[0][labels.index(x)]] for x in [(0,0),(0,1),(1,0)]]
    if not all(tuple(sorted(e)) in set(edges) for e in combinations(source_triangle,2)): raise ValueError('triangle failed')
    collisions=[]
    for p,rows in sorted(occurrences.items()):
        if len(rows)>1: collisions.append([[k,*labels[j]] for k,j in rows])
    patch_adj=[set() for _ in range(4)]
    for a,b in collision_pairs: patch_adj[a].add(b); patch_adj[b].add(a)
    pcom,parts,pbridges=tarjan(patch_adj)
    return {
      'schema':1,'rho':'(5+i*sqrt(11))/6','translation_v':'11+i*sqrt(11)','translation_w':'omega^2*v',
      'patch_vertices':len(P),'patch_edges':len(patch_edges),'raw_labels':4*len(P),
      'vertices':len(points),'edges':len(edges),'collision_multiplicity_histogram':sorted([list(x) for x in Counter(map(len,occurrences.values())).items()]),
      'collisions':collisions,'patch_collision_pairs':[[a,b,n] for (a,b),n in sorted(collision_pairs.items())],
      'extra_edges_beyond_inherited_union':len(set(edges)-inherited),'inherited_union_edges':len(inherited),
      'physical_components':components,'physical_articulations':len(articulations),'physical_bridges':len(bridges),
      'patch_contact_components':pcom,'patch_contact_articulations':len(parts),'patch_contact_bridges':len(pbridges),
      'four_core_vertices':sum(alive),'four_core_patch_memberships':[],
      'peel_order_sha256':digest(peel),'colouring':''.join(word),'source_triangle':source_triangle,
      'chromatic_number':3,'point_sha256':digest(list(map(encode,points))),'edge_sha256':digest(edges),
      'target_found':False
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); args=ap.parse_args()
    data=build(); Path(args.out).write_bytes(raw(data)); print(json.dumps(data,indent=2))
if __name__=='__main__': main()
