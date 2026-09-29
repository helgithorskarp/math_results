"""Complete monotone halo-closure encoding for upper bounds."""
from collections import defaultdict,deque
from geometry import normalize,halo,orientations,contacts,transform_between,transform
from exact_cover import enumerate_exact
from pysat.card import CardEnc,EncType
from pysat.formula import IDPool
def encode(cells,k,max_placements=40000):
    os=orientations(cells);oid={o:i for i,o in enumerate(os)}
    local=contacts(cells)
    if k>=3:
        stats,sols=enumerate_exact(cells,local,limit=100000)
        if stats['complete']:
            ids={i for sol in sols for i in sol};local=[t for i,t in enumerate(local) if i in ids]
    adj=[]
    for o in os:
        g=transform_between(cells,o)
        a=set()
        for t in local:
            u=transform(g,t);x,y=min(u);a.add((oid[normalize(u)],x,y))
        adj.append(sorted(a))
    def footprint(p):
        o,x,y=p
        return tuple((u+x,v+y) for u,v in os[o])
    root=(oid[cells],0,0);ds={root:0};queue=deque([root]);base=set(cells)
    while queue:
        p=queue.popleft();d=ds[p]
        if d==k:continue
        i,x,y=p
        for j,a,b in adj[i]:
            q=(j,x+a,y+b)
            if q in ds or not base.isdisjoint(footprint(q)):continue
            ds[q]=d+1;queue.append(q)
        if len(ds)>max_placements:raise RuntimeError('Placement limit exceeded; incomplete')
    ps=sorted(ds,key=lambda p:(ds[p],p));pool=IDPool();z={}
    for p in ps:
        for i in range(ds[p],k+1):z[p,i]=pool.id((p,i))
    clauses=[[z[root,0]]];at=defaultdict(list)
    for p in ps:
        for cell in footprint(p):at[cell].append(p)
        for i in range(ds[p],k):clauses.append([-z[p,i],z[p,i+1]])
    for cell,qs in sorted(at.items()):
        if len(qs)>1:
            clauses.extend(CardEnc.atmost([z[q,k] for q in qs],bound=1,vpool=pool,
                                           encoding=EncType.seqcounter).clauses)
    for p in ps:
        for i in range(ds[p],k):
            for cell in sorted(halo(footprint(p))):
                clauses.append([-z[p,i]]+[z[q,i+1] for q in at[cell] if ds[q]<=i+1])
        if len(clauses)>1200000:raise RuntimeError('Clause limit exceeded; incomplete')
    return clauses,ps,z,footprint,ds,pool.top
