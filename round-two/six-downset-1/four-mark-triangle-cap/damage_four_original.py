"""Semantic original/empty/dual defects of FOUR-mark data, no producer import.

Credited defect algorithms from public source4dd74e66/damage_three_original.
Each independently checked four-mark original lift includes all light groups.
"""
from pathlib import Path
from fractions import Fraction as F
import json, copy, time, resource, signal
from four_spread import verify_data

def cases(raw, sector):
    out = []
    def test(label, mutation):
        r, s = copy.deepcopy(raw), copy.deepcopy(sector)
        mutation(r,s)
        try: verify_data(r,s)
        except ValueError as error:
            out.append(dict(name=label,rejected=True,reason=str(error))); return
        raise ValueError('mathematical original defect accepted: '+label)
    def empty(r,s): r['all_physical_rows'][0][0] = str(F(r['all_physical_rows'][0][0])+1)
    def omit(r,s): r['physical_metric'].pop()
    def matrix(r,s): r['original_M'][1][1] = '1'
    def family(r,s): r['family'][-1] |= 1
    def dual(r,s): s['residual_dual'][0] = str(F(s['residual_dual'][0])+1)
    def energy(r,s): s['kappa'] = str(F(s['kappa'])+1)
    for label, mutation in (
        ('change ACTUAL empty physical row',empty),
        ('omit a full physical metric direction',omit),
        ('make an intersecting original diagonal nonzero',matrix),
        ('change fourth-group private full set into a heavy marked set',family),
        ('change one full residual-dual coordinate',dual),
        ('change the original inverse/dual energy',energy)):
        test(label,mutation)
    return out

if __name__ == '__main__':
    def alarm(a,b): raise TimeoutError('unchanged60s data-damage guard')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(60)
    start = time.monotonic(); folder = Path(__file__).resolve().parent
    raw = json.loads((folder/'FOUR-MARK-FIRST-MATRIX.json').read_text())
    sector = json.loads((folder/'FOUR-MARK-FIRST-SECTOR.json').read_text())
    result = dict(agent='six-downset-1',role='researcher',private=True,
                  all_rejected=True,cases=cases(raw,sector))
    (folder/'FOUR-ORIGINAL-DAMAGES.json').write_text(json.dumps(result,indent=2)+'\n')
    result['execution'] = dict(seconds=time.monotonic()-start,
        peak_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,optimized=not __debug__)
    signal.alarm(0); print(json.dumps(result),flush=True)
