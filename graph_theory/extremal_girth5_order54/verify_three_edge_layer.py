"""Complete raw inventory, structural cuts, quad orbits, and encoding controls."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import argparse,copy,hashlib,json
from pysat.formula import IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver
from a0_inventory import profiles
from a0_independent import inventory
from three_quad_orbits import reps
from verify_three_quad_orbits import audit
from three_edge_sat import raw_cases,cases,isolated_pairs,proof_stage
from three_edge_positive_control import check_fixture
from verify_four_edge_layer import witness,one_quad_frames
from verify_a0_multi_quad import unit_controls

HERE=Path(__file__).resolve().parent
ROLES=((1,1),(2,0),(2,1),(3,0),(4,0),(5,0))
def need(test,why):
 if not test:raise ValueError(why)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def high_forest_control():
 E=list(combinations(range(12),2));counts=Counter();rejected=Counter();entry=[]
 for word in combinations(range(len(E)),3):
  H=[E[j] for j in word];N=[set() for _ in range(12)]
  for a,b in H:N[a].add(b);N[b].add(a)
  k=sum(len(n)==2 for n in N)
  if any(len(n)>2 for n in N):rejected['degree_exceeds_two']+=1;continue
  if any(int(b in N[a])+len(N[a]&N[b])>1 for a,b in E):rejected['repeated_short_connection']+=1;continue
  unseen=set(range(12));sizes=[]
  while unseen:
   root=min(unseen);component={root};front=[root]
   while front:
    for v in N[front.pop()]-component:component.add(v);front.append(v)
   unseen-=component;sizes.append(len(component))
  key=tuple(sorted((n for n in sizes if n>1),reverse=True))
  need(key in ((2,2,2),(3,2),(4,)), 'Unexpected high forest')
  need(sum(len(N[t])*(len(N[t])-1)//2 for t in range(12))==k,'High path variable total')
  counts[key]+=1;entry.append([list(word),k,list(key)])
 need(dict(counts)=={(2,2,2):13860,(3,2):23760,(4,):5940},'Complete high-forest count')
 need(sum(counts.values())+sum(rejected.values())==45760,'High-edge cover')
 return dict(edge_triples=45760,admissible=43560,forest_counts=[dict(nontrivial_components=list(k),count=v) for k,v in sorted(counts.items())],rejected=dict(rejected),entries_sha256=digest(entry))

def high_point_control():
 rows=[]
 for a,b,h in product(range(6),range(6),range(4)):
  pool=IDPool();X=[pool.id(('six',i)) for i in range(5)];Y=[pool.id(('seven',i)) for i in range(5)];H=[pool.id(('high',i)) for i in range(3)]
  clauses=[]
  for lits,n in [(X+[-v for v in H],6),(Y+[v for v in H for _ in range(2)],5)]:clauses+=CardEnc.equals(lits,bound=n,vpool=pool,encoding=EncType.seqcounter).clauses
  fixed=[v if i<a else -v for i,v in enumerate(X)]+[v if i<b else -v for i,v in enumerate(Y)]+[v if i<h else -v for i,v in enumerate(H)]
  with Solver(name='g4',bootstrap_with=clauses) as solver:ans=solver.solve(assumptions=fixed)
  need(ans==(a==3+h and b==5-2*h),'Signed high-point quota encoding')
  rows.append([a,b,h,ans])
 for a,b,p in product((False,True),repeat=3):
  clauses=[(-3,1),(-3,2),(3,-1,-2)];truth={1:a,2:b,3:p}
  actual=all(any(truth[abs(v)]==(v>0) for v in C) for C in clauses)
  need(actual==(p==(a and b)),'High-path conjunction')
 return dict(quota_assignments=len(rows),conjunction_assignments=8,quota_sha256=digest(rows))

def finite():
 census=list(profiles());need(sorted(census)==inventory(),'Independent full inventory')
 raw=[(i,*r) for i,r in enumerate(census) if r[0]==3 and not any(r[2][5:]) and not any(r[3][5:])]
 buckets={k:[] for k in ('zero','one_six','one_seven','multiple')};triple_rows=[]
 for i,m,k,s,t in raw:
  q=s[4]+t[4];category='zero' if q==0 else 'multiple' if q>=2 else 'one_six' if s[4] else 'one_seven';buckets[category].append(i)
  if q>=2:
   T=s[3]+t[3];need(T==15-3*q-k-s[0]-t[0],'Exact triple inventory')
   need(T<=9 and 2*(6+t[4]+6*s[0]+2*s[1])>T,'Double-quad necessity')
   triple_rows.append([i,q,T,6+t[4]+6*s[0]+2*s[1]])
 need(len(raw)==121 and len(buckets['zero'])==42 and len(buckets['one_six'])+len(buckets['one_seven'])==40 and len(buckets['multiple'])==39,'Whole raw cover')
 allcases=list(raw_cases());residual=list(cases());remaining=set(residual);closed=[c for c in allcases if c not in remaining]
 need(len(allcases)==135 and len(residual)==51 and len(closed)==84,'Whole orbit case subdivision')
 need({c[0] for c in residual}==set(buckets['multiple']),'Profile coverage')
 fixtures=json.loads((HERE/'four_edge_controls.json').read_text());positive=[check_fixture(r) for r in fixtures]
 mutants=[]
 x=copy.deepcopy(fixtures[0]);x['near'].pop();mutants.append(x)
 x=copy.deepcopy(fixtures[0]);x['covers'][0][1].pop();mutants.append(x)
 for x in mutants:
  try:witness(x)
  except ValueError:pass
  else:raise ValueError('Malformed direct fixture accepted')
 return dict(raw_profiles=raw,human_profile_buckets=buckets,exact_triple_rows=triple_rows,
             raw_orbit_cases=allcases,human_excluded_orbit_cases=closed,certificate_cases=residual,
             stage_counts=dict(Counter(proof_stage(c) for c in residual)),case_list_sha256=digest(residual),
             high_forests=high_forest_control(),high_point_encoding=high_point_control(),
             positive_controls=positive,rejected_mutants=len(mutants),one_quad_frames=one_quad_frames(),unit_controls=unit_controls())

def main():
 p=argparse.ArgumentParser();p.add_argument('--finite-only',action='store_true');args=p.parse_args();out={'finite':finite()}
 if not args.finite_only:
  rows=[]
  for role in ROLES:
   r=audit(*role);r['isolated_pairs']=[isolated_pairs(Qs) for Qs in reps(*role)];rows.append(r)
  need(sum(r['orbits'] for r in rows)==30,'All degree-role quad orbits')
  out['quad_orbits']=rows
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
