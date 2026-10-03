import pathlib,os,subprocess,json,time,resource,hashlib,sys
P=pathlib.Path(__file__).resolve().parent
env=os.environ.copy()
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
state=pathlib.Path(env['RESEARCH_PAUSE_DIR']) if env.get('RESEARCH_PAUSE_DIR') else None
packages=env.get('REVIEW_SYMPY_PATH','');runner="import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')"
receipts=[]
mode_summary=[];whole=[]
def run(mode,label,script,args=(),expected=0,cas=False):
 if state and any((state/n).exists() for n in ['PAUSED','PAUSED.json','HANDOVER','HANDOVER.json']):raise RuntimeError('operational barrier')
 name=mode+'-'+label
 cmd=[sys.executable,'-I','-B']+(['-O'] if mode=='optimized' else [])
 cmd+=['-c',runner,str(packages),str(P/script)] if cas and packages else [str(P/script)]
 cmd+=list(map(str,args));t=time.monotonic();r=subprocess.run(cmd,env=env,capture_output=True,timeout=55)
 (P/(name+'.stdout')).write_bytes(r.stdout);(P/(name+'.stderr')).write_bytes(r.stderr)
 if (expected==0 and r.returncode!=0) or (expected!=0 and r.returncode==0):raise RuntimeError(name+' '+r.stderr.decode()[-2000:])
 rr=dict(mode=mode,label=label,returncode=r.returncode,seconds=time.monotonic()-t,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,bytes=len(r.stdout),sha256=hashlib.sha256(r.stdout).hexdigest());receipts.append(rr)
 (P/'own-replay-incomplete.json').write_text(json.dumps(dict(complete=False,receipts=receipts),indent=2)+'\n')
 return r.stdout
for mode in ['normal','optimized']:
 out=P/('independent-'+mode);out.mkdir(exist_ok=True)
 primary=run(mode,'canonical','canonical.py',cas=True);(out/'primary.json').write_bytes(primary)
 if primary!=(P/'canonical.stdout').read_bytes():raise ValueError('whole sealed symbolic record')
 if hashlib.sha256(primary).hexdigest()!=json.loads((P/'EXPECTED.json').read_text())['primary']['sha256']:raise ValueError('sealed expected whole primary')
 fixtures=[]
 for n,h in [(3,3),(3,4),(3,10),(5,3)]:
  raw=run(mode,f'literal-{n}-{h}','literal.py',[n,h],cas=True);(out/f'literal-{n}-{h}.json').write_bytes(raw);fixtures.append(raw)
  print(json.dumps(dict(mode=mode,own_literal=[n,h],complete=True)),flush=True)
 work=P/'native-normal/work';cleared=out/'cleared.json'
 bind=run(mode,'binding','binding.py',[out/'primary.json',work/'raw-bounds.json',cleared],cas=True)
 nodes=[]
 for h in range(3,134):
  # Same exact point data, freshly independently checked in each mode.
  target=work/'newton'/f'independent-h{h}.json'
  raw=run(mode,f'point-{h}','checkpoint_polynomials.py',[cleared,work/'newton'/f'h{h}.json',target]);nodes.append(raw)
  (out/f'point-{h}.json').write_bytes(raw)
  if h==3 or h%20==3 or h==133:print(json.dumps(dict(mode=mode,own_complete_points=h-2,required=131)),flush=True)
 newton=run(mode,'Newton','checkpoint_polynomials.py',[cleared,work/'newton',out/'Newton.json','--newton',work/'newton-coefficients.json'])
 for damage in ['original-entry','negative-factor','degree']:
  run(mode,'damage-'+damage,'binding.py',[out/'primary.json',work/'raw-bounds.json',out/'bad.json','--damage',damage],expected=1,cas=True)
 for damage in ['shift-coefficient','missing-minor']:
  run(mode,'damage-'+damage,'checkpoint_polynomials.py',[cleared,work/'newton/h3.json',out/'bad.json','--damage',damage],expected=1)
 for damage in ['Newton-coefficient','real-domain']:
  run(mode,'damage-'+damage,'checkpoint_polynomials.py',[cleared,work/'newton',out/'bad.json','--newton',work/'newton-coefficients.json','--damage',damage],expected=1)
 for damage in ['whole-ground-complement','old-empty-retention']:
  run(mode,'damage-'+damage,'literal.py',[3,3,'--damage',damage],expected=1,cas=True)
 for damage in ['empty-omission','standard-metric']:
  bad=run(mode,'altered-primary-'+damage,'canonical.py',['--damage',damage],cas=True);(out/'bad-primary.json').write_bytes(bad)
  run(mode,'damage-'+damage,'binding.py',[out/'bad-primary.json',work/'raw-bounds.json',out/'bad.json'],expected=1,cas=True)
 run(mode,'damage-light-mean','canonical.py',['--damage','light-mean'],expected=1,cas=True)
 stream=primary+bind+b''.join(fixtures+nodes)+newton;whole.append(stream)
 mode_summary.append(dict(mode=mode,stream_bytes=len(stream),stream_sha256=hashlib.sha256(stream).hexdigest(),Newton=json.loads(newton)))
 if len(whole)==2 and whole[0]!=whole[1]:raise ValueError('ENTIRE independent normal/O stream')
 (P/'own-replay.json').write_text(json.dumps(dict(complete=len(whole)==2,entire_modes_equal=len(whole)==2,serial_math_children=True,native_threads=1,guard_seconds=55,unchanged_scope='1CPU2GiB',receipts=receipts,mode_summary=mode_summary),indent=2)+'\n')
 expected=json.loads((P/'EXPECTED.json').read_text())['independent']
 if mode_summary[-1]['stream_bytes']!=expected['stream_bytes'] or mode_summary[-1]['stream_sha256']!=expected['stream_sha256']:raise ValueError('entire independent expected stream')
 print(json.dumps(mode_summary[-1]),flush=True)
