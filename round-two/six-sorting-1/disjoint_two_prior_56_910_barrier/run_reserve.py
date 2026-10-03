"""Serial new-route seed and preparation reserve replay; no old negatives."""
import json
from pathlib import Path
import time

import run_preparations as serial

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def main():
    serial.operations_allow()
    old_stages = (WORK/'preparation-stages.json').read_bytes()
    started = time.monotonic()
    serial.child('reserve_seed.py')
    serial.child('verify_reserve_seed.py')
    serial.child('verify_reserve_seed.py', optimized=True)
    seed = serial.pair('reserve-seed-checked')
    serial.child('reserve_prune.py')
    serial.child('verify_reserve_preps.py')
    serial.child('verify_reserve_preps.py', optimized=True)
    checked = serial.pair('reserve-preparations-checked')
    producer = json.loads((WORK/'reserve-preparation-classifications.json').read_text())
    finite = {'literal_HIGH_word': [[5, 6], [9, 10]],
              'original_HIGH_cubes': 78,
              'seed_reserve_scalar_finite_sha256': seed['finite_sha256'],
              'preparation_reserve_scalar_finite_sha256': checked['finite_sha256'],
              'original_CLASS_maximum_live_costs': seed['finite']['CLASS_maximum_live_costs'],
              'all78_actual_seed_cost_plus_reserve_equal9': seed['finite']['all78_actual_seed_cost_plus_reserve_equal9'],
              'future_legal_event_words': seed['finite']['future_legal_event_words'],
              'census': checked['finite']['census'],
              'remaining_retained_offsets': producer['finite']['remaining_retained_offsets'],
              'remaining_function_ids': producer['finite']['remaining_function_ids'],
              'whole_route_exclusion_claimed': False,
              'entire_normal_O_records_equal': True}
    result = {'agent':'six-sorting-1', 'role':'researcher',
              'status':'FRESH_COMPLETE_ORIGINAL_HIGH_SEED_AND_SUFFICIENT_PREPARATION_RESERVE_REPLAY_ONLY',
              'finite':finite, 'finite_sha256':serial.digest(finite),
              'seconds':time.monotonic()-started}
    (WORK/'reserve-phase-complete.json').write_text(json.dumps(result, indent=2)+'\n')
    (WORK/'reserve-stages.json').write_text(json.dumps(serial.STAGES, indent=2)+'\n')
    (WORK/'preparation-stages.json').write_bytes(old_stages)
    print(json.dumps({**result, 'finite':{k:v for k,v in finite.items() if not k.startswith('remaining_')}}), flush=True)


if __name__ == '__main__':
    main()
