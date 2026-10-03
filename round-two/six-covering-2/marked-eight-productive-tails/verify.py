"""Copy only pinned arithmetic sources, regenerate and compare two modes."""
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--work',type=Path,default=root/'generated')
    args = parser.parse_args()
    work = args.work.resolve()
    require(not work.exists(), 'Fresh isolated work path required')
    expected = json.loads((root/'expected.json').read_text())
    for name, target in expected['source_sha256'].items():
        require(sha256((root/name).read_bytes()).hexdigest() == target, 'Arithmetic source changed: '+name)
    work.mkdir(parents=True)
    for name in expected['source_sha256']:
        shutil.copy2(root/name,work/name)
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','NUMEXPR_MAX_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
        env[key] = '1'
    runs = []
    both = []
    for mode, switches in (('normal',['-B']),('O',['-O','-B'])):
        record_path = work/('seven-tail-'+mode+'.json')
        records = {}
        commands = [('producer','seven_tail.py',['--out',str(record_path)]),
                    ('literal_audit','audit.py',[str(record_path)])]
        for label, source, arguments in commands:
            start = time.monotonic()
            result = subprocess.run([sys.executable,*switches,str(work/source),*arguments],
                                    cwd=work,env=env,capture_output=True,text=True,
                                    timeout=20,check=True)
            record = json.loads(record_path.read_text()) if label == 'producer' else json.loads(result.stdout)
            require(digest(record) == expected['whole_record_sha256'][label],
                    'Whole mathematical output differs: '+label)
            records[label] = record
            runs.append({'mode':mode,'record':label,'returncode':result.returncode,
                         'seconds':time.monotonic()-start,'whole_record_sha256':digest(record)})
        require(records['producer']['maximum_seven_tail_BASE_holes'] == 175 and
                records['literal_audit']['seven_tail_capacity'] == 175,
                'Seven-tail capacity not established')
        require(records['literal_audit']['every_full_mathematical_field_compared'],
                'Full literal audit missing')
        both.append(records)
    require(both[0] == both[1], 'Every normal/O mathematical field must agree')
    output = {'agent':'six-covering-2','role':'researcher','all_full_mathematical_records_equal':True,
              'source_only_isolated':True,'runs':runs,'seven_tail_capacity':175,
              'BASE_holes_lower_bound_imported_from_public9934':177,
              'public9934_previously_proved_productive_TAILs_at_least':7,
              'marked_essential_domain_productive_TAIL_lower_bound':8,
              'ordinary_public9934_dependency_replayed_by_this_driver':False,
              'capacity_175_claimed_sharp':False,'raw_original_phase_pairs':2698300,
              'third_parent_odd_phase_entries':43725,'complete_binary_controls':2091,
              'semantic_damages_per_mode':9,'guard_seconds_per_child':20,'native_threads':1,
              'one_intensive_child_at_a_time':True,
              'peak_child_RSS_KiB':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'independent_reviewer':False,'global_bound_changed':False}
    (work/'verification.json').write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
