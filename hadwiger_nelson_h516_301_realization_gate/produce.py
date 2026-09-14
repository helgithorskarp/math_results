#!/usr/bin/env python3
"""Produce the compact H516 301-point realization-gate certificate."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import argparse, json
from pathlib import Path

D=Path(__file__).resolve().parent; R=D.parent
S=R/'hadwiger_nelson_h516_degree4_surgeries'/'SOURCE.json'
G=R/'hadwiger_nelson_h516_k23free_edge_repair'/'graph.json'
RAD=(1,3,5,15,11,33,55,165); ONE=(Fraction(1),)+(Fraction(0),)*7

def digest(path):return sha256(path.read_bytes()).hexdigest()
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,q):return tuple(q*x for x in a)
def mul(a,b):
 out=[Fraction(0)]*8
 for i,x in enumerate(a):
  for j,y in enumerate(b):out[i^j]+=x*y*RAD[i&j]
 return tuple(out)
def norm_raw(p,q):
 out=[0]*8
 for axis in range(2):
  z=[a-b for a,b in zip(p[axis],q[axis])]
  for i in range(8):
   out[0]+=z[i]*z[i]*RAD[i]
   for j in range(i+1,8):out[i^j]+=2*z[i]*z[j]*RAD[i&j]
 return tuple(out)
def norm_field(p,q):return tuple(Fraction(x,96*96) for x in norm_raw(p,q))
def compact(a):return [[x.numerator,x.denominator] for x in a]
def field_sum(rows):
 out=(Fraction(0),)*8
 for row in rows:out=add(out,row)
 return out
def heron(a,b,c):
 return sub(scale(field_sum((mul(a,b),mul(b,c),mul(c,a))),2),
            field_sum((mul(a,a),mul(b,b),mul(c,c))))
def unit_defect(a,b,c):return sub(mul(mul(a,b),c),heron(a,b,c))

def physical_edges(vertices,coordinates):
 return [(a,b) for a,b in combinations(vertices,2)
         if norm_raw(coordinates[a],coordinates[b])==(96*96,)+(0,)*7]
def edge_hash(edges):return sha256(''.join(f'{a},{b}\n' for a,b in edges).encode()).hexdigest()
def point_hash(vertices,coordinates):
 return sha256(json.dumps([coordinates[v] for v in vertices],separators=(',',':')).encode()).hexdigest()

def colouring(vertices,edges):
 pos={v:i for i,v in enumerate(vertices)};adj=[set() for _ in vertices]
 for a,b in edges:a=pos[a];b=pos[b];adj[a].add(b);adj[b].add(a)
 colours=[-1]*len(vertices)
 for c,v in enumerate((0,143,162)):colours[pos[v]]=c
 def rec(left):
  if left==0:return True
  v=max((i for i,c in enumerate(colours) if c<0),key=lambda i:(len({colours[j] for j in adj[i] if colours[j]>=0}),len(adj[i]),-i))
  forbidden={colours[j] for j in adj[v] if colours[j]>=0}
  for c in range(4):
   if c not in forbidden:
    colours[v]=c
    if rec(left-1):return True
  colours[v]=-1;return False
 if not rec(len(vertices)-3):raise ValueError('unexpected non-four support')
 if any(colours[pos[a]]==colours[pos[b]] for a,b in edges):raise ValueError('bad word')
 return ''.join(map(str,colours))

def sqrt_mod(a,p):
 if p%4!=3 or pow(a,(p-1)//2,p)!=1:raise ValueError('prime gate')
 x=pow(a,(p+1)//4,p)
 if x*x%p!=a:raise ValueError('root gate')
 return min(x,p-x)
def eval_axis(a,p,roots):
 r3,r5,r11=roots;b=(1,r3,r5,r3*r5%p,r11,r3*r11%p,r5*r11%p,r3*r5*r11%p)
 return sum(x*y for x,y in zip(a,b))%p
def sparse_rank(rows,p):
 basis={}
 for source in rows:
  row={c:v%p for c,v in source.items() if v%p}
  while row:
   pivot=max(row)
   if pivot not in basis:
    inv=pow(row[pivot],p-2,p);basis[pivot]={c:v*inv%p for c,v in row.items()};break
   factor=row[pivot]
   for c,v in basis[pivot].items():
    z=(row.get(c,0)-factor*v)%p
    if z:row[c]=z
    else:row.pop(c,None)
 return len(basis)
def rigidity(fixed,edges,coordinates,p):
 roots=tuple(sqrt_mod(a,p) for a in (3,5,11));pos={v:i for i,v in enumerate(fixed)}
 xy={v:(eval_axis(coordinates[v][0],p,roots),eval_axis(coordinates[v][1],p,roots)) for v in fixed}
 if len(set(xy.values()))!=len(xy):raise ValueError('modular collision')
 rows=[]
 for a,b in edges:
  i,j=pos[a],pos[b];dx=(xy[a][0]-xy[b][0])%p;dy=(xy[a][1]-xy[b][1])%p
  rows.append({2*i:dx,2*i+1:dy,2*j:-dx,2*j+1:-dy})
 return {'prime':p,'roots_sqrt3_sqrt5_sqrt11':list(roots),'rank':sparse_rank(rows,p)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=D/'certificate.json');args=ap.parse_args()
 source=json.loads(S.read_text());graph=json.loads(G.read_text());coordinates=dict(zip(source['labels'],source['coordinates']))
 merged={int(k):v for k,v in graph['merged_classes'].items()};base=sorted(set(graph['labels'])-set(merged))
 adjacency={v:set() for v in graph['labels']}
 for a,b in graph['edges']:adjacency[a].add(b);adjacency[b].add(a)
 obstructions=[]
 for label in sorted(merged):
  neighbors=sorted(adjacency[label]);fixed_neighbors=[v for v in neighbors if v not in merged]
  for triple in combinations(fixed_neighbors,3):
   a=norm_field(coordinates[triple[1]],coordinates[triple[2]])
   b=norm_field(coordinates[triple[0]],coordinates[triple[2]])
   c=norm_field(coordinates[triple[0]],coordinates[triple[1]])
   h=heron(a,b,c)
   if h!=(Fraction(0),)*8:break
  defect=unit_defect(a,b,c)
  if defect==(Fraction(0),)*8:raise ValueError('selected triple lies on unit circle')
  obstructions.append({'label':label,'source_fibre':merged[label],'degree':len(neighbors),'determining_triple':list(triple),'side_squared':list(map(compact,(a,b,c))),'heron_16_area_squared':compact(h),'unit_circumradius_defect':compact(defect)})
 fixed_edges=[tuple(e) for e in graph['edges'] if e[0] in base and e[1] in base]
 rigid=[rigidity(base,fixed_edges,coordinates,p) for p in (1019,1031,1091)]
 supports=[]
 for bits in product((0,1),repeat=4):
  reps=[merged[label][bit] for label,bit in zip(sorted(merged),bits)];vertices=sorted(base+reps);edges=physical_edges(vertices,coordinates)
  supports.append({'bits':list(bits),'representatives':reps,'vertices':len(vertices),'edges':len(edges),'point_sha256':point_hash(vertices,coordinates),'edge_sha256':edge_hash(edges),'four_colouring':colouring(vertices,edges)})
 certificate={'schema':'hn-h516-301-realization-gate-v1','dependencies_sha256':{'SOURCE.json':digest(S),'graph.json':digest(G)},'abstract_graph':{'vertices':graph['vertices'],'edges':graph['edge_count'],'merged_classes':graph['merged_classes']},'fixed_realization_obstructions':obstructions,'fixed_subframework_rigidity':{'vertices':len(base),'edges':len(fixed_edges),'maximum_rank':2*len(base)-3,'specializations':rigid},'physical_endpoint_supports':supports}
 args.output.write_text(json.dumps(certificate,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(args.output),'supports':len(supports),'edge_histogram':dict(sorted(Counter(x['edges'] for x in supports).items())),'all_fixed_obstructions_nonzero':all(any(x!=[0,1] for x in row['unit_circumradius_defect']) for row in obstructions),'all_ranks_full':all(x['rank']==2*len(base)-3 for x in rigid),'certificate_sha256':digest(args.output)},sort_keys=True))
if __name__=='__main__':main()
