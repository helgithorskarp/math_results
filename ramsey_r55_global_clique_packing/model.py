"""Physical graphs and complete target CNFs for the unconditional packing cover."""
from itertools import combinations
from pathlib import Path
import argparse,hashlib,json
import census,domains

class Packing:
 def __init__(self,branch):
  self.types=census.kinds(branch);self.branch=list(branch);self.blocks=[];offset=0
  for kind in self.types:
   n,_=domains.TYPES[kind];self.blocks.append(list(range(offset,offset+n)));offset+=n
  if offset!=43:raise ValueError('vertex partition')
  self.fixed={};self.owner={v:i for i,b in enumerate(self.blocks) for v in b}
  for kind,block in zip(self.types,self.blocks):
   for (i,j),color in domains.inside(kind).items():self.fixed[block[i],block[j]]=color
  self.pairs=list(combinations(range(43),2));self.variables={p:k+2 for k,p in enumerate(p for p in self.pairs if p not in self.fixed)}
  if len(self.fixed)!=57 or len(self.variables)!=846:raise ValueError('physical edge partition')
  self.matrix_pairs=list(combinations(range(12),2))
  self.physical_positions={p:k for k,p in enumerate(self.pairs)}

 def check_matrices(self,matrices,require_domains=True):
  if not isinstance(matrices,list) or len(matrices)!=66:raise ValueError('exactly 66 matrices required')
  for x,(i,j) in zip(matrices,self.matrix_pairs):
   if type(x) is not int or not 0<=x<2**(len(self.blocks[i])*len(self.blocks[j])):raise ValueError('matrix bit width')
   if require_domains and x not in self.matrix_domain(i,j):raise ValueError('forbidden or noncanonical matrix')

 def matrix_domain(self,i,j):
  return domains.root_states(self.types[j]) if i==0 else domains.states(self.types[i],self.types[j])

 def root_clauses(self):
  for j in range(1,12):
   for a,b in domains.comparable_columns(self.types[j]):
    for left in range(16):
     for right in range(left+1,16):
      clause=[]
      for position,value in [(a,left),(b,right)]:
       for row in range(4):
        variable=self.variables[self.blocks[0][row],self.blocks[j][position]]
        clause.append(-variable if value>>row&1 else variable)
      yield tuple(clause)

 def graph(self,matrices,require_domains=True):
  self.check_matrices(matrices,require_domains);bits=sum(c<<self.physical_positions[p] for p,c in self.fixed.items())
  for x,(i,j) in zip(matrices,self.matrix_pairs):
   for a,u in enumerate(self.blocks[i]):
    for b,v in enumerate(self.blocks[j]):bits|=((x>>(a*len(self.blocks[j])+b))&1)<<self.physical_positions[u,v]
  return {'n':43,'red_hex':format(bits,'0226x')}

 def extract(self,matrix,require_domains=True):
  if len(matrix)!=43 or any(len(row)!=43 for row in matrix):raise ValueError('physical graph size')
  for p,c in self.fixed.items():
   if matrix[p[0]][p[1]]!=c:raise ValueError('internal block mismatch')
  result=[]
  for i,j in self.matrix_pairs:
   x=0
   for a,u in enumerate(self.blocks[i]):
    for b,v in enumerate(self.blocks[j]):x|=matrix[u][v]<<(a*len(self.blocks[j])+b)
   result.append(x)
  self.check_matrices(result,require_domains);return {'branch':self.branch,'matrices':result}

 def five_clauses(self,q):
  ps=list(combinations(q,2))
  for color in (1,0):
   if any(self.fixed[p]!=color for p in ps if p in self.fixed):continue
   yield tuple((-1 if color else 1)*self.variables[p] for p in ps if p in self.variables)

 def clauses(self):
  yield (1,)
  yield from self.root_clauses()
  for q in combinations(range(43),5):yield from self.five_clauses(q)

 def write(self,path):
  path=Path(path)
  if path.exists():raise ValueError('refusing to overwrite CNF')
  red=census.polynomial_clauses(self.types,1);blue=census.polynomial_clauses(self.types,0)
  ordering=120*sum(len(domains.comparable_columns(kind)) for kind in self.types[1:]);wanted=red+blue+ordering+1
  h=hashlib.sha256();hist={};count=0
  with path.open('wb') as f:
   line=f'p cnf 847 {wanted}\n'.encode();f.write(line);h.update(line)
   for clause in self.clauses():
    line=(' '.join(map(str,clause))+' 0\n').encode();f.write(line);h.update(line);count+=1;hist[len(clause)]=hist.get(len(clause),0)+1
  if count!=wanted:raise ValueError('actual clause count disagrees with polynomial')
  return {'branch':self.branch,'variables':847,'clauses':count,'red_clauses':red,'blue_clauses':blue,'root_order_clauses':ordering,'bytes':path.stat().st_size,'sha256':h.hexdigest(),'clause_lengths':hist}

def parse(data):
 if not isinstance(data,dict) or set(data)!={'branch','matrices'}:raise ValueError('exact packing fields required')
 p=Packing(data['branch']);p.check_matrices(data['matrices']);return p

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--data');p.add_argument('--branch');p.add_argument('--cnf');p.add_argument('--graph-output')
 a=p.parse_args()
 if a.data:
  data=json.loads(Path(a.data).read_text());packing=parse(data);graph=packing.graph(data['matrices'])
  if a.graph_output:
   out=Path(a.graph_output)
   if out.exists():raise ValueError('output exists')
   out.write_text(json.dumps(graph,indent=2,sort_keys=True)+'\n')
  print(json.dumps({'status':'ROOTED_PACKING_SURVIVOR_ONLY','graph':graph},sort_keys=True))
 elif a.branch and a.cnf:print(json.dumps(Packing(list(map(int,a.branch.split(',')))).write(a.cnf),sort_keys=True))
 else:p.error('provide --data or --branch with --cnf')
