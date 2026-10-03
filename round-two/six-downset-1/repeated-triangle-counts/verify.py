"""Regenerate every algebraic proof record and original fixture serially.

Standard library only. Each mathematical child has the original60s guard;
one child runs at a time. Large generated evidence remains under work/.
"""
import os
for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse, json, subprocess, sys, time

def require(ok, message):
    if not ok:
        raise ValueError(message)

def mathematical(record):
    if isinstance(record,dict):
        return {k:mathematical(v) for k,v in record.items() if k not in ('seconds','peak_KiB','optimized')}
    if isinstance(record,list):
        return [mathematical(v) for v in record]
    return record

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',type=Path)
    parser.add_argument('--resume',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    os.chdir(root)
    work=Path('work')
    require(args.resume or not work.exists(),'Use a fresh source-only copy, or --resume for its exact saved run')
    work.mkdir(exist_ok=True)
    code_hashes={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))}
    checkpoint=work/'DRIVER-CHECKPOINT.json'
    saved=json.loads(checkpoint.read_text()) if args.resume and checkpoint.exists() else {'code_hashes':code_hashes,'finished':{}}
    require(saved['code_hashes']==code_hashes,'resume is bound to the complete defining source')
    stream=sha256()
    mathematical_bytes=0
    phase_records=[]
    start=time.monotonic()
    prefix=[sys.executable]+(['-O'] if not __debug__ else [])
    mode='optimized' if not __debug__ else 'normal'

    def phase(label,program,arguments,path):
        nonlocal mathematical_bytes
        pause=os.environ.get('RESEARCH_PAUSE_DIR')
        require(not pause or not any((Path(pause)/p).exists() for p in ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),'operational pause/handover barrier')
        path=Path(path)
        if label in saved['finished']:
            require(args.resume and path.exists() and sha256(path.read_bytes()).hexdigest()==saved['finished'][label]['file_sha256'],'entire saved phase output binding')
        else:
            child_start=time.monotonic()
            result=subprocess.run(prefix+[program]+arguments,text=True,capture_output=True,timeout=60)
            require(result.returncode==0,'phase '+label+' failed: '+result.stdout[-1800:]+result.stderr[-1800:])
            require(path.is_file(),'complete phase output '+label)
            saved['finished'][label]={'file_sha256':sha256(path.read_bytes()).hexdigest(),'seconds':time.monotonic()-child_start}
        record=json.loads(path.read_text())
        blob=json.dumps(mathematical(record),sort_keys=True,separators=(',',':')).encode()
        stream.update(label.encode()+b'\n'+blob+b'\n')
        mathematical_bytes+=len(blob)
        phase_records.append({'phase':label,'mathematical_bytes':len(blob),'mathematical_sha256':sha256(blob).hexdigest()})
        saved.update(agent='six-downset-1',role='researcher',complete=False,last_phase=label,mode=mode,updated_at=datetime.now(timezone.utc).isoformat())
        checkpoint.write_text(json.dumps(saved,indent=2)+'\n')
        return record

    raw=phase('raw','raw_bounds.py',[],'work/raw-bounds.json')
    require(raw['maximum_h_grid_size']==131 and raw['maximum_q_columns']==82,'complete degree grid')
    point_checks=[]
    for h in range(3,134):
        phase('point:'+str(h),'point.py',['--h',str(h)],f'work/newton/h{h}.json')
        point_checks.append(phase('point-check:'+str(h),'point_check.py',['--h',str(h)],f'work/newton/h{h}-checked.json'))
        if h==3 or h%20==3 or h==133:
            print(json.dumps({'mode':mode,'complete_points':len(point_checks),'required_points':131,'last_h':h,'seconds':time.monotonic()-start}),flush=True)
    newton=phase('Newton','newton.py',[],'work/newton-coefficients.json')
    checked=phase('Newton-check','newton_check.py',[],f'work/newton-checked-{mode}.json')
    damage=phase('semantic-damages','damages.py',[],f'work/newton-damages-{mode}.json')
    require(checked['nonnegative_coefficients']==38880 and checked['complete_Newton_identity_points']==44324,'complete positivity/reconstruction coverage')
    require(checked['independent_raw_points']==131 and checked['full_determinant_identity_points']==78469 and checked['full_shift_identity_points']==78469,'complete Gaussian/shift coverage')
    require(len(damage['controls'])==8 and all(z['rejected'] is True for z in damage['controls']),'all semantic corruptions reject')
    phase('h2-signs','fixed.py',['--fixed','--h','2','--output','work/h2-signs.json'],'work/h2-signs.json')
    h2=phase('h2-check','fixed_check.py',['work/h2-signs.json','--output','work/h2-checked.json'],'work/h2-checked.json')
    require(h2['checks']['complete'] is True and len(h2['checks']['checks'])==24,'h2 entire scalar/cap certificate')
    sectors=phase('complete-sector-controls','sectors.py',[],'work/sectors-controls.json')
    fixtures=[]
    for h,n in ((3,3),(4,3),(10,3),(3,5)):
        fixture=phase(f'original:{h}:{n}','model.py',['--h',str(h),'--n',str(n)],f'work/original-h{h}-n{n}.json')['fixture']
        require(fixture['sharp']['lower_rank']==fixture['N']-1,'literal greatest rank')
        fixtures.append(fixture)
        print(json.dumps({'mode':mode,'complete_original_fixture':[h,n],'N':fixture['N'],'seconds':time.monotonic()-start}),flush=True)
    result=dict(agent='six-downset-1',role='researcher',complete=True,domain='every integer h>=2 and n>=3; distinct old x,y; all private points mutually distinct/outside cube',auxiliary_domain='integer h>=3 and real q>=4',whole_mathematical_stream_sha256=stream.hexdigest(),whole_mathematical_bytes=mathematical_bytes,phase_count=len(phase_records),phase_records=phase_records,Newton_nonnegative_coefficients=checked['nonnegative_coefficients'],Newton_identity_points=checked['complete_Newton_identity_points'],independent_raw_points=checked['independent_raw_points'],determinant_identity_points=checked['full_determinant_identity_points'],q_shift_identity_points=checked['full_shift_identity_points'],positive_original_row_factor_occurrences=checked['positive_original_row_factor_occurrences'],semantic_rejections=len(damage['controls']),h2_summary=h2['checks'],sector_controls=sectors['controls'],original_fixtures=fixtures,actual_original_positions_per_whole_phase=sum(z['original_positions'] for z in fixtures),physical_Gram_positions=sum(z['physical_Gram_positions'] for z in fixtures),physical_full_frame_positions=sum(z['physical_frame_positions'] for z in fixtures),ordinary_bridge_formalized=False,extension_external_person_review=False,source_only=True,serial_math_children=True,native_threads=1,child_guard_seconds=60,polynomial_term_guard=512)
    (work/'FULL-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    if args.check:
        expected=json.loads(args.check.read_text())
        require(result==expected,'ENTIRE source-only final mathematical record equals compact expected evidence')
    saved.update(complete=True,last_phase='COMPLETE',whole_mathematical_stream_sha256=stream.hexdigest(),seconds=time.monotonic()-start)
    checkpoint.write_text(json.dumps(saved,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('phase_records','h2_summary','sector_controls','original_fixtures')}),flush=True)

if __name__=='__main__':
    main()
