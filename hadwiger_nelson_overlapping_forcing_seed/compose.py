import sys,json,time,math
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'hadwiger_nelson_small_triangle_forcer375'))
import geometry as g
import radicals as r
w=Path(__file__).resolve().parent/'out';w.mkdir(exist_ok=True)

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def affine(f):
 def row(p):
  x,y=p
  if any(x[i] for i in (0,3,4,5,6,7)) or any(y[i] for i in (1,2,4,5,6,7)):raise ValueError('Unexpected field')
  return x[1],x[2],y[0],y[3]
 offset=row(r.apply(f,r.point((0,0,0,0))))
 cols=[sub(row(r.apply(f,r.point([int(i==j) for j in range(4)]))),offset) for i in range(4)]
 return offset,cols

def transform(am,p):
 o,cs=am
 return tuple(o[j]+sum(cs[i][j]*p[i] for i in range(4)) for j in range(4))

def pair_frame(src,dst,length,reflect=False):return affine(r.frame(*map(r.point,src),*map(r.point,dst),length,reflect))

def attach(host,child,es,frames):
 pts=list(host);index={p:i for i,p in enumerate(pts)};edges=set(tuple(e) for e in g.edges(pts));maps=[]
 for k,f in enumerate(frames):
  ids=[]
  for p in child:
   q=transform(f,p)
   if q not in index:index[q]=len(pts);pts.append(q)
   ids.append(index[q])
  edges.update(tuple(sorted((ids[i],ids[j]))) for i,j in es);maps.append(ids)
 return pts,sorted(edges),maps

def save(name,pts,es,maps):
 den=math.lcm(*(F(x).denominator for p in pts for x in p))
 x={'denominator':den,'points':[[int(v*den) for v in p] for p in pts],'edges':es,'attachment_maps':maps}
 (w/(name+'.json')).write_text(json.dumps(x,separators=(',',':'))+'\n')
 print(name,len(pts),len(es),'denominator',den,flush=True)

if __name__=='__main__':
 t=time.monotonic();host=list(map(tuple,g.read('g49.json')));child,es=g.graph()
 tri=[t for t in combinations(range(49),3) if all(g.squared(host[i],host[j])==(432,0) for i,j in combinations(t,2))]
 fs=[]
 for a,b,c in tri:
  f=pair_frame(child[:2],[host[a],host[b]],432)
  if transform(f,child[2])!=host[c]:f=pair_frame(child[:2],[host[a],host[b]],432,True)
  if transform(f,child[2])!=host[c]:raise ValueError('Bad triangle frame')
  fs.append(f)
 pts,ed,maps=attach(host,child,es,fs);save('inequality_union',pts,ed,maps)
 print('seconds',time.monotonic()-t,flush=True)
