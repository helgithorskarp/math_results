#!/usr/bin/env python3
"""Independent exact verifier for the H516 301-point realization gate."""

from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import argparse,json
from pathlib import Path

D=Path(__file__).resolve().parent;R=D.parent
S=R/'hadwiger_nelson_h516_degree4_surgeries'/'SOURCE.json'
G=R/'hadwiger_nelson_h516_k23free_edge_repair'/'graph.json'
C=D/'certificate.json';E=D/'EXPECTED.json';RAD=(1,3,5,15,11,33,55,165)

def need(ok,why):
 if not ok:raise ValueError(why)
def digest_bytes(data):return sha256(data).hexdigest()
def digest(path):return digest_bytes(path.read_bytes())
def field_mul(a,b):
 z=[Fraction(0) for _ in range(8)]
 for i in range(8):
  for j in range(8):z[i^j]+=a[i]*b[j]*RAD[i&j]
 return tuple(z)
def field_add(*rows):return tuple(sum(row[i] for row in rows) for i in range(8))
def field_neg(a):return tuple(-x for x in a)
def field_scale(a,q):return tuple(q*x for x in a)
def parse(row):
 need(type(row) is list and len(row)==8 and all(type(x) is list and len(x)==2 and type(x[0]) is int and type(x[1]) is int and x[1]>0 for x in row),'field row')
 return tuple(Fraction(a,b) for a,b in row)
def compact(a):return [[x.numerator,x.denominator] for x in a]
def square_distance(p,q):
 answer=[0]*8
 for axis in range(2):
  delta=[p[axis][i]-q[axis][i] for i in range(8)]
  for i in range(8):
   for j in range(8):answer[i^j]+=delta[i]*delta[j]*RAD[i&j]
 return tuple(answer)
def field_distance(p,q):return tuple(Fraction(x,9216) for x in square_distance(p,q))
def heron(a,b,c):
 ab=field_mul(a,b);bc=field_mul(b,c);ca=field_mul(c,a)
 squares=field_add(field_mul(a,a),field_mul(b,b),field_mul(c,c))
 return field_add(field_scale(field_add(ab,bc,ca),2),field_neg(squares))
def unit_defect(a,b,c):return field_add(field_mul(field_mul(a,b),c),field_neg(heron(a,b,c)))
def edges_for(vertices,coordinates):
 one=(9216,)+(0,)*7
 return [(a,b) for a,b in combinations(vertices,2) if square_distance(coordinates[a],coordinates[b])==one]
def point_hash(vertices,coordinates):return digest_bytes(json.dumps([coordinates[v] for v in vertices],separators=(',',':')).encode())
def edge_hash(edges):return digest_bytes(''.join(f'{a},{b}\n' for a,b in edges).encode())

def modular_axis(axis,p,roots):
 r3,r5,r11=roots
 values=(1,r3,r5,r3*r5%p,r11,r3*r11%p,r5*r11%p,r3*r5*r11%p)
 return sum(a*b for a,b in zip(axis,values))%p
def alternate_rank(rows,p):
 basis={}
 for source in rows:
  row={i:a%p for i,a in source.items() if a%p}
  while row:
   pivot=min(row)
   if pivot not in basis:
    inverse=pow(row[pivot],p-2,p);basis[pivot]={i:a*inverse%p for i,a in row.items()};break
   factor=row[pivot]
   for i,a in basis[pivot].items():
    value=(row.get(i,0)-factor*a)%p
    if value:row[i]=value
    else:row.pop(i,None)
 return len(basis)
def rigidity_rank(vertices,edges,coordinates,p,roots):
 need(p%4==3 and all(r*r%p==a for r,a in zip(roots,(3,5,11))),'modular roots')
 xy={v:(modular_axis(coordinates[v][0],p,roots),modular_axis(coordinates[v][1],p,roots)) for v in vertices}
 need(len(set(xy.values()))==len(vertices),'modular point collision');pos={v:i for i,v in enumerate(vertices)};rows=[]
 for a,b in reversed(edges):
  i,j=pos[a],pos[b];dx=(xy[a][0]-xy[b][0])%p;dy=(xy[a][1]-xy[b][1])%p
  rows.append({2*i:dx,2*i+1:dy,2*j:-dx,2*j+1:-dy})
 return alternate_rank(rows,p)

def run(certificate):
 need(type(certificate) is dict and set(certificate)=={'schema','dependencies_sha256','abstract_graph','fixed_realization_obstructions','fixed_subframework_rigidity','physical_endpoint_supports'},'top fields')
 need(certificate['schema']=='hn-h516-301-realization-gate-v1','schema')
 need(certificate['dependencies_sha256']=={'SOURCE.json':digest(S),'graph.json':digest(G)},'dependencies')
 source=json.loads(S.read_text());graph=json.loads(G.read_text());coordinates=dict(zip(source['labels'],source['coordinates'],strict=True));need(len(coordinates)==516,'source coordinates')
 merged={int(k):v for k,v in graph['merged_classes'].items()};need(certificate['abstract_graph']=={'vertices':301,'edges':1452,'merged_classes':graph['merged_classes']},'abstract graph')
 fixed=sorted(set(graph['labels'])-set(merged));adj={v:set() for v in graph['labels']}
 for a,b in graph['edges']:adj[a].add(b);adj[b].add(a)
 obstruction_rows=certificate['fixed_realization_obstructions'];need(len(obstruction_rows)==4 and [x['label'] for x in obstruction_rows]==sorted(merged),'obstruction coverage')
 obstruction_checks=0
 for row in obstruction_rows:
  label=row['label'];triple=row['determining_triple'];need(row['source_fibre']==merged[label] and row['degree']==len(adj[label]),'obstruction metadata');need(len(triple)==3 and len(set(triple))==3 and all(v in adj[label] and v in fixed for v in triple),'determining neighbors')
  a=field_distance(coordinates[triple[1]],coordinates[triple[2]]);b=field_distance(coordinates[triple[0]],coordinates[triple[2]]);c=field_distance(coordinates[triple[0]],coordinates[triple[1]]);h=heron(a,b,c);defect=unit_defect(a,b,c)
  need(row['side_squared']==list(map(compact,(a,b,c))) and row['heron_16_area_squared']==compact(h) and row['unit_circumradius_defect']==compact(defect),'obstruction arithmetic');need(h!=(Fraction(0),)*8 and defect!=(Fraction(0),)*8,'nondegenerate nonunit circumcircle');obstruction_checks+=1
 fixed_edges=[tuple(e) for e in graph['edges'] if e[0] in fixed and e[1] in fixed];rigid=certificate['fixed_subframework_rigidity'];need(rigid['vertices']==297 and rigid['edges']==len(fixed_edges)==1397 and rigid['maximum_rank']==591,'rigidity metadata');need(len(rigid['specializations'])==3,'rigidity rows')
 rigidity_checks=0
 for row in rigid['specializations']:
  rank=rigidity_rank(fixed,fixed_edges,coordinates,row['prime'],row['roots_sqrt3_sqrt5_sqrt11']);need(rank==row['rank']==591,'rigidity rank');rigidity_checks+=len(fixed_edges)
 supports=certificate['physical_endpoint_supports'];need(len(supports)==16 and [row['bits'] for row in supports]==[list(x) for x in product((0,1),repeat=4)],'support coverage')
 pair_checks=edge_checks=0;hist=Counter()
 for row in supports:
  reps=[merged[label][bit] for label,bit in zip(sorted(merged),row['bits'],strict=True)];vertices=sorted(fixed+reps);need(row['representatives']==reps and row['vertices']==len(vertices)==301 and len({tuple(sum(coordinates[v],[])) for v in vertices})==301,'support points');edges=edges_for(vertices,coordinates);pair_checks+=len(vertices)*(len(vertices)-1)//2;hist[len(edges)]+=1
  need(row['edges']==len(edges) and row['point_sha256']==point_hash(vertices,coordinates) and row['edge_sha256']==edge_hash(edges),'support graph identity');word=row['four_colouring'];need(type(word) is str and len(word)==301 and set(word)<=set('0123'),'word format');col=dict(zip(vertices,word,strict=True));need(all(col[a]!=col[b] for a,b in edges),'improper word');edge_checks+=len(edges)
 result={'verified':True,'abstract_vertices':301,'abstract_edges':1452,'fixed_coordinate_obstructions':obstruction_checks,'fixed_subframework_vertices':297,'fixed_subframework_edges':1397,'full_modular_rigidity_ranks':3,'rigidity_edge_rows_checked':rigidity_checks,'physical_supports':16,'physical_vertices_each':301,'physical_pair_distances_checked':pair_checks,'physical_edge_histogram':{str(k):v for k,v in sorted(hist.items())},'four_colour_words_checked':16,'four_colour_edge_checks':edge_checks,'record_candidate':False,'scope':'fixed inherited-coordinate endpoint choices and local neighborhood of the inherited 297-point framework'}
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=C);ap.add_argument('--check-expected',action='store_true');args=ap.parse_args();certificate=json.loads(args.certificate.read_text());result=run(certificate)
 controls={}
 for name,mutate in [('missing_support',lambda x:x['physical_endpoint_supports'].pop()),('bad_word',lambda x:x['physical_endpoint_supports'][0].__setitem__('four_colouring','0'*301)),('repeated_triple',lambda x:x['fixed_realization_obstructions'][0].__setitem__('determining_triple',[20,20,31])),('bad_rank',lambda x:x['fixed_subframework_rigidity']['specializations'][0].__setitem__('rank',590)),('bad_dependency',lambda x:x['dependencies_sha256'].__setitem__('SOURCE.json','0'*64))]:
  bad=deepcopy(certificate);mutate(bad)
  try:run(bad)
  except (ValueError,KeyError):controls[name]=True
  else:raise ValueError('bad certificate accepted: '+name)
 result['negative_controls']=controls
 if args.check_expected:need(result==json.loads(E.read_text()),'expected mismatch')
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
