"""Optional bounded witness rediscovery; proof replay does not need a solver."""
from pathlib import Path
from itertools import combinations
import argparse,json,sys,time
import pysat
from pysat.solvers import Cadical195
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
w=args.out;w.mkdir(parents=True,exist_ok=False);repo=Path(__file__).resolve().parent.parent
data={key:json.loads((args.work/f'graph{key}.json').read_text()) for key in ['159','214']}
rows=(repo/'hadwiger_nelson_nonmono159_moser_triple/colors_A.txt').read_text().splitlines()
ports={'159':[141,142,144],'214':[186,187]};patterns={'159':['001','010','011','012'],'214':['01']}
cert={};transcript=[];started=time.perf_counter()
for key in patterns:
 g=data[key];n=len(g['points']);ee=g['edges'];records=[]
 for pat in patterns[key]:
  source=None;row=None
  if key=='159':
   for i,s in enumerate(rows):
    seen=[];canon=[]
    for v in ports[key]:
     c=int(s[v])
     if c not in seen:seen.append(c)
     canon.append(seen.index(c))
    if ''.join(map(str,canon))==pat:
     seen+=sorted(set(range(4))-set(seen));mapping={c:j for j,c in enumerate(seen)};row=[mapping[int(c)] for c in s];source={'kind':'prior_library','row':i};break
  if row is None:
   cnf=[]
   for v in range(n):
    cnf.append([4*v+c+1 for c in range(4)])
    cnf += [[-4*v-c-1,-4*v-d-1] for c,d in combinations(range(4),2)]
   for a,b in ee:cnf.extend([[-4*a-c-1,-4*b-c-1] for c in range(4)])
   assumptions=[4*v+int(c)+1 for v,c in zip(ports[key],pat)]
   start=time.perf_counter()
   with Cadical195(bootstrap_with=cnf) as sat:
    sat.conf_budget(100000);status=sat.solve_limited(assumptions=assumptions);stats=sat.accum_stats()
    assert status is True,('incomplete positive-pattern milestone',key,pat,status)
    model=set(x for x in sat.get_model() if x>0);row=[next(c for c in range(4) if 4*v+c+1 in model) for v in range(n)]
   source={'kind':'native','variables':4*n,'clauses':len(cnf),'assumptions':assumptions,'seconds':time.perf_counter()-start,'stats':stats}
  assert len(row)==n and all(0<=c<4 for c in row) and all(row[a]!=row[b] for a,b in ee)
  assert ''.join(str(row[v]) for v in ports[key])==pat
  records.append({'pattern':pat,'colours':''.join(map(str,row))});transcript.append({'gadget':key,'pattern':pat,'source':source})
 cert[key]={'terminals':ports[key],'extensions':records}
(w/'certificate.json').write_text(json.dumps(cert,separators=(',',':'))+'\n')
(w/'discovery.json').write_text(json.dumps({'python':sys.version,'pysat':pysat.__version__,'solver':'CaDiCaL1.9.5','max_conflicts_per_native_call':100000,'native_calls':sum(r['source']['kind']=='native' for r in transcript),'seconds':time.perf_counter()-started,'transcript':transcript},indent=2)+'\n')
print(json.dumps({'all_patterns_have_checked_extensions':True,'patterns':5,'native_calls':sum(r['source']['kind']=='native' for r in transcript),'seconds':time.perf_counter()-started},indent=2))
