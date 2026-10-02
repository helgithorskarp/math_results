from pathlib import Path
import datetime,json,subprocess,os,hashlib,shutil,time,resource,sys,tempfile
src=Path(__file__).resolve().parent; temp=tempfile.TemporaryDirectory(prefix='reviewer1-mean-square-');cold=Path(temp.name)
files=['core.py','owned_core.py','owned_centered.py','validate.py','EXPECTED.json']
env=os.environ.copy()
keys=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']
for k in keys:env[k]='1'
py=sys.executable;checks=[]
def run(args,label,success=True,cwd=None):
    t=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,env=env,cwd=cwd,timeout=45)
    if (p.returncode==0)!=success:raise ValueError(label+'\n'+p.stdout+'\n'+p.stderr)
    checks.append({'label':label,'expected_success':success,'returncode':p.returncode,'seconds':round(time.monotonic()-t,6),'stdout':p.stdout.strip()[:1000],'stderr_tail':p.stderr.strip()[-400:]if not success else''});return p
for n in files:shutil.copyfile(src/n,cold/n)
for mode in [[],['-O']]:
    run([py,'-B',*mode,str(src/'validate.py')],('optimized'if mode else'normal')+' whole record')
    run([py,'-B',*mode,str(cold/'validate.py')],('optimized'if mode else'normal')+' cold isolated whole record')
original=(src/'core.py').read_text()
mutations=[
 ('invalid-penalty8','-Q(39,5)*dm','-Q(8)*dm'),
 ('missing-quartic-majorant','bs[4]=sc(pw(v,2),Q(3,32))','bs[4]=sc(pw(v,2),Q(1,32))'),
 ('overstrong-first-coercivity','cut=Q(1,6)','cut=Q(1,4)'),
 ('overstrong-second-coercivity','cut=Q(4,9)','cut=Q(1,2)'),
 ('old-complex-gradient5/2',"'complex-gradient14/5',Q(14,5)-complex_","'complex-gradient14/5',Q(5,2)-complex_"),
 ('invalid-H39',"'retained-gap-actual-H40',40-","'retained-gap-actual-H40',39-"),
 ('old-displacementW6',"'whole-delta-W/5',Bd-5*Nc","'whole-delta-W/5',Bd-6*Nc"),
 ('wrong-entire-square',"-Q(1216,225)))","-Q(1200,225)))"),
 ('old-small-energy1/512',"'actual-H-entry1/375',Q(1,375)-42*e","'actual-H-entry1/375',Q(1,512)-42*e"),
 ('damaged-all-twolevel-ratio',"p3*p3==Q((8-2*k)**2,8*k*(8-k))*v**3","p3*p3==Q((8-2*k)**2,4*k*(8-k))*v**3")]
for name,old,new in mutations:
    if original.count(old)!=1:raise ValueError('unique damage '+name)
    (cold/'core.py').write_text(original.replace(old,new))
    run([py,'-B','-O','-c','import core;core.build()'],name+' build-only math rejection WITHOUT fixture',False,cwd=cold)
(cold/'core.py').write_text(original)
d=json.loads((src/'EXPECTED.json').read_text());variants=[]
def damage(name,alter):
    x=json.loads(json.dumps(d));alter(x);variants.append((name,json.dumps(x)))
damage('bool-schema',lambda x:x.update(schema=True))
damage('floating-endpoint',lambda x:x.update(eta_endpoint=0.0000625))
damage('truncated-polar',lambda x:x['polar']['streams']['mean']['coefficients'].pop())
damage('missing-sector',lambda x:x['sectors']['whole15_sector_integrals'].pop())
damage('missing-face-coefficient',lambda x:x['whole_radial_faces39over5'][0]['whole_coefficients'].pop())
damage('lost-ordered-Hessian',lambda x:x['fresh_Gaussian_controls'][0]['whole_ordered_Hessian'].pop())
damage('damaged-square',lambda x:x['whole_mean_square']['whole_completed'].pop())
variants += [('nonfinite','{"schema":NaN}'),('duplicate-key','{"schema":1,"schema":1}')]
for name,t in variants:
    f=cold/'damaged.json';f.write_text(t)
    run([py,'-B','-O',str(cold/'validate.py'),'--fixture',str(f)],name+' optimized malformed typed record rejection',False)
need_summary=json.loads(checks[0]['stdout'])
if need_summary!=json.loads(checks[2]['stdout']):raise ValueError('normal optimized whole summary')
receipt={'agent':'six-reviewer-1','role':'independent mathematical reviewer','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'portable complete independent record checks, cold copies and semantic damages; owned arithmetic primitives credited','python':subprocess.run([py,'--version'],capture_output=True,text=True,check=True).stdout.strip(),'thread_environment':{k:env[k]for k in keys},'normal_optimized_cold_whole_record_equal':True,'whole_record_sha256':need_summary['whole_record_sha256'],'summary':need_summary,'math_damage_build_only_rejections':len(mutations),'optimized_fixture_rejections':len(variants),'checks':checks,'source_hashes':{n:hashlib.sha256((src/n).read_bytes()).hexdigest()for n in files},'peak_child_maxrss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'scope':'one serial math child, fixed45s each, unchanged1CPU2GiB'}
print(json.dumps({k:v for k,v in receipt.items()if k not in ['checks','source_hashes']},indent=2))
temp.cleanup()
