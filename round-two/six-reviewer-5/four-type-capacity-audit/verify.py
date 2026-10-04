"""Sealed independent review replay; every mathematical test survives -O."""
import hashlib,json,os,pathlib,subprocess,sys,tempfile,time,resource
P=pathlib.Path(__file__).resolve().parent
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
def check(ok,msg):
    if not ok:raise ValueError(msg)
def bind():
    seal=json.loads((P/'SOURCE.json').read_text());check(set(seal)=={'flow.py','literal.py','audit.py','COEFFICIENTS.json','RECORD.json'},'entire input source census')
    for n,h in seal.items():check(hashlib.sha256((P/n).read_bytes()).hexdigest()==h,'before-import whole source digest '+n)
    return seal
def child():
    bind();sys.path.insert(0,str(P));import flow,literal,audit
    a,large=literal.comparison(json.loads((P/'COEFFICIENTS.json').read_text()));b=audit.run();record=dict(literal=a,extension=b)
    check(record==json.loads((P/'RECORD.json').read_text()),'ENTIRE fresh mathematics equals compact fixture')
    raw=flow.canon(record);return dict(status='PASS',complete=True,record_bytes=len(raw),record_sha256=hashlib.sha256(raw).hexdigest(),original_comparison_positions=a['whole_original_comparison_positions'],individual_edges=a['whole_nn_edges'],envelope_pieces=len(a['full_piecewise_envelope']),generic_elimination_cases=b['generic_elimination_cases'],scope=a['scope'])
if __name__=='__main__':
    if '--child' in sys.argv:print(json.dumps(child(),sort_keys=True));raise SystemExit(0)
    bind();env=os.environ.copy();env.update({n:'1' for n in THREADS});st=time.monotonic();cmd=[sys.executable,'-I','-B']+(['-O'] if '--optimized' in sys.argv else [])+[str(__file__),'--child'];r=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=45)
    check(r.returncode==0,'actual completed math child: '+r.stderr);out=json.loads(r.stdout);out.update(seconds=time.monotonic()-st,peak_RSS_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,native_threads=1,serial_jobs=1,fixed_child_seconds=45)
    if '--out' in sys.argv:pathlib.Path(sys.argv[sys.argv.index('--out')+1]).write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,sort_keys=True))
