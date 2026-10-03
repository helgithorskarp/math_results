"""Fresh serial reproduction. Arithmetic subprocess guard20s; threads1."""
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


def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))


def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=('normal','optimized'),required=True)
    p.add_argument('--out-dir',type=Path,required=True);args=p.parse_args()
    source=Path(__file__).resolve().parent;expected=json.loads((source/'expected.json').read_text())
    work=args.out_dir.resolve();require(not work.exists(),'Fresh output directory required');work.mkdir(parents=True)
    threads=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
    env={'PATH':os.defpath,'PYTHONDONTWRITEBYTECODE':'1',**{key:'1' for key in threads}}
    flags=['-I','-B']+(['-O'] if args.mode=='optimized' else [])
    cap=work/'capacity.json';glue=work/'gluing.json';acap=work/'audit-capacity.json';aglue=work/'audit-gluing.json';audit=work/'audit-finish.json'
    stages=[('capacity','capacity.py',['--out',str(cap),'--raw-stream',str(work/'capacity.bin')]),('gluing','gluing.py',['--out',str(glue),'--raw-stream',str(work/'gluing.bin')]),
      ('audit-capacity','audit.py',['--stage','capacity','--capacity',str(cap),'--out',str(acap),'--raw-stream',str(work/'audit-capacity.bin'),'--producer-raw-stream',str(work/'capacity.bin')]),
      ('audit-gluing','audit.py',['--stage','gluing','--capacity',str(cap),'--gluing',str(glue),'--out',str(aglue),'--raw-stream',str(work/'audit-gluing.bin'),'--producer-raw-stream',str(work/'gluing.bin')]),
      ('audit-finish','audit.py',['--stage','finish','--capacity',str(cap),'--gluing',str(glue),'--audit-capacity',str(acap),'--audit-gluing',str(aglue),'--out',str(audit)])]
    receipts=[];start=time.monotonic()
    for name,file,argv in stages:
        cmd=[sys.executable,*flags,str(source/file),*argv];t=time.monotonic()
        try:r=subprocess.run(cmd,cwd=work,env=env,capture_output=True,text=True,timeout=20)
        except subprocess.TimeoutExpired as error:raise RuntimeError('Incomplete '+name+' after20s; no exclusion established by this run') from error
        require(r.returncode==0,name+' failed: '+r.stderr)
        receipts.append({'stage':name,'seconds':time.monotonic()-t,'returncode':r.returncode,'stdout':json.loads(r.stdout)})
    c=json.loads(cap.read_text());g=json.loads(glue.read_text());a=json.loads(audit.read_text())
    require(c==json.loads(acap.read_text()) and g==json.loads(aglue.read_text()),'Whole independent producer/audit records must agree')
    require(sha256(canonical(c).encode()).hexdigest()==expected['capacity_whole_sha256'],'Complete capacity record pin differs')
    require(sha256(canonical(g).encode()).hexdigest()==expected['gluing_whole_sha256'],'Complete gluing record pin differs')
    require(c['surviving_relaxed_inventory_rows']==[expected['unique_survivor']],'Complete global original inventory survivor differs')
    require(len(c['all_nine_three_parent_type_cases'])==expected['type_cases'] and c['total_global_H_allocation_rows']==expected['global_H_allocation_rows'],'Complete count/type/H-label census differs')
    require([len(b['all_raw_phase_repair_counts']) for b in g['all_parent_full_physical_phase_blocks']]==expected['raw_original_phase_tuples'],'Full physical phase blocks missing')
    require([len(b['qualifying_original_phases_and_shapes']) for b in g['all_parent_full_physical_phase_blocks']]==expected['qualifying_phase_tuples'],'Qualifying literal phase blocks differ')
    require(len(g['all_800_original_phase_completions'])==expected['combined_literal_phase_completions'] and len(g['all_400_BASE_gluing_shapes'])==expected['protected_BASE_shapes'],'Complete phase/shape census differs')
    require(g['gluing_maximum']==expected['BASE_outside_upper']<g['outside_required']==expected['BASE_outside_required'],'BASE gluing contradiction absent')
    require(a['binary_controls']==expected['binary_controls'] and len(a['damages']['rejected_semantic_domain_damages'])==expected['semantic_damages'],'Complete binary/domain controls differ')
    result={'agent':'six-covering-2','role':'researcher','mode':args.mode,'seconds':time.monotonic()-start,
      'python':sys.version,'child_guard_seconds':20,'all_threads':1,'one_intensive_child_at_a_time':True,
      'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'stages':receipts,
      'capacity_whole_sha256':expected['capacity_whole_sha256'],'gluing_whole_sha256':expected['gluing_whole_sha256'],
      'all_full_mathematical_records_equal':True,'all_raw_capacity_streams_byte_equal':True,
      'all_raw_BASE_phase_streams_byte_equal':True,'independent_author_audit':a,
      'exactly_nine_implies_exactly_two_hole_parents':[2,6],'remaining_two_parent_counts':expected['remaining_two_parent_counts'],
      'status':'COMPLETE AUTHOR-CHECKED CONDITIONAL TWO-PARENT REDUCTION; independent review pending',
      'ordinary_proof_formalized':False,'independent_reviewer':False,'new_tenth_tail_bound_claimed':False,'global_bound_changed':False}
    (work/'verification.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(canonical({'mode':args.mode,'seconds':result['seconds'],'peak_child_RSS_KiB':result['peak_child_RSS_KiB'],
      'all_full_mathematical_records_equal':True,'hole_parents':[2,6],'global_bound_changed':False}))


if __name__=='__main__':main()
