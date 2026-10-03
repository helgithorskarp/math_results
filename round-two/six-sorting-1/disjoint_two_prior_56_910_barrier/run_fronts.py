"""One bounded fresh open-function slice; actual child guards remain55s."""
import json
from pathlib import Path
import sys
import time

import run_preparations as serial

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def main():
    serial.operations_allow()
    first, last = map(int, sys.argv[1:3])
    serial.need(0 <= first < last and last-first <= 128, 'At most128 open functions per pilot')
    old_stages = (WORK/'preparation-stages.json').read_bytes()
    started = time.monotonic()
    serial.child('fronts.py', 3, first, last)
    serial.child('verify_fronts.py', 3, first, last)
    serial.child('verify_fronts.py', 3, first, last, optimized=True)
    checked = serial.pair(f'check03-{first:05}-{last:05}')
    producer = json.loads((WORK/f'fronts03-{first:05}-{last:05}.json').read_text())
    finite = {'branch_index':3, 'new_reserve_open_function_interval':[first,last],
              'actual_function_ids':producer['retained_function_ids'],
              'front_scalar_finite_sha256':checked['finite_sha256'],
              'producer_front_finite_sha256':producer['finite_sha256'],
              'census':checked['finite']['census'],
              'survivors':len(producer['survivors']),
              'entire_normal_O_records_equal':True, 'whole_route_exclusion_claimed':False,
              'published_head_cut_ref':producer['public_universal_graph_ref']}
    result = {'agent':'six-sorting-1', 'role':'researcher',
              'status':'FRESH_COMPLETE_BOUNDED_ORIGINAL_HEAD_TAIL_REPLAY_ONLY',
              'finite':finite, 'finite_sha256':serial.digest(finite),
              'seconds':time.monotonic()-started}
    (WORK/f'front-phase-complete-{first:05}-{last:05}.json').write_text(json.dumps(result, indent=2)+'\n')
    (WORK/f'front-stages-{first:05}-{last:05}.json').write_text(json.dumps(serial.STAGES, indent=2)+'\n')
    (WORK/'preparation-stages.json').write_bytes(old_stages)
    print(json.dumps({**result,'finite':{k:v for k,v in finite.items() if k!='actual_function_ids'}}), flush=True)


if __name__ == '__main__':
    main()
