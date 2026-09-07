#!/usr/bin/env python3
"""Deterministic positive witness transport; its output is checked separately."""
import json
from collections import deque
from pathlib import Path
B=Path(__file__).resolve().parent

def generate(source,g,rotations,existing=None):
 n=721;terms=[0,1];edges=g['half_edges'];adj=[[]for _ in range(n)]
 for u,v in edges:adj[u].append(v);adj[v].append(u)
 inverses=[[p.index(v)for v in range(n)]for p in rotations]
 seen={};queue=deque();steps=[];batches=[]
 if existing is not None:
  batches=existing.get('seed_batches',[])[:]
  for row in existing['steps']:
   v=row['deleted'];kind=row['kind']
   if kind=='seed':w=row['word']
   elif kind=='rotation':w=''.join(seen[row['parent']][inverses[row['power']][u]]for u in range(n))
   else:
    ww=list(seen[row['parent']])
    for u,c in row['changes']:ww[u]=c
    w=''.join(ww)
   seen[v]=w;steps.append(row)
 before_seeds=sum(row['kind']=='seed'for row in steps)
 def check(v,w):
  if v in terms or len(w)!=n or any(c not in ('-'if u==v else'0123')for u,c in enumerate(w))or w[0]==w[1]or any(w[u]==w[z]for u,z in edges if v not in(u,z)):raise ValueError('invalid positive word')
 def insert(v,w,parent=None):
  if v in seen:return
  check(v,w)
  if parent is None:row={'kind':'seed','deleted':v,'word':w}
  else:row={'kind':'patch','deleted':v,'parent':parent,'changes':[[i,c]for i,c in enumerate(w)if c!=seen[parent][i]]}
  seen[v]=w;queue.append(v);steps.append(row)
  for k,p in enumerate(rotations[1:],1):
   vv=p[v]
   if vv in seen or vv in terms:continue
   ww=''.join(w[inverses[k][x]]for x in range(n))
   if ww[0]==ww[1]:continue
   check(vv,ww);seen[vv]=ww;queue.append(vv);steps.append({'kind':'rotation','deleted':vv,'parent':v,'power':k})
 for row in source['steps']:insert(row['deleted'],row['word'])
 def variants(v,w):
  yield w
  for c in range(4):
   for d in range(c):
    rem={u for u in range(n)if w[u]in(str(c),str(d))}
    while rem:
     root=min(rem);comp={root};stack=[root];rem.remove(root)
     while stack:
      u=stack.pop()
      for z in adj[u]:
       if z in rem:rem.remove(z);comp.add(z);stack.append(z)
     if not comp.intersection(adj[v]):continue
     ww=list(w)
     for u in comp:ww[u]=str(d)if w[u]==str(c)else str(c)
     if ww[0]!=ww[1]:yield ''.join(ww)
 while queue and len(seen)+2<255:
  v=queue.popleft();w=seen[v]
  for variant in variants(v,w):
   for c in '0123':
    vs=[u for u in adj[v]if variant[u]==c]
    if len(vs)==1 and vs[0]not in terms:
     u=vs[0];ww=list(variant);ww[v]=c;ww[u]='-';insert(u,''.join(ww),v)
   if len(seen)+2>=255:break
 batches.append(sum(row['kind']=='seed'for row in steps)-before_seeds)
 return {'version':'heule-t721-spindle-cover-v1','target':508,'terminals':terms,'baseline':source['baseline'],'steps':steps,'seed_batches':batches}
