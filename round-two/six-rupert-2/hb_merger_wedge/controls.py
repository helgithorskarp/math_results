#!/usr/bin/env python3
"""Reject false mathematical premises before any expected-record/hash gate."""
from pathlib import Path
import copy,json
import check as c
g=c.g
data=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
cases=[]
def fixture(name,mutate=None,**kw):
    bad=copy.deepcopy(data)
    if mutate is not None:mutate(bad)
    cases.append((name,bad,kw))
fixture('wrong original HB label',lambda d:d['source_mapping'][0].__setitem__(1,13))
fixture('false full-solid Ax symmetry',claim_full_action=True)
improper=tuple(tuple(-v if j==0 else v for j,v in enumerate(row)) for row in c.HB)
fixture('improper original HB source',source_override=improper)
fixture('wrong original triangle negative',lambda d:d['positive_triangle_pairs'][0].__setitem__(1,10))
fixture('wrong original width negative',lambda d:d['width_pairs'][1].__setitem__(1,38))
fixture('changed genuine stress weight',lambda d:d['stress_contacts'][0].__setitem__('weight',['1','0']))
fixture('omitted actual receiving extreme point',lambda d:d['open_receiving_cycle'].remove(43))
fixture('unremoved merger degeneracy',lambda d:d.__setitem__('q_receiving_cycle',d['open_receiving_cycle'][:]))
fixture('wrong Cr instead of actual Jr',companion_factor=g.MX)
fixture('enlarged finite receiver wedge',lambda d:d.__setitem__('receiver_wedge_delta',['1/1000','0']))
rejections=[]
for name,bad,kw in cases:
    try:c.record(bad,**kw)
    except ValueError as error:rejections.append({'fixture':name,'semantic_rejection':str(error)})
    else:raise ValueError('false mathematical fixture accepted: '+name)
result={'agent':'six-rupert-2','role':'researcher','semantic_false_fixture_rejections':rejections,
        'uses_expected_or_hash_gate':False,'global_J74_status':'OPEN'}
print(json.dumps(result,indent=2))
