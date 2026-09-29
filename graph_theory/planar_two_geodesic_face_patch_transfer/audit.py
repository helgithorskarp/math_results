"""Separate controls using an explicit core and breadth-first insertions.

No target Python module is imported. The shared inputs are the earlier
1,112-byte metric certificate and the expected generator stream hashes.
Floyd--Warshall and direct separator-bag inspection check the small
models independently of the production Dijkstra/centroid routines.
"""
from collections import deque,Counter
from itertools import combinations
from pathlib import Path
from random import Random
import hashlib
import json

HERE=Path(__file__).resolve().parent
CERT=HERE.parent/'planar_two_geodesic_icosahedron_price_region/certificate.json'


def rotate(F):return min(F,F[1:]+F[:1],F[2:]+F[:2])


def core():
    rows=[(1,2,3,4,5),(0,2,5,6,10),(0,1,3,6,7),(0,2,4,7,8),
          (0,3,5,8,9),(0,1,4,9,10),(1,2,7,10,11),(2,3,6,8,11),
          (3,4,7,9,11),(4,5,8,10,11),(1,5,6,9,11),(6,7,8,9,10)]
    adj=[set(row) for row in rows]
    faces=[F for F in combinations(range(12),3) if all(v in adj[u] for u,v in combinations(F,2))]
    incidences={}
    for i,F in enumerate(faces):
        for e in combinations(F,2):incidences.setdefault(e,[]).append(i)
    assert len(faces)==20 and all(len(fs)==2 for fs in incidences.values())
    oriented={0:(0,1,2)};queue=deque([0])
    while queue:
        f=queue.popleft();F=oriented[f]
        for u,v in zip(F,F[1:]+F[:1]):
            g=next(i for i in incidences[tuple(sorted((u,v)))] if i!=f)
            w=next(x for x in faces[g] if x not in (u,v));G=rotate((v,u,w))
            if g in oriented:assert oriented[g]==G
            else:oriented[g]=G;queue.append(g)
    assert len(oriented)==20
    return faces,[oriented[i] for i in range(20)]


def floyd(n,cost):
    infinity=sum(cost.values())+1
    d=[[0 if u==v else infinity for v in range(n)] for u in range(n)]
    nxt=[[None]*n for _ in range(n)]
    for (u,v),w in cost.items():d[u][v]=d[v][u]=w;nxt[u][v]=v;nxt[v][u]=u
    for k in range(n):
        for u in range(n):
            for v in range(n):
                new=d[u][k]+d[k][v]
                if new<d[u][v]:d[u][v]=new;nxt[u][v]=nxt[u][k]
    return d,nxt


def make(depths,prices,pricing):
    faces,oriented=core();core_d,_=floyd(12,prices);long=1+max(map(max,core_d))
    cost=dict(prices);patches=[];bags=[];parents=[];triangles=[];offset=12
    for f,depth in enumerate(depths):
        size=(3**depth-1)//2;K=set(range(offset,offset+size));patches.append(K)
        local_bags=[];local_parents=[];queue=deque([(oriented[f],0,-1)])
        while queue:
            F,level,parent=queue.popleft()
            if level==depth:triangles.append(F);continue
            index=len(local_bags);v=offset+index;local_bags.append(set(F)|{v});local_parents.append(parent)
            for u in F:cost[min(u,v),max(u,v)]=long if pricing=='all_long' or u<12 else 1+(u+v)%11
            a,b,c=F
            queue.extend((T,level+1,index) for T in ((a,b,v),(b,c,v),(c,a,v)))
        assert len(local_bags)==size
        if not size:local_bags=[set(faces[f])];local_parents=[-1]
        bags.append(local_bags);parents.append(local_parents);offset+=size
    adj=[set() for _ in range(offset)]
    for u,v in cost:adj[u].add(v);adj[v].add(u)
    return {'adj':adj,'cost':cost,'patches':patches,'bags':bags,'parents':parents,
            'triangles':triangles,'faces':faces,'core_d':core_d}


def parts(adj,removed):
    remaining=set(range(len(adj)))-set(removed);out=[]
    while remaining:
        start=min(remaining);component={start};queue=deque([start]);remaining.remove(start)
        while queue:
            v=queue.popleft()
            for u in adj[v]:
                if u in remaining:remaining.remove(u);component.add(u);queue.append(u)
        out.append(component)
    return out


def stream_hash(g):
    payload={'edges':sorted((u,v,w) for (u,v),w in g['cost'].items()),
             'oriented_faces':sorted(g['triangles']),'patches':[sorted(K) for K in g['patches']],
             'bags':[[sorted(B) for B in group] for group in g['bags']],'parents':g['parents']}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def path_from(next_vertex,u,v):
    path=[u]
    while path[-1]!=v:
        path.append(next_vertex[path[-1]][v]);assert len(path)==len(set(path))
    return path


def run():
    cert=json.loads(CERT.read_text());center={(u,v):c for u,v,c in cert['core_edges']}
    pairs=cert['candidate_pairs'];paths=[P for pair in pairs for P in pair]
    records=json.loads((HERE/'expected.json').read_text())['verify']['fixtures']
    counts=Counter();rng=Random(2026092921);heavy_outside=0;guard_cases=0
    for record in records:
        if record['metric']=='center':prices={e:151*c for e,c in center.items()}
        else:
            P=paths[int(record['metric'].split(':')[1])];selected={tuple(sorted(e)) for e in zip(P,P[1:])}
            prices={e:(158 if e in selected else 144)*c for e,c in center.items()}
        g=make(record['depths'],prices,record['pricing']);assert stream_hash(g)==record['sha256']
        counts['exact_generator_hash_matches']+=1
        n=len(g['adj']);assert len(g['cost'])==3*n-6 and len(g['triangles'])==2*n-4
        # Full ambient Floyd controls are deliberately bounded. Larger
        # input streams are still compared in full, not by aggregate counts.
        if n>150:continue
        distances,nxt=floyd(n,g['cost']);counts['ambient_models']+=1
        assert all(distances[u][v]==g['core_d'][u][v] for u in range(12) for v in range(12))
        for P in paths:
            assert sum(g['cost'][tuple(sorted(e))] for e in zip(P,P[1:]))==distances[P[0]][P[-1]]
            counts['core_path_checks']+=1
        partitions=[parts(g['adj'],set(P)|set(Q)) for P,Q in pairs]
        profiles=[[0]*n,[1]*n,[int(v<12) for v in range(n)]]
        for K in g['patches']:
            if K:
                profiles.append([int(v in K) for v in range(n)])
                equal=[int(v in K) for v in range(n)];equal[0]+=len(K);profiles.append(equal)
        profiles.extend([rng.randrange(13) for _ in range(n)] for _ in range(16))
        for mass in profiles:
            total=sum(mass);sizes=[sum(mass[v] for v in K) for K in g['patches']];B=max(sizes,default=0)
            largest=[max((sum(mass[v] for v in K) for K in partition),default=0) for partition in partitions]
            assert 2*min(largest)<=max(total,2*B);counts['quantitative_cases']+=1
            heavy=next((f for f,s in enumerate(sizes) if 2*s>total),None)
            if heavy is None:assert 2*min(largest)<=total;counts['light_or_zero_cases']+=1;continue
            # Independent of any centroid algorithm: inspect every local
            # size-four bag directly as a whole-graph vertex separator.
            candidates=[sorted(Bag) for Bag in g['bags'][heavy]
                        if all(2*sum(mass[v] for v in K)<=total for K in parts(g['adj'],Bag))]
            assert candidates;bag=min(candidates)
            covering=[path_from(nxt,bag[i],bag[min(i+1,len(bag)-1)]) for i in range(0,len(bag),2)]
            removed=set().union(*map(set,covering))
            assert set(bag)<=removed and all(2*sum(mass[v] for v in K)<=total for K in parts(g['adj'],removed))
            for P in covering:
                assert sum(g['cost'][tuple(sorted(e))] for e in zip(P,P[1:]))==distances[P[0]][P[-1]]
            torso=g['patches'][heavy]|set(g['faces'][heavy])
            heavy_outside+=any(v not in torso for P in covering for v in P)
            counts['heavy_bag_cases']+=1;assert all(2*x>total for x in largest)
        # A bounded direct guard control on the original 32-vertex case.
        if n==32:
            for k in range(5):
                for removed in combinations(range(12),k):
                    sub=[{u for u in row if u<12} for row in g['adj'][:12]]
                    assert len(parts(sub,removed))==1
                    unaffected=sum(not(set(F)<=set(removed)) for F in g['faces'])-(4-k)
                    assert unaffected>=16;guard_cases+=1
    assert heavy_outside and counts['heavy_bag_cases'] and counts['light_or_zero_cases']
    return {'status':'PASS','counts':dict(sorted(counts.items())),'heavy_repairs_leaving_torso':heavy_outside,
            'guard_core_deletions':guard_cases,'seed':2026092921,
            'scope':'independent construction, complete stream hash matches, Floyd distances and direct separator-bag checks'}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
