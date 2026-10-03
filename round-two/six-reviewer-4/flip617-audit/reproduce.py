"""Serial bounded fresh computations; large intermediate traces stay in output."""
import argparse,hashlib,json,os,pathlib,subprocess,sys,time
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
def need(ok,why):
 if not ok:raise ValueError(why)
def run(output):
 out=pathlib.Path(output);need(not out.exists(),'fresh output directory required');out.mkdir(parents=True)
 src=pathlib.Path(__file__).resolve().parent;env=os.environ.copy();env.update({x:'1' for x in THREADS});env['PYTHONDONTWRITEBYTECODE']='1'
 journal=[];records={};started=time.monotonic()
 def pair(name,script,args):
  modes=[]
  for opt in (False,True):
   f=out/(name+('-O' if opt else '')+'.json');t=time.monotonic()
   cmd=[sys.executable]+(['-O'] if opt else [])+[str(src/script),*args,'--output',str(f)]
   p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=30)
   journal.append(dict(name=name,optimized=opt,exit=p.returncode,seconds=time.monotonic()-t,stdout=p.stdout,stderr=p.stderr))
   (out/'journal.json').write_text(json.dumps(journal,indent=2)+'\n');need(p.returncode==0,'child failure: '+name)
   modes.append(json.loads(f.read_text()))
  need(modes[0]==modes[1],'entire normal/optimized record equality: '+name);records[name]=modes[0]
 pair('controls','controls.py',[]);pair('tuples','tuple_check.py',[]);pair('field','field_check.py',[])
 lift=[]
 for N in (3702,3704):
  for lo in range(1,N+1,256):
   hi=min(N,lo+255);name=f'lift-{N}-{lo}-{hi}';pair(name,'lift_check.py',['--N',str(N),'--lo',str(lo),'--hi',str(hi)]);lift.append(records[name])
 need(sum(x['total'] for x in lift)==4562096,'full lift count')
 summary=dict(schema=1,controls=records['controls'],tuples=records['tuples'],field=records['field'],lift_shards=lift,lift_total=sum(x['total'] for x in lift),normal_optimized_pairs=len(records))
 data=(json.dumps(summary,indent=2,sort_keys=True)+'\n').encode();(out/'RESULT.json').write_bytes(data)
 receipt=dict(children=len(journal),whole_record_pairs=len(records),seconds=time.monotonic()-started,
  max_child_seconds=max(x['seconds'] for x in journal),fixed_child_guard_seconds=30,numerical_threads=1,
  result_bytes=len(data),result_sha256=hashlib.sha256(data).hexdigest(),python=sys.version)
 (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args();run(args.output)
