"""Reject semantic damage to the complete evidence, with checks live under -O."""
from copy import deepcopy
import json
from pathlib import Path
import audit
import check

root = Path(__file__).parent
original = json.loads((root/'certificate.json').read_text())
expected = json.loads((root/'expected.json').read_text())
check.require(check.replay(original) == expected and audit.replay(original)[0] == expected,
              'undamaged full evidence fails')
damages = []


def damage(name, change):
    c = deepcopy(original)
    change(c)
    damages.append((name,c))


damage('wrong physical period', lambda c:c.update(period=5040))
damage('wrong target family', lambda c:c.update(target_moduli=[18,6]))
damage('missing original720 label', lambda c:c['labels'].remove(720))
damage('wrong original9 phase', lambda c:c.update(fixed=[[8,5],[9,0]]))
damage('missing new45 deduction', lambda c:c['anchors'].pop())
damage('wrong sequential overlap', lambda c:c.update(forced_overlap=36,hole_lower=102))
damage('pair partition repeats an original label', lambda c:c['pair_partition'][4].__setitem__(0,40))
damage('missing target case', lambda c:c['cases'].pop())
damage('duplicated target case', lambda c:c['cases'].__setitem__(-1,deepcopy(c['cases'][0])))
pair_index = next(i for i,r in enumerate(original['cases']) if r[2]=='pairs')


def corrupt_pair(c):
    row = c['cases'][pair_index]
    row[5] -= 1
    row[6][0] -= 1


damage('invented smaller actual pair capacity',corrupt_pair)
damage('incorrect literal demand',lambda c:c['cases'][pair_index].__setitem__(4,441))


def nonstrict_singleton(c):
    row = c['cases'][pair_index]
    a,b = row[:2]
    U = sum(1<<x for x in range(720) if x%18==a or x%8==b)
    R = check.FULL & ~(check.FIXED|U)
    caps,_ = check.capacities(R,[[m] for m in check.FREE])
    check.require(sum(caps)==row[4], 'control no longer tests a nonstrict capacity')
    row[2],row[5],row[6] = 'singleton',sum(caps),caps


damage('equality falsely declared exclusion',nonstrict_singleton)
rejected = []
for name,c in damages:
    failures = []
    for label,replay in (('bitsets',check.replay),('physical_sets',audit.replay)):
        try:
            replay(c)
        except RuntimeError:
            failures.append(label)
    check.require(failures == ['bitsets','physical_sets'], 'semantic damage accepted: '+name)
    rejected.append(name)
print(json.dumps({'agent':'six-covering-1','role':'researcher','status':'CONTROLS_PASSED',
                  'undamaged_complete_evidence_passed':True,'semantic_damages_rejected':rejected,
                  'production_and_independent_audit_rejected_each':True,'assert_statements_used':False}))
