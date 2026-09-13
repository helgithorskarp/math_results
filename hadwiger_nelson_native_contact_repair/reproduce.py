#!/usr/bin/env python3
"""Regenerate geometry and check a fresh four-colour UNSAT refutation."""
from pathlib import Path
from hashlib import sha256
import argparse,json,subprocess,time
import verify

def digest(path):
 h=sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);p.add_argument('--kissat',required=True);p.add_argument('--drat-trim',required=True);p.add_argument('--seconds',type=int,default=600);a=p.parse_args();a.work.mkdir(parents=True,exist_ok=True)
 geometry=verify.verify(a.work,Path(__file__).with_name('certificate.json'));cnf=a.work/'selected.cnf';proof=a.work/'selected.drat';t=time.monotonic()
 with (a.work/'kissat.log').open('w') as f:r=subprocess.run([a.kissat,f'--time={a.seconds}',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
 if r.returncode!=20:raise RuntimeError('no UNSAT certificate: native exit '+str(r.returncode))
 with (a.work/'drat-check.log').open('w') as f:r=subprocess.run([a.drat_trim,str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT)
 if r.returncode!=0 or 's VERIFIED' not in (a.work/'drat-check.log').read_text():raise RuntimeError('refutation not verified')
 result={'status':'CERTIFIED CHROMATIC NUMBER FIVE','selected_vertices':geometry['selected']['vertices'],'selected_edges':geometry['selected']['edges'],'cnf_sha256':digest(cnf),'proof_sha256':digest(proof),'proof_bytes':proof.stat().st_size,'proof_seconds':time.monotonic()-t}
 (a.work/'proof-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
