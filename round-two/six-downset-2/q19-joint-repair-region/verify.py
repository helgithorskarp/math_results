"""Entire new source-only region proof, normal/O, seven serial children per mode."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from binding import source_files, require


def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()+b'\n'


def validate_whole(records):
    a=records['first-entries'];b=records['first-physical']
    require(a['data']['entries']['all_entry_inequalities_paid'] and
            a['all_twelve_shifted_forms_positive'] and b['all_twelve_shifted_forms_positive'],
            'entire first real entry/physical test')
    for name in ('original_L_rational_sha256','original_T_rational_sha256'):
        require(a['data']['entries'][name]==b['data'][name],'whole literal/named-set original '+name)
    r=records['polyhedron-vertices'];g=records['geometric-census'];f=records['affine-generators']
    require(r['vertex_count']==16 and len(r['vertices'])==16 and r['all_vertices_entry_feasible'] and
            r['all_vertices_twelve_shifted_forms_positive'], 'complete sixteen-vertex original region')
    require(g['entire_active_subset_vertex_sets_equal'] and g['geometric_vertex_count']==16 and
            {tuple(x['coords']) for x in r['vertices']}=={tuple(x) for x in g['vertices']},
            'entire two vertex sets and full coordinate records')
    require(f['all_original_entry_lift_metric_and_action_identities_verified'] and
            len(f['affine_generators'])==5 and all(x['all_allowed_entry_checks']==72817 and
            x['actions']['entire_original_action_positions']==181202 for x in f['affine_generators']),
            'all five spanning original entry/lift/metric/action generators')
    require(records['defects']['rejection_count']==22 and len(records['defects']['semantic_rejections'])==22,
            'twenty-two actual mathematical damages')


def run(output):
    root=Path(__file__).resolve().parent
    frozen=source_files(root)
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env.pop('PYTHONPATH',None)
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[name]='1'
    programs=[('first-entries','joint.py',['entries']),('first-physical','joint.py',['physical']),
              ('entry-polyhedron','entries.py',[]),('polyhedron-vertices','polyhedron.py',[]),
              ('affine-generators','affine_check.py',[]),('geometric-census','geometry.py',[]),
              ('defects','defects.py',[])]
    complete=None;observations=[];modes=[];source_controls=[]
    with tempfile.TemporaryDirectory(prefix='q19-joint-source-only-',dir=output) as tmp:
        cold=Path(tmp)/'source';cold.mkdir()
        for name,raw,sha in frozen:
            (cold/name).write_bytes(raw)
            require(hashlib.sha256((cold/name).read_bytes()).hexdigest()==sha,'every full isolated cold source byte')
        (cold/'SHA256SUMS').write_bytes((root/'SHA256SUMS').read_bytes())
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal';records={}
            for tag,script,args in programs:
                command=[sys.executable,'-B','-s']+(['-O'] if optimized else [])+[str(cold/script)]+args
                start=time.monotonic()
                target=output/(mode+'-'+tag+'.json')
                with target.open('wb') as stdout,target.with_suffix('.stderr').open('wb') as stderr:
                    p=subprocess.run(command,cwd=cold,env=env,stdout=stdout,stderr=stderr,timeout=45)
                error=target.with_suffix('.stderr').read_text()
                require(p.returncode==0,'complete new mathematical child '+tag+': '+error)
                record=json.loads(target.read_bytes())
                runtime={name:record.pop(name) for name in ('observed_seconds','peak_RSS_KiB') if name in record}
                records[tag]=record
                raw=canonical(record)
                obs=dict(mode=mode,tag=tag,seconds=time.monotonic()-start,runtime=runtime,
                         whole_mathematical_bytes=len(raw),whole_mathematical_sha256=hashlib.sha256(raw).hexdigest(),
                         returncode=p.returncode,stderr=error,fixed_child_guard_seconds=45,native_threads_one=True)
                observations.append(obs);print(json.dumps(obs),flush=True)
            validate_whole(records)
            raw=canonical(records)
            if complete is None:complete=records
            else:require(raw==canonical(complete),'ENTIRE canonical mathematics normal/optimized equality')
            expected=json.loads((cold/'EXPECTED.json').read_text())
            require(expected['whole_mathematical_bytes']==len(raw) and
                    expected['whole_mathematical_sha256']==hashlib.sha256(raw).hexdigest(),
                    'ENTIRE declared new mathematical evidence matches expected')
            modes.append(dict(mode=mode,whole_mathematical_bytes=len(raw),whole_mathematical_sha256=hashlib.sha256(raw).hexdigest()))
        # Distinct source-before-input rejects, kept separate from the44
        # mathematical damages. No damaged source is imported by a math child.
        for optimized in (False,True):
            mode='optimized' if optimized else 'normal'
            for name in ('model.py','COEFFICIENTS.json'):
                target=cold/name;original=target.read_bytes()
                target.write_bytes(original+b'\n#source-binding-control\n')
                try:
                    command=[sys.executable,'-B','-s']+(['-O'] if optimized else [])+[str(cold/'joint.py'),'entries']
                    p=subprocess.run(command,cwd=cold,env=env,capture_output=True,text=True,timeout=45)
                    require(p.returncode!=0 and p.stdout=='' and
                            'ValueError: ENTIRE source seal before mathematical import: '+name in p.stderr,
                            'actual source-before-math rejection: '+name)
                    source_controls.append(dict(mode=mode,file=name,returncode=p.returncode,
                                                mathematical_import_not_reached=True,
                                                reason='ENTIRE source seal before mathematical import: '+name))
                finally:target.write_bytes(original)
    raw=canonical(complete);(output/'MATHEMATICS.json').write_bytes(raw)
    receipt=dict(agent='six-downset-2',role='researcher',all_completed=True,
                 source_only_cold=True,frozen_source_files=len(frozen),
                 frozen_source_bytes=sum(len(raw) for name,raw,sha in frozen),
                 frozen_manifest_sha256=hashlib.sha256((root/'SHA256SUMS').read_bytes()).hexdigest(),
                 entire_source_bytes_checked_before_mathematical_import=True,
                 normal_optimized_entire_mathematics_equal=True,
                 only_two_explicit_top_level_runtime_observation_fields_removed=True,
                 mathematical_record_bytes=len(raw),mathematical_record_sha256=hashlib.sha256(raw).hexdigest(),
                 modes=modes,observations=observations,total_mathematical_children=14,
                 actual_semantic_rejections=44,independent_review=False,ordinary_bridges_unformalized=True,
                 distinct_source_binding_children=4,source_binding_rejections=source_controls,
                 fixed_child_guard_seconds=45,native_threads_one=True,serial_mathematical_children=1,
                 max_observed_child_seconds=max(o['seconds'] for o in observations),
                 peak_observed_child_RSS_KiB=max(o['runtime'].get('peak_RSS_KiB',0) for o in observations),
                 verification_does_not_publish_or_submit=True,
                 resource_status_never_mathematical_nonexistence=True)
    (output/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='observations'}),flush=True)
    return receipt


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    run(parser.parse_args().out)
