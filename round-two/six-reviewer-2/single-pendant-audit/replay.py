"""Serial portable replay: local generation followed by independent checking.
Every mathematical child has its own unchanged 60s alarm and 65s parent guard.
Generated certificates and entire matrices stay under the local output directory.
"""
from pathlib import Path
import os,sys,json,argparse,subprocess,time
from linear import need,digest,canonical
ROOT=Path(__file__).resolve().parent
THREADS=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',default='_generated');p.add_argument('--check');a=p.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);env=dict(os.environ)
 for k in THREADS:env[k]='1'
 mode=['-O'] if sys.flags.optimize else [];records={};validation=[]
 def run(name,args):
  start=time.monotonic();r=subprocess.run([sys.executable,'-B']+mode+args,cwd=ROOT,env=env,text=True,capture_output=True,timeout=65);validation.append({'stage':name,'code':r.returncode,'seconds':time.monotonic()-start});(out/(name+'.stderr')).write_text(r.stderr)
  need(r.returncode==0,'stage '+name+' failed: '+r.stderr[-1800:]);d=json.loads(r.stdout);(out/(name+'.json')).write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(name,file=sys.stderr,flush=True);return d
 for case in ['signs','anti','triangle','fixed_inverse','final']:
  d=run('generate-'+case,['cas.py','--case',case]);records['generate-'+case]=d;file=out/('generate-'+case+'.json')
  for name,ts in d['tests'].items():
   for test in ts:
    order=test['order'];key='check-'+name+'-'+str(order);records[key]=run(key,['checker.py',str(file),name,str(order)])
 for stage in ['bridges','cas_identities','controls']:records[stage]=run(stage,[stage+'.py'])
 for n,r,l in [(3,2,1),(4,3,1),(4,2,1),(5,3,1),(5,4,1)]:
  for phase in ['seed','old','strict']:
   name=f'original-{n}-{r}-{l}-{phase}';records[name]=run(name,['original.py',str(n),str(r),str(l),phase])
 for n,r,l in [(3,2,1),(4,3,1),(4,2,1),(5,3,1),(5,4,1),(6,5,1)]:
  name=f'original-{n}-{r}-{l}-physical';records[name]=run(name,['original.py',str(n),str(r),str(l),'physical'])
 records['damages']=run('damages',['damages.py',str(out)])
 entire={'schema':'six-reviewer-2/single-pendant/v1','mathematical_records':records};full_hash=digest(entire);(out/'full-record.json').write_text(json.dumps(canonical(entire),sort_keys=True,separators=(',',':'))+'\n');summary={'whole_record_sha256':full_hash,'stage_hashes':{k:digest(v) for k,v in records.items()},'uniform_obligations':sum(k.startswith('check-')for k in records),'uniform_positive_coefficients':sum(v['coefficient_count']for k,v in records.items() if k.startswith('check-')),'uniform_identity_points':sum(v['all_grid_points']for k,v in records.items() if k.startswith('check-')),'literal_whole_positions_per_phase':sum(v['whole_positions']for k,v in records.items()if k.startswith('original-')and v.get('phase')=='seed'),'literal_physical_fixtures':6,'physical_changed_positions':sum(v['whole_changed_positions']for k,v in records.items()if k.endswith('physical'))}
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'timing.json').write_text(json.dumps(validation,indent=2)+'\n')
 if a.check:need(json.loads(Path(a.check).read_text())==summary,'ENTIRE compact expected record mismatch')
 print(json.dumps(summary,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
