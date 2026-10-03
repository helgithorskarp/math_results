#!/usr/bin/env python3
"""Cold source-only reproduction with strict WHOLE BYTE comparisons.
Primary code and old validation are unchanged after their recorded seal.
"""
import argparse,copy,datetime,hashlib,json,os,pathlib,resource,subprocess,sys,tempfile,time
P=pathlib.Path(__file__).resolve().parent
ENV=dict(os.environ)
for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:ENV[k]='1'
ENV['PYTHONDONTWRITEBYTECODE']='1'
def require(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native');ap.add_argument('--output',required=True);a=ap.parse_args()
 checks=[];static=(P/'full.json').read_bytes()
 with tempfile.TemporaryDirectory(prefix='g21-reviewer-reproduction-') as tmp:
  for opt in [False,True]:
   dest=pathlib.Path(tmp)/'full.json';cmd=[sys.executable]+(['-O'] if opt else [])+[str(P/'audit.py'),'--output',str(dest)]
   start=time.monotonic();r=subprocess.run(cmd,env=ENV,capture_output=True,timeout=45);require(r.returncode==0,r.stderr.decode());require(dest.read_bytes()==static,'strict complete cold serialized record mismatch')
   checks.append({'stage':'cold independent full record','optimized':opt,'seconds':time.monotonic()-start,'status':'PASS','bytes':len(static),'sha256':hashlib.sha256(static).hexdigest()})
   # The optional primary --expected flag uses Python JSON value equality;
   # this byte comparison preserves boolean/int distinctions as well.
   if a.native:
    native=pathlib.Path(a.native).resolve();pins=json.loads((P/'NATIVE-PINS.json').read_text())['files']
    for f,v in pins.items():require(hashlib.sha256((native/f).read_bytes()).hexdigest()==v['sha256'],'whole pinned target input changed')
    for damage in [None,'coordinate','missing-triple','duplicate-triple','missing-cell','swapped-sign']:
     d=pathlib.Path(tmp)/'late.json';cmd=[sys.executable]+(['-O'] if opt else [])+[str(P/'late_compare.py'),'--native',str(native),'--output',str(d)]
     if damage:cmd+=['--damage',damage]
     start=time.monotonic();r=subprocess.run(cmd,env=ENV,capture_output=True,timeout=45);require((r.returncode==0)==(damage is None),'late semantic damage/replay unexpected result '+r.stderr.decode())
     if not damage:
      out=json.loads(d.read_text());out.pop('seconds');checks.append({'stage':'late complete native data/Cramer/cover','optimized':opt,'seconds':time.monotonic()-start,'status':'PASS','whole_result':out})
     else:checks.append({'stage':'late damage '+damage,'optimized':opt,'seconds':time.monotonic()-start,'status':'REJECTED'})
 seal=json.loads((P/'PRIMARY-SEAL.json').read_text())
 for f in ['audit.py','validate.py','PROOF.md','full.json']:
  require(hashlib.sha256((P/f).read_bytes()).hexdigest()==seal['files'][f]['sha256'],'primary seal changed')
 out={'actual_agent':'six-reviewer-3','role':'independent mathematical reviewer','status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'all_native_threads':1,'external_math_child_guard_seconds':45,'serial_children':True,'peak_children_rss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'checks':checks,'primary_seals_unchanged':True,'strict_whole_byte_comparison':'does not conflate JSON bool/int values'}
 pathlib.Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'total_seconds':sum(r['seconds'] for r in checks),'max_seconds':max(r['seconds'] for r in checks),'peak_children_rss_KiB':out['peak_children_rss_KiB']}))
if __name__=='__main__':main()
