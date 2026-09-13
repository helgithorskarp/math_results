from geometry51 import *
import subprocess

def run(tag):
 st=time.time();h=json.loads((W/f'host_edges_{tag}.json').read_text());n=490+len(h['new_point_ids']);es=h['edges'];adj=[set()for _ in range(n)]
 for a,b in es:adj[a].add(b);adj[b].add(a)
 tri=next((a,b,min(adj[a]&adj[b]))for a,b in es if adj[a]&adj[b]);cnf=W/f'host_{tag}.cnf';proof=W/f'host_{tag}.drat';log=W/f'kissat_{tag}.log'
 with cnf.open('w')as out:
  out.write(f'p cnf {4*n} {n+4*len(es)+3}\n')
  for v in range(n):out.write(' '.join(str(4*v+c+1)for c in range(4))+' 0\n')
  for a,b in es:
   for c in range(4):out.write(f'{-4*a-c-1} {-4*b-c-1} 0\n')
  for c,v in enumerate(tri):out.write(f'{4*v+c+1} 0\n')
 with log.open('w')as out:r=subprocess.run([os.environ.get('HN_KISSAT','kissat'),'--time=180',str(cnf),str(proof)],stdout=out,stderr=subprocess.STDOUT)
 result={'tag':tag,'vertices':n,'edges':len(es),'solver_exit':r.returncode,'status':'UNSAT_signal'if r.returncode==20 else'SAT_signal'if r.returncode==10 else'UNKNOWN','seconds':time.time()-st,'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest()}
 if r.returncode==20:
  with (W/f'drat_{tag}.log').open('w')as out:q=subprocess.run([os.environ.get('HN_DRAT_TRIM','drat-trim'),str(cnf),str(proof)],stdout=out,stderr=subprocess.STDOUT)
  checked='s VERIFIED'in(W/f'drat_{tag}.log').read_text();require(q.returncode==0 and checked,'refutation failed');result.update(status='verified_not_four',proof_bytes=proof.stat().st_size,proof_sha256=hashlib.sha256(proof.read_bytes()).hexdigest())
 (W/f'native_host_{tag}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':run(sys.argv[1])
