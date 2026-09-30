#!/usr/bin/env python3
"""Definition-level rational incidence cone audit; no author imports.

All labelled simple regular graphs on 4..6 leaves are covered. Sixteen
attributed author examples also validate the infinite incidence proof.
Every guard is an exception, including arithmetic operation caps.
"""
import argparse
import hashlib
import itertools as it
import json
import resource
import time
from fractions import Fraction as Q
from pathlib import Path
from linear import check,digest,image,inverse,product,psd_rank,span_rank

def nullspace(a):
    a=[[Q(x) for x in r] for r in a];n=len(a[0]);pivots=[];row=0
    for col in range(n):
        pivot=next((i for i in range(row,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];v=a[row][col]
        a[row]=[x/v for x in a[row]]
        for i in range(len(a)):
            if i!=row:
                v=a[i][col];a[i]=[x-v*y for x,y in zip(a[i],a[row])]
        pivots.append(col);row+=1
        if row==len(a):break
    result=[]
    for col in range(n):
        if col in pivots:continue
        v=[Q(i==col) for i in range(n)]
        for r,p in enumerate(pivots):v[p]=-a[r][col]
        result.append(v)
    return result

def normalize(h,edges):
    check(type(h) is int and h>=4,'leaf count')
    check(all(len(e)==2 and all(type(v) is int and 0<=v<h for v in e) and e[0]<e[1]
              for e in edges),'ordered simple edges')
    check(len(edges)==len(set(edges)),'duplicate edge')
    degrees=[sum(i in e for e in edges) for i in range(h)];d=degrees[0]
    check(2<=d<=h-2 and degrees==[d]*h,'regular degree range')
    return d

def centered(h,edges):
    d=normalize(h,edges);ell=len(edges);m=1+2*h+ell
    A=[[Q(i!=j and (min(i,j),max(i,j)) in edges) for j in range(h)] for i in range(h)]
    B=[[Q(i in e) for e in edges] for i in range(h)]
    BB=product(B,list(map(list,zip(*B))))
    check(BB==[[d*(i==j)+A[i][j] for j in range(h)] for i in range(h)],'incidence Gram')
    alpha=Q(h-d,d);q=Q(2,d);w=Q(2*(d-1),d*(h-2));z=Q(2*(2*d-h),d*(h-4)+2)
    C=[[Q(0) for _ in range(m)] for _ in range(m)]
    # Construct the global incidence block matrix (a,X,C,E), rather than
    # dispatching entries by set types as in the author implementation.
    for i in range(m):C[i][i]=h
    xs=list(range(1,h+1));cs=list(range(h+1,2*h+1));es=list(range(2*h+1,m))
    for i in range(h):
        C[0][xs[i]]=C[xs[i]][0]=C[0][cs[i]]=C[cs[i]][0]=-1
        for j in range(h):
            C[xs[i]][xs[j]]=(h+1)*(i==j)-1
            C[cs[i]][cs[j]]=h*(i==j)-alpha*A[i][j]
            C[xs[i]][cs[j]]=C[cs[j]][xs[i]]=-(i==j)+q*A[i][j]
        for j in range(ell):
            C[xs[i]][es[j]]=C[es[j]][xs[i]]=w-(1+w)*B[i][j]
            C[cs[i]][es[j]]=C[es[j]][cs[i]]=-B[i][j]
    for i,e in enumerate(edges):
        C[0][es[i]]=C[es[i]][0]=q
        for j,f in enumerate(edges):
            C[es[i]][es[j]]=(h+2+z)*(i==j)-(1+z)*len(set(e)&set(f))+z
    masks=[1<<h]+[(1<<h)|(1<<i) for i in range(h)]+[1<<i for i in range(h)]
    masks += [(1<<i)|(1<<j) for i,j in edges]
    check(len(masks)==m and len(set(masks))==m,'domain size')
    order=sorted(range(m),key=lambda i:masks[i]);members=[masks[i] for i in order]
    return members,[[C[i][j] for j in order] for i in order],d,B,z

def lift(c,s):
    n=len(c)+1;rows=[sum(r) for r in c]
    L=[[1+sum(rows)]+[1-v for v in rows]]+[
       [1-rows[i]]+[1+v for v in r] for i,r in enumerate(c)]
    M=[[(L[i][j]-s*(i==j))/(n-s) for j in range(n)] for i in range(n)]
    check(all(sum(r)==n for r in L),'lift row sums')
    return L,M

def component_count(h,edges):
    neighbors=[set() for _ in range(h)]
    for i,j in edges:neighbors[i].add(j);neighbors[j].add(i)
    unseen=set(range(h));components=0;bipartite=0
    while unseen:
        colors={min(unseen):0};todo=list(colors);valid=True
        while todo:
            i=todo.pop()
            for j in neighbors[i]:
                if j not in colors:colors[j]=1-colors[i];todo.append(j)
                elif colors[j]==colors[i]:valid=False
        unseen-=set(colors);components+=1;bipartite+=valid
    return components,bipartite

def audit(h,edges,modules=False):
    members,c,d,B,z=centered(h,edges);m=len(members);n=m+1;s=h+1;ell=len(edges)
    family=[0]+members;center=1<<h;star=[Q(bool(a&center)) for a in members]
    check(all(a^(1<<i) in family for a in family for i in range(h+1) if a>>i&1),'closure')
    check(all(sum(r)==0 for r in c) and not any(image(c,star)),'centered kernels')
    check(all(c[i][j]==(h if i==j else -1) for i,a in enumerate(members)
              for j,b in enumerate(members) if a&b),'all support entries')
    check(psd_rank(c)==m-2,'centered PSD rank')
    u=[[Q(n*(i==j)-1)-c[i][j] for j in range(m)] for i in range(m)]
    check(psd_rank([[u[i][j]-Q(2*(i==j))+Q(1,m) for j in range(m)]
                    for i in range(m)])==m-1,'stronger centered upper buffer')
    colors=[]
    for a in members:
        points=[i for i in range(h+1) if a>>i&1]
        colors.append((2*points[0] if len(points)==1 else sum(points))%s)
    check(all(colors[i]!=colors[j] for i,a in enumerate(members)
              for j,b in enumerate(members) if i!=j and a&b),'proper transversal coloring')
    counts=[colors.count(i) for i in range(s)];qmax=max(counts);beta=s*qmax-n
    check(min(counts)>=1 and beta>=1 and n%s not in (0,1),'partition arithmetic')
    part=[[Q(s*(colors[i]==colors[j])-1) for j in range(m)] for i in range(m)]
    check(psd_rank(part)==s-1 and not any(image(part,star)),'partition PSD/kernel')
    maximum_mass=sum(q for q in counts if q==qmax)
    mu=Q(beta*s*(m-maximum_mass),m*(beta+1)*(beta+s))
    check(0<mu<1,'strict endpoint buffer')
    results={}
    for name,eps in [('published',Q(1,2*(beta+1))),('endpoint',Q(1,beta+1))]:
        mix=[[(1-eps)*c[i][j]+eps*part[i][j] for j in range(m)] for i in range(m)]
        check(psd_rank(mix)==m-1 and not any(image(mix,star)),'repaired lower rank')
        U=[[Q(n*(i==j)-1)-mix[i][j] for j in range(m)] for i in range(m)]
        gap=1-eps*(beta+1)*(1-mu)
        check(psd_rank([[U[i][j]-gap*(i==j) for j in range(m)] for i in range(m)])>=0,
              'proved repaired upper buffer')
        L,M=lift(mix,s)
        check(all(sum(r)==1 for r in M),'M row sums')
        check(all(M[i][j]==0 for i,a in enumerate(family) for j,b in enumerate(family) if a&b),'M support')
        least=min(M[i][j] for i in range(n) for j in range(i+1,n))
        check((least<0)==(h>2*d),'exact sign frontier')
        check(min(L[0][1:])==1-eps*(beta+1),'empty-row maximum-color formula')
        results[name]={'epsilon':str(eps),'upper_buffer':str(gap),'matrix_sha256':digest(M),
                       'minimum_offdiagonal':str(least),'L_rank':n-1}
    components,b=component_count(h,edges)
    check(span_rank(list(map(list,zip(*B))))==h-b,'incidence rank / component count')
    module_result=None
    if modules:
        index={a:i for i,a in enumerate(members)}
        def embed(kind,values):
            v=[Q(0)]*m
            masks=([center|(1<<i) for i in range(h)] if kind=='X' else
                   [1<<i for i in range(h)] if kind=='C' else
                   [(1<<i)|(1<<j) for i,j in edges])
            for a,x in zip(masks,values):v[index[a]]=x
            return v
        kernel=nullspace(B);basis=[embed('E',v) for v in kernel]
        check(len(kernel)==ell-h+b,'edge-kernel dimension')
        for v in basis:check(image(c,v)==[(h+2+z)*x for x in v],'edge-kernel image')
        imgs=[]
        for i in range(h-1):
            y=[Q((j==i)-(j==h-1)) for j in range(h)]
            basis.extend((embed('X',y),embed('C',y)))
            ey=[y[a]+y[b] for a,b in edges]
            Ay=[sum(y[j] for j in range(h) if (min(v,j),max(v,j)) in edges)
                for v in range(h)]
            by=[-a+Q(2,d)*b for a,b in zip(y,Ay)]
            cy=[h*a-Q(h-d,d)*b for a,b in zip(y,Ay)]
            gy=[d*a+b for a,b in zip(y,Ay)]
            w=Q(2*(d-1),d*(h-2))
            def addvectors(*vectors):return [sum(row) for row in zip(*vectors)]
            check(image(c,embed('X',y))==addvectors(
                  embed('X',[(h+1)*v for v in y]),embed('C',by),
                  embed('E',[-(1+w)*v for v in ey])),'spoke module image')
            check(image(c,embed('C',y))==addvectors(embed('X',by),embed('C',cy),
                  embed('E',[-v for v in ey])),'singleton module image')
            ty=[(h+2+z)*a-(1+z)*b for a,b in zip(y,gy)]
            check(image(c,embed('E',ey))==addvectors(
                  embed('X',[-(1+w)*v for v in gy]),embed('C',[-v for v in gy]),
                  embed('E',[ty[a]+ty[b] for a,b in edges])),'edge-incidence module image')
            if span_rank(imgs+[ey])>len(imgs):imgs.append(ey)
        basis += [embed('E',y) for y in imgs]
        a=[Q(mask==center) for mask in members]
        constants=[a,embed('C',[1]*h),embed('X',[1]*h),embed('E',[1]*ell)]
        F=[[1,0],[0,1],[-1,0],[0,-1]];K=[[h,-h],[-h,h*d]]
        want=product(product(F,K),list(map(list,zip(*F))))
        got=[[sum(x*y for x,y in zip(v,image(c,w))) for w in constants] for v in constants]
        check(got==want and sum(Q(got[i][i],v) for i,v in enumerate((1,h,h,ell)))==h+d+3,
              'constant Gram / normalized trace')
        basis+=constants
        check(len(basis)==m and span_rank(basis)==m,'complete rational spanning decomposition')
        module_result={'components':components,'bipartite_components':b,
                       'nonconstant_d_modes':components-1,'edge_kernel_dimension':len(kernel),
                       'nonconstant_edge_image_dimension':len(imgs),'basis_rank':m}
    return {'h':h,'d':d,'N':n,'s':s,'partition_sizes':counts,'beta':beta,
            'endpoint_buffer_mu':str(mu),'centered_core_rank':m-2,'module_check':module_result,
            **results}

def cycle(h):return sorted({tuple(sorted((i,(i+1)%h))) for i in range(h)})
def circulant(h,steps):return sorted({tuple(sorted((i,(i+r)%h))) for i in range(h) for r in steps})
def bipartite(t):return [(i,t+j) for i in range(t) for j in range(t)]
def union(parts):
    edges=[];offset=0
    for h,pairs in parts:
        edges += [(i+offset,j+offset) for i,j in pairs];offset+=h
    return offset,edges

def cases():
    out=[('C'+str(h),h,cycle(h)) for h in (5,6,7,10,12)]
    out += [('Mobius8',8,circulant(8,(1,4))),('Mobius12',12,circulant(12,(1,6))),
            ('middle-h9-d4',9,circulant(9,(1,2)))]
    for name,parts in [('two-C3',[(3,cycle(3))]*2),('two-C4',[(4,cycle(4))]*2),
                       ('three-C4',[(4,cycle(4))]*3),('C3-and-C4',[(3,cycle(3)),(4,cycle(4))]),
                       ('two-K3,3',[(6,bipartite(3))]*2)]:
        h,edges=union(parts);out.append((name,h,edges))
    out += [('dense-K2,2',4,bipartite(2)),('dense-K3,3',6,bipartite(3)),
            ('dense-K7-minus-C7',7,[e for e in it.combinations(range(7),2) if e not in cycle(7)])]
    return out

def run(compare=None):
    examples=[]
    for name,h,edges in cases():examples.append({'name':name,**audit(h,edges,True)})
    if compare:
        old=json.loads(compare.read_text())['cases'];check(len(old)==len(examples),'author case coverage')
        for a,b in zip(examples,old):
            check(a['name']==b['name'] and a['partition_sizes']==b['partition_sizes'] and
                  a['published']['matrix_sha256']==b['matrix_sha256'],'author all-entry bridge')
    census={};digests={}
    for h in range(4,7):
        pairs=list(it.combinations(range(h),2));records=[]
        for mask in range(1<<len(pairs)):
            edges=[e for i,e in enumerate(pairs) if mask>>i&1]
            degrees=[sum(v in e for e in edges) for v in range(h)]
            if not 2<=degrees[0]<=h-2 or degrees!=[degrees[0]]*h:continue
            r=audit(h,edges)
            records.append([mask,r['d'],r['published']['matrix_sha256'],r['endpoint']['matrix_sha256']])
        census[str(h)]=len(records)
        digests[str(h)]=hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest()
    check(census=={'4':3,'5':12,'6':155},'complete labelled graph census')
    controls=0
    for h,edges in [(True,[]),(3,cycle(3)),(4,[(0,1)]),(4,[(0,1),(0,1)]),
                   (4,[(0,0)]),(4,[(0,4)]),(4,list(it.combinations(range(4),2)))]:
        try:centered(h,edges)
        except ValueError:controls+=1
        else:raise ValueError('malformed graph accepted')
    check(controls==7,'input rejection controls')
    psd_controls=0
    for vals in it.product((-1,0,1),repeat=6):
        a,b,c,d,e,f=vals;mat=[[a,b,c],[b,d,e],[c,e,f]]
        want=(a>=0 and d>=0 and f>=0 and a*d-b*b>=0 and a*f-c*c>=0 and d*f-e*e>=0
              and a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b>=0)
        try:psd_rank(mat)
        except ValueError:got=False
        else:got=True
        check(got==want,'principal minor control');psd_controls+=1
    return {'status':'COMPLETE','agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'examples':examples,'complete_labelled_graph_census':census,'census_matrix_digests':digests,
            'malformed_graph_rejections':controls,'principal_minor_controls':psd_controls}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--compare-author',type=Path)
    p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);args=p.parse_args()
    start=time.monotonic();r=run(args.compare_author)
    payload=json.dumps(r,sort_keys=True,separators=(',',':'))+'\n'
    if args.check:check(r==json.loads(args.check.read_text()),'expected result mismatch')
    if args.output:args.output.write_text(payload)
    print(json.dumps({'status':'COMPLETE','sha256':hashlib.sha256(payload.encode()).hexdigest(),
                     'examples':len(r['examples']),'census':r['complete_labelled_graph_census'],
                     'seconds':time.monotonic()-start,'rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
