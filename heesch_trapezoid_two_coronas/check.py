#!/usr/bin/env python3
"""Independent exact two-corona and three-copy obstruction checker.

Standard library only. Uses Gram columns, rational polygon clipping, complete
five-port mate enumeration and direct unit propagation. No author's geometry,
native SAT encoder/solver/proof trace or prior executable is imported.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import gcd
from pathlib import Path
import sys

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

def main():
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
    witness=DATA['witness'];poses=tuple(tuple(row['pose']) for row in witness)
    levels=[row['level'] for row in witness]
    assert levels==sorted(levels) and Counter(levels)==Counter({0:1,1:10,2:25})
    assert poses[0]==(0,0,0,0) and len(poses)==len(set(poses))
    first=poses[:11];old=(poses[0],);results=[]
    for prefix in (first,poses):
        outside,result=network_check(prefix);strict_check(old,prefix,outside)
        results.append(result);old=prefix
    endpoints=[{image(v,p) for v in V} for p in poses]
    for i,level in enumerate(levels):
        if level:
            assert any(levels[j]==level-1 and endpoints[i]&endpoints[j] for j in range(i))
    pattern=tuple(map(tuple,DATA['interior_pattern']))
    lemma=pattern_check(pattern)
    owner,port=DATA['first_prefix_forced_arc']
    raw,arc=mates(target_edge(first[owner],port),first);assert len(arc)==1
    gap_results=[forced_ninety(tuple(p),first) for p in DATA['first_prefix_forced_gaps']]
    forced=tuple(arc+[row[0] for row in gap_results])
    assert forced==tuple(map(tuple,DATA['first_prefix_forced_pattern_absolute']))
    matches=[anchor for anchor in poses if tuple(compose(anchor,p) for p in pattern)==forced]
    assert len(matches)==1 and set(forced)<=set(poses)
    growth=1
    for depth in range(1000):
        cap=(F(22,7)*F(6553,800)**2/F(1299,100)*(depth+1)**2).__floor__()
        if growth>cap:break
        growth=(9*growth+7)//8
    assert depth==86 and growth==130235 and cap==122872
    result={'agent':'six-heesch-3','role':'researcher','witness_coronas':results,
            'interior_three_copy_pattern':lemma,
            'fixed_first_prefix':{'charged_arc_raw_mates':len(raw),'charged_arc_retained_mates':len(arc),
                'ninety_gap_geometric_trials':[r[1] for r in gap_results],'forced_second_poses':forced,
                'pattern_embedding_anchor':matches[0],
                'claim':'Any arbitrary-motion second surround of these eleven first-prefix copies cannot extend to a third, even allowing holes.'},
            'candidate_bound':'2 <= Hc(T) <= Hh(T) <=85; other first coronas and exact Heesch numbers remain open',
            'charge_packing_failure':{'depth':depth,'minimum_copies':growth,'maximum_copies':cap},
            'trust_boundary':'Written quartic-contact, uniform-buffer, finite-angle and Jordan-isotopy arguments plus exact standard-library Python; no formalization or independent reviewer verdict'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
