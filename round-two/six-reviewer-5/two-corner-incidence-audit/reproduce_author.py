"""Optional strictly serial replay of byte-bound published author source.

Needs a full repository checkout; no network or private corpus. The parent
bridge is optional corroboration, not a premise of the new A--C review.
"""
import pathlib,subprocess,sys,os,json,time,resource,hashlib,tempfile,argparse
P=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--author-dir',type=pathlib.Path,default=P.parents[1]/'six-tammes-1'/'two-corner-incidence');args=parser.parse_args()
source=json.loads((P/'target-source.json').read_text())
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
with tempfile.TemporaryDirectory(prefix='two-corner-review-') as tmp:
 root=pathlib.Path(tmp);target=root/'two-corner-incidence';target.mkdir()
 for e in source['files']:
  raw=(args.author_dir/e['name']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=e['sha256'] or len(raw)!=e['bytes']:raise ValueError('full target source binding')
  (target/e['name']).write_bytes(raw)
 pins=json.loads((target/'PINS.json').read_text());parent=root/'triangle-surrounded-faces';parent.mkdir()
 for e in pins['parent_files']:
  raw=(args.author_dir.parent/'triangle-surrounded-faces'/e['path']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=e['sha256'] or len(raw)!=e['bytes']:raise ValueError('full optional parent binding')
  (parent/e['path']).write_bytes(raw)
 rows=[]
 for mode in ('normal','optimized'):
  for name in ('check.py','audit.py','bridge.py','controls.py'):
   start=time.monotonic();r=subprocess.run([sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(target/name)],env=env,cwd=target,capture_output=True,text=True,timeout=45)
   if r.returncode:raise ValueError(r.stderr)
   rows.append(dict(program=name,mode=mode,seconds=time.monotonic()-start,maxrss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,result=json.loads(r.stdout),guard_seconds=45))
 for name in ('check.py','audit.py','bridge.py','controls.py'):
  a=[v['result'] for v in rows if v['program']==name]
  if a[0]!=a[1]:raise ValueError('normal/optimized native difference')
 print(json.dumps(dict(strictly_serial=True,native_threads=1,target_commit=source['commit'],optional_parent_only=True,runs=rows),sort_keys=True))
