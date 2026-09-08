"""Audit every existing CNF clause directly against the raw author graph."""
from pathlib import Path
from itertools import combinations
import json,hashlib,time
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve()

def require(x,msg):
 if not x:raise ValueError(msg)
def main():
 start=time.monotonic();rows=(P/'source_graph.dimacs').read_text().splitlines();header=rows.pop(0).split();require(header==['p','edge','64513','542472'],'author header')
 es=[]
 for row in rows:
  a=row.split();require(len(a)==3 and a[0]=='e','author edge syntax');u,v=sorted(int(x)-1 for x in a[1:]);require(0<=u<v<64513,'edge labels');es.append((u,v))
 es.sort();require(len(es)==len(set(es))==542472,'author edge count');tri=[0,1,5];require(set(combinations(tri,2))<=set(es),'triangle')
 n=64513;nc=n+4*len(es)+3;count=0
 with (P/'gate.cnf').open() as f:
  require(f.readline().split()==['p','cnf',str(4*n),str(nc)],'CNF header')
  def take(want):
   nonlocal count
   got=[int(x) for x in f.readline().split()];require(got==want+[0],'CNF clause '+str(count));count+=1
  for v in range(n):take([4*v+1,4*v+2,4*v+3,4*v+4])
  for u,v in es:
   for c in range(4):take([-(4*u+c+1),-(4*v+c+1)])
  for c,v in enumerate(tri):take([4*v+c+1])
  require(not f.read(),'no extra CNF syntax');require(count==nc,'CNF count')
 h=hashlib.sha256()
 with (P/'gate.cnf').open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 out={'verified':True,'raw_author_edge_count':len(es),'clause_lines_verified':count,'variables':4*n,'clauses':nc,'independent_raw_graph_to_CNF_mapping':True,'at_most_one_clauses_required':False,'symmetry_triangle':tri,'CNF_sha256':h.hexdigest(),'elapsed_seconds':time.monotonic()-start}
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
