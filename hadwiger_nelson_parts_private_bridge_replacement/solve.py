from pathlib import Path
from itertools import combinations
import json,subprocess,time,hashlib,datetime
import argparse
import verify
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--kissat',type=Path,required=True);a=ap.parse_args()
if a.out.exists():raise ValueError('output already exists')
a.out.mkdir(parents=True);S=a.out;K=a.kissat.resolve()
points=verify.load_points();verify.provenance(points);n=len(points)
edges=[(i,j) for i,j in combinations(range(n),2) if verify.unit(points[i],points[j])];out={}
version=subprocess.check_output([str(K),'--version'],text=True).strip()
for k in (5,4):
 clauses=[]
 for v in range(n):
  clauses.append([k*v+c+1 for c in range(k)])
  clauses.extend([-(k*v+a+1),-(k*v+b+1)] for a,b in combinations(range(k),2))
 for v,w in edges:clauses.extend([-(k*v+c+1),-(k*w+c+1)] for c in range(k))
 data=f'p cnf {k*n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
 cnf=S/f'colour{k}.cnf';cnf.write_text(data);start=time.monotonic();log=S/f'colour{k}.log'
 limit=60 if k==5 else 120
 try:
  with log.open('w') as f:p=subprocess.run([str(K),f'--time={limit}',str(cnf)],stdout=f,stderr=subprocess.STDOUT,timeout=limit+10)
  status={10:'SAT',20:'UNSAT'}.get(p.returncode,'UNKNOWN')
 except subprocess.TimeoutExpired:status='UNKNOWN'
 seconds=time.monotonic()-start
 item={'status':status,'seconds':seconds,'variables':k*n,'clauses':len(clauses),'cnf_sha256':hashlib.sha256(data.encode()).hexdigest(),'solver_version':version,'solver_sha256':hashlib.sha256(K.read_bytes()).hexdigest(),'wall_cap_seconds':limit,'pins':[]}
 if status=='SAT':
  values={int(x) for l in log.read_text().splitlines() if l.startswith('v ') for x in l[2:].split() if int(x)>0}
  word=[]
  for v in range(n):
   colors=[c for c in range(k) if k*v+c+1 in values]
   if len(colors)!=1:raise ValueError('model domain')
   word.append(colors[0])
  if any(word[v]==word[w] for v,w in edges):raise ValueError('bad colour edge')
  (S/f'colour{k}.txt').write_text(''.join(map(str,word))+'\n');item.update({'direct_edge_checks':len(edges),'colours_used':len(set(word)),'word_sha256':hashlib.sha256((S/f'colour{k}.txt').read_bytes()).hexdigest()})
 out[str(k)]=item;(S/'solver_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'k':k,**item}),flush=True)
 if k==5 and status!='SAT':break
print('FINISHED',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
