"""Exact safe-parser audit of VND's supplied plane case10 coordinates and edges."""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from math import isqrt,lcm
from collections import Counter
import ast,re,json,hashlib,time
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve()
R=[1,2,3,6,5,10,15,30]
def require(x,msg):
 if not x:raise ValueError(msg)
def add(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,Q(0))+v
 return {k:v for k,v in c.items() if v}
def neg(a):return {k:-v for k,v in a.items()}
def mul(a,b):
 c={}
 for i,x in a.items():
  for j,y in b.items():c[i^j]=c.get(i^j,Q(0))+x*y*R[i&j]
 return {k:v for k,v in c.items() if v}
def rational(a):
 require(not set(a)-{0},'nonrational radicand');return a.get(0,Q(0))
def square_root(q):
 require(q>0,'nonpositive square root');n,d=q.numerator,q.denominator
 for k,r in enumerate(R):
  x=Q(n,d*r);a,b=isqrt(x.numerator),isqrt(x.denominator)
  if a*a==x.numerator and b*b==x.denominator:return {k:Q(a,b)}
 raise ValueError('outside specified field')
@lru_cache(maxsize=None)
def parse_scalar(s):
 def val(n):
  if isinstance(n,ast.Constant):
   require(type(n.value)is int,'integer literal');return {} if n.value==0 else {0:Q(n.value)}
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)):
   a=val(n.operand);return neg(a) if isinstance(n.op,ast.USub) else a
  if isinstance(n,ast.BinOp):
   a,b=val(n.left),val(n.right)
   if isinstance(n.op,ast.Add):return add(a,b)
   if isinstance(n.op,ast.Sub):return add(a,neg(b))
   if isinstance(n.op,ast.Mult):return mul(a,b)
   if isinstance(n.op,ast.Div):
    require(len(b)==1,'denominator must be a nonzero monomial');k,x=next(iter(b.items()));return mul(a,{k:1/(x*R[k])})
  if isinstance(n,ast.Call):
   require(isinstance(n.func,ast.Name) and n.func.id=='sqrt' and len(n.args)==1 and not n.keywords,'allowed square root');return square_root(rational(val(n.args[0])))
  raise ValueError('unapproved source syntax '+ast.dump(n))
 result=val(ast.parse(s,mode='eval').body)
 return tuple(result.get(i,Q(0)) for i in range(8))
def coordinates():
 raw=(P/'source_graph.vtx').read_text();records=re.findall(r'\{([^{}]*)\}',raw,flags=re.S)
 require(not re.sub(r'\{[^{}]*\}','',raw,flags=re.S).strip(),'extra source syntax')
 rows=[];den=1
 for s in records:
  parts=s.split(',');require(len(parts)==2,'coordinate pair')
  row=[]
  for part in parts:
   part=' '.join(part.replace('Sqrt[','sqrt(').replace(']',')').split());q=parse_scalar(part);row.extend(q)
   for x in q:den=lcm(den,x.denominator)
  rows.append(row)
 return [[int(x*den) for x in q] for q in rows],den
@lru_cache(maxsize=None)
def norm(d):
 out=[0]*8
 for off in (0,8):
  a=d[off:off+8]
  for i,x in enumerate(a):
   if not x:continue
   out[0]+=x*x*R[i]
   for j in range(i+1,8):
    if a[j]:out[i^j]+=2*x*a[j]*R[i&j]
 return tuple(out)
def main():
 start=time.monotonic();points,den=coordinates();require(len(points)==len(set(map(tuple,points)))==64513,'distinct points')
 print('parsed',len(points),'denominator',den,'seconds',time.monotonic()-start,flush=True)
 lines=(P/'source_graph.dimacs').read_text().splitlines();require(lines[0].split()==['p','edge','64513','542472'],'graph header')
 edges=[]
 for line in lines[1:]:
  a=line.split();require(len(a)==3 and a[0]=='e','edge format');u,v=sorted([int(a[1])-1,int(a[2])-1]);require(0<=u<v<64513,'edge labels');edges.append((u,v))
 require(len(edges)==len(set(edges))==542472,'edge count');edges.sort()
 want=(den*den,)+(0,)*7
 for k,(u,v) in enumerate(edges):
  d=tuple(x-y for x,y in zip(points[u],points[v]));d=min(d,tuple(-x for x in d));require(norm(d)==want,'nonunit edge '+str((u,v)))
  if k and k%100000==0:print('unit_edges_checked',k,flush=True)
 cross=[(u,v) for u,v in edges if 0<u<=32256<v]
 require(len(cross)==120,'cross edge census');require(points[0]==[0]*16,'origin')
 # The second half is a rotation of the nonorigin first half; sign and ordering need not agree.
 rho_x={0:Q(-7,8)};rho_y={6:Q(1,8)}
 def rot(q):
  x={k:Q(q[k],den) for k in range(8) if q[k]};y={k:Q(q[k+8],den) for k in range(8) if q[k+8]}
  X=add(mul(rho_x,x),neg(mul(rho_y,y)));Y=add(mul(rho_y,x),mul(rho_x,y))
  return tuple(X.get(k,Q(0))*den for k in range(8))+tuple(Y.get(k,Q(0))*den for k in range(8))
 require({rot(q) for q in points[1:32257]}==set(map(tuple,points[32257:])),'rotated half')
 out={'verified':True,'source_vertices':64513,'source_declared_edges':542472,'all_declared_edges_exactly_unit':True,'coordinate_denominator':den,'basis_radicands':R,'cross_edges':len(cross),'distinct_unit_displacement_classes':norm.cache_info().currsize,'second_half_is_rho_first_half':True,'rho':'-7/8+i*sqrt(15)/8','points_sha256':hashlib.sha256(json.dumps(points,separators=(',',':')).encode()).hexdigest(),'edges_sha256':hashlib.sha256(json.dumps(edges,separators=(',',':')).encode()).hexdigest(),'nonedge_completeness_checked':False,'chromatic_lower_bound_reproved':False,'elapsed_seconds':time.monotonic()-start}
 (P/'exact_points.json').write_text(json.dumps({'denominator':den,'basis_radicands':R,'points':points},separators=(',',':'))+'\n')
 (P/'exact_edges.json').write_text(json.dumps(edges,separators=(',',':'))+'\n')
 (P/'source_geometry.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()
