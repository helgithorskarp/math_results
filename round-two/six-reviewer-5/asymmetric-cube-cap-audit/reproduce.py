"""Source-only serial exact replay and semantic rejection controls."""
import argparse,hashlib,json,os,pathlib,resource,shutil,subprocess,sys,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(source,mode,cas_path,check_positive=True):
 env=os.environ.copy()
 for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[k]='1'
 code="import runpy,sys;sys.path.insert(0,sys.argv[2]) if sys.argv[2] else None;runpy.run_path(sys.argv[1],run_name='__main__')"
 args=[sys.executable,'-I','-B']+(['-O'] if mode else [])+['-c',code,str(source),cas_path or '']
 t=time.monotonic();r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=45)
 if check_positive and r.returncode:raise ValueError(r.stderr)
 if not check_positive and (r.returncode==0 or 'ValueError:' not in r.stderr):raise ValueError('damage must reject mathematically, not timeout/import/status')
 return dict(source=source.name,optimized=bool(mode),exit_code=r.returncode,seconds=time.monotonic()-t,peak_child_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cas-path');ap.add_argument('--controls',action='store_true');a=ap.parse_args();work=ROOT/'work';work.mkdir(exist_ok=True)
 expected=json.loads((ROOT/'expected.json').read_text());core=['field.py','original.py','polynomial.py','reproduce.py'];sealed={n:digest(ROOT/n) for n in core};runs=[];records=[]
 for mode in (False,True):
  for source in ('field.py','polynomial.py','original.py'):runs.append(run(ROOT/source,mode,a.cas_path))
  actual={n:digest(work/n) for n in expected}
  if actual!=expected:raise ValueError('whole independently regenerated mathematical records differ after arithmetic')
  records.append(actual)
 controls=[]
 if a.controls:
  changes=[('empty-frame',"allrows=[z]+rows","allrows=[mul(z,0)]+rows"),('light-mean',"mul(Bbar,3*l)","mul(Bbar,2*l)"),('empty-update',"u=[R(-3)]","u=[R(-2)]"),('private-full',"par['c']/(k-1)))]","par['c']/k))]"),('dual-heavy',"R(i==0)-R(1,h)","R(i==0)-R(2,h)"),('old-complement',"range(1,len(pairs))","range(1,len(pairs)-1)"),('mean-metric',"[[h*l*b['tau']]]","[[h*l*b['tau']+1]]"),('original-carrier',"sets.append(mem)","sets.append(mem|1)")]
  for mode in (False,True):
   for label,old,new in changes:
    with tempfile.TemporaryDirectory(prefix='damage-',dir=work) as tmp:
     D=pathlib.Path(tmp)
     for n in ('field.py','original.py','polynomial.py'):shutil.copyfile(ROOT/n,D/n)
     text=(D/'original.py').read_text()
     if text.count(old)!=1:raise ValueError('one precise mutation '+label)
     (D/'original.py').write_text(text.replace(old,new));(D/'work').mkdir()
     r=run(D/'original.py',mode,a.cas_path,False);controls.append(dict(label=label,**r))
   for label in ('missing-block','shift-sign','row-clear','leading-pivot'):
    with tempfile.TemporaryDirectory(prefix='damage-',dir=work) as tmp:
     D=pathlib.Path(tmp);shutil.copyfile(ROOT/'polynomial.py',D/'polynomial.py');(D/'work').mkdir();v=json.loads((work/'fresh-field-record.json').read_text())
     if label=='missing-block':del v['blocks']['old-difference']
     if label=='shift-sign':v['inverse_bound']['shifted_numerator'][0][1]='-1'
     if label=='row-clear':v['blocks']['aggregate-five']['cleared'][0][0][0][1]='1'
     if label=='leading-pivot':v['blocks']['aggregate-five']['pivots'][4]['numerator'][0][1]='1'
     (D/'work/fresh-field-record.json').write_text(json.dumps(v));r=run(D/'polynomial.py',mode,a.cas_path,False);controls.append(dict(label=label,**r))
 if sealed!={n:digest(ROOT/n) for n in core}:raise ValueError('core source changed during validation')
 out=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',python=sys.version.split()[0],positive_children=runs,all_six_whole_math_records_match=True,whole_math_records=records,semantic_damage_rejections=len(controls),controls=controls,unchanged_core=sealed,serial_children=1,native_threads=1,child_timeout_seconds=45,formalized=False)
 (work/'VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(dict(complete=True,positive_children=len(runs),semantic_rejections=len(controls),maximum_child_seconds=max(r['seconds'] for r in runs+controls),peak_KiB=max(r['peak_child_KiB'] for r in runs+controls),whole_record_hashes=records[0])))
if __name__=='__main__':main()
