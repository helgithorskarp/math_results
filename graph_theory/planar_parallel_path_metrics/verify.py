"""Exact regression checks for the written parallel-path metric theorem.

Python 3.11+, standard library only.  No finite run proves the all-order
theorem.  Floyd distances and set components directly check the witnesses.
"""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import json


def edge(a,b):
    return tuple(sorted((a,b)))


def number(*args):
    return int.from_bytes(sha256(':'.join(map(str,args)).encode()).digest()[:8],'big')


def adjacency(n,cost):
    adj=[set() for _ in range(n)]
    for a,b in cost:
        assert 0<=a<b<n
        adj[a].add(b);adj[b].add(a)
    return adj


def distances(n,cost):
    inf=sum(cost.values())+1
    d=[[0 if a==b else inf for b in range(n)] for a in range(n)]
    for (a,b),w in cost.items():
        assert w>0
        d[a][b]=d[b][a]=w
    for k in range(n):
        for a in range(n):
            for b in range(n):d[a][b]=min(d[a][b],d[a][k]+d[k][b])
    assert all(x<inf for row in d for x in row)
    return d


def components(adj,removed):
    unseen=set(range(len(adj)))-set(removed);out=[]
    while unseen:
        s=min(unseen);unseen.remove(s);todo=[s];part={s}
        while todo:
            u=todo.pop();new=adj[u]&unseen;unseen-=new;part|=new;todo.extend(new)
        out.append(part)
    return out


def path_length(p,cost):
    assert p and len(set(p))==len(p)
    return sum(cost[edge(a,b)] for a,b in zip(p,p[1:]))


def check_geodesic(p,cost,d):
    assert path_length(p,cost)==d[p[0]][p[-1]]


def validate(n,cost,branches):
    assert branches
    a,b=branches[0][0],branches[0][-1];assert a!=b
    seen=set();owner={};core={}
    for i,p in enumerate(branches):
        assert p[0]==a and p[-1]==b and len(set(p))==len(p)
        assert not (set(p[1:-1])&seen)
        seen.update(p[1:-1]);owner.update({v:i for v in p[1:-1]})
        for u,v in zip(p,p[1:]):
            e=edge(u,v);assert e not in core
            core[e]=cost[e]
    assert seen|{a,b}==set(range(n)), 'The parallel paths must span every vertex'
    dh=distances(n,core);dg=distances(n,cost)
    assert dh==dg, 'H must preserve all ambient distances'
    r=len(branches)
    for (u,v),w in cost.items():
        assert w>=dh[u][v]
        if u in owner and v in owner and r>=3:
            assert (owner[u]-owner[v])%r in (0,1,r-1)
    return dg


def cover(branches,cost,i,j):
    halves=[]
    for p in (branches[i],branches[j]):
        coordinates=[0]
        for a,b in zip(p,p[1:]):coordinates.append(coordinates[-1]+cost[edge(a,b)])
        length=coordinates[-1]
        left=max(k for k,x in enumerate(coordinates) if 2*x<=length)
        right=min(k for k,x in enumerate(coordinates) if 2*x>=length)
        halves.append((p[:left+1],p[right:]))
    (li,ri),(lj,rj)=halves
    return [list(reversed(li))+lj[1:],ri+list(reversed(rj))[1:]]


def median(branches,masses):
    assert all(w>=0 for w in masses)
    weights=[sum(masses[v] for v in p[1:-1]) for p in branches]
    total=sum(weights)
    if len(branches)==2 or total==0 or 2*weights[0]>=total:return 0,1
    partial=weights[0]
    for j in range(1,len(branches)):
        partial+=weights[j]
        if 2*partial>=total:return 0,j
    raise AssertionError('Missing median')


def sphere(n,faces,cost):
    darts=set();rotation=[{} for _ in range(n)]
    for f in faces:
        assert len(f)>=3 and len(set(f))==len(f)
        for i,v in enumerate(f):
            before,after=f[i-1],f[(i+1)%len(f)]
            assert (v,after) not in darts and before not in rotation[v]
            darts.add((v,after));rotation[v][before]=after
    assert {edge(a,b) for a,b in darts}==set(cost)
    assert all((b,a) in darts for a,b in darts)
    for p in rotation:
        assert p and set(p)==set(p.values())
        first=min(p);seen=set();v=first
        while v not in seen:seen.add(v);v=p[v]
        assert v==first and seen==set(p)
    assert n-len(cost)+len(faces)==2
    assert len(components(adjacency(n,cost),set()))==1


def annulus(r,h,seed,with_faces=False):
    n=2+r*h
    def v(i,j):return 2+(i%r)*h+j
    branches=[[0]+[v(i,j) for j in range(h)]+[1] for i in range(r)]
    core={edge(a,b):(1 if seed==0 else 1+number('price',r,h,seed,a,b)%31)
          for p in branches for a,b in zip(p,p[1:])}
    dh=distances(n,core);cost=dict(core);faces=[]
    for i in range(r):
        faces.append([0,v(i+1,0),v(i,0)])
        faces.append([1,v(i,h-1),v(i+1,h-1)])
        for j in range(h):
            x,y=v(i,j),v(i+1,j);e=edge(x,y)
            cost[e]=dh[x][y]+(number('slack',seed,x,y)%5 if seed else 0)
            if j+1<h:
                a,b,c,d=v(i,j),v(i+1,j),v(i+1,j+1),v(i,j+1)
                if (i+j)%2==0:
                    faces.extend([[a,b,c],[a,c,d]]);x,y=a,c
                else:
                    faces.extend([[a,b,d],[b,c,d]]);x,y=b,d
                cost[edge(x,y)]=dh[x][y]+(number('slack',seed,x,y)%5 if seed else 0)
    sphere(n,faces,cost)
    if with_faces:return n,cost,branches,faces
    return n,cost,branches


def mass_vectors(n,tag):
    yield [0]*n
    yield [1]*n
    yield [7]+[0]*(n-1)
    yield [0,0,7]+[0]*(n-3)
    yield [Fraction(number('rational',tag,v)%11,1+number('denom',tag,v)%7) for v in range(n)]
    for k in range(11):yield [number('mass',tag,k,v)%10 for v in range(n)]
    if n<=8:
        yield from (list(x) for x in product((0,1),repeat=n))


def marked_face_control():
    # The unweighted topology is a triangulated capped 6-by-3 cylinder.
    # Its alternating diagonals make three helical cheap core branches.
    n,topology,_=annulus(6,3,0)
    branches=[[0]+[2+((start+j)%6)*3+j for j in range(3)]+[1] for start in (0,2,4)]
    active=set().union(*(set(p) for p in branches));marked=set(range(n))-active
    cheap={edge(a,b):1 for p in branches for a,b in zip(p,p[1:])}
    for u in marked:
        i,j=divmod(u-2,3);parent=2+((i-1)%6)*3+j
        assert edge(u,parent) in topology and parent in active
        cheap[edge(u,parent)]=1
    expensive=sum(cheap.values())+1
    cost={e:cheap.get(e,expensive) for e in topology};adj=adjacency(n,cost)
    d=distances(n,cost);failures=[]
    for i,j in combinations(range(3),2):
        qs=cover(branches,cost,i,j)
        for q in qs:check_geodesic(q,cost,d)
        removed=set(branches[i])|set(branches[j])
        assert set(qs[0])|set(qs[1])==removed
        weights=sorted(len(c&marked) for c in components(adj,removed))
        assert max(weights)==6
        failures.append({'branches':[i,j],'component_marked_counts':weights})
    # Supply a positive separator as an independently distance-checked control.
    paths=[]
    for s in range(n):
        for t in range(s,n):
            p=[s]
            while p[-1]!=t:
                x=p[-1]
                p.append(min(u for u in adj[x] if cost[edge(x,u)]+d[u][t]==d[x][t]))
            paths.append(p)
    paths.sort(key=lambda p:(-len(set(p)&marked),-len(p),p))
    witness=None
    for p,q in combinations_with_replacement(paths,2):
        counts=sorted(len(c&marked) for c in components(adj,set(p)|set(q)))
        if max(counts,default=0)<=4:
            for path in (p,q):check_geodesic(path,cost,d)
            witness={'paths':[p,q],'component_marked_counts':counts};break
    assert witness is not None
    four_sets=0
    for cut in combinations(range(n),4):
        four_sets+=1
        assert any(len(c&marked)>=5 for c in components(adj,set(cut)))
    # The same topology and masses satisfy the new theorem when the
    # longitudinal columns, rather than only the helical core, carry the metric.
    _,column_cost,column_branches=annulus(6,3,1)
    assert set(column_cost)==set(cost)
    column_d=validate(n,column_cost,column_branches)
    weights=[int(v in marked) for v in range(n)]
    i,j=median(column_branches,weights);column_pair=cover(column_branches,column_cost,i,j)
    for q in column_pair:check_geodesic(q,column_cost,column_d)
    column_counts=sorted(len(c&marked) for c in components(adj,set(column_pair[0])|set(column_pair[1])))
    assert max(column_counts)<=4
    return {'vertices':n,'edges':len(cost),'marked_vertices':sorted(marked),
            'cheap_edges':[list(e) for e in sorted(cheap)],'cheap_length':1,'other_length':expensive,
            'core_branches':branches,'all_full_branch_pairs_fail':failures,'positive_separator':witness,
            'four_vertex_cuts_checked':four_sets,'balanced_four_vertex_cuts':0,
            'longitudinal_metric_positive_separator':{'paths':column_pair,'component_marked_counts':column_counts}},(n,cost,branches)


def interval_scope_control():
    # All vertices carry positive mass. Test every interval and every triangle,
    # so this comparison is independent of the choice of plane embedding.
    n,cost,branches,faces=annulus(6,3,1,with_faces=True)
    d=validate(n,cost,branches)
    intervals=[[{v for v in range(n) if d[s][v]+d[v][t]==d[s][t]}
                for t in range(n)] for s in range(n)]
    triangles=[t for t in combinations(range(n),3)
               if all(edge(a,b) in cost for a,b in combinations(t,2))]
    assert all(len(f)==3 for f in faces) and len(cost)==3*n-6
    largest_interval=max(len(x) for row in intervals for x in row)
    largest_facial_union=max(len(set().union(*(intervals[r][v] for v in t)))
                             for r in range(n) for t in triangles)
    assert (n,len(triangles),largest_interval,largest_facial_union)==(20,36,12,17)
    i,j=median(branches,[1]*n);qs=cover(branches,cost,i,j)
    for q in qs:check_geodesic(q,cost,d)
    sizes=sorted(len(c) for c in components(adjacency(n,cost),set(qs[0])|set(qs[1])))
    assert max(sizes,default=0)<=n//2
    return {'vertices':n,'positive_mass_vertices':n,'metric_parameters':[6,3,1],
            'maximum_interval_vertices':largest_interval,'triangles_checked':len(triangles),
            'maximum_rooted_triangle_interval_union_vertices':largest_facial_union,
            'positive_separator':{'paths':qs,'component_vertex_counts':sizes}}


def main():
    totals={'annular_metrics':0,'branch_pairs':0,'mass_cases':0,'nongeodesic_full_branches':0,
            'spherical_embeddings':0,'boundary_metrics':0,'rejected_controls':0,
            'zero_face_metrics':0,'zero_face_branch_pairs':0,'zero_face_mass_cases':0}
    for r in (3,4,5,6,8,12):
        for h in (1,2,3,5,8):
            for seed in (0,1):
                n,cost,branches=annulus(r,h,seed);d=validate(n,cost,branches);adj=adjacency(n,cost)
                totals['annular_metrics']+=1;totals['spherical_embeddings']+=1
                totals['nongeodesic_full_branches']+=sum(path_length(p,cost)>d[0][1] for p in branches)
                for i,j in combinations(range(r),2):
                    qs=cover(branches,cost,i,j)
                    assert set(qs[0])|set(qs[1])==set(branches[i])|set(branches[j])
                    for q in qs:check_geodesic(q,cost,d)
                    totals['branch_pairs']+=1
                for w in mass_vectors(n,(r,h,seed)):
                    i,j=median(branches,w);qs=cover(branches,cost,i,j)
                    for q in qs:check_geodesic(q,cost,d)
                    assert all(2*sum(w[v] for v in c)<=sum(w) for c in components(adj,set(qs[0])|set(qs[1])))
                    totals['mass_cases']+=1
    # Unequal branch orders, a direct pole edge, and rational edge lengths.
    for sizes in ((7,),(1,5),(1,2,4,7)):
        branches=[];nextv=2
        for length in sizes:
            internal=list(range(nextv,nextv+length-1));nextv+=length-1
            branches.append([0]+internal+[1])
        cost={edge(a,b):Fraction(1+number('boundary',a,b)%17,1+number('q',a,b)%5)
              for p in branches for a,b in zip(p,p[1:])}
        d=validate(nextv,cost,branches)
        if len(branches)==1:check_geodesic(branches[0],cost,d)
        else:
            for i,j in combinations(range(len(branches)),2):
                qs=cover(branches,cost,i,j)
                for q in qs:check_geodesic(q,cost,d)
                assert set(qs[0])|set(qs[1])==set(branches[i])|set(branches[j])
        totals['boundary_metrics']+=1
    # Nonspanning isometric H: all additional facial vertices have zero mass.
    for r,h in ((3,2),(4,2),(5,3)):
        base_n,cost,branches,faces=annulus(r,h,1,with_faces=True)
        original_d=validate(base_n,cost,branches);price=max(map(max,original_d))+1
        augmented=dict(cost);new_faces=[]
        for i,f in enumerate(faces):
            center=base_n+i
            for a,b in zip(f,f[1:]+f[:1]):
                augmented[edge(center,a)]=price
                new_faces.append([a,b,center])
        n=base_n+len(faces);sphere(n,new_faces,augmented)
        d=distances(n,augmented);adj=adjacency(n,augmented)
        assert [row[:base_n] for row in d[:base_n]]==original_d
        for i,j in combinations(range(r),2):
            qs=cover(branches,augmented,i,j)
            for q in qs:check_geodesic(q,augmented,d)
            assert set(qs[0])|set(qs[1])==set(branches[i])|set(branches[j])
            totals['zero_face_branch_pairs']+=1
        for w in mass_vectors(base_n,('zero',r,h)):
            w=w+[0]*(n-base_n);i,j=median(branches,w);qs=cover(branches,augmented,i,j)
            for q in qs:check_geodesic(q,augmented,d)
            assert all(2*sum(w[v] for v in c)<=sum(w) for c in components(adj,set(qs[0])|set(qs[1])))
            totals['zero_face_mass_cases']+=1
        totals['zero_face_metrics']+=1;totals['spherical_embeddings']+=1
    control,bad_span=marked_face_control()
    n,cost,branches=annulus(5,2,1)
    bad_metric=dict(cost);bad_metric[edge(2,4)]=Fraction(1,100)
    bad_order=dict(cost);bad_order[edge(2,6)]=sum(cost.values())
    bad_positive=dict(cost);bad_positive[edge(0,2)]=0
    checks=[lambda:validate(n,bad_metric,branches),lambda:validate(n,bad_order,branches),
            lambda:validate(n,bad_positive,branches),lambda:validate(*bad_span),
            lambda:path_length([0,2,0],cost),lambda:median(branches,[-1]+[0]*(n-1))]
    for test in checks:
        try:test()
        except (AssertionError,KeyError):totals['rejected_controls']+=1
    assert totals['rejected_controls']==len(checks)
    out={'status':'PASS','counts':totals,'marked_face_control':control,
         'interval_scope_control':interval_scope_control(),
         'scope':'Regression evidence for the written all-order proof; no unrestricted planar counterexample claim.'}
    path=Path(__file__).with_name('expected.json')
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:assert out==json.loads(path.read_text()), 'Expected output differs'
    else:path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS',**totals,'face_control_full_branch_pairs':3,'face_control_maximum_remaining':6},sort_keys=True))


if __name__=='__main__':main()
