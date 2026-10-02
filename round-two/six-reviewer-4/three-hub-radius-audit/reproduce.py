"""Serial offline cold audit. Full regenerated corpora stay in requested scratch."""
import argparse,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
from rows import need,encoded

def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent;work=a.work.resolve();need(not work.exists(),'fresh work directory');work.mkdir(parents=True)
 env={**os.environ,**{k:'1'for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']}}
 mode=['-O']if sys.flags.optimize else[];receipts=[];started=time.monotonic()
 sources={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest()for f in root.rglob('*')if f.is_file()and '__pycache__'not in f.parts}
 def execute(name,args):
  t=time.monotonic();r=subprocess.run([sys.executable,*mode,*args],env=env,capture_output=True,timeout=60)
  (work/(name+'.stdout')).write_bytes(r.stdout);(work/(name+'.stderr')).write_bytes(r.stderr)
  receipts.append({'stage':name,'seconds':round(time.monotonic()-t,6),'returncode':r.returncode,'guard_seconds':60})
  need(r.returncode==0,'failed/incomplete '+name);return r.stdout
 execute('population',[str(root/'populations.py'),'--input',str(root/'fixtures.json'),'--out',str(work/'record.json')])
 radius=execute('radius',[str(root/'radius.py')]);controls=execute('controls',[str(root/'controls.py'),'--input',str(root/'fixtures.json'),'--record',str(work/'record.json')])
 producer=work/'original-producer.json';verifier=work/'original-verifier.json'
 execute('original-producer',[str(root/'original/produce.py'),'--fixtures',str(root/'fixtures.json'),'--out',str(producer)])
 execute('original-verifier',[str(root/'original/verify.py'),'--fixtures',str(root/'fixtures.json'),'--expected',str(root/'original/expected.json'),'--out',str(verifier)])
 need(producer.read_bytes()==verifier.read_bytes(),'entire unchanged native producer/checker record')
 script="import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[1]);import controls;print(json.dumps(controls.run(json.loads(Path(sys.argv[2]).read_text()),json.loads(Path(sys.argv[3]).read_text())),sort_keys=True,separators=(',',':')))"
 native_controls=execute('original-controls',['-c',script,str(root/'original'),str(root/'fixtures.json'),str(root/'original/expected.json')])
 corroboration=execute('corroboration',[str(root/'corroborate.py'),'--own',str(work/'record.json'),'--original',str(producer),'--expected',str(root/'original/expected.json')])
 raw=(work/'record.json').read_bytes();z=json.loads(raw)
 result={'whole_independent_record_bytes':len(raw),'whole_independent_record_sha256':hashlib.sha256(raw).hexdigest(),
  'physical_rows':len(z['physical']),'types':len(z['types']),'branches':len(z['branches']),
  'raw_populations':sum(len(b['records'])for b in z['branches']),
  'raw_by_branch':[[b[k]for k in ('Q','T','X','tau')]+[len(b['records'])]for b in z['branches']],
  'necessary_survivors':sum(r['failure']is None for b in z['branches']for r in b['records']),
  'final_support':z['final_support'],'radius':json.loads(radius),'controls':json.loads(controls),'corroboration':json.loads(corroboration),'native_controls':json.loads(native_controls)}
 stable=encoded(result);(work/'RESULT.json').write_bytes(stable)
 need(stable==(root/'expected.json').read_bytes(),'whole cold compact readout vs frozen exact bytes')
 first=json.loads((root/'first-seal.json').read_bytes())
 need(hashlib.sha256(raw).hexdigest()==first['whole_population_record_sha256'],'whole first sealed output')
 for f,digest in first['sources'].items():need(sources[f]==digest,'first sealed source changed')
 after={str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest()for f in root.rglob('*')if f.is_file()and '__pycache__'not in f.parts};need(after==sources,'source changed during replay')
 metadata={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','python':sys.version,'optimized':bool(sys.flags.optimize),'seconds':time.monotonic()-started,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'receipts':receipts,'source_sha256':sources,'threads':1,'serial_mathematical_children':1,'result_sha256':hashlib.sha256(stable).hexdigest(),'unchanged_scope':'1CPU2GiB','prefix_guard_updates':500000,'prefix_guard_seconds_per_branch':20}
 (work/'METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n')
 print(json.dumps({'status':'PASS_COMPLETE_COLD_REPLAY','seconds':metadata['seconds'],'peak_child_rss_kib':metadata['peak_child_rss_kib'],'result_sha256':metadata['result_sha256']},sort_keys=True))
if __name__=='__main__':main()
