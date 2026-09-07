"""Independent, solver-free proof of the complete orbit-repair dichotomy."""
import argparse
import hashlib
import json
from collections import Counter
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
N=372
EDGE_SHA256='dc979b14d9e8e08f497513adee55767e81f36076c40e2082693fe6d209b94d6d'


def require(test,message):
    if not test:
        raise ValueError(message)


def read_graph(path):
    data=path.read_bytes()
    require(hashlib.sha256(data).hexdigest()==EDGE_SHA256,'source edge hash')
    edges=[tuple(map(int,line.split())) for line in data.decode().splitlines()]
    require(len(edges)==1710 and edges==sorted(set(edges)),'edge count/order')
    require(all(len(e)==2 and 0<=e[0]<e[1]<N for e in edges),'edge labels')
    return edges


def group_elements(generators,edges,n=N):
    require(isinstance(generators,list) and len(generators)>0,'generator list')
    for g in generators:
        require(isinstance(g,list) and len(g)==n and all(type(v) is int for v in g)
                and sorted(g)==list(range(n)),'generator permutation')
    edge_set=set(edges)
    for g in generators:
        require({tuple(sorted((g[a],g[b]))) for a,b in edges}==edge_set,'graph automorphism')
    identity=tuple(range(n));found={identity};frontier=[identity]
    while frontier:
        permutation=frontier.pop()
        for generator in generators:
            # Compose on the right; producer traverses edge images directly.
            q=tuple(permutation[generator[i]] for i in range(n))
            if q not in found:
                found.add(q);frontier.append(q)
    return sorted(found)


def orbits_from_group(edges,group):
    index={e:i for i,e in enumerate(edges)}
    remaining=set(range(len(edges)));orbits=[]
    while remaining:
        a,b=edges[min(remaining)]
        orbit={index[tuple(sorted((g[a],g[b])))] for g in group}
        require(orbit<=remaining,'overlapping edge orbits')
        orbits.append(sorted(orbit));remaining-=orbit
    return orbits


def neighbourhood_cycles(edges,n=N):
    """Independent component decomposition; all source local degrees are <=2."""
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b);adj[b].add(a)
    cycles=[]
    for centre in range(n):
        local={v:adj[v]&adj[centre] for v in adj[centre]}
        require(all(len(neighbours)<=2 for neighbours in local.values()),'unexpected local branching')
        unvisited=set(local)
        while unvisited:
            start=min(unvisited);component={start};queue=[start]
            for v in queue:
                for u in local[v]:
                    if u not in component:
                        component.add(u);queue.append(u)
            unvisited-=component
            if not all(len(local[v])==2 for v in component):
                continue
            start=min(component);previous=start;v=min(local[start]);rim=[start]
            while v!=start:
                require(v not in rim,'cycle traversal')
                rim.append(v)
                previous,v=v,next(iter(local[v]-{previous}))
            require(set(rim)==component,'cycle coverage')
            cycles.append((centre,tuple(rim)))
    return cycles


def wheel_mask(centre,rim,edges,edge_orbit):
    require(type(centre) is int and 0<=centre<N,'wheel centre')
    require(isinstance(rim,(tuple,list)) and len(rim)>=3 and len(rim)%2==1,'odd rim')
    require(all(type(v) is int and 0<=v<N for v in rim)
            and len(set(rim))==len(rim) and centre not in rim,'wheel vertices')
    index={e:i for i,e in enumerate(edges)}
    required=[tuple(sorted((centre,v))) for v in rim]
    required += [tuple(sorted((rim[i],rim[(i+1)%len(rim)]))) for i in range(len(rim))]
    require(all(e in index for e in required),'missing wheel edge')
    return sum(1<<o for o in {edge_orbit[index[e]] for e in required})


def maximal_cube(nbits,forbidden):
    singles=[m for m in forbidden if m.bit_count()==1]
    pairs=[m for m in forbidden if m.bit_count()==2]
    require(len(singles)==1 and len(pairs)==6 and len(forbidden)==7,'seven-factor structure')
    used=0
    for m in forbidden:
        require(m>0 and m<(1<<nbits) and not(used&m),'overlapping forbidden factors')
        used|=m
    free=((1<<nbits)-1)^used
    choices=[[1<<k for k in range(nbits) if m>>k&1] for m in pairs]
    maximal=sorted(free|sum(bits) for bits in product(*choices))
    return maximal,free,singles[0],pairs


def check_colouring(n,edges,word):
    require(isinstance(word,str) and len(word)==n and set(word)<=set('0123'),'colour word')
    require(all(word[a]!=word[b] for a,b in edges),'colour conflict')


def verify(certificate_path=None):
    edges=read_graph(HERE/'source.edges')
    generators=json.loads((HERE/'generators.json').read_text())
    group=group_elements(generators,edges)
    require(len(group)==60,'group order')
    orbits=orbits_from_group(edges,group)
    require(len(orbits)==29 and Counter(map(len,orbits))==Counter({60:28,30:1}),'edge orbit sizes')
    edge_orbit={e:k for k,orbit in enumerate(orbits) for e in orbit}
    cycles=neighbourhood_cycles(edges)
    require(len(cycles)==444 and all(len(rim)==5 for _,rim in cycles),'source wheel census')
    all_masks={wheel_mask(c,rim,edges,edge_orbit) for c,rim in cycles}
    minimal=sorted(m for m in all_masks if not any(q!=m and q&m==q for q in all_masks))
    path=certificate_path or HERE/'certificate.json'
    data=json.loads(path.read_text())
    require(isinstance(data,dict) and set(data)=={'wheels','colourings'},'certificate schema')
    witnesses=data['wheels'];require(isinstance(witnesses,list) and len(witnesses)==7,'wheel witnesses')
    verified=[]
    for w in witnesses:
        require(isinstance(w,dict) and set(w)=={'centre','rim','mask'},'wheel schema')
        m=wheel_mask(w['centre'],w['rim'],edges,edge_orbit)
        require(type(w['mask']) is int and m==w['mask'],'wheel orbit mask')
        verified.append(m)
    require(sorted(verified)==minimal,'minimal wheel mask coverage')
    maximal,free,single,pairs=maximal_cube(len(orbits),minimal)
    recipes=data['colourings']
    require(isinstance(recipes,list) and len(recipes)==64,'colouring count')
    masks=[];edge_counts=[];checks=0
    for item in recipes:
        require(isinstance(item,dict) and set(item)=={'mask','word'},'colour recipe schema')
        mask=item['mask'];require(type(mask) is int and 0<=mask<(1<<len(orbits)),'selector mask')
        selected=[edges[e] for k,orbit in enumerate(orbits) if mask>>k&1 for e in orbit]
        check_colouring(N,selected,item['word'])
        require(not any(mask&f==f for f in minimal),'unbroken wheel in claimed maximal support')
        masks.append(mask);edge_counts.append(len(selected));checks+=len(selected)
    require(sorted(masks)==maximal,'maximal cube coverage')
    require(set(edge_counts)=={1320},'maximal edge count')
    require(free.bit_count()==16,'free selector count')
    singleton_orbit=(single&-single).bit_length()-1
    require(len(orbits[singleton_orbit])==30,'forced removed orbit size')
    for m in pairs:
        require(all(len(orbits[k])==60 for k in range(29) if m>>k&1),'paired orbit size')
    degrees=Counter(v for e in edges for v in e)
    return dict(vertices=N,source_edges=len(edges),source_degree_census=dict(sorted(Counter(degrees.values()).items())),
                group_order=len(group),edge_orbits=len(orbits),edge_orbit_sizes=dict(sorted(Counter(map(len,orbits)).items())),
                source_odd_wheels=len(cycles),distinct_wheel_orbit_masks=len(all_masks),minimal_forbidden_masks=minimal,
                constrained_orbits=13,free_orbits=16,total_orbit_selections=1<<29,
                wheel_free_orbit_selections=(1<<16)*3**6,maximal_supports=len(maximal),maximal_edges=1320,
                necessary_removed_edges_for_plane_map=390,colour_inequalities_checked=checks,
                every_maximal_support_four_colourable=True,no_non_four_colourable_orbit_repair_has_a_plane_unit_map=True,
                full_image_unit_graph_not_classified=True,
                certificate_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_edge_sha256=EDGE_SHA256)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--check-expected',action='store_true');args=p.parse_args()
    result=verify(args.certificate)
    rendered=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.check_expected:
        require(json.loads(rendered)==json.loads((HERE/'expected.json').read_text()),'expected result mismatch')
    if args.output:
        args.output.write_text(rendered)
    print(rendered,end='')
