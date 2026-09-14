#!/usr/bin/env python3
"""Produce the exact star-closure certificate for the 39-point kernel."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse, hashlib, json, time

from pysat.solvers import Cadical195


# q=(a,b) means a+b*sqrt(3); z=(x,y) is x+i*y.
def qa(x,y): return x[0]+y[0],x[1]+y[1]
def qn(x): return -x[0],-x[1]
def qm(x,y): return x[0]*y[0]+3*x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def ca(z,w): return qa(z[0],w[0]),qa(z[1],w[1])
def cn(z): return qn(z[0]),qn(z[1])
def cs(z,w): return ca(z,cn(w))
def cm(z,w): return qa(qm(z[0],w[0]),qn(qm(z[1],w[1]))),qa(qm(z[0],w[1]),qm(z[1],w[0]))
def cj(z): return z[0],qn(z[1])
def norm(z,w):
    d=cs(z,w);return qa(qm(d[0],d[0]),qm(d[1],d[1]))
Q0=(F(0),F(0));Q1=(F(1),F(0));ZERO=(Q0,Q0);ONE=(Q1,Q0);II=(Q0,Q1)
OMEGA=((F(1,2),F(0)),(F(0),F(1,2)));ROOTS=[ONE]
for _ in range(5): ROOTS.append(cm(ROOTS[-1],OMEGA))


def flat(z): return tuple(x for axis in z for x in axis)
def enc(z): return [[[x.numerator,x.denominator] for x in axis] for axis in z]
def raw(x): return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def digest(x): return hashlib.sha256(raw(x)).hexdigest()


def base_graph():
    w5=ROOTS[5];us=(OMEGA,ONE,OMEGA,ONE);vs=(II,II,cm(II,w5),cm(II,w5))
    ds=[cs(u,v) for u,v in zip(us,vs)]
    centres=(ZERO,cs(ds[0],ds[2]),ds[0],ds[1])
    cross=((0,0),(0,1),(1,0),(1,1));intersections=[]
    for (i,j),u in zip(cross,us):
        x=ca(centres[i],u);intersections.append((x,cs(ca(centres[i],centres[2+j]),x)))
    directions=[set(),set()]
    for g in range(2):
        seeds=[cs(centres[2*g+1],centres[2*g])]
        for (i,j),row in zip(cross,intersections):
            seeds.extend(cs(p,centres[i if g==0 else 2+j]) for p in row)
        for seed in seeds: directions[g].update(cm(seed,u) for u in ROOTS)
    points=set()
    for h,c in enumerate(centres): points.update(ca(c,u) for u in directions[h//2])
    vertices=sorted(points,key=flat)
    edges=[e for e in combinations(range(len(vertices)),2) if norm(vertices[e[0]],vertices[e[1]])==Q1]
    return centres,vertices,edges


def move(z,source0,target0,alpha,reflected):
    d=cs(z,source0)
    return ca(target0,cm(alpha,cj(d) if reflected else d))


def closure(centres,base,edges):
    host=set(base);support_hashes=set();raw_attachments=0
    for s0,s1 in ((0,1),(2,3)):
        source=cs(centres[s1],centres[s0])
        for ea,eb in edges:
            for reverse in (False,True):
                ta,tb=(eb,ea) if reverse else (ea,eb);target0=base[ta];target=cs(base[tb],target0)
                for reflected in (False,True):
                    raw_attachments+=1
                    alpha=cm(target,source if reflected else cj(source))
                    moved={move(z,centres[s0],target0,alpha,reflected) for z in base}
                    host.update(moved)
                    support_hashes.add(digest([enc(z) for z in sorted(set(base)|moved,key=flat)]))
    host=sorted(host,key=flat)
    host_edges=[e for e in combinations(range(len(host)),2) if norm(host[e[0]],host[e[1]])==Q1]
    return raw_attachments,support_hashes,host,host_edges


PATTERNS=((0,1,0,1),(0,1,0,2),(0,1,2,0),(0,1,1,0),(0,1,1,2),(0,1,2,1))
def colouring(vertices,edges,pins):
    k=4;var=lambda v,c:k*v+c+1;clauses=[]
    for v in range(vertices):
        clauses.append([var(v,c) for c in range(k)])
        clauses.extend([-var(v,a),-var(v,b)] for a,b in combinations(range(k),2))
    for a,b in edges: clauses.extend([-var(a,c),-var(b,c)] for c in range(k))
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve(assumptions=[var(v,c) for v,c in pins.items()]): return None
        model={x for x in solver.get_model() if x>0}
    return ''.join(str(next(c for c in range(k) if var(v,c) in model)) for v in range(vertices))


def mod3(x): return (x.numerator*pow(x.denominator,-1,3))%3


def build():
    centres,base,base_edges=base_graph();raw_count,support_hashes,host,host_edges=closure(centres,base,base_edges)
    ci=[host.index(z) for z in centres];pi=host.index(cn(II))
    words={''.join(map(str,p)):colouring(len(host),host_edges,dict(zip(ci,p))) for p in PATTERNS}
    if any(v is None for v in words.values()): raise ValueError('missing terminal colouring')
    linear=''.join(str((mod3(z[0][0])+mod3(z[1][0]))%3) for z in host)
    residues=sorted({tuple((mod3(x)-mod3(y))%3 for x,y in zip(flat(host[a]),flat(host[b]))) for a,b in host_edges})
    return {
        'schema':1,'field':'Q(sqrt(3),i)','base_vertices':len(base),'base_edges':len(base_edges),
        'base_point_sha256':digest([enc(z) for z in base]),'base_edge_sha256':digest(base_edges),
        'raw_attachments':raw_count,'canonical_two_copy_supports':len(support_hashes),
        'support_hash_set_sha256':digest(sorted(support_hashes)),'host_vertices':len(host),'host_edges':len(host_edges),
        'host_point_sha256':digest([enc(z) for z in host]),'host_edge_sha256':digest(host_edges),
        'centre_indices':ci,'common_neighbour_index':pi,'allowed_terminal_patterns':[list(p) for p in PATTERNS],
        'terminal_colourings':words,'three_colouring_rule':'a+c mod 3 for z=(a+b sqrt(3))+i(c+d sqrt(3))',
        'three_colouring':linear,'unit_edge_residues_mod3':[list(x) for x in residues],
        'star_interface_preserved':True,'record_improved':False,
    }


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    if args.out.exists(): raise SystemExit(f'refusing to overwrite {args.out}')
    start=time.monotonic();data=build();args.out.write_bytes(raw(data))
    print(json.dumps({'status':'PASS','host_vertices':data['host_vertices'],'host_edges':data['host_edges'],
      'raw_attachments':data['raw_attachments'],'canonical_supports':data['canonical_two_copy_supports'],
      'terminal_patterns':len(data['terminal_colourings']),'seconds':time.monotonic()-start,
      'certificate_sha256':hashlib.sha256(raw(data)).hexdigest()},sort_keys=True))
if __name__=='__main__': main()
