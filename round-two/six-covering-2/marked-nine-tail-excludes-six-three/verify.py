"""Cold exact reproduction; one arithmetic child at a time, each capped at20s."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

def require(ok,message):
    if not ok:raise ValueError(message)

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=('normal','optimized'),required=True)
    p.add_argument('--out-dir',type=Path,required=True);args=p.parse_args()
    source=Path(__file__).resolve().parent;expected=json.loads((source/'expected.json').read_text())
    work=args.out_dir.resolve();require(not work.exists(),'Fresh output directory required');work.mkdir(parents=True)
    flags=['-I','-B']+(['-O'] if args.mode=='optimized' else [])
    threads=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
             'NUMEXPR_MAX_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS')
    env={'PATH':os.defpath,'PYTHONDONTWRITEBYTECODE':'1',**{name:'1' for name in threads}}
    plan=[('capacity','capacity.py',['capacity','--out',str(work/'capacity.json')]),
      ('small','gluing.py',['small','--out',str(work/'small.json'),'--raw-stream',str(work/'small.raw')]),
      ('symmetry','symmetry.py',['--out',str(work/'symmetry.json'),'--raw-stream',str(work/'symmetry.raw')]),
      ('phases','capacity.py',['phases','--out',str(work/'phases.json'),'--capacity',str(work/'capacity.json')]),
      ('gluing','gluing.py',['gluing','--out',str(work/'gluing.json'),'--raw-stream',str(work/'gluing.raw'),
                           '--phases',str(work/'phases.json')])]
    receipts=[];start=time.monotonic();controls={}
    for stage,file,argv in plan:
        commands=[(stage,file,argv),('audit-'+stage,'audit.py',[stage,'--work-dir',str(work),
                    '--out',str(work/('audit-'+stage+'.json'))])]
        for label,name,options in commands:
            cmd=[sys.executable,*flags,str(source/name),*options];t=time.monotonic()
            try:r=subprocess.run(cmd,cwd=work,env=env,capture_output=True,text=True,timeout=20)
            except subprocess.TimeoutExpired as error:
                raise RuntimeError('INCOMPLETE '+label+' after20s; no exclusion established by this run') from error
            require(r.returncode==0,label+' failed: '+r.stderr)
            result=json.loads(r.stdout)
            receipts.append({'stage':label,'seconds':time.monotonic()-t,'returncode':r.returncode,'result':result})
            (work/'completed-stages.json').write_text(json.dumps(receipts,sort_keys=True,indent=2)+'\n')
            if label.startswith('audit-'):controls[stage]=result['negative_controls']
        require((work/(stage+'.json')).read_bytes()==(work/('audit-'+stage+'.json')).read_bytes(),
                'Entire independent '+stage+' record differs')
        if stage in ('small','symmetry','gluing'):
            require((work/(stage+'.raw')).read_bytes()==(work/('audit-'+stage+'.raw')).read_bytes(),
                    'Every independent '+stage+' raw count byte must agree')
    manifests=[]
    for pin in expected['mathematical_records']:
        raw=(work/pin['name']).read_bytes()
        actual={'name':pin['name'],'bytes':len(raw),'sha256':sha256(raw).hexdigest()}
        require(actual==pin,'Complete record/stream pin differs: '+pin['name']);manifests.append(actual)
    cap=json.loads((work/'capacity.json').read_text());phases=json.loads((work/'phases.json').read_text())
    glue=json.loads((work/'gluing.json').read_text());small=json.loads((work/'small.json').read_text())
    sym=json.loads((work/'symmetry.json').read_text())
    for record in (cap,phases,glue,small,sym):
        require(json.dumps(record['domain'],sort_keys=True)==json.dumps(expected['domain'],sort_keys=True),
                'Complete literal domain differs')
    checks={'pair_phase_values':sum(len(row[1]) for row in cap['all_raw_pair_union_rows']),
      'inventory_rows':sum(len(row['all_caps']) for row in cap['all_six_parent2_types']),
      'phase_candidates':len(cap['phase_candidates']),'uniform_parent2_capacity':cap['uniform_parent2_capacity'],
      'canonical_phase_rows':phases['canonical_phase_rows'],'weighted_raw_phase_rows':phases['weighted_raw_phase_rows'],
      'canonical_shapes':phases['canonical_shapes'],'BASE_phase_entries':glue['all_BASE_phase_entries'],
      'BASE_deficit_range':[min(r['deficit'] for r in glue['all_canonical_shapes']),max(r['deficit'] for r in glue['all_canonical_shapes'])],
      'BASE_outside_upper_range':[min(r['sum_per_original_outside_maxima'] for r in glue['all_canonical_shapes']),max(r['sum_per_original_outside_maxima'] for r in glue['all_canonical_shapes'])],
      'repair_shadow_sizes':sorted({r['size'] for r in glue['all_canonical_shapes']}),
      'small_BASE_phase_entries':sum(len(f[1]) for r in small['all_odd_phases'] for f in r.get('all_BASE_phase_families',[])),
      'generator_count':sym['generator_count'],'all_original_families':len(sym['all_original_moduli']),
      'physical_generator_original_n_checks':sym['physical_n_m_checks'],
      'semantic_record_damages_rejected':sum(len(v['semantic_record_damages_rejected']) for v in controls.values()),
      'raw_stream_damages_rejected':sum(len(v['raw_stream_damages_rejected']) for v in controls.values())}
    require(checks==expected['complete_census'],'Complete domain census differs')
    require(glue['unexcluded_shapes']==0 and glue['minimum_deficit']>0,'Some BASE-compatible shape remains')
    result={'agent':'six-covering-2','role':'researcher','mode':args.mode,
      'status':'COMPLETE AUTHOR-CHECKED CONDITIONAL SIX/THREE EXCLUSION; independent review pending',
      'python':sys.version,'seconds':time.monotonic()-start,
      'child_guard_seconds':20,'all_threads':1,'one_intensive_child_at_a_time':True,
      'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
      'stages':receipts,'mathematical_records':manifests,'complete_census':checks,
      'all_full_mathematical_records_equal':True,'all_raw_streams_byte_equal':True,
      'source_only_arithmetic_inputs':True,'independent_person_reviewed':False,
      'ordinary_proof_formalized':False,'remaining_two_parent_counts':expected['remaining_two_parent_counts'],
      'new_tenth_tail_bound_claimed':False,'global_bound_changed':False}
    (work/'verification.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ('mode','seconds','peak_child_RSS_KiB',
       'all_full_mathematical_records_equal','source_only_arithmetic_inputs','complete_census','global_bound_changed')}))

if __name__=='__main__':main()
