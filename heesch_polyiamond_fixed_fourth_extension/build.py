"""Complete integer fifth-surround inventory, full overlaps and interior cuts."""
from collections import defaultdict
import json
from common import g,PRIOR,compact,masks,star,footprint


def inventory():
    shape,fixture=g.inputs();fixed=[p for p in fixture if p['level']<=4]
    occupied=set()
    for p in fixed:
        f=footprint(shape,p)
        assert len(f)==214 and occupied.isdisjoint(f);occupied.update(f)
    vm=masks(occupied);boundary={v:m for v,m in vm.items() if m!=63}
    assert all(sum(((m>>j)&1)!=((m>>((j+1)%6))&1) for j in range(6))==2
               for m in boundary.values())
    required=set()
    for v in boundary:required.update(star(v)-occupied)
    tried=set();good={};feet={}
    for matrix in g.matrices():
        rotation={'matrix':list(matrix),'translation':[0,0]}
        rotated=sorted(compact(g.move(t,rotation)) for t in shape)
        for k,x,y in sorted(required):
            for q,a,b in rotated:
                if k!=q:continue
                tx,ty=x-a,y-b;key=(matrix,(tx,ty))
                if key in tried:continue
                tried.add(key)
                if any((r,u+tx,v+ty) in occupied for r,u,v in rotated):continue
                f=frozenset((r,u+tx,v+ty) for r,u,v in rotated)
                assert len(f)==214 and occupied.isdisjoint(f)
                good[key]={'matrix':list(matrix),'translation':[tx,ty]};feet[key]=f
                assert len(good)<=10000,'inventory guard: incomplete, no exclusion'
    keys=sorted(good);poses=[good[k] for k in keys];fs=[feet[k] for k in keys]
    required=sorted(required);owners={t:[] for t in required}
    for j,f in enumerate(fs,1):
        for t in f & owners.keys():owners[t].append(j)
    expected=json.loads((PRIOR/'expected.json').read_text())
    raw=g.catalogues(shape)[3]
    negatives=[raw[r['attachment']-1] for r in expected['pair_negatives']]
    lookup={g.key(p):i for i,p in enumerate(poses,1)}
    fixed_lookup={g.key(p) for p in fixed}
    pruned=set();pairs=set()
    for p in fixed:
        for q in negatives:
            assert g.key(g.compose(p,q)) not in fixed_lookup,'fixed forbidden pair'
            for r in (q,g.inverse(q)):
                j=lookup.get(g.key(g.compose(p,r)))
                if j is not None:pruned.add(j)
    for i,p in enumerate(poses,1):
        for q in negatives:
            j=lookup.get(g.key(g.compose(p,q)))
            if j is not None:
                assert i!=j;pairs.add(tuple(sorted((i,j))))
    report={'fixed_copies':len(fixed),'fixed_cells':len(occupied),
            'boundary_vertices':len(boundary),'required_cells':len(required),
            'anchored_trials':len(tried),'candidates':len(poses),
            'fixed_pair_pruned':len(pruned),'candidate_pair_exclusions':len(pairs)}
    return fixed,poses,fs,owners,pruned,pairs,report


def formula(fs,owners,pruned,pairs):
    clauses=[owners[t] for t in sorted(owners)]
    clauses += [[-j] for j in sorted(pruned)]
    conflicts=set(pairs);cellowners=defaultdict(list)
    for j,f in enumerate(fs,1):
        for t in f:
            for i in cellowners[t]:conflicts.add((i,j))
            cellowners[t].append(j)
    clauses += [[-i,-j] for i,j in sorted(conflicts)]
    return clauses,len(conflicts)


def instances(pattern,fixed,candidates):
    lookup={g.key(p):(0 if j<len(fixed) else j-len(fixed)+1)
            for j,p in enumerate(fixed+candidates)}
    out=set()
    for anchor in fixed+candidates:
        matched=[]
        for relative in pattern['poses']:
            j=lookup.get(g.key(g.compose(anchor,relative)))
            if j is None:break
            matched.append(j)
        else:
            clause=tuple(-j for j in sorted(set(matched)-{0}))
            assert clause,'fixed prefix contains impossible pattern'
            out.add(clause)
    return sorted(out)
