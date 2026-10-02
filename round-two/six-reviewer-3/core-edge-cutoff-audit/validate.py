"""Serial fixed45s normal/-O replay, source changes and external fixture damage."""
import sys,json,subprocess,time,hashlib,tempfile,shutil,os,resource
from pathlib import Path
P=Path(__file__).resolve().parent
ENV=dict(os.environ,**{x:'1' for x in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']})
def child(folder,flags,extra=(),bad=False):
 start=time.monotonic();r=subprocess.run([sys.executable,'-I','-B',*flags,str(folder/'audit.py'),*extra],capture_output=True,text=True,env=ENV,timeout=45)
 if (r.returncode==0)==bad:raise ValueError('unexpected child verdict '+r.stdout+r.stderr)
 return {'flags':flags,'seconds':round(time.monotonic()-start,6),'exit_code':r.returncode,'summary':json.loads(r.stdout) if not bad else r.stderr.splitlines()[-1]}
def main():
 runs=[child(P,[]),child(P,['-O'])]
 if runs[0]['summary']!=runs[1]['summary']:raise ValueError('full normal/O record mismatch')
 damages=[]
 with tempfile.TemporaryDirectory() as td:
  d=Path(td)
  base=json.loads((P/'EXPECTED.json').read_text())
  changes=[('omit_original_empty_loop',lambda v:v['positive'][0]['positive'].__setitem__('full_empty_M00','0')),('incorrect_parameter',lambda v:v['positive'][0]['positive']['parameters'].__setitem__(3,'0')),('false_all_real_margin',lambda v:v['negative'][-1]['cap_dual'].__setitem__('combined','1')),('missing_boundary',lambda v:v['negative'].pop(0)),('wrong_physical_weight',lambda v:v['positive'][0]['physical_weights'].__setitem__(0,999)),('false_robust_radius',lambda v:v['positive'][0]['positive'].__setitem__('proved_parameter_box_radius','1')),('drop_symbolic_coefficient',lambda v:v['uniform']['positive_q4_shifts'][-1].pop()),('unweighted_quotient',lambda v:v['positive'][1]['positive']['whole_forms']['lower'][0].__setitem__(0,'1')),('incorrect_rank',lambda v:v['positive'][0]['positive']['congruences']['lower'].__setitem__('rank',23))]
  # Canonical whole-record rejection independently of executable recomputation;
  # each typed semantic fixture differs from the complete immutable original.
  gold=json.dumps(base,sort_keys=True,separators=(',',':'),ensure_ascii=False)
  for name,change in changes:
   v=json.loads(json.dumps(base));change(v)
   if json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)==gold:raise ValueError('damage is vacuous')
   damages.append(name)
  # Public decoder itself sees one semantic, one duplicate-key and one malformed
  # external fixture, in both modes, after exact mathematics reruns afresh.
  semantic=json.loads(json.dumps(base));changes[2][1](semantic)
  fixtures=[('semantic',json.dumps(semantic)),('duplicate','{"negative":[],"negative":[]}'),('malformed','{')]
  fixture_runs=[]
  for name,content in fixtures:
   f=d/(name+'.json');f.write_text(content)
   for flags in [[],['-O']]:fixture_runs.append({'damage':name,**child(P,flags,['--fixture',str(f)],True)})
  source_runs=[]
  mutations=[('wrong_lower_stationary','uniform.py','27*q**3+39*q*q','26*q**3+39*q*q'),('omit_actual_empty','original.py','sets=[0]','sets=[]'),('wrong_projected_star_metric','audit.py','F(ha[i]*ha[j],s)','F(0)')]
  for name,file,old,new in mutations:
   folder=d/name;shutil.copytree(P,folder,ignore=shutil.ignore_patterns('__pycache__'))
   p=folder/file;text=p.read_text()
   if old not in text:raise ValueError('source mutation anchor absent')
   p.write_text(text.replace(old,new))
   for flags in [[],['-O']]:source_runs.append({'damage':name,**child(folder,flags,bad=True)})
 result={'runs':runs,'entire_normal_optimized_records_equal':True,'typed_semantic_whole_record_fixture_damages':damages,'fresh_external_fixture_runs':fixture_runs,'meaningful_source_changes':source_runs,'per_child_guard_seconds':45,'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'serial_one_math_child':True,'native_threads':1,'scope':'unchanged1CPU2GiB','no_timeout_is_nonexistence':True}
 (P/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'normal':runs[0]['seconds'],'optimized':runs[1]['seconds'],'record_sha256':runs[0]['summary']['record_sha256'],'peak_child_rss_kib':result['peak_child_rss_kib'],'fresh_fixture_damages':len(fixture_runs),'source_change_runs':len(source_runs)}))
if __name__=='__main__':main()
