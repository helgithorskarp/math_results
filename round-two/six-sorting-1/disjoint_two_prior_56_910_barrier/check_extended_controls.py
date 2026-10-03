"""Four semantic damages to an actual extended original-cube certificate."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from controls import operations_allow
from run_preparations import ENV, need, digest

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def main():
    operations_allow()
    started = time.monotonic()
    destination = Path(sys.argv[1]) if len(sys.argv)>1 else WORK/'extended-controls-scratch'
    need(not destination.exists(), 'Fresh extended semantic control directory required')
    destination.mkdir(parents=True)
    for directory in ('prior','work'):
        (destination/directory).mkdir()
    for parent in (ROOT,ROOT/'prior'):
        relative = parent.relative_to(ROOT)
        for p in parent.iterdir():
            if p.is_file() and p.suffix in ('.py','.json'):
                shutil.copy2(p,destination/relative/p.name)
    phase_path = sorted(WORK.glob('extended-phase-complete-*.json'))[0]
    phase = json.loads(phase_path.read_text())
    first,last = phase['finite']['new_reserve_open_function_interval']
    label = f'{first:05}-{last:05}'
    need(phase['finite']['positive_extended_cases'] > 0 and
         phase['finite']['remaining_open_indices'] == [], 'Actual positive extension required')
    inputs = [f'fronts03-{label}.json',f'check03-{label}.json',f'check03-{label}-O.json',
              f'witness-phase-complete-{label}.json',f'extended-{label}.json']
    for p in sorted(WORK.glob(f'constant03-{label}-*.json')):
        inputs.append(p.name)
    for p in sorted(WORK.glob(f'constant-check03-{label}-*.json')):
        inputs.append(p.name)
    baseline = {}
    for name in inputs:
        raw = (WORK/name).read_bytes()
        baseline[name] = raw
        (destination/'work'/name).write_bytes(raw)
    original = json.loads(baseline[f'extended-{label}.json'])

    def missing_case(p):
        del p['cases'][0]
        p['finite']['positive_count'] -= 1

    def false_cost(p):
        case = p['cases'][0]
        w = case['selected_witnesses'][0]
        w['outer_record'][4] += 1
        w['label'] += 1
        case['selected_mass'] = sum(1 << x['label'] for x in case['selected_witnesses'])

    def nonstrict_mass(p):
        case = p['cases'][0]
        del case['selected_witnesses'][0]
        case['selected_mass'] = sum(1 << x['label'] for x in case['selected_witnesses'])
        need(case['selected_mass'] <= 1 << 44, 'Control must actually destroy strictness')

    def duplicate_class(p):
        case = p['cases'][0]
        need(len(case['selected_witnesses']) > 1, 'At least2 true original classes required for this control')
        case['selected_witnesses'][1] = deepcopy(case['selected_witnesses'][0])
        case['selected_mass'] = sum(1 << x['label'] for x in case['selected_witnesses'])

    tasks = (
        ('missing_actual_genuine_miss',missing_case,'Complete genuine-miss binding differs'),
        ('false_original_extended_cost',false_cost,'Whole original scalar record differs'),
        ('nonstrict_actual_root_mass',nonstrict_mass,'Strict extended original inequality fails'),
        ('duplicate_actual_marker_class',duplicate_class,'Duplicate current dyadic class'),
    )
    receipts = []
    for name,mutation,reason in tasks:
        for optimized in (False,True):
            operations_allow()
            damaged = deepcopy(original)
            mutation(damaged)
            damaged['finite']['extended_cases_sha256'] = digest(damaged['cases'])
            damaged['finite_sha256'] = digest(damaged['finite'])
            (destination/'work'/f'extended-{label}.json').write_text(json.dumps(damaged,indent=2)+'\n')
            command = [sys.executable]+(['-O'] if optimized else [])+[str(destination/'verify_extended.py'),str(first),str(last)]
            actual = subprocess.run(command,env=ENV,capture_output=True,text=True,timeout=55)
            (destination/(name+('-O' if optimized else '')+'.log')).write_text(actual.stdout+actual.stderr)
            need(actual.returncode != 0 and 'ValueError: '+reason in actual.stderr,
                 'Actual extended semantic damage accepted or rejected for a different/operational reason: '+name)
            receipts.append({'damage':name,'optimized':optimized,'returncode':actual.returncode,
                             'expected_mathematical_rejection':reason,'transport_hashes_repaired':True})
            print(json.dumps(receipts[-1]),flush=True)
    for name,raw in baseline.items():
        need((WORK/name).read_bytes()==raw, 'Actual original evidence changed during isolated controls')
    finite = {'damage_types':len(tasks),'actual_math_children':len(receipts),
              'actual_complete_extended_front_interval':[first,last],
              'all_rejections':receipts,'all_original_inputs_unchanged':True,
              'all_transport_hashes_repaired':True,'operational_failure_counted_as_math_rejection':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'ALL_FOUR_EXTENDED_SEMANTIC_DAMAGES_REJECTED_NORMALLY_AND_OPTIMIZED',
              'finite':finite,'finite_sha256':digest(finite),'seconds':time.monotonic()-started}
    (WORK/'extended-semantic-controls-complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='finite'}),flush=True)


if __name__ == '__main__':
    main()
