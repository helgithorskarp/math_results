#!/usr/bin/env python3
"""Read a small exact hat-contact certificate; no solver or upstream imports.

Author: six-heesch-3, researcher, 2026-10-01.
"""
import argparse
from collections import defaultdict, deque
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PRIME = 1009

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sub(a,b): return a[0]-b[0],a[1]-b[1]
def cross(a,b): return a[0]*b[1]-a[1]*b[0]
def linear(m,v): return m[0]*v[0]+m[1]*v[1],m[3]*v[0]+m[4]*v[1]
def point(m,v):
    x,y=linear(m,v)
    return x+m[2],y+m[5]
def quarter(v): return -v[0]-2*v[1],2*v[0]+v[1]
def handedness(m): return m[0]*m[4]-m[1]*m[3]
def digest(value):
    return sha256(json.dumps(value,separators=(',',':')).encode()).hexdigest()

def twice_area(poly):
    return sum(cross(v,poly[(j+1)%len(poly)]) for j,v in enumerate(poly))

def on_segment(p,a,b):
    return cross(sub(b,a),sub(p,a))==0 and all(min(a[k],b[k])<=p[k]<=max(a[k],b[k]) for k in (0,1))

def segment_intersection(a,b,c,d):
    ca=cross(sub(b,a),sub(c,a));da=cross(sub(b,a),sub(d,a))
    ac=cross(sub(d,c),sub(a,c));bc=cross(sub(d,c),sub(b,c))
    return (ca*da<0 and ac*bc<0) or any((on_segment(c,a,b),on_segment(d,a,b),
                                                      on_segment(a,c,d),on_segment(b,c,d)))

def triangle_overlap(a,b):
    """Separating axes for closed convex triangles, testing INTERIOR overlap."""
    for tri,other in ((a,b),(b,a)):
        for j,x in enumerate(tri):
            edge=sub(tri[(j+1)%3],x)
            if max(cross(edge,sub(y,x)) for y in other)<=0:
                return False
    return True

def in_triangle_closed(p,t):
    return all(cross(sub(t[(j+1)%3],t[j]),sub(p,t[j]))>=0 for j in range(3))

def triangulate(poly):
    require(twice_area(poly)>0,'prototype must be counterclockwise')
    ids=list(range(len(poly)))
    # Remove the one artificial collinear endpoint from the triangulation,
    # retaining it in all port and endpoint calculations.
    changed=True
    while changed:
        changed=False
        for k,i in enumerate(ids):
            a,b=poly[ids[k-1]],poly[ids[(k+1)%len(ids)]]
            if cross(sub(poly[i],a),sub(b,poly[i]))==0:
                ids.pop(k);changed=True;break
    result=[]
    while len(ids)>3:
        for k,i in enumerate(ids):
            ix=(ids[k-1],i,ids[(k+1)%len(ids)])
            t=tuple(poly[j] for j in ix)
            if twice_area(t)<=0:continue
            if any(in_triangle_closed(poly[j],t) for j in ids if j not in ix):continue
            result.append(t);ids.pop(k);break
        else:raise ValueError('ear decomposition failed')
    result.append(tuple(poly[j] for j in ids))
    require(all(twice_area(t)>0 for t in result),'degenerate triangle')
    require(sum(twice_area(t) for t in result)==twice_area(poly),'area decomposition')
    return result

def geometry(data):
    vertices=data['vertices'];copies=data['copies']
    require(len(vertices)==14 and len(copies)==25,'fixture cardinalities')
    require(all(len(v)==2 and all(type(x) is int for x in v) for v in vertices),'integer vertices')
    require(len({tuple(v) for v in vertices})==14,'duplicate prototype vertex')
    require(twice_area(vertices)==32,'reference prototype area')
    for i,a in enumerate(vertices):
        b=vertices[(i+1)%14]
        for j in range(i):
            if (i-j)%14 in (1,13):continue
            require(not segment_intersection(a,b,vertices[j],vertices[(j+1)%14]),
                    'prototype has nonincident edge intersection')
    poses=[c['pose'] for c in copies]
    require(all(len(m)==6 and all(type(x) is int for x in m) for m in poses),'integer poses')
    require(poses[0]==[1,0,0,0,1,0],'root pose')
    require(len({tuple(m) for m in poses})==25,'duplicate tile pose')
    for m in poses:
        a,b,_,d,e,_=m
        require(handedness(m) in (-1,1),'pose determinant')
        require(a*a+a*d+d*d==1 and b*b+b*e+e*e==1 and
                2*a*b+a*e+b*d+2*d*e==1,'pose Euclidean Gram equation')
    lengths=[]
    for j,v in enumerate(vertices):
        x,y=sub(vertices[(j+1)%14],v)
        lengths.append(x*x+x*y+y*y)
    require(sorted(lengths)==[1]*8+[3]*6,'unit and sqrt(3) ports')
    triangles=triangulate(vertices)
    tiled_triangles=[]
    polygons=[]
    for m in poses:
        poly=[point(m,v) for v in vertices];polygons.append(poly)
        tt=[]
        for t in triangles:
            image=[point(m,v) for v in t]
            if twice_area(image)<0:image[1],image[2]=image[2],image[1]
            tt.append(image)
        tiled_triangles.append(tt)
    for i,p in enumerate(polygons):
        for j,q in enumerate(polygons[:i]):
            if any(max(v[axis] for v in p)<=min(v[axis] for v in q) or
                   max(v[axis] for v in q)<=min(v[axis] for v in p) for axis in (0,1)):
                continue
            require(not any(triangle_overlap(a,b) for a in tiled_triangles[i]
                            for b in tiled_triangles[j]),f'tile interiors overlap: {i},{j}')
    edges=defaultdict(list)
    for n,poly in enumerate(polygons):
        for j,a in enumerate(poly):
            b=poly[(j+1)%14]
            edges[tuple(sorted((a,b)))].append((n,j,a,b))
    pairs=[];relations={};tile_adj=[set() for _ in poses]
    for key,inc in sorted(edges.items()):
        require(len(inc)<=2,'three copies share a port')
        if len(inc)!=2:continue
        a,b=sorted(inc)
        reverse=int(a[2]==b[3])
        require(reverse or a[2]==b[2],'endpoint order')
        require(handedness(poses[a[0]])==(-1)**(reverse+1)*handedness(poses[b[0]]),
                'shared-edge interior sides')
        require(lengths[a[1]]==lengths[b[1]],'matched lengths')
        pairs.append((a[0],a[1],b[0],b[1],reverse))
        rel=tuple(sorted((a[1],b[1])))+(reverse,)
        relations.setdefault(rel,len(pairs)-1)
        tile_adj[a[0]].add(b[0]);tile_adj[b[0]].add(a[0])
    visited={0};queue=deque([0])
    while queue:
        for j in tile_adj[queue.popleft()]:
            if j not in visited:visited.add(j);queue.append(j)
    require(len(visited)==25,'full-port adjacency disconnected')
    return vertices,poses,pairs,relations,len(triangles),twice_area(vertices)

def lifted_graph(relations):
    graph=[set() for _ in range(28)]
    for i,j,reverse in relations:
        for r in (0,1):
            a=2*i+r;b=2*j+(r^reverse)
            graph[a].add(b);graph[b].add(a)
    return graph

def profile_certificate(graph):
    """Discovery of compact odd closed walks; the reader checks every edge."""
    done=set();components=[]
    for root in range(28):
        if root in done:continue
        parent={root:None};color={root:0};queue=deque([root]);conflict=None
        while queue:
            a=queue.popleft()
            for b in sorted(graph[a]):
                if b not in color:
                    parent[b]=a;color[b]=1-color[a];queue.append(b)
                elif color[b]==color[a] and conflict is None:conflict=(a,b)
        require(conflict is not None,'a profile component retains freedom')
        def route(a):
            path=[a]
            while parent[a] is not None:a=parent[a];path.append(a)
            return path
        a,b=conflict;walk=list(reversed(route(a)))+route(b)
        components.append({'nodes':sorted(parent),'odd_closed_walk':walk})
        done.update(parent)
    return components

def check_profile_certificate(graph,certificate):
    covered=set()
    for component in certificate:
        nodes=set(component['nodes']);walk=component['odd_closed_walk']
        require(nodes and not (nodes & covered),'profile component partition')
        require(all(0<=i<28 for i in nodes),'profile node range')
        require(all(graph[i]<=nodes for i in nodes),'component not closed')
        visited={min(nodes)};queue=deque(visited)
        while queue:
            for j in graph[queue.popleft()]:
                if j not in visited:visited.add(j);queue.append(j)
        require(visited==nodes,'component not connected')
        require(len(walk)>=2 and walk[0]==walk[-1] and (len(walk)-1)%2==1,
                'walk must be closed and odd')
        require(all(i in nodes for i in walk),'walk leaves component')
        require(all(b in graph[a] for a,b in zip(walk,walk[1:])),'missing walk edge')
        covered.update(nodes)
    require(covered==set(range(28)),'unforced profile states')

def endpoint_matrix(vertices,poses,pairs):
    rows=[];equations=[]
    for a,i,b,j,reverse in pairs:
        for ai,bj in ((i,(j+reverse)%14),((i+1)%14,(j+1-reverse)%14)):
            require(point(poses[a],vertices[ai])==point(poses[b],vertices[bj]),'endpoint equality')
            equations.append(((a,ai),(b,bj)))
            for axis in (0,1):
                row=[0]*100
                for (n,k),sign in (((a,ai),1),((b,bj),-1)):
                    m=poses[n]
                    row[2*k]+=sign*m[3*axis];row[2*k+1]+=sign*m[3*axis+1]
                    if n:
                        at=28+3*(n-1)
                        row[at+axis]+=sign
                        row[at+2]+=sign*quarter(linear(m,vertices[k]))[axis]
                rows.append(row)
    return rows,equations

def exact_kernel(vertices,poses,equations):
    columns=[]
    for u in ((1,0),(0,1)):
        z=[c for _ in vertices for c in u]
        for m in poses[1:]:z.extend(sub(u,linear(m,u))+(0,))
        columns.append(z)
    z=[c for v in vertices for c in v]
    for m in poses[1:]:z.extend((m[2],m[5],0))
    columns.append(z)
    z=[c for v in vertices for c in quarter(v)]
    for m in poses[1:]:z.extend(quarter((m[2],m[5]))+(1-handedness(m),))
    columns.append(z)
    w=[];s=(0,0)
    for j,v in enumerate(vertices):
        w.append(s);edge=sub(vertices[(j+1)%14],v)
        if edge[0]**2+edge[0]*edge[1]+edge[1]**2==3:
            s=(s[0]+edge[0],s[1]+edge[1])
    require(s==(0,0),'long-side vectors do not close')
    adjacency=defaultdict(list)
    for (a,i),(b,j) in equations:
        d=sub(linear(poses[a],w[i]),linear(poses[b],w[j]))
        adjacency[a].append((b,d));adjacency[b].append((a,(-d[0],-d[1])))
    shifts={0:(0,0)};queue=deque([0])
    while queue:
        a=queue.popleft()
        for b,d in adjacency[a]:
            value=(shifts[a][0]+d[0],shifts[a][1]+d[1])
            if b not in shifts:shifts[b]=value;queue.append(b)
            else:require(shifts[b]==value,'edge-length family inconsistent')
    require(len(shifts)==25,'edge-length family disconnected')
    z=[c for v in w for c in v]
    for n in range(1,25):z.extend(shifts[n]+(0,))
    columns.append(z)
    return columns,w,shifts

def discover_minor(matrix):
    """Optional certificate generator; separate from determinant reading."""
    basis={};selected=[]
    for i,row in enumerate(matrix):
        v=[x%PRIME for x in row]
        for j,b in basis.items():
            c=v[j]
            if c:v=[(x-c*y)%PRIME for x,y in zip(v,b)]
        j=next((j for j,x in enumerate(v) if x),None)
        if j is None:continue
        scale=pow(v[j],-1,PRIME);basis[j]=[(scale*x)%PRIME for x in v]
        selected.append((i,j))
    return {'rows':[i for i,j in selected],'columns':[j for i,j in selected]}

def determinant(matrix):
    """Exact determinant modulo PRIME with row swaps only."""
    n=len(matrix)
    require(all(len(row)==n for row in matrix),'nonsquare minor')
    m=[[x%PRIME for x in row] for row in matrix];value=1
    for j in range(n):
        k=next((k for k in range(j,n) if m[k][j]),None)
        if k is None:return 0
        if k!=j:m[j],m[k]=m[k],m[j];value=-value
        pivot=m[j][j];value=(value*pivot)%PRIME;inv=pow(pivot,-1,PRIME)
        for k in range(j+1,n):
            c=m[k][j]*inv%PRIME
            if c:
                for l in range(j+1,n):m[k][l]=(m[k][l]-c*m[j][l])%PRIME
            m[k][j]=0
    return value%PRIME

def read_minor(matrix,cert,size):
    rows=cert['rows'];columns=cert['columns']
    require(len(rows)==size and len(set(rows))==size,'minor rows')
    require(len(columns)==size and len(set(columns))==size,'minor columns')
    require(all(type(i) is int and 0<=i<len(matrix) for i in rows),'minor row range')
    require(all(type(j) is int and 0<=j<len(matrix[0]) for j in columns),'minor column range')
    value=determinant([[matrix[i][j] for j in columns] for i in rows])
    require(value!=0 and value==cert['determinant_mod_1009'],'minor determinant mismatch')
    return value

def verify(data,cert):
    require(all(PRIME%d for d in range(2,32)),'certificate modulus is not prime')
    v,m,pairs,relations,triangles,area2=geometry(data)
    graph=lifted_graph(relations);check_profile_certificate(graph,cert['profile_components'])
    M,equations=endpoint_matrix(v,m,pairs);K,w,shifts=exact_kernel(v,m,equations)
    require(len(M)==544 and len(M[0])==100,'Jacobian dimensions')
    require(all(sum(a*b for a,b in zip(row,k))==0 for row in M for k in K),'exact kernel failed')
    require(digest(M)==cert['matrix_sha256'],'Jacobian hash')
    lower=read_minor(M,cert['jacobian_minor'],95)
    kernel_det=read_minor(K,cert['kernel_minor'],5)
    require(len(relations)==31 and len(pairs)==136,'contact counts')
    return {'copies':25,'prototype_vertices':14,'prototype_area':'8*sqrt(3)',
            'prototype_twice_axial_area':area2,'prototype_triangles':triangles,
            'whole_shared_ports':len(pairs),'oriented_port_relations':len(relations),
            'profile_components':len(cert['profile_components']),'forced_flat_port_functions':14,
            'jacobian_rows':len(M),'jacobian_columns':len(M[0]),'exact_rank':95,
            'exact_kernel_dimension':5,'prime':PRIME,'jacobian_minor_determinant':lower,
            'kernel_minor_determinant':kernel_det,'matrix_sha256':digest(M),
            'kernel_sha256':digest(K),'long_edge_derivative':[list(p) for p in w],
            'local_family':'similarities of Tile(1,sqrt(3)*(1+lambda))'}

def make_certificate(data):
    v,m,pairs,relations,_,_=geometry(data);M,equations=endpoint_matrix(v,m,pairs)
    K,_,_=exact_kernel(v,m,equations)
    a=discover_minor(M);b=discover_minor(K)
    for c,matrix in ((a,M),(b,K)):
        c['determinant_mod_1009']=determinant([[matrix[i][j] for j in c['columns']] for i in c['rows']])
    return {'matrix_sha256':digest(M),'jacobian_minor':a,'kernel_minor':b,
            'profile_components':profile_certificate(lifted_graph(relations))}

def controls(data,cert):
    bad=[]
    c=deepcopy(data);c['copies'][1]['pose'][0]=2;bad.append((c,cert))
    c=deepcopy(data);c['copies'][1]['pose']=c['copies'][0]['pose'][:];bad.append((c,cert))
    c=deepcopy(data);c['copies'][1]['pose'][2]+=1;bad.append((c,cert))
    c=deepcopy(cert);c['jacobian_minor']['determinant_mod_1009']=0;bad.append((data,c))
    c=deepcopy(cert);c['kernel_minor']['columns'][0]=c['kernel_minor']['columns'][1];bad.append((data,c))
    c=deepcopy(cert);c['profile_components'][0]['odd_closed_walk']=[0,0];bad.append((data,c))
    c=deepcopy(cert);c['profile_components']=c['profile_components'][:-1];bad.append((data,c))
    c=deepcopy(cert);c['matrix_sha256']='0'*64;bad.append((data,c))
    for i,(d,c) in enumerate(bad):
        try:verify(d,c)
        except ValueError:pass
        else:raise ValueError(f'malformed control {i} accepted')
    return len(bad)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--make-certificate',action='store_true')
    parser.add_argument('--expected',action='store_true');args=parser.parse_args()
    data=json.loads((HERE/'input.json').read_text())
    if args.make_certificate:
        cert=make_certificate(data)
        (HERE/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    else:cert=json.loads((HERE/'certificate.json').read_text())
    result=verify(data,cert);result['rejected_controls']=controls(data,cert)
    if args.expected:
        require(result==json.loads((HERE/'expected.json').read_text()),'expected output mismatch')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
