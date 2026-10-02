"""Damaged facial inputs plus a mathematically harmless cyclic rotation."""
from pathlib import Path
from copy import deepcopy
import json
import audit

root=Path(__file__).resolve().parent
data=json.loads((root/'FACE_CHART.json').read_text())
reference=json.loads((root/'inputs/fourteen-certificate.json').read_text())
name='asymmetric'
cases=[]
x=deepcopy(data);x[name]['faces'].pop();cases.append(('missing-face',x,reference))
x=deepcopy(data);x[name]['faces'][0].reverse();cases.append(('reversed-physical-face',x,reference))
x=deepcopy(data);x[name]['faces'][0][1]=1;cases.append(('noncontact-side',x,reference))
x=deepcopy(data);x[name]['edges'].pop();cases.append(('omitted-actual-contact',x,reference))
x=deepcopy(data);x[name]['face_count']=16;cases.append(('false-Euler-face-count',x,reference))
x=deepcopy(data);x[name]['convexity'][0]['strictly_convex']=False;cases.append(('false-turn-record',x,reference))
x=deepcopy(data);x[name]['face_length_counts']={'3':9,'4':7,'5':1};cases.append(('incorrect-profile',x,reference))
r=deepcopy(reference);r['alternate_vector'][0][0]='-8/4';cases.append(('changed-alternative-coordinate',data,r))
rejected=[]
for label,x,r in cases:
    try:audit.verify(x,r)
    except ValueError:rejected.append(label)
    else:raise ValueError('damaged input unexpectedly accepted: '+label)
rot=deepcopy(data);face=rot[name]['faces'][0];shifted=face[1:]+face[:1]
rot[name]['faces'][0]=shifted
for row in rot[name]['convexity']:
    if row['cycle']==face:row['cycle']=shifted
audit.verify(rot,reference)
print(json.dumps({'rejected':rejected,'accepted_harmless_cyclic_face_rotation':True},sort_keys=True))
