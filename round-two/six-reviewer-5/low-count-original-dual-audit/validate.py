"""Serial guarded cold full-record comparisons and mathematical damage controls."""
import pathlib,subprocess,sys,os,json,hashlib,time,tempfile,shutil,resource
P=pathlib.Path(__file__).resolve().parent
CAS=pathlib.Path(sys.argv[1]).resolve();EXPECTED=json.loads((P/'RECORD.json').read_text())
env=os.environ.copy()
for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']:env[key]='1'
receipts=[];begin=time.monotonic()
def run(name,root,mode,which='finite',reject=False):
 if which=='literal':a=['-c','import sys;sys.path.insert(0,'+repr(str(root))+');from energy import literal;import json;print(json.dumps([literal(8,8),literal(10,8),literal(12,9)],sort_keys=True))']
 else:a=[str(root/(which+'.py')),str(CAS) if which=='symbolic' else str(root/'finite-input.json')]
 t=time.monotonic();r=subprocess.run([sys.executable,'-I','-B',*(['-O'] if mode else []),*a],capture_output=True,env=env,timeout=45)
 if reject:
  if r.returncode==0:raise ValueError('mathematical damage accepted '+name)
 else:
  if r.returncode:raise ValueError('positive failed '+name+' '+r.stderr.decode())
  if json.loads(r.stdout)!=EXPECTED[which]:raise ValueError('whole record mismatch '+name)
 receipts.append({'name':name,'optimized':bool(mode),'seconds':time.monotonic()-t,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()})
for mode in (0,1):
 for which in ('symbolic','finite','literal'):run(which,P,mode,which)
 for kind in ('omitted-point','duplicate-point','coordinate-key','changed-vector','negative-weight','changed-constant','changed-slope','wrong-count'):
  with tempfile.TemporaryDirectory(prefix='dual-damage-',dir=P/'work') as d:
   root=pathlib.Path(d)
   for n in ('energy.py','finite.py'):shutil.copyfile(P/n,root/n)
   x=json.loads((P/'finite-input.json').read_text())
   if kind=='omitted-point':x['points'].pop()
   elif kind=='duplicate-point':x['points'][-1]=x['points'][-2]
   elif kind=='coordinate-key':x['coordinate_order'][0][0]=1
   elif kind=='changed-vector':x['points'][0]['lower'][8]='0'
   elif kind=='negative-weight':x['points'][0]['positive_weights'][0]='-1'
   elif kind=='changed-constant':x['points'][0]['whole_original_affine_sum'][0]='1'
   elif kind=='changed-slope':x['points'][0]['whole_original_affine_sum'][1]='1'
   elif kind=='wrong-count':x['points'][0]['k']=7
   (root/'finite-input.json').write_text(json.dumps(x));run(kind,root,mode,reject=True)
 for kind,old,new,which in [('physical-mass','m=[choose(k,z)*choose(q-k,w)','m=[2*choose(k,z)*choose(q-k,w)','symbolic'),('cap-J','-m[i]*m[j]-out[0][i][j]','-out[0][i][j]','symbolic'),('empty-metric','-sum((a*b for a,b in zip(m,x)),N*0)**2/N','', 'symbolic'),('lower-table-sign','(6/q-q-4)/(q-1)','(6/q+q-4)/(q-1)','symbolic')]:
  with tempfile.TemporaryDirectory(prefix='core-damage-',dir=P/'work') as d:
   root=pathlib.Path(d)
   for n in ('energy.py','finite.py','symbolic.py'):shutil.copyfile(P/n,root/n)
   s=(root/'energy.py').read_text()
   if s.count(old)!=1:raise ValueError('damage site '+kind)
   (root/'energy.py').write_text(s.replace(old,new));run(kind,root,mode,which,reject=True)
summary={'all_6_complete_positive_records_match':True,'semantic_damage_rejections':24,'guard_seconds':45,'native_threads':1,'serial_children':True,'children':receipts,'seconds':time.monotonic()-begin,'children_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'versions':{'python':sys.version.split()[0],'sympy':EXPECTED['symbolic']['sympy']},'unformalized':True}
(P/'VALIDATION.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='children'},indent=2))
