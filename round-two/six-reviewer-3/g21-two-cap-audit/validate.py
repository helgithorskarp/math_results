#!/usr/bin/env python3
import argparse, hashlib, json, os, pathlib, subprocess, sys, time
P=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ)
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:ENV[k]='1'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def run(args,opt=False,success=True):
 cmd=[sys.executable]+(['-O'] if opt else [])+[str(P/'audit.py')]+args
 start=time.monotonic();r=subprocess.run(cmd,capture_output=True,text=True,env=ENV,timeout=45)
 require((r.returncode==0)==success,'unexpected child result: '+r.stdout+r.stderr)
 return {'optimized':opt,'args':args,'exit_code':r.returncode,'seconds':time.monotonic()-start,'stdout':r.stdout.strip(),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();checks=[]
 for opt in [False,True]:
  dest=P/('full-O.json' if opt else 'full.json')
  args=['--output',str(dest)]
  if opt:args+=['--expected',str(P/'full.json')]
  checks.append(run(args,opt))
  for damage in ['candidate','pruning-sign','missing-contact','wrong-cut','missing-triple','sturm-root','endpoint-zero','critical-cancellation','worst-cap2']:
   checks.append(run(['--build-only','--damage',damage,'--output',str(P/'damage-output.json')],opt,False))
 full=json.loads((P/'full.json').read_text());require((P/'full.json').read_bytes()==(P/'full-O.json').read_bytes(),'whole normal/O mismatch')
 triples=full['triples'];require(len(triples)==364,'full364 count')
 leaves=[l for tr in triples if not tr['singular'] for l in tr['leaves']]
 stats={'triples':len(triples),'singular':[t['active'] for t in triples if t['singular']], 'leaves':len(leaves),'norm':sum(l['type']=='norm' for l in leaves),'opposite':sum(l['type']=='opposite violations' for l in leaves),'max_depth':max(len(l['path']) for l in leaves),'generic_identities':len(full['identities']),'core_pairs':len(full['sharpness']['core_pairs']),'full_sha256':hashlib.sha256((P/'full.json').read_bytes()).hexdigest(),'bytes':(P/'full.json').stat().st_size}
 result={'status':'PASS','literal_model_checks':stats,'children':checks,'native_access':'NONE; written original theorem/proof exposed; prior own arithmetic/dual/Sturm reused with credit','resource_scope':'native threads1, external45s each, serial math jobs, no escalation'}
 pathlib.Path(a.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(stats))
if __name__=='__main__':main()
