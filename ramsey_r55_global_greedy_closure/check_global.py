"""Independent literal physical formula and whole-family count auditor."""
from pathlib import Path
from itertools import combinations,product
from math import prod,comb
from collections import Counter
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent

def physical(branch):
 r,s,t=branch
 if r not in (5,6,7) or s not in range(1,5) or t not in range(4) or (s<4 and t==3):raise ValueError('branch')
 blocks=[list(range(4*i,4*i+4)) for i in range(7)]+[list(range(28+3*i,31+3*i)) for i in range(5)]
 fixed={}
 for i,vertices in enumerate(blocks):
  for k,p in enumerate(combinations(vertices,2)):
   fixed[p]=int(i<r) if i<7 else int(i<7+s) if i<11 else ((0,1,3,7)[t]>>k)&1
 variables={p:len([q for q in combinations(range(43),2) if q<p and q not in fixed])+2 for p in combinations(range(43),2) if p not in fixed}
 return blocks,fixed,variables

def forbid(vertices,size,fixed,variables):
 for chosen in combinations(vertices,size):
  edges=list(combinations(chosen,2))
  if any(p in fixed and fixed[p]==0 for p in edges):continue
  yield tuple(-variables[p] for p in edges if p not in fixed)

def extras(branch):
 blocks,fixed,variables=physical(branch);r,s,t=branch
 # Residual vertex intervals are computed arithmetically, independently of
 # producer block unions. They include previously removed blue blocks.
 if r<7:yield from forbid(range(4*r,43),4,fixed,variables)
 if s<4:yield from forbid(range(28+3*s,43),3,fixed,variables)

def full(branch):
 blocks,fixed,variables=physical(branch);r,s,t=branch
 yield (1,)
 for j,child in enumerate(blocks[1:],1):
  if j<11 or t in (0,3):ordered=list(zip(child,child[1:]))
  elif t==1:ordered=[(child[0],child[1])]
  else:ordered=[(child[1],child[2])]
  for a,b in ordered:
   for mask in range(256):
    left,right=divmod(mask,16)
    if left>=right:continue
    yield tuple((-1 if value>>i&1 else 1)*variables[i,v] for v,value in [(a,left),(b,right)] for i in range(4))
 for chosen in combinations(range(43),5):
  edges=list(combinations(chosen,2))
  for color in (1,0):
   if any(p in fixed and fixed[p]!=color for p in edges):continue
   yield tuple((-1 if color else 1)*variables[p] for p in edges if p not in fixed)
 if r<7:yield from forbid(range(4*r,43),4,fixed,variables)
 if s<4:yield from forbid(range(28+3*s,43),3,fixed,variables)

def audit_file(branch,path):
 count=0;h=hashlib.sha256()
 with Path(path).open('rb') as f:
  header=f.readline();h.update(header);parts=header.decode().split()
  if len(parts)!=4 or parts[:3]!=['p','cnf','847']:raise ValueError('DIMACS header')
  wanted=int(parts[3])
  for expected in full(branch):
   line=f.readline();h.update(line)
   fields=line.decode().split()
   if not fields or fields[-1]!='0' or tuple(map(int,fields[:-1]))!=expected:raise ValueError(('literal formula mismatch',branch,count))
   count+=1
  if f.read() or count!=wanted:raise ValueError('DIMACS length')
 return {'status':'VERIFIED_EVERY_LITERAL_OF_COMPLETE_STRENGTHENED_BRANCH','branch':branch,'variables':847,'clauses':count,'bytes':Path(path).stat().st_size,'sha256':h.hexdigest()}

def counts(base):
 # Reconstruct every Cartesian factor from the independently reviewed domain
 # tables, without dividing the producer's parent-count field.
 old=json.loads((base/'COUNTS.json').read_text());domains=json.loads((base/'DOMAINS.json').read_text());root=json.loads((base/'ROOT_DOMAINS.json').read_text())
 pair={(x['left'],x['right']):x['count'] for x in domains}
 # Root record schema is fixed by the accepted h3835 source.
 rooted={x['child']:x['count'] for x in root}
 tail=json.loads((HERE/'TAIL_AUDIT.json').read_text());cover={x['n']:x['cover_totals'] for x in tail['totals']}
 expected=json.loads((HERE/'GLOBAL_COUNTS.json').read_text());rows={tuple(x['branch']):x for x in expected['branches']};total=parent_total=0
 removed=[]
 for r in (5,6,7):
  for s in range(5):
   for t,last in enumerate(('B3','E3','P3','R3')):
    kinds=['R4']*r+['B4']*(7-r)+['R3']*s+['B3']*(4-s)+[last]
    fullpairs=list(combinations(range(12),2));factors={(i,j):rooted[kinds[j]] if i==0 else pair[kinds[i],kinds[j]] for i,j in fullpairs}
    parent_count=prod(factors.values());parent_total+=parent_count
    if s==0 or (s!=4 and t==3):removed.append([r,s,t]);continue
    residual=set(range(7+s,12));inside=[p for p in fullpairs if set(p)<=residual];outside=[p for p in fullpairs if p not in inside];oldtail=prod(factors[p] for p in inside);raw=cover[15-3*s][t] if s<4 else 1
    carrier=min(raw,oldtail);count=carrier*prod(factors[p] for p in outside);total+=count;row=rows[r,s,t]
    if (oldtail,raw,carrier,count,parent_count)!=(row['parent_tail_pair_count'],row['catalog_embedding_cover'],row['tail_carrier_count'],row['whole_graph_cover_count'],row['parent_count']):raise ValueError('Branch count mismatch')
 if parent_total!=old['retained_rooted_family'] or total!=expected['whole_graph_representation_count'] or len(rows)!=39 or removed!=expected['removed_normal_form_branches'] or not 4*total<parent_total:raise ValueError('Global count gate')
 return {'status':'VERIFIED_INDEPENDENT_COMPLETE_FAMILY_BOUND','branches':39,'parent_physical_count':parent_total,'new_representation_count':total,'removed_normal_form_branches':21,'factor4_strict':True,'power_two_upper':total.bit_length()}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path,default=HERE.parent/'ramsey_r55_global_clique_packing');p.add_argument('--branch');p.add_argument('--cnf',type=Path);a=p.parse_args()
 print(json.dumps(audit_file(list(map(int,a.branch.split(','))),a.cnf) if a.cnf else counts(a.base),sort_keys=True))
