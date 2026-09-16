"""Frozen exact 17-word assembly; no numerical coordinates or search."""
from pathlib import Path
import hashlib, importlib.util, json
HERE=Path(__file__).resolve().parent

def load(name,rel):
 p=HERE.parent/rel
 expected=json.loads((HERE/'SOURCE_PINS.json').read_text())[rel]
 if hashlib.sha256(p.read_bytes()).hexdigest()!=expected: raise ValueError('source pin '+rel)
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
F=load('tower16','hadwiger_nelson_snail_congruence_cluster_gate/verify.py')
def inverse(f):
 t,u,k=f
 v=F.bar(u) if not k else u
 return (F.scale(F.mul(v,F.bar(t) if k else t),-1),v,k)
def motion(points,r):
 i,j,k,l,flip=r
 x=F.sub(points[j],points[i]);y=F.sub(points[l],points[k])
 F.need(F.norm(x)==F.norm(y) and x!=F.ZERO,'congruent nonzero anchor pair')
 u=F.mul(y,F.inv(F.bar(x) if flip else x))
 t=F.sub(points[k],F.mul(u,F.bar(points[i]) if flip else points[i]));f=t,u,flip
 F.need(F.norm(u)==F.ONE,'unit multiplier')
 F.need(F.apply(f,points[i])==points[k] and F.apply(f,points[j])==points[l],'anchor images')
 F.need(F.compose(f,inverse(f))==(F.ZERO,F.ONE,0),'inverse composition')
 return f

def reconstruct():
 c=json.loads((HERE/'CONTRACT.json').read_text());rows=json.loads((HERE/'seed.json').read_text())['moser_rows']
 s=F.seed(rows);gs=[motion(s,r) for r in c['generator_anchors']];fs=[]
 for word in c['words']:
  f=F.ZERO,F.ONE,0
  for a in word:f=F.compose(f,gs[a-1] if a>0 else inverse(gs[-a-1]))
  fs.append(f)
 F.need(len(fs)==17 and len(set(fs))==17,'17 distinct physical motions')
 formal=[[F.apply(f,x) for x in s] for f in fs];points=sorted(set(x for group in formal for x in group));ids={x:i for i,x in enumerate(points)}
 address=[[ids[x] for x in group] for group in formal]
 F.need(len(points)<=508,'physical cap')
 edges,false=F.graph(points)
 return s,gs,fs,points,address,edges,false

def geometry_hash(points):return hashlib.sha256(('\n'.join(','.join(str(x) for x in p) for p in points)+'\n').encode()).hexdigest()
def edge_hash(edges):return hashlib.sha256((''.join(f'{a} {b}\n' for a,b in edges)).encode()).hexdigest()
