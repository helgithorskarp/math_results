"""Separate Floyd--Warshall, embedding, attachment, and mass audit.

Imports neither verify.py nor private discovery code. Integer arithmetic
only; no external solver, graph package, or dataset is required.
"""
from itertools import combinations
from pathlib import Path
from random import Random
import json

HERE=Path(__file__).resolve().parent


def fixture():
    oriented=[]
    for i in range(5):
        u,v=1+i,1+(i+1)%5;a,b=6+i,6+(i+1)%5
        oriented.extend([(0,u,v),(v,u,a),(v,a,b),(11,b,a)])
    oriented.sort(key=lambda F:tuple(sorted(F)))
    edges={tuple(sorted((u,v))) for F in oriented for u,v in zip(F,F[1:]+F[:1])}
    triangles=[]
    for i,F in enumerate(oriented):
        z=12+i
        for u,v in zip(F,F[1:]+F[:1]):
            triangles.append((u,v,z));edges.add(tuple(sorted((u,z))))
    darts=[(u,v) for F in triangles for u,v in zip(F,F[1:]+F[:1])]
    assert len(darts)==len(set(darts)) and all((v,u) in darts for u,v in darts)
    adj=[set() for _ in range(32)]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    for v in range(32):
        link={}
        for F in triangles:
            if v in F:
                j=F.index(v);link[F[(j+1)%3]]=F[(j+2)%3]
        visited=set();start=min(link);x=start
        while x not in visited:visited.add(x);x=link[x]
        assert x==start and visited==set(link)==set(link.values())
    assert len(edges)==90 and len(triangles)==60 and 32-90+60==2
    return adj,[tuple(sorted(F)) for F in oriented],edges


def floyd(n,cost):
    infinity=sum(cost.values())+1
    d=[[0 if u==v else infinity for v in range(n)] for u in range(n)]
    for (u,v),w in cost.items():d[u][v]=d[v][u]=w
    for k in range(n):
        for u in range(n):
            for v in range(n):d[u][v]=min(d[u][v],d[u][k]+d[k][v])
    return d


def components(adj,removed):
    remaining=set(range(len(adj)))-removed;answer=[]
    while remaining:
        todo=[min(remaining)];part=set()
        while todo:
            v=todo.pop()
            if v in part:continue
            part.add(v);todo.extend(adj[v]&remaining-part)
        remaining-=part;answer.append(part)
    return answer


def main():
    data=json.loads((HERE/'certificate.json').read_text());adj,faces,edges=fixture()
    assert faces==[tuple(F) for F in data['faces']]
    center={(u,v):c for u,v,c in data['core_edges']}
    assert set(center)=={e for e in edges if e[1]<12}
    pairs=data['candidate_pairs'];paths=[p for pair in pairs for p in pair]
    metrics=[{e:151*c for e,c in center.items()}]
    for path in paths:
        selected={tuple(sorted((u,v))) for u,v in zip(path,path[1:])}
        metrics.append({e:(158 if e in selected else 144)*c for e,c in center.items()})
    rng=Random(2026092919)
    for _ in range(6):metrics.append({e:rng.randint(144*c,158*c) for e,c in center.items()})
    partitions=[components(adj,set(p)|set(q)) for p,q in pairs]
    H1=max(partitions[0],key=len);H2=max(partitions[1],key=len)
    assert all(len(K)==1 or not(K&H1) or not(K&H2) for K in partitions[2])
    masses=[[0]*32,[1]*32]
    masses.extend([int(v==u) for v in range(32)] for u in range(32))
    masses.extend([int(v in S) for v in range(32)] for S in (H1,H2,H1&H2))
    masses.extend([rng.randrange(20) for _ in range(32)] for _ in range(128))
    counts={'zero':0,'heavy_vertex':0,'pair_1':0,'pair_2':0,'pair_3':0}
    full_models=0;path_checks=0;star_checks=0;mass_checks=0
    for metric in metrics:
        # Double lengths so the three-point metric star has integer legs.
        price={e:2*w for e,w in metric.items()};d=floyd(12,price)
        for mode in range(5):
            cost=dict(price)
            for i,F in enumerate(faces):
                z=12+i
                if mode<4:
                    parent=F[mode if mode<3 else i%3];leg=1+i%7
                    for v in F:cost[v,z]=leg+d[parent][v]
                else:
                    for v in F:
                        u,w=[x for x in F if x!=v]
                        cost[v,z]=max(1,(d[v][u]+d[v][w]-d[u][w])//2)
                for u,v in combinations(F,2):
                    assert cost[u,z]+cost[v,z]>=d[u][v];star_checks+=1
            assert set(cost)==edges and all(w>0 for w in cost.values())
            full=floyd(32,cost)
            assert all(full[u][v]==d[u][v] for u in range(12) for v in range(12))
            for path in paths:
                length=sum(cost[tuple(sorted((u,v)))] for u,v in zip(path,path[1:]))
                assert length==full[path[0]][path[-1]];path_checks+=1
            for mass in masses:
                total=sum(mass);mass_checks+=1
                if total==0:counts['zero']+=1;continue
                heavy=next((v for v,w in enumerate(mass) if 2*w>=total),None)
                if heavy is not None:
                    assert all(2*sum(mass[v] for v in K)<=total for K in components(adj,{heavy}))
                    counts['heavy_vertex']+=1;continue
                valid=[i for i,parts in enumerate(partitions) if all(2*sum(mass[v] for v in K)<=total for K in parts)]
                assert valid;counts[f'pair_{min(valid)+1}']+=1
            full_models+=1
    assert all(counts.values())
    # A face shortcut violating the stated hypothesis really changes
    # core distances. Such metrics are deliberately outside this theorem.
    bad=dict(cost);bad[0,12]=bad[1,12]=1
    assert 2<d[0][1] and floyd(32,bad)[0][1]<d[0][1]
    print(json.dumps({'status':'PASS','metric_models':len(metrics),'attachment_models':full_models,
                      'star_inequalities':star_checks,'ambient_path_checks':path_checks,
                      'mass_checks':mass_checks,'separator_branches':counts,
                      'rejected_shortcut_control':1,'seed':2026092919},sort_keys=True))


if __name__=='__main__':main()
