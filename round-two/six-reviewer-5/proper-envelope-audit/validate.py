"""Whole-record checks and twelve semantic defects, fixed serial resource guard."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time
CONTROLS={'anchor-sign':'common sign conjugation','missing-edge':'basis sum equals independent entire block P','vector-row':'every literal original resolvent row','nonpositive-vector':'strictly positive original vector','false-upper-640':'every literal original resolvent row','false-lower-641':'full original Rayleigh lower bound','wrong-empty':'literal original empty loop','omit-empty-metric':'entire actual original Gram','wrong-core-floor':'explicit proper seed gap units','multi-star-sign':'all maximum singleton signs needed','frozen-endpoints':'cannot reopen saturated endpoints','false-full-corner':'competing corner empty Rayleigh exceeds norm five'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--out',required=True);arg=parser.parse_args();root=pathlib.Path(__file__).resolve().parent
 expected=(root/'RECORD.json').read_bytes();env=dict(os.environ)
 for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
 receipt=dict(interpreter=sys.version,native_threads=1,serial_children=1,guard_seconds_per_child=45,positive_children=[],controls=[])
 with tempfile.TemporaryDirectory(prefix='literal-star-envelope-') as name:
  tmp=pathlib.Path(name);shutil.copyfile(root/'check.py',tmp/'check.py')
  def run(mode,damage=''):
   out=tmp/'record.json';cmd=[sys.executable,'-I','-B']+(['-O'] if mode=='optimized' else [])+[str((tmp if mode=='cold' else root)/'check.py'),'--record',str(out)]+(['--damage',damage] if damage else [])
   start=time.monotonic();child=subprocess.run(cmd,capture_output=True,env=env,timeout=45)
   row=dict(mode=mode,exit_code=child.returncode,seconds=time.monotonic()-start,peak_child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
   return child,row,out
  for mode in ('normal','optimized','cold'):
   child,row,out=run(mode);need(child.returncode==0,child.stderr.decode());need(out.read_bytes()==expected,'entire mathematical record equality')
   row.update(record_bytes=len(expected),record_sha256=hashlib.sha256(expected).hexdigest());receipt['positive_children'].append(row)
   print('complete positive '+mode,flush=True)
  for mode in ('normal','optimized'):
   for damage,failure in CONTROLS.items():
    child,row,out=run(mode,damage);need(child.returncode!=0 and ('ValueError: '+failure).encode() in child.stderr,'named mathematical defect must reject: '+damage)
    row.update(name=damage,rejected=True,failure=child.stderr.decode().strip().splitlines()[-1]);receipt['controls'].append(row)
   print('complete twelve defects '+mode,flush=True)
 pathlib.Path(arg.out).write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 print(json.dumps(dict(positive=3,rejections=len(receipt['controls']),record_sha256=hashlib.sha256(expected).hexdigest())))
if __name__=='__main__':main()
