"""Exact whole degree/rotation cover for q9, all degrees four. six-tammes-1 researcher.
No geometry/nonexistence verdict is inferred from an incomplete run.
"""
from itertools import combinations, permutations
from collections import Counter
import json

N=8;PAIRS=tuple(combinations(range(N),2));INDEX={p:i for i,p in enumerate(PAIRS)}
DEG=(3,3,4,4,4,4,4,4)

def need(x,m):
    if not x:raise ValueError(m)

def generate():
    rem=list(DEG);out=[]
    def visit(i,mask):
        if i==N:
            need(not any(rem),'degree sequence complete');out.append(mask);return
        k=rem[i];cand=[j for j in range(i+1,N) if rem[j]>0]
        if k<0 or k>len(cand):return
        for chosen in combinations(cand,k):
            new=mask
            for j in chosen:rem[j]-=1;new|=1<<INDEX[(i,j)]
            rem[i]=0
            # Future vertices can only acquire future neighbors now.
            if all(0<=rem[j]<=N-i-2 for j in range(i+1,N)) and sum(rem)%2==0:visit(i+1,new)
            rem[i]=k
            for j in chosen:rem[j]+=1
    visit(0,0)
    need(len(out)==len(set(out)),'unique row-generation graphs')
    return set(out)

GROUP=[]
for swap in (False,True):
    for tail in permutations(range(2,N)):
        m=((1,0) if swap else (0,1))+tail
        GROUP.append(tuple(INDEX[tuple(sorted((m[i],m[j])))] for i,j in PAIRS))
need(len(GROUP)==1440,'whole degree-preserving relabeling group')

def relabel(mask,m):
    out=0
    while mask:
        bit=mask&-mask;out|=1<<m[bit.bit_length()-1];mask-=bit
    return out

def representatives(graphs):
    todo=set(graphs);reps=[]
    while todo:
        mask=min(todo);orbit={relabel(mask,m) for m in GROUP}
        need(orbit<=todo,'whole graph orbit unprocessed')
        todo-=orbit;reps.append({'mask':mask,'orbit':len(orbit)})
    need(sum(r['orbit'] for r in reps)==len(graphs),'complete graph orbit partition')
    return reps

def adjacent(mask):
    adj=[[] for _ in range(N)]
    for k,(i,j) in enumerate(PAIRS):
        if mask>>k&1:adj[i].append(j);adj[j].append(i)
    need(tuple(map(len,adj))==DEG,'decoded graph degrees')
    return adj

def faces(rotation):
    # phi(i,j)=(j, predecessor(i) in rotation[j]); orientable face cycles.
    nxt={(i,j):(j,r[(r.index(i)-1)%len(r)]) for j,r in enumerate(rotation) for i in r}
    unseen=set(nxt);out=[]
    while unseen:
        d=min(unseen);start=d;face=[];darts=[]
        while True:
            if d not in unseen:return None
            unseen.remove(d);face.append(d[0]);darts.append(d);d=nxt[d]
            if d==start:break
        if len(face) not in (3,4) or len(set(face))!=len(face):return None
        out.append((tuple(face),tuple(darts)))
    if len(out)!=9 or Counter(map(lambda x:len(x[0]),out))!={3:6,4:3}:return None
    return out

def medial(rotation,fs):
    ed=sorted({tuple(sorted((i,j))) for i,r in enumerate(rotation) for j in r})
    ei={e:k for k,e in enumerate(ed)}
    black=[tuple(ei[tuple(sorted((i,j)))] for j in r) for i,r in enumerate(rotation)]
    white=[tuple(ei[tuple(sorted(d))] for d in darts) for f,darts in fs]
    allfaces=black+white
    Qs=[f for f in allfaces if len(f)==4];Ts=[f for f in allfaces if len(f)==3]
    # Complete-graph contact/convexity necessities: same pair cannot be
    # both an edge and a Q diagonal, or an opposite pair of two Qs.
    E={tuple(sorted((f[k],f[(k+1)%len(f)]))) for f in allfaces for k in range(len(f))}
    diag=[tuple(sorted((f[k],f[k+2]))) for f in Qs for k in range(2)]
    if len(diag)!=len(set(diag)) or set(diag)&E:return None
    need(len(E)==30,'medial degree4 edge count')
    nb=[set() for _ in ed]
    for a,b in E:nb[a].add(b);nb[b].add(a)
    need(all(len(n)==4 for n in nb),'all medial degrees four')
    tcount=Counter(v for f in Ts for v in f)
    if any(tcount[v]>2 for v in range(15)):return None
    role=Counter(tcount[v] for v in range(15))
    need(role[1]+2*role[0]==6,'six deficit T-corner count')
    return {'black':black,'white':white,'Ts':Ts,'Qs':Qs,'tcount':[tcount[v] for v in range(15)],
            'role_counts':dict(sorted(role.items()))}

def rotations_pruned(adj,counts):
    """Whole rotation product; prune only forced nonsimple/long face paths."""
    ed=sorted({tuple(sorted((i,j))) for i,r in enumerate(adj) for j in r})
    darts=tuple(d for e in ed for d in (e,e[::-1]));di={d:i for i,d in enumerate(darts)}
    tails=tuple(i for i,j in darts);succ=[-1]*len(darts);rotation=[None]*N
    orders=[tuple((r[0],)+q for q in permutations(r[1:])) for r in adj]
    after=[1]*(N+1)
    for j in range(N-1,-1,-1):after[j]=after[j+1]*len(orders[j])
    need(after[0]==186624,'whole rotation product for this degree pattern')
    def short_face_paths():
        for start in range(len(darts)):
            v=start;used=set();length=0
            while True:
                if v==start and length:
                    if length not in (3,4):return False
                    break
                if length>=4 or tails[v] in used:return False
                used.add(tails[v]);length+=1
                if succ[v]<0:break
                v=succ[v]
        return True
    def visit(j):
        if j==N:
            counts['visited_complete_rotations']+=1
            yield tuple(rotation);return
        for r in orders[j]:
            counts['visited_rotation_prefixes']+=1;rotation[j]=r
            assigned=[]
            for k,i in enumerate(r):
                a=di[(i,j)];succ[a]=di[(j,r[(k-1)%len(r)])];assigned.append(a)
            if short_face_paths():yield from visit(j+1)
            else:
                counts['pruned_prefixes']+=1;counts['pruned_full_rotations']+=after[j+1]
            for a in assigned:succ[a]=-1
        rotation[j]=None
    yield from visit(0)

def run():
    graphs=generate();reps=representatives(graphs);counts=Counter();entries=[];survivors=[]
    for rep in reps:
        mask=rep['mask'];adj=adjacent(mask)
        # Connectedness is checked directly, not an unproved planar assumption.
        seen={0};todo=[0]
        while todo:
            v=todo.pop()
            for w in adj[v]:
                if w not in seen:seen.add(w);todo.append(w)
        need(len(seen)==N,'connected degree graph')
        for rot in rotations_pruned(adj,counts):
            fs=faces(rot);need(fs is not None,'completed short face paths give a T6Q3 sphere map')
            ed=sorted({tuple(sorted((i,j))) for i,r in enumerate(rot) for j in r});ei={e:k for k,e in enumerate(ed)}
            black=[tuple(ei[tuple(sorted((i,j)))] for j in r) for i,r in enumerate(rot)]
            white=[tuple(ei[tuple(sorted(d))] for d in ds) for f,ds in fs]
            complex=black+white;tc=Counter(v for f in complex if len(f)==3 for v in f)
            bad=[v for v in range(15) if tc[v]>2]
            row={'graph_mask':mask,'rotation':rot,'bad_three_T_vertices':bad}
            entries.append(row)
            if not bad:
                m=medial(rot,fs);need(m is not None,'accepted medial contact-face audit')
                survivors.append({'graph_mask':mask,'rotation':rot,'Ts':m['Ts'],'Qs':m['Qs'],'tcount':m['tcount']})
    need(counts['pruned_full_rotations']+counts['visited_complete_rotations']==186624*len(reps),'complete disjoint rotation-product coverage')
    need(len(graphs)==15740 and len(reps)==28 and len(entries)==10 and len(survivors)==2,'complete cover counts')
    return {'labelled_degree_graphs':len(graphs),'unlabelled_degree_graphs':len(reps),
            'graph_representatives':reps,'full_rotation_product_domain':186624*len(reps),
            'rotation_coverage_counts':dict(counts),'spherical_rotation_entries':entries,'survivors':survivors}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
