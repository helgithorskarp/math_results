#!/usr/bin/env python3
"""Generate the exact regular two-variable paired-circle obstruction."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import argparse,hashlib,json,time


# Complex coordinates over Q(sqrt(3)); q=(a,b) denotes a+b*sqrt(3).
def qa(x,y):return (x[0]+y[0],x[1]+y[1])
def qn(x):return (-x[0],-x[1])
def qm(x,y):return (x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def ca(z,w):return (qa(z[0],w[0]),qa(z[1],w[1]))
def cn(z):return (qn(z[0]),qn(z[1]))
def cs(z,w):return ca(z,cn(w))
def cm(z,w):return (qa(qm(z[0],w[0]),qn(qm(z[1],w[1]))),qa(qm(z[0],w[1]),qm(z[1],w[0])))
def norm(z):return qa(qm(z[0],z[0]),qm(z[1],z[1]))
Q0=(F(0),F(0));Q1=(F(1),F(0));ZERO=(Q0,Q0);ONE=(Q1,Q0);II=(Q0,Q1)
OMEGA=((F(1,2),F(0)),(F(0),F(1,2)));ROOTS=[ONE]
for _ in range(5):ROOTS.append(cm(ROOTS[-1],OMEGA))
if cm(ROOTS[-1],OMEGA)!=ONE:raise RuntimeError('sixth-root failure')


def flat(z):return tuple(x for axis in z for x in axis)
def enc(z):return [[[x.numerator,x.denominator] for x in axis] for axis in z]
def raw(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x):return hashlib.sha256(raw(x)).hexdigest()
def orbit(direction):
    candidates=[cm(direction,u) for u in ROOTS];rep=min(candidates,key=flat)
    return rep,next(k for k,u in enumerate(ROOTS) if cm(rep,u)==direction)


def colour(vertices,edges,k):
    adj=[set() for _ in vertices]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    values=[-1]*len(vertices);nodes=0
    def visit(left):
        nonlocal nodes
        nodes+=1
        if not left:return values.copy()
        v=max(left,key=lambda x:(len({values[y] for y in adj[x] if values[y]>=0}),len(adj[x]),-x))
        forbidden={values[y] for y in adj[v] if values[y]>=0}
        for c in range(k):
            if c not in forbidden:
                values[v]=c;answer=visit(left-{v})
                if answer is not None:return answer
        values[v]=-1;return None
    return visit(set(range(len(vertices)))),nodes


def build():
    w5=ROOTS[5];us=(OMEGA,ONE,OMEGA,ONE);vs=(II,II,cm(II,w5),cm(II,w5));ds=[cs(u,v) for u,v in zip(us,vs)]
    centres=(ZERO,cs(ds[0],ds[2]),ds[0],ds[1])
    if cs(centres[3],centres[1])!=ds[3]:raise ValueError('parallelogram')
    if norm(centres[1])!=Q1 or norm(cs(centres[3],centres[2]))!=Q1:raise ValueError('segments')
    if len({flat(x) for x in centres})!=4:raise ValueError('centres')
    cross=((0,0),(0,1),(1,0),(1,1));intersections=[];reps={};clauses=[]
    for (i,j),u,v in zip(cross,us,vs):
        if u in (v,cn(v)):raise ValueError('regularity')
        x=ca(centres[i],u);y=cs(ca(centres[i],centres[2+j]),x)
        for p in (x,y):
            if norm(cs(p,centres[i]))!=Q1 or norm(cs(p,centres[2+j]))!=Q1:raise ValueError('intersection')
        intersections.append((x,y));ru,k=orbit(u);rv,l=orbit(v);reps[flat(ru)]=ru;reps[flat(rv)]=rv;s=(1+i+j)&1
        clauses.append(((flat(ru),(s+k)&1),(flat(rv),(1+s+l)&1)))
    ordered=sorted(reps);oi={r:i for i,r in enumerate(ordered)}
    clauses=[sorted([[oi[r],value] for r,value in row]) for row in clauses]
    solutions=sum(all(any(a[v]==value for v,value in row) for row in clauses) for a in product(range(2),repeat=len(ordered)))
    S=[set(),set()]
    for g in range(2):
        seeds=[cs(centres[2*g+1],centres[2*g])]
        for (i,j),row in zip(cross,intersections):seeds.extend(cs(p,centres[i if g==0 else 2+j]) for p in row)
        for seed in seeds:S[g].update(cm(seed,u) for u in ROOTS)
    points=set()
    for h,c in enumerate(centres):points.update(ca(c,u) for u in S[h//2])
    vertices=sorted(points,key=flat);edges=[list(e) for e in combinations(range(len(vertices)),2) if norm(cs(vertices[e[0]],vertices[e[1]]))==Q1]
    colouring,_=colour(vertices,edges,3)
    if colouring is None:raise ValueError('missing three-colouring')
    p=cn(II);pi=vertices.index(p);ci=[vertices.index(c) for c in centres]
    if any([min(pi,i),max(pi,i)] not in edges for i in ci):raise ValueError('common neighbour')
    triangle=(pi,ci[0],ci[1])
    if any([min(a,b),max(a,b)] not in edges for a,b in combinations(triangle,2)):raise ValueError('triangle lower bound')
    return {'schema':1,'field':'Q(sqrt(3),i)','centres':[enc(x) for x in centres],
            'cross_squared_norms':[[[x.numerator,x.denominator] for x in norm(d)] for d in ds],
            'orbit_variables':len(ordered),'clauses':clauses,'phase_solutions':solutions,
            'common_neighbour':enc(p),'direction_sizes':list(map(len,S)),
            'patch_vertices':len(vertices),'patch_edges':len(edges),'point_sha256':digest([enc(x) for x in vertices]),
            'edge_sha256':digest(edges),'chromatic_number':3,'three_colouring':''.join(map(str,colouring)),
            'kernel_list_colourable':False,
            'full_support_four_colourable':None,'record_improved':False}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out');args=ap.parse_args();start=time.monotonic();data=build();blob=raw(data)
    if args.out:Path(args.out).write_bytes(blob)
    print(json.dumps({'status':'PASS','vertices':data['patch_vertices'],'edges':data['patch_edges'],
                      'chromatic_number':data['chromatic_number'],'phase_solutions':data['phase_solutions'],
                      'seconds':time.monotonic()-start,'certificate_sha256':hashlib.sha256(blob).hexdigest()}))


if __name__=='__main__':main()
