"""Optional network corroboration of pinned source and ENTIRE native/scoped common records."""
import pathlib,sys,tempfile,urllib.request,hashlib,json,shutil,subprocess,os
P=pathlib.Path(__file__).resolve().parent;meta=json.loads((P/'AUTHOR-SOURCE.json').read_text());env=dict(os.environ)
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
mode=['-O'] if sys.flags.optimize else []
with tempfile.TemporaryDirectory(prefix='deficit-native-') as tmp:
 D=pathlib.Path(tmp);A=D/'author';A.mkdir();shutil.copytree(P/'core',D/'core',ignore=shutil.ignore_patterns('__pycache__'));shutil.copy2(P/'bridge.py',D/'bridge.py')
 for row in meta['files']:
  b=urllib.request.urlopen(urllib.request.Request('https://raw.githubusercontent.com/helgithorskarp/math_results/'+meta['commit']+'/'+row['path'],headers={'User-Agent':'independent mathematical review'}),timeout=20).read()
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise ValueError('pinned complete source bytes')
  f=A/pathlib.Path(row['path']).relative_to(meta['base']);f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
 r=subprocess.run([sys.executable,'-I',*mode,'-B',str(A/'verify.py')],cwd=A,env=env,capture_output=True,timeout=45)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 native=json.loads(r.stdout)
 if native['bytes']!=73825 or native['sha256']!='249b2778b1c92125ec9334a42846e86829c0df6074482b3a43a47d43f973304d':raise ValueError('whole native record')
 r=subprocess.run([sys.executable,*mode,'-B',str(D/'bridge.py')],cwd=D,env=env,capture_output=True,timeout=45)
 if r.returncode:raise RuntimeError(r.stderr.decode())
 if (D/'COMMON.json').read_bytes()!=(P/'COMMON.json').read_bytes():raise ValueError('ENTIRE independently recomputed native categories')
print(json.dumps(dict(ok=True,native_bytes=native['bytes'],native_sha256=native['sha256'],common_bytes=(P/'COMMON.json').stat().st_size,common_sha256=hashlib.sha256((P/'COMMON.json').read_bytes()).hexdigest(),exact_pinned_source_files=len(meta['files']))))
