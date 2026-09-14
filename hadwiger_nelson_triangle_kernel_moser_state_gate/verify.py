"""Independent exact reconstruction and strict RUP replay of the state gate."""
from fractions import Fraction as F
from itertools import combinations,combinations_with_replacement,product
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,math

def req(ok,msg):
 if not ok:raise ValueError(msg)
def clean(x):return {r:F(v) for r,v in x.items() if v}
def plus(x,y):
 z=dict(x)
 for r,v in y.items():z[r]=z.get(r,F(0))+v
 return clean(z)
def minus(x):return {r:-v for r,v in x.items()}
def times(x,y):
 z={}
 for r,a in x.items():
  for s,b in y.items():
   g=math.gcd(r,s);z[r*s//(g*g)]=z.get(r*s//(g*g),F(0))+g*a*b
 return clean(z)
def cadd(z,w):return plus(z[0],w[0]),plus(z[1],w[1])
def csub(z,w):return plus(z[0],minus(w[0])),plus(z[1],minus(w[1]))
def cmul(z,w):return plus(times(z[0],w[0]),minus(times(z[1],w[1]))),plus(times(z[0],w[1]),times(z[1],w[0]))
def sq(z,w):x,y=csub(z,w);return plus(times(x,x),times(y,y))
def cross(z,w):return plus(times(z[0],w[1]),minus(times(z[1],w[0])))
Q=lambda x:{1:F(x)} if x else {}
O=({},{});U=(Q(1),{});omega=(Q(F(1,2)),{3:F(1,2)});eta=(Q(F(5,6)),{11:F(1,6)})
M=(O,U,omega,cadd(U,omega),eta,cmul(eta,omega),cmul(eta,cadd(U,omega)))

def repair_three(forbidden):
 edges=[]
 for i in range(3):
  for j in range(6):
   v=6*i+j;edges.append((v,6*i+(j+1)%6))
   for k in range(i+1,3):edges.append((v,6*k+j))
 rows=[]
 for sign in (1,-1):
  base=[(i+sign*(-1)**j)%3 for i in range(3) for j in range(6)];rows.append(base)
  for v in range(18):r=base.copy();r[v]=3;rows.append(r)
 for row in rows:
  if all(row[a]!=row[b] for a,b in edges) and all(row[v]!=c for v,c in forbidden):return row
 return None

def reconstruct():
 one=Q(1);edges=tuple((i,j) for i,j in combinations(range(7),2) if sq(M[i],M[j])==one);req(len(edges)==11,'edges')
 colours=tuple(c for c in product(range(4),repeat=7) if all(c[a]!=c[b] for a,b in edges));req(len(colours)==384,'colours')
 triples=[]
 for t in combinations(range(7),3):
  a,b,c=(M[i] for i in t);de=cross(csub(b,a),csub(c,a))
  left=times(times(sq(a,b),sq(b,c)),sq(c,a));right=times(Q(4),times(de,de))
  if left==right:triples.append(t)
 req(len(triples)==10,'triples')
 events=tuple(product(range(18),range(4)));blocked=[];positive=0
 for f in combinations_with_replacement(events,3):
  row=repair_three(f)
  if row is None:blocked.append(f)
  else:positive+=1
 expected=[tuple((v,c) for c in range(4) if c!=v//6) for v in range(18)]
 req(blocked==expected and positive==64806,'three-contact classification')
 variables=tuple((o,t) for o in range(3) for t in triples);clauses=[];sizes=[]
 for c in colours:
  row=[i+1 for i,(o,t) in enumerate(variables) if {c[v] for v in t}==set(range(4))-{o}]
  req(row,'coverage');clauses.append(row);sizes.append(len(row))
 capacity=0
 for v in range(7):
  for o in range(3):
   group=[i+1 for i,(q,t) in enumerate(variables) if q==o and v in t]
   for row in combinations(group,3):clauses.append([-x for x in row]);capacity+=1
 lines=[f'p cnf {len(variables)} {len(clauses)}']+[' '.join(map(str,c))+' 0' for c in clauses]
 cnf=('\n'.join(lines)+'\n').encode()
 data={'scope':'Moser exterior, no patch contacts, at most three incidences per generic component',
  'moser_vertices':7,'moser_complete_unit_edges':[list(e) for e in edges],
  'moser_proper_four_colourings':len(colours),'shell_column_states':11,
  'shell_compatible_ordered_state_pairs':44,'three_incidence_restriction_multisets':64824,
  'blocking_restriction_multisets':len(blocked),'unit_circumradius_moser_triples':[list(t) for t in triples],
  'blocker_variables':len(variables),'coverage_clauses':len(colours),'capacity_clauses':capacity,
  'cnf_clauses':len(clauses),'coverage_clause_size_histogram':{str(k):sizes.count(k) for k in sorted(set(sizes))},
  'cnf_sha256':hashlib.sha256(cnf).hexdigest(),'physical_incidence_bound':42,
  'maximum_important_components':14,'maximum_finite_kernel_vertices':271,'record_candidate':False}
 return data,cnf,positive

def parse_cnf(raw):
 clauses={};declared=None
 for line in raw.decode().splitlines():
  if not line or line[0]=='c':continue
  if line[0]=='p':declared=tuple(map(int,line.split()[2:]));continue
  row=list(map(int,line.split()));req(row[-1]==0,'CNF terminator');clauses[len(clauses)+1]=tuple(row[:-1])
 req(declared==(30,len(clauses)),'CNF header');return clauses

def strict_rup(cnf_raw,lrat_raw):
 clauses=parse_cnf(cnf_raw);initial=len(clauses);adds=deletes=0;final_empty=False
 for line in lrat_raw.decode().splitlines():
  tok=line.split();req(tok,'LRAT line')
  cid=int(tok[0])
  if tok[1]=='d':
   ids=list(map(int,tok[2:]));req(ids[-1]==0,'delete terminator')
   for x in ids[:-1]:req(x in clauses,'delete live clause');del clauses[x];deletes+=1
   continue
  nums=list(map(int,tok[1:]));cut=nums.index(0);lits=tuple(nums[:cut]);hints=nums[cut+1:-1]
  req(nums[-1]==0 and hints,'addition shape');assignment={};conflict=False
  def set_true(lit):
   var=abs(lit);value=lit>0
   if var in assignment:return assignment[var]==value
   assignment[var]=value;return True
  for lit in lits:req(set_true(-lit),'tautological addition')
  for pos,hint in enumerate(hints):
   req(hint>0 and hint in clauses,'positive live RUP hint');row=clauses[hint];unassigned=[];satisfied=False
   for lit in row:
    if abs(lit) not in assignment:unassigned.append(lit)
    elif assignment[abs(lit)]==(lit>0):satisfied=True;break
   req(not satisfied,'satisfied RUP hint')
   if not unassigned:
    req(pos==len(hints)-1,'early conflict');conflict=True;break
   req(len(unassigned)==1 and set_true(unassigned[0]),'nonunit RUP hint')
  req(conflict,'RUP contradiction');clauses[cid]=lits;adds+=1
  if not lits:final_empty=True
 req(final_empty,'no final empty clause')
 return initial,adds,deletes

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--lrat');p.add_argument('--discover',action='store_true');a=p.parse_args();work=Path(a.work);here=Path(__file__).parent
 data,cnf,positive=reconstruct();raw=(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()
 req(raw==(here/'certificate.json').read_bytes()==(work/'certificate.json').read_bytes(),'certificate bytes')
 req(cnf==(here/'state.cnf').read_bytes()==(work/'state.cnf').read_bytes(),'CNF bytes')
 lrat=Path(a.lrat).read_bytes() if a.lrat else (here/'state.lrat').read_bytes();initial,adds,deletes=strict_rup(cnf,lrat)
 out={'status':'PASS','moser_vertices':7,'moser_complete_unit_edges':11,'moser_proper_four_colourings':384,
  'three_incidence_restriction_multisets':64824,'positive_repair_witnesses':positive,
  'blocking_restriction_multisets':18,'unit_circumradius_moser_triples':10,
  'cnf_variables':30,'cnf_clauses':initial,'lrat_additions':adds,'lrat_deletions':deletes,
  'strict_rup_verified':True,'maximum_finite_kernel_vertices':271,'record_candidate':False,
  'certificate_sha256':hashlib.sha256(raw).hexdigest(),'cnf_sha256':hashlib.sha256(cnf).hexdigest(),
  'lrat_sha256':hashlib.sha256(lrat).hexdigest()}
 if not a.discover:req(out==json.loads((here/'expected.json').read_text()),'expected')
 (work/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
