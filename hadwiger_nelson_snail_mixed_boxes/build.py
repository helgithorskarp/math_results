#!/usr/bin/env python3
"""Optional certificate producer; requires python-sat 1.9.dev15."""
from __future__ import annotations
import argparse,base64,hashlib,json,time
from pathlib import Path
from pysat.solvers import Cadical195
import geometry as G

HERE=Path(__file__).parent


def pack(word):
    data=bytearray((len(word)+3)//4)
    for i,c in enumerate(word):data[i//4]|=c<<(2*(i%4))
    return base64.b64encode(data).decode()


def colouring(n,edges):
    k=4;clauses=[[k*i+c+1 for c in range(k)] for i in range(n)]
    clauses += [[-(k*i+c+1),-(k*j+c+1)] for i,j in edges for c in range(k)]
    adj=[set() for _ in range(n)]
    for i,j in edges:adj[i].add(j);adj[j].add(i)
    tri=next(((i,j,z) for i,j in edges for z in adj[i]&adj[j]),None)
    if tri:clauses += [[k*v+c+1] for v,c in zip(tri,range(3))]
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():return None
        model=set(solver.get_model())
    return [next(c for c in range(k) if k*i+c+1 in model) for i in range(n)]


def maximal_box(hp,up,order,short):
    last=None
    for long in range(2,31):
        transforms=G.box(hp,up,order,long,short)
        points={x for f in transforms for x in G.cloud(f)}
        if len(points)>508:break
        if last is not None and len(transforms)==len(last[1]):
            last=(long,transforms);break
        last=(long,transforms)
    if last is None:raise ValueError('no target-sized box')
    return last


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--limit',type=int,default=4400);a=p.parse_args()
    high=G.high_generators();aug=G.augmentation_generators();rows=[];start=time.monotonic()
    hp=[G.powers(t,31) for _,_,t in high];up=[G.powers(t,7) for t in aug]
    stop=False
    for hr,H in enumerate(hp):
      for ai,U in enumerate(up):
       for order in (0,1):
        for short in range(2,7):
         long,transforms=maximal_box(H,U,order,short)
         points,edges=G.residue_graph(transforms);word=colouring(len(points),edges)
         if word is None:raise RuntimeError(('candidate residue obstruction',hr,ai,order,long,short))
         rows.append([hr,ai,order,long,short,len(transforms),len(points),len(edges),pack(word)])
         if len(rows)%250==0:print(json.dumps({'rows':len(rows),'elapsed_seconds':time.monotonic()-start}),flush=True)
         if len(rows)>=a.limit:stop=True;break
        if stop:break
       if stop:break
      if stop:break
    out={'version':1,'family':'Snail mixed congruence boxes',
         'source_seed_sha256':hashlib.sha256((HERE/'seed.json').read_bytes()).hexdigest(),
         'prime':G.PRIME,'parameters':{'high_generators':20,'augmentation_generators':22,
         'orders':2,'short_min':2,'short_max':6,'long_min':2,'long_max':30,
         'physical_vertex_cap':508},'high_source_indices':[i for _,i,_ in high],
         'high_overlaps':[o for o,_,_ in high],'rows':rows}
    a.output.write_text(json.dumps(out,separators=(',',':'))+'\n')
    print(json.dumps({'complete':len(rows)==4400,'rows':len(rows),
                      'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest()},indent=2))


if __name__=='__main__':main()
