"""Produce the exact Moser/three-contact state certificate and canonical CNF."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product
import argparse, hashlib, json
from pathlib import Path

Z=(F(0),)*4; ONE=(F(1),F(0),F(0),F(0))
def sc(x):return (F(x),F(0),F(0),F(0))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def neg(a):return tuple(-x for x in a)
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 out=[F(0)]*4
 for i,x in enumerate(a):
  for j,y in enumerate(b):
   q=i&j;out[i^j]+=x*y*(3 if q&1 else 1)*(11 if q&2 else 1)
 return tuple(out)
def ca(z,w):return add(z[0],w[0]),add(z[1],w[1])
def cs(z,w):return sub(z[0],w[0]),sub(z[1],w[1])
def cm(z,w):return sub(mul(z[0],w[0]),mul(z[1],w[1])),add(mul(z[0],w[1]),mul(z[1],w[0]))
def sq(z,w):x,y=cs(z,w);return add(mul(x,x),mul(y,y))
def cross(z,w):return sub(mul(z[0],w[1]),mul(z[1],w[0]))
def need(ok,msg):
 if not ok:raise ValueError(msg)

O=(Z,Z); U=(ONE,Z); omega=(sc(F(1,2)),(F(0),F(1,2),F(0),F(0)))
eta=(sc(F(5,6)),(F(0),F(0),F(1,6),F(0)))
M=(O,U,omega,ca(U,omega),eta,cm(eta,omega),cm(eta,ca(U,omega)))
STATES=tuple(s for s in permutations(range(4),3) if all(s[i]!=i for i in range(3)))
COMPAT=tuple(tuple(all(a[i]!=b[i] for i in range(3)) for b in STATES) for a in STATES)

def oracle(forbidden):
 masks=[set(range(4))-{i} for i in range(3) for _ in range(6)]
 for v,c in forbidden:masks[v].discard(c)
 allowed=[[s for s,p in enumerate(STATES) if all(p[i] in masks[6*i+j] for i in range(3))] for j in range(6)]
 for start in allowed[0]:
  reached={start}
  for j in range(1,6):
   reached={t for t in allowed[j] if any(COMPAT[p][t] for p in reached)}
  if any(COMPAT[t][start] for t in reached):return True
 return False

def produce():
 edges=tuple((i,j) for i,j in combinations(range(7),2) if sq(M[i],M[j])==ONE);need(len(edges)==11,'edges')
 colours=tuple(c for c in product(range(4),repeat=7) if all(c[a]!=c[b] for a,b in edges));need(len(colours)==384,'colours')
 triples=[]
 for t in combinations(range(7),3):
  a,b,c=(M[i] for i in t);de=cross(cs(b,a),cs(c,a))
  if mul(mul(sq(a,b),sq(b,c)),sq(c,a))==mul(sc(4),mul(de,de)):triples.append(t)
 need(len(triples)==10,'triples')
 events=tuple(product(range(18),range(4)))
 blocked=[f for f in combinations_with_replacement(events,3) if not oracle(f)]
 expected=[tuple((v,c) for c in range(4) if c!=v//6) for v in range(18)]
 need(blocked==expected,'blockers')
 variables=tuple((o,t) for o in range(3) for t in triples);clauses=[];sizes=[]
 for c in colours:
  row=[i+1 for i,(o,t) in enumerate(variables) if {c[v] for v in t}==set(range(4))-{o}]
  need(row,'coverage');clauses.append(row);sizes.append(len(row))
 capacity=0
 for v in range(7):
  for o in range(3):
   group=[i+1 for i,(q,t) in enumerate(variables) if q==o and v in t]
   for row in combinations(group,3):clauses.append([-x for x in row]);capacity+=1
 lines=[f'p cnf {len(variables)} {len(clauses)}']+[' '.join(map(str,c))+' 0' for c in clauses]
 cnf=('\n'.join(lines)+'\n').encode()
 data={'scope':'Moser exterior, no patch contacts, at most three incidences per generic component',
  'moser_vertices':7,'moser_complete_unit_edges':[list(e) for e in edges],
  'moser_proper_four_colourings':len(colours),'shell_column_states':len(STATES),
  'shell_compatible_ordered_state_pairs':sum(map(sum,COMPAT)),
  'three_incidence_restriction_multisets':64824,'blocking_restriction_multisets':len(blocked),
  'unit_circumradius_moser_triples':[list(t) for t in triples],
  'blocker_variables':len(variables),'coverage_clauses':len(colours),'capacity_clauses':capacity,
  'cnf_clauses':len(clauses),'coverage_clause_size_histogram':{str(k):sizes.count(k) for k in sorted(set(sizes))},
  'cnf_sha256':hashlib.sha256(cnf).hexdigest(),'physical_incidence_bound':42,
  'maximum_important_components':14,'maximum_finite_kernel_vertices':271,'record_candidate':False}
 return data,cnf

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--discover',action='store_true');a=p.parse_args()
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True);data,cnf=produce();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
 here=Path(__file__).parent
 if not a.discover:
  need(raw==(here/'certificate.json').read_bytes(),'certificate mismatch');need(cnf==(here/'state.cnf').read_bytes(),'CNF mismatch')
 (out/'certificate.json').write_bytes(raw);(out/'state.cnf').write_bytes(cnf)
 report={'status':'PASS','certificate_sha256':hashlib.sha256(raw).hexdigest(),'cnf_sha256':hashlib.sha256(cnf).hexdigest()}
 (out/'build.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':main()
