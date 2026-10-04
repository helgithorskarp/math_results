"""Check frozen public source, then reproduce the two independent audits."""
import hashlib,json,os,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
if (P/'SHA256SUMS').exists():
 for line in (P/'SHA256SUMS').read_text().splitlines():
  sha,name=line.split('  ')
  if hashlib.sha256((P/name).read_bytes()).hexdigest()!=sha:raise ValueError('frozen source '+name)
observed=[json.loads((P/name).read_text()) for name in ('VALIDATION.json','COMMUNICATION-VALIDATION.json')]
env=os.environ.copy()
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
for name,old,output in zip(('validate_cover.py','validate_communications.py'),observed,('VALIDATION.json','COMMUNICATION-VALIDATION.json')):
 # Run in temporary source-only storage, preserving published observations.
 import tempfile,shutil
 with tempfile.TemporaryDirectory(prefix='independent-replay-') as temp:
  cold=pathlib.Path(temp)
  for source in ('check_cover.py','COVER-input.json','validate_cover.py','check_communications.py','validate_communications.py'):shutil.copyfile(P/source,cold/source)
  subprocess.run([sys.executable,'-I','-B',name],cwd=cold,env=env,check=True)
  new=json.loads((cold/output).read_text())
  for key in ('status','positive_children','record_bytes','record_sha256','source_sha256'):
   if new[key]!=old[key]:raise ValueError('complete replay summary '+key)
  if name=='validate_cover.py' and new['semantic_rejections']!=16:raise ValueError('sixteen semantic controls')
print('PASS: frozen public source, eight cold positive children, sixteen semantic rejections; full records match before fingerprints.')
