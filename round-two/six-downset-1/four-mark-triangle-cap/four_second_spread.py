"""All original inverse, real-line controls and symmetry positions for N76."""
from pathlib import Path
import json, signal, time, resource
from four_spread import verify_data, require, alarm

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, alarm); signal.alarm(60)
    start = time.monotonic(); folder = Path(__file__).resolve().parent
    raw = json.loads((folder/'FOUR-MARK-SECOND-MATRIX.json').read_text())
    sector = json.loads((folder/'FOUR-MARK-SECOND-SECTOR.json').read_text())
    result = verify_data(raw, sector)
    packed = json.dumps(result, indent=2)+'\n'
    require(len(packed.encode()) <= 32*1024*1024, 'unchanged32MiB packing guard')
    (folder/'FOUR-MARK-SECOND-SPREAD-RESULT.json').write_text(packed)
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        optimized=not __debug__, one_mathematical_child=True, native_threads_one=True)
    signal.alarm(0); print(json.dumps(result), flush=True)
