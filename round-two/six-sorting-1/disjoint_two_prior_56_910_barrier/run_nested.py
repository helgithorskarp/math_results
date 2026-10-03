"""Serial actual final-prefix nested check, canonical entire mathematical data."""
import hashlib
import json
from pathlib import Path
import time

import run_preparations as serial
from run_witnesses import source_fingerprint
from verify_nested import canonical

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def nested_fingerprint():
    return serial.digest([[name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest()]
        for name in ('nested-fixture.json','generate_nested.py','verify_nested.py','run_nested.py','prior/anchors.py')])


def main():
    serial.operations_allow()
    start = time.monotonic()
    old_stages = (WORK/'preparation-stages.json').read_bytes()
    serial.child('generate_nested.py')
    serial.child('verify_nested.py')
    serial.child('verify_nested.py',optimized=True)
    normal = json.loads((WORK/'nested-checked.json').read_text())
    optimized = json.loads((WORK/'nested-checked-O.json').read_text())
    serial.need(normal['finite']==optimized['finite'] and normal['metrics']==optimized['metrics'] and
                canonical(normal['finite'])==normal['finite_sha256']==optimized['finite_sha256'],
                'Entire nested scalar normal/O records differ')
    finite = {'branch_index':3,'literal_prefix_sha256':normal['finite']['literal_prefix_sha256'],
              'nested_scalar_finite_sha256':normal['finite_sha256'],
              'selected_mass':normal['finite']['selected_mass'],
              'actual_original_outer_labels':normal['finite']['actual_outer_labels'],
              'source_computation_sha256':source_fingerprint(),'nested_source_sha256':nested_fingerprint(),
              'entire_normal_O_records_equal':True,'global_size44_exclusion_claimed':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'COMPLETE_ACTUAL_P32_NESTED_FOUR_ORIGINAL_EXCLUSION_ONLY',
              'finite':finite,'finite_sha256':serial.digest(finite),'seconds':time.monotonic()-start}
    (WORK/'nested-phase-complete.json').write_text(json.dumps(result,indent=2)+'\n')
    (WORK/'nested-stages.json').write_text(json.dumps(serial.STAGES,indent=2)+'\n')
    (WORK/'preparation-stages.json').write_bytes(old_stages)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
