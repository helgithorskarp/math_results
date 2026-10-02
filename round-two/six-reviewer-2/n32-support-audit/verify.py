"""Cold whole-evidence replay: exact child records, explicit comparisons in -O."""
from pathlib import Path
import argparse,hashlib,json,os,resource,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
THREADS=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
def need(ok,why):
 if not ok:raise ValueError(why)
def main():
 p=argparse.ArgumentParser();p.add_argument('--freeze',action='store_true',help='ONLY initial pre-author-code whole-record creation');args=p.parse_args();env=os.environ.copy();env.update({k:'1'for k in THREADS});env['PYTHONDONTWRITEBYTECODE']='1';records={};timings=[];t=time.monotonic()
 for name in ['core','literal','controls']:
  started=time.monotonic();cmd=[sys.executable]+(['-O']if sys.flags.optimize else[])+[str(ROOT/(name+'.py'))];child=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,timeout=55);need(child.returncode==0,{'phase':name,'code':child.returncode,'stderr':child.stderr});record=json.loads(child.stdout);records[name]=record;timings.append({'phase':name,'seconds':time.monotonic()-started})
 raw=json.dumps(records,sort_keys=True,separators=(',',':')).encode();expected=ROOT/'EXPECTED.json'
 if args.freeze:
  need(not expected.exists(),'frozen evidence already exists; no overwrite');expected.write_bytes(raw+b'\n')
 else:need(json.loads(expected.read_text())==records,'ENTIRE frozen mathematical record, all phases/fields/rational data')
 print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),'phases':timings,'seconds':time.monotonic()-t,'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'python':sys.version,'optimize':sys.flags.optimize,'whole_expected_equal':not args.freeze,'rejections':records['controls']['rejections'],'all_threads_one':True},sort_keys=True))
if __name__=='__main__':main()
