"""Definition-level pattern oracle by affine triangle matching.

Does not use the convex-vertex/matrix generator used in discovery. Every tile
triangle is mapped bijectively onto the missing triangle, deriving the affine
isometry from the vertex images, and whole footprints are checked exactly.
"""
from itertools import permutations
from common import g,vertices,compact,masks,star,adjacent,footprint


def affine(source,target):
    u,v,w=source;a,b,c=target
    x,y=v[0]-u[0],v[1]-u[1];z,t=w[0]-u[0],w[1]-u[1]
    det=x*t-y*z;assert abs(det)==1
    e,f=b[0]-a[0],c[0]-a[0];h,k=b[1]-a[1],c[1]-a[1]
    matrix=[(e*t-f*y)//det,(-e*z+f*x)//det,
            (h*t-k*y)//det,(-h*z+k*x)//det]
    g.check.isometry(matrix)
    r,s,i,j=matrix
    return {'matrix':matrix,'translation':[a[0]-r*u[0]-s*u[1],a[1]-i*u[0]-j*u[1]]}


def providers(shape,v,cell,gap):
    poses={}
    for t in sorted(shape):
        for image in permutations(vertices(cell)):
            pose=affine(t,image);poses[g.key(pose)]=pose
    out=[]
    for key,pose in sorted(poses.items()):
        f=footprint(shape,pose);sector=masks(f).get(v,0)
        if sector.bit_count() in (1,2) and not sector & ~gap:
            assert cell in f;out.append((pose,f))
    return out


def check(shape,pattern):
    occupied=set()
    for p in pattern['poses']:
        g.check.isometry(p['matrix']);assert all(type(x) is int for x in p['translation'])
        f=footprint(shape,p)
        assert len(f)==214 and occupied.isdisjoint(f);occupied.update(f)
    if pattern['kind']=='small_hole':
        hole=set(map(tuple,pattern['hole_cells']))
        assert 0<len(hole)<214 and hole.isdisjoint(occupied)
        assert all(q in hole or q in occupied for t in hole for q in adjacent(t))
        return {'verified':True,'hole_area_units':len(hole),'copies':len(pattern['poses'])}
    targets=pattern['targets'] if pattern['kind']=='forced_clash' else \
            [{'vertex':pattern['target'],'cell':pattern['missing_cell']}]
    vm=masks(occupied);trials=[];available=[];star_masks=[]
    for row in targets:
        v=tuple(row['vertex']);cell=tuple(row['cell']);mask=vm[v];gap=63^mask
        assert mask.bit_count() in (4,5) and cell in star(v)-occupied
        assert sum(((mask>>j)&1)!=((mask>>((j+1)%6))&1) for j in range(6))==2
        options=providers(shape,v,cell,gap);trials.append(len(options));star_masks.append(mask)
        available.append([(p,f) for p,f in options if occupied.isdisjoint(f)])
    if pattern['kind']=='empty_corner':
        assert len(targets)==1 and not available[0]
        return {'verified':True,'provider_trials':trials[0],'filled_star_mask':star_masks[0],
                'copies':len(pattern['poses'])}
    assert pattern['kind']=='forced_clash' and len(targets)==2 and all(available)
    assert all(f!=h and not f.isdisjoint(h) for p,f in available[0] for q,h in available[1])
    return {'verified':True,'copies':len(pattern['poses']),'provider_trials':trials,
            'available_providers':[len(a) for a in available],
            'forced_poses':[[p for p,f in choices] for choices in available]}
