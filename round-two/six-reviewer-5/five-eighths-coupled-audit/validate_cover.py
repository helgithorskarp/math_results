"""Four cold replays and bounded semantic damage checks, serial threads one."""
import copy, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, time

P=pathlib.Path(__file__).resolve().parent
env=os.environ.copy()
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[k]='1'
rows=[]; reference=None; parsed=None
def run(args,cwd):
    start=time.monotonic()
    r=subprocess.run([sys.executable,'-I','-B',*args],cwd=cwd,env=env,capture_output=True,text=True,timeout=45)
    row=dict(command=args,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,elapsed_seconds=time.monotonic()-start)
    rows.append(row);return r

with tempfile.TemporaryDirectory(prefix='five-eighths-audit-',dir=P) as root:
    root=pathlib.Path(root)
    for number,mode in enumerate(([],['-O'],[],['-O'])):
        cold=root/('positive-'+str(number));cold.mkdir()
        for name in ('check_cover.py','COVER-input.json'):shutil.copyfile(P/name,cold/name)
        r=run(mode+['check_cover.py'],cold)
        if r.returncode:raise ValueError('positive replay '+str(number)+': '+r.stderr)
        raw=(cold/'computed-private.json').read_bytes();record=json.loads(raw)
        if reference is None:reference,parsed=raw,record
        if raw!=reference or record!=parsed:raise ValueError('whole cold record mismatch')
        rows[-1]['result']=json.loads(r.stdout)
        print('positive',number,'PASS',flush=True)
    d=json.loads((P/'COVER-input.json').read_text())
    cases=[]
    def data_case(label,mutate,message):
        x=copy.deepcopy(d);mutate(x);cases.append((label,x,'',message))
    data_case('closed upper endpoint changed',lambda x:x['root'].__setitem__(1,'3/5'),'entire closed root')
    data_case('numeric root bypass',lambda x:x['root'].__setitem__(0,0.6),'root types')
    data_case('boolean split axis',lambda x:x['splits'].__setitem__('',True),'axis types')
    data_case('out of range split axis',lambda x:x['splits'].__setitem__('',5),'axis types')
    data_case('unknown leaf status',lambda x:x['leaves'].__setitem__('00','sampled'),'status types')
    data_case('missing defining leaf',lambda x:x['leaves'].pop('00'),'input census')
    data_case('extra defining leaf',lambda x:x['leaves'].__setitem__('000','origin-passes'),'input census')
    data_case('split leaf overlap',lambda x:x['leaves'].__setitem__('',x['leaves'].pop('00')),'disjoint leaves')
    data_case('false empty parent',lambda x:x['leaves'].__setitem__('00','empty-necessary-inequalities'),'nonempty is not declared empty')
    def disconnected(x):x['splits']['1111111111111111111']=x['splits'].pop('0')
    data_case('disconnected subtree',disconnected,'both children reachable')
    cases += [
      ('sqrt floor raised',d,'old=m.isqrt\nm.isqrt=lambda x:old(x)+1','sqrt floor square enclosure'),
      ('beta denominator damaged',d,'old=m.beta\nm.beta=lambda i,j:2*old(i,j)','entire polar integral'),
      ('kernel square top coefficient dropped',d,'old=m.mul\ndef bad(a,b):\n c=old(a,b)\n if len(a)==6 and len(b)==6:c[-1]=m.ZERO\n return c\nm.mul=bad','entire polar integral'),
      ('highest integration coefficient dropped',d,'old=m.integral\nm.integral=lambda a,shift=0:old(a[:-1],shift)','low first-power integral'),
      ('centered multinomial vector damaged',d,'old=m.multinomial_quadratic\ndef bad(a,n):\n c=old(a,n)\n if n:c[-1]+=m.ONE\n return c\nm.multinomial_quadratic=bad','centered beta power'),
      ('seventh Maclaurin cardinality damaged',d,'old=m.comb\nm.comb=lambda n,k:old(n,k)+(1 if n==8 and k==7 else 0)','seven recurrence minima'),
    ]
    for number,(label,data,patch,message) in enumerate(cases):
        cold=root/('negative-'+str(number));cold.mkdir();shutil.copyfile(P/'check_cover.py',cold/'check_cover.py')
        (cold/'damaged.json').write_text(json.dumps(data))
        source="import importlib.util,json,pathlib\np=pathlib.Path(__file__).resolve().parent\ns=importlib.util.spec_from_file_location('auditor',p/'check_cover.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n"+patch+"\ntry:\n m.audit(json.loads((p/'damaged.json').read_text()))\nexcept ValueError as e:\n if "+repr(message)+" not in str(e):raise\n print(str(e))\nelse:raise RuntimeError('semantic damage accepted')\n"
        (cold/'control.py').write_text(source)
        r=run(['-O','control.py'],cold)
        if r.returncode:raise ValueError('control '+label+': '+r.stderr)
        rows[-1]['label']=label;rows[-1]['intended_rejection']=message
        print('negative',number,label,'PASS',flush=True)
    # Complete record is regenerated; only compact summaries are public evidence.
    (P/'computed-private.json').write_bytes(reference)
result=dict(status='PASS',python=sys.version,positive_children=4,semantic_rejections=len(cases),guard_seconds=45,native_threads=1,serial=True,
            record_bytes=len(reference),record_sha256=hashlib.sha256(reference).hexdigest(),source_sha256=hashlib.sha256((P/'check_cover.py').read_bytes()).hexdigest(),
            input_sha256=hashlib.sha256((P/'COVER-input.json').read_bytes()).hexdigest(),max_child_seconds=max(x['elapsed_seconds'] for x in rows),rows=rows)
(P/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},sort_keys=True))
