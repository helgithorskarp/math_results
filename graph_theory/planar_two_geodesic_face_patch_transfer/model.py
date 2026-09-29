"""Explicit stacked face patches and exact ambient path helpers."""
from heapq import heappop,heappush
from pathlib import Path
import hashlib
import json

CERT=Path(__file__).resolve().parent.parent/'planar_two_geodesic_icosahedron_price_region/certificate.json'


def certificate():
    blob=CERT.read_bytes()
    assert hashlib.sha256(blob).hexdigest()=='070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d'
    return json.loads(blob)


def core_faces():
    out=[]
    for i in range(5):
        u,v=1+i,1+(i+1)%5;a,b=6+i,6+(i+1)%5
        out.extend([(0,u,v),(v,u,a),(v,a,b),(11,b,a)])
    out=[min(F,F[1:]+F[:1],F[2:]+F[:2]) for F in out]
    return sorted(out,key=lambda F:tuple(sorted(F)))


def distances(adj,source):
    d={source:0};previous={source:None};heap=[(0,source)]
    while heap:
        value,u=heappop(heap)
        if value!=d[u]:continue
        for v,w in sorted(adj[u].items()):
            new=value+w
            if v not in d or new<d[v]:
                d[v]=new;previous[v]=u;heappush(heap,(new,v))
    assert len(d)==len(adj)
    return d,previous


def shortest_path(adj,source,target):
    d,previous=distances(adj,source);path=[target]
    while path[-1]!=source:path.append(previous[path[-1]])
    path.reverse();return path,d[target]


def components(adj,removed):
    left=set(adj)-set(removed);out=[]
    while left:
        part={left.pop()};todo=list(part)
        while todo:
            u=todo.pop();new=set(adj[u])&left;left-=new;part|=new;todo.extend(new)
        out.append(part)
    return sorted(out,key=lambda K:(-len(K),sorted(K)))


def metric(which):
    data=certificate();center={(u,v):c for u,v,c in data['core_edges']}
    if which=='center':return {e:151*c for e,c in center.items()}
    index=int(which.split(':')[1]);path=[p for pair in data['candidate_pairs'] for p in pair][index]
    selected={tuple(sorted((u,v))) for u,v in zip(path,path[1:])}
    return {e:(158 if e in selected else 144)*c for e,c in center.items()}


def build(depths,prices,pricing='boundary_long'):
    assert len(depths)==20 and all(type(d) is int and d>=0 for d in depths)
    faces=core_faces();adj={v:{} for v in range(12)}
    def edge(u,v,w):
        assert u!=v and w>0
        if v in adj[u]:assert adj[u][v]==w
        adj[u][v]=adj[v][u]=w
    for (u,v),w in prices.items():edge(u,v,w)
    core_d={v:distances(adj,v)[0] for v in range(12)}
    long=1+max(value for row in core_d.values() for value in row.values())
    triangles=[];patches=[];bags=[];parents=[];atom={v:v for v in range(12)};offset=12
    for f,(face,depth) in enumerate(zip(faces,depths)):
        count=(3**depth-1)//2;K=set(range(offset,offset+count));patches.append(K)
        for v in K:adj[v]={};atom[v]=12+f
        local_bags=[None]*count;local_parents=[-1]*count
        def split(F,level,rank,parent):
            if level==depth:triangles.append(F);return
            index=(3**level-1)//2+rank;v=offset+index
            local_bags[index]=set(F)|{v};local_parents[index]=parent
            for u in F:
                w=long if pricing=='all_long' or u<12 else 1+(u+v)%11
                edge(u,v,w)
            a,b,c=F
            for j,T in enumerate(((a,b,v),(b,c,v),(c,a,v))):split(T,level+1,3*rank+j,index)
        split(face,0,0,-1)
        if not count:local_bags=[set(face)];local_parents=[-1]
        bags.append(local_bags);parents.append(local_parents);offset+=count
    return {'adj':adj,'core_faces':faces,'triangles':triangles,'patches':patches,
            'bags':bags,'parents':parents,'atom':atom,'prices':prices,'core_d':core_d,
            'long':long,'depths':list(depths),'pricing':pricing}


def centroid_bag(graph,index,mass):
    K=graph['patches'][index];bags=graph['bags'][index];parents=graph['parents'][index]
    total=sum(mass.values());inside=sum(mass[v] for v in K)
    assert 2*inside>total and K
    children=[[] for _ in bags]
    for i,parent in enumerate(parents):
        if parent>=0:children[parent].append(i)
    # BFS labels put every parent before its children. Assign each patch
    # vertex to its insertion bag, with all outside mass at an extra leaf.
    offset=min(K);sub=[mass[offset+i] for i in range(len(bags))]
    for i in range(len(bags)-1,0,-1):sub[parents[i]]+=sub[i]
    for i,bag in enumerate(bags):
        branch=[total-sub[i]]+[sub[j] for j in children[i]]
        if all(2*w<=total for w in branch):return sorted(bag),i
    raise AssertionError('no local centroid although the patch is heavy')


def separator(graph,mass):
    adj=graph['adj'];total=sum(mass.values())
    if total==0:return [[0]],{'branch':'zero'}
    heavy=next((f for f,K in enumerate(graph['patches']) if 2*sum(mass[v] for v in K)>total),None)
    if heavy is not None:
        bag,node=centroid_bag(graph,heavy,mass);paths=[]
        for i in range(0,len(bag),2):
            path,_=shortest_path(adj,bag[i],bag[min(i+1,len(bag)-1)]);paths.append(path)
        return paths,{'branch':'heavy_patch','patch':heavy,'bag':bag,'node':node}
    for i,pair in enumerate(certificate()['candidate_pairs']):
        if all(2*sum(mass[v] for v in K)<=total for K in components(adj,set(pair[0])|set(pair[1]))):
            return pair,{'branch':f'pair_{i+1}'}
    raise AssertionError('light patches left no balancing core pair')


def fixture_hash(graph):
    rows=sorted((u,v,w) for u in graph['adj'] for v,w in graph['adj'][u].items() if u<v)
    payload={'edges':rows,'oriented_faces':sorted(graph['triangles']),
             'patches':[sorted(K) for K in graph['patches']],
             'bags':[[sorted(B) for B in group] for group in graph['bags']],
             'parents':graph['parents']}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
