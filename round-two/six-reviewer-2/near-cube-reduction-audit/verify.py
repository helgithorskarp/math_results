"""Serial bounded cold phases and comparison of the ENTIRE deterministic record."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
from linear import need
THREADS=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
def run():
 root=Path(__file__).resolve().parent;env=dict(os.environ)
 for name in THREADS:env[name]='1'
 phases={}
 for phase in['basis','literal','controls']:
  cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+['-B',str(root/(phase+'.py'))]
  r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=55)
  need(r.returncode==0,{'phase':phase,'exit':r.returncode,'stderr':r.stderr});phases[phase]=json.loads(r.stdout)
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','phases':phases,'scope':'Whole independent primary record, ALL three phases, standard-library exact arithmetic. Fixed45s internal/55s child; one serial mathematical child; finite evidence not universal proof.'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--emit',action='store_true');a=ap.parse_args();out=run();raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode()
 if a.check:need(out==json.loads(a.check.read_text()),'ENTIRE independent expected record differs')
 if a.emit:print(raw.decode())
 else:print(json.dumps({'ok':True,'entire_record_compared':bool(a.check),'whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),'basis_cases':out['phases']['basis']['complete_case_count'],'literal_domains':[6,7],'damages':out['phases']['controls']['damage_count'],'positive_controls':out['phases']['controls']['positive_count']},sort_keys=True))
if __name__=='__main__':main()
