"""Portable source-only six-phase verifier; full generated records stay in work/."""
from pathlib import Path
from hashlib import sha256
import argparse,json,os,subprocess,sys,time

def require(ok,msg):
    if not ok:raise ValueError(msg)
def canonical(data):return json.dumps(data,sort_keys=True,separators=(',',':')).encode()

def compact(records,rows,stream):
    uniform=records['uniform'];checker=records['independent']['result']
    return dict(agent='six-downset-1',role='researcher',scope='Exact source verification of n2 integer h>=2 boundary signs and literal controls; ordinary geometric/product proof in PROOF.md is unformalized and independently unreviewed',phases=6,complete_mathematical_bytes=len(stream),whole_mathematical_stream_sha256=sha256(stream).hexdigest(),phase_records=rows,uniform=dict(domain=uniform['domain'],fixed_quotient=9,signs=[{k:r[k] for k in ('group','order','positive','degree','original_terms','shifted_terms')} for r in uniform['rows']],guards=uniform['guards']),independent=checker,original_controls=[records['original-h'+str(h)] for h in (2,3,10)],damages=records['damages']['cases'])

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--check');ap.add_argument('--output');args=ap.parse_args()
    root=Path(__file__).resolve().parent;work=root/'work';work.mkdir(exist_ok=True)
    mode=sys.flags.optimize;require(mode in (0,1),'reproduce normal or O1')
    env=dict(os.environ)
    for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[n]='1'
    phases=[('uniform','uniform.py',[],'uniform-O{mode}.json'),('independent','check_uniform.py',['work/uniform-O{mode}.json'],'checked-O{mode}.json')]
    phases += [('original-h'+str(h),'control.py',['--h',str(h)],'control-h'+str(h)+'-O{mode}.json') for h in (2,3,10)]
    phases += [('damages','damages.py',['work/uniform-O{mode}.json'],'damages-O{mode}.json')]
    records={};rows=[];stream=bytearray();runtime=[];start=time.monotonic()
    for phase,script,arguments,file in phases:
        command=[sys.executable,'-I','-B']+(['-O'] if mode else [])+[script]+[a.format(mode=mode) for a in arguments]
        then=time.monotonic();child=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=60)
        (work/(phase+f'-O{mode}.stdout')).write_bytes(child.stdout);(work/(phase+f'-O{mode}.stderr')).write_bytes(child.stderr)
        require(child.returncode==0,'complete '+phase+' failed: '+child.stderr.decode()[-1600:])
        data=json.loads((work/file.format(mode=mode)).read_text());require(data['optimized']==mode,'actual optimization flags')
        math={k:v for k,v in data.items() if k not in ('seconds','peak_KiB','optimized')}
        if 'certificate_sha256' in math:
            raw=(work/f'uniform-O{mode}.json').read_bytes();require(sha256(raw).hexdigest()==math['certificate_sha256'],'entire certificate input byte binding')
            math['certificate_sha256']=sha256(canonical(records['uniform'])).hexdigest()
        records[phase]=math;encoded=canonical(dict(phase=phase,record=math));stream+=encoded+b'\n'
        rows.append(dict(phase=phase,mathematical_bytes=len(encoded),mathematical_sha256=sha256(encoded).hexdigest()))
        runtime.append(dict(phase=phase,seconds=time.monotonic()-then,peak_KiB=data['peak_KiB']))
        print(json.dumps(dict(phase=phase,complete=True,optimized=mode)),flush=True)
    result=compact(records,rows,bytes(stream))
    if args.check:
        expected=json.loads(Path(args.check).read_text());require(result==expected,'ENTIRE compact record and full six-phase mathematical stream')
    output=Path(args.output) if args.output else work/f'replay-O{mode}.json'
    output.write_bytes(canonical(result)+b'\n')
    # The complete regenerated stream is evidence, not a future run input.
    (work/f'whole-mathematical-O{mode}.jsonl').write_bytes(stream)
    measured=dict(agent='six-downset-1',role='researcher',optimized=mode,complete=True,source_only=True,phases=runtime,seconds=time.monotonic()-start,whole_mathematical_stream_sha256=result['whole_mathematical_stream_sha256'],compact_result_sha256=sha256(canonical(result)+b'\n').hexdigest())
    (work/f'execution-O{mode}.json').write_text(json.dumps(measured,indent=2)+'\n')
    print(json.dumps({k:v for k,v in measured.items() if k!='phases'}))
if __name__=='__main__':run()
