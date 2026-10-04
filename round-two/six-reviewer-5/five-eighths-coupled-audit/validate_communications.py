"""Independent cold normal/optimized communication controls, serial."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile,time
P=pathlib.Path(__file__).resolve().parent;env=os.environ.copy()
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
rows=[];first=None;parsed=None
with tempfile.TemporaryDirectory(prefix='communications-audit-',dir=P) as temp:
 for i,mode in enumerate(([],['-O'],[],['-O'])):
  cold=pathlib.Path(temp)/str(i);cold.mkdir();shutil.copyfile(P/'check_communications.py',cold/'check_communications.py')
  start=time.monotonic();r=subprocess.run([sys.executable,'-I','-B',*mode,'check_communications.py'],cwd=cold,env=env,capture_output=True,text=True,timeout=45)
  if r.returncode:raise ValueError(r.stderr)
  raw=(cold/'communications-private.json').read_bytes();obj=json.loads(raw)
  if first is None:first,parsed=raw,obj
  if raw!=first or obj!=parsed:raise ValueError('whole cold communication record mismatch')
  rows.append(dict(mode=mode,returncode=r.returncode,result=json.loads(r.stdout),elapsed_seconds=time.monotonic()-start))
(P/'communications-private.json').write_bytes(first)
out=dict(status='PASS',positive_children=4,serial=True,native_threads=1,guard_seconds=45,python=sys.version,record_sha256=hashlib.sha256(first).hexdigest(),record_bytes=len(first),source_sha256=hashlib.sha256((P/'check_communications.py').read_bytes()).hexdigest(),rows=rows)
(P/'COMMUNICATION-VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
