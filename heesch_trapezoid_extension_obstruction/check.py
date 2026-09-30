#!/usr/bin/env python3
"""Independent exact reconstruction and direct finite packing exhaustion.

Standard library only. No author's geometry, SAT encoding/solver or native
proof checker is imported. See proof.md for the written geometric bridges.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE/'input.json').read_text())
V = tuple(map(tuple,DATA['prototype_axial_vertices']))
CYCLE = tuple(DATA['counterclockwise_vertex_cycle'])
PORTS = tuple(map(tuple,DATA['ports_counterclockwise']))
SIGN = tuple(DATA['states'])
FIRST = tuple((int(p['reflect']),p['turns'],*p['axial_translation'])
              for p in DATA['flat_first_corona_poses'])
N = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
RAYS = ((1,0),(1,1),(0,1),(-1,2),(-1,1),(-2,1),
        (-1,0),(-1,-1),(0,-1),(1,-2),(1,-1),(2,-1))


def plus(a,b): return a[0]+b[0],a[1]+b[1]
def minus(a,b): return a[0]-b[0],a[1]-b[1]
def det(a,b): return a[0]*b[1]-a[1]*b[0]
def norm(a): return a[0]**2+a[0]*a[1]+a[1]**2
def scalar(a,b): return F(2*a[0]*b[0]+a[0]*b[1]+a[1]*b[0]+2*a[1]*b[1],2)


# Enumerate integral Gram-preserving column pairs, rather than generating
# matrices by repeated sixty-degree rotations and reflections.
UNITS = [(q,r) for q in range(-1,2) for r in range(-1,2) if norm((q,r))==1]
assert set(UNITS)==set(N)
MATRICES = {}
for a in UNITS:
    for b in UNITS:
        if scalar(a,b)==F(1,2):
            key = (int(det(a,b)<0),N.index(a))
            assert key not in MATRICES
            MATRICES[key] = (a,b)
assert len(MATRICES)==12


def image(v,p):
    a,b = MATRICES[p[:2]]
    return v[0]*a[0]+v[1]*b[0]+p[2],v[0]*a[1]+v[1]*b[1]+p[3]


def chord_list(p):
    edges = [(image(V[a],p),image(V[b],p),i,SIGN[i]) for i,(a,b) in enumerate(PORTS)]
    return [(b,a,i,s) for a,b,i,s in edges] if p[0] else edges


def quad(p):
    indices = (1,17,16,2)
    if p[0]: indices=indices[::-1]
    return [image(V[i],p) for i in indices]


def primitive(v):
    k = gcd(*v)
    assert k > 0
    return v[0]//k,v[1]//k


def planes(poly):
    return [(primitive(minus(b,a)),a) for a,b in zip(poly,poly[1:]+poly[:1])]


def clip(subject,border):
    """Rational half-plane clipping, independently of separating axes."""
    out = [(F(x),F(y)) for x,y in subject]
    for direction,anchor in planes(border):
        if not out: break
        nxt = []
        for a,b in zip(out[-1:]+out[:-1],out):
            x,y = det(direction,minus(a,anchor)),det(direction,minus(b,anchor))
            if (x < 0) != (y < 0):
                t = x/(x-y)
                nxt.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
            if y >= 0: nxt.append(b)
        out = list(dict.fromkeys(nxt))
    return out


def area2(poly):
    return sum(det(a,b) for a,b in zip(poly,poly[1:]+poly[:1]))


def overlap(a,b,buffer_audit=False):
    intersection = clip(a,b)
    if len(intersection)<3 or area2(intersection)==0: return False
    assert area2(intersection)>0
    if buffer_audit:
        assert len(intersection)<=8
        assert all(z.denominator in (1,2,3) for v in intersection for z in v)
        center = tuple(sum(v[i] for v in intersection)/len(intersection) for i in (0,1))
        for direction,anchor in planes(a)+planes(b):
            slack = det(direction,minus(center,anchor))
            assert slack>=F(1,48)
            distance2 = F(3,4)*slack**2/norm(direction)
            assert distance2>=F(1,96**2)>F(1,1600**2)
    return True


def direction_index(a,b): return RAYS.index(primitive(minus(b,a)))


def sector(point,p):
    order = CYCLE[::-1] if p[0] else CYCLE
    vertices = [image(V[i],p) for i in order]
    if point not in vertices: return set()
    k = vertices.index(point)
    start = direction_index(point,vertices[(k+1)%len(vertices)])
    end = direction_index(point,vertices[k-1])
    return {(start+j)%12 for j in range((end-start)%12)}


def segment_contains(a,b,p):
    return det(minus(b,a),minus(p,a))==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])


def distance2(point,a,b):
    d = minus(b,a)
    t = max(F(0),min(F(1),scalar(minus(point,a),d)/norm(d)))
    z = (a[0]+t*d[0],a[1]+t*d[1])
    return norm(minus(point,z))


def reconstruct_first():
    assert len(V)==18 and len(set(V))==18
    assert set(CYCLE)==set(range(18))
    assert set(PORTS)==set(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
    assert [norm(minus(V[b],V[a])) for a,b in PORTS]==[1]*17+[3]
    assert Counter(SIGN)==Counter({1:9,-1:8,0:1})
    assert area2(quad((0,0,0,0)))==30
    assert max(norm(minus(a,b)) for a in V for b in V)==67
    assert F(433,250)**2<3 and F(819,100)**2>67
    assert Counter(len(sector(v,(0,0,0,0)))*30 for v in V)==Counter({60:1,90:2,120:1,180:14})
    all_edges=defaultdict(list)
    for i,p in enumerate(FIRST):
        for a,b,port,s in chord_list(p): all_edges[tuple(sorted((a,b)))].append((i,a,b,port,s))
        for q in FIRST[:i]: assert not overlap(quad(p),quad(q))
    outside,contacts=[],[]
    for edge,owners in sorted(all_edges.items()):
        assert len(owners)<=2
        if len(owners)==1:
            i,a,b,port,s=owners[0]
            outside.append((a,b,i,port,s))
        else:
            a,b=owners
            assert a[1:3]==b[2:0:-1] and a[4]+b[4]==0
            contacts.append((edge,owners))
    nxt={}
    for e in outside:
        assert e[0] not in nxt
        nxt[e[0]]=e
    assert set(nxt)=={e[1] for e in outside}
    start=min(nxt);v=start;seen=[]
    while not seen or v!=start:
        assert len(seen)<len(outside)
        seen.append(nxt[v]);v=nxt[v][1]
    assert len(seen)==len(outside)
    root_neighbors=set()
    for _,owners in contacts:
        ids={o[0] for o in owners}
        if 0 in ids: root_neighbors|=ids-{0}
    assert root_neighbors==set(range(1,6))
    for point in V:
        covered=set()
        for p in FIRST:
            new=sector(point,p);assert not covered&new;covered|=new
        assert covered==set(range(12))
        assert not any(segment_contains(a,b,point) for a,b,*_ in outside)
    minimum=None
    edges=list(all_edges)
    for i,(a,b) in enumerate(edges):
        for c,d in edges[:i]:
            if {a,b}&{c,d}: continue
            # Proper crossings must be separately excluded; endpoint
            # distance alone would not detect them.
            x,y=det(minus(b,a),minus(c,a)),det(minus(b,a),minus(d,a))
            z,w=det(minus(d,c),minus(a,c)),det(minus(d,c),minus(b,c))
            assert not (x*y<0 and z*w<0)
            gap=min(distance2(a,c,d),distance2(b,c,d),distance2(c,a,b),distance2(d,a,b))
            assert gap>0
            minimum=gap if minimum is None else min(minimum,gap)
    assert minimum==F(3,4)
    incident=defaultdict(set)
    for a,b in edges:
        incident[a].add(direction_index(a,b));incident[b].add(direction_index(b,a))
    assert all(min((a-b)%12,(b-a)%12)>=1 for rays in incident.values() for a in rays for b in rays if a!=b)
    return seen,{'copies':6,'full_contacts':len(contacts),'exposed_ports':len(outside),
                 'charged_exposed_ports':sum(bool(e[4]) for e in outside),
                 'nonincident_distance_squared':str(minimum),'ray_separation_degrees':30}


def catalog(outside):
    charged=[e for e in outside if e[4]]
    raw=defaultdict(set)
    # Solve ordered endpoint image equations for each of the 12 matrices.
    for target,(a,b,owner,port,state) in enumerate(charged):
        for hand,turn in sorted(MATRICES):
            base=(hand,turn,0,0)
            for x,y,prototype_port,s in chord_list(base):
                if s!=-state or minus(y,x)!=minus(a,b): continue
                t=minus(b,x);raw[(hand,turn,*t)].add(target)
    candidates=[]
    for p,targets in sorted(raw.items()):
        if not any(overlap(quad(p),quad(q),True) for q in FIRST):
            candidates.append((p,tuple(sorted(targets))))
    assert len(raw)==275 and len(candidates)==185
    conflicts=set()
    physical_positive=set()
    plus_edges=defaultdict(list)
    for i,(p,targets) in enumerate(candidates):
        for j,(q,_) in enumerate(candidates[:i]):
            if overlap(quad(p),quad(q),True): conflicts.add((j,i))
        for a,b,port,s in chord_list(p):
            if s==1:
                edge=tuple(sorted((a,b)))
                for j in plus_edges[edge]: physical_positive.add((j,i))
                plus_edges[edge].append(i)
    assert len(conflicts)==3043
    assert len(physical_positive)==1864
    return charged,candidates,conflicts,physical_positive,len(raw)


def audit_cut(row,ids):
    point=tuple(row['point'])
    providers=tuple(map(tuple,row['provider_poses']))
    assert point in {image(v,p) for p in FIRST for v in V}
    assert all(p in ids for p in providers)
    occupied=set();rays=defaultdict(list)
    for p in FIRST+providers:
        new=sector(point,p)
        assert not occupied&new
        occupied|=new
        for a,b,port,s in chord_list(p):
            if a==point: rays[direction_index(a,b)].append(s)
            if b==point: rays[direction_index(b,a)].append(s)
    width=row['angle_degrees']//30;start=row['start_ray'];end=(start+width)%12
    assert width in (1,2)
    assert {(start+j)%12 for j in range(width)}.isdisjoint(occupied)
    assert (start-1)%12 in occupied and end in occupied
    assert len(rays[start])==len(rays[end])==1
    if width==2:
        # Unique 60-degree prototype corner has one + and one - port.
        assert rays[start][0]==rays[end][0] and rays[start][0] in (-1,1)
        adjacent=[SIGN[i] for i,(a,b) in enumerate(PORTS) if 1 in (a,b)]
        assert sorted(adjacent)==[-1,1]
    return tuple(sorted(ids[p] for p in providers))


def direct_search(covers,conflicts,unary):
    """Complete monotone covering search with whole-copy binary conflicts."""
    n=max(i for mask in covers for i in mask)+1
    masks=[sum(1<<i for i in c) for c in covers]
    adjacency=[1<<i for i in range(n)]
    for i,j in conflicts:
        adjacency[i]|=1<<j;adjacency[j]|=1<<i
    coverage=[0]*n
    for j,c in enumerate(covers):
        for i in c: coverage[i]|=1<<j
    allowed=((1<<n)-1)&~sum(1<<i for i in unary)
    all_targets=(1<<len(covers))-1
    calls=0;memo=set()

    def visit(filled,available):
        nonlocal calls
        calls+=1
        if calls>1000000: raise RuntimeError('Complete search guard reached; no negative claim')
        if filled==all_targets: return True
        state=(filled,available)
        if state in memo: return False
        remaining=all_targets^filled
        choices=None
        while remaining:
            bit=remaining&-remaining;j=bit.bit_length()-1;remaining-=bit
            a=masks[j]&available
            if not a: memo.add(state);return False
            if choices is None or a.bit_count()<choices.bit_count(): choices=a
        while choices:
            bit=choices&-choices;i=bit.bit_length()-1;choices-=bit
            if visit(filled|coverage[i],available&~adjacency[i]): return True
        memo.add(state);return False
    answer=visit(0,allowed)
    return answer,{'calls':calls,'failed_states':len(memo)}


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def main():
    assert DATA['amplitude']=='1/100'
    outside,first=reconstruct_first()
    charged,candidates,geometric,positive,raw=catalog(outside)
    ids={p:i for i,(p,_) in enumerate(candidates)}
    cuts=[audit_cut(row,ids) for row in DATA['cuts']]
    assert len(cuts)==len(set(cuts))==15
    unary={x[0] for x in cuts if len(x)==1}
    binary={x for x in cuts if len(x)==2}
    assert all(len(x) in (1,2) for x in cuts)
    conflicts=geometric|positive|binary
    covers=[{i for i,(p,targets) in enumerate(candidates) if target in targets}
            for target in range(len(charged))]
    answer,search=direct_search(covers,conflicts,unary)
    assert not answer
    n=1
    for depth in range(1000):
        cap=(F(22,7)*F(6553,800)**2/F(1299,100)*(depth+1)**2).__floor__()
        if n>cap: break
        n=(9*n+7)//8
    else: raise AssertionError('No finite bound')
    assert depth==86
    result={'agent':'six-heesch-3','role':'researcher','first_corona':first,
            'buffered_overlap_radius_lower':'1/96','profile_displacement_upper':'1/1600',
            'charged_contact_catalog':{'raw':raw,'retained':len(candidates),
                'whole_overlap_pairs':len(geometric),'outward_arc_pairs':len(positive),
                'canonical_sha256':canonical_hash(candidates)},
            'local_cuts':{'count':15,'unary':len(unary),'binary':len(binary),
                'angles':dict(sorted(Counter(x['angle_degrees'] for x in DATA['cuts']).items())),
                'canonical_sha256':canonical_hash(cuts)},
            'direct_complete_search':dict(answer='UNSAT',**search),
            'charge_packing_failure':{'depth':depth,'minimum_copies':n,'maximum_copies':cap},
            'claim':'This fixed first corona admits no finite strict surrounding under any real Euclidean motions; other first coronas remain open.',
            'candidate_written_bound':'1 <= Hc(T) <= Hh(T) <= 85; no exact value or finite-seven claim',
            'trust_boundary':'Written analytic contact, isotopy and finite-angle arguments; exact standard-library checker; no formalization or independent peer-review verdict'}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__': main()
