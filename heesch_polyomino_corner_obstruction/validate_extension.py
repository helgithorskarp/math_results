"""Check the different-root compiler before any mathematical SAT claim."""
import json
import hashlib
from pathlib import Path
import time

from extension import ROOT,inventory,independent_inventory,build_formula,load_dependencies,scale_cells


def main():
    start=time.monotonic()
    cover,motion=load_dependencies(ROOT/'heesch_polyomino_euler_cnf',
                                   ROOT/'heesch_polyomino_motion_bridge')
    from pysat.solvers import Solver
    equal=[]
    for tile in (((0,0),),((0,0),(1,0)),((0,0),(1,0),(0,1)),
                 scale_cells(((0,0),)),scale_cells(((0,0),(1,0),(0,1)))):
        c,halo,owners,stats=inventory(tile,tile,cover,motion)
        new=build_formula(c,halo,owners)
        old,prior,expected=cover.build_cover(tile,1)
        if (new.nv!=old.nv or new.clauses!=old.clauses
                or [q['cells'] for q in c]!=[q['cells'] for q in prior]):
            raise RuntimeError('same-root formula differs from pinned proven compiler')
        equal.append({'cells':len(tile),'candidates':len(c),'variables':new.nv,'clauses':len(new.clauses)})
    projected=[]
    for root in (((0,0),),((0,0),(1,0)),((-2,3),(-1,3)),((0,0),(1,0),(0,1))):
        tile=((0,0),)
        candidates,halo,owners,stats=inventory(root,tile,cover,motion)
        other_halo,other_candidates=independent_inventory(root,tile,motion)
        if halo!=other_halo or {(q['shape'],q['tx'],q['ty']) for q in candidates}!=other_candidates:
            raise RuntimeError('independent inventory mismatch')
        circuit=build_formula(candidates,halo,owners)
        count=0
        with Solver(name='glucose4',bootstrap_with=circuit.clauses) as solver:
            for mask in range(1<<len(candidates)):
                chosen=[q for i,q in enumerate(candidates) if mask>>i&1]
                assumptions=[q['variable'] if mask>>i&1 else -q['variable'] for i,q in enumerate(candidates)]
                footprints=[set(q['cells']) for q in chosen]
                covered=set().union(*footprints) if footprints else set()
                direct=(halo<=covered and all(not a&b for i,a in enumerate(footprints) for b in footprints[i+1:]))
                if solver.solve(assumptions=assumptions)!=direct:
                    raise RuntimeError('primary CNF projection disagrees with direct geometry')
                count+=direct
        projected.append({'root_cells':len(root),'root':root,'candidates':len(candidates),
                          'complete_primary_subsets':1<<len(candidates),'positive_subsets':count})
    result={'agent':'six-heesch-1','role':'researcher','same_root_exact_formula_agreement':equal,
            'different_root_complete_projection':projected,'seconds':round(time.monotonic()-start,3)}
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
