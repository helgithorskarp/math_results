"""Complete per-task CNFs: exact whole-block order, optional shared triangles."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json
import dependencies,carrier

def comparisons(q,r):
 return list(zip(range(1,r-1),range(2,r)))+list(zip(range(r,q-1),range(r+1,q)))

def lex_clauses(left,right,first):
 """Unsigned words; lists run most significant bit first. Constant 1 is true."""
 if not left or len(left)!=len(right):raise ValueError('word lengths')
 prefix=1;next_variable=first
 for i,(x,y) in enumerate(zip(left,right)):
  yield (-prefix,x,-y)
  if i+1<len(left):
   z=next_variable;next_variable+=1
   yield (-z,prefix);yield (-z,-x,y);yield (-z,x,-y)
   yield (z,-prefix,x,y);yield (z,-prefix,-x,-y)
   prefix=z

def suffix(task,base_variables):
 first=base_variables+1
 for left,right in comparisons(task.q,task.r):
  words=[[task.variables[row,4*block+col] for row in reversed(range(4)) for col in reversed(range(4))] for block in (left,right)]
  yield from lex_clauses(*words,first);first+=15

def build(name,cache,triangles=False):
 modules=dependencies.load();task=modules['family'].Task(carrier.parent_name(name),cache)
 plan=modules['factor'].plan(task) if triangles else None
 base_variables=max(plan['variables'].values()) if triangles else len(task.variables)+1
 base_clauses=task.dimensions()['clauses']+(sum(len(x)+1 for x in plan['inputs'].values()) if triangles else 0)
 pairs=comparisons(task.q,task.r);meta=dict(task=name,triangles=triangles,physical_variables=len(task.variables),variables=base_variables+15*len(pairs),clauses=base_clauses+91*len(pairs),ordering_comparisons=len(pairs),ordering_variables=15*len(pairs),ordering_clauses=91*len(pairs),base_variables=base_variables,base_clauses=base_clauses)
 return task,plan,meta

def clauses(task,plan,meta):
 if plan is None:yield from task.clauses()
 else:
  for _,clause in dependencies.load()['factor'].clauses(task,plan):yield clause
 yield from suffix(task,meta['base_variables'])

def write(name,cache,path,triangles=False):
 task,plan,meta=build(name,cache,triangles);h=hashlib.sha256();size=0;count=0;width=0;path=Path(path)
 with path.open('xb') as f:
  line=f"p cnf {meta['variables']} {meta['clauses']}\n".encode();f.write(line);h.update(line);size+=len(line)
  for clause in clauses(task,plan,meta):
   line=(' '.join(map(str,clause))+' 0\n').encode();f.write(line);h.update(line);size+=len(line);count+=1;width=max(width,len(clause))
 if count!=meta['clauses']:raise ValueError('clause dimensions')
 return dict(**meta,bytes=size,sha256=h.hexdigest(),max_width=width)

def accept(name,cache,path,triangles=False):
 task,plan,meta=build(name,cache,triangles);values={};statuses=[]
 for line in Path(path).read_text().splitlines():
  if line.startswith('s '):statuses.append(line)
  if line.startswith('v '):
   for item in line[2:].split():
    literal=int(item)
    if literal==0:continue
    v=abs(literal);color=int(literal>0)
    if v in values and values[v]!=color:raise ValueError('conflicting assignment')
    values[v]=color
 if statuses!=['s SATISFIABLE'] or set(values)!=set(range(1,meta['variables']+1)) or values[1]!=1:raise ValueError('complete exact SAT assignment required')
 for clause in clauses(task,plan,meta):
  if not any(values[abs(x)]==int(x>0) for x in clause):raise ValueError('unsatisfied full formula')
 a=[[0]*43 for _ in range(43)]
 for u,v in combinations(range(43),2):a[u][v]=a[v][u]=task.fixed[u,v] if (u,v) in task.fixed else values[task.variables[u,v]]
 family=dependencies.load()['family'];graph=family.graph(a);code=carrier.Carrier(name,cache).rank(graph);certificate=family.parent()['verify_target'].count(graph)
 if certificate['status']!='VERIFIED_GOOD43':raise ValueError('physical target rejected')
 return dict(status='VERIFIED_GOOD43',graph=graph,certificate=certificate,task=name,carrier_code=code)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('--task',required=True);p.add_argument('--cnf');p.add_argument('--triangles',action='store_true');p.add_argument('--sat');a=p.parse_args()
 out=accept(a.task,a.cache,a.sat,a.triangles) if a.sat else write(a.task,a.cache,a.cnf,a.triangles) if a.cnf else build(a.task,a.cache,a.triangles)[2]
 print(json.dumps(out,indent=2,sort_keys=True))
