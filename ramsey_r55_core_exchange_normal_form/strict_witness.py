"""A complete all-red-task countermodel schema to redundancy of the new rule."""
from itertools import combinations
from exchange import need, encode, validate, violations
from catalog import obtain, adjacency


def witness(data,q,index):
    n=43-4*q;C=adjacency(obtain(data)[n][index])
    v0=min(range(n),key=lambda v:sum(C[v]));d=sum(C[v0])
    need(d<n-1,'complete core is outside this strictness schema')
    a=[[0]*43 for _ in range(43)];blocks=[list(range(4*b,4*b+4)) for b in range(q)];core=list(range(4*q,43))
    for B in blocks:
        for u,v in combinations(B,2):a[u][v]=a[v][u]=1
    ordinary=[[int((j-i)%4 in (0,1)) for j in range(4)] for i in range(4)]
    order=sorted(range(4),key=lambda j:sum(ordinary[i][j]<<i for i in range(4)),reverse=True)
    root=[[ordinary[i][j] for j in order] for i in range(4)]
    for b,c in combinations(range(q),2):
        M=root if b==0 else ordinary
        for i,u in enumerate(blocks[b]):
            for j,v in enumerate(blocks[c]):a[u][v]=a[v][u]=M[i][j]
    for u,v in combinations(range(n),2):a[core[u]][core[v]]=a[core[v]][core[u]]=C[u][v]
    for w in (1,2,3):a[w][core[v0]]=a[core[v0]][w]=1
    for v in [v for v in core if v!=core[v0]][:d+1]:a[0][v]=a[v][0]=1
    validate(a,blocks,[],core)
    need(any(e['vertex']==core[v0] and e['displaced']==0 for e in violations(a,blocks,[],core)),'strict exchange')
    # Explicit unrelated red K5; this is a carrier assignment, never good43.
    bad=[4*b for b in range(1,6)]
    need(all(a[u][v] for u,v in combinations(bad,2)),'declared non-target defect')
    return dict(encode(a),red=blocks,blue=[],core=core,task=f'bo1-q{q}-r{q}-c{index:06d}',known_red_K5=bad)

if __name__=='__main__':
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser();p.add_argument('data');p.add_argument('q',type=int);p.add_argument('index',type=int);p.add_argument('out');x=p.parse_args()
    Path(x.out).write_text(json.dumps(witness(x.data,x.q,x.index),sort_keys=True,indent=2)+'\n')
