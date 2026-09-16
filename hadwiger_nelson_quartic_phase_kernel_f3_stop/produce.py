"""Build the frozen one-round F3 completion of the quartic phase kernel."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse, hashlib, json

Z4=(F(0),)*4
O4=(F(1),F(0),F(0),F(0))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def scale(a,q): return tuple(q*x for x in a)
def mul(a,b):
    c=[F(0)]*4
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[(i+j)%4]+=x*y*(12 if i+j>=4 else 1)
    return tuple(c)
def ca(a,b): return add(a[0],b[0]),add(a[1],b[1])
def cn(a): return neg(a[0]),neg(a[1])
def cs(a,b): return ca(a,cn(b))
def cm(a,b): return sub(mul(a[0],b[0]),mul(a[1],b[1])),add(mul(a[0],b[1]),mul(a[1],b[0]))
def norm(a,b):
    x,y=cs(a,b); return add(mul(x,x),mul(y,y))

ZERO=(Z4,Z4); ONE=(O4,Z4)
SQRT3=(F(0),F(0),F(1,2),F(0)); ETA=(F(0),F(1),F(0),F(0))
OMEGA=(scale(O4,F(1,2)),scale(SQRT3,F(1,2)))
U=[ONE]
for _ in range(5): U.append(cm(U[-1],OMEGA))

def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()

def source():
    zeta=U[2]; a1=U[4]
    u=(scale(SQRT3,F(1,2)),scale(O4,F(-1,2)))
    y=cm(u,(scale(sub(O4,SQRT3),F(1,2)),scale(ETA,F(1,2))))
    z=cm(u,(scale(sub(O4,SQRT3),F(1,2)),scale(ETA,F(-1,2))))
    centres=[ZERO,a1,cs(cn(ONE),y),ca(cn(zeta),z)]
    tips=[cn(ONE),cn(zeta)]
    cross=[(0,2),(0,3),(1,2),(1,3)]
    roots=[sorted([tips[j-2],cs(ca(centres[i],centres[j]),tips[j-2])]) for i,j in cross]
    directions=[set(),set()]
    for group in range(2):
        seeds=[cs(centres[2*group+1],centres[2*group])]
        for (i,j),row in zip(cross,roots):
            seeds.extend(cs(x,centres[i if group==0 else j]) for x in row)
        for seed in seeds: directions[group].update(cm(seed,r) for r in U)
    points=sorted({ca(c,d) for h,c in enumerate(centres) for d in directions[h//2]})
    return points

def edges(points):
    return [(i,j) for i,j in combinations(range(len(points)),2) if norm(points[i],points[j])==O4]

def colour3(adjacency):
    n=len(adjacency); colours=[-1]*n; masks=[0]*n; degree=list(map(len,adjacency)); nodes=0
    first=max(range(n),key=lambda v:(degree[v],-v)); colours[first]=0
    for w in adjacency[first]: masks[w]|=1
    def search(done):
        nonlocal nodes
        nodes+=1
        if done==n: return tuple(colours)
        v=max((w for w in range(n) if colours[w]<0),key=lambda w:(masks[w].bit_count(),degree[w],-w))
        used=0
        for c in colours:
            if c>=0: used|=1<<c
        for c in range(min(2,used.bit_length())+1):
            bit=1<<c
            if masks[v]&bit: continue
            colours[v]=c; changed=[]
            for w in adjacency[v]:
                if colours[w]<0 and not masks[w]&bit:
                    masks[w]|=bit; changed.append(w)
            answer=search(done+1)
            if answer is not None: return answer
            for w in changed: masks[w]^=bit
            colours[v]=-1
        return None
    answer=search(1)
    if answer is None: raise ValueError('frozen support unexpectedly not three-colourable')
    return answer,nodes

def build():
    old=source(); old_set=set(old); old_edges=edges(old)
    adjacency=[set() for _ in old]
    for i,j in old_edges: adjacency[i].add(j); adjacency[j].add(i)
    candidates=set()
    for r in range(len(old)):
        for p,q in combinations(sorted(adjacency[r]),2):
            x=cs(ca(old[p],old[q]),old[r])
            if x not in old_set: candidates.add(x)
    hist={}
    selected=[]
    for x in sorted(candidates):
        contacts=sum(norm(x,v)==O4 for v in old)
        hist[contacts]=hist.get(contacts,0)+1
        if contacts>=3: selected.append(x)
    points=sorted(old+selected); graph_edges=edges(points)
    adj=[set() for _ in points]
    for i,j in graph_edges: adj[i].add(j); adj[j].add(i)
    colouring,nodes=colour3(adj)
    old_indices=[points.index(v) for v in old]
    edge_set=set(graph_edges)
    triangle=next((i,j,k) for i,j,k in combinations(old_indices,3)
                  if (i,j) in edge_set and (i,k) in edge_set and (j,k) in edge_set)
    return {
      'schema':1,'source_vertices':len(old),'source_edges':len(old_edges),
      'completion_threshold':3,'all_new_candidates':len(candidates),
      'candidate_contact_histogram':[[k,hist[k]] for k in sorted(hist)],
      'selected_new_points':len(selected),'vertices':len(points),'edges':len(graph_edges),
      'source_index_sha256':digest(old_indices),'point_sha256':digest([encode(v) for v in points]),
      'edge_sha256':digest(graph_edges),'colouring':''.join(map(str,colouring)),
      'colour_search_nodes':nodes,'source_triangle':list(triangle),'chromatic_number':3,
      'target_found':False
    }

def encode(point):
    return [[[x.numerator,x.denominator] for x in axis] for axis in point]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',required=True); args=ap.parse_args()
    data=build(); Path(args.out).write_bytes(raw(data)); print(json.dumps(data,indent=2))
if __name__=='__main__': main()
