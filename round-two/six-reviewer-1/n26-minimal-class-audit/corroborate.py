"""Optional LATE native replay; never part of the sealed primary proof.

Use a separate process for the author's modules. Compare ALL original
operator, metric and kernel fields, not merely expected output hashes.
The adapter follows the credited earlier reviewer n24 comparison method.
"""
import argparse
from pathlib import Path
import sys
import os
import json
import hashlib
import subprocess
import time
import resource


def require(value, message):
    if not value:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--native-dir', type=Path, required=True)
    p.add_argument('--primary-record', type=Path, required=True)
    p.add_argument('--scratch', type=Path, required=True)
    a = p.parse_args()
    source = Path(__file__).resolve().parent
    native = a.native_dir.resolve()
    dest = a.scratch.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    provenance = json.loads((source/'PROVENANCE.json').read_text())
    seal = json.loads((source/'PRIMARY_SEAL.json').read_text())
    for name, row in seal['primary_files'].items():
        require(hashlib.sha256((source/name).read_bytes()).hexdigest() == row['sha256'],
                'Primary seal changed: '+name)
    for name, row in provenance['all18_target_file_whole_byte_pins'].items():
        raw = (native/name).read_bytes()
        require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                'Whole pinned native file: '+name)
    own = json.loads(a.primary_record.read_text())
    require(hashlib.sha256(a.primary_record.read_bytes()).hexdigest() ==
            json.loads((source/'expected.json').read_text())['record_sha256'],
            'Complete primary regenerated record')
    require(json.loads((source/'WITNESS.json').read_text()) ==
            json.loads((native/'CERTIFICATE.json').read_text()),
            'All declarative certificate fields and numbers')
    env = os.environ.copy()
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:
        env[key] = '1'
    receipts = []

    def run(command, role):
        start = time.monotonic()
        child = subprocess.run(command, cwd=dest, env=env,
                               capture_output=True, text=True, timeout=45)
        require(child.returncode == 0, role+' failed: '+child.stderr)
        result = json.loads(child.stdout)
        receipt = {'role':role, 'seconds':round(time.monotonic()-start,6),
                   'exit':child.returncode, 'result':result,
                   'cumulative_peak_child_rss_kib':
                   resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
        receipts.append(receipt)
        print(json.dumps({'role':role,'seconds':receipt['seconds'],'exit':0}),flush=True)
        return result

    outputs = []
    for optimize in [False,True]:
        out = dest/('native-O.json' if optimize else 'native-normal.json')
        command = [sys.executable,'-I','-B']+(['-O'] if optimize else [])
        command += [str(native/'verify.py'),'--output',str(out),
                    '--check',str(native/'expected.json'),
                    '--mode',str(dest/('mode-O.json' if optimize else 'mode-normal.json'))]
        result = run(command, 'late native optimized' if optimize else 'late native normal')
        require(result['expected_checked'] and result['summary']['rejected_damages'] == 13,
                'All native expected fields and internal damages')
        outputs.append(out.read_bytes())
    require(outputs[0] == outputs[1], 'Whole native normal/O records')
    complete = json.loads(outputs[0])
    require(complete['zero_core_floor_result']['table'] == own['completed_table'],
            'Entire regenerated original disjoint table')
    require(complete['zero_core_floor_result']['actual_empty']['row'] ==
            own['summary']['actual_empty_rows'] and
            complete['zero_core_floor_result']['actual_empty']['loop'] ==
            own['summary']['actual_empty_loop'], 'ALL original empty entries and loop')
    operator = dest/'native-operators.json'
    script = '''import sys,json
from pathlib import Path
from fractions import Fraction as Q
sys.path.insert(0,sys.argv[1])
from model import specification,table,sectors
from original_forms import original_form
w=json.loads(Path(sys.argv[1],'CERTIFICATE.json').read_text())
spec=specification(w['n'],tuple(w['active']));B=table(spec,list(map(Q,w['values'])))
out={'full_table':B,'original_blocks':[original_form(spec,x) for x in sectors(spec,B)]}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'),default=str)+'\\n').encode()
Path(sys.argv[2]).write_bytes(raw)
print(json.dumps({'full_physical_degrees':len(out['original_blocks']),'bytes':len(raw)}))
'''
    run([sys.executable,'-I','-B','-c',script,str(native),str(operator)],
        'late full operator export in separate native process')
    other = json.loads(operator.read_text())
    require(other['full_table'] == own['completed_table'], 'Whole exported table')
    require(len(other['original_blocks']) == len(own['sectors']) == 14,
            'Every physical degree including mean and middle13')
    entries = 0
    for x,y in zip(own['sectors'],other['original_blocks']):
        require(x['j'] == y['j'] and x['sizes'] == y['layers'] and
                x['multiplicity'] == y['multiplicity'], 'All sector indices and multiplicities')
        for field,other_field in [('actual_original_lower','lower'),
                                  ('actual_original_upper','upper'),
                                  ('actual_original_metric','gram'),
                                  ('actual_original_kernel','kernels')]:
            require(x[field] == y[other_field], 'WHOLE original physical field '+field)
            entries += sum(len(row) for row in x[field])
    for name,row in seal['primary_files'].items():
        require(hashlib.sha256((source/name).read_bytes()).hexdigest() == row['sha256'],
                'Primary changed during native corroboration')
    record = {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
              'late_corroboration_only_not_primary_proof':True,
              'python':sys.version,'native_threads':1,'serial_children':True,
              'unchanged_child_guard_seconds':45,'all6_primary_seals_unchanged':True,
              'all18_target_files_pinned':True,'all_declarative_certificate_fields_equal':True,
              'entire_primary_native_tables_empty_rows_loop_equal':True,
              'full_original_operator_metric_kernel_fields_equal':56,
              'all_compared_physical_entries':entries,
              'normal_O_whole_native_records_equal':True,
              'native_record_bytes':len(outputs[0]),
              'native_record_sha256':hashlib.sha256(outputs[0]).hexdigest(),
              'native_internal_damage_rejections':26,
              'rss_is_cumulative_maximum_not_per_child':True,'receipts':receipts}
    (dest/'corroboration.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__ == '__main__':
    main()
