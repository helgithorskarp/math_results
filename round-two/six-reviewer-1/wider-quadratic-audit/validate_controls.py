from pathlib import Path
import datetime,json,subprocess,os,hashlib,shutil,time,resource,sys,tempfile
src=Path(__file__).resolve().parent;cold=Path(tempfile.mkdtemp(prefix='wider-audit-'))
files=['core.py','owned_effective.py','validate.py','EXPECTED.json']
keys=['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']
env=dict(os.environ)
for k in keys:env[k]='1'
py=sys.executable;checks=[]
def run(args,label,success=True,cwd=None):
    t=time.monotonic();p=subprocess.run(args,capture_output=True,text=True,env=env,cwd=cwd,timeout=45)
    if (p.returncode==0)!=success:raise ValueError(label+'\n'+p.stdout+'\n'+p.stderr)
    checks.append({'label':label,'expected_success':success,'returncode':p.returncode,'seconds':round(time.monotonic()-t,6),'stdout':p.stdout.strip()[:1000],'stderr_tail':p.stderr.strip()[-350:]if not success else''})
    return p
shutil.copyfile(src/'core.py',cold/'core.py');shutil.copyfile(src/'owned_effective.py',cold/'owned_effective.py')
run([py,'-B','-c',"import core,json; from pathlib import Path; Path('EXPECTED.json').write_text(json.dumps(core.build(),sort_keys=True,separators=(',',':'))+'\\n')"],'author complete independent record before target access',cwd=cold)
for n in files:shutil.copyfile(src/n,cold/n)
summaries=[]
for mode in [[],['-O']]:
    summaries.append(json.loads(run([py,'-B',*mode,str(src/'validate.py')],('optimized'if mode else'normal')+' whole record').stdout))
    summaries.append(json.loads(run([py,'-B',*mode,str(cold/'validate.py')],('optimized'if mode else'normal')+' cold whole record').stdout))
if not all(x==summaries[0]for x in summaries):raise ValueError('whole cold normal optimized equality')
# Mathematical build-only damage: NO EXPECTED fixture is read on these calls.
configs=[
 ('invalid-alpha3over4',"{'alpha':core.F(3,4)}"),
 ('unjustified-Vbelow4eta',"{'final_variance':core.F(4)}"),
 ('missing-fourth-phase-degree3',"{'lower_degree3_present':False}"),
 ('truncated-fine-normal1over8',"{'fine_normal':core.F(1,8)}"),
 ('overstrong-objective237',"{'new_objective':core.F(237)}"),
 ('overstrong-physical267',"{'new_physical':core.F(267)}"),
 ('objective238-used-as-physical',"{'new_physical':core.F(238)}"),
 ('invalid-imaginary-quadratic30',"{'imaginary_quadratic':core.F(30)}"),
 ('invalid-full-motion9',"{'motion_delta':core.F(9)}"),
]
for name,config in configs:
    run([py,'-B','-O','-c','import core;core.build('+config+')'],name+' mathematical build-only rejection',False,cwd=cold)
original=(src/'core.py').read_text()
damages=[
 ('missing-signed-cubic-Q-elimination','elimination=8*eta-replacement-Q/2+(vvP+3*Q)/4','elimination=8*eta-replacement+(vvP+3*Q)/4'),
 ('wrong-Laplace-cubic-sign','*(-1)**j*X**(n-2*j)','*X**(n-2*j)'),
 ('wrong-full-physical-square','(ee/2-kv*wc)**2-kv*kv*wc*wc','(ee/2-kv*wc)**2-kv*kv*wc*wc/2'),
 ('damaged-eighth-coordinate','xs.append(-sum(xs,R()));ys.append(-sum(ys,R()))','xs.append(-sum(xs,R())/2);ys.append(-sum(ys,R()))'),
]
for name,old,new in damages:
    if original.count(old)!=1:raise ValueError('unique source damage '+name)
    (cold/'core.py').write_text(original.replace(old,new))
    run([py,'-B','-O','-c','import core;core.build()'],name+' mathematical build-only rejection',False,cwd=cold)
(cold/'core.py').write_text(original)
record=json.loads((src/'EXPECTED.json').read_text());variants=[]
def damage(name,fn):
    v=json.loads(json.dumps(record));fn(v);variants.append((name,json.dumps(v)))
damage('bool-schema',lambda v:v.update(schema=True))
damage('floating-endpoint',lambda v:v['whole_arithmetic'].update(endpoint=0.0000625))
damage('missing-last-phase',lambda v:v['whole_phase_table'].pop())
damage('missing-full-SOS-coefficient',lambda v:next(i for i in v['whole_identities']if i['name']=='WHOLE centered quartic SOS')['whole_rational_map'].pop())
damage('missing-last-control-phase',lambda v:v['fresh_Gaussian_controls'][-1]['whole_nine_phase_values'].pop())
damage('changed-last-source-value',lambda v:v.update(trust='damaged'))
damage('removed-degree12-coefficient',lambda v:v['whole_Legendre_through_degree12'][-1]['whole_coefficients'].pop())
damage('lost-fine-degree3-budget',lambda v:v['whole_arithmetic']['fine_Bj'].pop('3'))
variants.extend([('nonfinite','{"schema":NaN}'),('duplicate','{"schema":1,"schema":1}')])
for name,body in variants:
    f=cold/'damaged.json';f.write_text(body)
    run([py,'-B','-O',str(cold/'validate.py'),'--fixture',str(f)],name+' malformed whole typed record rejection',False)
receipt={'agent':'six-reviewer-1','role':'independent mathematical reviewer','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Independent full written-proof reconstruction BEFORE target native access; OWN345e13e primitives disclosed; old helper compute/literal_controls not called.','python':subprocess.run([py,'--version'],capture_output=True,text=True,check=True).stdout.strip(),'thread_environment':{k:env[k]for k in keys},'normal_optimized_cold_whole_record_equal':True,'whole_record_sha256':summaries[0]['whole_record_sha256'],'summary':summaries[0],'math_build_only_rejections':len(configs)+len(damages),'optimized_whole_fixture_rejections':len(variants),'checks':checks,'source_hashes':{n:hashlib.sha256((src/n).read_bytes()).hexdigest()for n in files},'peak_child_maxrss_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'scope':'One serial exact math child; fixed45s per child; unchanged1CPU2GiB/native threads1. All universal analytic bridges ordinary and unformalized.'}
for check in receipt['checks']:
    check['stderr_tail']=check['stderr_tail'].replace(str(src),'<source>').replace(str(cold),'<isolated>')
(src/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
shutil.rmtree(cold)
print(json.dumps({k:v for k,v in receipt.items()if k not in ['checks','source_hashes']},indent=2))
