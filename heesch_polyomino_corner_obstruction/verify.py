"""Independent rectangle replay of every published corner-forcing certificate."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import time

from corners import (QUADRANTS,cells,disc,footprint,image_cell,normalize,
                     propagate,variants,vertices)

HERE=Path(__file__).resolve().parent
if not __debug__:
    raise RuntimeError('certificate checks require Python assertions; omit -O and -OO')


def rectangle_variants(raw):
    # Rotate doubled square centers successively; reflect in the horizontal
    # axis. This does not use the signed-permutation orientation generator.
    centers=[(2*x+1,2*y+1) for x,y in cells(raw)]
    result=set()
    for reflection in (1,-1):
        current=[(x,reflection*y) for x,y in centers]
        for turn in range(4):
            lower=[((x-1)//2,(y-1)//2) for x,y in current]
            xmin=min(x for x,y in lower);ymin=min(y for x,y in lower)
            result.add(tuple(sorted((x-xmin,y-ymin) for x,y in lower)))
            current=[(-y,x) for x,y in current]
    return tuple(sorted(result))


def rectangles(shape,translation):
    tx,ty=translation
    return tuple((x+tx,y+ty,x+tx+1,y+ty+1) for x,y in shape)


def interiors_intersect(a,b):
    return a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]


def rectangle_choices(shapes,target,occupied):
    ux,uy=target;result=[]
    for shape in shapes:
        for x,y in shape:
            translation=ux-x,uy-y
            candidate=rectangles(shape,translation)
            if not any(interiors_intersect(a,b) for a in candidate for b in occupied):
                result.append((shape,translation,candidate))
    return result


def vertex_quadrants(vertex,occupied):
    # Test one point at the center of each incident unit quadrant; exact
    # doubled coordinates suffice because all current rectangles are integral.
    vx,vy=vertex
    result=[]
    for dx,dy in QUADRANTS:
        px,py=2*(vx+dx)+1,2*(vy+dy)+1
        result.append(any(2*a[0]<px<2*a[2] and 2*a[1]<py<2*a[3] for a in occupied))
    return result


def replay(tile,copies,steps):
    shapes=rectangle_variants(tile)
    assert shapes==variants(tile) and disc(tile)
    occupied=[];original_vertices=set()
    for shape,translation in copies:
        shape=cells(shape)
        assert shape in shapes
        new=rectangles(shape,translation)
        assert not any(interiors_intersect(a,b) for a in new for b in occupied)
        occupied.extend(new)
        for a in new:
            original_vertices.update(((a[0],a[1]),(a[0],a[3]),(a[2],a[1]),(a[2],a[3])))
    for step in steps:
        vertex=tuple(step['vertex']);quadrant=step['quadrant']
        target=tuple(step['target_cell']);qs=vertex_quadrants(vertex,occupied)
        assert vertex in original_vertices and type(quadrant) is int and 0<=quadrant<4
        dx,dy=QUADRANTS[quadrant]
        assert target==(vertex[0]+dx,vertex[1]+dy)
        assert not qs[quadrant] and qs[(quadrant-1)%4] and qs[(quadrant+1)%4]
        feasible=rectangle_choices(shapes,target,occupied)
        assert len(feasible)==step['feasible_poses']
        if step['feasible_poses']==1:
            chosen=step.get('forced_copy',step)
            assert feasible[0][:2]==(cells(chosen['shape']),tuple(chosen['translation']))
            occupied.extend(feasible[0][2])
        else:
            assert step['feasible_poses']==0 and step is steps[-1]
    assert steps and steps[-1]['feasible_poses']==0
    return len(steps)-1


def transformed_motif(data,swap,sx,sy):
    out=copy.deepcopy(data)
    def pose(p):
        image=[image_cell(q,swap,sx,sy) for q in footprint(p['shape'],p['translation'])]
        return {'shape':normalize(image),'translation':[min(x for x,y in image),min(y for x,y in image)]}
    out['fixed_copies']=[pose(p) for p in data['fixed_copies']]
    for step,original in zip(out['steps'],data['steps']):
        x,y=original['vertex']
        step['vertex']=(sx*(y if swap else x),sy*(x if swap else y))
        step['target_cell']=image_cell(original['target_cell'],swap,sx,sy)
        offset=tuple(a-b for a,b in zip(step['target_cell'],step['vertex']))
        step['quadrant']=QUADRANTS.index(offset)
        if 'forced_copy' in original:step['forced_copy']=pose(original['forced_copy'])
    return out


def check_motif(data):
    copies=[(p['shape'],tuple(p['translation'])) for p in data['fixed_copies']]
    assert len(copies)==2 and len(variants(data['tile']))==8 and len(data['tile'])==17
    return replay(data['tile'],copies,data['steps'])


def reject_bad_fixtures(data):
    bad=[]
    x=copy.deepcopy(data);x['steps'][0]['feasible_poses']=2;bad.append(x)
    x=copy.deepcopy(data);x['steps'][0]['forced_copy']['translation'][0]+=1;bad.append(x)
    x=copy.deepcopy(data);x['steps'][1]['target_cell'][1]+=1;bad.append(x)
    x=copy.deepcopy(data);x['tile'].append(x['tile'][0]);bad.append(x)
    x=copy.deepcopy(data);x['fixed_copies'][1]['translation'][0]+=1;bad.append(x)
    for fixture in bad:
        try:check_motif(fixture)
        except (AssertionError,ValueError):continue
        raise RuntimeError('malformed certificate was accepted')
    return len(bad)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--motif-only',action='store_true')
    args=parser.parse_args();start=time.monotonic()
    data=json.loads((HERE/'motif.json').read_text())
    assert check_motif(data)==1
    for swap in (False,True):
        for sx in (-1,1):
            for sy in (-1,1):assert check_motif(transformed_motif(data,swap,sx,sy))==1
    bad=reject_bad_fixtures(data)
    result={'agent':'six-heesch-1','role':'researcher','tile_cells':17,'D4_variants':8,
            'unit_cell_pose_choices_per_corner':136,'primitive_feasible_counts':[1,0],
            'symmetry_images_replayed':8,'malformed_fixtures_rejected':bad,
            'motif_sha256':hashlib.sha256((HERE/'motif.json').read_bytes()).hexdigest()}
    if not args.motif_only:
        library=json.loads((HERE/'pairs.json').read_text());shapes=variants(data['tile'])
        assert cells(library['tile'])==cells(data['tile'])
        checked=0;maximum=0
        for orientation,x,y in library['forbidden_poses']:
            result1=propagate(data['tile'],[(normalize(data['tile']),(0,0)),(shapes[orientation],(x,y))])
            assert result1['status']=='contradiction'
            steps=result1['trace']+[result1['empty_corner']]
            maximum=max(maximum,replay(data['tile'],[(normalize(data['tile']),(0,0)),(shapes[orientation],(x,y))],steps))
            checked+=1
        assert checked==237 and maximum==4
        result.update({'forbidden_pair_certificates_replayed':checked,
                       'maximum_forced_copies':maximum,
                       'pairs_sha256':hashlib.sha256((HERE/'pairs.json').read_bytes()).hexdigest()})
    result['seconds']=round(time.monotonic()-start,3)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
