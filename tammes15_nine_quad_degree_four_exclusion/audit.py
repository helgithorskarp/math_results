"""Independent embedding representation: directed cycle exact covers.
six-tammes-1, researcher. Separate audit; no library planarity predicate.
"""
from itertools import combinations,permutations
from collections import Counter
import json

import atlas as a

def cycle_candidates(adj):
    n=len(adj);ed=sorted({(min(i,j),max(i,j)) for i,r in enumerate(adj) for j in r})
    darts=tuple(d for e in ed for d in (e,e[::-1]));di={d:i for i,d in enumerate(darts)};cycles=[]
    for k in (3,4):
        for vertices in combinations(range(n),k):
            start=vertices[0]
            for rest in permutations(vertices[1:]):
                f=(start,)+rest
                if not all(f[(i+1)%k] in adj[f[i]] for i in range(k)):continue
                ds=tuple((f[i],f[(i+1)%k]) for i in range(k));mask=sum(1<<di[d] for d in ds)
                # Face transitions at j give its predecessor mapping i -> k.
                pred=tuple((f[(i+1)%k],f[i],f[(i+2)%k]) for i in range(k))
                cycles.append((f,mask,pred))
    return darts,cycles

def face_covers(adj,tquota=6,qquota=3):
    darts,cs=cycle_candidates(adj);n=len(adj);full=(1<<len(darts))-1;containing=[[] for _ in darts]
    for i,c in enumerate(cs):
        for d in range(len(darts)):
            if c[1]>>d&1:containing[d].append(i)
    # Distinct representation from the rotation-product/face-path generator.
    pred=[{} for _ in adj];answer=[];visits=0
    def add(c):
        made=[]
        for v,x,y in c[2]:
            if x in pred[v] or y in pred[v].values():
                for u,z in made:del pred[u][z]
                return None
            pred[v][x]=y;made.append((v,x))
            # A proper closed local cycle cannot extend to one degree cycle.
            start=x;seen=set();q=x
            while q in pred[v] and q not in seen:seen.add(q);q=pred[v][q]
            if q==start and len(seen)!=len(adj[v]):
                for u,z in made:del pred[u][z]
                return None
        return made
    def visit(mask,nt,nq,chosen):
        nonlocal visits;visits+=1
        if mask==full:
            if (nt,nq)!=(tquota,qquota):return
            rot=[]
            for v,r in enumerate(adj):
                if set(pred[v])!=set(r):raise ValueError('all local predecessors assigned')
                inv={y:x for x,y in pred[v].items()};seq=[min(r)]
                for i in range(len(r)-1):seq.append(inv[seq[-1]])
                if len(set(seq))!=len(r) or inv[seq[-1]]!=seq[0]:raise ValueError('one local rotation cycle')
                rot.append(tuple(seq))
            answer.append(tuple(rot));return
        if nt>tquota or nq>qquota:return
        if (tquota-nt)*3+(qquota-nq)*4!=len(darts)-mask.bit_count():return
        candidates=None
        for d in range(len(darts)):
            if mask>>d&1:continue
            poss=[i for i in containing[d] if not cs[i][1]&mask and (nt<tquota if len(cs[i][0])==3 else nq<qquota)]
            if not poss:return
            if candidates is None or len(poss)<len(candidates):candidates=poss
        for i in candidates:
            c=cs[i];made=add(c)
            if made is None:continue
            visit(mask|c[1],nt+(len(c[0])==3),nq+(len(c[0])==4),chosen+[i])
            for v,z in made:del pred[v][z]
    visit(0,0,0,[])
    if len(answer)!=len(set(answer)):raise ValueError('unique face-cover representations')
    return sorted(answer),{'cycle_candidates':len(cs),'exact_cover_nodes':visits}

def degree_graphs_by_edge_prefix():
    """Different state/order from row-neighbor generation; compare full masks."""
    pairs=tuple(reversed(a.PAIRS));target=a.DEG;deg=[0]*a.N;answer=set();suffix=[[0]*a.N for _ in range(len(pairs)+1)]
    for k in range(len(pairs)-1,-1,-1):
        suffix[k]=suffix[k+1][:]
        for v in pairs[k]:suffix[k][v]+=1
    def visit(k,mask):
        if any(deg[v]>target[v] or deg[v]+suffix[k][v]<target[v] for v in range(a.N)):return
        if k==len(pairs):answer.add(mask);return
        i,j=pairs[k];visit(k+1,mask);deg[i]+=1;deg[j]+=1
        visit(k+1,mask|(1<<a.INDEX[(i,j)]));deg[i]-=1;deg[j]-=1
    visit(0,0);return answer

def audit():
    direct=a.run();graphs=degree_graphs_by_edge_prefix()
    if graphs!=a.generate():raise ValueError('entry-level degree graph generation mismatch')
    known={}
    for x in direct['spherical_rotation_entries']:known.setdefault(x['graph_mask'],set()).add(tuple(map(tuple,x['rotation'])))
    records=[]
    for g in direct['graph_representatives']:
        rots,counts=face_covers(a.adjacent(g['mask']));expected=known.get(g['mask'],set())
        if set(rots)!=expected:raise ValueError('entry-level embedding mismatch for graph '+str(g['mask']))
        records.append({'graph_mask':g['mask'],'rotations':rots,'counts':counts,'matches_all_rotation_entries':True})
    k4=tuple(tuple(j for j in range(4) if i!=j) for i in range(4));rots,cnt=face_covers(k4,4,0)
    if len(rots)!=2:raise ValueError('two K4 embeddings')
    return {'agent':'six-tammes-1','role':'researcher',
            'status':'COMPLETE_SEPARATE_ENUMERATION_AUDIT_NOT_INDEPENDENT_MATHEMATICAL_REVIEW',
            'degree_graph_masks_compared':len(graphs),'graphs':records,
            'total_rotations':sum(len(r['rotations']) for r in records),
            'entry_level_all_graphs_match':True,'K4_rotations':rots}
if __name__=='__main__':print(json.dumps(audit(),indent=2,sort_keys=True))
