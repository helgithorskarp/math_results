"""Independent integer geometry, corner replay and lazy cover enumeration.

Discovery aligned tile pixels with halo pixels, built every conflict row and
branched on a minimum-owner target. This reader transports the complete
allowed contact domain, constructs conflict rows through cell incidence only
when needed and branches on the first uncovered target. All arithmetic is
integer. Guards raise exceptions, never reject a mathematical configuration.
"""
from collections import defaultdict, deque
from itertools import product

QUADRANTS=((0,0),(-1,0),(-1,-1),(0,-1))
FOUR=((1,0),(-1,0),(0,1),(0,-1))


def require(ok,message):
    if not ok:raise ValueError(message)


def halo(cs):
    return {(x+dx,y+dy) for x,y in cs for dx,dy in product((-1,0,1),repeat=2)}-set(cs)


def image(cs,g):
    a,b,c,d=g
    raw=[(a*x+b*y+min(a,b,0),c*x+d*y+min(c,d,0)) for x,y in cs]
    lo=min(x for x,y in raw),min(y for x,y in raw)
    return tuple(sorted((x-lo[0],y-lo[1]) for x,y in raw)),lo


def mv(g,p):
    a,b,c,d=g;x,y=p
    return a*x+b*y,c*x+d*y


def flood(cs,start):
    queue=deque([start]);seen={start}
    while queue:
        x,y=queue.popleft()
        for dx,dy in FOUR:
            q=x+dx,y+dy
            if q in cs and q not in seen:seen.add(q);queue.append(q)
    return seen


def disc(cs):
    cs=set(cs)
    if not cs or flood(cs,min(cs))!=cs:return False
    vertices={(x+dx,y+dy) for x,y in cs for dx,dy in product((0,1),repeat=2)}
    for x,y in vertices:
        bits=[(x+dx,y+dy) in cs for dx,dy in QUADRANTS]
        if sum(bits)==2 and bits[0]==bits[2]:return False
    xmin=min(x for x,y in cs)-1;xmax=max(x for x,y in cs)+1
    ymin=min(y for x,y in cs)-1;ymax=max(y for x,y in cs)+1
    empty={(x,y) for x in range(xmin,xmax+1) for y in range(ymin,ymax+1)}-cs
    return flood(empty,(xmin,ymin))==empty


class Geometry:
    def __init__(self,raw):
        cells=tuple(sorted(map(tuple,raw)))
        require(cells and len(cells)==len(set(cells)) and all(len(p)==2 and all(type(z) is int for z in p) for p in cells),'invalid prototype')
        require(min(x for x,y in cells)==min(y for x,y in cells)==0 and disc(cells),'unnormalized or nondisc prototype')
        self.cells=cells
        matrices=tuple(g for g in product((-1,0,1),repeat=4) if g[0]**2+g[1]**2==g[2]**2+g[3]**2==1 and g[0]*g[2]+g[1]*g[3]==0)
        self.shapes=tuple(sorted({image(cells,g)[0] for g in matrices}))
        self.indices={s:i for i,s in enumerate(self.shapes)}
        self.root=(self.indices[cells],0,0)
        self.frames=[]
        for shape in self.shapes:
            frames=[(g,(-lo[0],-lo[1])) for g in matrices for s,lo in [image(cells,g)] if s==shape]
            require(len(frames)==1,'prototype stabilizer is not trivial')
            self.frames.append(frames[0])
        self.relative_cache={}
        for ao,(g,b) in enumerate(self.frames):
            a,e,c,d=g;gi=(a,c,e,d);gb=mv(gi,b)
            for bo,shape in enumerate(self.shapes):
                im,lo=image(shape,gi)
                self.relative_cache[ao,bo]=(gi,self.indices[im],(lo[0]-gb[0],lo[1]-gb[1]))
        self.integer_contacts=self.contact_inventory()

    def pixels(self,p):
        require(len(p)==3 and all(type(z) is int for z in p) and 0<=p[0]<len(self.shapes),'invalid pose')
        o,x,y=p
        return frozenset((a+x,b+y) for a,b in self.shapes[o])

    def union(self,poses):
        occupied=set()
        for p in poses:
            fp=self.pixels(p);require(not fp&occupied,'whole-copy overlap')
            occupied.update(fp)
        return occupied

    def relative(self,a,b):
        g,o,offset=self.relative_cache[a[0],b[0]]
        x,y=mv(g,(b[1]-a[1],b[2]-a[2]))
        return o,x+offset[0],y+offset[1]

    def transport(self,a,t):
        g,b=self.frames[a[0]]
        shape,lo=image(self.shapes[t[0]],g)
        x,y=mv(g,(t[1],t[2]))
        return self.indices[shape],a[1]+b[0]+lo[0]+x,a[2]+b[1]+lo[1]+y

    def contact_inventory(self):
        root=set(self.cells);hh=halo(root);result=set()
        w=max(x for x,y in root)+1;h=max(y for x,y in root)+1
        for o,shape in enumerate(self.shapes):
            ow=max(x for x,y in shape)+1;oh=max(y for x,y in shape)+1
            for x in range(-ow,w+1):
                for y in range(-oh,h+1):
                    p=o,x,y;fp=self.pixels(p)
                    if not fp&root and fp&hh:result.add(p)
        return result

    def corner(self,fixed,certificate):
        occupied=self.union(fixed)
        original={(x+dx,y+dy) for x,y in occupied for dx,dy in product((0,1),repeat=2)}
        def choices(vertex,quadrant):
            require(vertex in original,'new forced-copy vertex improperly required interior')
            qs=[(vertex[0]+dx,vertex[1]+dy) for dx,dy in QUADRANTS]
            require(0<=quadrant<4 and qs[quadrant] not in occupied and qs[(quadrant-1)%4] in occupied and qs[(quadrant+1)%4] in occupied,'not an isolated empty90-degree sector')
            ux,uy=qs[quadrant];feasible=[]
            for o,shape in enumerate(self.shapes):
                for x,y in shape:
                    pose=(o,ux-x,uy-y);fp=self.pixels(pose)
                    if not fp&occupied:feasible.append((pose,fp))
            return feasible
        for step in certificate['steps']:
            require(len(step)==6 and all(type(z) is int for z in step),'malformed corner step')
            x,y,q,o,tx,ty=step
            feasible=choices((x,y),q)
            require(len(feasible)==1 and feasible[0][0]==(o,tx,ty),'unproved corner force')
            occupied.update(feasible[0][1])
        last=certificate['empty']
        require(len(last)==3 and all(type(z) is int for z in last),'malformed empty-corner conclusion')
        require(not choices(tuple(last[:2]),last[2]),'empty corner has a feasible whole-copy pose')
        return len(certificate['steps'])


class Cover:
    def __init__(self,geometry,fixed,bad):
        self.g=geometry;self.bad=bad
        self.old=geometry.union(fixed);target=halo(self.old)
        allowed=geometry.integer_contacts-bad
        require(all(geometry.relative(p,geometry.root) in allowed for p in allowed),'domain is not reciprocal')
        fixed_pixels=[geometry.pixels(p) for p in fixed]
        fixed_halos=[halo(fp) for fp in fixed_pixels]
        for i,a in enumerate(fixed):
            for j,b in enumerate(fixed[:i]):
                require(not fixed_pixels[i]&fixed_pixels[j],'fixed overlap')
                require(not fixed_pixels[i]&fixed_halos[j] or geometry.relative(a,b) not in bad,'fixed forbidden pair')
        raw={geometry.transport(a,t) for a in fixed for t in allowed}
        candidates=[]
        for p in sorted(raw):
            fp=geometry.pixels(p)
            if fp&self.old or not fp&target:continue
            if any(fp&hh and geometry.relative(a,p) in bad for a,hh in zip(fixed,fixed_halos)):continue
            candidates.append((p,fp))
        require(len(candidates)<=2000,'candidate guard; incomplete verification')
        self.pool=candidates;self.target=sorted(target)
        index={q:i for i,q in enumerate(self.target)}
        self.covers=[];self.owners=[0]*len(index);self.incidence=defaultdict(set)
        for i,(p,fp) in enumerate(candidates):
            covered=0
            for q in fp:
                self.incidence[q].add(i)
                if q in index:
                    covered|=1<<index[q];self.owners[index[q]]|=1<<i
            require(covered,'redundant candidate')
            self.covers.append(covered)
        self.conflict_cache={}

    def conflicts(self,i):
        if i in self.conflict_cache:return self.conflict_cache[i]
        pose,fp=self.pool[i];overlap={i};touch=set()
        for q in fp:overlap.update(self.incidence[q])
        for q in halo(fp):touch.update(self.incidence[q])
        overlap.update(j for j in touch-overlap if self.g.relative(pose,self.pool[j][0]) in self.bad)
        mask=sum(1<<j for j in overlap);self.conflict_cache[i]=mask
        return mask

    def enumerate(self,first_only=False):
        failed=set();answers=set();self.nodes=0
        def visit(remaining,available,selected):
            self.nodes+=1
            require(self.nodes<=100000,'search-node guard; incomplete verification')
            if not remaining:
                answers.add(tuple(sorted(self.pool[i][0] for i in selected)));return True
            key=remaining,available
            if key in failed:return False
            # Independent first-uncovered ordering, rather than discovery MRV.
            k=(remaining&-remaining).bit_length()-1
            possible=self.owners[k]&available;positive=False
            while possible:
                bit=possible&-possible;possible-=bit;i=bit.bit_length()-1
                yes=visit(remaining&~self.covers[i],available&~self.conflicts(i),selected+(i,))
                positive=yes or positive
                if yes and first_only:return True
            if not positive:failed.add(key)
            return positive
        visit((1<<len(self.owners))-1,(1<<len(self.pool))-1,())
        return answers

    def accepts(self,poses):
        bypose={p:fp for p,fp in self.pool}
        require(all(p in bypose for p in poses),'positive cover has a missing candidate')
        occupied=set(self.old)
        for p in poses:
            require(not occupied&bypose[p],'positive cover overlap')
            occupied.update(bypose[p])
        require(set(self.target)<=occupied,'positive cover misses a required halo cell')
        for i,a in enumerate(poses):
            for b in poses[:i]:
                if self.g.pixels(a)&halo(self.g.pixels(b)):
                    require(self.g.relative(a,b) not in self.bad,'positive cover has a forbidden pair')
        return True
