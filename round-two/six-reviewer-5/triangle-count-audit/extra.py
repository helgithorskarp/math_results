import pathlib,subprocess,os,json,time,hashlib,resource,sys
P=pathlib.Path(__file__).resolve().parent;env=os.environ.copy()
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
rows=[];outputs=[]
def run(mode,label,script,args,cas=False,reject=False):
 cmd=[sys.executable,'-I','-B']+(['-O'] if mode=='optimized' else [])
 if cas and env.get('REVIEW_SYMPY_PATH'):cmd+=['-c',"import sys,runpy;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",env['REVIEW_SYMPY_PATH'],str(P/script)]
 else:cmd+=[str(P/script)]
 pause=env.get('RESEARCH_PAUSE_DIR')
 if pause and any((pathlib.Path(pause)/n).exists() for n in ['PAUSED','PAUSED.json','HANDOVER','HANDOVER.json']):raise RuntimeError('operational barrier')
 cmd+=list(map(str,args));t=time.monotonic();r=subprocess.run(cmd,env=env,capture_output=True,timeout=55)
 name='supp-'+mode+'-'+label;(P/(name+'.stdout')).write_bytes(r.stdout);(P/(name+'.stderr')).write_bytes(r.stderr)
 if (not reject and r.returncode!=0) or (reject and r.returncode==0):raise RuntimeError(name+' '+r.stderr.decode()[-1500:])
 rows.append(dict(mode=mode,label=label,returncode=r.returncode,seconds=time.monotonic()-t,peak_child_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,bytes=len(r.stdout),sha256=hashlib.sha256(r.stdout).hexdigest()))
 print(json.dumps(rows[-1]),flush=True);return r.stdout
for mode in ['normal','optimized']:
 ident=run(mode,'identities','identities.py',[P/'canonical.stdout'],cas=True)
 inv=run(mode,'inverse','inverse.py',[P/'canonical.stdout'])
 native=run(mode,'producer-export','producer_export.py',[P/'target-source'])
 exported=P/('producer-'+mode+'.json');exported.write_bytes(native)
 common=run(mode,'correspondence','correspond.py',[exported,P/'independent-normal'])
 for script,damage,cas,args in [('identities.py','private-support',True,[P/'canonical.stdout']),('inverse.py','wrong-triple',False,[P/'canonical.stdout']),('correspond.py','vertex',False,[exported,P/'independent-normal']),('correspond.py','repaired-entry',False,[exported,P/'independent-normal'])]:
  run(mode,'damage-'+damage,script,args+['--damage',damage],cas=cas,reject=True)
 stream=ident+inv+native+common;outputs.append(stream)
 if len(outputs)==2 and outputs[0]!=outputs[1]:raise ValueError('entire supplementary modes')
 (P/'supplement.json').write_text(json.dumps(dict(complete=len(outputs)==2,entire_modes_equal=len(outputs)==2,whole_stream_bytes=len(stream),whole_stream_sha256=hashlib.sha256(stream).hexdigest(),receipts=rows),indent=2)+'\n')

expected=json.loads((P/'EXPECTED.json').read_text())['supplement']
if len(stream)!=expected['bytes'] or hashlib.sha256(stream).hexdigest()!=expected['sha256']:raise ValueError('whole supplementary expected stream')
