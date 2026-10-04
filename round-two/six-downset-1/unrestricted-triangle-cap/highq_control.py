"""Fresh physical high-q boundary control, actual carrier N62/parent N68."""
from pathlib import Path
import json,time,signal,resource
from sector_control_harmonic import control,alarm

if __name__=='__main__':
    signal.signal(signal.SIGALRM,alarm);signal.alarm(60);start=time.monotonic()
    record=control(5,3,2)
    p=Path(__file__).resolve().parent/'HIGHQ-ORIGINAL-CONTROL.json'
    raw=json.dumps(record,indent=2,default=str)+'\n'
    if len(raw.encode())>32*1024*1024:raise ValueError('unchanged32MiB record guard')
    p.write_text(raw);signal.alarm(0)
    print(json.dumps({k:v for k,v in record.items() if k not in ('basis','metric','frame','cap','residual_dual')}|
        dict(seconds=time.monotonic()-start,peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)),flush=True)
