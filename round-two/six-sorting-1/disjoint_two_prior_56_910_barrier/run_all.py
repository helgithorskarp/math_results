"""Complete the scoped fresh branch in serial128-function/1000-front jobs.

No guard is enlarged. Any actual miss, failed child or operation barrier
leaves the branch incomplete. Existing current-source complete phases are
reused with their exact source and finite bindings; old negatives are absent.
"""
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import time

import run_preparations as serial
from run_witnesses import read, source_fingerprint
from run_extended import extension_fingerprint
from run_nested import nested_fingerprint

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def driver(script, first, last):
    serial.operations_allow()
    command = [sys.executable,str(ROOT/script),str(first),str(last)]
    # This lightweight serial driver has no aggregate timeout. Every actual
    # mathematical subprocess is already guarded55s, with internal45s.
    result = subprocess.run(command,env=serial.ENV,capture_output=True,text=True)
    (WORK/f'all-{script}-{first:05}-{last:05}.log').write_text(result.stdout+result.stderr)
    serial.need(result.returncode == 0, 'Incomplete bounded phase; inspect recorded log; no exclusion')


def main():
    started = time.monotonic()
    serial.operations_allow()
    source = source_fingerprint()
    preparation = read('preparation-phase-complete.json')
    reserve = read('reserve-phase-complete.json')
    total = len(reserve['finite']['remaining_function_ids'])
    expected_ids = reserve['finite']['remaining_function_ids']
    intervals, ids, counts, front_counts = [], [], Counter(), Counter()
    minimum = None
    for first in range(0,total,128):
        serial.operations_allow()
        serial.need(source_fingerprint() == source, 'Source changed during complete finite cover')
        last = min(first+128,total)
        label = f'{first:05}-{last:05}'
        if not (WORK/f'front-phase-complete-{label}.json').exists():
            driver('run_fronts.py',first,last)
        front = read('front-phase-complete-'+label+'.json')
        if not (WORK/f'witness-phase-complete-{label}.json').exists():
            driver('run_witnesses.py',first,last)
        witness = read('witness-phase-complete-'+label+'.json')
        serial.need(witness['finite']['source_computation_sha256'] == source and
                    witness['finite']['new_reserve_open_function_interval'] == [first,last] and
                    witness['finite']['front_producer_finite_sha256'] == front['finite']['producer_front_finite_sha256'] and
                    witness['finite']['front_scalar_finite_sha256'] == front['finite']['front_scalar_finite_sha256'],
                    'Current-source checked whole interval binding differs')
        actual_misses = witness['finite']['remaining_open_front_indices']
        extension = None
        if actual_misses:
            serial.need(len(actual_misses) <= 32, 'More than32 actual misses; preserve them without enlarging guards')
            if not (WORK/f'extended-phase-complete-{label}.json').exists():
                driver('run_extended.py',first,last)
            extended = read('extended-phase-complete-'+label+'.json')
            ef = extended['finite']
            serial.need(ef['actual_genuine_miss_front_indices'] == actual_misses and
                        ef['previous_witness_phase_finite_sha256'] == witness['finite_sha256'] and
                        ef['source_computation_sha256'] == source and
                        ef['extension_source_sha256'] == extension_fingerprint(),
                        'Independent actual-miss/source bindings differ')
            final_open = ef['remaining_open_indices']
            nested = None
            if final_open:
                serial.need(first==1536 and last==1594 and final_open==[449],
                            'Another actual miss needs its own proof; no whole route inference')
                if not (WORK/'nested-phase-complete.json').exists():
                    driver('run_nested.py',first,last)
                nested_phase = read('nested-phase-complete.json')
                nf = nested_phase['finite']
                actual_front = json.loads((WORK/f'fronts03-{label}.json').read_text())['survivors'][449]
                serial.need(nf['source_computation_sha256']==source and
                            nf['nested_source_sha256']==nested_fingerprint() and
                            nf['literal_prefix_sha256']==actual_front['prefix_sha256'] and
                            nf['selected_mass'] > 1<<44,
                            'Nested proof is not bound to this actual original front and current source')
                counts['independently_nested_cases'] += 1
                minimum = nf['selected_mass'] if minimum is None else min(minimum,nf['selected_mass'])
                nested = {'phase_finite_sha256':nested_phase['finite_sha256'],
                          'scalar_finite_sha256':nf['nested_scalar_finite_sha256'],
                          'actual_front_index':449,'literal_prefix_sha256':nf['literal_prefix_sha256']}
            serial.need(ef['positive_extended_cases']+len(final_open)==len(actual_misses) and
                        (not final_open or nested is not None),
                        'Unaccounted actual sufficient misses remain; no whole route inference')
            counts['independently_extended_cases'] += ef['positive_extended_cases']
            counts['extended_selected_original_occurrences'] += ef['selected_original_occurrences']
            current_extended = ef['minimum_selected_mass']
            if current_extended is not None:
                minimum = current_extended if minimum is None else min(minimum,current_extended)
            extension = {'phase_finite_sha256':extended['finite_sha256'],
                         'scalar_finite_sha256':ef['scalar_finite_sha256'],
                         'actual_genuine_miss_front_indices':actual_misses,
                         'independently_positive_cases':ef['positive_extended_cases'],
                         'nested_remainder':nested}
        else:
            serial.need(witness['finite']['all_remaining_fronts_excluded'], 'False complete witness flag')
        actual_ids = front['finite']['actual_function_ids']
        serial.need(actual_ids == expected_ids[first:last], 'One actual complete function interval is missing')
        ids.extend(actual_ids)
        counts.update(witness['finite']['census'])
        front_counts.update(front['finite']['census'])
        current = witness['finite']['minimum_selected_mass']
        if current is not None:
            minimum = current if minimum is None else min(minimum,current)
        intervals.append({'new_reserve_open_function_interval':[first,last],
                          'front_scalar_finite_sha256':front['finite']['front_scalar_finite_sha256'],
                          'front_phase_finite_sha256':front['finite_sha256'],
                          'witness_phase_finite_sha256':witness['finite_sha256'],
                          'actual_surviving_fronts':witness['finite']['actual_surviving_fronts'],
                          'independently_closed_fronts':witness['finite']['census'].get('independently_constant16_excluded_cases',0)+len(actual_misses),
                          'extension':extension})
        progress = {'agent':'six-sorting-1','role':'researcher',
                    'status':'ACTIVE_SCOPED_FULL_BRANCH_SERIAL_PARTITION',
                    'completed_open_functions':len(ids),'total_open_functions':total,
                    'source_computation_sha256':source,'intervals':intervals,
                    'no_whole_route_claim_before_final_partition':True}
        (WORK/'whole-progress.json').write_text(json.dumps(progress,indent=2)+'\n')
        print(json.dumps({'completed_functions':len(ids),'total_functions':total,
                          'last_interval':[first,last],'fronts':intervals[-1]['actual_surviving_fronts'],
                          'closed_fronts':intervals[-1]['independently_closed_fronts']}),flush=True)
    serial.need(ids == expected_ids and len(ids) == len(set(ids)), 'Complete preparation-function partition differs')
    finite = {'branch_index':3,'literal_HIGH_word':[[5,6],[9,10]],
              'source_computation_sha256':source,
              'preparation_phase_finite_sha256':preparation['finite_sha256'],
              'reserve_phase_finite_sha256':reserve['finite_sha256'],
              'full_preparation_functions':preparation['finite']['full_functions'],
              'preparation_free_cut_census':preparation['finite']['cut_census'],
              'reserve_census':reserve['finite']['census'],'open_functions_checked':total,
              'checked_function_ids_sha256':serial.digest(ids),'intervals':intervals,
              'original_head_tail_census':dict(front_counts),'original_witness_census':dict(counts),
              'minimum_selected_mass':minimum,'strict_size44_mass':1 << 44,
              'all_preparations_partitioned_and_excluded':True,
              'entire_normal_O_records_equal':True,'actual_prep_length_bounded':False,
              'suffix_depth_bounded':False,'conditional_route_only':True,
              'global_size44_exclusion_claimed':False,'external_person_review_claimed':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'COMPLETE_PRIVATE_SCOPED_BRANCH_PARTITION_PENDING_COLD_SEAL_AND_SEMANTIC_CONTROLS',
              'finite':finite,'finite_sha256':serial.digest(finite),'seconds':time.monotonic()-started}
    (WORK/'whole-result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({**result,'finite':{k:v for k,v in finite.items() if k!='intervals'}}),flush=True)


if __name__ == '__main__':
    main()
