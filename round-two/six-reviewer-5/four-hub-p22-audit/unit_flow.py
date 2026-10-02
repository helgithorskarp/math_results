"""Every <=15-edge unit graph checked by residual distinct-edge max flow.
An exact binary unit graph is enlarged by arbitrary feasible U--C flow;
no existence of ambient stars/codes is inferred from a passing mask.
"""
from independent import *

def flow(cap,allowed,demand):
    # Edmonds--Karp, integer capacities, U--C arcs have capacity1.
    m=len(demand);n=len(cap);N=m+n+2;s=N-2;t=N-1;A=[[0]*N for _ in range(N)]
    for u,v in enumerate(demand):A[s][u]=v
    for c,v in enumerate(cap):A[m+c][t]=v
    for u,c in allowed:A[u][m+c]=1
    value=0
    while True:
        prev={s:None};queue=[s]
        for a in queue:
            for b in range(N):
                if A[a][b]>0 and b not in prev:prev[b]=a;queue.append(b)
            if t in prev:break
        if t not in prev:return value
        b=t;aug=10**9
        while prev[b] is not None:a=prev[b];aug=min(aug,A[a][b]);b=a
        b=t
        while prev[b] is not None:a=prev[b];A[a][b]-=aug;A[b][a]+=aug;b=a
        value+=aug

def mask_check(V,case,graph):
    U,A,C,B,D,I,C1,R=metric(V);pot={(a,b):set(col) for a,b,col in graph['potential']};forced={(a,b):j for a,b,j in graph['forced']}
    edges=[pair for pair,col in sorted(pot.items()) if pair[0] in U and pair[1] in U and 0 in col]
    need(len(edges)<=15,'INCOMPLETE fixed15 potentialunitedge guard')
    fmask=sum(1<<j for j,pair in enumerate(edges) if pair in forced)
    start=start_guard();bits=[];stats=collections.Counter()
    fc=[sum(a in pair and j==0 for pair,j in forced.items()) for a in C]
    cap=[V[a][2][0]-x for a,x in zip(C,fc)]
    forceduc=[sum(a in pair and ((pair[1] if pair[0]==a else pair[0]) in C) and j==0 for pair,j in forced.items()) for a in U]
    allowed=[(u,c) for u,a in enumerate(U) for c,b in enumerate(C) if tuple(sorted((a,b))) in pot and 0 in pot[tuple(sorted((a,b)))] and tuple(sorted((a,b))) not in forced]
    for mask in range(1<<len(edges)):
        reason='accepted'
        if mask&fmask!=fmask:reason='forced_internal_edge'
        degree={a:0 for a in U};nbr={a:set() for a in U}
        if reason=='accepted':
            for j,(a,b) in enumerate(edges):
                if mask>>j&1:degree[a]+=1;degree[b]+=1;nbr[a].add(b);nbr[b].add(a)
            demand=[V[a][2][0]-degree[a]-f for a,f in zip(U,forceduc)]
            if any(v<0 for v in demand) or any(v<0 for v in cap):reason='degree'
            elif case['tau']==0 and any(sum(b in nbr[a] for a,b in it.combinations(nbr[r],2))>(sum(V[r][2])*(sum(V[r][2])-1)//2-(V[r][1][4]-1-V[r][1][2])) for r in U):reason='internal_triangle'
            elif flow(cap,allowed,demand)<sum(demand):reason='residual_distinct_edge_flow'
        stats[reason]+=1;bits.append(int(reason=='accepted'))
        if mask%256==0:guard(start,mask+1,32768,10)
    return {'potential_unit_edges':edges,'forced_mask':fmask,'all_mask_accept_bits':bits,'outcomes':dict(stats),'accepted':sum(bits)}

def compute():
    data=json.loads((P/'independent-census.json').read_text());records=[];surv=[]
    for s in data['survivors']:
        V=expand_vertices(data['types'],data['histograms'],s['counts']);result=mask_check(V,s['case'],s['graph']);records.append({'case':s['case'],'counts':s['counts'],'mask_check':result})
        if result['accepted']:surv.append(s)
    out={'records':records,'survivors':surv,'all_masks':sum(len(r['mask_check']['all_mask_accept_bits']) for r in records)}
    (P/'independent-unit-flow.json').write_bytes(enc(out));print(json.dumps({'input':len(records),'remaining':len(surv),'all_masks':out['all_masks'],'sha256':sha(out)}),flush=True)
if __name__=='__main__':compute()
