"""Reproduce the ENTIRE independent record, then check exact frozen certificates."""
import pathlib,os,sys,subprocess,json,hashlib,tempfile,shutil
P=pathlib.Path(__file__).resolve().parent;env=dict(os.environ)
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
mode=['-O'] if sys.flags.optimize else [];got={}
with tempfile.TemporaryDirectory(prefix='deficit-review-') as tmp:
 D=pathlib.Path(tmp);shutil.copytree(P/'core',D/'core',ignore=shutil.ignore_patterns('__pycache__'));shutil.copy2(P/'frozen.py',D/'frozen.py');shutil.copy2(P/'PRIMARY.json',D/'PRIMARY.json')
 for program in ['algebra','original','principal','optimizer']:
  r=subprocess.run([sys.executable,*mode,'-B',str(D/'core'/f'{program}.py')],cwd=D,env=env,capture_output=True,timeout=45)
  if r.returncode:raise RuntimeError(r.stderr.decode())
  got[program]=json.loads(r.stdout)
 text=json.dumps(got,indent=2,sort_keys=True)+'\n'
 if text.encode()!=(P/'PRIMARY.json').read_bytes():raise ValueError('entire independently regenerated record differs')
 r=subprocess.run([sys.executable,*mode,'-B',str(D/'frozen.py')],cwd=D,env=env,capture_output=True,timeout=45)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 controls=json.loads(r.stdout)
 if json.dumps(controls,sort_keys=True)!=json.dumps(json.loads((P/'CONTROLS.json').read_text()),sort_keys=True):raise ValueError('entire certificate controls differ')
print(json.dumps(dict(ok=True,bytes=len(text.encode()),sha256=hashlib.sha256(text.encode()).hexdigest(),valid_certificates=controls['valid_certificates'],semantic_damages=len(controls['rejected_semantic_damages']),all_children_guard_seconds=45)))
