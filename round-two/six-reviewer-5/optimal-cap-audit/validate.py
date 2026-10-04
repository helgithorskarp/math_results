"""Serial, fixed 45 second guards; whole records compare in both modes."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time
P=pathlib.Path(__file__).resolve().parent
def need(ok,label):
 if not ok:raise ValueError(label)
def main():
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);v=a.parse_args()
 env=dict(os.environ)
 for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
 records=[];wanted={};events=[];start=time.monotonic()
 cases=[('core',3)]+[('root',j) for j in range(9)]+[('restricted',j) for j in (3,4,5,6)]
 damages=[('M','root',3),('beta','root',4),('odd-common','root',3),('odd-pair','root',4),('no-inward','root',6),('anchor','core',3),('multiplicity','core',3),('pair-cross','core',3),('skew-multiplicity','core',3),('motion','root',7)]
 with tempfile.TemporaryDirectory(prefix='audit-',dir=P) as tmp:
  tmp=pathlib.Path(tmp)
  def child(route,label,damage='none',optimized=False,directory=P):
   dest=tmp/'child.json';cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(directory/'check.py'),'--route',route,'--label',str(label),'--damage',damage,'--output',str(dest)]
   began=time.monotonic()
   try:p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=45)
   except subprocess.TimeoutExpired:
    events.append(dict(route=route,label=label,damage=damage,timeout=True,guard=45));pathlib.Path(v.output).write_text(json.dumps(dict(complete=False,events=events,mathematical_nonexistence=False))+'\n');raise
   event=dict(route=route,label=label,damage=damage,optimized=optimized,cold=directory!=P,exit_code=p.returncode,seconds=time.monotonic()-began,peak_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
   events.append(event)
   if damage=='none':
    need(p.returncode==0,'positive child failed: '+p.stderr);out=json.loads(dest.read_text());key=(route,label)
    if key in wanted:need(out==wanted[key],'whole mathematical records differ')
    else:wanted[key]=out;records.append(out)
   else:need(p.returncode!=0 and 'ValueError' in p.stderr,'semantic damage not rejected: '+str(event))
  for optimized in (False,True):
   for route,label in cases:child(route,label,optimized=optimized)
   for damage,route,label in damages:child(route,label,damage,optimized)
  cold=tmp/'cold';cold.mkdir()
  for name in ('check.py','algebra.py','signs.py'):shutil.copyfile(P/name,cold/name)
  for route,label in cases:child(route,label,directory=cold)
 b=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
 if (P/'RECORD.json').exists():need((P/'RECORD.json').read_bytes()==b+b'\n','whole sealed expected record mismatch')
 else:(P/'RECORD.json').write_bytes(b+b'\n')
 out=dict(complete=True,python=sys.version,standard_library_only=True,normal_optimized_whole_records=True,cold_whole_records=True,positive_children=42,semantic_controls=20,record_bytes=len(b),record_sha256=hashlib.sha256(b).hexdigest(),seconds=time.monotonic()-start,max_child_seconds=max(e['seconds'] for e in events),peak_kib=max(e['peak_kib'] for e in events),guard_seconds=45,native_threads=1,serial_math_children=True,events=events)
 pathlib.Path(v.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:x for k,x in out.items() if k!='events'},indent=2))
if __name__=='__main__':main()
