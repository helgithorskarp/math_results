"""Fetch and check all pinned native bytes; repeat the late comparison only."""
import pathlib,tempfile,json,hashlib,urllib.request,concurrent.futures,subprocess,sys,os,shutil
P=pathlib.Path(__file__).resolve().parent;receipt=json.loads((P/'AUTHOR-SOURCE.json').read_text())
for row in json.loads((P/'PRIMARY-SEAL.json').read_text())['files']:
 if hashlib.sha256((P/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise ValueError('sealed primary mismatch')
env=dict(os.environ)
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
with tempfile.TemporaryDirectory(prefix='native-',dir=P) as tmp:
 root=pathlib.Path(tmp);(root/'author').mkdir()
 for name in ['PRIMARY-SEAL.json','COMMON.json','common.py']+[r['path'] for r in json.loads((P/'PRIMARY-SEAL.json').read_text())['files']]:shutil.copyfile(P/name,root/name)
 def fetch(row):
  url='https://raw.githubusercontent.com/helgithorskarp/math_results/'+receipt['source_commit']+'/'+receipt['base']+'/'+row['path']
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'six-reviewer-5'}),timeout=20) as r:raw=r.read()
  if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('native full source mismatch')
  (root/'author'/row['path']).write_bytes(raw)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,receipt['files']))
 def run(program,*args,optimized=False):
  r=subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/program),*args],cwd=root,env=env,capture_output=True,timeout=45)
  if r.returncode:raise RuntimeError(r.stderr.decode())
  return r.stdout
 for mode in (False,True):run('author/check.py','--output','native-optimized.json' if mode else 'native-normal.json',optimized=mode)
 controls=run('author/controls.py');optimized=run('author/controls.py',optimized=True)
 if controls!=optimized or json.loads(controls)['rejected_count']!=20:raise ValueError('native whole controls normal/O')
 result=run('common.py',optimized=bool(sys.flags.optimize))
 if result!=(root/'COMMON.json').read_bytes():raise ValueError('entire late correspondence differs')
 print(result.decode(),end='')
