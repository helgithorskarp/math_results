"""Reject damaged coverage, scope and strict-sign instructions."""
from pathlib import Path
from copy import deepcopy
import json
import replay
HERE=Path(__file__).resolve().parent
def run():
    data=json.loads((HERE/'PLAN-bad.json').read_text());damaged=[]
    x=deepcopy(data);x['trees'].pop();damaged.append(('missing orientation',x))
    x=deepcopy(data);x['box'][0]='577/1000';damaged.append(('unjustified narrower domain',x))
    x=deepcopy(data);x['trees'][0]['tree']='3';damaged.append(('target qualifier in wrong proof',x))
    x=deepcopy(data);code=replay.CODES[replay.WITNESSES.index(['pair',7,10])];x['trees'][0]['tree']=code;damaged.append(('non-strict witness on unsplit rectangle',x))
    rejected=[]
    for name,x in damaged:
        try:replay.replay(x)
        except (ValueError,ArithmeticError):rejected.append(name)
        else:raise ValueError('damaged proof was accepted: '+name)
    return {'all_four_controls_rejected':True,'controls':rejected}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True))
