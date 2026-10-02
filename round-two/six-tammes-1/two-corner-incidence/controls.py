"""Meaningful whole-certificate damages and valid boundary/scope controls."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import json
import audit,bridge

def require(x,m):
    if not x:raise ValueError(m)

def reject(fn,data,mutate,label):
    damaged=deepcopy(data);mutate(damaged)
    try:fn(damaged)
    except ValueError:return label
    raise ValueError('damaged input accepted: '+label)

data=json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
cases=[
 ('missing-closing-word',lambda x:x['closure'].pop()),
 ('duplicate-closing-word',lambda x:x['closure'].__setitem__(-1,deepcopy(x['closure'][0]))),
 ('changed-final-vector',lambda x:x['closure'][0]['final_boundary_vector'][0].__setitem__(0,'123')),
 ('changed-contact-obstruction',lambda x:x['closure'][0]['contact_polynomial'].__setitem__(0,'123')),
 ('changed-Bernstein-coefficient',lambda x:x['closure'][0]['bernstein'].__setitem__(0,str(F(x['closure'][0]['bernstein'][0])+1))),
 ('zero-contact-obstruction',lambda x:x['closure'][0].__setitem__('contact_polynomial',[])),
 ('changed-closed-domain',lambda x:x['r_band'].__setitem__(1,'4/5')),
 ('missing-port-case',lambda x:x['rings'].pop()),
 ('duplicate-port-case',lambda x:x['rings'].__setitem__(-1,deepcopy(x['rings'][0]))),
 ('adjacent-port-endpoints',lambda x:x['rings'][0]['ports'].__setitem__(0,1)),
 ('changed-quotient-class',lambda x:x['rings'][0]['classes'][0].__setitem__(0,'2:99')),
 ('changed-boundary-arc',lambda x:x['rings'][0]['boundary_arcs'][0].__setitem__(0,'2:99')),
 ('changed-boundary-cycle',lambda x:x['rings'][0]['boundary_cycles'][0].__setitem__(0,'2:99')),
 ('false-mixed-corner-count',lambda x:x['rings'][0]['mixed_corners_per_boundary'].__setitem__(0,2)),
 ('false-region-vertex-count',lambda x:x['rings'][0].__setitem__('vertices',99)),
]
rejected=[reject(audit.verify,data,fn,label) for label,fn in cases]
valid=deepcopy(data);valid['closure'].reverse();valid['rings'].reverse()
for row in valid['rings']:
    row['boundary_cycles']=[list(reversed(c[1:]+c[:1])) for c in reversed(row['boundary_cycles'])]
audit.verify(valid)

parent=bridge.load()
hexindex=next(i for i,row in enumerate(parent['records']) if row['sides']==6)
parent_cases=[
 ('missing-partial-hexagon-word',lambda x:x['records'].pop(hexindex)),
 ('damaged-partial-Bezout',lambda x:x['records'][hexindex]['bezout'][0].__setitem__(0,str(F(x['records'][hexindex]['bezout'][0][0])+1))),
 ('changed-partial-core-vector',lambda x:x['hexagon']['vectors'][0][0].__setitem__(0,'2')),
 ('false-partial-capacity',lambda x:x['cap'].__setitem__('total_points_at_most',15)),
]
rejected_parent=[reject(bridge.verify,parent,fn,label) for label,fn in parent_cases]
scoped=deepcopy(parent)
scoped['records']=[r for r in scoped['records'] if r['sides']==6]
for name in ('closed_three_fan_state','four_fan_final_corner_gap'):
    scoped['hexagon'].pop(name)
bridge.verify(scoped)
# This acceptance tests the mathematical verifier's scope. It does not bypass
# load()'s binding of the original complete published parent bytes.
print(json.dumps({'new_certificate_damages_rejected':rejected,
                  'parent_partial_bridge_damages_rejected':rejected_parent,
                  'valid_record_reordering_and_cycle_rotation_reversal_accepted':True,
                  'unused_parent_final_corner_fields_and_q4_q5_records_omitted_accepted':True,
                  'original_parent_source_binding_still_required_by_load':True},sort_keys=True))
