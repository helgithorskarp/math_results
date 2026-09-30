#!/usr/bin/env python3
"""Independent exact four-corona, root-tip rigidity and local-obstruction checker.

Standard library only. Uses Gram columns, rational polygon clipping, complete
charged-port and sector enumeration and direct unit propagation. No author's geometry,
native SAT encoder/solver/proof trace or prior executable is imported.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import gcd
from pathlib import Path
import sys
import signal
from itertools import product

if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python with assertions enabled; -O is unsupported')
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'input.json').read_text())
V=tuple(map(tuple,DATA['prototype_axial_vertices']))
CYCLE=tuple(DATA['counterclockwise_vertex_cycle'])
PORTS=tuple(map(tuple,DATA['ports_counterclockwise']))
SIGN=tuple(DATA['states'])
N=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
RAYS=((1,0),(1,1),(0,1),(-1,2),(-1,1),(-2,1),
      (-1,0),(-1,-1),(0,-1),(1,-2),(1,-1),(2,-1))

def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def det(a,b):return a[0]*b[1]-a[1]*b[0]
def norm(a):return a[0]**2+a[0]*a[1]+a[1]**2
def dot2(a,b):return 2*a[0]*b[0]+a[0]*b[1]+a[1]*b[0]+2*a[1]*b[1]
def primitive(a):
    d=gcd(*a);assert d>0
    return a[0]//d,a[1]//d

# A different orientation inventory from repeated rotations/reflections.
UNITS=[(q,r) for q in range(-1,2) for r in range(-1,2) if norm((q,r))==1]
MATRICES={}
for a in UNITS:
    for b in UNITS:
        if dot2(a,b)==1:
            key=(int(det(a,b)<0),N.index(a))
            assert key not in MATRICES
            MATRICES[key]=(a,b)
assert len(MATRICES)==12

def image(v,p):
    a,b=MATRICES[p[:2]]
    return v[0]*a[0]+v[1]*b[0]+p[2],v[0]*a[1]+v[1]*b[1]+p[3]

def compose(p,q):
    a=image((1,0),q);z=image((0,0),q);b=image((0,1),q)
    x=sub(image(a,p),image(z,p));y=sub(image(b,p),image(z,p))
    keys=[k for k,columns in MATRICES.items() if columns==(x,y)]
    assert len(keys)==1
    return (*keys[0],*image(z,p))

def chords(p):
    edges=[(image(V[a],p),image(V[b],p),i,SIGN[i]) for i,(a,b) in enumerate(PORTS)]
    return [(b,a,i,s) for a,b,i,s in edges] if p[0] else edges

def quad(p):
    indices=(1,17,16,2)
    return [image(V[i],p) for i in (indices[::-1] if p[0] else indices)]

def planes(poly):
    return [(primitive(sub(b,a)),a) for a,b in zip(poly,poly[1:]+poly[:1])]

def clip(subject,border):
    out=[(F(x),F(y)) for x,y in subject]
    for direction,anchor in planes(border):
        if not out:break
        result=[]
        for a,b in zip(out[-1:]+out[:-1],out):
            x,y=det(direction,sub(a,anchor)),det(direction,sub(b,anchor))
            if (x<0)!=(y<0):
                t=x/(x-y);result.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
            if y>=0:result.append(b)
        out=list(dict.fromkeys(result))
    return out

def area2(poly):return sum(det(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))

def overlap(a,b,audit=False):
    # An exact integer broad phase, followed by independent rational clipping.
    if any(max(p[k] for p in a)<=min(p[k] for p in b) or
           max(p[k] for p in b)<=min(p[k] for p in a) for k in (0,1)):
        return False
    poly=clip(a,b)
    if len(poly)<3 or area2(poly)==0:return False
    assert area2(poly)>0
    if audit:
        assert len(poly)<=8
        assert all(z.denominator in (1,2,3) for p in poly for z in p)
        center=tuple(sum(p[k] for p in poly)/len(poly) for k in (0,1))
        for d,p in planes(a)+planes(b):
            slack=det(d,sub(center,p))
            assert slack>=F(1,48)
            assert F(3,4)*slack**2/norm(d)>=F(1,96**2)>F(1,1600**2)
    return True

def ray(a,b):return RAYS.index(primitive(sub(b,a)))

def sector(point,p):
    order=CYCLE[::-1] if p[0] else CYCLE
    vertices=[image(V[i],p) for i in order]
    if point not in vertices:return set()
    k=vertices.index(point);start=ray(point,vertices[(k+1)%len(vertices)]);end=ray(point,vertices[k-1])
    return {(start+j)%12 for j in range((end-start)%12)}

def gaps(occupied):
    assert occupied
    result=[]
    for j in range(12):
        if j in occupied or (j-1)%12 not in occupied:continue
        width=0
        while (j+width)%12 not in occupied:width+=1
        result.append((j,width))
    return result

def point_segment_distance(point,a,b):
    d=sub(b,a);t=dot2(sub(point,a),d);n=norm(d)
    if t<=0:return norm(sub(point,a)),1
    if t>=2*n:return norm(sub(point,b)),1
    return 3*det(d,sub(point,a))**2,4*n

def network_check(poses):
    owners=defaultdict(list)
    for i,p in enumerate(poses):
        for q in poses[:i]:assert not overlap(quad(p),quad(q))
        for a,b,port,s in chords(p):owners[tuple(sorted((a,b)))].append((i,a,b,port,s))
    outside=[];contacts=0
    for edge,rows in sorted(owners.items()):
        assert len(rows)<=2
        if len(rows)==2:
            x,y=rows
            assert x[1:3]==y[2:0:-1] and x[4]+y[4]==0
            contacts+=1
        else:outside.append(rows[0])
    nxt={}
    for row in outside:
        assert row[1] not in nxt,('pinched boundary',row[1])
        nxt[row[1]]=row
    assert set(nxt)=={r[2] for r in outside}
    start=min(nxt);p=start;seen=[]
    while not seen or p!=start:
        assert len(seen)<len(outside)
        seen.append(nxt[p]);p=nxt[p][2]
    assert len(seen)==len(outside),'more than one boundary cycle'
    edges=list(owners)
    minimum=None
    incident=defaultdict(set)
    for a,b in edges:
        assert norm(sub(b,a)) in (1,3)
        incident[a].add(ray(a,b));incident[b].add(ray(b,a))
    for i,(a,b) in enumerate(edges):
        for c,d in edges[:i]:
            if {a,b}&{c,d}:continue
            x,y=det(sub(b,a),sub(c,a)),det(sub(b,a),sub(d,a))
            z,w=det(sub(d,c),sub(a,c)),det(sub(d,c),sub(b,c))
            assert not (x*y<0 and z*w<0),'proper network crossing'
            for numerator,denominator in (point_segment_distance(a,c,d),point_segment_distance(b,c,d),
                                          point_segment_distance(c,a,b),point_segment_distance(d,a,b)):
                assert numerator>0,'unrecorded partial contact'
                assert 4*numerator>=denominator
                if minimum is None or numerator*minimum[1]<minimum[0]*denominator:
                    minimum=(numerator,denominator)
    assert all(min((a-b)%12,(b-a)%12)>=1 for rows in incident.values() for a in rows for b in rows if a!=b)
    return outside,{'copies':len(poses),'contacts':contacts,'exposed_ports':len(outside),
                    'nonincident_distance_squared':str(F(*minimum)),'ray_separation_degrees':30}

def strict_check(old,poses,outside):
    assert not any(i<len(old) for i,a,b,port,s in outside)
    for p in old:
        for v in V:
            point=image(v,p);occupied=set()
            for q in poses:
                s=sector(point,q);assert not occupied&s;occupied|=s
            assert occupied==set(range(12)),('older vertex is exposed',point)

def target_edge(p,port):
    assert SIGN[port] in (-1,1)
    return chords(p)[port]

def mates(edge,old):
    a,b,port,s=edge;raw=set()
    for key in sorted(MATRICES):
        for x,y,new_port,t in chords((*key,0,0)):
            if t!=-s or sub(y,x)!=sub(a,b):continue
            raw.add((*key,*sub(b,x)))
    retained=[]
    for p in sorted(raw):
        if not any(overlap(quad(p),quad(q),True) for q in old):retained.append(p)
    return raw,retained

def unit_refutation(clauses):
    assignments={};steps=[]
    while True:
        reduced=[]
        for row in clauses:
            if any(assignments.get(abs(v))==(v>0) for v in row if abs(v) in assignments):continue
            rest=[v for v in row if abs(v) not in assignments]
            if not rest:return {'answer':'UNSAT','assigned_variables':len(assignments),'steps':steps}
            reduced.append(rest)
        units=[r[0] for r in reduced if len(r)==1]
        if not units:raise AssertionError('No complete unit refutation; no exclusion certified')
        v=units[0];assignments[abs(v)]=v>0;steps.append(v)

def pattern_check(pattern):
    for i,p in enumerate(pattern):
        for q in pattern[:i]:assert not overlap(quad(p),quad(q))
    chord_owners=defaultdict(list)
    for i,p in enumerate(pattern):
        for a,b,port,s in chords(p):chord_owners[tuple(sorted((a,b)))].append((i,port))
    raw=set();rows=[]
    for owner,port in DATA['pattern_target_ports']:
        edge=target_edge(pattern[owner],port)
        assert len(chord_owners[tuple(sorted(edge[:2]))])==1,'target is already paired internally'
        candidates,allowed=mates(edge,pattern);raw|=candidates;rows.append(allowed)
    pool=sorted(set().union(*map(set,rows)));ids={p:i+1 for i,p in enumerate(pool)}
    covers=[[ids[p] for p in row] for row in rows]
    conflicts=[]
    for i,p in enumerate(pool,1):
        for j,q in enumerate(pool[:i-1],1):
            if overlap(quad(p),quad(q),True):conflicts.append([-j,-i])
    refutation=unit_refutation(covers+conflicts)
    return {'copies':len(pattern),'target_arcs':len(rows),'raw_mates':len(raw),'retained_mates':len(pool),
            'cover_sizes':[len(row) for row in covers],'whole_overlap_pairs':len(conflicts),
            'pool_sha256':canonical_hash(pool),'clauses_sha256':canonical_hash(covers+conflicts),
            'unit_refutation':refutation}

def forced_ninety(point,old):
    local=[p for p in old if point in [image(v,p) for v in V]]
    occupied=set();radial=defaultdict(list)
    for p in local:
        s=sector(point,p);assert not s&occupied;occupied|=s
        for a,b,port,sign in chords(p):
            if point==a:radial[ray(a,b)].append((b,sign))
            if point==b:radial[ray(b,a)].append((a,sign))
    found=gaps(occupied);assert len(found)==1 and found[0][1]==3
    start,width=found[0];ends=(start,(start+width)%12)
    assert all(len(radial[r])==1 for r in ends)
    old_sides=[radial[r][0] for r in ends]
    assert sorted(s for end,s in old_sides) in ([-1,0],[0,1])
    pool=set();geometric=0
    for key in sorted(MATRICES):
        for tip in (16,17):
            p=(*key,*sub(point,image(V[tip],(*key,0,0))))
            if sector(point,p)!={(start+j)%12 for j in range(width)}:continue
            geometric+=1
            sides={}
            for a,b,port,s in chords(p):
                if a==point:sides[ray(a,b)]=(b,s)
                if b==point:sides[ray(b,a)]=(a,s)
            if any(sides[r][0]!=radial[r][0][0] or sides[r][1]+radial[r][0][1]!=0 for r in ends):continue
            if any(overlap(quad(p),quad(q),True) for q in old):continue
            pool.add(p)
    assert len(pool)==1,'Ninety-degree filler is not uniquely forced'
    return next(iter(pool)),geometric

def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def partitions(width):
    if width == 0:
        yield ()
    for part in (2, 3, 4, 6):
        if part <= width:
            for tail in partitions(width-part):
                yield (part,) + tail


def radial(point, poses):
    result = defaultdict(list)
    for p in poses:
        for a, b, port, state in chords(p):
            if a == point:
                result[ray(a, b)].append((b, state, port, p))
            if b == point:
                result[ray(b, a)].append((a, state, port, p))
    return result


def fitted(point, start, width):
    desired = {(start+j) % 12 for j in range(width)}
    result = set()
    for v in V:
        for h, k in sorted(MATRICES):
            # These are Gram-preserving columns, with the independently
            # sorted public pose code attached by the published module.
            p = (h, k, *sub(point, image(v, (h, k, 0, 0))))
            if sector(point, p) == desired:
                result.add(p)
    return sorted(result)


def compatible(a, b):
    return a[0] == b[0] and a[1]+b[1] == 0


def audit(point, old, start=None, width=None):
    old = tuple(map(tuple, old))
    occupied = set()
    for p in old:
        piece = sector(point, p)
        assert not occupied & piece
        occupied |= piece
    missing = gaps(occupied)
    if start is None:
        assert len(missing) == 1, missing
        start, width = missing[0]
    else:
        assert (start, width) in missing
    ends = (start, (start+width) % 12)
    old_radial = radial(point, old)
    assert all(len(old_radial[r]) == 1 for r in ends)
    external = {r: old_radial[r][0] for r in ends}
    # At least one charged old boundary is needed for the endpoint-locking
    # argument used by current callers.
    assert any(external[r][1] for r in ends)
    tested, accepted = [], []
    for sizes in partitions(width):
        cursor, pools = start, []
        for size in sizes:
            pools.append(fitted(point, cursor, size))
            cursor += size
        for poses in product(*pools):
            new_radial = radial(point, poses)
            reasons = []
            for r in ends:
                assert len(new_radial[r]) == 1
                if not compatible(external[r], new_radial[r][0]):
                    reasons.append({'kind': 'external-contact', 'ray': r})
            for r, rows in new_radial.items():
                if r not in ends:
                    assert len(rows) == 2
                    if not compatible(*rows):
                        reasons.append({'kind': 'internal-contact', 'ray': r})
            if not reasons:
                for i, p in enumerate(poses):
                    for q in poses[:i]:
                        if overlap(quad(p), quad(q), True):
                            reasons.append({'kind': 'filler-overlap', 'poses': [p, q]})
                    for q in old:
                        if overlap(quad(p), quad(q), True):
                            reasons.append({'kind': 'old-overlap', 'poses': [p, q]})
            if not reasons:
                accepted.append(poses)
            tested.append({'sizes': sizes, 'poses': poses, 'reasons': reasons})
    return {'point': point, 'start_ray': start, 'angle_degrees': width*30,
            'external_states': [external[r][1] for r in ends],
            'tested': tested, 'accepted': accepted}

def verify_root90():
    root = (0, 0, 0, 0)
    mate = (1, 3, 8, -2)
    old = [root, mate]
    raw, pool = mates(target_edge(root, 16), old)
    assert pool == [(0, 5, 8, -1)]
    right = pool[0]
    old.append(right)
    cap, trials = forced_ninety((8, -1), old)
    assert cap == (1, 3, 15, 0)
    old.append(cap)
    tip = audit((0, -1), old)
    assert tip['angle_degrees'] == 210 and tip['external_states'] == [1, 0]
    expected_tip = ((0, 1, -1, 0), (0, 2, -1, -1), (1, 0, -7, -2))
    assert tip['accepted'] == [expected_tip]
    old.extend(expected_tip)
    left = audit((0, 1), old)
    assert left['angle_degrees'] == 60 and left['external_states'] == [1, -1]
    top = (0, 0, 0, 2)
    assert left['accepted'] == [(top,)]
    old.append(top)
    poses = (root,) + tuple(sorted(set(old)-{root}))
    fixture = tuple(map(tuple, DATA['root90_first']))
    assert poses == fixture
    outside, network = network_check(poses)
    strict_check((root,), poses, outside)
    root_endpoints = {image(v, root) for v in V}
    assert all(root_endpoints & {image(v, p) for v in V} for p in poses[1:])

    # This target is an older point: it belongs to top and cap. If both are
    # interior, the additional ninety-degree filler must occur, but need not
    # itself be interior for the following five charged-arc contradiction.
    interior_old = (top, right, cap)
    filler, second_trials = forced_ninety((8, 1), interior_old)
    assert filler == (1, 3, 15, 2)
    absolute_pattern = (right, cap, filler)
    normalized = tuple(map(tuple, DATA['interior_pattern']))
    assert tuple(compose(cap, p) for p in normalized) == absolute_pattern
    assert set(owner for owner, port in DATA['pattern_target_ports']) == {0, 1}
    obstruction = pattern_check(absolute_pattern)

    return {
        'first_poses': poses, 'network': network,
        'port16_raw': len(raw), 'port16_unique': right,
        'first90_trials': trials, 'first210_trials': len(tip['tested']),
        'first210_unique_partition': tip['accepted'][0],
        'first60_trials': len(left['tested']), 'first60_unique': top,
        'old_pattern': interior_old, 'forced_second_tile': filler,
        'second90_trials': second_trials, 'five_arc_obstruction': obstruction,
        'second_filler_interiority_required': False,
        'claim': 'This attachment forces the eight-copy touching first corona, which has no second strict surround under arbitrary motions and final topology.'}


def verify_two_caps():
    poses = ((0, 0, 0, 2), (1, 3, 15, 0), (0, 0, 4, -2))
    outside, network = network_check(poses)
    forces = [forced_ninety(point, poses) for point in ((8, 1), (11, -1))]
    fillers = [p for p, count in forces]
    assert fillers == [(1, 3, 15, 2), (1, 3, 19, -2)]
    assert not overlap(quad(fillers[0]), quad(fillers[1]))
    edge = target_edge(poses[1], 1)
    raw, pool = mates(edge, poses)
    assert len(raw) == len(pool) == 16
    blockers = []
    for p in pool:
        hits = [i for i, q in enumerate(fillers) if overlap(quad(p), quad(q), True)]
        assert hits
        blockers.append({'pose': p, 'forced_filler_indices': hits})
    assert sum(0 in row['forced_filler_indices'] for row in blockers) == 15
    return {
        'poses': poses, 'network': network, 'forced_fillers': fillers,
        'ninety_geometric_trials': [n for p,n in forces],
        'target_port': 1, 'raw_mates': len(raw), 'retained_mates': len(pool),
        'first_filler_blocks': 15, 'second_filler_blocks_remaining': 1,
        'pool_sha256': canonical_hash(pool),
        'claim': 'The three older copies cannot all be interior; the two forced fillers need not be interior.'}


def verify_six_fan():
    old = ((0, 0, -9, 2), (1, 3, -2, 10), (1, 3, 0, 8),
           (1, 3, 2, 6), (1, 3, 4, 4), (1, 4, -3, 1))
    for i, p in enumerate(old):
        for q in old[:i]:
            assert not overlap(quad(p), quad(q))
    ninety_points = ((-8, 9), (-6, 7), (-4, 5))
    forces = [forced_ninety(point, old) for point in ninety_points]
    fillers = [p for p, n in forces]
    sixty = audit((-4, 1), old)
    assert sixty['angle_degrees'] == 60
    assert sixty['accepted'] == [((1, 4, -5, 1),)]
    fillers.append(sixty['accepted'][0][0])
    assert fillers == [(0, 0, -15, 8), (0, 0, -13, 6),
                       (0, 0, -11, 4), (1, 4, -5, 1)]
    rows, raw = [], set()
    for port in (1, 2, 6):
        all_poses, allowed = mates(target_edge(old[0], port), old+tuple(fillers))
        raw |= all_poses
        rows.append(allowed)
    pool = sorted(set().union(*map(set, rows)))
    assert len(pool) == 7 and list(map(len, rows)) == [1, 5, 1]
    ids = {p: i+1 for i, p in enumerate(pool)}
    clauses = [[ids[p] for p in row] for row in rows]
    pairs = []
    for i, p in enumerate(pool):
        for j, q in enumerate(pool[:i]):
            if overlap(quad(p), quad(q), True):
                pairs.append([-j-1, -i-1])
    clauses += pairs
    refutation = unit_refutation(clauses)
    fixture = {tuple(row['pose']) for row in DATA['second_branch_witness']}
    assert set(old) <= fixture
    return {
        'poses': old, 'ninety_gap_points': ninety_points,
        'ninety_trials': [n for p,n in forces], 'sixty_gap_point': (-4,1),
        'sixty_trials': len(sixty['tested']), 'forced_fillers': fillers,
        'charged_ports': [1,2,6], 'raw_mates': len(raw), 'retained_mates': len(pool),
        'cover_sizes': list(map(len,rows)), 'whole_overlap_pairs': len(pairs),
        'pool_sha256': canonical_hash(pool), 'clauses_sha256': canonical_hash(clauses),
        'unit_refutation': refutation,
        'claim': 'The six older copies cannot all be interior; the checked43-copy second prefix has no third strict surround.'}


def verify_tip():
    root=(0,0,0,0);point=(0,-1)
    raw,pool=mates(target_edge(root,2),(root,))
    assert len(raw)==len(pool)==18
    survivors=[];excluded=[]
    for p in pool:
        network_check((root,p))
        old_sector=sector(point,root);new_sector=sector(point,p)
        assert new_sector and not old_sector&new_sector
        gap=gaps(old_sector|new_sector);assert len(gap)==1
        start,width=gap[0]
        ports=radial(point,(root,p));ends=(start,(start+width)%12)
        assert all(len(ports[r])==1 for r in ends)
        signs=[ports[r][0][1] for r in ends]
        forbidden=width==4 and signs==[1,1]
        assert forbidden==(len(new_sector)==6)
        (excluded if forbidden else survivors).append(p)
    expected=[(0,0,0,-2),(0,5,1,-1),(1,3,8,-2),(1,4,1,-1)]
    assert survivors==expected and len(excluded)==14
    return {'raw_mates':18,'signed120_excluded':14,'one_corona_survivors':survivors,
            'two_corona_survivors':[p for p in survivors if p!=(1,3,8,-2)],
            'scope':'Necessary mate lists, not a classification of all first coronas.'}


def verify_witness(field, counts):
    witness=DATA[field]
    poses=tuple(tuple(row['pose']) for row in witness)
    levels=[row['level'] for row in witness]
    assert levels==sorted(levels) and Counter(levels)==Counter(dict(enumerate(counts)))
    assert poses[0]==(0,0,0,0) and len(poses)==len(set(poses))
    metrics=[];old=(poses[0],)
    endpoints=[{image(v,p) for v in V} for p in poses]
    for level in range(1,len(counts)):
        prefix=poses[:sum(counts[:level+1])]
        outside,metric=network_check(prefix);strict_check(old,prefix,outside)
        for i in range(len(old),len(prefix)):
            assert any(levels[j]==level-1 and endpoints[i]&endpoints[j] for j in range(len(old)))
        metrics.append(metric);old=prefix
    return {'layer_counts':list(counts),'prefixes':metrics,
            'witness_sha256':canonical_hash(witness)}


def run_all():
    assert DATA['amplitude']=='1/100'
    expected_vertices=((0,0),(0,-1),(0,1))+tuple(p for j in range(1,8) for p in ((j,-1),(j,1)))+((8,-1),)
    assert V==expected_vertices
    assert CYCLE==(0,1,3,5,7,9,11,13,15,17,16,14,12,10,8,6,4,2)
    expected_pairs=[(0,1),(0,2)]+[(i,i+2) for i in range(1,16)]+[(16,17)]
    assert tuple(map(frozenset,PORTS))==tuple(map(frozenset,expected_pairs))
    assert SIGN==(1,1)+tuple(-1 if i%2==0 else 1 for i in range(2,17))+(0,)
    assert len(V)==len(set(V))==18 and set(CYCLE)==set(range(18))
    assert set(PORTS)==set(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
    assert [norm(sub(V[b],V[a])) for a,b in PORTS]==[1]*17+[3]
    assert Counter(SIGN)==Counter({1:9,-1:8,0:1})
    assert area2(quad((0,0,0,0)))==30
    assert max(norm(sub(a,b)) for a in V for b in V)==67
    assert Counter(len(sector(v,(0,0,0,0)))*30 for v in V)==Counter({60:1,90:2,120:1,180:14})
    assert tuple(map(tuple,DATA['pattern_target_ports']))==((0,3),(1,10),(1,6),(1,2),(1,1))

    tip=verify_tip();root90=verify_root90();caps=verify_two_caps();fan=verify_six_fan()
    four=verify_witness('witness',(1,11,33,49,53))
    branch=verify_witness('second_branch_witness',(1,11,31))
    growth=1
    for depth in range(1000):
        cap=(F(22,7)*F(6553,800)**2/F(1299,100)*(depth+1)**2).__floor__()
        if growth>cap:break
        growth=(9*growth+7)//8
    assert depth==86 and growth==130235 and cap==122872
    return {'agent':'six-heesch-3','role':'researcher',
            'candidate_bound':'4 <= Hc(T) <= Hh(T) <=85',
            'four_coronas':four,'root_tip_reduction':tip,'root90_branch':root90,
            'two_cap_obstruction':caps,'six_fan_obstruction':fan,
            'reflected120_two_coronas':branch,
            'charge_upper_obstruction':{'first_failed_depth':depth,'minimum_copies':growth,'maximum_copies':cap},
            'scope':'The connected Euclidean finite-seven target and exact Heesch number remain open.',
            'trust_boundary':'Separate same-author exact standard-library geometry; written atomic-contact, buffer, finite-angle and Jordan-isotopy bridges, prior finite85 charge proof. No formalization or independent reviewer verdict.'}


def controls():
    global DATA
    original=DATA
    rejected=[]
    for name in ('amplitude','missing_fourth_copy','wrong_root90_fixture'):
        DATA=json.loads(json.dumps(original))
        if name=='amplitude':DATA['amplitude']='1/99'
        elif name=='missing_fourth_copy':DATA['witness'].pop()
        else:DATA['root90_first'][-1]=[1,3,15,1]
        try:run_all()
        except AssertionError:rejected.append(name)
        else:raise RuntimeError('Malformed input accepted: '+name)
        finally:DATA=original
    return rejected


def main():
    signal.alarm(55)
    result=run_all()
    if '--expected' in sys.argv:
        i=sys.argv.index('--expected')
        expected=json.loads(Path(sys.argv[i+1]).read_text())
        assert json.loads(json.dumps(result))==expected,'Expected result mismatch'
    if '--controls' in sys.argv:
        result['rejected_controls']=controls()
    signal.alarm(0)
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
