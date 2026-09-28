"""Exact finite checks for the written nine-marked-face theorem.

Python 3.11+, standard library only. No solver or census is a premise.
The construction uses midpoint halves; Dijkstra and component searches
check the resulting paths in the original complete graph, including ties.
"""
from fractions import Fraction
from hashlib import sha256
from heapq import heappush,heappop
from itertools import product,combinations
from math import lcm
from pathlib import Path
import argparse,json


def edge(u,v):return tuple(sorted((u,v)))


def number(*xs):return int.from_bytes(sha256(':'.join(map(str,xs)).encode()).digest()[:8],'big')


def adjacency(n,cost):
    adj=[{} for _ in range(n)]
    for (a,b),c in cost.items():
        assert 0<=a<b<n and c>0
        adj[a][b]=c;adj[b][a]=c
    return adj


def distances(adj):
    rows=[];routes=[]
    for s in range(len(adj)):
        d=[None]*len(adj);p=[None]*len(adj);d[s]=0;p[s]=(s,);q=[(0,s)]
        while q:
            x,v=heappop(q)
            if d[v]!=x:continue
            for u,c in sorted(adj[v].items()):
                if d[u] is None or x+c<d[u]:
                    d[u]=x+c;p[u]=p[v]+(u,);heappush(q,(x+c,u))
        assert all(x is not None for x in d)
        rows.append(d);routes.append(p)
    return rows,routes


def components(adj,removed):
    unseen=set(range(len(adj)))-set(removed);out=[]
    while unseen:
        first=min(unseen);unseen.remove(first);todo=[first];part={first}
        while todo:
            v=todo.pop();new=set(adj[v])&unseen;unseen-=new;part|=new;todo.extend(new)
        out.append(part)
    return out


def path_check(path,cost,d):
    assert path and len(path)==len(set(path))
    assert sum(cost[edge(a,b)] for a,b in zip(path,path[1:]))==d[path[0]][path[-1]]


def template():
    def v(i,j):return 2+(i%6)*3+j
    edges=set();faces=[]
    for i in range(6):
        faces.extend([[0,v(i+1,0),v(i,0)],[1,v(i,2),v(i+1,2)]])
        edges.update([edge(0,v(i,0)),edge(1,v(i,2))])
        for j in range(3):
            edges.add(edge(v(i,j),v(i+1,j)))
            if j<2:
                a,b,c,d=v(i,j),v(i+1,j),v(i+1,j+1),v(i,j+1)
                edges.add(edge(a,d))
                if (i+j)%2==0:edges.add(edge(a,c));faces.extend([[a,b,c],[a,c,d]])
                else:edges.add(edge(b,d));faces.extend([[a,b,d],[b,c,d]])
    branches=[[0]+[v(start+j,j) for j in range(3)]+[1] for start in (0,2,4)]
    leaves={v(start+j,j):v(start+j+1,j) for start in (0,2,4) for j in range(3)}
    core={edge(a,b) for p in branches for a,b in zip(p,p[1:])}
    cheap=core|{edge(a,b) for a,b in leaves.items()}
    assert len(edges)==54 and len(core)==12 and len(cheap)==21
    assert cheap<=edges and len(leaves)==9
    return edges,faces,branches,leaves,core,cheap


def embedding(n,edges,faces):
    rotation=[{} for _ in range(n)];incidence={}
    for k,f in enumerate(faces):
        assert len(set(f))==len(f)>=3
        for i,v in enumerate(f):
            before,after=f[i-1],f[(i+1)%len(f)]
            assert (v,after) not in incidence and before not in rotation[v]
            incidence[v,after]=k;rotation[v][before]=after
    assert {edge(a,b) for a,b in incidence}==set(edges)
    assert all((b,a) in incidence for a,b in incidence)
    for p in rotation:
        assert p and set(p)==set(p.values())
        start=min(p);v=start;seen=set()
        while v not in seen:seen.add(v);v=p[v]
        assert v==start and seen==set(p)
    assert n-len(edges)+len(faces)==2
    assert len(components(adjacency(n,{e:1 for e in edges}),set()))==1
    return incidence


def check_regions(edges,faces,branches,leaves,core):
    incidence=embedding(20,edges,faces)
    dual=[set() for _ in faces]
    for a,b in edges-core:
        x,y=incidence[a,b],incidence[b,a];dual[x].add(y);dual[y].add(x)
    regions=components(dual,set());assert len(regions)==3
    marked=set(leaves.values())
    assert all(not (a in marked and b in marked) for a,b in edges)
    for i,p in enumerate(branches):
        expected={leaves[v] for v in p[1:-1]}
        found=[r for r in regions if expected & set().union(*(set(faces[k]) for k in r))]
        assert len(found)==1;r=found[0]
        assert marked & set().union(*(set(faces[k]) for k in r))==expected
        boundary={edge(a,b) for a,b in core if (incidence[a,b] in r)!=(incidence[b,a] in r)}
        want={edge(a,b) for q in (branches[i],branches[(i+1)%3]) for a,b in zip(q,q[1:])}
        assert boundary==want
    assert all(len(set(f)&marked)==1 for f in faces)


def perturb(cost):
    denominator=lcm(*(Fraction(c).denominator for c in cost.values()))
    scale=1<<len(cost)
    return {e:int(c*denominator)*scale+(1<<i) for i,(e,c) in enumerate(sorted(cost.items()))}


def halves(branch,cost):
    coords=[0]
    for a,b in zip(branch,branch[1:]):coords.append(coords[-1]+cost[edge(a,b)])
    assert all(2*x!=coords[-1] for x in coords[1:-1])
    left=max(i for i,x in enumerate(coords) if 2*x<coords[-1])
    right=min(i for i,x in enumerate(coords) if 2*x>coords[-1])
    return branch[:left+1],branch[right:]


def uniform_pair(branches,leaves,cost):
    perturbed=perturb(cost);parts=[halves(p,perturbed) for p in branches]
    def via_a(i,j):return list(reversed(parts[i][0]))+parts[j][0][1:]
    def via_b(i,j):return parts[i][1]+list(reversed(parts[j][1]))[1:]
    for i,(a,b) in enumerate(parts):
        if len(a)>1 and len(b)>1:
            j=(i-1)%3;qa=via_a(i,j);qb=via_b(i,j)
            assert qa[0]!=qb[0]
            return [[leaves[qa[0]]]+qa,[leaves[qb[0]]]+qb],'middle'
    A=[i for i,(a,b) in enumerate(parts) if len(a)>1]
    B=[i for i,(a,b) in enumerate(parts) if len(b)>1]
    assert set(A)|set(B)=={0,1,2} and not(set(A)&set(B))
    if A and B:
        i,j=A[0],B[0];k=({0,1,2}-{i,j}).pop()
        return [via_a(i,k),via_b(j,k)],'mixed_outer'
    k=min(range(3),key=lambda i:sum(perturbed[edge(a,b)] for a,b in zip(branches[i],branches[i][1:])))
    i,j=sorted({0,1,2}-{k})
    return [branches[k][:],via_a(i,j) if A else via_b(i,j)],'all_A' if A else 'all_B'


def check_metric(label,core_prices,leaf_prices,seed,augment=False,binary=False):
    edges,faces,branches,leaves,core,cheap=template()
    cost={edge(a,b):core_prices[i][j] for i,p in enumerate(branches) for j,(a,b) in enumerate(zip(p,p[1:]))}
    cost.update({edge(v,z):leaf_prices[i] for i,(v,z) in enumerate(sorted(leaves.items()))})
    dh,routes=distances(adjacency(20,cost))
    full={e:cost[e] if e in cheap else dh[e[0]][e[1]]+number('slack',seed,*e)%3 for e in edges}
    n=20
    if augment:
        newfaces=[];price=max(map(max,dh))+1
        for k,f in enumerate(faces):
            z=20+k
            for a,b in zip(f,f[1:]+f[:1]):full[edge(a,z)]=price;newfaces.append([a,b,z])
        n+=len(faces);faces=newfaces
    embedding(n,full,faces)
    adj=adjacency(n,full);dg,_=distances(adj)
    assert [row[:20] for row in dg[:20]]==dh
    pair,case=uniform_pair(branches,leaves,cost)
    for p in pair:path_check(p,full,dg)
    support=sorted(leaves.values());removed=set(pair[0])|set(pair[1])
    counts=sorted(len(c&set(support)) for c in components(adj,removed))
    assert max(counts,default=0)<=4
    if case!='middle':assert set().union(*map(set,branches))<=removed
    vectors=[[0]*9,[1]*9,[2]+[1]*8,[100]+[1]*8]
    vectors += [[100+number('near',seed,k,v)%7 for v in support] for k in range(5)]
    vectors += [[Fraction(number('mass',seed,k,v)%13,1+number('denom',seed,k,v)%7) for v in support] for k in range(5)]
    if binary:vectors+=list(product((0,1),repeat=9))
    weighted=0;heavy=0
    for values in vectors:
        w=[0]*n
        for v,m in zip(support,values):w[v]=m
        W=sum(w);largest=sorted(support,key=lambda v:(-w[v],v))[:4]
        if 2*sum(w[v] for v in largest)>=W:
            chosen=[routes[largest[0]][largest[1]],routes[largest[2]][largest[3]]];heavy+=1
        else:chosen=pair
        for p in chosen:path_check(p,full,dg)
        assert all(2*sum(w[v] for v in c)<=W for c in components(adj,set(chosen[0])|set(chosen[1])))
        weighted+=1
    ties=0
    for prices in core_prices:
        total=sum(prices);prefix=0
        for q in prices[:-1]:prefix+=q;ties+=2*prefix==total
    return {'label':label,'case':case,'paths':pair,'component_marked_counts':counts,
            'original_midpoint_ties':ties,'weighted_cases':weighted,'top_four_cases':heavy,'vertices':n}


def sweep_controls():
    edges,faces,branches,leaves,core,cheap=template();marked=set(leaves.values())
    def v(i,j):return 2+(i%6)*3+j
    columns=[[0]+[v(i,j) for j in range(3)]+[1] for i in range(6)]
    cost={edge(a,b):1+number('price',6,3,1,a,b)%31 for p in columns for a,b in zip(p,p[1:])}
    dh,_=distances(adjacency(20,cost))
    for i in range(6):
        for j in range(3):
            x,y=v(i,j),v(i+1,j);cost[edge(x,y)]=dh[x][y]+number('slack',1,x,y)%5
            if j<2:
                a,b,c,d=v(i,j),v(i+1,j),v(i+1,j+1),v(i,j+1)
                x,y=(a,c) if (i+j)%2==0 else (b,d)
                cost[edge(x,y)]=dh[x][y]+number('slack',1,x,y)%5
    assert set(cost)==edges
    adj=adjacency(20,cost);d,_=distances(adj);assert d==dh
    face=[12,16,13];assert face in faces
    J={x for x in range(20) if any(d[0][x]+d[x][z]==d[0][z] for z in face)}
    comparisons=[]
    for support,p,expected in [(set(range(20)),[0,2,3,4,1,13],(3,6,[6,6])),
                               (marked,[0,17,18,19,1,13],(2,3,[1,4]))]:
        q=[0,11,12]
        for path in [p,q]:path_check(path,cost,d)
        E=len(support-J);p_mass=len(set(p)&support)
        counts=sorted(len(c&support) for c in components(adj,set(p)|set(q)))
        assert (E,p_mass,counts)==expected and E<=p_mass
        comparisons.append({'total_mass':len(support),'root':0,'face':face,'outside_mass':E,
                            'first_path_mass':p_mass,'paths':[p,q],'component_masses':counts})
    # The marked-leaf metric remains outside both full and error criteria.
    base={e:1 for e in cheap};d,_=distances(adjacency(20,base))
    intervals=[[{z for z in marked if d[s][z]+d[z][t]==d[s][t]} for t in range(20)] for s in range(20)]
    mi=max(len(x) for row in intervals for x in row)
    mf=max(len(set().union(*(intervals[r][z] for z in f))) for r in range(20) for f in faces)
    assert mi==mf==2
    return {'longitudinal_error_bound_witnesses':comparisons,
            'marked_leaf_maximum_interval_marks':mi,'marked_leaf_maximum_facial_union_marks':mf}


def main():
    edges,faces,branches,leaves,core,cheap=template();check_regions(edges,faces,branches,leaves,core)
    rows=[];forms={'M':[2,3,5,2],'A':[1,1,1,9],'B':[9,1,1,1]}
    for k,pattern in enumerate(product('MAB',repeat=3)):
        rows.append(check_metric(''.join(pattern),[forms[t] for t in pattern],[1]*9,k,binary=k==0))
    for k,pattern in enumerate(product('AB',repeat=3)):
        for seed in range(4):
            q=[]
            for i,t in enumerate(pattern):
                tail=[1+number('outer',k,seed,i,j)%71 for j in range(3)]
                large=sum(tail)+1+number('large',k,seed,i)%37
                q.append(tail+[large] if t=='A' else [large]+tail)
            rows.append(check_metric('unequal '+''.join(pattern)+' '+str(seed),q,[1]*9,k*4+seed+600))
    for seed in range(128):
        q=[[1+number('core',seed,i,j)%127 for j in range(4)] for i in range(3)]
        leaf=[1+number('leaf',seed,j)%31 for j in range(9)]
        rows.append(check_metric('integer '+str(seed),q,leaf,seed+100))
    for seed in range(32):
        q=[[Fraction(1+number('num',seed,i,j)%23,1+number('den',seed,i,j)%11) for j in range(4)] for i in range(3)]
        leaf=[Fraction(1+number('ln',seed,j)%19,1+number('ld',seed,j)%7) for j in range(9)]
        rows.append(check_metric('rational '+str(seed),q,leaf,seed+300))
    for k,q in enumerate(([1,1,1,1],[6,1,2,3],[1,2,3,6],[2,5,4,3])):
        rows.append(check_metric('ties '+str(k),[q,q,q],[1]*9,k+400))
        rows.append(check_metric('augmented '+str(k),[q,q,q],[1]*9,k+500,augment=True))
    kinds={k:sum(r['case']==k for r in rows) for k in ['middle','all_A','all_B','mixed_outer']}
    assert all(kinds.values())
    base={e:1 for e in cheap};d,_=distances(adjacency(20,base))
    full={e:base.get(e,d[e[0]][e[1]]) for e in edges}
    bad_price=dict(base);bad_price[min(base)]=0
    bad_extra=dict(full);bad_extra[edge(0,5)]=Fraction(1,100)
    bad_leaves=dict(leaves);x,y=branches[0][1],branches[1][1]
    bad_leaves[x],bad_leaves[y]=bad_leaves[y],bad_leaves[x]
    rejected=0
    def isometry_check():assert distances(adjacency(20,bad_extra))[0]==d
    controls=[lambda:adjacency(20,bad_price),lambda:path_check([0,2,0],full,d),
              isometry_check,lambda:check_regions(edges,faces,branches,bad_leaves,core)]
    for test in controls:
        try:test()
        except (AssertionError,KeyError):rejected+=1
    assert rejected==len(controls)
    out={'status':'PASS','metrics':len(rows),'case_counts':kinds,'original_midpoint_ties':sum(r['original_midpoint_ties'] for r in rows),
         'weighted_cases':sum(r['weighted_cases'] for r in rows),'top_four_cases':sum(r['top_four_cases'] for r in rows),
         'augmented_metrics':sum(r['vertices']>20 for r in rows),'maximum_vertices':max(r['vertices'] for r in rows),
         'rejected_controls':rejected,
         'marked_facial_groups':[[leaves[v] for v in p[1:-1]] for p in branches],
         'sweep_comparison':sweep_controls(),
         'examples':[next(r for r in rows if r['case']==k) for k in kinds],
         'scope':'Exact regression of a written real-parameter theorem; no unrestricted counterexample claim.'}
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    path=Path(__file__).with_name('expected.json')
    if args.check:assert json.loads(path.read_text())==out
    else:path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('examples','scope','marked_facial_groups','sweep_comparison')},sort_keys=True))


if __name__=='__main__':main()
