"""Cold serial normal/-O replays with full byte seals and semantic damages."""
import hashlib,json,os,pathlib,resource,subprocess,sys,time
P=pathlib.Path(__file__).resolve().parent
def require(ok,why):
    if not ok:raise ValueError(why)
def source_gate():
    expected={}
    for row in (P/'SHA256SUMS').read_text().splitlines():
        value,name=row.split('  ');require(name not in expected,'source manifest distinct');expected[name]=value
    actual={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in P.iterdir() if p.is_file() and p.name!='SHA256SUMS'}
    require(actual==expected,'whole source census and byte seals')
    return hashlib.sha256((P/'SHA256SUMS').read_bytes()).hexdigest()
def barriers():
    state=os.environ.get('DISCOVERY_REVIEW_STATE')
    if state:
        S=pathlib.Path(state);h=json.loads((S/'monitor/health.json').read_text())
        require(not h['reasons'] and h['credit_budget']['status']=='authorized' and not any('paused' in p.name.lower() or 'handover' in p.name.lower() for p in S.iterdir()),'operations barrier')
def main():
    manifest=source_gate();expected=json.loads((P/'EXPECTED.json').read_text());env=dict(os.environ)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[name]='1'
    env.pop('PYTHONPATH',None)
    rows=[];paired={}
    bad={'domain':'entire specified domain','derivative':'entire independently scattered Wronskian','denominator':'entire coefficient sign denominator','compact':'ENTIRE inverse compact homography identity','endpoint':'separate closed endpoint mandatory','curve':'ENTIRE curve remainder','radical':'ENTIRE inverse radical rational channel','norm36':'both required norm curves'}
    for optimized in (False,True):
        for filename,damage in [('generate.py',None),('check.py',None)]+[('check.py',x) for x in bad]:
            barriers();source_gate();cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(P/filename)]+([damage] if damage else [])
            start=time.monotonic();run=subprocess.run(cmd,cwd=P,env=env,capture_output=True,text=True,timeout=45)
            row=dict(phase=filename,damage=damage,optimized=optimized,seconds=time.monotonic()-start,returncode=run.returncode)
            if damage:require(run.returncode!=0 and bad[damage] in run.stderr,'intended semantic rejection '+damage);row['intended_rejection']=bad[damage]
            else:
                require(run.returncode==0,'positive phase failed '+run.stderr)
                name='certificate.json' if filename=='generate.py' else 'check-result.json';raw=(P/'work'/name).read_bytes();sha=hashlib.sha256(raw).hexdigest()
                require(sha==expected[name]['sha256'] and len(raw)==expected[name]['bytes'],'ENTIRE private/public record seal '+name)
                if not optimized:paired[name]=raw
                else:require(raw==paired[name],'ENTIRE normal/O mathematical record bytes')
                row.update(record=name,bytes=len(raw),sha256=sha)
            rows.append(row);print(json.dumps(row,sort_keys=True),flush=True)
    source_gate();out=dict(status='all 4 positive replays and 16 intended semantic rejections pass',children=rows,manifest_sha256=manifest,peak_child_rss_KiB=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,native_threads=1,serial=True,guard_seconds=45,scope='unchanged1CPU/2GiB; original matrix premises remain explicit')
    (P/'work/validation.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],flush=True)
if __name__=='__main__':main()
