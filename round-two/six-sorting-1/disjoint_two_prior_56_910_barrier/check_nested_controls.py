"""Actual inner-floor, full-profile, carrier, class and strict-mass damages."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

from controls import operations_allow
from run_preparations import ENV, need
from verify_nested import canonical

ROOT = Path(__file__).resolve().parent
WORK = ROOT/'work'


def main():
    operations_allow()
    start = time.monotonic()
    destination = Path(sys.argv[1]) if len(sys.argv)>1 else WORK/'nested-controls-scratch'
    need(not destination.exists(), 'Fresh nested control directory required')
    destination.mkdir(parents=True)
    (destination/'prior').mkdir()
    (destination/'work').mkdir()
    for parent in (ROOT,ROOT/'prior'):
        relative = parent.relative_to(ROOT)
        for p in parent.iterdir():
            if p.is_file() and p.suffix in ('.py','.json'):
                shutil.copy2(p,destination/relative/p.name)
    fixture_raw = (ROOT/'nested-fixture.json').read_bytes()
    proposal_raw = (WORK/'nested-proposal.json').read_bytes()
    fixture,proposal = json.loads(fixture_raw),json.loads(proposal_raw)

    def false_floor(f,p):
        f['original_domains'][0][2] = 18
        f['expected_labels'][0] = 44
        f['expected_selected_mass'] = sum(1 << x for x in f['expected_labels'])
        p['records'][0]['claimed_B7'] = 18
        p['records'][0]['label'] = 44

    def wrong_carrier(f,p):
        gate = p['records'][0]['actual_oriented_pruning']['retained_prefix'][0]
        gate.reverse()

    def wrong_complete_inner_profile(f,p):
        p['records'][0]['inner_profiles']['two_minima']['records_sha256'] = '0'*64

    def overlapping_actual_classes(f,p):
        f['original_domains'][1] = deepcopy(f['original_domains'][0])
        f['expected_labels'][1] = f['expected_labels'][0]
        f['expected_selected_mass'] = sum(1 << x for x in f['expected_labels'])
        p['records'][1] = deepcopy(p['records'][0])

    def exact_nonstrict_mass(f,p):
        del f['original_domains'][-1]
        del f['expected_labels'][-1]
        del p['records'][-1]
        f['expected_selected_mass'] = sum(1 << x for x in f['expected_labels'])
        need(f['expected_selected_mass']==1<<44, 'Control must have exactly nonstrict mass2^44')

    tasks = (
        ('unsupported_actual_inner_floor',false_floor,'Scalar actual inner bound does not justify the chosen floor'),
        ('reversed_actual_carrier_gate',wrong_carrier,'Entire actual-original nested records differ between algorithms'),
        ('false_full_inner_original_record_hash',wrong_complete_inner_profile,'Entire actual-original nested records differ between algorithms'),
        ('overlapping_actual_outer_classes',overlapping_actual_classes,'Nested actual outer marker classes overlap'),
        ('exactly_nonstrict_actual_mass',exact_nonstrict_mass,'Actual scalar nested inequality is not strict'),
    )
    receipts = []
    for name,mutation,reason in tasks:
        for optimized in (False,True):
            operations_allow()
            f,p = deepcopy(fixture),deepcopy(proposal)
            mutation(f,p)
            p['finite']['actual_original_nested_records_sha256'] = canonical(p['records'])
            p['finite']['actual_outer_labels'] = list(f['expected_labels'])
            p['finite']['selected_mass'] = f['expected_selected_mass']
            p['finite_sha256'] = canonical(p['finite'])
            (destination/'nested-fixture.json').write_text(json.dumps(f,indent=2)+'\n')
            (destination/'work/nested-proposal.json').write_text(json.dumps(p,indent=2)+'\n')
            command = [sys.executable]+(['-O'] if optimized else [])+[str(destination/'verify_nested.py')]
            actual = subprocess.run(command,env=ENV,capture_output=True,text=True,timeout=55)
            (destination/(name+('-O' if optimized else '')+'.log')).write_text(actual.stdout+actual.stderr)
            need(actual.returncode != 0 and 'ValueError: '+reason in actual.stderr,
                 'Nested semantic damage accepted or rejected for a different/operational reason: '+name)
            receipts.append({'damage':name,'optimized':optimized,'returncode':actual.returncode,
                             'expected_mathematical_rejection':reason,'transport_hashes_repaired':True})
            print(json.dumps(receipts[-1]),flush=True)
    need((ROOT/'nested-fixture.json').read_bytes()==fixture_raw and
         (WORK/'nested-proposal.json').read_bytes()==proposal_raw, 'Original nested inputs changed')
    finite = {'damage_types':len(tasks),'actual_math_children':len(receipts),'all_rejections':receipts,
              'all_original_inputs_unchanged':True,'all_transport_hashes_repaired':True,
              'operational_failure_counted_as_math_rejection':False}
    result = {'agent':'six-sorting-1','role':'researcher',
              'status':'ALL_FIVE_NESTED_SEMANTIC_DAMAGES_REJECTED_IN_BOTH_PYTHON_MODES',
              'finite':finite,'finite_sha256':canonical(finite),'seconds':time.monotonic()-start}
    (WORK/'nested-semantic-controls-complete.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='finite'}),flush=True)


if __name__=='__main__':
    main()
