#!/usr/bin/env python3
"""Serial cold source checks; each child has an unchanged45-second guard."""
import json,sys,subprocess,tempfile,time,os,resource,shutil,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
SOURCES=['poly.py','audit.py','literal.py']
SECTORS=['scalars','heavy-odd','light-odd','contrast','fixed']
ENV={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')}}
DAMAGES=[('physical_N','literal.py','N==6*h+10','N==6*h+9','literal'),('light_coefficient','audit.py','cl=24/(ell*s)','cl=25/(ell*s)','literal'),('private_even','literal.py','times(Wf(i),-F(1,2))','times(Wf(i),F(1,2))','literal'),('inverse_energy','literal.py','+4/d[\'bl\']','+3/d[\'bl\']','literal'),('actual_empty','literal.py','new[0][0]+=2*delta','new[0][0]+=delta','literal'),('fixed_empty_omitted','audit.py',"(zz,1)","(zz,0)",'fixed')]
def child(root,module,args,optimized=False,should_pass=True):
 cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+['-c',"import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_module('"+module+"',run_name='__main__')",str(root)]+args
 before=time.monotonic();r=subprocess.run(cmd,env=ENV,capture_output=True,text=True,timeout=45);sec=time.monotonic()-before
 if (r.returncode==0)!=should_pass:raise ValueError('unexpected child result '+r.stdout+r.stderr)
 return {'optimized':optimized,'seconds':sec,'exit_code':r.returncode,'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'last_line':(r.stdout or r.stderr).strip().splitlines()[-1]}
def main():
 result={'positive':[],'semantic_source_damages':[],'record_damages':[]}
 with tempfile.TemporaryDirectory(prefix='boundary-review-') as td:
  root=Path(td)
  for name in SOURCES:shutil.copyfile(BASE/name,root/name)
  for opt in (False,True):
   for sector in SECTORS:
    dest=root/(sector+'.json');r=child(root,'audit',['--sector',sector,'--output',str(dest),'--check',str(BASE/(sector+'.json'))],opt);r['sector']=sector;result['positive'].append(r)
   for h in (2,3,10):
    dest=root/('h'+str(h)+'.json');r=child(root,'literal',['--h',str(h),'--output',str(dest),'--check',str(BASE/('h'+str(h)+'.json'))],opt);r['h']=h;result['positive'].append(r)
  for name,file,before,after,kind in DAMAGES:
   for opt in (False,True):
    for f in SOURCES:shutil.copyfile(BASE/f,root/f)
    src=(root/file).read_text()
    if before not in src:raise ValueError('damage did not alter source')
    (root/file).write_text(src.replace(before,after))
    args=['--h','2','--output',str(root/'damaged.json')] if kind=='literal' else ['--sector','fixed','--output',str(root/'damaged.json')]
    r=child(root,'literal' if kind=='literal' else 'audit',args,opt,False);r['name']=name;result['semantic_source_damages'].append(r)
  for f in SOURCES:shutil.copyfile(BASE/f,root/f)
  for opt in (False,True):
   for name in ('missing_obligation','wrong_coefficient','boolean_coefficient'):
    o=json.loads((BASE/'scalars.json').read_text());
    if name=='missing_obligation':del o['signs']['ml']
    elif name=='wrong_coefficient':o['signs']['ah']['positive']['shifted_coefficients'][0]*=-1
    else:o['signs']['ah']['positive']['shifted_coefficients'][0]=True
    dest=root/'bad-record.json';dest.write_text(json.dumps(o));r=child(root,'audit',['--sector','scalars','--output',str(root/'new.json'),'--check',str(dest)],opt,False);r['name']=name;result['record_damages'].append(r)
 result['status']='PASS';result['guards']={'child_seconds':45,'native_threads':1,'cpu_jobs':1,'literal_h_max':10,'literal_N_max':70};result['seconds_total']=sum(r['seconds'] for group in ('positive','semantic_source_damages','record_damages') for r in result[group]);(BASE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','children':sum(len(result[k]) for k in ('positive','semantic_source_damages','record_damages')),'seconds':result['seconds_total'],'max_child_seconds':max(r['seconds'] for group in ('positive','semantic_source_damages','record_damages') for r in result[group])}))
if __name__=='__main__':main()
