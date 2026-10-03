"""Five serial source-only phases; whole original controls are in sector_control."""
from pathlib import Path
from hashlib import sha256
import argparse,json,os,subprocess,sys,time

def require(condition,message):
    if not condition:raise ValueError(message)
def canonical(data):return json.dumps(data,sort_keys=True,separators=(',',':')).encode()

def compact(records,rows,stream):
    uniform=records['uniform']
    return dict(agent='six-downset-1',role='researcher',
        scope='Complete q4 balanced h>=2 sign/identity verification and full original h2/h3 controls. Ordinary geometric/completeness/rank proof in PROOF.md is unformalized; independent review pending.',
        phases=5,complete_mathematical_bytes=len(stream),whole_mathematical_stream_sha256=sha256(stream).hexdigest(),phase_records=rows,
        uniform=dict(domain=uniform['domain'],fixed_sector_dimensions=uniform['fixed_sector_dimensions'],signs=[{k:r[k] for k in ('group','order','positive','degree','original_terms','shifted_terms')} for r in uniform['rows']],guards=uniform['guards']),
        separate_arithmetic=records['independent']['result'],
        original_complete_sector_controls=[records['sectors-h'+str(h)] for h in (2,3)],
        damages=records['damages']['cases'])

def run():
    ap=argparse.ArgumentParser();ap.add_argument('--check');ap.add_argument('--output');args=ap.parse_args()
    root=Path(__file__).resolve().parent;work=root/'work';work.mkdir(exist_ok=True)
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
    mode=sys.flags.optimize;require(mode in (0,1),'Use normal or optimization level one')
    env=dict(os.environ)
    for n in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):env[n]='1'
    phases=[('uniform','uniform.py',[],'uniform-O{mode}.json'),
            ('independent','check_uniform.py',['work/uniform-O{mode}.json'],'checked-O{mode}.json'),
            ('sectors-h2','sector_control.py',['--h','2'],'sectors-h2-O{mode}.json'),
            ('sectors-h3','sector_control.py',['--h','3'],'sectors-h3-O{mode}.json'),
            ('damages','damages.py',['work/uniform-O{mode}.json'],'damages-O{mode}.json')]
    records={};rows=[];runtime=[];stream=bytearray();start=time.monotonic()
    for phase,script,arguments,file in phases:
        require(not any((state/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational barrier before each child')
        command=[sys.executable,'-I','-B']+(['-O'] if mode else [])+[script]+[a.format(mode=mode) for a in arguments]
        then=time.monotonic()
        child=subprocess.run(command,cwd=root,env=env,capture_output=True,timeout=60)
        (work/(phase+f'-O{mode}.stdout')).write_bytes(child.stdout)
        (work/(phase+f'-O{mode}.stderr')).write_bytes(child.stderr)
        require(child.returncode==0,'Full phase '+phase+' failed: '+child.stderr.decode()[-1600:])
        data=json.loads((work/file.format(mode=mode)).read_text())
        require(data['optimized']==mode,'Actual child optimization flag')
        mathematical={k:v for k,v in data.items() if k not in ('seconds','peak_KiB','optimized')}
        if phase=='uniform':require(len(mathematical['rows'])==18 and all(r['positive'] for r in mathematical['rows']),'All eighteen original signs')
        if 'certificate_sha256' in mathematical:
            raw=(work/f'uniform-O{mode}.json').read_bytes()
            require(sha256(raw).hexdigest()==mathematical['certificate_sha256'],'Entire raw certificate input binding')
            mathematical['certificate_sha256']=sha256(canonical(records['uniform'])).hexdigest()
        records[phase]=mathematical
        encoded=canonical(dict(phase=phase,record=mathematical));stream+=encoded+b'\n'
        rows.append(dict(phase=phase,mathematical_bytes=len(encoded),mathematical_sha256=sha256(encoded).hexdigest()))
        runtime.append(dict(phase=phase,seconds=time.monotonic()-then,peak_KiB=data['peak_KiB']))
        print(json.dumps(dict(phase=phase,complete=True,optimized=mode)),flush=True)
    result=compact(records,rows,bytes(stream))
    if args.check:require(result==json.loads(Path(args.check).read_text()),'Entire compact record and full five-phase mathematical stream')
    output=Path(args.output) if args.output else work/f'replay-O{mode}.json'
    output.write_bytes(canonical(result)+b'\n');(work/f'whole-mathematical-O{mode}.jsonl').write_bytes(stream)
    measured=dict(agent='six-downset-1',role='researcher',optimized=mode,complete=True,source_only=True,serial_children=True,native_threads=1,phases=runtime,seconds=time.monotonic()-start,whole_mathematical_stream_sha256=result['whole_mathematical_stream_sha256'],compact_result_sha256=sha256(canonical(result)+b'\n').hexdigest())
    (work/f'execution-O{mode}.json').write_text(json.dumps(measured,indent=2)+'\n')
    print(json.dumps({k:v for k,v in measured.items() if k!='phases'}))
if __name__=='__main__':run()
