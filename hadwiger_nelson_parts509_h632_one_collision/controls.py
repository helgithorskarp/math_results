"""Finite checks of matching witnesses, propagation soundness, and corruption.

The matching control uses subset dynamic programming. The graph control checks
all maps with at most one identification on all graph pairs through order four.
"""
from itertools import combinations,product
from pathlib import Path
from copy import deepcopy
import argparse,json
import generate as P
import verify as V

def maxmatch(rows):
 possible={0}
 for row in rows:
  nxt=set(possible)
  for b in possible:
   for h in row:
    if not (b>>h&1):nxt.add(b|(1<<h))
  possible=nxt
 return max(map(int.bit_count,possible))

def matching_controls():
 count=0;deficient=0
 for l in range(5):
  for r in range(5):
   for bits in range(1<<(l*r)):
    rows={u:{h for h in range(r) if bits>>(u*r+h)&1} for u in range(l)}
    A=P.hall_witness(rows);maximum=maxmatch(list(rows.values()))
    V.require((A is None)==(maximum>=l-1),'Hall producer versus subset DP')
    if A is not None:
     B=set().union(*(rows[u] for u in A));V.require(len(B)<=len(A)-2,'literal Hall inequality');deficient+=1
    count+=1
 return count,deficient

def allgraphs(n):
 pairs=list(combinations(range(n),2));out=[]
 for bits in range(1<<len(pairs)):
  edges=[e for i,e in enumerate(pairs) if bits>>i&1];out.append((edges,V.adjacency(n,edges)))
 return out

def small_reduce(sa,ha):
 n=len(sa);m=len(ha);D=[{h for h in range(m) if len(ha[h])>=len(sa[v])-1} for v in range(n)]
 while True:
  new=[]
  for v in range(n):
   keep=set()
   for h in D[v]:
    rows=[D[u]&ha[h] for u in sa[v]]
    if all(rows) and maxmatch(rows)>=len(sa[v])-1:keep.add(h)
   new.append(keep)
  if new==D:return D
  D=new

def graph_controls():
 graphs={n:allgraphs(n) for n in range(1,5)};cases=maps=homomorphisms=0
 for n in range(1,5):
  for m in range(1,5):
   candidates=[f for f in product(range(m),repeat=n) if len(set(f))>=n-1]
   for edges,sa in graphs[n]:
    for _,ha in graphs[m]:
     D=small_reduce(sa,ha);cases+=1
     for f in candidates:
      maps+=1
      if all(f[v] in ha[f[u]] for u,v in edges):
       homomorphisms+=1;V.require(all(f[v] in D[v] for v in range(n)),'actual near-injective map removed')
 return cases,maps,homomorphisms

def malformed_controls(path):
 cert=json.loads(path.read_text());se,he=V.inputs();sa=V.adjacency(509,se);ha=V.adjacency(632,he);mutants=[]
 def alter(key,value):
  c=deepcopy(cert);c[key]=value;mutants.append(c)
 alter('format','other');alter('source_vertices',508);alter('host_vertices',631);alter('maximum_identifications',2);alter('empty_source_vertex',-1)
 alter('removals',cert['removals'][:-1]);alter('removals',[cert['removals'][0]]+cert['removals'])
 c=deepcopy(cert);c['removals'][0][1]=632;mutants.append(c)
 c=deepcopy(cert);c['removals'][0][3]=[509];mutants.append(c)
 c=deepcopy(cert);i=next(i for i,r in enumerate(c['removals']) if r[2]=='H');c['removals'][i][3]=c['removals'][i][3][:1];mutants.append(c)
 c=deepcopy(cert);c['removals'][0][2]='Z';mutants.append(c)
 c=deepcopy(cert);c['removals'][0][3]=[];mutants.append(c)
 rejected=0
 for c in mutants:
  try:V.check_proof(sa,ha,c)
  except (ValueError,IndexError,KeyError):rejected+=1
  else:raise ValueError('malformed certificate accepted')
 return rejected

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',required=True,type=Path);a=ap.parse_args();b,d=matching_controls();c,m,h=graph_controls();bad=malformed_controls(a.certificate)
 print(json.dumps({'bipartite_graphs':b,'Hall_deficient_graphs':d,'source_host_graph_pairs':c,'near_injective_functions_tested':m,'proper_homomorphisms_preserved':h,'malformed_certificates_rejected':bad,'all_checks_passed':True},sort_keys=True))
