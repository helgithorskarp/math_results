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
 for case in ['uniform','signs','anti','pendant','triangle','fixed_inverse','final']:
  args=['cas.py']+([] if case=='uniform' else ['--boundary','--case',case]);d=run('generate-'+case,args);records['generate-'+case]=d;file=out/('generate-'+case+'.json');orders=[('signs',0)] if case=='signs' else [(name,t['order']) for name,ts in d['tests'].items() for t in ts]
  for name,order in orders:records['check-'+case+'-'+str(order)]=run('check-'+case+'-'+str(order),['checker.py',str(file),name,str(order)])
 for stage in ['bridges','cas_identities','controls']:records[stage]=run(stage,[stage+'.py'])
 for n,r,l in [(4,2,2),(5,2,3),(5,3,2)]:
  for phase in ['seed','old','strict','physical']:
   name=f'original-{n}-{r}-{l}-{phase}';records[name]=run(name,['original.py',str(n),str(r),str(l),phase])
 for n,r,l in [(6,3,3),(6,4,2)]:
  name=f'original-{n}-{r}-{l}-physical';records[name]=run(name,['original.py',str(n),str(r),str(l),'physical'])
 records['damages']=run('damages',['damages.py',str(out)])
 entire={'schema':'six-reviewer-2/unbounded-mixed-cap/v1','mathematical_records':records};full_hash=digest(entire);(out/'full-record.json').write_text(json.dumps(canonical(entire),sort_keys=True,separators=(',',':'))+'\n');summary={'whole_record_sha256':full_hash,'stage_hashes':{k:digest(v) for k,v in records.items()},'boundary_minor_positive_coefficients':sum(x['coefficient_count'] for k,v in records.items() if k.startswith('check-') and k not in ['check-signs-0'] and 'uniform' not in k for x in [v]),'boundary_identity_points':sum(v.get('all_grid_points',0) for k,v in records.items() if k.startswith('check-') and 'uniform' not in k),'uniform_identity_points':sum(v.get('all_grid_points',0) for k,v in records.items() if k.startswith('check-uniform-')),'literal_whole_positions_per_phase':sum(v['whole_positions'] for k,v in records.items() if k.startswith('original-') and v.get('phase')=='seed'),'literal_physical_fixtures':5}
 (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(out/'timing.json').write_text(json.dumps(validation,indent=2)+'\n')
 if a.check:need(json.loads(Path(a.check).read_text())==summary,'ENTIRE compact expected record mismatch')
 print(json.dumps(summary,sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
