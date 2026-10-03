"""Serial fixed20s cold normal/O reproduction; full byte comparisons."""
import argparse,hashlib,json,os,resource,subprocess,sys,time
from pathlib import Path
from exact import need
ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);ap.add_argument('--result',type=Path,required=True);args=ap.parse_args();need(not args.work.exists(),'fresh work path required');args.work.mkdir(parents=True);src=Path(__file__).resolve().parent;env=os.environ.copy();variables=['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']
for v in variables:env[v]='1'
timings=[]
def child(mode,name,*argv):
 cmd=[sys.executable,'-B']+(['-O']if mode=='optimized'else[])+[str(src/name),*map(str,argv)];t=time.monotonic();r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=20);timings.append(dict(mode=mode,child=name,args=list(map(str,argv)),seconds=time.monotonic()-t,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,exit_code=r.returncode));(args.work/(mode+'-'+name+'-'+str(len(timings))+'.stderr')).write_text(r.stderr);need(r.returncode==0,r.stderr)
for mode in ('normal','optimized'):
 work=args.work/mode;work.mkdir()
 for q in range(7,28):child(mode,'produce.py',q,work/f'q{q}-produce.json');child(mode,'check.py',work/f'q{q}-produce.json',work/f'q{q}-check.json')
 child(mode,'controls.py',work,work/'controls.json');print(mode,'complete21 entire cases and controls',flush=True)
files={};names=sorted(p.name for p in(args.work/'normal').glob('*.json'));need(len(names)==43,'entire output file census')
for name in names:
 a=(args.work/'normal'/name).read_bytes();b=(args.work/'optimized'/name).read_bytes();need(a==b,'entire normal/O bytes '+name);files[name]=dict(bytes=len(a),sha256=hashlib.sha256(a).hexdigest())
cases=[json.loads((args.work/'normal'/f'q{q}-check.json').read_text())for q in range(7,28)];positive=cases[-1];positive.pop('full_determinant_polynomials');separations=[dict(q=c['q'],bound=c['dyadic_spectral_separation'])for c in cases[:-1]];bound=min(__import__('fractions').Fraction(c['bound'])for c in separations);out=dict(actual_agent='six-reviewer-4',role='independent mathematical reviewer',python=sys.version.split()[0],all_complete=True,whole_normal_optimized_equal=True,child_guard_seconds=20,native_threads={v:1 for v in variables},serial_mathematical_children=len(timings),timings=timings,total_seconds=sum(t['seconds']for t in timings),complete_output_files=files,negative_order_count=20,positive_order=27,original_ordered_pairs=sum(c['ordered_pairs']for c in cases),physical_form_entries=sum(c['physical_form_entries']for c in cases),dual_plane_count=sum(c['dual_planes']for c in cases[:-1]),dyadic_separations=separations,common_dyadic_spectral_separation=str(bound),positive=positive,semantic_damages_per_mode=21,singular_positive_controls_per_mode=3)
args.result.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('PASS whole source-only normal/O computation; result',args.result)
