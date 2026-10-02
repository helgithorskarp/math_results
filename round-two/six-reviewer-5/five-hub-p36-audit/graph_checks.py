"""Fresh whole four-vertex colored-graph/role calibration of ordinary cuts.

These are abstract graphs satisfying the named graph hypotheses, not packings.
The all-order statements still require the ordinary proof in REVIEW.md.
"""
import itertools as it,time
import audit as a

def inspect(roles,edges):
    n=len(roles);adj=[set() for _ in roles];c1=[0]*n;c2=[0]*n
    U={i for i,r in enumerate(roles) if r in ('A','V')};A={i for i,r in enumerate(roles) if r=='A'}
    C={i for i,r in enumerate(roles) if r=='C'};B={i for i,r in enumerate(roles) if r=='B'}
    for x,y,color in edges:
        a.need(0<=x<y<n and color in (1,2),'literal colored edge')
        if (x in U or y in U) and color!=1:return None
        if (x in U and roles[y] in ('B','V')) or (y in U and roles[x] in ('B','V')):return None
        adj[x].add(y);adj[y].add(x)
        counts=c1 if color==1 else c2;counts[x]+=1;counts[y]+=1
    roots={i for i in range(n) if {i}|adj[i]|set().union(*(adj[j] for j in adj[i]))==set(range(n))}
    R=len(roots&U)
    r={'D':sum(len(adj[i]) for i in U),'I':sum(min(len(adj[i]),len(A)-1) for i in A),
       'C1':sum(c1[i] for i in C),'C2':sum(c2[i] for i in C),'B2':sum(c2[i] for i in B),
       'R':R,'B':len(B),'closed_root':len(roots&(U|C))}
    a.need(r['D']<=r['I']+r['C1'],'actual graph unit endpoint inequality')
    if R and B:
        capacity=r['C1']+r['C2']
        a.need(capacity>=R+len(B),'actual distinct-edge radius cut')
        a.need(capacity>=max(R,r['D']-r['I'])+len(B),'joint endpoint radius cut')
        paths=sum(max(k*min(len(B),len(adj[i])-k) for k in range(min(R,c1[i])+1)) for i in C)
        a.need(R*len(B)<=paths,'all-root/all-B common-neighbor capacity')
    closure=r['D']==r['I']+r['C1'] and bool(B) and (r['C2']==0 or r['B2']==0)
    if closure:a.need(not r['closed_root'],'guarded whole-color closed partition')
    return r

def run():
    start=time.monotonic();edges=list(it.combinations(range(4),2));tested=admissible=radius_cases=0
    for roles in it.product(('A','V','C','B'),repeat=4):
        for colors in it.product(range(3),repeat=6):
            tested+=1
            if tested%2048==0:a.need(time.monotonic()-start<10,'INCOMPLETE fixed10s graph calibration guard')
            record=inspect(roles,[(x,y,c) for (x,y),c in zip(edges,colors) if c])
            if record is not None:
                admissible+=1;radius_cases+=bool(record['R'] and record['B'])
    path=inspect(('A','C','B'),[(0,1,1),(1,2,2)])
    a.need(path is not None and path['D']==path['I']+path['C1'] and path['C2']==path['B2']==1,'positive heavy crossing retained')
    a.need(path['C1']+path['C2']==max(path['R'],path['D']-path['I'])+path['B'],'joint endpoint bound sharp on abstract heavy path')
    # Dropping heavy support or adding the two overlapping endpoint demands
    # would wrongly reject this actual positive graph control.
    a.need(path['C1']<path['R']+path['B'],'heavy support essential positive witness')
    a.need(path['C1']+path['C2']<path['R']+path['D']-path['I']+path['B'],'max rather than double-counted sum is essential')
    return {'complete_four_vertex_role_color_cases':tested,'admissible_structural_graphs':admissible,
            'nonvacuous_unit_root_B_cases':radius_cases,'positive_heavy_crossing_path':path,
            'boundary':'Abstract structural calibration and sharp positive three-vertex control; no actual packing realization or substitute for ordinary all-order proof.'}

if __name__=='__main__':
    record=run();(a.P/'graph-record.json').write_bytes(a.encode(record));print(a.encode(record).decode())
