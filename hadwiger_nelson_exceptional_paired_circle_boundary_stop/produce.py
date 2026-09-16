from pathlib import Path
from itertools import combinations
import argparse,json,subprocess,time,hashlib
from geometry import construct,need,raw
p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',type=Path,required=True);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False)
t=time.monotonic();g,points,edges,s=construct();s['geometry_seconds']=time.monotonic()-t
n=len(points);cls=[]
for i in range(n):
 vs=[4*i+c+1 for c in range(4)];cls.append(vs);cls.extend([[-a,-b] for a,b in combinations(vs,2)])
for i,j in edges:cls.extend([[-(4*i+c+1),-(4*j+c+1)] for c in range(4)])
cls.append([1]);cnf=f'p cnf {4*n} {len(cls)}\n'+''.join(' '.join(map(str,x))+' 0\n' for x in cls);(a.work/'input.cnf').write_text(cnf)
s.update(cnf_variables=4*n,cnf_clauses=len(cls),cnf_sha256=hashlib.sha256(cnf.encode()).hexdigest())
(a.work/'GEOMETRY.json').write_text(json.dumps(s,indent=2)+'\n');(a.work/'QUERY_STARTED').write_text('One frozen ordinary four query\n')
t=time.monotonic();r=subprocess.run([str(a.kissat.resolve()),'--time=60','--conflicts=1000000','--no-binary',str((a.work/'input.cnf').resolve()),str((a.work/'proof.drat').resolve())],text=True,capture_output=True,timeout=90);s['solver_seconds']=time.monotonic()-t;s['solver_exit']=r.returncode
(a.work/'solver.stdout').write_text(r.stdout);(a.work/'solver.stderr').write_text(r.stderr)
if r.returncode==10:
 pos={int(x) for l in r.stdout.splitlines() if l.startswith('v ') for x in l[2:].split() if int(x)>0};word=[]
 for i in range(n):
  cs=[c for c in range(4) if 4*i+c+1 in pos];need(len(cs)==1,'one colour');word.append(cs[0])
 need(all(word[i]!=word[j] for i,j in edges),'complete proper4');four=''.join(map(str,word));five='4'+four[1:]
 cert={'four_word':four,'five_word':five,'vertices':n,'edges':len(edges),'coordinate_sha256':s['coordinate_sha256'],'edge_sha256':s['edge_sha256']};(a.work/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n');s['status']='SAT_checked_four_word'
else:s['status']='UNSAT_unchecked' if r.returncode==20 else 'UNKNOWN'
s['record_certified']=False;(a.work/'RESULT.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps({k:v for k,v in s.items() if k!='kernel_ids'},indent=2))
