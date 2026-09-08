"""Compact replay and optional full physical CNF regeneration/audit."""
from pathlib import Path
import argparse,hashlib,json,time,math
import audit,catalog,family
HERE=Path(__file__).resolve().parent

def cases():
 out=[]
 for row in family.registry()['classes']:
  c=[0,row['core_stop']//2,row['core_stop']-1][(row['r']-5)%3]
  out.append(family.task_id(row['q'],row['r'],c))
 return out

def replay(cache,cnfs=None,generate=False):
 catalog.inputs(cache);reg=audit.registry();checked=0;edges=0;negative=0;formulae=[]
 for name in cases():
  task=family.Task(name,cache);q,r,n,fixed,variables=audit.physical(name,cache)
  if fixed!=task.fixed or variables!=task.variables:raise ValueError('edge model')
  size=task.size
  if math.prod(task.radices())!=size:raise ValueError('physical radix product')
  for local in [0,size-1]:
   if family.locate(family.global_index(name,local))!=(name,local):raise ValueError('global interval transport')
  for code in sorted(set([0,1,size//2,size-2,size-1])):
   g=task.unrank(code)
   if task.rank(g)!=code:raise ValueError('rank/unrank')
   # Independent graph-bit read and physical pair/star checks.
   word=int(g['red_hex'],16);values={e:(word>>k)&1 for k,e in enumerate(__import__('itertools').combinations(range(43),2))}
   for e,c in fixed.items():
    if values[e]!=c:raise ValueError('fixed edge')
   for i,j in __import__('itertools').combinations(range(q),2):
    vs=list(range(4*i,4*i+4))+list(range(4*j,4*j+4))
    for five in __import__('itertools').combinations(vs,5):
     colors=[values[e] for e in __import__('itertools').combinations(five,2)]
     if len(set(colors))==1:raise ValueError('literal pair domain')
    if i==0:
     signs=[sum(values[u,v]<<u for u in range(4)) for v in range(4*j,4*j+4)]
     if signs!=sorted(signs,reverse=True):raise ValueError('physical root order')
   for i in range(q):
    for v in range(4*q,43):
     colors=[values[u,v] for u in range(4*i,4*i+4)]
     if all(x==int(i<r) for x in colors):raise ValueError('physical star domain')
   checked+=1;edges+=903
  for bad in [-1,size,True,0.5]:
   try:task.unrank(bad)
   except ValueError:negative+=1
   else:raise ValueError('bad code accepted')
  if cnfs:
   path=Path(cnfs)/(name+'.cnf')
   if generate:task.write(path)
   result=audit.formula(name,cache,path)
   if result['clauses']!=task.dimensions()['clauses']:raise ValueError('dimensions')
   formulae.append(result);print(json.dumps({'physical_cnf_verified':name,'sha256':result['sha256']}),flush=True)
 result=dict(status='GLOBAL_COVER_INTERFACE_VERIFIED_NO_TARGET',macro_classes=reg['macro_classes'],tasks=reg['tasks'],carrier_graphs_checked=checked,physical_edges_checked=edges,negative_codes_rejected=negative,full_formulas_checked=len(formulae))
 return result,formulae

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('--cnfs');p.add_argument('--generate-cnfs',action='store_true');p.add_argument('--output');a=p.parse_args();t=time.monotonic()
 if a.generate_cnfs and not a.cnfs:p.error('--generate-cnfs needs --cnfs')
 if a.cnfs:Path(a.cnfs).mkdir(parents=True,exist_ok=True)
 result,formulae=replay(a.cache,a.cnfs,a.generate_cnfs)
 if formulae:
  expected=HERE/'FORMULA_AUDIT.json'
  canonical=json.loads(json.dumps(formulae))
  if expected.exists() and canonical!=json.loads(expected.read_text()):raise ValueError('frozen formula receipt changed')
  if a.output:Path(a.output).write_text(json.dumps(formulae,indent=2)+'\n')
 result['seconds']=time.monotonic()-t;print(json.dumps(result,sort_keys=True))
