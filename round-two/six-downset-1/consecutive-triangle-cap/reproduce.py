"""Portable, source-sealed serial replay; metadata is checked after mathematics."""
from pathlib import Path
import argparse, hashlib, json, os, runpy, subprocess, sys, time

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
THREADS=('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
         'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
for name in THREADS:os.environ[name]='1'


def require(ok,message):
    if not ok:raise ValueError(message)


def canonical(data):
    return (json.dumps(data,sort_keys=True,separators=(',',':'),default=str)+'\n').encode()


def sha(data):return hashlib.sha256(data).hexdigest()


def verify_source():
    manifest=ROOT/'SHA256SUMS'
    files={}
    for line in manifest.read_text().splitlines():
        digest,name=line.split(maxsplit=1)
        require(Path(name).name==name and name not in files,'single unique source filename')
        data=(ROOT/name).read_bytes()
        require(sha(data)==digest,'whole source checksum: '+name)
        files[name]=digest
    census={p.name for p in ROOT.iterdir() if p.is_file()}
    require(census==set(files)|{'SHA256SUMS'},'entire regular source file census')
    require(all(p.name in ('work','__pycache__') for p in ROOT.iterdir() if p.is_dir()),
            'no unexpected source/import directory')
    return files


STAGES={'gaussian':'gaussian_harmonic.py','pack':'pack_certificate.py',
        'check':'check_harmonic.py','repair':'repair_harmonic.py',
        'sector':'sector_control_harmonic.py','boundaries':'boundary_controls.py',
        'damages':'damages_harmonic.py'}


def math_record(work):
    checked=json.loads((work/'CHECKED.json').read_text())['result']
    first=json.loads((work/'HARMONIC-FIRST-REPAIR-RESULT.json').read_text())
    physical=json.loads((work/'HARMONIC-FIRST-SECTOR-CONTROL.json').read_text())
    first_summary=dict(n=4,h=3,N=first['N'],s=first['s'],
        lower_rank=first['final']['lower_rank'],cap_rank=first['final']['upper_rank'],
        original_M_sha256=first['final']['matrix_sha256'],seed_sha256=first['seed']['matrix_sha256'],
        common_norm=first['seed']['common_norm'],tau=first['seed']['tau'],kappa=first['kappa'],
        delta=first['delta'],scaled_cap_floor=first['scaled_cap_floor'],
        physical_dimension=physical['complete_dimension'],physical_metric_sha256=physical['metric_sha256'],
        physical_frame_sha256=physical['frame_sha256'],all_original_entries=first['all_original_entries'],
        all_physical_positions=physical['all_metric_and_frame_positions'],
        whole_dual_scores=True,all_inverse_equations=True)
    names=['HARMONIC-FIRST-REPAIR.json','HARMONIC-FIRST-SECTOR-CONTROL.json',
           'BOUNDARY-n3-h3-REPAIR.json','BOUNDARY-n3-h3-SECTOR.json',
           'BOUNDARY-n3-h4-REPAIR.json','BOUNDARY-n3-h4-SECTOR.json','DAMAGES.json']
    hashes={}
    for name in names:
        data=json.loads((work/name).read_text());data.pop('status',None)
        hashes[name]=sha(canonical(data))
    controls=[first_summary]+json.loads((work/'BOUNDARY-CONTROLS.json').read_text())
    whole=dict(agent='six-downset-1',role='researcher',complete=True,
        certificate_sha256=sha((ROOT/'CERTIFICATE.json').read_bytes()),
        coefficient_result=checked,original_controls=controls,whole_artifact_sha256=hashes,
        semantic_damages=json.loads((work/'DAMAGES.json').read_text()))
    summary=dict(agent='six-downset-1',role='researcher',complete=True,
        certificate_sha256=whole['certificate_sha256'],whole_mathematical_replay_sha256=sha(canonical(whole)),
        coefficient={k:v for k,v in checked.items() if k not in ('original_checks','Gaussian_checks','trust')},
        original_controls=controls,whole_artifact_sha256=hashes,
        semantic_damages=[r['case'] for r in whole['semantic_damages']['semantic_rejections']])
    return whole,summary


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--stage',choices=STAGES)
    p.add_argument('--regenerate',action='store_true',help='also independently check producer output against the whole compact certificate')
    p.add_argument('--check-expected',action='store_true',help='compare compact metadata only after every mathematical check')
    p.add_argument('--verify-source-only',action='store_true')
    args=p.parse_args();source=verify_source()
    if args.verify_source_only:
        print(json.dumps(dict(source_files=len(source)+1,whole_source_verified=True,optimized=sys.flags.optimize)))
        return
    if args.stage:
        program=STAGES[args.stage]
        sys.argv=[str(ROOT/program)]
        if args.stage=='check':sys.argv += [str(ROOT/'CERTIFICATE.json'),'--output',str(Path.cwd()/'CHECKED.json')]
        runpy.run_path(str(ROOT/program),run_name='__main__')
        verify_source()
        return
    work=ROOT/'work';work.mkdir(exist_ok=True)
    steps=(['gaussian','pack'] if args.regenerate else [])+['check','repair','sector','boundaries','damages']
    runs=[]
    for stage in steps:
        command=[sys.executable,'-I','-B']+(['-O'] if sys.flags.optimize else [])+[str(Path(__file__).resolve()),'--stage',stage]
        started=time.monotonic()
        with (work/(stage+'.stdout')).open('w') as out,(work/(stage+'.stderr')).open('w') as err:
            child=subprocess.Popen(command,cwd=work,env=os.environ.copy(),stdout=out,stderr=err)
            timed_out=False
            try:code=child.wait(timeout=60)
            except subprocess.TimeoutExpired:
                timed_out=True;child.kill();code=child.wait()
        record=dict(stage=stage,seconds=time.monotonic()-started,exit_code=code,
                    timed_out=timed_out,actual_child_exit_waited=True)
        runs.append(record)
        (work/'RUNS.json').write_text(json.dumps(runs,indent=2)+'\n')
        if code or timed_out:
            print((work/(stage+'.stderr')).read_text()[-3000:],file=sys.stderr)
            raise RuntimeError('incomplete stage; interruption is not a mathematical rejection: '+stage)
        if stage=='pack':
            require((work/'CERTIFICATE.json').read_bytes()==(ROOT/'CERTIFICATE.json').read_bytes(),
                    'whole regenerated compact certificate, all fields and coefficients')
        print(json.dumps(record),flush=True)
    whole,summary=math_record(work)
    (work/'REPLAY.json').write_bytes(canonical(whole))
    (work/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    if args.check_expected:
        require(summary==json.loads((ROOT/'expected.json').read_text()),
                'entire saved compact record AFTER complete mathematical reconstruction')
    require(verify_source()==source,'whole source unchanged during every stage')
    print(json.dumps(dict(complete=True,whole_mathematical_replay_sha256=summary['whole_mathematical_replay_sha256'],
                         certificate_sha256=summary['certificate_sha256'],stages=len(steps),
                         semantic_damages=len(summary['semantic_damages']),optimized=sys.flags.optimize)),flush=True)


if __name__=='__main__':main()
