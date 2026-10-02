"""Portable postseal whole native/source/common-field corroboration.

Materializes exact13-file public Git closure in temporary scratch; never
imports researcher code into primary verify.py. No network, signing or push.
"""
from pathlib import Path
import argparse,hashlib,json,os,resource,subprocess,sys,tempfile,time
ROOT=Path(__file__).resolve().parent
THREADS=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
def need(ok,why):
 if not ok:raise ValueError(why)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,default=ROOT.parents[2]);args=p.parse_args();repo=args.repository.resolve();manifest=json.loads((ROOT/'AUTHOR-INPUTS.json').read_text());env=os.environ.copy();env.update({k:'1'for k in THREADS});env['PYTHONDONTWRITEBYTECODE']='1';records=[]
 for name,h in json.loads((ROOT/'PROVENANCE.json').read_text())['sealed_files'].items():need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'all9 primary files unchanged')
 def run(cmd,cwd):
  t=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True,timeout=55);need(r.returncode==0,{'code':r.returncode,'stderr':r.stderr});return json.loads(r.stdout),time.monotonic()-t
 with tempfile.TemporaryDirectory(prefix='six-reviewer2-n32-native-')as td:
  work=Path(td)
  for f in manifest['files']:
   need(f['path'].startswith('round-two/six-downset-2/near_full_n32_sharp_support/')and '..'not in Path(f['path']).parts,'bounded original public input path');raw=subprocess.check_output(['git','-C',str(repo),'show',f['source_commit']+':'+f['path']],timeout=30);need(len(raw)==f['bytes']and hashlib.sha256(raw).hexdigest()==f['sha256'],'complete pinned public input bytes');(work/Path(f['path']).name).write_bytes(raw)
  need(len(manifest['files'])==13,'whole native13-file closure')
  for optimized in[False,True]:
   py=[sys.executable]+(['-O']if optimized else[]);out=work/('whole-O.json'if optimized else'whole.json');fields=work/('fields-O.json'if optimized else'fields.json')
   cmd=py+['-c',"import runpy,signal,sys;signal.signal(signal.SIGALRM,lambda *a:(_ for _ in()).throw(TimeoutError('fixed45s original native guard')));signal.alarm(45);sys.argv=['verify.py','--check','expected.json','--output',sys.argv[1]];runpy.run_path('verify.py',run_name='__main__')",str(out)]
   summary,seconds=run(cmd,work);raw=out.read_bytes();need(raw==(work/'expected.json').read_bytes(),'ENTIRE unchanged native frozen record; not stdout summary');export,et=run(py+[str(ROOT/'native_export.py'),str(work),str(fields)],ROOT);compare,ct=run(py+[str(ROOT/'compare.py'),str(out),str(fields)],ROOT)
   records.append({'optimized':optimized,'native_seconds':seconds,'native_stdout_summary':summary,'whole_native_record_bytes':len(raw),'whole_native_record_sha256':hashlib.sha256(raw).hexdigest(),'entire_native_expected_equal':True,'whole_native_fields_export':export,'fields_seconds':et,'whole_common_comparison':compare,'comparison_seconds':ct,'peak_child_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
  for f in manifest['files']:need(hashlib.sha256((work/Path(f['path']).name).read_bytes()).hexdigest()==f['sha256'],'all13 native source/oracle files unchanged')
 need(records[0]['whole_native_record_sha256']==records[1]['whole_native_record_sha256']and records[0]['whole_native_fields_export']['sha256']==records[1]['whole_native_fields_export']['sha256']and records[0]['whole_common_comparison']['whole_comparison_sha256']==records[1]['whole_common_comparison']['whole_comparison_sha256'],'ENTIRE normal/O native, fields and own common output match')
 for name,h in json.loads((ROOT/'PROVENANCE.json').read_text())['sealed_files'].items():need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'all9 primary files unchanged after corroboration')
 print(json.dumps({'agent':'six-reviewer-2','role':'independent mathematical reviewer','records':records,'all13_original_pinned_inputs_unchanged':True,'all9_primary_seals_unchanged':True,'all_native_full_records_equal':True,'all_fields_and_entire_common_export_equal':True,'temporary_dense_exports_published':False,'scope':'Postseal corroboration only. Complete primary verify.py remains own-only; exact seed is credited mathematical author input. Native729-arithmetic/baseline and12adverse cases reproduced, no fresh historical baseline verdict.'},sort_keys=True))
if __name__=='__main__':main()
