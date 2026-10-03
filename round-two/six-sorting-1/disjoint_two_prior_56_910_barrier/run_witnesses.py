"""Serial bounded original witnesses for one previously checked front interval.

Completed current-source arrays may be reused only with exact input/finite
bindings. No prior route or external negative corpus is loaded.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import time

import run_preparations as serial

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'
LOGIC = ('controls.py','cover.py','verify_original.py','preparations.py','verify_preparations.py',
         'screen_cuts.py','verify_cuts.py','reserve_seed.py','verify_reserve_seed.py',
         'reserve_prune.py','verify_reserve_preps.py','fronts.py','verify_fronts.py','bindings.py',
         'select_witnesses.py','verify_constant.py','universal-10060.json','prior/base.py',
         'prior/verify_base.py','prior/minimum_packed.py','prior/profile.py','prior/pruning.py',
         'prior/numeric.py','prior/fixture.json','prior/source-manifest.json')


def source_fingerprint():
    return serial.digest([[name,hashlib.sha256((ROOT/name).read_bytes()).hexdigest()] for name in LOGIC])


def read(file):
    result = json.loads((WORK/file).read_text())
    serial.need(serial.digest(result['finite']) == result['finite_sha256'], 'Changed finite record: '+file)
    return result


def main():
    serial.operations_allow()
    started = time.monotonic()
    first, last = map(int, sys.argv[1:3])
    source = source_fingerprint()
    prefix = f'{first:05}-{last:05}'
    front = json.loads((WORK/f'fronts03-{prefix}.json').read_text())
    checked = serial.pair('check03-'+prefix)
    serial.need(checked['finite']['producer_front_sha256'] == front['finite_sha256'],
                'Whole fresh bounded interface not checked')
    total = len(front['survivors'])
    old_stages = (WORK/'preparation-stages.json').read_bytes()
    counts, slices, misses, minimum = Counter(), [], [], None
    for a in range(0,total,1000):
        b = min(a+1000,total)
        serial.need(source_fingerprint() == source, 'Source changed during mathematical replay')
        proposed_name = f'constant03-{prefix}-{a:05}-{b:05}'
        proposed_path = WORK/(proposed_name+'.json')
        if not proposed_path.exists():
            serial.child('select_witnesses.py',first,last,a,b)
        proposed = read(proposed_name+'.json')
        serial.need(proposed['finite']['producer_front_sha256'] == front['finite_sha256'] and
                    serial.digest(proposed['cases']) == proposed['finite']['cases_sha256'] and
                    [r['front_index'] for r in proposed['cases']] == list(range(a,b)),
                    'Exact fresh case/front interval differs')
        normal_name = f'constant-check03-{prefix}-{a:05}-{b:05}'
        if not (WORK/(normal_name+'.json')).exists():
            serial.child('verify_constant.py',first,last,a,b)
        if not (WORK/(normal_name+'-O.json')).exists():
            serial.child('verify_constant.py',first,last,a,b,optimized=True)
        normal = serial.pair(normal_name)
        serial.need(normal['finite']['complete_case_certificate_sha256'] == proposed['finite']['cases_sha256'] and
                    normal['finite']['complete_front_cover_sha256'] == front['finite_sha256'],
                    'Independent scalar case/front bindings differ')
        counts.update(normal['finite']['census'])
        current = normal['finite']['minimum_selected_mass']
        if current is not None:
            minimum = current if minimum is None else min(minimum,current)
        misses.extend(proposed['finite']['inconclusive_front_indices'])
        slices.append({'case_slice':[a,b],'producer_finite_sha256':proposed['finite_sha256'],
                       'scalar_finite_sha256':normal['finite_sha256'],
                       'misses':proposed['finite']['inconclusive_front_indices']})
    positive = counts['independently_constant16_excluded_cases']
    serial.need(positive+len(misses) == total, 'Some actual surviving fronts are unaccounted for')
    finite = {'branch_index':3,'new_reserve_open_function_interval':[first,last],
              'actual_surviving_fronts':total,'census':dict(counts),'remaining_open_front_indices':misses,
              'minimum_selected_mass':minimum,'strict_size44_mass':1 << 44,
              'all_remaining_fronts_excluded':not misses,
              'source_computation_sha256':source,'front_scalar_finite_sha256':checked['finite_sha256'],
              'front_producer_finite_sha256':front['finite_sha256'],'slices':slices,
              'entire_normal_O_records_equal':True,'whole_route_exclusion_claimed':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'COMPLETE_CURRENT_SOURCE_BOUNDED_ORIGINAL_WITNESS_REPLAY',
              'finite':finite,'finite_sha256':serial.digest(finite),'seconds':time.monotonic()-started}
    (WORK/f'witness-phase-complete-{prefix}.json').write_text(json.dumps(result,indent=2)+'\n')
    (WORK/f'witness-stages-{prefix}.json').write_text(json.dumps(serial.STAGES,indent=2)+'\n')
    (WORK/'preparation-stages.json').write_bytes(old_stages)
    print(json.dumps(result),flush=True)


if __name__ == '__main__':
    main()
