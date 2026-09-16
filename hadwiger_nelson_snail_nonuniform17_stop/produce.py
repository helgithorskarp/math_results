"""One frozen geometry; one bounded ordinary-four query. Expanded files external."""
from pathlib import Path
import argparse, hashlib, json, subprocess, time
from itertools import combinations
from geometry import HERE,F,reconstruct,geometry_hash,edge_hash
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',type=Path,required=True);a=p.parse_args()
a.work.mkdir(parents=True,exist_ok=False);started=time.monotonic()
s,gs,fs,points,addresses,edges,false=reconstruct();geometry_seconds=time.monotonic()-started
n=len(points);clauses=[]
for i in range(n):
 vs=[4*i+c+1 for c in range(4)];clauses.append(vs)
 clauses.extend([[-x,-y] for x,y in combinations(vs,2)])
for i,j in edges:
 clauses.extend([[-(4*i+c+1),-(4*j+c+1)] for c in range(4)])
# First vertex can always be assigned colour zero by a global permutation.
clauses.append([1]);cnf=f'p cnf {4*n} {len(clauses)}\n'+''.join(' '.join(map(str,r))+' 0\n' for r in clauses)
(a.work/'input.cnf').write_text(cnf);(a.work/'QUERY_STARTED').write_text('One frozen ordinary-four decision\n')
command=[str(a.kissat.resolve()),'--time=60','--conflicts=1000000','--no-binary',str((a.work/'input.cnf').resolve()),str((a.work/'proof.drat').resolve())]
begin=time.monotonic();r=subprocess.run(command,text=True,capture_output=True,timeout=90);solver_seconds=time.monotonic()-begin
(a.work/'solver.stdout').write_text(r.stdout);(a.work/'solver.stderr').write_text(r.stderr)
base={'copies':len(fs),'formal_addresses':493,'physical_vertices':n,'strict_edges':len(edges),'pair_count':n*(n-1)//2,'modular_false_edges':false,'coordinate_sha256':geometry_hash(points),'edge_sha256':edge_hash(edges),'cnf_sha256':hashlib.sha256(cnf.encode()).hexdigest(),'cnf_variables':4*n,'cnf_clauses':len(clauses),'solver_exit':r.returncode,'geometry_seconds':geometry_seconds,'solver_seconds':solver_seconds,'solver_command':command,'solver_sha256':hashlib.sha256(a.kissat.read_bytes()).hexdigest()}
if r.returncode==10:
 positive={int(x) for line in r.stdout.splitlines() if line.startswith('v ') for x in line[2:].split() if int(x)>0}
 cols=[]
 for i in range(n):
  cs=[c for c in range(4) if 4*i+c+1 in positive];F.need(len(cs)==1,'one selected colour');cols.append(cs[0])
 F.need(all(cols[i]!=cols[j] for i,j in edges),'positive complete-graph word')
 word=''.join(map(str,cols));five='4'+word[1:]
 F.need(set(word)==set('0123') and set(five)==set('01234'),'word alphabets')
 cert={'four_word':word,'five_word':five,'coordinate_sha256':geometry_hash(points),'edge_sha256':edge_hash(edges),'physical_vertices':n,'strict_edges':len(edges)}
 (a.work/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n');base.update(status='SAT_checked_four_word',record_certified=False)
else:base.update(status='UNSAT_unchecked' if r.returncode==20 else 'UNKNOWN',record_certified=False)
(a.work/'RESULT.json').write_text(json.dumps(base,indent=2)+'\n');print(json.dumps(base,indent=2))
