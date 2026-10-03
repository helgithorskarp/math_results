"""Cold source-only serial replay; fixed20-second initial guards; normal/optimized."""
import argparse,sys,os,subprocess,time,json,resource,hashlib
from pathlib import Path
from exact import need,canon
p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--result',required=True);args=p.parse_args();work=Path(args.work).resolve();need(not work.exists(),'fresh work directory');work.mkdir(parents=True);source=Path(__file__).resolve().parent;env=os.environ.copy()
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[key]='1'
env['PYTHONDONTWRITEBYTECODE']='1';rows=[];started=time.monotonic();modes=[]
for flags,name in [([], 'normal'),(['-O'],'optimized')]:
 dest=work/name;dest.mkdir();ldl=dest/'congruence.json';poly=dest/'polynomial.json';face=dest/'affine.json';controls=dest/'damages.json'
 calls=[('produce.py',[str(ldl)]),('check.py',[str(ldl),str(poly)]),('face.py',[str(face)]),('controls.py',[str(ldl),str(controls)])]
 for file,tail in calls:
  t=time.monotonic();r=subprocess.run([sys.executable,*flags,'-B',str(source/file),*tail],env=env,capture_output=True,text=True,timeout=20);seconds=time.monotonic()-t
  (dest/(file+'.stdout')).write_text(r.stdout);(dest/(file+'.stderr')).write_text(r.stderr);need(r.returncode==0,file+' failed: '+r.stderr)
  rows.append(dict(mode=name,child=file,seconds=seconds,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,exit_code=r.returncode))
 modes.append(dest)
for f in ['congruence.json','polynomial.json','affine.json','damages.json']:need((modes[0]/f).read_bytes()==(modes[1]/f).read_bytes(),'WHOLE mode equality '+f)
ldl=json.loads((modes[0]/'congruence.json').read_text());poly=json.loads((modes[0]/'polynomial.json').read_text());face=json.loads((modes[0]/'affine.json').read_text());damage=json.loads((modes[0]/'damages.json').read_text())
files={f:{'bytes':(modes[0]/f).stat().st_size,'sha256':hashlib.sha256((modes[0]/f).read_bytes()).hexdigest()}for f in ['congruence.json','polynomial.json','affine.json','damages.json']}
result=dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',python=sys.version.split()[0],all_complete=True,whole_normal_optimized_equal=True,child_guard_seconds=20,native_threads=1,serial_mathematical_children=len(rows),timings=rows,total_seconds=time.monotonic()-started,files=files,semantic_damages_per_mode=damage['damage_count'],affine_probes=face['probe_count'],affine_table_entries=face['table_entries'],affine_physical_entries=face['physical_entries'],cases=[dict(n=c['n'],N=c['N'],s=c['s'],h=c['h'],floor=c['floor'],coordinate_count=c['coordinate_count'],q=c['q'],lower_rank=c['lower_rank'],upper_rank=c['upper_rank'],gap=c['gap'],original=c['original'],sector_dimensions=[len(p['layers'])for p in c['parts']],lower_nullities=[len(p['layers'])-p['lower_rank']for p in c['parts']],minimum_classes=z['minimum_classes'],unique_equality_absent_profiles=z['unique_absent_profiles'],class_subset_count=len(z['all_absent_class_subsets']),entire_polynomial_record_hash=hashlib.sha256(canon(z)).hexdigest())for c,z in zip(ldl['cases'],poly['cases'],strict=True)])
Path(args.result).write_bytes(json.dumps(result,indent=2).encode()+b'\n');print(json.dumps(result,indent=2))
