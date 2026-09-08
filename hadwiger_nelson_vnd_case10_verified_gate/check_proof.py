"""Check an existing fixed-source refutation; never call a SAT solver."""
from pathlib import Path
import argparse,subprocess,resource,time,json,hashlib

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
def limits():resource.setrlimit(resource.RLIMIT_AS,(8*2**30,8*2**30))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--checkers',type=Path,required=True);ap.add_argument('--lrat-only',action='store_true');a=ap.parse_args();w=a.work.resolve();c=a.checkers.resolve()
 expected='aa4305ebd561a52e89fe77738deee93c53f0c062a7715b879a51d0ada69b3bef'
 if digest(w/'gate.cnf')!=expected:raise ValueError('fixed CNF hash mismatch')
 results=[]
 def run(cmd,log,accept):
  start=time.monotonic()
  with (w/log).open('w') as f:r=subprocess.run([str(x) for x in cmd],stdout=f,stderr=subprocess.STDOUT,preexec_fn=limits,timeout=1830)
  if r.returncode!=0 or accept not in (w/log).read_text().splitlines():raise ValueError('proof checker rejected or did not finish; see '+log)
  results.append({'checker':Path(cmd[0]).name,'checker_sha256':digest(Path(cmd[0])),'returncode':r.returncode,'elapsed_seconds':time.monotonic()-start,'acceptance_line':accept})
 if not a.lrat_only:
  run([c/'drat-trim',w/'gate.cnf',w/'gate.drat','-l',w/'gate.trimmed.drat','-L',w/'gate.lrat','-t','1800'],'drat_verification.log','s VERIFIED')
 strict=w/'strict_lrat'
 subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',str(Path(__file__).resolve().parent/'strict_lrat.cpp'),'-o',str(strict)],check=True)
 run([strict,w/'gate.cnf',w/'gate.lrat'],'strict_lrat_verification.log','VERIFIED_STRICT_RUP_LRAT')
 out={'verified':True,'status':'VERIFIED_VND_CASE10_FULL_LRAT_REFUTATION','CNF_sha256':expected,'LRAT_bytes':(w/'gate.lrat').stat().st_size,'LRAT_sha256':digest(w/'gate.lrat'),'checker_results':results,'source_vertices':64513,'non_four_colourability':True,'exactly_five_chromatic_claimed':False,'physical_core_extraction_performed':False,'target_508_found':False}
 (w/'PROOF_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
