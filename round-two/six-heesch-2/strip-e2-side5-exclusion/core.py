"""All-k raw/sealed-cell/top-endpoint reductions, plus an exact E1 cap tree.

The lower endpoint is not settled here. No full E2 inclusion or Heesch bound.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

H=Path(__file__).resolve().parent
import deps
import conditional_collars as C
import reader as V
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_contact_rectangles import systems,selected_rectangles,order_atoms
from strip_point_suppliers import finite_suppliers,IDENTITY

Q=((2,-3,1,-1),(0,-1),(0,0))
A=((2,-3,1,-1),(0,-2),(0,1))
B=((-1,0,0,-1),(0,-3),(1,1))
P=(((0,-2),(0,1)),((0,-2),(0,2)),((-3,-1),(-1,1)))
ENTRY={'name':'side5_angle_Q','pose':Q,'points':P}
C.PLANS={'side5_angle_Q':{'root_point':P[0],
                         'leaves':((A,P[2]),(B,P[1]))}}
TOP=((1,0,0,1),(0,5),(1,2))
TOP_POINT=((0,4),(1,2))
FORCED=((2,-3,1,-1),(0,4),(1,2))


def wedge_nonnegative(row):
    """Exact minimum of Ak+Bb+C on k>=6,3<=b<=k+1."""
    a,b,c=row
    if b>=0:tail=a;at_six=6*a+3*b+c;edge='b=3'
    else:tail=a+b;at_six=6*(a+b)+b+c;edge='b=k+1'
    if tail<0 or at_six<0:raise ValueError('False all-k wedge inequality')
    return {'row':row,'minimum_edge':edge,'tail_slope':tail,'at_six':at_six}


def check_sealed_cell():
    # Root cells (3,b),(2,b-1),(3,b-1); translated cells
    # (5,b),(6,b+1),(5,b+1). These are all six UV neighbors of(4,b).
    rows=((0,1,-2),(1,-1,1),(0,1,-3),(1,-1,2),
          (1,0,0),(1,0,-1),(1,0,-1),(1,0,-6))
    evidence=[wedge_nonnegative(r) for r in rows]
    offsets=((-1,0),(-2,-1),(-1,-1),(1,0),(2,1),(1,1))
    if set(offsets)!=set(G.UV_DIRS):raise ValueError('Missing hex-neighbor direction')
    # P has u=4, absent from root; P-TOP_b has(-1,0), while source
    # column-1 has height k. The last inequality above gives k>=6.
    return {'domain':'k>=6,3<=b<=k+1','empty_cell':'(4,b)',
            'all_six_neighbor_offsets':offsets,'inequalities':evidence,
            'ordinary_bridge':'A connected registered polyhex with area>1 '
                'contains a neighboring cell at every prototype cell. All six '
                'neighbors of the demand are already occupied, so no copy '
                'covering it can pack.'}


def check_Q(record,guard):
    if R.freeze(record['fixed'])!=(IDENTITY,Q) or R.freeze(record['points'])!=P:
        raise ValueError('Wrong literal Q pair or collar')
    if R.freeze(record['root_point'])!=P[0]:raise ValueError('Wrong cap root')
    return V.check(record,guard)


def main():
    (H/'generated').mkdir(exist_ok=True)
    start=time.monotonic();operations=[0]
    def guard():
        operations[0]+=1
        if deps.paused() or time.monotonic()-start>=43 or operations[0]>100000:
            raise RuntimeError('Operational/time/work guard; unfinished is inconclusive')
    def alarm(a,b):raise RuntimeError('45s signal guard; unfinished is inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    s=next(x for x in systems() if x['matrix']==IDENTITY[0] and x.get('a')==5)
    raw_part=G.partition(order_atoms([s]))
    expected=(((-1,2),(-1,3)),((0,3),(0,4)),((0,4),(1,3)))
    for interval in raw_part['intervals']:
        if R.freeze(selected_rectangles(s,interval['representatives'][0]))!=expected:
            raise ValueError('Wrong complete raw U5 intervals')
    if raw_part['cuts']!=[6]:raise ValueError('Unexpected raw domain class')
    raw={'system':s,'partition':raw_part,'selected':expected,
         'normalized_union':'b=2-k or 3<=b<=k+2'}
    sealed=check_sealed_cell()
    guard();record=C.build(ENTRY,guard);qcheck=check_Q(record,guard)
    guard();top=finite_suppliers(TOP_POINT,(IDENTITY,TOP))
    independent=R.supplier_atlas(TOP_POINT,(IDENTITY,TOP),guard)
    if R.freeze(top)!=R.freeze(independent):raise ValueError('Top supplier sweeps differ')
    if not top['finite'] or R.freeze(top['atlas'])!=(FORCED,):
        raise ValueError('Top endpoint has another possible supplier')
    predicates=[G.neg(G.point_membership(f,TOP_POINT)) for f in (IDENTITY,TOP)]
    predicates.append(G.either(*(G.point_membership(f,
        (G.sub(TOP_POINT[0],(0,u)),G.sub(TOP_POINT[1],(0,v))))
        for f in (IDENTITY,TOP) for u,v in G.UV_DIRS)))
    predicates.extend((G.touching(G.relative(TOP,FORCED)),
                       G.neg(G.intersection(TOP))))
    part=G.partition(predicates)
    if part!=R.splitter(predicates):raise ValueError('Top membership partitions differ')
    if not all(all(G.evaluate(p,k) for p in predicates) for k in part['representatives']):
        raise ValueError('Top point is not always an original pair-halo demand')
    if G.relative(TOP,FORCED)!=Q:raise ValueError('Wrong forced E1 contact')
    controls=[]
    for label in ['missing_root_supplier','wrong_leaf_point','nonempty_leaf_atlas','wrong_fixed_pair']:
        bad=deepcopy(record)
        if label=='missing_root_supplier':bad['root_suppliers']['atlas'].pop()
        elif label=='wrong_leaf_point':bad['leaves'][0]['point']=((0,50),(0,50))
        elif label=='nonempty_leaf_atlas':bad['leaves'][0]['suppliers']['atlas'].append(IDENTITY)
        else:bad['fixed']=(IDENTITY,TOP)
        try:check_Q(bad,guard)
        except (ValueError,TypeError):controls.append(label)
        else:raise ValueError('Damaged Q certificate accepted')
    try:wedge_nonnegative((0,1,-4))
    except ValueError:controls.append('false_wedge_minimum')
    else:raise ValueError('False wedge certificate accepted')
    math={'raw':raw,'sealed_cell':sealed,'Q_E1_cap_tree':record,
          'Q_reader':qcheck,'top_forced_supplier':top,'top_demand_partition':part,
          'top_forced_relative':Q,'damaged_controls':controls,
          'uniform_conclusions':['Raw U5: b=2-k or 3<=b<=k+2',
              '3<=b<=k+1 implies(I;5,b) outside E1',
              '(2,-3,1,-1;-1,0) outside E1',
              '(I;5,k+2) outside E2',
              'E2 identity-U5 implies b=2-k'],
          'scope':'Every integer k>=6; registered local tests only. This component '
              'handles raw/middle/upper contacts; the collar component excludes '
              'the lower endpoint. No full E2 inclusion or Heesch conclusion.'}
    mode='normal' if __debug__ else 'optimized'
    result={'agent':'six-heesch-2','role':'researcher','complete':True,
        'evidence':math,'mathematics_sha256':R.sha(math),
        'seconds':round(time.monotonic()-start,3),
        'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'guard_calls':operations[0],
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated'/f'core-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'agent':'six-heesch-2','role':'researcher',
        'complete':True,'mathematics_sha256':result['mathematics_sha256'],
        'Q_root_suppliers':len(record['root_suppliers']['atlas']),
        'Q_leaves':len(record['leaves']),'damaged_controls':controls,
        'top_supplier':FORCED,'raw_partition':raw_part['cuts'],
        'scope':math['scope'],'seconds':result['seconds'],
        'max_rss_kib':result['max_rss_kib']},sort_keys=True),flush=True)
    signal.alarm(0)


if __name__=='__main__':main()
