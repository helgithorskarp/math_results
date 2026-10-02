"""Portable serial cold replay; complete mathematical output remains in scratch."""
import argparse,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path

def need(x,m):
 if not x:raise ValueError(m)
def main():
 p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
 root=Path(__file__).resolve().parent;work=a.work.resolve();need(not work.exists(),'fresh work directory required');work.mkdir(parents=True)
 expected=json.loads((root/'expected.json').read_bytes());cert=json.loads((root/'coefficient-certificate.json').read_bytes())
 before={f.name:hashlib.sha256(f.read_bytes()).hexdigest()for f in root.iterdir()if f.is_file()}
 env={**os.environ,**{k:'1'for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']}}
 opt=['-O']if sys.flags.optimize else[];receipts=[];start=time.monotonic()
 stages=[('census','census.py',['--input',str(root/'fixtures.json'),'--out',str(work/'record.json')]),
  ('controls','controls.py',['--input',str(root/'fixtures.json'),'--record',str(work/'record.json')]),
  ('baseline','baseline.py',['--input',str(root/'primary69.txt')])]
 for name,script,args in stages:
  t=time.monotonic();r=subprocess.run([sys.executable,*opt,str(root/script),*args],env=env,capture_output=True,timeout=45)
  (work/(name+'.stdout')).write_bytes(r.stdout);(work/(name+'.stderr')).write_bytes(r.stderr)
  receipts.append({'stage':name,'exit_code':r.returncode,'seconds':time.monotonic()-t,'guard_seconds':45})
  need(r.returncode==0,'failed/incomplete stage '+name)
 raw=(work/'record.json').read_bytes();record=json.loads(raw)
 need(len(raw)==expected['whole_record_bytes']and hashlib.sha256(raw).hexdigest()==expected['whole_record_sha256'],'complete first independent record')
 need(record['row_count']==expected['row_count']and record['in_scope_count']==expected['in_scope_count'],'carrier count')
 need(record['coefficient']==expected['coefficient']and record['boundaries']==expected['boundaries'],'every coefficient/category/composition field')
 need(json.loads((work/'controls.stdout').read_bytes())==expected['controls'],'all physical controls')
 need(json.loads((work/'baseline.stdout').read_bytes())==expected['baseline'],'literal primary calibration')
 lookup={(r['fixture'],tuple(r['hubs'])):r for r in record['rows']}
 for key in ['lower_witness','upper_witness']:
  r=cert[key];need(lookup[(r['fixture'],tuple(r['hubs']))]==r,'literal coefficient witness')
 need(cert['interval']==record['coefficient']['interval'],'whole coefficient interval')
 for ck,rk in [('all_lower_attaining_marks','lower_attaining_rows'),('all_upper_attaining_marks','upper_attaining_rows'),('off_scope_failures','off_scope_failures')]:
  need(cert[ck]==record['coefficient'][rk],'complete coefficient extrema/scope')
 after={f.name:hashlib.sha256(f.read_bytes()).hexdigest()for f in root.iterdir()if f.is_file()};need(before==after,'source bytes changed during cold replay')
 result={'whole_record_bytes':len(raw),'whole_record_sha256':hashlib.sha256(raw).hexdigest(),
  'rows':record['row_count'],'in_scope':record['in_scope_count'],'coefficient_interval':record['coefficient']['interval'],
  'boundary_compositions':[len(b['compositions'])for b in record['boundaries']],
  'controls':expected['controls'],'baseline':expected['baseline']}
 stable=(json.dumps(result,sort_keys=True,separators=(',',':'))+'\n').encode();(work/'RESULT.json').write_bytes(stable)
 metadata={'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','python':sys.version,'optimized':bool(sys.flags.optimize),
  'seconds':time.monotonic()-start,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'receipts':receipts,
  'source_sha256':before,'threads':1,'cpu_intensive_jobs':1,'guards':'45s/stage;100000 category state updates',
  'result_sha256':hashlib.sha256(stable).hexdigest()}
 (work/'METADATA.json').write_text(json.dumps(metadata,indent=2)+'\n')
 print(json.dumps({'status':'PASS_COMPLETE_INDEPENDENT_COLD_REPLAY','seconds':metadata['seconds'],'peak_child_rss_kib':metadata['peak_child_rss_kib'],
  'result_sha256':metadata['result_sha256'],'whole_record_sha256':result['whole_record_sha256']},sort_keys=True))
if __name__=='__main__':main()
