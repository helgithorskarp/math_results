"""Independent physical split/input audit and additional admission controls."""
import argparse
from copy import deepcopy
import hashlib
from itertools import product
import json
from pathlib import Path

import gate


def verify(directory, original_positive, prepared, controls):
    p=Path(prepared);plan=json.loads((p/'PREPARED.json').read_text())
    edges={};variable=2
    for u in range(43):
        for v in range(u+1,43):
            if u<32 and u//4==v//4:continue
            edges[variable]=(u,v);variable+=1
    x,y=plan['selection']['variables']
    if x==y or not 2<=x<=801 or not 2<=y<=801 or 119 in (x,y) or set(edges[x])&set(edges[y]):
        raise ValueError('Independent split scope')
    if [list(edges[x]),list(edges[y])]!=plan['selection']['edges']:
        raise ValueError('Independent physical labels')
    root=Path(original_positive).read_bytes()
    if hashlib.sha256(root).hexdigest()!='326d54a4a9b2abb26c5865536c7bb42d20696c5a59c6c8e1a0d1477465f21c67':
        raise ValueError('Independent prepared positive root')
    _,body=root.split(b'\n',1)
    signatures=[];inputs=[]
    for i,leaf in enumerate(plan['leaves']):
        if leaf['index']!=i:raise ValueError('Join index order')
        job=leaf['job'];literals=job['edge_cube']
        if job['r']!=8 or job['core_assumptions']!=[-810,-819,-824,-832,-833,-836,-842,-856] or len(literals)!=3 or literals[0]!=119:
            raise ValueError('Independent complete cohort scope')
        if list(map(abs,literals[1:]))!=[x,y]:raise ValueError('Independent split coordinates')
        signs=tuple(v>0 for v in literals[1:]);signatures.append(signs)
        raw=(p/leaf['cnf']).read_bytes()
        expected=b'p cnf 946 1502532\n'+body+''.join(f'{v} 0\n' for v in literals[1:]).encode()
        if raw!=expected or hashlib.sha256(raw).hexdigest()!=leaf['sha256']:
            raise ValueError('Independent complete physical input bytes')
        if json.loads((p/f'leaf-{i}.job.json').read_text())!=job:
            raise ValueError('Disk job and manifest differ')
        inputs.append(dict(index=i,bytes=len(raw),sha256=leaf['sha256']))
    if signatures!=list(product((True,False),repeat=2)):
        raise ValueError('Four exhaustive leaves in complementary join order')
    for assignment in product((False,True),repeat=2):
        if signatures.count(assignment)!=1:raise ValueError('Independent disjoint cover')
    empty=json.loads((Path(controls)/'EMPTY_COVER_CONTROL.json').read_text())
    bad=deepcopy(empty['positive_refutation']);bad['core_assumptions']=gate.GUARD
    try:gate.mixed_cover(directory,empty['unit_theorem'],bad)
    except ValueError:pass
    else:raise ValueError('Empty-core control falsely transferred to the real cohort')
    bad_unit=deepcopy(empty['unit_theorem']);bad_unit['implied_unit']=118
    try:gate.mixed_cover(directory,bad_unit,empty['positive_refutation'])
    except ValueError:pass
    else:raise ValueError('Changed imported premise accepted')
    for rc,text in [(20,'c UNKNOWN'),(0,'s UNSATISFIABLE'),(10,'c UNKNOWN'),(0,'s SATISFIABLE')]:
        try:gate.classify(rc,text)
        except ValueError:pass
        else:raise ValueError('Malformed solver status accepted')
    return dict(status='PRE_TARGET_INDEPENDENT_AUDIT_PASSED',
        variables=[x,y],physical_edges=[list(edges[x]),list(edges[y])],
        full_inputs=inputs,exhaustive_assignments_checked=4,
        forged_nonempty_original_cover_rejected=True,changed_imported_premise_rejected=True,
        malformed_solver_statuses_rejected=4,actual_target_solver_calls=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory');p.add_argument('positive');p.add_argument('prepared');p.add_argument('controls')
    a=p.parse_args();result=verify(a.directory,a.positive,a.prepared,a.controls)
    gate.write_json(Path(a.prepared)/'AUDIT.json',result)
    print(json.dumps(result,indent=2))
