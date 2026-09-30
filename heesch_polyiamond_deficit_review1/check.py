"""six-reviewer-1: independent centroid geometry and direct finite packing.

Only Python's standard library. No author code, SAT solver or cardinality encoder.
Faces are represented by three times their centroids, not vertex triples.
Search limits raise an exception; an interrupted search proves nothing.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time

BASE = Path(__file__).resolve().parent
IDENTITY = (1, 0, 0, 1, 0, 0)
DIR = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def norm(v):
    x, y = v
    return x*x+x*y+y*y

def vertices(f):
    sx, sy = f
    r = sx % 3
    require(r == sy % 3 and r in (1, 2), ('invalid face', f))
    x, y = (sx-r)//3, (sy-r)//3
    if r == 1:
        return ((x, y), (x+1, y), (x, y+1))
    return ((x+1, y+1), (x, y+1), (x+1, y))

def triangle(vs):
    require(len(set(vs)) == 3 and all(norm((u[0]-v[0],u[1]-v[1])) == 1
            for u, v in combinations(vs, 2)), ('non-unit triangle', vs))
    f = (sum(v[0] for v in vs), sum(v[1] for v in vs))
    require(set(vertices(f)) == set(vs), 'face decoder mismatch')
    return f

def point(p, v):
    a,b,c,d,x,y = p
    return (a*v[0]+b*v[1]+x, c*v[0]+d*v[1]+y)

def face(p, f):
    a,b,c,d,x,y = p
    return (a*f[0]+b*f[1]+3*x, c*f[0]+d*f[1]+3*y)

def compose(p, q):
    a,b,c,d,x,y = p; e,f,g,h,u,v = q
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h,a*u+b*v+x,c*u+d*v+y)

def inverse(p):
    a,b,c,d,x,y = p; z = a*d-b*c
    require(abs(z) == 1, 'nonunimodular pose')
    q = (d//z,-b//z,-c//z,a//z,0,0)
    u,v = point(q, (-x,-y))
    out = q[:4]+(u,v)
    require(compose(p,out) == compose(out,p) == IDENTITY, 'inverse mismatch')
    return out

def matrices():
    unit = [(x,y) for x in range(-1,2) for y in range(-1,2) if norm((x,y)) == 1]
    out = sorted((a,b,c,d) for a,c in unit for b,d in unit
                 if 2*a*b+a*d+b*c+2*c*d == 1)
    require(len(out) == 12, 'Gram isometry census')
    return out

@lru_cache(maxsize=None)
def star(v):
    x,y = v
    return tuple(triangle((v,(x+DIR[j][0],y+DIR[j][1]),
                          (x+DIR[(j+1)%6][0],y+DIR[(j+1)%6][1]))) for j in range(6))

def mesh(fs):
    edges = defaultdict(list); vs = set()
    for f in fs:
        tri = vertices(f); vs.update(tri)
        for e in combinations(tri,2):
            edges[tuple(sorted(e))].append(f)
    require(all(len(rows) in (1,2) for rows in edges.values()), 'nonmanifold edge')
    boundary = defaultdict(set); adjacent = defaultdict(set)
    for e, rows in edges.items():
        if len(rows) == 1:
            u,v = e; boundary[u].add(v); boundary[v].add(u)
        else:
            u,v = rows; adjacent[u].add(v); adjacent[v].add(u)
    seen = set(); todo = [next(iter(fs))]
    while todo:
        f = todo.pop()
        if f not in seen:
            seen.add(f); todo.extend(adjacent[f]-seen)
    require(seen == fs, 'not edge connected')
    for v in vs:
        link = [f in fs for f in star(v)]
        transitions = sum(link[j] != link[(j+1)%6] for j in range(6))
        require(transitions in (0,2), ('pinched vertex',v))
    require(boundary and all(len(row)==2 for row in boundary.values()), 'boundary degree')
    seen = set(); todo = [next(iter(boundary))]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v); todo.extend(boundary[v]-seen)
    require(seen == set(boundary), 'multiple boundary components')
    chi = len(vs)-len(edges)+len(fs)
    require(chi == 1, 'Euler characteristic not one')
    return {'faces':len(fs),'vertices':len(vs),'edges':len(edges),'chi':chi,
            'boundary_vertices':len(boundary)},vs

def shape(signs):
    def rot(v):
        x,y = v; return (-y,x+y)
    fs = set()
    for t in range(4):
        center = (3*t,3*t)
        for x in range(-3,4):
            for y in range(-3,4):
                for r in (1,2):
                    f = (3*x+r,3*y+r)
                    if all(max(abs(u),abs(v),abs(u+v)) <= 3 for u,v in vertices(f)):
                        fs.add((f[0]+3*center[0],f[1]+3*center[1]))
    require(len(fs)==216, 'base hexagon count')
    ports = sorted(((i,0),(i+dx,dy)) for i in range(4) for dx,dy in DIR
                   if (i+dx,dy) not in {(j,0) for j in range(4)})
    require(len(ports)==len(signs)==18 and Counter(signs)=={1:9,-1:8,0:1}, 'sign table')
    for (center,neighbor),sign in zip(ports,signs):
        if not sign:
            continue
        turns = DIR.index((neighbor[0]-center[0],neighbor[1]-center[1]))
        feature = (vertices((1,7)),vertices((7,1)))
        if sign == -1:
            feature = [tuple((3-y,3-x) for x,y in tri) for tri in feature]
        for tri in feature:
            for _ in range(turns):
                tri = tuple(rot(v) for v in tri)
            cx,cy = center; shift = (3*(cx-cy),3*(cx+2*cy))
            f = triangle(tuple((x+shift[0],y+shift[1]) for x,y in tri))
            require((f in fs) == (sign==1), 'feature add/remove overlap')
            if sign == 1:
                fs.remove(f)
            else:
                fs.add(f)
    require(len(fs)==214, 'tile size')
    return frozenset(fs)

def lower(fs, placements):
    occupied = set(); layers = [set() for _ in range(6)]; feet = []
    ms = set(matrices()); counts = Counter()
    for p in placements:
        level = p['level']; q = tuple(p['matrix']+p['translation'])
        require(type(level) is int and level in range(6) and
                all(type(x) is int for x in q) and q[:4] in ms, 'pose encoding')
        f = {face(q,t) for t in fs}
        require(len(f)==214 and not occupied & f, 'copy footprint overlap')
        if level==0:
            require(q==IDENTITY, 'root pose')
        occupied.update(f);layers[level].update(f); feet.append((level,f));counts[level]+=1
    require([counts[i] for i in range(6)]==[1,5,11,23,39,52], 'layer counts')
    prefixes = []; rows=[]; occupied=set()
    layer_vs = [{v for f in layer for v in vertices(f)} for layer in layers]
    for level in range(6):
        occupied |= layers[level]; prefixes.append(set(occupied))
        row,vs = mesh(occupied); row['level']=level
        if level<5:
            nxt = occupied | layers[level+1]
            require(all(set(star(v)) <= nxt for v in vs), 'unfilled prefix vertex')
        rows.append(row)
    for level,f in feet:
        if level:
            require(any(v in layer_vs[level-1] for t in f for v in vertices(t)), 'missing layer contact')
    return rows

class Geometry:
    def __init__(self,fs):
        self.fs = fs
        self.vs = {v for f in fs for v in vertices(f)}
        self.angles = {v:sum(f in fs for f in star(v)) for v in self.vs}
        self.tips = sorted(v for v,a in self.angles.items() if a==1)
        self.corners = sorted(v for v,a in self.angles.items() if a in (4,5))
        self.pockets = sorted(v for v,a in self.angles.items() if a==5)
        self.ms = matrices()

    @lru_cache(maxsize=4000)
    def footprint(self,p):
        return frozenset(face(p,f) for f in self.fs)

    def anchor_pool(self, corners):
        # Enumerate all 12 Gram-preserving integral linear maps of any tile
        # face onto any missing face. A centroid congruence determines shift.
        gaps = set().union(*(set(star(v))-self.fs for v in corners))
        candidates = set()
        for m in self.ms:
            for f in self.fs:
                u,v = face(m+(0,0),f)
                for x,y in gaps:
                    if (x-u)%3==0 and (y-v)%3==0:
                        candidates.add(m+((x-u)//3,(y-v)//3))
        out = sorted(p for p in candidates if not self.fs & self.footprint(p))
        return out, len(candidates), len(gaps)

    def union(self,fixed):
        occupied = set()
        for p in fixed:
            f = self.footprint(p)
            require(not occupied & f, 'overlapping fixed copies')
            occupied.update(f)
        return occupied

    def local_pool(self,fixed,raw):
        occupied = self.union(fixed)
        keys = {compose(p,q) for p in fixed for q in raw}-set(fixed)
        poses = sorted(p for p in keys if not occupied & self.footprint(p))
        return poses, [self.footprint(p) for p in poses], occupied

    def bad(self,p,q,excluded):
        return compose(inverse(p),q) in excluded or compose(inverse(q),p) in excluded

def conflict_masks(feet):
    owners = defaultdict(list); masks = [1<<i for i in range(len(feet))]
    pairs = set()
    for j,f in enumerate(feet):
        for t in f:
            for k in owners[t]:
                masks[j] |= 1<<k; masks[k] |= 1<<j; pairs.add((j,k))
            owners[t].append(j)
    return masks, pairs

class SearchLimit(RuntimeError):
    pass

class Search:
    def __init__(self,seconds=40,nodes=200000):
        self.deadline = time.monotonic()+seconds; self.limit=nodes;self.nodes=0
    def tick(self):
        self.nodes+=1
        if self.nodes>self.limit or (self.nodes%256==0 and time.monotonic()>self.deadline):
            raise SearchLimit('incomplete direct search; no exclusion established')

def cover_search(feet,missing):
    conflicts,_ = conflict_masks(feet)
    missing = sorted(missing); index = {f:i for i,f in enumerate(missing)}
    covers = [sum(1<<index[f] for f in foot if f in index) for foot in feet]
    owners = [sum(1<<j for j,c in enumerate(covers) if c>>i&1) for i in range(len(missing))]
    search = Search(); memo=set()
    def dfs(available,needed):
        search.tick()
        if needed==0:
            return True
        state=(available,needed)
        if state in memo:
            return False
        choices=None; scan=needed
        while scan:
            bit=scan&-scan; scan-=bit; i=bit.bit_length()-1
            pool=available & owners[i]
            if pool==0:
                memo.add(state);return False
            if choices is None or pool.bit_count()<choices.bit_count():
                choices=pool
        while choices:
            bit=choices&-choices; choices-=bit; j=bit.bit_length()-1
            if dfs(available & ~conflicts[j],needed & ~covers[j]):
                return True
            # Later branches need not revisit packings containing this pose.
            available &= ~bit
        memo.add(state);return False
    answer=dfs((1<<len(feet))-1,(1<<len(missing))-1)
    return answer, search.nodes

def geometry_negative(g,fixed,wide):
    poses,feet,occupied = g.local_pool(fixed,wide)
    missing = set().union(*(set(star(point(p,v)))-occupied for p in fixed for v in g.corners))
    answer,nodes = cover_search(feet,missing)
    require(answer is False, 'claimed geometric exclusion has a completion')
    empty = sorted(missing-set().union(*feet))
    return {'poses':len(poses),'missing_faces':len(missing),'nodes':nodes,
            'empty_face':list(empty[0]) if empty else None}

def incoming_model(g,fixed,incoming,excluded):
    poses,feet,occupied = g.local_pool(fixed,incoming)
    conflicts,_ = conflict_masks(feet)
    available=(1<<len(poses))-1
    for i,p in enumerate(poses):
        if any(g.bad(p,q,excluded) for q in fixed):
            available &= ~(1<<i)
        for j,q in enumerate(poses[:i]):
            if g.bad(p,q,excluded):
                conflicts[i] |= 1<<j; conflicts[j] |= 1<<i
    require(not any(g.bad(p,q,excluded) for i,p in enumerate(fixed) for q in fixed[:i]), 'bad fixed pair')
    fixedfeet=[g.footprint(p) for p in fixed]
    covers=[[0]*len(fixed) for _ in poses]; auto=[]
    for k,p in enumerate(fixed):
        aut=0
        for j,v in enumerate(g.tips):
            gap=set(star(point(p,v)))-fixedfeet[k]
            require(len(gap)==5, 'tip gap')
            if any(gap <= f for i,f in enumerate(fixedfeet) if i!=k):
                aut |= 1<<j
            for i,f in enumerate(feet):
                if gap <= f:
                    covers[i][k] |= 1<<j
        auto.append(aut)
    return poses,conflicts,available,covers,auto

def charge_search(model,bound,cuts):
    poses,conflicts,available,covers,auto=model
    cuts=[sum(1<<(i-1) for i in cut) for cut in cuts]
    require(all(cut and cut>>len(poses)==0 for cut in cuts), 'bad cut index')
    search=Search(); witness=[]
    def dfs(left,selected,covered):
        search.tick()
        if any(selected & cut == cut for cut in cuts):
            return False
        if all(c.bit_count()>=bound for c in covered):
            witness.append(selected);return True
        # Exact optimistic coverage: no compatibility assumption is needed.
        optimistic=list(covered);scan=left
        while scan:
            bit=scan&-scan;scan-=bit;i=bit.bit_length()-1
            for k,c in enumerate(covers[i]):
                optimistic[k] |= c
        if any(c.bit_count()<bound for c in optimistic):
            return False
        # Select the pose with greatest new coverage in unsatisfied rows.
        best=None;scan=left
        while scan:
            bit=scan&-scan;scan-=bit;i=bit.bit_length()-1
            score=sum((c & ~covered[k]).bit_count() for k,c in enumerate(covers[i])
                      if covered[k].bit_count()<bound)
            if best is None or score>best[0]:
                best=(score,i)
        require(best is not None, 'empty available after optimism')
        _,i=best;bit=1<<i
        if dfs(left & ~conflicts[i],selected|bit,[a|b for a,b in zip(covered,covers[i])]):
            return True
        return dfs(left & ~bit,selected,covered)
    answer=dfs(available,0,auto)
    return answer,search.nodes,([] if not witness else [i+1 for i in range(len(poses)) if witness[0]>>i&1])

def outdegree(g,narrow,admitted,excluded):
    poses=[p for i,p in enumerate(narrow,1) if i in admitted]
    feet=[g.footprint(p) for p in poses]
    # Independent complete quadruple census, with direct set intersections.
    # Any four compatible recipients would form an unblocked quadruple.
    blocked={}
    for i,j in combinations(range(len(poses)),2):
        blocked[i,j]=bool(feet[i]&feet[j]) or g.bad(poses[i],poses[j],excluded)
    checked=0
    for quadruple in combinations(range(len(poses)),4):
        require(any(blocked[i,j] for i,j in combinations(quadruple,2)),
                ('four compatible recipients',quadruple))
        checked+=1
    triples=[triple for triple in combinations(range(len(poses)),3)
             if not any(blocked[i,j] for i,j in combinations(triple,2))]
    require(checked==5985 and triples,'complete quadruple census')
    witness=triples[0]
    indices=sorted(admitted)
    return {'max_compatible_recipients':3,'checked_quadruples':checked,
            'compatible_triples':len(triples),
            'witness_attachment_indices':[indices[i] for i in witness],
            'blocked_pairs':sum(blocked.values()),'assignment_multiplicity':4}

def arithmetic(g):
    diameter = max(norm((u[0]-v[0],u[1]-v[1])) for u,v in combinations(g.vs,2))
    require(diameter==448,'exact diameter')
    # A containing regular hexagon with apothem D(K+1) has area
    # 2 sqrt(3) D^2 (K+1)^2. Tile area is 214 sqrt(3)/4.
    rows=[];n=1
    for k in range(1400):
        left=214*n;right=8*diameter*(k+1)**2
        rows.append((k,n,left,right))
        if left>right:
            break
        n=(33*n+31)//32
    require(rows[-1][0]==384 and all(a<=b for _,_,a,b in rows[:-1]),'rounded area threshold')
    require(214*73**1314 <= 16*24**2*1315**2*72**1314 and
            214*73**1315 > 16*24**2*1316**2*72**1315,'author area threshold')
    return {'exact_diameter_squared':diameter,'growth_ratio':[33,32],
            'rounded_first_failure':list(rows[-1]),'previous':list(rows[-2]),
            'finite_upper':385,'checked_depths':len(rows)}

def controls(g,data,incoming,excluded):
    # Directly validate returned positive assignments from the root relaxation.
    root=incoming_model(g,[IDENTITY],incoming,excluded)
    yes,nodes,witness=charge_search(root,8,[])
    require(yes and witness,'threshold-eight relaxation positive control')
    selected=[i-1 for i in witness]
    require(all(not root[1][i]>>j&1 for i in selected for j in selected if i!=j), 'invalid positive footprint')
    covered=0
    for i in selected:
        covered |= root[3][i][0]
    require(covered.bit_count()>=8,'invalid positive charge count')
    reject=[]
    def bad(name,fn):
        try:
            fn()
        except (ValueError,SearchLimit):
            reject.append(name)
        else:
            raise ValueError(('mutation escaped',name))
    placements=[dict(p) for p in data['placements']]
    placements[1]=dict(placements[0],level=5)
    bad('overlapping corona copy',lambda:lower(g.fs,placements))
    placements=[dict(p) for p in data['placements'] if p['level']!=5]
    bad('deleted fifth corona',lambda:lower(g.fs,placements))
    placements=[dict(p) for p in data['placements']]
    placements[1]=dict(placements[1],matrix=[1,1,0,1])
    bad('nonisometric shear',lambda:lower(g.fs,placements))
    bad('invalid face centroid',lambda:vertices((0,0)))
    limited=Search(nodes=0)
    bad('incomplete enumeration',limited.tick)
    # A small definition-level search control detects overlap pruning errors.
    feet=[{(0,0),(1,0)},{(1,0),(2,0)}]
    require(cover_search(feet,{(0,0),(2,0)})[0] is False,'conflict control')
    require(cover_search([{(0,0)},{(2,0)}],{(0,0),(2,0)})[0] is True,'cover positive control')
    return {'positive_root_eight':witness,'positive_charge_count':covered.bit_count(),
            'positive_nodes':nodes,'rejected_mutations':reject,'cover_controls':2}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=['lower','pairs','deficit','controls','arithmetic','all'],default='all')
    parser.add_argument('--output',type=Path);parser.add_argument('--expected',type=Path)
    args=parser.parse_args();start=time.monotonic()
    data=json.loads((BASE/'input.json').read_text());fs=shape(data['side_signs']);g=Geometry(fs)
    input_digest=hashlib.sha256((BASE/'input.json').read_bytes()).hexdigest()
    require(input_digest=='158e3ad324a15e47c956813e9813600b3908c339649a4cafd826f0dc51cc7cc0','input digest')
    canonical=json.dumps({'triangles':sorted(tuple(sorted(vertices(f))) for f in fs)},separators=(',',':'))+'\n'
    digest=hashlib.sha256(canonical.encode()).hexdigest()
    require(digest=='8d42c74f1e219ae37f34d5706f83ab4eb20e921ada66d70090c8a539f481335f','tile digest')
    report={'agent':'six-reviewer-1','role':'independent mathematical reviewer','shape_sha256':digest,'input_sha256':input_digest,
            'angles':dict(sorted(Counter(a*60 for a in g.angles.values() if a<6).items()))}
    narrow,ncand,ngap=g.anchor_pool(g.pockets);wide,wcand,wgap=g.anchor_pool(g.corners)
    require(len(narrow)==59 and len(wide)==475 and set(narrow)<=set(wide), 'corner pool census')
    report['pools']={'narrow':59,'wide':475,'narrow_anchors':ncand,'wide_anchors':wcand,'missing_faces':wgap}
    report['pools']['narrow_sha256']=hashlib.sha256(json.dumps(narrow,separators=(',',':')).encode()).hexdigest()
    report['pools']['wide_sha256']=hashlib.sha256(json.dumps(wide,separators=(',',':')).encode()).hexdigest()
    if args.phase in ('lower','all'):
        report['lower']=lower(fs,data['placements'])
        report['arithmetic']=arithmetic(g)
    admitted=set(data['retained_indices']);excluded={p for i,p in enumerate(narrow,1) if i not in admitted}
    incoming=sorted(inverse(p) for i,p in enumerate(narrow,1) if i in admitted)
    require(len(incoming)==21,'incoming pool')
    if args.phase in ('arithmetic','all'):
        report['outdegree']=outdegree(g,narrow,admitted,excluded)
        report['arithmetic']=arithmetic(g)
    if args.phase in ('pairs','all'):
        report['pair_exclusions']=[]
        for i,p in enumerate(narrow,1):
            if i not in admitted:
                row=geometry_negative(g,[IDENTITY,p],wide);row['attachment']=i
                report['pair_exclusions'].append(row)
                print('pair',i,row,flush=True)
    if args.phase in ('deficit','all'):
        root=incoming_model(g,[IDENTITY],incoming,excluded)
        require(root[0]==incoming,'incoming root indexing')
        ans,nodes,witness=charge_search(root,9,[]);require(ans is False,'capacity nine SAT')
        report['capacity_nine']={'nodes':nodes}
        report['conditional_cases']=[]
        for case in data['saturation_cases']:
            fixed=[IDENTITY]+[incoming[i-1] for i in case['providers']]
            model=incoming_model(g,fixed,incoming,excluded);deep=[]
            for cut in case['deep_cuts']:
                row=geometry_negative(g,fixed+[model[0][i-1] for i in cut],wide)
                row['providers']=cut;deep.append(row);print('deep',case['providers'],cut,row,flush=True)
            ans,nodes,witness=charge_search(model,8,case['deep_cuts'])
            require(ans is False, ('conditional saturation has completion',witness))
            report['conditional_cases'].append({'root_providers':case['providers'],'poses':len(model[0]),'deep':deep,'nodes':nodes})
        cuts=[case['providers'] for case in data['saturation_cases']]
        ans,nodes,witness=charge_search(root,8,cuts);require(ans is False,('forced deficit has completion',witness))
        report['forced_deficit']={'nodes':nodes}
    if args.phase in ('controls','all'):
        report['controls']=controls(g,data,incoming,excluded)
    if args.expected:
        expected=json.loads(args.expected.read_text())
        normalized=json.loads(json.dumps(report))
        require(normalized==expected,('deterministic expected-result mismatch',
                [k for k in set(normalized)|set(expected) if normalized.get(k)!=expected.get(k)]))
    report['elapsed_seconds']=time.monotonic()-start;report['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    text=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text)

if __name__=='__main__':
    main()
