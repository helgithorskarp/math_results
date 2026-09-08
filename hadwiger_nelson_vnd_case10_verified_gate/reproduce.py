"""Audit the fixed source; proof regeneration is explicit and separately capped."""
from pathlib import Path
import argparse,subprocess,sys,os,json,shutil
S=Path(__file__).resolve().parent

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,default=S/'work');ap.add_argument('--solve',action='store_true',help='explicitly run the one capped four-colour query after geometry');args=ap.parse_args();w=args.work.resolve();w.mkdir(parents=True,exist_ok=True);env=dict(os.environ,VND_WORKDIR=str(w))
 for name in ['UPSTREAM_INPUTS.json','SIEVE_CONSTANTS.json','interface_profile.json','PARAMETERS.json']:
  out=w/name;raw=(S/name).read_bytes()
  if out.exists() and out.read_bytes()!=raw:raise ValueError('refuse overwrite of different '+name)
  if not out.exists():out.write_bytes(raw)
 def run(cmd,out=None):
  print('RUN',Path(cmd[0]).name,' '.join(str(x) for x in cmd[1:]),flush=True)
  if out:
   with (w/out).open('w') as f:subprocess.run(list(map(str,cmd)),env=env,stdout=f,check=True)
  else:subprocess.run(list(map(str,cmd)),env=env,check=True)
 def py(name,*args,out=None):run([sys.executable,S/name,*args],out)
 py('reproduce_inputs.py','fetch');py('audit_source.py',out='source_geometry.log');py('independent_geometry.py',out='independent_geometry.json');py('reproduce_inputs.py','residues')
 run(['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',S/'strict_sieve.cpp','-o',w/'strict_sieve'])
 run(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-omit-frame-pointer','-Wall','-Wextra','-pedantic',S/'strict_sieve.cpp','-o',w/'strict_sieve_sanitized'])
 run([w/'strict_sieve',w/'residues.tsv','2000',w/'sieve_pilot.bin'],'sieve_pilot.json');py('validate_sieve.py',out='sieve_controls.log')
 run([w/'strict_sieve',w/'residues.tsv','64513',w/'full_sieve.bin'],'full_sieve.json');py('finish_census.py',out='strict_census.log');py('controls_and_profile.py',out='controls_and_profile.json')
 py('write_cnf.py');py('audit_cnf.py',out='independent_CNF_audit.json')
 required={'source_geometry.json':'verified','independent_geometry.json':'verified','sieve_controls.json':'verified','strict_census.json':'verified','controls_and_profile.json':'verified','independent_CNF_audit.json':'verified'}
 for name,key in required.items():
  if json.loads((w/name).read_text())[key] is not True:raise ValueError('unverified '+name)
 print('VERIFIED_VND_CASE10_EXACT_STRICT_GEOMETRY_AND_CNF',flush=True)
 if args.solve:py('run_gate.py',out='run.log')
if __name__=='__main__':main()
