"""Direct exhaustive star check and an odd-cycle obstruction for C3598."""
from geometry import DIRS,affine,halo,inverse,pose

ID=(1,0,0,1,0,0)
G=(0,1,-1,-1,1,-1)


def compose(f,g):
    a,b,c,d,u,v=f;e,h,i,j,x,y=g
    return (a*e+b*i,a*h+b*j,c*e+d*i,c*h+d*j,a*x+b*y+u,c*x+d*y+v)


def invalid_pair(tiles,tile,domain):
    """Direct geometric/contact-domain rejection; None means admissible."""
    tiles=tuple(sorted(set(tiles)))
    for i,t in enumerate(tiles):
        for u in tiles[:i]:
            overlap=sorted(set(t)&set(u))
            if overlap:return {'reason':'overlap','cell':overlap[0],'a':t,'b':u}
            if any((x+a,y+b) in u for x,y in t for a,b in DIRS):
                relative=affine(u,inverse(pose(tile,t)))
                if relative not in domain:return {'reason':'forbidden_contact','a':t,'b':u,'relative':relative}
    return None


def all_subset_stars(tile,domain):
    """All 2^11 subsets; no MRV, memo table, or search conflict bitsets."""
    candidates=tuple(sorted(domain));required=halo(tile);stars=set()
    assert len(candidates)==11
    for mask in range(1<<len(candidates)):
        selected=tuple(candidates[i] for i in range(len(candidates)) if mask>>i&1)
        occupied=set(tile).union(*selected)
        if not required<=occupied:continue
        if invalid_pair((tile,)+selected,tile,domain) is None:stars.add(tuple(sorted(selected)))
    return stars


def verify(p,domain):
    tile=p.tile
    assert p.stabilizers==[ID]
    p.check_domain(domain)
    c=p.cover((tile,),domain)
    stars={tuple(sorted(c.tiles[i] for i in s)) for s in c.solutions()}
    assert stars==all_subset_stars(tile,domain)
    stars=sorted(stars,key=lambda s:(len(s),s))
    assert [len(s) for s in stars]==[5,7]
    assert compose(compose(G,G),G)==ID
    gtile=affine(tile,G);ggtile=affine(tile,compose(G,G))
    assert len({tile,gtile,ggtile})==3
    assert all(gtile in s and ggtile in s for s in stars)
    # All triangle vertices are root/first-corona copies. In H=3 their full
    # E1 stars exist, and all copies of their stars have level <=2. Equal
    # types across the G edge are impossible, at each of its three images.
    failures=[]
    for star in stars:
        moved=tuple(affine(t,G) for t in star)
        assert tile in moved
        failure=invalid_pair((tile,)+star+(gtile,)+moved,tile,domain)
        assert failure is not None
        failures.append(failure)
    return {'domain_size':len(domain),'subset_masks':1<<len(domain),
            'star_degrees':[len(s) for s in stars],'triangle_generator':G,
            'same_type_rejections':[f['reason'] for f in failures],
            'Hh_upper':2,'plane_tiling_excluded':True}
