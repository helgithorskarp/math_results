"""Complete compact-source replay in fresh serial normal/optimized children.

Actual author six-downset-1 / researcher. Runner adapted from source4dd;
fresh four-mark original coverage. Ordinary generic proof is in PROOF.md.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

SOURCES = (
    'exact.py','linear.py','probe.py','trivariate.py','pack_certificate.py',
    'four_mark.py','four_second.py','four_sector.py','four_second_sector.py',
    'four_spread.py','four_second_spread.py','four_five_allq.py',
    'check_four_five.py','bind_four_forms.py','damage_four_five.py','damage_four_original.py',
)
CERT = 'FOUR-EVEN-FIVE-ALLQ-CERTIFICATE.json'
SEALED = set(SOURCES) | {CERT,'PROOF.md','README.md','EXPECTED.json',
                         'CREDITS.json','DEPENDENCIES.json','.gitignore','verify.py'}
STAGES = (
    'four_mark.py','four_second.py','four_sector.py','four_second_sector.py',
    'four_spread.py','four_second_spread.py','four_five_allq.py',
    'check_four_five.py','bind_four_forms.py','damage_four_five.py','damage_four_original.py',
)
GENERATED = {
    'FOUR-MARK-FIRST-MATRIX.json','FOUR-MARK-FIRST-RESULT.json',
    'FOUR-MARK-SECOND-MATRIX.json','FOUR-MARK-SECOND-RESULT.json',
    'FOUR-MARK-FIRST-SECTOR.json','FOUR-MARK-FIRST-SECTOR-RESULT.json',
    'FOUR-MARK-SECOND-SECTOR.json','FOUR-MARK-SECOND-SECTOR-RESULT.json',
    'FOUR-MARK-FIRST-SPREAD-RESULT.json','FOUR-MARK-SECOND-SPREAD-RESULT.json',
    CERT,'FOUR-EVEN-FIVE-ALLQ-RESULT.json','FOUR-EVEN-FIVE-ALLQ-CHECKED.json',
    'FOUR-ORIGINAL-FORM-BINDINGS.json','FOUR-FIVE-DAMAGES.json','FOUR-ORIGINAL-DAMAGES.json',
}
TIMED = {'FOUR-EVEN-FIVE-ALLQ-RESULT.json','FOUR-EVEN-FIVE-ALLQ-CHECKED.json'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def read(folder,name):
    return json.loads((folder/name).read_text())

def mathematical(name,obj):
    if name in TIMED:
        return {k:v for k,v in obj.items() if k not in ('seconds','peak_KiB','optimized')}
    return obj

def operational_barrier():
    # Optional campaign context; standalone reproduction needs no campaign files.
    task_root = os.environ.get('DISCOVERY_RESEARCH_TEAM_ROOT')
    if task_root:
        require(not any((Path(task_root)/n).exists() for n in
                        ('PAUSED','PAUSED.json','HANDOVER','HANDOVER.json')),
                'campaign operational barrier; preserve progress')

def integrity(source):
    allowed = SEALED | {'SHA256SUMS'} | GENERATED | {'__pycache__','replay-output'}
    require(all(p.name in allowed for p in source.iterdir()),
            'all and only declared source/runtime entries')
    lines = (source/'SHA256SUMS').read_text().splitlines()
    require(len(lines) == len(SEALED), 'whole sealed source census')
    hashes = {}
    for line in lines:
        expected,name = line.split(maxsplit=1)
        require(name in SEALED and name not in hashes and Path(name).name == name,
                'unique plain sealed filename')
        require(len(expected) == 64 and set(expected) <= set('0123456789abcdef'),
                'canonical whole SHA256')
        p = source/name
        require(p.is_file() and not p.is_symlink() and digest(p) == expected,
                'regular whole source integrity '+name)
        hashes[name] = expected
    require(set(hashes) == SEALED, 'complete source seal')
    credits = read(source,'CREDITS.json')['utilities']
    require(len(credits) == 5 and len({r['file'] for r in credits}) == 5,
            'all five unique verbatim credits')
    for row in credits:
        name = row['file']
        require(name in SOURCES and row['copied_verbatim'] is True
                and (source/name).stat().st_size == row['bytes']
                and hashes[name] == row['sha256'], 'whole credited original utility '+name)
    return hashes

def checked_mode(folder,expected):
    producer = read(folder,'FOUR-EVEN-FIVE-ALLQ-RESULT.json')
    require(producer['status'].startswith('ALL5 PIVOTS COEFFICIENT POSITIVE')
            and producer['traceback'] is None and producer['pivots'] == 5
            and producer['local_updates'] == 30 and producer['complete_form_fields'] == 25,
            'complete producer fields; incomplete exit zero is not success')
    require(digest(folder/CERT) == expected['certificate_sha256'],
            'entire freshly generated coefficient certificate')
    whole = {name:mathematical(name,read(folder,name)) for name in sorted(GENERATED)}
    for name,value in expected['records'].items():
        require(whole[name] == value, 'whole mathematical record '+name)
    for name,row in expected['whole_generated_files'].items():
        p = folder/name
        require(p.is_file() and p.stat().st_size == row['bytes'] and digest(p) == row['sha256'],
                'whole generated original data '+name)
    require(set(expected['whole_generated_files']) == GENERATED-TIMED,
            'whole raw generated census')
    require(expected['excluded_execution_observations'] ==
            {name:['seconds','peak_KiB','optimized'] for name in TIMED},
            'only explicit two-record execution observations excluded')
    for name in ('FOUR-FIVE-DAMAGES.json','FOUR-ORIGINAL-DAMAGES.json'):
        d = whole[name]
        require(d['all_rejected'] is True and len(d['cases']) == 6
                and all(r['rejected'] is True for r in d['cases']),
                'all six actual semantic rejections '+name)
    checked = whole['FOUR-EVEN-FIVE-ALLQ-CHECKED.json']
    require(checked['complete'] is True and checked['original_form_fields'] == 25
            and checked['pivots'] == 5 and checked['local_updates'] == 30
            and checked['field_count'] == 55 and checked['polynomial_count'] == 59
            and checked['positive_pivot_coefficients'] == 265,
            'complete separate whole coefficient reader')
    binding = whole['FOUR-ORIGINAL-FORM-BINDINGS.json']
    require(binding['complete'] is True and binding['actual_original_form_positions'] == 50
            and len(binding['controls']) == 2,
            'all original even-five positions on both complete controls')
    for label,N,parent in (('FIRST',70,52),('SECOND',76,64)):
        seed = whole[f'FOUR-MARK-{label}-RESULT.json']
        sector = whole[f'FOUR-MARK-{label}-SECTOR-RESULT.json']
        repair = whole[f'FOUR-MARK-{label}-SPREAD-RESULT.json']
        require(seed['N'] == sector['N'] == repair['N'] == N
                and seed['full_core'] == dict(psd=True,rank=N-3)
                and seed['original_lower'] == dict(psd=True,rank=N-2)
                and seed['original_cap'] == dict(psd=True,rank=N-1)
                and seed['original_cap_floor_one'] == dict(psd=True,rank=N-1)
                and seed['whole_physical_cap_floor_one'] == dict(psd=True,rank=N-3),
                'whole original core/empty/cap/greatest ranks '+label)
        require(seed['baseline_two_mark']['N'] == parent
                and seed['baseline_transports_new_cap'] is False
                and seed['all_actual_empty_equations_checked'] is True
                and seed['all_original_rows_spanned'] is True
                and seed['checked_original_positions'] == N*N,
                'complete original equations and baseline scope '+label)
        require(sector['all_cross_sector_positions_checked'] is True
                and sector['all_three_light_means_retained'] is True
                and sector['aggregate_dimension'] == 20
                and sector['light_standard_copies'] == 2
                and sector['light_profile_squared_norms'] == [2,6]
                and sector['all_light_split_cross_positions_checked'] is True
                and sector['aggregate_first_trace_mean_cross_checked'] is True
                and sector['all_metric_and_frame_positions'] == 2*(N-3)**2,
                'whole physical directions/multiplicities/crosses '+label)
        require(repair['all_original_inverse_positions'] == N-1
                and repair['complete_actual_empty_lift_positions'] == 3*N*N
                and len(repair['repaired']) == 2
                and all(r['lower_rank'] == r['upper_rank'] == N-1 for r in repair['repaired'])
                and repair['all_original_symmetry_positions'] ==
                    3*repair['symmetry_generators']*N*N,
                'whole original inverse/empty/repair/invariance '+label)
    canonical = json.dumps(whole,sort_keys=True,separators=(',',':'))+'\n'
    require(len(canonical.encode()) == expected['entire_generated_mathematics_bytes']
            and sha256(canonical.encode()).hexdigest() == expected['entire_generated_mathematics_sha256'],
            'whole 16-record mathematical agreement with paid final-source evidence')
    return canonical

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--work-dir',type=Path,default=Path('replay-output'))
    parser.add_argument('--integrity-only',action='store_true')
    args = parser.parse_args()
    operational_barrier()
    source = Path(__file__).resolve().parent
    hashes = integrity(source)
    if args.integrity_only:
        print(json.dumps(dict(complete=True,sealed_files=len(hashes),
            source_integrity_verified=True,optimized=not __debug__)))
        return
    require(sys.version_info[:3] == (3,12,14), 'recorded CPython3.12.14 runtime')
    require(not args.work_dir.exists(), 'fresh work directory required')
    work = args.work_dir.resolve()
    require(work != source, 'cold output distinct from source')
    work.mkdir(parents=True)
    expected = read(source,'EXPECTED.json')
    environment = os.environ.copy()
    for name in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
                 'BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        environment[name] = '1'
    environment.pop('PYTHONPATH',None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    children,results = [],[]
    start = time.monotonic()
    for optimized in (False,True):
        folder = work/('optimized' if optimized else 'normal')
        folder.mkdir()
        for name in SOURCES+(CERT,):
            shutil.copyfile(source/name,folder/name)
            require(digest(folder/name) == hashes[name], 'whole cold input '+name)
        for stage in STAGES:
            operational_barrier()
            require(integrity(source) == hashes, 'entire frozen public source unchanged')
            require(all(digest(folder/name) == hashes[name] for name in SOURCES),
                    'all cold mathematical source unchanged')
            command = [sys.executable,'-B']+(['-O'] if optimized else [])+[stage]
            child_start = time.monotonic()
            try:
                completed = subprocess.run(command,cwd=folder,env=environment,
                    capture_output=True,text=True,timeout=60)
            except subprocess.TimeoutExpired as failure:
                (work/'INCOMPLETE.json').write_text(json.dumps(dict(complete=False,
                    reason='60s child timeout; not mathematical absence',
                    program=stage,optimized=optimized),indent=2)+'\n')
                raise ValueError('incomplete guarded child '+stage) from failure
            elapsed = time.monotonic()-child_start
            (folder/(stage+'.stdout')).write_text(completed.stdout)
            (folder/(stage+'.stderr')).write_text(completed.stderr)
            require(completed.returncode == 0 and not completed.stderr,
                    'actual complete child exit '+stage)
            output = json.loads(completed.stdout.strip().splitlines()[-1])
            children.append(dict(program=stage,optimized=optimized,seconds=elapsed,
                exit_code=completed.returncode,actual_child_exit_waited=True,
                peak_KiB=output.get('peak_KiB',output.get('execution',{}).get('peak_KiB'))))
            (work/'PROGRESS.json').write_text(json.dumps(dict(complete=False,
                reason='serial replay in progress',children=children),indent=2)+'\n')
            print(json.dumps(dict(stage=stage,optimized=optimized,
                completed=True,seconds=elapsed)),flush=True)
        results.append(checked_mode(folder,expected))
    require(results[0] == results[1], 'entire normal/optimized mathematical records agree')
    for name in GENERATED-TIMED:
        require((work/'normal'/name).read_bytes() == (work/'optimized'/name).read_bytes(),
                'whole normal/optimized raw generated bytes '+name)
    require(integrity(source) == hashes, 'final whole frozen source seal')
    (work/'WHOLE-REPLAY.json').write_text(results[0])
    out = dict(agent='six-downset-1',role='researcher',complete=True,
        runtime=sys.version.split()[0],children=children,children_completed=len(children),
        native_threads=1,serial_intensive_children=1,child_seconds_limit=60,
        source_hashes=hashes,whole_normal_optimized_mathematics_agree=True,
        whole_normal_optimized_generated_bytes_agree=True,
        complete_mathematical_record_files=16,complete_raw_byte_record_files=14,
        semantic_defects_rejected_each_mode=12,total_semantic_defect_rejections=24,
        controls=[70,76],complete_original_form_positions=50,
        whole_replay_bytes=len(results[0].encode()),
        whole_replay_sha256=sha256(results[0].encode()).hexdigest(),
        certificate_sha256=expected['certificate_sha256'],
        generated_artifacts_are_not_published_inputs=True,
        ordinary_infinite_parameter_bridges_unformalized=True,independent_review=False,
        seconds=time.monotonic()-start,verified_utc=datetime.now(timezone.utc).isoformat())
    (work/'VALIDATION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('children','source_hashes')}),flush=True)

if __name__ == '__main__':
    main()
