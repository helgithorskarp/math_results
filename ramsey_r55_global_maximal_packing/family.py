"""Complete maximal-packing tasks, physical carrier indexing, and CNF producer."""
from pathlib import Path
from itertools import combinations
from functools import lru_cache
from math import comb
import argparse,hashlib,json
import base,catalog
PARENT=None

def parent():
 global PARENT
 if PARENT is None:PARENT=base.load()
 return PARENT

def validate(q,r):
 if type(q) is not int or type(r) is not int or not 7<=q<=10 or not 5<=r<=q:raise ValueError('q,r range')

def task_id(q,r,c):return f'mp1-q{q}-r{r}-c{c:06d}'
def parameters(name):
 try:
  prefix,q,r,c=name.split('-');q=int(q[1:]);r=int(r[1:]);c=int(c[1:])
 except (ValueError,TypeError):raise ValueError('task syntax') from None
 validate(q,r)
 s=next(x for x in catalog.specs() if x['n']==43-4*q)
 if prefix!='mp1' or not 0<=c<s['count'] or name!=task_id(q,r,c):raise ValueError('noncanonical task')
 return q,r,c

def per_core(q,r):
 validate(q,r);a=r-1;b=q-r;n=43-4*q
 return 15**(q*n)*1998**a*1931**b*37823**(comb(a,2)+comb(b,2))*35714**(a*b)

def registry():
 rows=[];offset=0
 for q in range(7,11):
  n=43-4*q;s=next(x for x in catalog.specs() if x['n']==n)
  for r in range(5,q+1):
   count=per_core(q,r);end=offset+s['count']*count
   rows.append(dict(q=q,r=r,n=n,core_start=0,core_stop=s['count'],first_task=task_id(q,r,0),last_task=task_id(q,r,s['count']-1),per_task=count,code_start=offset,code_stop=end,physical_variables=903-6*q-comb(n,2),input_sha256=s['sha256']))
   offset=end
 return dict(format='mp1',macro_classes=18,tasks=sum(x['core_stop'] for x in rows),carrier_count=offset,classes=rows)

def locate(index):
 reg=registry()
 if type(index) is not int or not 0<=index<reg['carrier_count']:raise ValueError('global code range')
 for row in reg['classes']:
  if row['code_start']<=index<row['code_stop']:
   core,local=divmod(index-row['code_start'],row['per_task'])
   return task_id(row['q'],row['r'],core),local
 raise ValueError('registry gap')

def global_index(name,local):
 q,r,c=parameters(name);row=next(x for x in registry()['classes'] if (x['q'],x['r'])==(q,r))
 if type(local) is not int or not 0<=local<row['per_task']:raise ValueError('local code range')
 return row['code_start']+c*row['per_task']+local


def mul(a,b):
 return [sum(a[j]*b[k-j] for j in range(len(a)) if 0<=k-j<len(b)) for k in range(min(6,len(a)+len(b)-1))]

class Task:
 def __init__(self,name,cache):
  self.q,self.r,self.c=parameters(name);self.name=name;self.n=43-4*self.q
  self.core=catalog.get(cache,self.n,self.c);self.stats=catalog.statistics(self.core)
  self.blocks=[list(range(4*i,4*i+4)) for i in range(self.q)];self.tail=list(range(4*self.q,43));self.fixed={}
  for i,block in enumerate(self.blocks):
   for e in combinations(block,2):self.fixed[e]=int(i<self.r)
  for i,j in combinations(range(self.n),2):self.fixed[self.tail[i],self.tail[j]]=(self.core[i]>>j)&1
  self.edges=list(combinations(range(43),2));self.variables={e:i+2 for i,e in enumerate(e for e in self.edges if e not in self.fixed)}
  self.pairs=list(combinations(range(self.q),2));self.stars=[(i,v) for i in range(self.q) for v in self.tail]
  self.size=per_core(self.q,self.r)
 @lru_cache(maxsize=None)
 def domain(self,i,j):
  d=parent()['domains'];a='R4' if i<self.r else 'B4';b='R4' if j<self.r else 'B4'
  return d.root_states(b) if i==0 else d.states(a,b)
 def radices(self):return [len(self.domain(i,j)) for i,j in self.pairs]+[15]*len(self.stars)
 def unrank(self,index):
  if type(index) is not int or not 0<=index<self.size:raise ValueError('carrier code range')
  digits=[]
  for radix in reversed(self.radices()):index,d=divmod(index,radix);digits.append(d)
  digits.reverse();a=[[0]*43 for _ in range(43)]
  def put(u,v,c):a[u][v]=a[v][u]=c
  for (u,v),c in self.fixed.items():put(u,v,c)
  for k,(i,j) in enumerate(self.pairs):
   x=self.domain(i,j)[digits[k]]
   for row,u in enumerate(self.blocks[i]):
    for col,v in enumerate(self.blocks[j]):put(u,v,(x>>(4*row+col))&1)
  for d,(i,v) in zip(digits[len(self.pairs):],self.stars):
   x=d if i<self.r else d+1
   for row,u in enumerate(self.blocks[i]):put(u,v,(x>>row)&1)
  return graph(a)
 def rank(self,g):
  a=matrix(g);digits=[]
  for (u,v),c in self.fixed.items():
   if a[u][v]!=c:raise ValueError('fixed core/block mismatch')
  for i,j in self.pairs:
   x=sum(a[u][v]<<(4*row+col) for row,u in enumerate(self.blocks[i]) for col,v in enumerate(self.blocks[j]))
   try:digits.append(self.domain(i,j).index(x))
   except ValueError:raise ValueError('pair/root domain') from None
  for i,v in self.stars:
   x=sum(a[u][v]<<row for row,u in enumerate(self.blocks[i]));d=x if i<self.r else x-1
   if not 0<=d<15:raise ValueError('star domain')
   digits.append(d)
  value=0
  for d,radix in zip(digits,self.radices()):value=value*radix+d
  return value
 def dimensions(self):
  e,tr,tb=self.stats;five=[]
  for color in (1,0):
   poly=[1,self.n,e if color else comb(self.n,2)-e,tr if color else tb,0,0]
   for i in range(self.q):poly=mul(poly,[comb(4,k) for k in range(5)] if int(i<self.r)==color else [1,4])
   five.append(poly[5])
  b=self.q-self.r;extra=256*comb(b,4)+64*self.n*comb(b,3)+16*e*comb(b,2)+4*tr*b
  root=360*(self.q-1)
  return dict(task=self.name,variables=len(self.variables)+1,physical_variables=len(self.variables),red_five=five[0],blue_five=five[1],red_four_closure=extra,root_order=root,clauses=1+root+sum(five)+extra)
 def root_clauses(self):
  for j in range(1,self.q):
   for col in range(3):
    for lo in range(16):
     for hi in range(lo+1,16):
      yield tuple((-1 if value>>row&1 else 1)*self.variables[row,self.blocks[j][c]] for c,value in ((col,lo),(col+1,hi)) for row in range(4))
 def forbid(self,vertices,color):
  pairs=list(combinations(vertices,2))
  if any(self.fixed[e]!=color for e in pairs if e in self.fixed):return None
  return tuple((-1 if color else 1)*self.variables[e] for e in pairs if e in self.variables)
 def clauses(self):
  yield (1,);yield from self.root_clauses()
  for vertices in combinations(range(43),5):
   for color in (1,0):
    clause=self.forbid(vertices,color)
    if clause is not None:yield clause
  for vertices in combinations(range(4*self.r,43),4):
   clause=self.forbid(vertices,1)
   if clause is not None:yield clause
 def write(self,path):
  d=self.dimensions();h=hashlib.sha256();count=0;hist={};path=Path(path)
  with path.open('xb') as f:
   line=f"p cnf {d['variables']} {d['clauses']}\n".encode();f.write(line);h.update(line)
   for clause in self.clauses():
    line=(' '.join(map(str,clause))+' 0\n').encode();f.write(line);h.update(line);count+=1;hist[len(clause)]=hist.get(len(clause),0)+1
  if count!=d['clauses']:raise ValueError('dimension mismatch')
  return dict(**d,sha256=h.hexdigest(),bytes=path.stat().st_size,clause_lengths=hist)
 def closure(self,g):
  a=matrix(g)
  return not any(all(a[u][v] for u,v in combinations(xs,2)) for xs in combinations(range(4*self.r,43),4))

def matrix(g):return parent()['verify_target'].adjacency(g)
def graph(a):return {'n':43,'red_hex':format(sum(a[u][v]<<k for k,(u,v) in enumerate(combinations(range(43),2))),'0226x')}

def transport(g,permutation,task):
 """Check an explicit new-label -> old-label isomorphism certificate.
 Selection/canonical-isomorphism finding is not supplied by this function.
 """
 if len(permutation)!=43 or any(type(v) is not int for v in permutation) or sorted(permutation)!=list(range(43)):raise ValueError('permutation')
 a=matrix(g);out=graph([[a[u][v] for v in permutation] for u in permutation]);code=task.rank(out)
 if not task.closure(out):raise ValueError('red maximality')
 return dict(task=task.name,code=code,graph=out)

def accept_sat(task,path):
 assignments={};status=[]
 for line in Path(path).read_text().splitlines():
  if line.startswith('s '):status.append(line)
  if line.startswith('v '):
   for word in line[2:].split():
    x=int(word)
    if not x:continue
    if abs(x) in assignments and assignments[abs(x)]!=int(x>0):raise ValueError('conflicting assignment')
    assignments[abs(x)]=int(x>0)
 if status!=['s SATISFIABLE'] or set(assignments)!=set(range(1,len(task.variables)+2)) or assignments[1]!=1:raise ValueError('exact complete SAT assignment required')
 a=[[0]*43 for _ in range(43)]
 for u,v in task.edges:a[u][v]=a[v][u]=task.fixed[u,v] if (u,v) in task.fixed else assignments[task.variables[u,v]]
 g=graph(a);task.rank(g)
 if not task.closure(g):raise ValueError('closure violation')
 certificate=parent()['verify_target'].count(g)
 if certificate['status']!='VERIFIED_GOOD43':raise ValueError('physical target rejected')
 return dict(graph=g,certificate=certificate)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('--task');p.add_argument('--cnf');p.add_argument('--code',type=int);p.add_argument('--sat');p.add_argument('--registry',action='store_true');a=p.parse_args()
 catalog.inputs(a.cache)
 if a.registry:print(json.dumps(registry(),indent=2))
 else:
  task=Task(a.task,a.cache)
  if a.cnf:out=task.write(a.cnf)
  elif a.code is not None:out=dict(status='CARRIER_ONLY_NOT_A_TARGET',graph=task.unrank(a.code))
  elif a.sat:out=accept_sat(task,a.sat)
  else:out=task.dimensions()
  print(json.dumps(out,indent=2,sort_keys=True))
