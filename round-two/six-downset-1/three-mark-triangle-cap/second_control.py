"""Second original carrier, not a larger exhaustive classification."""
from pathlib import Path
import json,signal,time,resource
from three_mark import build,alarm
from three_sector import control
from three_spread import verify_data
from exact import require

if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    folder=Path(__file__).resolve().parent
    seed,raw=build(4,3,2)
    encoded=json.dumps(raw,indent=2,default=str)+'\n'
    require(len(encoded.encode())<=32*1024*1024,'unchanged32MiB record guard')
    (folder/'THREE-MARK-SECOND-MATRIX.json').write_text(encoded)
    sec,sdata=control(folder,'THREE-MARK-SECOND-MATRIX.json')
    repair=verify_data(raw,sdata)
    result=dict(agent='six-downset-1',role='researcher',private=True,
        status='EXACT SECOND ORIGINAL CONTROL; ordinary infinite bridge separate; unformalized/unreviewed',
        seed=seed,sector=sec,repair=repair)
    (folder/'THREE-MARK-SECOND-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution']=dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__,
        one_mathematical_child=True,native_threads_one=True)
    signal.alarm(0);print(json.dumps(result),flush=True)
