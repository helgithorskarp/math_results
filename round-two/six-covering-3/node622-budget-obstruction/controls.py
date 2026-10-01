"""Reject invalid resources, loads, modes, identity and false domination."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from check import check


def main():
    directory=Path(__file__).resolve().parent
    raw=(directory/'certificate.json').read_bytes();data=json.loads(raw)
    expected=json.loads((directory/'expected.json').read_text())
    if check(data)!=expected:raise ValueError('Expected exact record mismatch')
    tests=[]
    bad=deepcopy(data);bad['fixture']['available_moduli'].pop();tests.append(('incomplete resources',bad))
    bad=deepcopy(data);bad['mixtures'][0]['entries'][0]['numerator']+=1;tests.append(('wrong rational load',bad))
    bad=deepcopy(data);bad['mixtures'][0]['periodic_mode']='individual_sum';tests.append(('wrong periodic union rule',bad))
    bad=deepcopy(data);bad['mixtures'][-1]['entries'][0]['phases'][0][0]=5;tests.append(('wrong TOP resource identity',bad))
    bad=deepcopy(data)
    for group in bad['mixtures']:
        phases=[[d,0,0] for d in (1,5,7,35)] if group['kind']=='top_union' else [0]*len(group['resources'])
        group['entries']=[{'numerator':bad['denominator'],'phases':phases}]
    tests.append(('legal phases with false domination',bad))
    rejected=[]
    for name,fixture in tests:
        try:check(fixture)
        except ValueError as e:rejected.append({'case':name,'reason':str(e)})
        else:raise ValueError('Corrupted evidence accepted: '+name)
    print(json.dumps({'agent':'six-covering-3','role':'researcher','rejected':rejected,
        'certificate_sha256':hashlib.sha256(raw).hexdigest(),'expected_record_matched':True},sort_keys=True))


if __name__=='__main__':main()
