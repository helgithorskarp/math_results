#!/usr/bin/env python3
"""Every V214 anchor and every angle against the specified reflected A159 union."""
from pathlib import Path
from hashlib import sha256
from collections import defaultdict,Counter
import importlib.util,json,argparse
import coverage as C
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
P=ROOT/'hadwiger_nelson_mixed505_all_gadget_anchors/verify.py'
if sha256(P.read_bytes()).hexdigest()!='526b12cbd9d28217e59feb7191c93ace4e5a572ebeadd66cdf384393126aee38':
 raise ValueError('integer arithmetic dependency mismatch')
s=importlib.util.spec_from_file_location('integer_reduction',P);F=importlib.util.module_from_spec(s);s.loader.exec_module(F)
require=F.require

def construction():
 A=F.read_points(159);V=F.read_points(214)
 image=[(a+5,b+1,5-c,-1-d) for a,b,c,d in A]
 B12=list(dict.fromkeys(A+image));B=[tuple(6*x for x in v) for v in B12]
 require(len(B)==293 and B[0]==F.ZERO,'incorrect inner union')
 require(len(set(A)&set(image))==25,'incorrect inner overlap')
 EB,EV=F.edges(B,72),F.edges(V,12)
 require((len(EB),len(EV))==(1389,977),'incorrect internal edges')
 degrees=Counter(v for e in EB for v in e)
 require(degrees[0]==30 and max(degrees[v] for v in range(1,293))==29,'incorrect attachment degree')
 require({(a,b,-c,-d) for a,b,c,d in V}==set(V),'reflection reduction unavailable')
 dd=defaultdict(list)
 for q,a in enumerate(V):
  for v,b in enumerate(V):
   if q!=v:dd[F.subtract(b,a)].append((q,v))
 D=[F.ZERO]+sorted(dd);inc=[[]]+[dd[d] for d in D[1:]]
 require(len(D)==4419,'incorrect difference census')
 return B,V,D,inc,EB,EV

def libraries(B,V,EB,EV):
 libs=[]
 for name,pts,edges in [('B',B,EB),('V',V,EV)]:
  rows=[tuple(map(int,l)) for l in (HERE/f'colors_{name}.txt').read_text().splitlines()]
  require(rows and all(len(c)==len(pts) and c[0]==0 and set(c)<=set(range(4)) and all(c[i]!=c[j] for i,j in edges) for c in rows),'invalid component colouring')
  libs.append(rows)
 require(tuple(map(len,libs))==(5,14),'unexpected library sizes')
 return libs

def result(B,V,D,counts,groups,ch,coverage):
 table=F.anchor_table(coverage.pop('anchors'))
 return {'B_vertices':len(B),'B_edges':1389,'V_vertices':len(V),'V_edges':977,'inner_overlap':25,'origin_degree':30,'B_library_size':5,'V_library_size':14,'difference_vectors':len(D)-1,'nonzero_pairs':(len(B)-1)*(len(D)-1),'pairs':counts,'ambient_classes':len(groups),'classification_sha256':ch,**coverage,'anchor_table_sha256':sha256(table.encode()).hexdigest()},table

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--anchors',type=Path);args=p.parse_args()
 B,V,D,inc,EB,EV=construction();lb,lv=libraries(B,V,EB,EV)
 counts,groups,ch=F.enumerate_groups(B,D)
 covered=C.cover(groups,inc,lb,lv)
 answer,table=result(B,V,D,counts,groups,ch,covered)
 if args.anchors:args.anchors.write_text(table)
 print(json.dumps(answer,indent=2))
if __name__=='__main__':main()
