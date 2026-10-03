"""Cold source-only normal/O replay; all complete records must agree."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(record):
    return sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    root = Path(__file__).resolve().parent
    parser=argparse.ArgumentParser();parser.add_argument('--work',type=Path,default=root/'generated');args=parser.parse_args()
    work=args.work.resolve();require(not work.exists(),'Fresh isolated replay path required')
    expected=json.loads((root/'expected.json').read_text())
    for name, target in expected['source_sha256'].items():
        require(sha256((root/name).read_bytes()).hexdigest()==target,'Arithmetic source changed: '+name)
    work.mkdir(parents=True)
    for name in expected['source_sha256']:shutil.copy2(root/name,work/name)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS',
                'NUMEXPR_MAX_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):env[key]='1'
    runs=[];both=[]
    for mode,switches in (('normal',['-B']),('O',['-O','-B'])):
        path=work/('nine-tail-'+mode+'.json');records={}
        for label,source,arguments in (('producer','nine_tail.py',['--out',str(path)]),
                                       ('literal_audit','audit.py',[str(path)])):
            start=time.monotonic()
            result=subprocess.run([sys.executable,*switches,str(work/source),*arguments],cwd=work,
                                  env=env,capture_output=True,text=True,timeout=20)
            require(result.returncode==0,'Arithmetic child failed: '+result.stderr)
            record=json.loads(path.read_text()) if label=='producer' else json.loads(result.stdout)
            require(digest(record)==expected['whole_record_sha256'][label],'Whole output differs: '+label)
            records[label]=record
            runs.append({'mode':mode,'record':label,'seconds':time.monotonic()-start,
                         'whole_record_sha256':digest(record),'returncode':result.returncode})
        require(records['literal_audit']['every_full_mathematical_field_compared'],'Full physical comparison missing')
        require(records['producer']['new_productive_TAIL_lower_bound']==9,'Wrong conditional tail bound')
        both.append(records)
    require(both[0]==both[1],'Every complete normal/O mathematical field must agree')
    output={'agent':'six-covering-2','role':'researcher','source_only_isolated':True,
            'all_full_mathematical_records_equal':True,'runs':runs,
            'new_productive_TAIL_lower_bound':9,'BASE177_and_prior8_dependencies_replayed_by_driver':False,
            'new_three_parent_two_parent_and_BASE_gluing_replayed':True,
            'H_raw_union_entries':351584,'original_phase_counts_compared':46856,
            'BASE_raw_phase_rows_compared':46255,'local_binary_controls':10980,
            'semantic_damages_per_mode':17,'guard_seconds_per_child':20,'native_threads':1,
            'one_intensive_child_at_a_time':True,
            'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
            'ordinary_proof_formalized':False,'independent_reviewer':False,'global_bound_changed':False}
    (work/'verification.json').write_text(json.dumps(output,sort_keys=True,indent=2)+'\n')
    print(json.dumps(output,sort_keys=True,indent=2))


if __name__=='__main__':main()
