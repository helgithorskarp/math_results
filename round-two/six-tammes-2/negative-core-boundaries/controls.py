"""Four damaged certificates must fail the independent arithmetic audit."""
from pathlib import Path
from copy import deepcopy
import json
from audit import verify,require
HERE=Path(__file__).resolve().parent
def check():
    baseline=json.loads((HERE/'certificate.json').read_text());verify(baseline)
    cases=[]
    c=deepcopy(baseline);c['critical']['resultants']['other']['P'][0]['n'][0]+=1
    cases.append(('wrong critical bordered-Gram coefficient',c))
    c=deepcopy(baseline);c['lower']['resultants']['other']['E'][0]['n'][0]+=1
    cases.append(('wrong lower common-neighbor coefficient',c))
    c=deepcopy(baseline)
    c['critical']['resultants']['other']['numerator_factors']['factors']=[
        row for row in c['critical']['resultants']['other']['numerator_factors']['factors']
        if row['coefficients']!=[-1,-3,2,6,-1,13]]
    cases.append(('omitted incumbent boundary factor',c))
    c=deepcopy(baseline)
    for row in c['lower']['resultants']['other']['numerator_factors']['factors']:
        if row['coefficients']==[-1,0,3]:row['coefficients']=[-1,0,5]
    cases.append(('wrong lower threshold polynomial',c))
    rejected=[]
    for label,c in cases:
        try:verify(c)
        except ValueError:rejected.append(label)
        else:raise ValueError('damaged certificate accepted: '+label)
    return {'status':'CONTROLS_PASSED','rejected':rejected,'count':len(rejected)}
if __name__=='__main__':print(json.dumps(check(),sort_keys=True))
