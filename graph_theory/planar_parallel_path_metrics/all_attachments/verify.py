"""Check the finite certificate for all pendant attachments and all prices.

Python 3.11+, standard library only. This file imports no search code.
It verifies universal geodesic templates, full-graph components, and
attachment coverage by recursive four-valued case splitting, not bitsets.
"""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations,product
from pathlib import Path
import argparse,copy,json

HERE=Path(__file__).resolve().parent


def edge(a,b):return tuple(sorted((a,b)))


def components(adj,removed):
    left=set(range(len(adj)))-set(removed);result=[]
    while left:
        root=min(left);left.remove(root);part={root};todo=[root]
        while todo:
            v=todo.pop();new=set(adj[v])&left
            left-=new;part|=new;todo.extend(new)
        result.append(part)
    return result


def fixture(data):
    n=data['vertices'];edges={tuple(e) for e in data['edges']}
    assert n==20 and len(edges)==len(data['edges'])==54
    assert all(0<=a<b<n for a,b in edges)
    def v(i,j):return 2+3*(i%6)+j
    described=set()
    for i in range(6):
        described|={edge(0,v(i,0)),edge(1,v(i,2))}
        for j in range(3):described.add(edge(v(i,j),v(i+1,j)))
        for j in range(2):
            described.add(edge(v(i,j),v(i,j+1)))
            described.add(edge(v(i,j),v(i+1,j+1)) if (i+j)%2==0 else edge(v(i+1,j),v(i,j+1)))
    assert edges==described
    branches=data['branches'];marks=data['marks']
    assert branches==[[0,2,6,10,1],[0,8,12,16,1],[0,14,18,4,1]]
    assert marks==[5,9,13,11,15,19,17,3,7]
    core=set().union(*map(set,branches))
    assert len(core)==11 and core.isdisjoint(marks) and core|set(marks)==set(range(n))
    adj=[set() for _ in range(n)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    assert len(components(adj,set()))==1
    assert all(len(adj[z])==4 and adj[z]<=core for z in marks)
    assert all(edge(a,b) in edges for p in branches for a,b in zip(p,p[1:]))
    faces=data['faces'];assert len(faces)==36
    darts={};rotations=[{} for _ in range(n)]
    for f in faces:
        assert len(f)==len(set(f))==3 and len(set(f)&set(marks))==1
        for j,v in enumerate(f):
            before,after=f[j-1],f[(j+1)%3]
            assert edge(v,after) in edges and (v,after) not in darts
            assert before not in rotations[v]
            darts[v,after]=1;rotations[v][before]=after
    assert set(darts)=={d for a,b in edges for d in ((a,b),(b,a))}
    for v,rotation in enumerate(rotations):
        assert set(rotation)==set(rotation.values())==adj[v]
        start=min(rotation);u=start;seen=set()
        while u not in seen:seen.add(u);u=rotation[u]
        assert u==start and seen==adj[v]
    assert n-len(edges)+len(faces)==2
    return adj,branches,marks


def generators(branches,region,shortest):
    halves=[(p[:k+1],p[k+1:]) for p,k in zip(branches,region)]
    out=[branches[shortest]]
    for i,j in combinations(range(3),2):
        out.append(halves[i][0][::-1]+halves[j][0][1:])
        out.append(halves[i][1]+halves[j][1][::-1][1:])
    return out


def subpath(path,walk):
    return any(path==walk[i:i+len(path)] for i in range(len(walk)-len(path)+1))


def path_conditions(path,adj,marks,gs):
    assert path and len(path)==len(set(path))
    assert all(0<=v<len(adj) for v in path)
    assert all(b in adj[a] for a,b in zip(path,path[1:]))
    assert not (set(path[1:-1])&set(marks))
    core=path[:];conditions={}
    if core[0] in marks:
        assert len(core)>=2;z=core.pop(0);conditions[z]=core[0]
    if core[-1] in marks:
        assert len(core)>=2;z=core.pop();conditions[z]=core[-1]
    assert core and not(set(core)&set(marks))
    assert any(subpath(core,g) or subpath(core[::-1],g) for g in gs)
    return conditions


def count_assignments(cubes,marks,adj):
    options=[sorted(adj[z]) for z in marks]
    terms=tuple(sorted({tuple(sorted((marks.index(z),options[marks.index(z)].index(v)) for z,v in c.items())) for c in cubes}))
    @cache
    def count(level,terms):
        if () in terms:return 4**(9-level)
        if not terms:return 0
        assert level<9 and all(t[0][0]>=level for t in terms)
        total=0
        for value in range(4):
            child=set()
            for term in terms:
                if term[0][0]>level:child.add(term)
                elif term[0][1]==value:child.add(term[1:])
            total+=count(level+1,tuple(sorted(child)))
        return total
    result=count(0,terms)
    return result,count.cache_info().currsize


def verify(data):
    adj,branches,marks=fixture(data);seen=set();templates=0;nodes=0;unconditional=0;condition_counts=Counter()
    for case in data['cases']:
        region=tuple(case['region']);s=case['shortest'];key=(region,s)
        assert len(region)==3 and all(type(k) is int and 0<=k<4 for k in region)
        assert type(s) is int and 0<=s<3 and key not in seen
        seen.add(key);gs=generators(branches,region,s);cubes=[]
        for pair in case['pairs']:
            assert len(pair)==2;cube={}
            for path in pair:
                for z,v in path_conditions(path,adj,marks,gs).items():
                    assert z not in cube or cube[z]==v
                    cube[z]=v
            removed=set(pair[0])|set(pair[1])
            assert all(len(c&set(marks))<=4 for c in components(adj,removed))
            cubes.append(cube);templates+=1;condition_counts[len(cube)]+=1
        covered,states=count_assignments(cubes,marks,adj)
        assert covered==4**9
        nodes+=states;unconditional+=any(not c for c in cubes)
    assert seen==set(product(product(range(4),repeat=3),range(3)))
    return {'status':'PASS','vertices':20,'edges':54,'triangular_faces':36,
            'attachment_assignments':4**9,'chambers':len(seen),'templates':templates,
            'unconditional_chambers':unconditional,'condition_sizes':dict(sorted(condition_counts.items())),
            'recursive_count_states':nodes}


def distances(n,cost):
    d=[[None]*n for _ in range(n)]
    for v in range(n):d[v][v]=0
    for (a,b),q in cost.items():assert q>0;d[a][b]=d[b][a]=q
    for k in range(n):
        for i in range(n):
            if d[i][k] is None:continue
            for j in range(n):
                if d[k][j] is None:continue
                q=d[i][k]+d[k][j]
                if d[i][j] is None or q<d[i][j]:d[i][j]=q
    assert all(q is not None for row in d for q in row)
    return d


def number(*xs):return int.from_bytes(sha256(':'.join(map(str,xs)).encode()).digest()[:8],'big')


def metric_checks(data):
    adj,branches,marks=fixture(data);cases={(tuple(c['region']),c['shortest']):c for c in data['cases']}
    tests=[]
    for seed,(region,s) in enumerate(product(product(range(4),repeat=3),range(3))):
        q=[[1+number('core',seed,i,j)%19 for j in range(4)] for i in range(3)]
        for i,k in enumerate(region):q[i][k]=sum(q[i])+1
        shortest_length=sum(q[s])
        q=[[x*(1 if i==s else shortest_length+1) for x in row] for i,row in enumerate(q)]
        tests.append((seed,q))
    for i,q in enumerate(([1,1,1,1],[6,1,2,3],[1,2,3,6],[2,5,4,3])):
        tests.append((192+i,[q,q,q]))
    ties=0
    for seed,q in tests:
        parents={z:sorted(adj[z])[number('parent',seed,z)%4] for z in marks}
        cheap={edge(a,b):q[i][j] for i,p in enumerate(branches) for j,(a,b) in enumerate(zip(p,p[1:]))}
        cheap.update({edge(z,v):1+number('leaf',seed,z)%23 for z,v in parents.items()})
        d=distances(20,cheap)
        full={edge(v,u):cheap.get(edge(v,u),d[v][u]+seed%2) for v in range(20) for u in adj[v] if v<u}
        assert distances(20,full)==d
        perturbed={e:c*(1<<21)+(1<<j) for j,(e,c) in enumerate(sorted(cheap.items()))}
        # Total secondary weight < 2^21: perturbed geodesics stay geodesic
        # for the original integer prices. This is a finite regression of
        # the limiting argument used for arbitrary real prices in the proof.
        lengths=[];region=[]
        for i,p in enumerate(branches):
            xs=[0]
            for a,b in zip(p,p[1:]):xs.append(xs[-1]+perturbed[edge(a,b)])
            assert all(2*x!=xs[-1] for x in xs[1:-1])
            region.append(max(j for j,x in enumerate(xs) if 2*x<xs[-1]));lengths.append(xs[-1])
            prefix=0
            for x in q[i][:-1]:prefix+=x;ties+=2*prefix==sum(q[i])
        s=min(range(3),key=lengths.__getitem__);gs=generators(branches,region,s)
        found=False
        for pair in cases[tuple(region),s]['pairs']:
            conditions={z:v for path in pair for z,v in path_conditions(path,adj,marks,gs).items()}
            if any(parents[z]!=v for z,v in conditions.items()):continue
            for path in pair:
                assert sum(full[edge(a,b)] for a,b in zip(path,path[1:]))==d[path[0]][path[-1]]
            assert all(len(c&set(marks))<=4 for c in components(adj,set(pair[0])|set(pair[1])))
            found=True;break
        assert found
    return {'exact_metrics':len(tests),'original_midpoint_equalities':ties}


def rejection_checks(data):
    bad=[]
    q=copy.deepcopy(data);q['cases'].pop();bad.append(q)
    q=copy.deepcopy(data);q['faces'][0]=q['faces'][0][::-1];bad.append(q)
    q=copy.deepcopy(data);p=q['cases'][0]['pairs'][0][0];p.append(p[0]);bad.append(q)
    q=copy.deepcopy(data);q['cases'][0]['pairs']=[[[0],[1]]];bad.append(q)
    q=copy.deepcopy(data);q['cases'][0]['pairs']=[];bad.append(q)
    for q in bad:
        try:verify(q)
        except AssertionError:continue
        raise AssertionError('malformed certificate accepted')
    return len(bad)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    raw=(HERE/'certificate.json').read_bytes();data=json.loads(raw)
    result=verify(data);result.update(metric_checks(data))
    result['rejected_controls']=rejection_checks(data)
    result['certificate_sha256']=sha256(raw).hexdigest()
    result=json.loads(json.dumps(result,sort_keys=True))
    if args.check:assert result==json.loads((HERE/'expected.json').read_text())
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
