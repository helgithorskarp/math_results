#!/usr/bin/env python3
"""Exact whole-family finite obstruction for A5(z), standard library only."""
from collections import Counter
from itertools import product,combinations
from pathlib import Path
from math import comb
import argparse,hashlib,json
import geometry as G
import eisenstein as E
HERE=Path(__file__).resolve().parent

def need(ok,message):
 if not ok:raise ValueError(message)
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def degree(poly):return max(i+j for i,j,c in poly)
def monomial(row):return sum(bool(a or b) for a,b in row)==1

def independent_event(row):
 # Expand P(Z) conjugate(P)(V)-1, Z=x+s*y,V=x-s*y,s^2=-3.
 # Coefficients (a,b) mean a+b*omega; this does not use G.POWERS.
 out={}
 for j,d in enumerate(row):
  for k,e in enumerate(row):
   cross=G.emul(d,(e[0]+e[1],-e[1]))
   # 2*cross=(2a+b)+b*s. Expand the two binomials separately.
   for h in range(j+1):
    for l in range(k+1):
     n=h+l;co=comb(j,h)*comb(k,l)*(-1)**l
     for shift,c in [(0,2*cross[0]+cross[1]),(1,cross[1])]:
      power=n+shift
      if power%2==0:
       key=(j+k-n,n);out[key]=out.get(key,0)+co*c*(-3)**(power//2)
 need(all(v%2==0 for v in out.values()),'integral norm expansion')
 out={k:v//2 for k,v in out.items()};out[0,0]=out.get((0,0),0)-1
 return G.primitive(out)

def build():
 rows,edgegroups=G.inventory();need(len(rows)==2801,'difference class count')
 need(sum(map(len,edgegroups))==29403 and all(edgegroups),'complete pair inventory')
 circle=G.primitive({(2,0):1,(0,2):3,(0,0):-1})
 events=[];simple_counts=Counter();radial_exponents=[]
 for row in rows:
  f=G.distance_event(row)
  need(f==independent_event(row),'independent squared-distance identity')
  if monomial(row):
   k=next(i for i,d in enumerate(row) if d!=(0,0))
   radial_exponents.append(k);events.append(circle if k else ())
   S={(2,0):1,(0,2):3};power={(0,0):1};quotient={}
   for _ in range(k):quotient=G.add(quotient,power);power=G.mul(power,S)
   if k:need(G.primitive(G.mul(G.decode(circle),quotient))==f,'radial factor identity')
  else:
   simple=E.simple_root_factor(row);need(len(simple)>=2,'nonmonomial has a simple complex root')
   simple_counts[len(simple)-1]+=1;events.append(f)
 factors=sorted(set(events)-{()});need(len(factors)==2797,'active real curves')
 # Every nonmonomial polynomial is absolutely irreducible by the written
 # reciprocal Eisenstein proof; circle is a nonsingular irreducible conic.
 need(len({G.distance_event(r) for r in rows if not monomial(r)})==2796,'distinct nonmonomial curves')
 need(circle not in {G.distance_event(r) for r in rows if not monomial(r)},'separate circle curve')
 fids={f:i for i,f in enumerate(factors)};fe=[[] for _ in factors];base=[]
 for f,ee in zip(events,edgegroups):
  if f:fe[fids[f]]+=ee
  else:base+=ee
 need(len(base)==243,'universal triangles')
 # Complete nonzero collision inventory; remove leading/trailing zero digits.
 collisions=set()
 for row in rows:
  q=list(row)
  while q and q[0]==(0,0):q.pop(0)
  while q and q[-1]==(0,0):q.pop()
  if len(q)>1:collisions.add(G.canon(q))
 collisions=sorted(collisions)
 need(len(collisions)==2400,'nonzero collision polynomials')
 return rows,events,factors,fe,base,collisions,dict(sorted(simple_counts.items())),fids[circle]

def colour_word(spec):
 field=spec['field'];weights=spec['weights']
 need(field in (3,4) and len(weights)==5 and weights[0]==1,'colour specification')
 need(all(type(w) is int and 0<=w<field for w in weights),'colour weights')
 if field==3:return [sum(w*t for w,t in zip(weights,a))%3 for a in G.LABELS]
 def times_omega(w):return (w<<1)^((w>>1)*7)
 word=[]
 for a in G.LABELS:
  c=0
  for w,t in zip(weights,a):c^=(0,w,times_omega(w))[t]
  word.append(c)
 return word

def finite_cover(specs,factors,fe,base):
 words=[colour_word(s) for s in specs];bad=[]
 for word in words:
  need(all(word[a]!=word[b] for a,b in base),'proper universal edges')
  bad.append({f for f,ee in enumerate(fe) if any(word[a]==word[b] for a,b in ee)})
 degrees=list(map(degree,factors));protect=[]
 for f in sorted(bad[0]):
  choices=[i for i,b in enumerate(bad) if f not in b]
  need(choices,'every primary failure curve has a protecting word')
  w=min(choices,key=lambda i:(sum(degrees[g] for g in bad[i]),i));protect.append((f,w))
 pairs=sorted({tuple(sorted((f,g))) for f,w in protect for g in bad[w]})
 need(all(a!=b for a,b in pairs),'coprime distinct curve pairs')
 return words,bad,protect,pairs

def run(certificate_path):
 cert=json.loads(certificate_path.read_text());need(cert['schema']=='hn-complex-radix-v1','certificate schema')
 rows,events,factors,fe,base,collisions,simple,circle=build()
 need(cert['factor_inventory_sha256']==digest(factors),'factor inventory hash')
 words,bad,protect,pairs=finite_cover(cert['colour_specs'],factors,fe,base)
 need(cert['protectors']==[list(x) for x in protect],'canonical protecting word assignment')
 # A direct six-word three-colour cover for every single-curve graph.
 single_specs=[{'field':3,'weights':[1]+[int(i==k) for i in range(4)]} for k in range(4)]
 single_specs=[{'field':3,'weights':[1,0,0,0,0]}]+single_specs+[{'field':3,'weights':[1,1,1,1,1]}]
 single_words=[colour_word(s) for s in single_specs]
 assignment=[]
 for ee in fe:
  choices=[w for w,c in enumerate(single_words) if all(c[a]!=c[b] for a,b in base+ee)]
  need(choices,'single-curve three-colour cover');assignment.append(min(choices))
 # Witnesses for the two counting bounds used in the >=4-curve obstruction.
 # In affine F4^4 a nonzero linear equation has 64 roots; in (F4*)^4,
 # fixing three coordinates leaves at most one of the three final choices.
 # These are proved in PROOF.md, with one exact scalar check below.
 fm=lambda a,b: ((0,a,(a<<1)^((a>>1)*7),a^((a<<1)^((a>>1)*7)))[b])
 need(all(len({fm(a,b) for b in range(4)})==4 for a in (1,2,3)),'F4 nonzero multipliers permute')
 degrees=list(map(degree,factors));bezout=sum(degrees[a]*degrees[b] for a,b in pairs)
 cb=sum(len(q)-1 for q in collisions)
 return {'status':'COMPLEX_RADIX_NONFOUR_PARAMETERS_HAVE_FINITE_EXACT_COVER',
  'maximum_physical_order':243,'label_pairs':29403,'universal_unit_edges':len(base),
  'canonical_difference_polynomials':len(rows),'active_absolutely_irreducible_curves':len(factors),
  'active_curve_degree_histogram':dict(sorted(Counter(degrees).items())),
  'nonmonomial_simple_root_degree_histogram':simple,
  'single_curve_graphs_three_colourable':len(assignment),'single_curve_word_assignment_sha256':digest(assignment),
  'primary_failure_curves':len(bad[0]),'primary_failure_degree_sum':sum(degrees[f] for f in bad[0]),
  'cover_words':len(words),'factor_pair_systems':len(pairs),'factor_pairs_sha256':digest(pairs),
  'injective_parameter_bezout_bound':bezout,'maximum_pair_degree_product':max(degrees[a]*degrees[b] for a,b in pairs),
  'minimum_simultaneous_active_curves_for_injective_nonfour':4,
  'nonzero_collision_polynomials':len(collisions),'collision_polynomial_degree_histogram':dict(sorted(Counter(len(q)-1 for q in collisions).items())),
  'collision_parameter_upper_bound':cb,'all_parameter_upper_bound':bezout+cb,
  'nonfour_parameter_radial_constraint':'1/2 < |z| <= 2',
  'injective_parameter_field_degree_Q_x_y_upper_bound':64,
  'collision_degree_over_Q_omega_upper_bound':4,
  'factor_inventory_sha256':digest(factors),'collision_inventory_sha256':digest(collisions),
  'colour_word_sha256':digest(words),'certificate_sha256':hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
  'proof_CAS_calls':0,'proof_solver_calls':0,'record_improvement':False,
  'full_architecture_four_colour_closure':False,'external_reviewer_acceptance_claimed':False}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--certificate',type=Path,default=HERE/'certificate.json');parser.add_argument('--check-expected',action='store_true');args=parser.parse_args()
 result=run(args.certificate)
 if args.check_expected:need(json.loads(json.dumps(result))==json.loads((HERE/'EXPECTED.json').read_text()),'expected output')
 print(json.dumps(result,indent=2,sort_keys=True))
