"""Complete false-SAT models exercise the target rejection boundary."""
from pathlib import Path
import json,tempfile
import carrier,ordered,dependencies

def run(cache):
 rejected=0;clauses_checked=0;families=0
 for triangles in [False,True]:
  name='bo1-q7-r7-c000000';task,plan,meta=ordered.build(name,cache,triangles);graph=carrier.Carrier(name,cache).unrank(0);family=dependencies.load()['family'];a=family.matrix(graph)
  # Five vertices from distinct all-red four-blocks are pairwise blue here.
  witnesses=[0,4,8,12,16]
  if any(a[u][v] for i,u in enumerate(witnesses) for v in witnesses[i+1:]):raise ValueError('negative fixture')
  values={1:1,**{v:a[u][w] for (u,w),v in task.variables.items()}}
  if plan:
   for key,v in plan['variables'].items():values[v]=int(all(values[abs(l)]==int(l>0) for l in plan['inputs'][key]))
  next_var=meta['base_variables']+1
  for i,j in ordered.comparisons(task.q,task.r):
   equal=1
   for bit in range(15,0,-1):
    row,col=divmod(bit,4);equal=int(equal and a[row][4*i+col]==a[row][4*j+col]);values[next_var]=equal;next_var+=1
  if set(values)!=set(range(1,meta['variables']+1)):raise ValueError('complete model fixture')
  for clause in ordered.suffix(task,meta['base_variables']):
   if not any(values[abs(x)]==int(x>0) for x in clause):raise ValueError('valid ordering extension')
   clauses_checked+=1
  body='s SATISFIABLE\nv '+' '.join(str(v if color else -v) for v,color in sorted(values.items()))+' 0\n'
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'model'
   for text in [body,body.replace(' 0\n',' 999999 0\n')]:
    path.write_text(text)
    try:ordered.accept(name,cache,path,triangles)
    except ValueError:rejected+=1
    else:raise ValueError('non-target complete SAT accepted')
  families+=1
 return dict(status='COMPLETE_NON_TARGET_MODELS_REJECTED',encoding_variants=families,models_rejected=rejected,valid_ordering_clauses_checked=clauses_checked)

if __name__=='__main__':
 import sys
 print(json.dumps(run(sys.argv[1]),sort_keys=True))
