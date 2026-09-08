"""One bounded proof-producing positive chromatic gate on exact VND case10."""
from pathlib import Path
from itertools import combinations
import json,time,threading,hashlib,shutil,resource,os,datetime
from pysat.solvers import Glucose42
import os
P=Path(os.environ.get("VND_WORKDIR",str(Path(__file__).resolve().parent/"work"))).resolve()

def require(x,msg):
 if not x:raise ValueError(msg)
def file_hash(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(2**20),b''):h.update(block)
 return h.hexdigest()
def main():
 require(not (P/'GATE_RESULT.json').exists(),'gate already recorded; do not rerun')
 contract=json.loads((P/'PARAMETERS.json').read_text());geometry=json.loads((P/'source_geometry.json').read_text())
 require(geometry['verified'] and geometry['all_declared_edges_exactly_unit'],'exact source prerequisite')
 resource.setrlimit(resource.RLIMIT_AS,(contract['address_space_bytes'],contract['address_space_bytes']))
 resource.setrlimit(resource.RLIMIT_FSIZE,(contract['proof_file_maximum_bytes'],contract['proof_file_maximum_bytes']))
 edges=json.loads((P/'exact_edges.json').read_text());n=geometry['source_vertices'];tri=[0,1,5];es=set(map(tuple,edges))
 require(all(tuple(sorted((u,v))) in es for u,v in combinations(tri,2)),'sound symmetry triangle');del es
 nc=n+4*len(edges)+3;nv=4*n;count=0
 with Glucose42(with_proof=True,use_timer=True) as solver:
  with (P/'gate.cnf').open('w') as out:
   out.write(f'p cnf {nv} {nc}\n')
   def add(clause):
    nonlocal count
    out.write(' '.join(map(str,clause))+' 0\n');solver.add_clause(clause);count+=1
   for v in range(n):add([4*v+c+1 for c in range(4)])
   for u,v in edges:
    for c in range(4):add([-4*u-c-1,-4*v-c-1])
   for c,v in enumerate(tri):add([4*v+c+1])
  require(count==nc,'clause count')
  cnf_sha=file_hash(P/'gate.cnf');print('ENCODED',n,len(edges),nv,nc,cnf_sha,flush=True)
  stop=threading.Event();start=time.monotonic();reason=[]
  def watchdog():
   last=-1
   while not stop.wait(1):
    elapsed=time.monotonic()-start;size=os.fstat(solver.prfile.fileno()).st_size
    if int(elapsed)//30!=last:
     last=int(elapsed)//30;print('RUNNING',round(elapsed,1),'seconds; proof bytes',size,flush=True)
    if elapsed>=contract['solver_wall_seconds']:
     reason.append('wall_time');solver.interrupt();return
    if size>=contract['proof_file_maximum_bytes']-2**22:
     reason.append('proof_file_size');solver.interrupt();return
  thread=threading.Thread(target=watchdog,daemon=True);thread.start();solver.conf_budget(contract['conflict_budget'])
  answer=solver.solve_limited(expect_interrupt=True);elapsed=time.monotonic()-start;stop.set();thread.join();stats=solver.accum_stats()
  proofname='gate.drat' if answer is False else 'partial_gate.drat'
  solver.prfile.flush();solver.prfile.seek(0)
  with (P/proofname).open('wb') as f:shutil.copyfileobj(solver.prfile,f,2**20)
  if answer is True:
   model=set(x for x in solver.get_model() if x>0);word=[next(c for c in range(4) if 4*v+c+1 in model) for v in range(n)]
   require(all(word[u]!=word[v] for u,v in edges),'decoded word');(P/'colouring.json').write_text(json.dumps(word)+'\n')
  result={'answer':str(answer),'source_vertices':n,'source_edges':len(edges),'variables':nv,'clauses':nc,'triangle':tri,'CNF_sha256':cnf_sha,'solver':'PySAT Glucose42','conflict_budget':contract['conflict_budget'],'solver_wall_budget':contract['solver_wall_seconds'],'elapsed_solver_seconds':elapsed,'interrupt_reason':reason,'statistics':stats,'proof_file':proofname,'proof_bytes':(P/proofname).stat().st_size,'proof_sha256':file_hash(P/proofname),'proof_independently_verified':False,'non_four_colourability_independently_established':False,'record_improvement':False,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  (P/'GATE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
