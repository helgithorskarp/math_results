"""Concrete damaged obligations and original-space mutations must reject."""
import copy,json,os,subprocess,sys,tempfile,shutil,time
from pathlib import Path
from audit import symbolic
from polycheck import P
ROOT=Path(__file__).resolve().parent
BASE=json.loads((ROOT/'CERTIFICATE.json').read_text())
def damaged():
 cases=[]
 def add(name,fn):
  data=copy.deepcopy(BASE);fn(data);cases.append((name,data))
 add('missing_whole_block',lambda x:x.pop())
 add('reordered_whole_blocks',lambda x:x.reverse())
 add('omitted_final_pivot',lambda x:x[4]['pivots'].pop())
 add('omitted_last_update',lambda x:x[4]['updates'].pop())
 add('detached_update_order',lambda x:x[4]['updates'].reverse())
 add('changed_original_cap_entry',lambda x:x[4]['original'][0][0]['n'][0][1].__setitem__(0,x[4]['original'][0][0]['n'][0][1][0]+1))
 add('changed_original_metric',lambda x:x[4]['metric'][0]['n'][0][1].__setitem__(0,x[4]['metric'][0]['n'][0][1][0]+1))
 add('changed_pivot',lambda x:x[4]['pivots'][-1]['n'][0][1].__setitem__(0,x[4]['pivots'][-1]['n'][0][1][0]+1))
 add('changed_update_result',lambda x:x[4]['updates'][-1]['after']['n'][0][1].__setitem__(0,x[4]['updates'][-1]['after']['n'][0][1][0]+1))
 add('missing_old_R_direction',lambda x:x[5]['original'].pop())
 add('boolean_polynomial_exponent',lambda x:x[0]['original'][0][0]['n'][0][0].__setitem__(0,True))
 add('duplicate_monomial',lambda x:x[0]['original'][0][0]['n'].append(x[0]['original'][0][0]['n'][0]))
 return cases

def main():
 results=[]
 for name,data in damaged():
  try:symbolic(data)
  except (ValueError,StopIteration)as e:results.append(dict(name=name,rejected=True,error_type=type(e).__name__,error=str(e)if str(e)else 'missing ordered update in deliberately damaged finite certificate'))
  else:raise ValueError('damaged certificate accepted '+name)
 try:P({(1,0):1,(0,0):-3}).positive()
 except ValueError as e:results.append(dict(name='negative_shift_constant',rejected=True,error=str(e)))
 else:raise ValueError('false unbounded sign accepted')
 mutations=[
 ('omit_actual_empty_frame','sectors.py','(1,[-1/(2*ell),1/(2*ell),-1/ell,zero,zero])','(0,[-1/(2*ell),1/(2*ell),-1/ell,zero,zero])','audit'),
 ('wrong_old_row_multiplicity','sectors.py','(q,[1/(2*(q-1)),zero,zero,zero,zero])','(q-1,[1/(2*(q-1)),zero,zero,zero,zero])','audit'),
 ('wrong_contrast_metric','sectors.py','gs=[2*s/3,12*s,2*beta,2*nu]','gs=[2*s/3,6*s,2*beta,2*nu]','audit'),
 ('drop_untouched_old_contrast','literal.py','for k in range(1,q-1):','for k in range(1,q-2):','literal'),
 ('wrong_actual_empty_repair_loop','literal.py','Qr[0][0]=sum(sum(row)for row in Core)','Qr[0][0]=sum(sum(row)for row in Core)+delta','literal')]
 work=ROOT/'work';work.mkdir(exist_ok=True);env=os.environ.copy()
 for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[k]='1'
 for name,file,before,after,script in mutations:
  with tempfile.TemporaryDirectory(dir=work,prefix='damage-')as d:
   directory=Path(d)
   for p in ROOT.iterdir():
    if p.is_file()and(p.suffix=='.py'or p.name=='CERTIFICATE.json'):shutil.copyfile(p,directory/p.name)
   text=(directory/file).read_text()
   if text.count(before)!=1:raise ValueError('controlled mutation not unique '+name)
   (directory/file).write_text(text.replace(before,after))
   args=[directory/(script+'.py'),directory/'CERTIFICATE.json']if script=='audit'else[directory/'literal.py','4','2']
   start=time.monotonic();r=subprocess.run([sys.executable,'-B',*(['-O']if sys.flags.optimize else []),*[str(a)for a in args]],env=env,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30)
   if r.returncode!=1 or 'ValueError:'not in r.stderr or r.stdout:raise ValueError('mutation rejection not a mathematical failure '+name+' '+r.stderr)
   results.append(dict(name=name,rejected=True,error=r.stderr.split('ValueError:')[-1].strip()))
 print(json.dumps(dict(semantic_rejections=results,complete=True,no_timeout_kill_incomplete_adopted=True),sort_keys=True,separators=(',',':')))
if __name__=='__main__':main()
