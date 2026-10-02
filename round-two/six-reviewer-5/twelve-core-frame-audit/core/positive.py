"""A nonempty rational rectangle of actual twelve-point twenty-contact packings."""
import json
from fractions import Fraction as F
from frame import scalar_frame,all_points,dot,chart_gap,TESTS
from enclosure import Box,SCALE

t=Box(F(592999,1000000),F(593,1000))
z=Box(F(949999,1000000),F(950001,1000000))
a=scalar_frame(t,z);points=all_points(a,-1,1)
chart=chart_gap(t,z)
if chart.hi>=0 or a['g'].lo<=SCALE//2:raise ValueError('positive chart/Gram condition')
gaps=[]
for i,j in TESTS:
 gap=dot(points[i],points[j],t)-t
 if gap.hi>=0:raise ValueError('positive packing rectangle failed '+str((i,j)))
 gaps.append(dict(pair=[i,j],upper_gap=str(F(gap.hi,SCALE))))
print(json.dumps(dict(parameter_rectangle=['592999/1000000','593/1000','949999/1000000','950001/1000000'],
 branch=[-1,1],strict_intercluster_gaps=gaps,chart_upper=str(F(chart.hi,SCALE)),g_lower=str(F(a['g'].lo,SCALE)),
 actual_packing_bridge='Sealed symbolic identities give all twelve unit norms, twenty prescribed contacts and twelve strict internal noncontacts. These33 negative gaps plus the negative chart give every other packing comparison. Exactly20 contacts throughout; no extra point.'),sort_keys=True,indent=2))
