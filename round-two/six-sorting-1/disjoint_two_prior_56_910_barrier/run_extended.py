"""Extend at most32 genuine original-pool misses under unchanged job guards."""
import hashlib
import json
from pathlib import Path
import sys
import time

import run_preparations as serial
from inputs import current_cases
from run_witnesses import source_fingerprint

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def extension_fingerprint():
    return serial.digest([[name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest()]
                          for name in ('inputs.py','select_extended.py','verify_extended.py','run_extended.py')])


def main():
    serial.operations_allow()
    first,last = map(int,sys.argv[1:3])
    started = time.monotonic()
    old,front,phase = current_cases(first,last)
    misses = phase['finite']['remaining_open_front_indices']
    serial.need(0 < len(misses) <= 32, 'Require1..32 actual current-source misses')
    old_stages = (WORK/'preparation-stages.json').read_bytes()
    serial.child('select_extended.py',first,last)
    serial.child('verify_extended.py',first,last)
    serial.child('verify_extended.py',first,last,optimized=True)
    checked = serial.pair(f'extended-check-{first:05}-{last:05}')
    producer = json.loads((WORK/f'extended-{first:05}-{last:05}.json').read_text())
    serial.need(checked['finite']['entire_case_front_indices'] == misses and
                checked['finite']['actual_complete_front_sha256'] == front['finite_sha256'],
                'Exact actual preserved miss cover differs')
    finite = {'branch_index':3,'new_reserve_open_function_interval':[first,last],
              'actual_genuine_miss_front_indices':misses,
              'positive_extended_cases':checked['finite']['independently_positive_cases'],
              'remaining_open_indices':checked['finite']['remaining_open_indices'],
              'scalar_finite_sha256':checked['finite_sha256'],
              'producer_finite_sha256':producer['finite_sha256'],
              'previous_witness_phase_finite_sha256':phase['finite_sha256'],
              'source_computation_sha256':source_fingerprint(),
              'extension_source_sha256':extension_fingerprint(),
              'selected_original_occurrences':checked['finite']['selected_original_occurrences'],
              'minimum_selected_mass':checked['finite']['minimum_selected_mass'],
              'entire_normal_O_records_equal':True,'whole_route_exclusion_claimed':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'COMPLETE_CURRENT_SOURCE_ACTUAL_MISS_EXTENDED_ORIGINAL_REPLAY',
              'finite':finite,'finite_sha256':serial.digest(finite),'seconds':time.monotonic()-started}
    (WORK/f'extended-phase-complete-{first:05}-{last:05}.json').write_text(json.dumps(result,indent=2)+'\n')
    (WORK/f'extended-stages-{first:05}-{last:05}.json').write_text(json.dumps(serial.STAGES,indent=2)+'\n')
    (WORK/'preparation-stages.json').write_bytes(old_stages)
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    main()
