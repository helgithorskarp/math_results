"""Bounded single-family runner. UNKNOWN and unchecked statuses prove nothing.
Linux resource limits; use a fresh bulk directory after generating the input.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,os,resource,subprocess,time
ap=argparse.ArgumentParser();ap.add_argument('outdir',type=Path);ap.add_argument('--solver',type=Path,required=True);args=ap.parse_args()
P=args.outdir.resolve();solver=args.solver.resolve()
if (P/'STARTED.json').exists(): raise SystemExit('Use a fresh bulk directory; preserve existing STARTED markers.')
cmd=[str(solver),'--no-binary',str(P/'four_frames.cnf'),str(P/'proof.drat')]
meta=json.load(open(P/'INPUT.json'));start=time.monotonic();wall=1200;proofcap=4*1024**3;memorycap=8*1024**3
out={'status':'STARTED','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'input_sha256':meta['sha256'],'solver_sha256':hashlib.sha256(solver.read_bytes()).hexdigest(),'wall_limit_seconds':wall,'proof_limit_bytes':proofcap,'address_space_limit_bytes':memorycap,'scope':meta['scope'],'new_global_exclusions':0,'terminal_certificates':[]}
(P/'STARTED.json').write_text(json.dumps(out,indent=2)+'\n')
def limits():
 resource.setrlimit(resource.RLIMIT_FSIZE,(proofcap,proofcap));resource.setrlimit(resource.RLIMIT_AS,(memorycap,memorycap));resource.setrlimit(resource.RLIMIT_CPU,(1250,1255))
peak=0;reason=None
with (P/'solver.log').open('wb') as log:
 proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,preexec_fn=limits)
 while proc.poll() is None:
  try:
   for line in Path(f'/proc/{proc.pid}/status').read_text().splitlines():
    if line.startswith('VmHWM:'):peak=max(peak,int(line.split()[1])*1024)
  except FileNotFoundError:pass
  if time.monotonic()-start>=wall:
   reason='PREDECLARED_WALL_LIMIT';proc.terminate()
   try:proc.wait(timeout=10)
   except subprocess.TimeoutExpired:proc.kill();proc.wait()
   break
  time.sleep(1)
 rc=proc.wait()
out.update({'status':'UNSAT_PROOF_REQUIRES_CHECK' if rc==20 else 'SAT_MODEL_REQUIRES_CHECK' if rc==10 else 'UNKNOWN','returncode':rc,'wall_seconds':time.monotonic()-start,'peak_rss_bytes':peak,'stop_reason':reason or 'SOLVER_EXIT','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
for name in ['four_frames.cnf','proof.drat','solver.log']:
 h=hashlib.sha256();f=P/name
 if f.exists():
  with f.open('rb') as src:
   for b in iter(lambda:src.read(1<<20),b''):h.update(b)
  out[name]={'bytes':f.stat().st_size,'sha256':h.hexdigest()}
(P/'RUN.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2),flush=True)
