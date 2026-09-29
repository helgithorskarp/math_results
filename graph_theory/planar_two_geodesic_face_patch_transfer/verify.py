"""Exact geometry, quotient-containment, torso and separator controls."""
from collections import Counter
from itertools import combinations
from pathlib import Path
from random import Random
import argparse
import json
import model as m

HERE=Path(__file__).resolve().parent


def tree_connected(nodes,parents):
    if not nodes:return True
    neighbors={i:set() for i in nodes}
    for i in nodes:
        if parents[i] in nodes:neighbors[i].add(parents[i]);neighbors[parents[i]].add(i)
    seen={min(nodes)};todo=list(seen)
    while todo:
        v=todo.pop();new=neighbors[v]-seen;seen|=new;todo.extend(new)
    return seen==set(nodes)


def check_graph(graph):
    adj=graph['adj'];n=len(adj);E={(u,v) for u in adj for v in adj[u] if u<v};faces=graph['triangles']
    assert len(E)==3*n-6 and len(faces)==2*n-4
    assert all(adj[v][u]==w for u in adj for v,w in adj[u].items())
    darts=[(u,v) for F in faces for u,v in zip(F,F[1:]+F[:1])]
    assert len(darts)==len(set(darts)) and all((v,u) in darts for u,v in darts)
    links={v:{} for v in adj}
    for F in faces:
        for i,v in enumerate(F):
            a,b=F[(i+1)%3],F[(i+2)%3];assert a not in links[v];links[v][a]=b
    for v,link in links.items():
        first=min(link);seen=set();x=first
        while x not in seen:seen.add(x);x=link[x]
        assert x==first and seen==set(link)==set(link.values())==set(adj[v])
    assert len(m.components(adj,[]))==1
    bag_count=0
    for f,K in enumerate(graph['patches']):
        boundary=set(graph['core_faces'][f]);T=K|boundary
        bags=graph['bags'][f];parents=graph['parents'][f]
        assert boundary<=bags[0] and parents[0]==-1
        assert all(0<=parents[i]<i for i in range(1,len(bags)))
        assert all(len(B)<=4 and B<=T for B in bags) and set.union(*bags)==T
        assert all(any({u,v}<=B for B in bags) for u,v in E if u in T and v in T)
        assert all(tree_connected({i for i,B in enumerate(bags) if v in B},parents) for v in T)
        bag_count+=len(bags)
        if K:assert len(m.components({v:{u:w for u,w in adj[v].items() if u in K} for v in K},[]))==1
    for v in range(12):
        d,_=m.distances(adj,v)
        assert all(d[u]==graph['core_d'][v][u] for u in range(12))
    return bag_count


def quotient():
    adj={v:set() for v in range(32)}
    for a,b,_ in m.certificate()['core_edges']:adj[a].add(b);adj[b].add(a)
    for f,F in enumerate(m.core_faces()):
        for u in F:adj[u].add(12+f);adj[12+f].add(u)
    return adj


def check_transfer_certificate():
    data=m.certificate();Q=quotient();pairs=data['candidate_pairs']
    assert [sorted(F) for F in m.core_faces()]==data['faces']
    prices={(u,v):c for u,v,c in data['core_edges']}
    paths=[P for pair in pairs for P in pair];potentials=data['critical_corner_potentials']
    assert len(paths)==len(potentials)==6
    inequalities=0
    for P,pi in zip(paths,potentials):
        assert len(P)==len(set(P)) and set(P)<=set(range(12)) and len(pi)==12
        selected={tuple(sorted(e)) for e in zip(P,P[1:])}
        assert selected<=set(prices) and pi[P[0]]==0
        assert pi[P[-1]]==sum(158*prices[e] for e in selected)
        for (u,v),c in prices.items():
            assert abs(pi[u]-pi[v])<=(158 if (u,v) in selected else 144)*c
            inequalities+=1
    partitions=[m.components(Q,set(P)|set(R)) for P,R in pairs]
    atom=lambda C:len(C)==1 and min(C)>=12
    heavy_sets=[]
    for partition in partitions[:2]:
        nonsingle=[C for C in partition if not atom(C)]
        assert len(nonsingle)==1;heavy_sets.append(nonsingle[0])
    assert all(atom(C) or any(C.isdisjoint(H) for H in heavy_sets) for C in partitions[2])
    return {'critical_potential_inequalities':inequalities,'quotient_partitions':3,
            'heavy_set_sizes':list(map(len,heavy_sets)),
            'third_nonatom_component_sizes':[len(C) for C in partitions[2] if not atom(C)]}


def check_pairs(graph):
    adj=graph['adj'];Q=quotient();checked=0
    for pair in m.certificate()['candidate_pairs']:
        removed=set(pair[0])|set(pair[1]);qparts=m.components(Q,removed)
        for K in m.components(adj,removed):
            projected={graph['atom'][v] for v in K}
            assert any(projected<=C for C in qparts);checked+=1
        for path in pair:
            d,_=m.distances(adj,path[0])
            assert sum(adj[u][v] for u,v in zip(path,path[1:]))==d[path[-1]]
    return checked


def mass_profiles(graph,seed):
    vertices=sorted(graph['adj']);n=len(vertices);out=[dict.fromkeys(vertices,0),dict.fromkeys(vertices,1)]
    out.append({v:int(v<12) for v in vertices})
    for f,K in enumerate(graph['patches']):
        if not K:continue
        out.append({v:int(v in K) for v in vertices})
        equal={v:int(v in K) for v in vertices};equal[0]+=len(K);out.append(equal)
    # Quotient masses that exercise the second and third alternatives.
    Q=quotient();pairs=m.certificate()['candidate_pairs']
    H=[max(m.components(Q,set(pair[0])|set(pair[1])),key=len) for pair in pairs[:2]]
    for chosen in (H[0],H[0]&H[1]):
        mass=dict.fromkeys(vertices,0)
        for atom in chosen:
            if atom<12:mass[atom]+=1
            elif graph['patches'][atom-12]:mass[min(graph['patches'][atom-12])]+=1
        out.append(mass)
    rng=Random(seed)
    for _ in range(24):out.append({v:rng.randrange(10) for v in vertices})
    return out


def run():
    transfer_certificate=check_transfer_certificate()
    cases=[('empty',[0]*20),('singletons',[1]*20),('depth2',[2]*20),
           ('depth3',[3]*20),('mixed',[i%4 for i in range(20)]),
           ('heavy',[4 if i==3 else 1 for i in range(20)]),
           ('one_deep',[5 if i==3 else 0 for i in range(20)]),('depth4',[4]*20)]
    counts=Counter();records=[];outside_cover=0;all_core_fail=0
    for case_index,(name,depths) in enumerate(cases):
        for metric_name in ('center','corner:3'):
            pricing='all_long' if case_index%2 else 'boundary_long'
            graph=m.build(depths,m.metric(metric_name),pricing)
            counts['models']+=1;counts['torso_bags']+=check_graph(graph)
            counts['quotient_component_checks']+=check_pairs(graph)
            records.append({'case':name,'depths':depths,'metric':metric_name,'pricing':pricing,
                            'vertices':len(graph['adj']),'sha256':m.fixture_hash(graph)})
            for mass in mass_profiles(graph,2026092920+case_index):
                total=sum(mass.values());B=max((sum(mass[v] for v in K) for K in graph['patches']),default=0)
                largest=[]
                for pair in m.certificate()['candidate_pairs']:
                    largest.append(max((sum(mass[v] for v in K) for K in m.components(graph['adj'],set(pair[0])|set(pair[1]))),default=0))
                assert 2*min(largest)<=max(total,2*B);counts['quantitative_mass_checks']+=1
                paths,detail=m.separator(graph,mass);removed=set().union(*map(set,paths))
                assert len(paths)<=2
                for path in paths:
                    assert path and len(path)==len(set(path));d,_=m.distances(graph['adj'],path[0])
                    assert sum(graph['adj'][u][v] for u,v in zip(path,path[1:]))==d[path[-1]]
                    counts['ambient_path_checks']+=1
                assert all(2*sum(mass[v] for v in K)<=total for K in m.components(graph['adj'],removed))
                counts[detail['branch']]+=1
                if detail['branch']=='heavy_patch':
                    f=detail['patch'];torso=graph['patches'][f]|set(graph['core_faces'][f])
                    outside_cover+=any(v not in torso for path in paths for v in path)
                    all_core_fail+=all(2*w>total for w in largest)
                    assert set(detail['bag'])<=removed
                    assert all(2*sum(mass[v] for v in K)<=total for K in m.components(graph['adj'],detail['bag']))
    assert counts['pair_1'] and counts['pair_2'] and counts['pair_3'] and counts['heavy_patch'] and outside_cover and all_core_fail
    bad=m.build([1]*20,m.metric('center'))
    z=min(bad['patches'][0]);bad['adj'][0][z]=bad['adj'][z][0]=1;bad['adj'][1][z]=bad['adj'][z][1]=1
    assert m.distances(bad['adj'],0)[0][1]<bad['core_d'][0][1]
    return {'status':'PASS','counts':dict(sorted(counts.items())),'maximum_order':max(r['vertices'] for r in records),
            'transfer_certificate':transfer_certificate,
            'heavy_repairs_leaving_torso':outside_cover,'heavy_cases_all_three_core_pairs_fail':all_core_fail,
            'shortening_patch_control':1,'fixtures':records,
            'scope':'finite controls; arbitrary sizes, metrics and real masses use the written transfer proof'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--write-expected',action='store_true');args=parser.parse_args()
    result=run()
    if args.write_expected:(HERE/'expected.json').write_text(json.dumps({'verify':result},indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},sort_keys=True))
