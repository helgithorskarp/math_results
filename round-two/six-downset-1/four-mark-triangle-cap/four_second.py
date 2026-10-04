"""Second bounded ORIGINAL four-mark control, N76; fixed pre-construction guards.

Only the original constructor is imported. Native threads are fixed by it.
This literal control does not prove the uniform or real interval bridge.
"""
from pathlib import Path
import json, signal, time, resource
from four_mark import build, require, alarm

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, alarm); signal.alarm(60)
    start = time.monotonic(); folder = Path(__file__).resolve().parent
    result, defining = build(4, 4, 2)
    packed = json.dumps(defining, indent=2, default=str) + '\n'
    require(len(packed.encode()) <= 32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'FOUR-MARK-SECOND-MATRIX.json').write_text(packed)
    (folder/'FOUR-MARK-SECOND-RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__, one_mathematical_child=True, native_threads_one=True)
    signal.alarm(0); print(json.dumps(result), flush=True)
