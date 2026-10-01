#!/usr/bin/env python3
"""Direct cell-anchor replay of one fixed-patch grid obstruction.

The candidate domain is generated anew from the69 fine prototype cells,
not read from the54504-pose collar search. Each alleged conflict is
then checked using actual convex atoms in the integer polygon reader.
This excludes only a registered-grid extension of the GIVEN169-copy
prefix. It is not an upper bound over all prefixes or all motions.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import resource
import time
import geometry as b
import mesh as g

HERE=Path(__file__).resolve().parent
TARGET=(1,-144,-68,-144,-66,-138,-66)

def check(data):
    start=time.monotonic();m=data['tile_hexagons']
    old=[tuple(r['pose']) for r in data['copies']]
    b.require(m==6 and len(old)==169,'one-cell target belongs to the fixed published six control')
    target=b.ccw(g.cell_vertices(TARGET))
    atoms=[]
    old_owner={}
    for i,p in enumerate(old):
        for cell in g.footprint(m,p):
            b.require(cell not in old_owner,'old fine-cell footprints overlap')
            old_owner[cell]=i
        atoms.extend(tuple((3*x,3*y) for x,y in a) for a in b.shape(m,p)[0])
    shared=[(v,i) for v in target for i,a in enumerate(atoms)
            if all(b.turn(a[k],a[(k+1)%len(a)],v)>=0 for k in range(len(a)))]
    b.require(shared,'target fine cell does not touch the old closed union')
    b.require(all(not b.convex_intersection(a,target,False) for a in atoms),
              'target fine cell intersects the old union interior')
    b.require(TARGET not in old_owner,'target fine cell already occupied')
    # Prove the fine prototypes represent the same polygon; the integer
    # reader independently verifies areas, noncrossing boundary and cells.
    cells=g.local_cells(m)
    polys=[b.ccw(g.hex_vertices(k[1:]) if k[0]==0 else g.cell_vertices(k)) for k in cells]
    fine,_=b.boundary(polys)
    coarse,_=b.boundary([tuple((3*x,3*y) for x,y in p) for p in b.atoms(m)])
    def essential(c):
        return {c[i] for i in range(len(c)) if b.turn(c[i-1],c[i],c[(i+1)%len(c)])}
    b.require(essential(fine)==essential(coarse),'fine prototype does not match actual polygon')
    for i,a in enumerate(polys):
        for other in polys[i+1:]:
            b.require(not b.convex_intersection(a,other,False),'fine prototype cells overlap')
    proposals=set();anchor_matches=0
    for angle in range(0,12,2):
        for flip in (0,1):
            for cell in cells:
                if not cell[0]:
                    continue
                turned=g.transform(cell,angle,flip,(0,0))
                delta=(TARGET[1]-turned[1],TARGET[2]-turned[2])
                if g.shifted(turned,delta)!=TARGET:
                    continue
                anchor_matches+=1
                c=b.rotate(angle,(12,0));c=(c[0]+delta[0],c[1]+delta[1])
                # Registered hex centers are(12+24*i+12*j,12*j).
                if c[1]%12 or (c[0]-12-c[1])%24:
                    continue
                b.require(delta[0]%3==delta[1]%3==0,'registered translation not in quarter module')
                proposals.add((angle,flip,delta[0]//3,delta[1]//3))
    b.require(proposals,'vacuous target domain')
    conflicts=[];histogram=Counter()
    for p in sorted(proposals):
        b.require(TARGET in g.footprint(m,p),'anchored pose fails to cover target cell')
        collision=sorted(g.footprint(m,p)&old_owner.keys())
        b.require(collision,'a non-overlapping registered target supplier remains')
        owner=old_owner[collision[0]]
        overlap,touch=b.pair(m,p,old[owner])
        b.require(overlap,'mesh collision is not positive actual-polygon overlap')
        conflicts.append({'pose':p,'old_copy_index':owner})
        histogram[owner]+=1
    digest=sha256(json.dumps(conflicts,separators=(',',':'),sort_keys=True).encode()).hexdigest()
    return {'agent':'six-heesch-3','role':'researcher',
            'scope':'fixed169-copy prefix; registered3.6.3.6 grid only',
            'target_triangle_scaled3':target,'touching_old_point':shared[0][0],
            'prototype_fine_triangles':sum(k[0] for k in cells),
            'orientation_reflection_cases':12,'raw_cell_anchor_matches':anchor_matches,
            'unique_registered_covering_poses':len(proposals),
            'actual_polygon_overlap_exclusions':len(conflicts),
            'overlap_witnesses_sha256':digest,'old_copy_conflict_histogram':dict(sorted(histogram.items())),
            'all_motion_upper_claimed':False,'elapsed_seconds':time.monotonic()-start,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
