"""Portable exact-pinned public inputs; serial late corroboration only."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,tempfile
from linear import need
ROOT=Path(__file__).resolve().parent
GUARD="import runpy,signal,sys;signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s native')));signal.alarm(45);sys.argv=sys.argv[1:];runpy.run_path(sys.argv[0],run_name='__main__')"
def audit():
 inputs=json.loads((ROOT/'AUTHOR-INPUTS.json').read_text());env=dict(os.environ)
 for name in['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[name]='1'
 def run(cmd,cwd=None,timeout=55):
  z=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=timeout);need(z.returncode==0,{'exit':z.returncode,'stderr':z.stderr.decode()});return z.stdout
 with tempfile.TemporaryDirectory(prefix='near-cube-review-')as temporary:
  td=Path(temporary);repo=td/'repo';author=td/'author';author.mkdir();run(['git','init','-q',str(repo)],timeout=30);sha=inputs['target']['source_commit'];run(['git','-C',str(repo),'fetch','--depth=1','https://github.com/helgithorskarp/math_results',sha],timeout=60);fetched=[]
  for z in inputs['files']:
   raw=run(['git','-C',str(repo),'show',sha+':'+z['path']],timeout=30);need(hashlib.sha256(raw).hexdigest()==z['sha256']and len(raw)==z['bytes'],'ENTIRE exact public input bytes');(author/z['name']).write_bytes(raw);fetched.append([z['name'],z['sha256']])
  for line in(author/'SHA256SUMS').read_text().splitlines():
   h,f=line.split();need(hashlib.sha256((author/f).read_bytes()).hexdigest()==h,'native whole manifest')
  native=[];expected=json.loads((author/'expected.json').read_text())
  for mode in['normal','optimized']:
   output=td/('native-'+mode+'.json');cmd=[sys.executable]+(['-O']if mode=='optimized'else[])+['-B','-c',GUARD,str(author/'verify.py'),'--check',str(author/'expected.json'),'--output',str(output)];stdout=json.loads(run(cmd,cwd=author));whole=json.loads(output.read_text());need(whole==expected,'ENTIRE generated native record, not stdout summary');raw=json.dumps(whole,sort_keys=True,separators=(',',':')).encode();need(hashlib.sha256(raw).hexdigest()==stdout['record_sha256'],'native whole canonical summary agreement');native.append({'mode':mode,'entire_expected_equal':True,'whole_native_record_bytes':len(raw),'whole_native_record_sha256':hashlib.sha256(raw).hexdigest(),'summary':stdout})
  comparisons=[]
  for mode in['normal','optimized']:
   cmd=[sys.executable]+(['-O']if mode=='optimized'else[])+['-B',str(ROOT/'compare.py'),str(author)];comparisons.append(json.loads(run(cmd)))
  need(comparisons[0]==comparisons[1],'ENTIRE normal/O common field comparison')
 return {'agent':'six-reviewer-2','role':'independent mathematical reviewer','exact_public11_inputs':fetched,'native_complete_records':native,'entire_common_comparison':comparisons[0],'scope':'Portable late corroboration only; original primary seals and independent EXPECTED never changed. Exact source commit fetched from authorized public Git repository. 45s math/55s outer perchild, serial, all threads1.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();out=audit()
 if a.check:need(out==json.loads(a.check.read_text()),'ENTIRE late corroboration record')
 if a.output:a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();print(json.dumps({'ok':True,'whole_corroboration_bytes':len(raw),'whole_corroboration_sha256':hashlib.sha256(raw).hexdigest(),'native_entire_expected_equal':True,'all_fields_and_entire_common_export_equal':True}))
