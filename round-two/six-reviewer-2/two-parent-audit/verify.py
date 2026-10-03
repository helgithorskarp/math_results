"""Cold-source verifier: exact whole records and every raw entry in both modes."""
from pathlib import Path
import argparse,ast,hashlib,json,os,platform,resource,shutil,subprocess,tempfile,time
ROOT=Path(__file__).resolve().parent
def need(ok,why):
 if not ok:raise ValueError(why)
def run(mode,destination):
 destination.mkdir(parents=True,exist_ok=False)
 names=('incidence.py','direct.py','physical.py','prerequisites.py','merge.py')
 for name in names:
  need(not any(isinstance(n,ast.Assert)for n in ast.walk(ast.parse((ROOT/name).read_bytes()))),'no removable proof checks')
  shutil.copyfile(ROOT/name,destination/name)
 env=os.environ.copy()
 for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[name]='1'
 executable=['/usr/bin/python3','-B']+(['-O']if mode=='optimized'else[])
 allocations=((2,5,2),(3,4,2),(4,3,2),(2,4,3),(3,3,3),(2,3,4))
 commands=[('incidence',('incidence.py','incidence'))]
 for r in(1,4):
  for ns in allocations:
   name='direct-'+str(r)+'-'+''.join(map(str,ns));key=','.join(map(str,(r,)+ns));commands.append((name,('direct.py','capacity',name,key)))
 for lo in(0,100,200,300):
  for label,script,args in(('physical','physical.py',()),('direct-physical','direct.py',('physical',))):
   name=label+'-'+str(lo);commands.append((name,(script,)+args+(name,str(lo)+','+str(lo+100))))
 commands.append(('prerequisites',('prerequisites.py','prerequisites')))
 receipts=[]
 for label,args in commands:
  started=time.monotonic()
  try:result=subprocess.run(executable+list(args),cwd=destination,env=env,capture_output=True,timeout=20)
  except subprocess.TimeoutExpired as failure:
   (destination/(label+'.stdout')).write_bytes(failure.stdout or b'');(destination/(label+'.stderr')).write_bytes(failure.stderr or b'')
   receipts.append(dict(child=label,seconds=time.monotonic()-started,guard_seconds=20,threads=1,status='INCOMPLETE_TIMEOUT_NO_MATHEMATICAL_INFERENCE'))
   (destination/'execution.json').write_text(json.dumps(receipts,indent=2)+'\n');raise
  (destination/(label+'.stdout')).write_bytes(result.stdout);(destination/(label+'.stderr')).write_bytes(result.stderr)
  rec=dict(child=label,seconds=time.monotonic()-started,returncode=result.returncode,rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,guard_seconds=20,threads=1)
  receipts.append(rec);(destination/'execution.json').write_text(json.dumps(receipts,indent=2)+'\n')
  need(result.returncode==0,{'failed_child':rec,'stderr':result.stderr.decode()})
 import merge
 merge.capacity(destination,destination/'direct-capacity')
 merge.physical(destination,destination/'physical','physical')
 merge.physical(destination,destination/'direct-physical','direct-physical')
 pins=json.loads((ROOT/'EXPECTED.json').read_text());comparisons=[]
 for a,b,kind in (('incidence','direct-capacity','capacity'),('physical','direct-physical','physical')):
  one=destination/a;two=destination/b;files=sorted(p.name for p in one.iterdir());need(files==sorted(p.name for p in two.iterdir()),'whole generated file catalogue equal')
  total=0
  for name in files:
   x=(one/name).read_bytes();y=(two/name).read_bytes();need(x==y,{'complete_entry_comparison':name});total+=len(x)
  raw=(one/'record.json').read_bytes();need(len(raw)-1==pins[kind]['bytes']and hashlib.sha256(raw[:-1]).hexdigest()==pins[kind]['sha256'],'fresh full-record pin')
  comparisons.append(dict(kind=kind,entire_files=len(files),whole_bytes_compared=total,record_bytes=len(raw)-1,record_sha256=hashlib.sha256(raw[:-1]).hexdigest()))
 raw=(destination/'prerequisites/record.json').read_bytes();need(hashlib.sha256(raw[:-1]).hexdigest()==pins['prerequisites']['sha256']and len(raw)-1==pins['prerequisites']['bytes'],'fresh prerequisite pin')
 cap=json.loads((destination/'incidence/record.json').read_bytes());need(cap['total_global_H_allocations']==643610 and len(cap['survivors'])==1,'full labelled capacity domain and unique inventory')
 pre=json.loads(raw);need(pre['BASE_holes_lower']==177 and pre['five_max']==120 and pre['binary_control_count']==3853,'fresh numerical prerequisites and inactive controls')
 return dict(mode=mode,status='COMPLETE_COLD_SOURCE_ONLY',python=platform.python_version(),copied_only=list(names),math_children=receipts,comparisons=comparisons,prerequisite_record_bytes=len(raw)-1,prerequisite_sha256=hashlib.sha256(raw[:-1]).hexdigest(),native_imported=False)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--mode',choices=('normal','optimized'),required=True);parser.add_argument('--out-dir',required=True);args=parser.parse_args()
 result=run(args.mode,Path(args.out_dir).resolve());Path(args.out_dir,'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
