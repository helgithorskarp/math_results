"""Completed positive source-only replays and concrete exited adverse controls."""
import hashlib,json,os,pathlib,subprocess,sys,tempfile,time,shutil,copy,resource
P=pathlib.Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
def check(ok,msg):
    if not ok:raise ValueError(msg)
def semantic():
    sys.path.insert(0,str(P));import flow,literal
    Q=flow.Q;case=json.loads((P/'RECORD.json').read_text())['extension']['unequal_inputs'][1];m=case['m'];d=list(map(Q,case['d']));c=list(map(Q,case['c']));t=Q(case['tau']);v=flow.parameters(m,d,c,t);tests=[]
    def reject(name,f):
        try:f()
        except ValueError as e:tests.append(dict(name=name,actual_exited_rejection=True,reason=str(e)))
        else:raise ValueError('accepted defect '+name)
    reject('negative_floor',lambda:flow.parameters(m,d,c,-t))
    reject('m2_zero_BC_degree',lambda:flow.parameters(2,d,c,t))
    dd=d[:];dd[0]=float(dd[0]);reject('floating_demand',lambda:flow.parameters(m,dd,c,t))
    reject('noncanonical_rational',lambda:flow.number('2/4'))
    reject('below_closed_eta',lambda:flow.check_literal(m,d,c,t,v['lo']-Q(1,100)))
    reject('above_closed_eta',lambda:flow.check_literal(m,d,c,t,v['hi']+Q(1,100)))
    for j in (1,2,3,4):
        cc=c[:];cc[j]=t-Q(1,100);reject('negative_actual_cap_'+str(j),lambda cc=cc:flow.check_literal(m,d,cc,t))
    cc=c[:];cc[1]=cc[4]=t;reject('nonnegative_caps_insufficient_B_degree',lambda:flow.check_literal(m,d,cc,t))
    case3=json.loads((P/'RECORD.json').read_text())['extension']['unequal_inputs'][0];d3=list(map(Q,case3['d']));c3=list(map(Q,case3['c']));reject('m3_wrong_forced_eta',lambda:flow.check_literal(3,d3,c3,t,Q(1,8)+Q(1,100)))
    data=json.loads((P/'COEFFICIENTS.json').read_text())
    for name,mut in [('wrong_defining_denominator',lambda x:x.update(denominator=32767)),('missing_defining_pair',lambda x:x['free_pair_values'].pop()),('duplicate_defining_pair',lambda x:x['free_pair_values'].__setitem__(1,copy.deepcopy(x['free_pair_values'][0]))),('noninteger31_division',lambda x:x['free_pair_values'][0].update(numerator=x['free_pair_values'][0]['numerator']+1))]:
        z=copy.deepcopy(data);mut(z);reject(name,lambda z=z:literal.comparison(z))
    # Valid-shaped exact data perturbation reaches the fresh original budget gate.
    z=copy.deepcopy(data);ix=next(i for i,x in enumerate(z['free_pair_values']) if x['types']==[[0,0,2],[0,0,2]]);z['free_pair_values'][ix]['numerator']+=31
    reject('exact_coefficient_changes_literal_YY_deficit',lambda:literal.comparison(z))
    return tests
if __name__=='__main__':
    if '--semantic-child' in sys.argv:print(json.dumps(semantic(),sort_keys=True));raise SystemExit(0)
    sys.path.insert(0,str(P));import verify;verify.bind();env=os.environ.copy();env.update({n:'1' for n in THREADS});mode=['-O'] if '--optimized' in sys.argv else [];st=time.monotonic();r=subprocess.run([sys.executable,'-I','-B']+mode+[str(__file__),'--semantic-child'],env=env,capture_output=True,text=True,timeout=45)
    check(r.returncode==0,'actual semantic child: '+r.stderr);negative=json.loads(r.stdout);positive=[];source=[]
    with tempfile.TemporaryDirectory(prefix='r5-capacity-cold-') as tmp:
        cold=pathlib.Path(tmp)/'packet';shutil.copytree(P,cold,ignore=shutil.ignore_patterns('__pycache__','VALIDATION.json','SHA256SUMS'))
        for where,label in [(P,'local'),(cold,'cold')]:
            rr=subprocess.run([sys.executable,'-I','-B']+mode+[str(where/'verify.py'),'--child'],env=env,capture_output=True,text=True,timeout=45);check(rr.returncode==0,'positive '+label+rr.stderr);positive.append(dict(where=label,**json.loads(rr.stdout)))
        for name in ('flow.py','RECORD.json'):
            f=cold/name;original=f.read_bytes();f.write_bytes(original+b' ');rr=subprocess.run([sys.executable,'-I','-B']+mode+[str(cold/'verify.py'),'--child'],env=env,capture_output=True,text=True,timeout=45);f.write_bytes(original)
            check(rr.returncode!=0 and 'before-import whole source digest' in rr.stderr,'preimport source reject '+name);source.append(dict(name=name,actual_exited_preimport_rejection=True))
    check(all(x['record_sha256']==positive[0]['record_sha256'] and x['record_bytes']==positive[0]['record_bytes'] for x in positive),'entire mathematical equality')
    out=dict(complete=True,mode='optimized' if mode else 'normal',positive=positive,semantic_rejections=negative,source_rejections=source,seconds=time.monotonic()-st,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,native_threads=1,serial_jobs=1,fixed_child_seconds=45)
    if '--out' in sys.argv:pathlib.Path(sys.argv[sys.argv.index('--out')+1]).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(dict(complete=True,mode=out['mode'],positive=len(positive),semantic_rejections=len(negative),source_rejections=len(source),record_sha256=positive[0]['record_sha256'],record_bytes=positive[0]['record_bytes'],seconds=out['seconds'],peak_RSS_KiB=out['peak_RSS_KiB']),sort_keys=True))
