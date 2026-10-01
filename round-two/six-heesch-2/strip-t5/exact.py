"""Solver-free axial-cell geometry and exhaustive rejection-certificate reader.

The producer uses halo/bitset incidence and MRV. Here candidate pools are
rebuilt from direct unit-edge incidence, conflicts from footprint sets,
and inventory branching from the lexicographically first uncovered cell.
All trust-boundary checks remain active under Python -O.
"""
import hashlib
import json

DIRS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(value):
    return hashlib.sha256(json.dumps(value, separators=(',',':'), sort_keys=True).encode()).hexdigest()


def matrices():
    # Choose successive (or preceding) unit-edge directions as the two axes.
    return tuple((DIRS[r][0], DIRS[(r+s)%6][0],
                  DIRS[r][1], DIRS[(r+s)%6][1])
                 for s in (1,-1) for r in range(6))


def affine(cells, g):
    require(len(g)==6 and all(type(v) is int for v in g), 'Invalid affine tuple')
    a,b,c,d,u,v = g
    return tuple(sorted((a*x+b*y+u,c*x+d*y+v) for x,y in cells))


def inverse(g):
    a,b,c,d,u,v = g
    det = a*d-b*c
    require(det in (-1,1), 'Noninvertible grid motion')
    aa,bb,cc,dd = d*det,-b*det,-c*det,a*det
    return aa,bb,cc,dd,-aa*u-bb*v,-cc*u-dd*v


def compose(g,h):
    a,b,c,d,u,v = g
    e,f,j,k,x,y = h
    return a*e+b*j,a*f+b*k,c*e+d*j,c*f+d*k,a*x+b*y+u,c*x+d*y+v


def frame(tile, target):
    target = tuple(sorted(target))
    answers = []
    for m in matrices():
        transformed = affine(tile, m+(0,0))
        u,v = min(transformed)
        x,y = min(target)
        g = m+(x-u,y-v)
        if affine(tile,g)==target:
            answers.append(g)
    require(len(answers)==1, 'The tile must have a unique D6 frame')
    return answers[0]


def halo(cells):
    cells = set(cells)
    return {(x+a,y+b) for x,y in cells for a,b in DIRS}-cells


def touching(a,b):
    b = set(b)
    return any((x+u,y+v) in b for x,y in a for u,v in DIRS)


def raw_contacts(tile):
    """Align opposing unit boundary edges, not cells with a halo mask."""
    root = set(tile)
    boundary = [(p,(a,b)) for p in root for a,b in DIRS
                if (p[0]+a,p[1]+b) not in root]
    orientations = set()
    for m in matrices():
        rotated = affine(tile,m+(0,0))
        x,y = min(rotated)
        orientations.add(tuple((u-x,v-y) for u,v in rotated))
    out = set()
    for oriented in orientations:
        own = set(oriented)
        edges = {(a,b):[p for p in oriented if (p[0]-a,p[1]-b) not in own]
                 for a,b in DIRS}
        for (x,y),(a,b) in boundary:
            for u,v in edges[a,b]:
                t = tuple((s+x+a-u,z+y+b-v) for s,z in oriented)
                if root.isdisjoint(t):
                    out.add(t)
    return tuple(sorted(out))


def pool(tile, fixed, domain):
    occupied = set().union(*(set(t) for t in fixed))
    required = tuple(sorted(halo(occupied)))
    transported = {t:{affine(u,frame(tile,t)) for u in domain} for t in fixed}
    candidates = set().union(*transported.values())
    tiles = tuple(sorted(u for u in candidates if occupied.isdisjoint(u)
                         and any(q in u for q in required)
                         and all(not touching(u,t) or u in transported[t] for t in fixed)))
    return required,tiles


def component(cells, first):
    cells = set(cells)
    require(first in cells, 'Missing component seed')
    reached = {first}
    todo = [first]
    while todo:
        x,y = todo.pop()
        for a,b in DIRS:
            q = x+a,y+b
            if q in cells and q not in reached:
                reached.add(q)
                todo.append(q)
    return reached


def holes(cells):
    cells = set(cells)
    require(bool(cells), 'Empty region')
    lx,hx = min(x for x,y in cells)-1,max(x for x,y in cells)+1
    ly,hy = min(y for x,y in cells)-1,max(y for x,y in cells)+1
    empty = {(x,y) for x in range(lx,hx+1) for y in range(ly,hy+1)}-cells
    return empty-component(empty,(lx,ly))


def coronas(tile, placements, final_holes):
    require(component(tile,min(tile))==set(tile) and not holes(tile), 'Tile is not a disc')
    require(len(set(tile))==len(tile), 'Repeated tile cell')
    copies = []
    levels = []
    occupied = set()
    for row in placements:
        level,g = row['level'],tuple(row['pose'])
        require(type(level) is int and level>=0 and g[:4] in matrices(), 'Bad placement')
        t = affine(tile,g)
        require(occupied.isdisjoint(t), 'Overlapping whole copies')
        occupied.update(t)
        copies.append(t)
        levels.append(level)
    require(levels.count(0)==1 and copies[levels.index(0)]==tile, 'Wrong central tile')
    previous = set()
    result = []
    for k in range(max(levels)+1):
        layer = [t for t,l in zip(copies,levels) if l==k]
        require(bool(layer), 'Missing layer')
        region = previous.union(*(set(t) for t in layer))
        require(component(region,min(region))==region, 'Disconnected prefix')
        missing = holes(region)
        if k<max(levels) or not final_holes:
            require(not missing, 'A required disc prefix has holes')
        if k:
            require(halo(previous)<=region, 'Incomplete corona')
            old = [t for t,l in zip(copies,levels) if l==k-1]
            require(all(any(touching(t,u) for u in old) for t in layer), 'Unattached corona copy')
        result.append({'level':k,'copies':len(layer),'cumulative_cells':len(region),
                       'hole_cells':len(missing)})
        previous = region
    return result


class Instance:
    def __init__(self,tile,required,tiles,domain=None):
        self.tile = tile
        self.required,self.tiles = tuple(required),tuple(tiles)
        self.domain = None if domain is None else set(domain)
        self.sets = [set(t) for t in tiles]
        self.frames = {}
        self.rows = {}
        self.at = [sum(1<<i for i,t in enumerate(self.sets) if q in t) for q in required]
        self.cover = [sum(1<<j for j,q in enumerate(required) if q in t) for t in self.sets]
        require(all(self.cover), 'Useless candidate')
        self.all,self.full = (1<<len(tiles))-1,(1<<len(required))-1

    def inv(self,i):
        if i not in self.frames:
            self.frames[i] = inverse(frame(self.tile,self.tiles[i]))
        return self.frames[i]

    def incompatible(self,i,j):
        if self.sets[i].intersection(self.sets[j]):
            return True
        return self.domain is not None and touching(self.tiles[i],self.sets[j]) and (
            affine(self.tiles[j],self.inv(i)) not in self.domain or
            affine(self.tiles[i],self.inv(j)) not in self.domain)

    def conflict(self,i):
        if i not in self.rows:
            self.rows[i] = sum(1<<j for j in range(len(self.tiles)) if self.incompatible(i,j))
        return self.rows[i]

    def reject(self,proof,forced=None):
        require(proof['pool_sha256']==sha({'required':self.required,'tiles':self.tiles}), 'Wrong pool hash')
        root = (self.all,self.full) if forced is None else (
            self.all&~self.conflict(forced),self.full&~self.cover[forced])
        require(tuple(int(s,16) for s in proof['root'])==root, 'Wrong rejection root')
        nodes = [(int(a,16),int(r,16),j) for a,r,j in proof['nodes']]
        require(len({(a,r) for a,r,j in nodes})==len(nodes), 'Repeated rejection state')
        valid = set()
        for available,remaining,j in sorted(nodes,key=lambda n:(n[1].bit_count(),n)):
            require(remaining and not (available&~self.all) and not (remaining&~self.full), 'Invalid state masks')
            require(type(j) is int and 0<=j<len(self.required) and (remaining>>j)&1, 'Invalid split')
            choices = self.at[j]&available
            while choices:
                bit = choices&-choices
                choices ^= bit
                i = bit.bit_length()-1
                child = available&~self.conflict(i),remaining&~self.cover[i]
                require(child in valid, 'Uncertified exhaustive branch')
            valid.add((available,remaining))
        require(root in valid, 'Missing certified root')
        return len(nodes)


def enumerate_stars(tile,domain,node_guard=100000):
    instance = Instance(tile,tuple(sorted(halo(tile))),tuple(sorted(domain)),domain)
    stars = set()
    nodes = 0
    def visit(chosen,remaining,available):
        nonlocal nodes
        nodes += 1
        require(nodes<=node_guard, 'Incomplete inventory: node guard')
        if not remaining:
            stars.add(tuple(sorted(chosen)))
            return
        j = (remaining&-remaining).bit_length()-1
        choices = instance.at[j]&available
        while choices:
            bit = choices&-choices
            choices ^= bit
            i = bit.bit_length()-1
            visit(chosen+(i,),remaining&~instance.cover[i],available&~instance.conflict(i))
    visit((),instance.full,instance.all)
    return tuple(sorted(tuple(instance.tiles[i] for i in ids) for ids in stars)),nodes
