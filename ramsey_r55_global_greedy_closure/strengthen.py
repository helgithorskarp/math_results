"""Complete physical good43 CNFs with greedy-packing residual closure."""
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json
import base

def allowed(branch):
 return isinstance(branch,list) and len(branch)==3 and all(type(x) is int for x in branch) and branch[0] in (5,6,7) and branch[1] in (1,2,3,4) and branch[2] in range(4) and (branch[1]==4 or branch[2]<3)

def unions(packing):
 r,s,t=packing.branch
 if not allowed(packing.branch):raise ValueError('Not one of the39 complete normalized branches')
 result=[]
 if r<7:result.append((4,[v for block in packing.blocks[r:] for v in block]))
 if s<4:result.append((3,[v for block in packing.blocks[7+s:] for v in block]))
 return result

def extra_clauses(packing):
 for size,vertices in unions(packing):
  for q in combinations(vertices,size):
   pairs=list(combinations(q,2))
   if any(packing.fixed[p]==0 for p in pairs if p in packing.fixed):continue
   clause=tuple(-packing.variables[p] for p in pairs if p in packing.variables)
   if not clause:raise ValueError('Fixed clique violates normal form')
   yield clause

def stats(packing):
 result={4:{'subsets':0,'clauses':0,'across_three_or_more_blocks':0},3:{'subsets':0,'clauses':0,'across_three_or_more_blocks':0}}
 for size,vertices in unions(packing):
  for q in combinations(vertices,size):
   result[size]['subsets']+=1
   if any(packing.fixed[p]==0 for p in combinations(q,2) if p in packing.fixed):continue
   result[size]['clauses']+=1
   if len({packing.owner[v] for v in q})>=3:result[size]['across_three_or_more_blocks']+=1
 return result

def clauses(packing):
 if not allowed(packing.branch):raise ValueError('Branch rejected by global normal form')
 yield from packing.clauses()
 yield from extra_clauses(packing)

def write(packing,path):
 path=Path(path)
 if path.exists():raise ValueError('Output already exists')
 extras=list(extra_clauses(packing));parent=sum(1 for _ in packing.clauses());expected=parent+len(extras);h=hashlib.sha256();actual=0
 with path.open('wb') as f:
  line=f'p cnf 847 {expected}\n'.encode();f.write(line);h.update(line)
  for c in clauses(packing):
   line=(' '.join(map(str,c))+' 0\n').encode();f.write(line);h.update(line);actual+=1
 if actual!=expected:raise ValueError('Clause count')
 return {'branch':packing.branch,'variables':847,'parent_clauses':parent,'extra_clauses':len(extras),'clauses':actual,'bytes':path.stat().st_size,'sha256':h.hexdigest(),'extra_statistics':stats(packing)}

def check_closure(matrix,packing):
 for size,vertices in unions(packing):
  for q in combinations(vertices,size):
   if all(matrix[u][v] for u,v in combinations(q,2)):return {'size':size,'vertices':list(q)}
 return None

def normalize(graph,parent):
 result=parent['normalize'].normalize(graph)
 if not allowed(result['parameters']['branch']):raise ValueError('Greedy normalization failed; input cannot be certified good43')
 packing=parent['model'].Packing(result['parameters']['branch']);matrix=parent['verify_target'].adjacency(result['graph'])
 if check_closure(matrix,packing) is not None:raise ValueError('Greedy closure violation')
 result['greedy_closure_holds']=True;return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--base',type=Path);p.add_argument('--branch');p.add_argument('--cnf',type=Path);p.add_argument('--normalize',type=Path);a=p.parse_args();parent=base.load(a.base)
 if a.normalize:print(json.dumps(normalize(json.loads(a.normalize.read_text()),parent),sort_keys=True))
 elif a.branch and a.cnf:print(json.dumps(write(parent['model'].Packing(list(map(int,a.branch.split(',')))),a.cnf),sort_keys=True))
 else:p.error('provide --branch/--cnf or --normalize')
