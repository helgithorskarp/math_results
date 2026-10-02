"""Reject four incorrect boundary/reference reconstructions and inexact input."""
import argparse
import json
from pathlib import Path
import signal
import time
import check
from arithmetic import E, require

def verify_controls():
    cases = [('wrong V orientation',dict(radical_orientation=1)),
             ('wrong U orientation',dict(u_orientation=-1)),
             ('shifted boundary parameter',dict(boundary_shift='1/1000')),
             ('damaged incumbent cross Gram',dict(reference_shift='1/1000'))]
    rejected = []
    for name,options in cases:
        try: check.verify(**options)
        except ValueError as exc: rejected.append(dict(case=name,reason=str(exc)))
        else: raise ValueError('damaged reconstruction accepted: '+name)
    for name,value in [('binary float coefficient',0.5),('zero divisor',0)]:
        try:
            if name=='zero divisor': E(value).inverse()
            else: E(value)
        except ValueError as exc: rejected.append(dict(case=name,reason=str(exc)))
        else: raise ValueError('invalid arithmetic input accepted: '+name)
    require(len(rejected)==6, 'all damaged/invalid cases actually rejected')
    return dict(status='CHECKED_SIX_DAMAGED_OR_INVALID_REJECTIONS',
                agent='six-tammes-2',role='researcher',rejections=rejected,
                independent_researcher_review=False)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt',type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(
        TimeoutError('160-second control guard: incomplete evidence')))
    signal.alarm(160)
    try: result = verify_controls()
    finally: signal.alarm(0)
    result['seconds'] = round(time.monotonic()-started,3)
    if args.receipt: args.receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
