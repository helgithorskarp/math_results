"""Actual semantic damages with repaired hashes, normal and optimized children.

Fresh input copies are mutated; original mathematical data remain intact.
Every reported rejection must match a mathematical reason, never a timeout.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

from controls import operations_allow
from run_preparations import ENV, need, digest

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT/'work'


def main():
    operations_allow()
    started = time.monotonic()
    destination = Path(sys.argv[1]) if len(sys.argv)>1 else ORIGINAL/'semantic-controls-scratch'
    need(not destination.exists(), 'Fresh semantic control directory required; preserve old receipts')
    destination.mkdir(parents=True)
    for directory in ('prior','prior/work','work'):
        (destination/directory).mkdir(exist_ok=True)
    for parent in (ROOT,ROOT/'prior'):
        relative = parent.relative_to(ROOT)
        for p in parent.iterdir():
            if p.is_file() and p.suffix in ('.py','.json'):
                shutil.copy2(p,destination/relative/p.name)
    for p in (ROOT/'prior/work').glob('*.json'):
        shutil.copy2(p,destination/'prior/work'/p.name)
    inputs = ('branch03.json','checked03.json','checked03-O.json','cuts03.json',
              'two-prior-independent-original-cubes.json','preparation-bindings.json',
              'preparation-phase-complete.json','reserve-seed.json','reserve-seed-checked.json',
              'reserve-seed-checked-O.json','reserve-preparation-classifications.json',
              'reserve-preparations-checked.json','reserve-preparations-checked-O.json',
              'reserve-phase-complete.json','fronts03-00000-00128.json',
              'check03-00000-00128.json','check03-00000-00128-O.json',
              'constant03-00000-00128-00000-01000.json')
    for name in inputs:
        shutil.copy2(ORIGINAL/name,destination/'work'/name)
    baseline = {name:(destination/'work'/name).read_bytes() for name in inputs}
    receipts = []

    def read(name):
        return json.loads(baseline[name])

    def write(name,value):
        (destination/'work'/name).write_text(json.dumps(value,indent=2)+'\n')

    def finite_top(value, omit):
        return {k:v for k,v in value.items() if k not in omit}

    def repair_front(front):
        front['survivors_sha256'] = digest(front['survivors'])
        front['rejections_sha256'] = digest(front['rejections'])
        finite = finite_top(front,{'agent','role','status','survivors','rejections',
                                  'finite_sha256','seconds','maximum_rss_kib','scope'})
        front['finite_sha256'] = digest(finite)
        write('fronts03-00000-00128.json',front)

    def repair_cases(proposed):
        proposed['finite']['cases_sha256'] = digest(proposed['cases'])
        proposed['finite_sha256'] = digest(proposed['finite'])
        write('constant03-00000-00128-00000-01000.json',proposed)

    def missing_function():
        p = read('branch03.json')
        del p['functions'][0]
        p['full_functions_sha256'] = digest(p['functions'])
        p['full_functions_seen'] = len(p['functions'])
        finite = finite_top(p,{'agent','role','status','functions','minimum_lock_proposals',
                              'finite_sha256','seconds','maximum_rss_kib','source_dependency','scope'})
        p['finite_sha256'] = digest(finite)
        write('branch03.json',p)

    def false_pivot():
        p = read('cuts03.json')
        row = next(r for r in p['classified_preparations'] if r['status'].startswith('ADDITIONAL_'))
        row['pivot_port'] = 2
        p['classification_sha256'] = digest(p['classified_preparations'])
        p['census']['pivot_3'] -= 1
        p['census']['pivot_2'] = 1
        p['finite_sha256'] = digest({k:p[k] for k in
            ('branch_index','HIGH_word','checked_preparation_functions_sha256','classification_sha256','census')})
        write('cuts03.json',p)

    def false_reserve():
        p = read('reserve-preparation-classifications.json')
        row = next(r for r in p['classifications'] if r['witness'] is not None)
        row['witness']['current_HIGH_class_maximum_E'] -= 1
        p['finite']['classification_sha256'] = digest(p['classifications'])
        p['finite_sha256'] = digest(p['finite'])
        write('reserve-preparation-classifications.json',p)

    def missing_head():
        p = read('fronts03-00000-00128.json')
        index = next(i for i,r in enumerate(p['rejections']) if r['stage']=='HEAD')
        del p['rejections'][index]
        p['census']['head_WHOLE_ORIGINAL_LOW_IDENTITY'] -= 1
        repair_front(p)

    def erased_root():
        p = read('fronts03-00000-00128.json')
        row = next(r for r in p['rejections'] if r.get('moved_live_root')==8)
        row['moved_live_root'] = 7
        repair_front(p)

    def false_conditional_output():
        p = read('fronts03-00000-00128.json')
        row = next(r for r in p['rejections'] if r['kind']=='PUBLIC_CONDITIONAL_MAXIMUM_OBSTRUCTION')
        row['F40'] ^= 8
        repair_front(p)

    def false_original_cost():
        p = read('constant03-00000-00128-00000-01000.json')
        case = p['cases'][0]
        row = case['selected_witnesses'][0]
        row['outer_record'][4] += 1
        row['label'] += 1
        case['selected_mass'] = sum(1 << r['label'] for r in case['selected_witnesses'])
        repair_cases(p)

    def overlapping_classes():
        p = read('constant03-00000-00128-00000-01000.json')
        case = next(r for r in p['cases'] if len(r['selected_witnesses'])==2)
        case['selected_witnesses'][1] = deepcopy(case['selected_witnesses'][0])
        case['selected_mass'] = sum(1 << r['label'] for r in case['selected_witnesses'])
        repair_cases(p)

    def false_oriented_carrier():
        p = read('constant03-00000-00128-00000-01000.json')
        case = p['cases'][0]
        row = case['selected_witnesses'][0]
        # A different claimed seven-port word cannot replace the actual
        # oriented carrier word; repairing packet checksums does not help.
        row['retained_Q_sha256'] = digest([[6,0]])
        repair_cases(p)

    tasks = (
        ('missing_full64_function','verify_preparations.py',[3,4],missing_function,
         'Complete independent function set differs'),
        ('false_original_free_pivot','verify_cuts.py',[3,4],false_pivot,
         'Claimed wrong full-input rank is correct'),
        ('false_actual_class_reserve','verify_reserve_preps.py',[],false_reserve,
         'Reported future CLASS maximum or marked-touch reserve differs'),
        ('missing_actual_head','verify_fronts.py',[3,0,128],missing_head,
         'Missing whole-cube head identity'),
        ('erased_moved_live_root','verify_fronts.py',[3,0,128],erased_root,
         'Public10060 cut does not match actual full preparation, zero head or moved root'),
        ('false_conditional_full_function_output','verify_fronts.py',[3,0,128],false_conditional_output,
         'Public10060 cut does not match actual full preparation, zero head or moved root'),
        ('false_original_marked_cost','verify_constant.py',[0,128,0,1000],false_original_cost,
         'Original scalar deletion/identity record differs'),
        ('overlapping_current_marker_classes','verify_constant.py',[0,128,0,1000],overlapping_classes,
         'Selected current outer classes overlap'),
        ('false_oriented_carrier_word','verify_constant.py',[0,128,0,1000],false_oriented_carrier,
         'Full oriented carrier word differs'),
    )
    for label, script, args, mutation, expected in tasks:
        for optimized in (False,True):
            operations_allow()
            for name,raw in baseline.items():
                (destination/'work'/name).write_bytes(raw)
            mutation()
            command = [sys.executable]+(['-O'] if optimized else [])+[str(destination/script),*map(str,args)]
            now = time.monotonic()
            actual = subprocess.run(command,env=ENV,capture_output=True,text=True,timeout=55)
            (destination/(label+('-O' if optimized else '')+'.log')).write_text(actual.stdout+actual.stderr)
            need(actual.returncode != 0 and 'ValueError: '+expected in actual.stderr,
                 'Semantic damage accepted, wrong failure or operational limit: '+label)
            receipt = {'damage':label,'optimized':optimized,'returncode':actual.returncode,
                       'expected_mathematical_rejection':expected,'transport_hashes_repaired':True}
            receipts.append(receipt)
            print(json.dumps({**receipt,'seconds':time.monotonic()-now}),flush=True)
    for name,raw in baseline.items():
        (destination/'work'/name).write_bytes(raw)
        need((ORIGINAL/name).read_bytes()==raw, 'Original proof input changed during isolated controls')
    finite = {'damage_types':len(tasks),'actual_math_children':len(receipts),
              'entire_normal_O_damage_labels_equal':True,'all_rejections':receipts,
              'all_transport_hashes_repaired':True,'all_original_inputs_unchanged':True,
              'operational_failure_counted_as_math_rejection':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'ALL_NINE_SEMANTIC_DAMAGES_REJECTED_IN_BOTH_PYTHON_MODES',
              'finite':finite,'finite_sha256':digest(finite),'seconds':time.monotonic()-started}
    (ORIGINAL/'semantic-controls-complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='finite'}),flush=True)


if __name__ == '__main__':
    main()
