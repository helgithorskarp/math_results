"""Search-free replay of supplier trees, with separate material geometry."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import signal
import sys
import time

H=Path(__file__).absolute().parent
import deps
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import IDENTITY


def universal(rows, guard):
    a=G.partition(rows);b=R.splitter(rows)
    require(a==b,'Parameter partition disagreement')
    for k in b['representatives']:
        guard();require(all(G.evaluate(row,k) for row in rows),'Uniform geometric assertion fails')
    return b


def in_halo(point, fixed):
    occupied=G.either(*(G.point_membership(f,point) for f in fixed))
    adjacent=G.either(*(G.point_membership(f,(G.sub(point[0],G.constant(u)),G.sub(point[1],G.constant(v))))
                       for f in fixed for u,v in G.UV_DIRS))
    return G.both(G.neg(occupied),adjacent)


def material(point, fixed, saved, guard):
    point=R.freeze(point);fixed=R.freeze(fixed)
    for cls in saved['classes']:
        for k in cls['representatives']:
            guard();tile=R.literal(k)
            occupied=set().union(*(set(R.E.affine(tile,R.axial(f,k))) for f in fixed))
            pu,pv=G.value(point[0],k),G.value(point[1],k);p=(pu-2*pv,pv)
            rebuilt=set()
            for m in R.E.matrices():
                for u,v in R.E.affine(tile,m+(0,0)):
                    pose=m+(p[0]-u,p[1]-v)
                    if occupied.isdisjoint(R.E.affine(tile,pose)):rebuilt.add(pose)
            expected={R.axial(R.freeze(g),k) for g in cls['atlas']}
            require(rebuilt==expected,'Separate material point-alignment inventory differs')


def check(record, guard, materialize=True):
    fixed=R.freeze(record['fixed']);points=R.freeze(record['points'])
    require(len(fixed)==2 and fixed[0]==IDENTITY,'Wrong fixed root pair')
    rootpoint=R.freeze(record['root_point'])
    require(rootpoint in points,'Cap is not a named original demand')
    rows=[G.neg(G.intersection(G.relative(fixed[0],fixed[1]))),
          G.touching(G.relative(fixed[0],fixed[1])),
          *[in_halo(p,fixed) for p in points]]
    geometry=universal(rows,guard)
    root=R.supplier_atlas(rootpoint,fixed,guard)
    require(R.freeze(root)==R.freeze(record['root_suppliers']),'Changed complete cap supplier reduction')
    candidates=[R.freeze(x['candidate']) for x in record['leaves']]
    require(len(set(candidates))==len(candidates) and set(candidates)==set(root['atlas']),
            'Missing or duplicate exhaustive cap branch')
    if materialize:material(rootpoint,fixed,root,guard)
    cuts=set(root['partition']['cuts'])|set(geometry['cuts'])
    for leaf in record['leaves']:
        guard();candidate=R.freeze(leaf['candidate']);point=R.freeze(leaf['point'])
        require(point in points,'Leaf is not a named original demand')
        # It remains demanded in the ORIGINAL pair halo, and the selected
        # cap copy does not fill it. No new halo obligations are introduced.
        extra=universal([G.neg(G.point_membership(candidate,point))],guard)
        fs=(*fixed,candidate);fresh=R.supplier_atlas(point,fs,guard)
        require(R.freeze(fresh)==R.freeze(leaf['suppliers']),'Changed conditional supplier reduction')
        require(not fresh['atlas'],'Leaf has an admissible supplier')
        if materialize:material(point,fs,fresh,guard)
        cuts.update(extra['cuts']);cuts.update(fresh['partition']['cuts'])
    require(record['complete'],'Not a complete supplier tree')
    return {'case':record['case'],'tree_nodes':1+len(candidates),
            'cap_suppliers':len(candidates),'cuts':sorted(cuts),'record_sha256':R.sha(record)}


def reduction(guard):
    I=IDENTITY;g=((1,0,0,1),(0,6),(-1,4));r=((-1,0,0,-1),(0,5),(0,3))
    fixed=(I,g,r);point=((0,4),(0,4))
    universe=universal([in_halo(point,fixed),
                       G.point_membership(I,((0,3),(0,4))),
                       G.point_membership(g,((0,5),(0,4))),
                       *[G.neg(G.intersection(G.relative(a,b))) for j,b in enumerate(fixed) for a in fixed[:j]]],guard)
    b=R.supplier_atlas(point,fixed,guard)
    material(point,fixed,b,guard)
    pose_to_case={
        ((-2,3,-1,1),(0,4),(0,5)):('angle2_short_at_shift',g),
        ((-2,3,-1,2),(0,4),(0,4)):('angle2_const',I),
        ((-1,3,-1,2),(0,4),(0,4)):('angle1_const',I),
        ((-1,3,0,1),(0,4),(0,4)):('reflection_at_shift',g),
        ((1,-3,1,-2),(3,5),(2,5)):('angle1_long',I),
        ((1,0,0,1),(0,4),(0,4)):('side4',I),
    }
    expected_survivors={((-1,0,-1,1),(0,7),(0,5)),((2,-3,1,-2),(3,6),(2,5))}
    require(set(b['atlas'])==set(pose_to_case)|expected_survivors,'Point44 eight-pose classification changed')
    inputs=json.loads((H/'inputs.json').read_text())['cases']
    named={x['name']:R.freeze(x['pose']) for x in inputs}
    mappings=[]
    for pose,(name,anchor) in pose_to_case.items():
        require(G.relative(anchor,pose)==named[name],'Wrong E1-relative exclusion transport')
        part=universal([G.touching(G.relative(anchor,pose)),G.neg(G.intersection(G.relative(anchor,pose)))],guard)
        mappings.append({'supplier':pose,'anchor':anchor,'E1_exclusion':name,'partition':part})
    return {'fixed':fixed,'point':point,'complete_supplier_record':b,'mappings':mappings,
            'survivors':sorted(expected_survivors),'parameter_partition':universe,
            'scope':'Assuming the published9404 forced half-turn, every E2 halo cover of g has one of these two point44 suppliers'}


def main():
    start=time.monotonic()
    def guard():
        if deps.paused() or time.monotonic()-start>=43:
            raise RuntimeError('Operational/time guard; unfinished reader inconclusive')
    def alarm(a,b):raise RuntimeError('45s signal guard; unfinished reader inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    normal=H/'generated/conditional';finite=H/'generated/finite'
    inputs={e['name']:e for e in json.loads((H/'inputs.json').read_text())['cases']}
    def bind(record,name):
        require(record['case']==name and R.freeze(record['fixed'])==(IDENTITY,R.freeze(inputs[name]['pose']))
                and R.freeze(record['points'])==R.freeze(inputs[name]['points']), 'Certificate differs from named literal case')
    mode='normal' if __debug__ else 'optimized';evidence=[];damages=[]
    for name in ('side4','angle2_short_at_shift','reflection_at_shift'):
        record=json.loads((finite/f'{name}-normal.json').read_text())
        bind(record,name)
        fixed=R.freeze(record['fixed'])
        universal([G.neg(G.intersection(G.relative(*fixed))),G.touching(G.relative(*fixed))],guard)
        entry=R.local_check(record,guard);entry['case']=name;evidence.append(entry)
        for label in ('missing_supplier','missing_DAG_branch','altered_conflict'):
            damaged=deepcopy(record)
            if label=='missing_supplier':damaged['supplier_records'][0]['atlas'].pop()
            elif label=='missing_DAG_branch':damaged['proof']['nodes'].pop()
            else:damaged['universal']['conflicts'][0]^=1
            try:R.local_check(damaged,guard,False)
            except ValueError:damages.append([name,label])
            else:raise ValueError('Damaged finite certificate accepted')
    for name in ('angle1_long','angle2_const','angle1_const'):
        record=json.loads((normal/f'{name}-normal.json').read_text())
        bind(record,name)
        evidence.append(check(record,guard))
        for label in ('missing_cap_branch','changed_leaf_point','false_empty_supplier'):
            damaged=deepcopy(record)
            if label=='missing_cap_branch':damaged['leaves'].pop()
            elif label=='changed_leaf_point':damaged['leaves'][0]['point']=damaged['root_point']
            else:damaged['leaves'][0]['suppliers']['atlas'].append(damaged['leaves'][0]['candidate'])
            try:check(damaged,guard,False)
            except ValueError:damages.append([name,label])
            else:raise ValueError('Damaged conditional certificate accepted')
    necessary=reduction(guard)
    signal.alarm(0)
    math={'exclusions':evidence,'two_branch_reduction':necessary,'damaged_controls':damages,
          'trust_boundary':'Shared affine and height systems; separate endpoint sweeps and material point-alignment; author proof unformalized and independently unreviewed'}
    out={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':math,
         'mathematics_sha256':R.sha(math),'seconds':round(time.monotonic()-start,3),
         'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/f'generated/verified-{mode}.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='evidence'}),flush=True)
    print(json.dumps({'exclusions':evidence,'survivors':necessary['survivors'],'damaged_controls':len(damages)}),flush=True)


if __name__=='__main__':main()
