"""Exact finite supplier trees; no truncation of a growing height family."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

H = Path(__file__).absolute().parent
import deps
import strip_contact_reader as R
from strip_point_suppliers import finite_suppliers, IDENTITY

# Each cap supplier is an exhaustive branch, followed by a demanded cell
# having no supplier after that cap copy has been chosen.
PLANS = {
    'angle1_long': {
        'root_point': ((0,4),(0,6)),
        'leaves': (
            (((-2,3,-1,2),(0,4),(0,6)), ((0,6),(0,7))),
            (((1,-3,1,-2),(3,5),(2,7)), ((3,-2),(2,2))),
            (((1,0,0,1),(0,4),(0,6)), ((0,6),(0,7))),
        ),
    },
    'angle2_const': {
        'root_point': ((0,5),(0,6)),
        'leaves': (
            (((-2,3,-1,2),(0,5),(0,6)), ((3,4),(2,5))),
            (((1,0,0,1),(0,5),(0,6)), ((0,4),(1,1))),
            (((1,0,1,-1),(0,6),(1,7)), ((0,5),(1,2))),
        ),
    },
    'angle1_const': {
        'root_point': ((0,5),(0,5)),
        'leaves': (
            (((1,0,0,1),(0,5),(0,5)), ((0,4),(1,1))),
            (((1,0,1,-1),(0,6),(1,6)), ((0,5),(1,2))),
        ),
    },
}


def build(entry, guard):
    name = entry['name']; plan = PLANS[name]
    fixed = (IDENTITY, R.freeze(entry['pose']))
    point = plan['root_point']; guard()
    root = finite_suppliers(point, fixed)
    if not root['finite']:
        raise RuntimeError('Root supplier family grows; proof incomplete')
    leaves = []
    for candidate, demand in plan['leaves']:
        guard(); supplier = finite_suppliers(demand, (*fixed, candidate))
        if not supplier['finite'] or supplier['atlas']:
            raise RuntimeError('Leaf is not a complete empty supplier family')
        leaves.append({'candidate': candidate, 'point': demand, 'suppliers': supplier})
    if set(root['atlas']) != {c for c, p in plan['leaves']}:
        raise RuntimeError('Plan omits a cap supplier')
    return {'agent':'six-heesch-2', 'role':'researcher', 'case':name,
            'fixed':fixed, 'points':entry['points'], 'root_point':point,
            'root_suppliers':root, 'leaves':leaves, 'complete':True,
            'scope':'Only the registered E1 pair exclusion for all k>=6'}


def main():
    start=time.monotonic()
    def guard():
        if deps.paused() or time.monotonic()-start>=43:
            raise RuntimeError('Operational/time guard; unfinished proof inconclusive')
    def alarm(a,b):
        raise RuntimeError('45s signal guard; unfinished proof inconclusive')
    signal.signal(signal.SIGALRM,alarm); signal.alarm(45)
    entries=json.loads((H/'inputs.json').read_text())['cases']
    folder=H/'generated/conditional';folder.mkdir(parents=True,exist_ok=True)
    mode='normal' if __debug__ else 'optimized';rows=[]
    for entry in entries:
        if entry['name'] not in PLANS:continue
        d=build(entry,guard)
        (folder/f"{entry['name']}-{mode}.json").write_text(json.dumps(d,indent=2)+'\n')
        row={'case':entry['name'],'tree_nodes':1+len(d['leaves']),
             'root_suppliers':len(d['root_suppliers']['atlas']),
             'root_cuts':d['root_suppliers']['partition']['cuts'],
             'leaf_cuts':[x['suppliers']['partition']['cuts'] for x in d['leaves']],
             'record_sha256':R.sha(d)}
        rows.append(row);print(json.dumps(row),flush=True)
    signal.alarm(0)
    out={'agent':'six-heesch-2','role':'researcher','cases':rows,
         'mathematics_sha256':R.sha(rows),'seconds':round(time.monotonic()-start,3),
         'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'checked_utc':datetime.now(timezone.utc).isoformat()}
    (folder/f'summary-{mode}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
