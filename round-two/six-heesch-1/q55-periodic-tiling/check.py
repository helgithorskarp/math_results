"""Exact finite checks supporting the all-depth periodic-tiling proof.

No SAT solver or producer import. Corona shells are rebuilt by graph BFS,
while the producer enumerates hexagonal norm shells. All area and topology
checks use integer unit-cell coordinates and the standard library.
"""
from copy import deepcopy
from itertools import product
import json
from pathlib import Path
import geometry as g

HERE=Path(__file__).resolve().parent
N={(-1,0),(1,0),(0,-1),(0,1),(-1,1),(1,-1)}


def check(data,fixture):
    listed=data['cells']
    g.require(listed and all(len(q)==2 and all(type(z) is int for z in q) for q in listed),
        'invalid prototype coordinates')
    raw=set(map(tuple,listed))
    g.require(len(raw)==len(listed)==55 and g.norm(raw)==tuple(map(tuple,listed)) and
        g.disc(raw), 'invalid normalized55-cell disc')
    g.require((max(x for x,y in raw),max(y for x,y in raw))==(10,9), 'prototype extents differ')
    g.require(data['periods']==[11,10] and data['representative_maps']==
        [[[1,0,0,1],[0,0]],[[-1,0,0,1],[16,5]]], 'literal period or affine maps differ')
    residues={}
    for i,((a,b,c,d),(sx,sy)) in enumerate(data['representative_maps']):
        for x,y in sorted(raw):
            point=a*x+b*y+sx,c*x+d*y+sy
            key=point[0]%11,point[1]%10
            g.require(key not in residues, 'overlapping residues in the periodic plane packing')
            residues[key]=(i,point)
    g.require(set(residues)==set(product(range(11),range(10))), 'uncovered period residue')

    def owner(point):
        i,(x,y)=residues[point[0]%11,point[1]%10]
        a,b=(point[0]-x)//11,(point[1]-y)//10
        return a-b,2*b+i

    def tile(u,v):
        tx=11*u+11*(v//2)+6*(v%2)
        return {((10-x if v%2 else x)+tx,y+5*v) for x,y in raw}

    inventory=[]
    for parity in (0,1):
        base=tile(0,parity)
        bx0,bx1=min(x for x,y in base),max(x for x,y in base)
        by0,by1=min(y for x,y in base),max(y for x,y in base)
        # Complete bounds follow from the exact width10 and height9:
        # a touching copy's bounding box meets the expanded base box.
        v0=-(-(by0-10)//5);v1=(by1+1)//5
        contacts4=set();contacts8=set();candidates=0
        edge4={(x+dx,y+dy) for x,y in base for dx,dy in g.FOUR}-base
        edge8=g.halo(base)
        for v in range(v0,v1+1):
            shift=11*(v//2)+6*(v%2)
            u0=-(-(bx0-11-shift)//11);u1=(bx1+1-shift)//11
            for u in range(u0,u1+1):
                candidates+=1
                if (u,v)==(0,parity):continue
                other=tile(u,v)
                g.require(not other&base, 'periodic copy overlap')
                relative=u,v-parity
                if other&edge4:contacts4.add(relative)
                if other&edge8:contacts8.add(relative)
        g.require(contacts4==contacts8==N, 'complete edge/corner contact stencil differs')
        g.require(all(owner(q) in {(0,parity)}|{(u,v+parity) for u,v in N}
            for q in edge8), 'neighbor cell has an unlisted host')
        inventory.append(dict(parity=parity,bounded_candidate_hosts=candidates,
            edge_contacts=list(map(list,sorted(contacts4))),
            corner_contacts=list(map(list,sorted(contacts8)))))

    # Every vertex pattern is periodic. Test every subset of its owner
    # labels, proving that no union of tiling copies has a diagonal pinch.
    patterns=0
    for x,y in product(range(11),range(10)):
        labels=[owner(q) for q in ((x,y),(x-1,y),(x-1,y-1),(x,y-1))]
        unique=sorted(set(labels))
        for mask in range(1<<len(unique)):
            chosen={q for i,q in enumerate(unique) if mask>>i&1}
            flags=[q in chosen for q in labels]
            g.require(not (sum(flags)==2 and flags[0]==flags[2]), 'possible union pinch at a periodic vertex')
            patterns+=1

    shapes=g.images(raw)
    root=shapes.index(g.norm(raw));flip=shapes.index(g.norm([(-x,y) for x,y in raw]))
    expected=[];seen={(0,0)};frontier={(0,0)}
    for k in range(6):
        expected.append(sorted([[flip if v%2 else root,
            11*u+11*(v//2)+6*(v%2),5*v] for u,v in frontier]))
        next_frontier={(u+du,v+dv) for u,v in frontier for du,dv in N}-seen
        seen|=next_frontier;frontier=next_frontier
    g.require(fixture['cells']==listed and fixture['levels']==expected, 'BFS corona fixture differs')
    stats=g.verify_lower(fixture)
    g.require([row['copies'] for row in stats]==[1+3*k*(k+1) for k in range(6)],
        'literal corona counts differ')
    return dict(prototype_area=55,period_area=110,representative_copies=2,
        residues_exactly_once=110,plane_tiling=True,contact_inventory=inventory,
        periodic_vertex_patterns=110,owner_subsets_checked=patterns,
        any_tiling_subunion_has_no_diagonal_pinch=True,
        explicit_coronas=5,corona_sizes=[len(level) for level in expected],
        prefix_stats=stats,heesch_c='infinity',heesch_h='infinity',
        all_depth_argument='PROOF.md: triangular-lattice balls and their complements are connected; each stencil contact contains an edge. Their unit-cell unions are discs and consecutive shells completely surround predecessors.',
        finite_heesch_construction=False,independent_review=False,formalized=False)


def audited_check(data,fixture):
    result=check(data,fixture)
    controls=[]
    bad=deepcopy(data);bad['cells'].pop()
    controls.append(('absent prototype cell',bad,fixture))
    bad=deepcopy(data);bad['periods'][0]+=1
    controls.append(('incorrect period',bad,fixture))
    bad=deepcopy(data);bad['representative_maps'][1][1][0]+=1
    controls.append(('incorrect representative translation',bad,fixture))
    bad=deepcopy(data);bad['representative_maps'][1][0][0]=1
    controls.append(('incorrect reflection',bad,fixture))
    bad=deepcopy(fixture);bad['levels'][-1].pop()
    controls.append(('absent fifth-corona member',data,bad))
    bad=deepcopy(fixture);bad['levels'][1][0][1]+=1
    controls.append(('moved first-corona member',data,bad))
    rejected=[]
    for name,bad_data,bad_fixture in controls:
        try:check(bad_data,bad_fixture)
        except ValueError as exc:rejected.append(dict(control=name,rejected=True,reason=str(exc)))
        else:raise ValueError('damaged tiling/corona input accepted: '+name)
    result['damage_controls']=rejected
    return result


def main():
    data=json.loads((HERE/'input.json').read_text())
    fixture=json.loads((HERE/'five-coronas.json').read_text())
    result=audited_check(data,fixture)
    expected=json.loads((HERE/'expected.json').read_text())
    g.require(result==expected,'compact expected mathematics differs')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
