"""Reproduce exact counts, whole-graph transport, and full combined formulas."""
from pathlib import Path
from itertools import combinations,product,combinations_with_replacement
from math import prod
import argparse,hashlib,json,random,tempfile,time
import carrier,ordered,check_order,dependencies
HERE=Path(__file__).resolve().parent

def controls(cache):
 small=0;image_orbits=0;gadgets=0;transports=0;edge_checks=0;negative=0;boundaries=0
 for m in range(1,7):
  for k in range(6):
   vectors=[list(reversed(x)) for x in combinations_with_replacement(range(m),k)];ranks=set()
   for xs in vectors:
    rank=carrier.rank_multiset(xs,m)
    if carrier.unrank_multiset(rank,m,k)!=xs:raise ValueError('small multiset')
    ranks.add(rank);small+=1
   if ranks!=set(range(len(vectors))) or len(vectors)!=check_order.multiset_table(m,k)[k]:raise ValueError('small complete index')
 for m in range(1,5):
  for k in range(6):
   roots={tuple(sorted(xs,reverse=True)) for xs in product(range(m),repeat=k)}
   if len(roots)!=check_order.multiset_table(m,k)[k]:raise ValueError('orbit image')
   image_orbits+=len(roots)
 # Exhaust every truth assignment for the local prefix definition.
 for p,x,y,z in product((0,1),repeat=4):
  cs=[(-4,1),(-4,-2,3),(-4,2,-3),(4,-1,2,3),(4,-1,-2,-3)];vals={1:p,2:x,3:y,4:z}
  actual=all(any(vals[abs(l)]==int(l>0) for l in c) for c in cs)
  if actual!=bool(z==(p and x==y)):raise ValueError('prefix truth table')
  gadgets+=1
 # Every assignment to two four-bit words and every possible auxiliary vector.
 for left,right in product(range(16),repeat=2):
  matches=0
  for aux in product((0,1),repeat=3):
   vals={1:1,**{2+i:(left>>(3-i))&1 for i in range(4)},**{6+i:(right>>(3-i))&1 for i in range(4)},**{10+i:x for i,x in enumerate(aux)}}
   if all(any(vals[abs(l)]==int(l>0) for l in c) for c in ordered.lex_clauses(list(range(2,6)),list(range(6,10)),10)):matches+=1
   gadgets+=1
  if matches!=int(left>=right):raise ValueError('word comparator')
 rng=random.Random(20260908);family=dependencies.load()['family']
 for row in carrier.registry()['classes']:
  name=row['first_task'];c=carrier.Carrier(name,cache)
  if prod(c.radices())!=c.size:raise ValueError('physical count product')
  for index in sorted(set([0,1,c.size//2,c.size-2,c.size-1])):
   graph=c.unrank(index)
   if c.rank(graph)!=index or carrier.locate(carrier.global_index(name,index))!=(name,index):raise ValueError('whole code interval')
   a=family.matrix(graph)
   keys=[sum(a[u][4*i+v]<<(4*u+v) for u in range(4) for v in range(4)) for i in range(1,c.q)]
   if keys[:c.a]!=sorted(keys[:c.a],reverse=True) or keys[c.a:]!=sorted(keys[c.a:],reverse=True):raise ValueError('physical block order')
   edge_checks+=903;boundaries+=1
  # Random prior carrier plus forced tied roots; every graph remains non-target
  # until a separate literal target verification. Normalization transports all edges.
  old_radices=c.old.radices()
  for repetition in range(4):
   digits=[rng.randrange(v) for v in old_radices]
   if repetition in [0,1]:
    digits[:c.a]=[0 if repetition==0 else 1997]*c.a
    digits[c.a:c.q-1]=[0 if repetition==0 else 1930]*c.b
   index=0
   for d,radix in zip(digits,old_radices):index=index*radix+d
   graph=c.old.unrank(index);out=c.normalize(graph);before=family.matrix(graph);after=family.matrix(out['graph']);perm=out['new_to_old']
   if sorted(perm)!=list(range(43)) or perm[:4]!=list(range(4)) or perm[4*c.q:]!=list(range(4*c.q,43)):raise ValueError('vertex bijection')
   for u,v in combinations(range(43),2):
    if after[u][v]!=before[perm[u]][perm[v]]:raise ValueError('edge transport')
   if c.normalize(out['graph'])['graph']!=out['graph']:raise ValueError('normalizer idempotence')
   transports+=1;edge_checks+=903
  for bad in [-1,c.size,True]:
   try:c.unrank(bad)
   except ValueError:negative+=1
   else:raise ValueError('bad code')
 for xs,m in [([0,1],2),([-1],2),([2],2),([True],2)]:
  try:carrier.rank_multiset(xs,m)
  except ValueError:negative+=1
  else:raise ValueError('bad multiset')
 with tempfile.TemporaryDirectory() as tmp:
  path=Path(tmp)/'model'
  for body in ['s UNKNOWN\n','s UNSATISFIABLE\n','s SATISFIABLE\nv 1 0\n','s SATISFIABLE\nv 1 -1 0\n']:
   path.write_text(body)
   try:ordered.accept('bo1-q7-r5-c000000',cache,path)
   except ValueError:negative+=1
   else:raise ValueError('invalid model accepted')
 return dict(status='INTERFACES_AND_FINITE_CONTROLS_VERIFIED',exhaustive_multisets=small,small_orbit_images=image_orbits,gadget_assignments=gadgets,whole_graph_boundaries=boundaries,whole_graph_transports=transports,physical_edges_checked=edge_checks,negative_inputs_rejected=negative)

def representatives():return [row['task'].replace('mp1','bo1') for row in json.loads((HERE.parent/'ramsey_r55_global_maximal_packing/FORMULA_AUDIT.json').read_text())]

def full(cache,directory,generate=False):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);out=[]
 for triangles,names in [(False,representatives()),(True,[f'bo1-q{q}-r5-c000000' for q in range(7,11)]+['bo1-q7-r7-c000000'])]:
  for name in names:
   file=directory/(name+('-triangles' if triangles else '')+'.cnf')
   produced=ordered.write(name,cache,file,triangles) if generate else None
   checked=check_order.audit_file(name,cache,file,triangles)
   if produced is not None and produced!=checked:raise ValueError('formula producer/auditor')
   out.append(checked);print(json.dumps({'complete_formula_verified':name,'triangles':triangles,'sha256':checked['sha256']}),flush=True)
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('--cnfs');p.add_argument('--generate',action='store_true');p.add_argument('--receipt');a=p.parse_args();t=time.monotonic();result=dict(count=check_order.count_audit(),controls=controls(a.cache))
 if a.generate and not a.cnfs:p.error('--generate needs --cnfs')
 if a.cnfs:
  result['formulas']=full(a.cache,a.cnfs,a.generate);expected=HERE/'FORMULAS.json'
  if expected.exists() and json.loads(json.dumps(result['formulas']))!=json.loads(expected.read_text()):raise ValueError('frozen formula receipt')
 result['seconds']=time.monotonic()-t
 if a.receipt:Path(a.receipt).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'status':'DECLARED_GLOBAL_ORDER_GATE_VERIFIED_NO_TARGET','full_formulas':len(result.get('formulas',[])),'controls':result['controls'],'seconds':result['seconds']}))
