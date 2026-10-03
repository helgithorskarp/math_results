"""Single serial child,45s guards, six native thread settings1, source-only replay."""
from pathlib import Path
from datetime import datetime,timezone
import os,subprocess,sys,json,time,hashlib,resource,argparse

def need(ok,why):
 if not ok:raise ValueError(why)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output)
 need(not out.exists(),'use a fresh nonexistent output directory');out.mkdir(parents=True)
 source=Path(__file__).resolve().parent;env=os.environ.copy()
 for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
 receipts=[];pairs=[]
 def child(name,program,argv,optimized=False):
  cmd=[sys.executable]+(['-O']if optimized else[])+[str(source/program)]+list(map(str,argv));t=time.monotonic()
  try:r=subprocess.run(cmd,capture_output=True,env=env,timeout=45)
  except subprocess.TimeoutExpired as e:
   (out/(name+'.stdout')).write_bytes(e.stdout or b'');(out/(name+'.stderr')).write_bytes(e.stderr or b'');raise ValueError('incomplete child timeout: '+name)
  (out/(name+'.json')).write_bytes(r.stdout);(out/(name+'.stderr')).write_bytes(r.stderr)
  row={'name':name,'seconds':time.monotonic()-t,'returncode':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'peak_children_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'optimized':optimized,'guard_seconds':45,'threads':1};receipts.append(row)
  (out/'EXECUTION.json').write_text(json.dumps(receipts,indent=2)+'\n');need(r.returncode==0,'incomplete child '+name+': '+r.stderr.decode());json.loads(r.stdout);return r.stdout
 for mode,opt in [('normal',False),('optimized',True)]:
  child('primitive-'+mode,'primitive.py',[],opt)
  child('second-'+mode,'second.py',[out/('primitive-'+mode+'.json')],opt)
  child('controls-'+mode,'controls.py',[out/('primitive-'+mode+'.json')],opt)
 for stage in ['primitive','second','controls']:
  a=(out/(stage+'-normal.json')).read_bytes();b=(out/(stage+'-optimized.json')).read_bytes();need(a==b,'ENTIRE mode record mismatch '+stage);pairs.append({'stage':stage,'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest(),'whole_mode_match':True})
 x={'status':'COMPLETE_SOURCE_ONLY_ASYMMETRIC_MOTION_AUDIT','utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'whole_mode_records':pairs,'execution':receipts,'max_child_seconds':max(x['seconds']for x in receipts),'total_child_seconds':sum(x['seconds']for x in receipts),'semantic_damages_per_mode':14,'malformed_damages_per_mode':10,'positive_repair_slacks':['1/2','1','2'],'one_serial_child':True,'threads':1,'guard_seconds':45}
 (out/'RESULT.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
if __name__=='__main__':main()
