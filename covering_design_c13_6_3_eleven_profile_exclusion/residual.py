"""Exact residual-cover search for joined point links; no solver."""
from itertools import combinations
from collections import Counter

TRIPLES=tuple(sum(1<<x for x in t) for t in combinations(range(13),3))
TRIPLE_ID={t:i for i,t in enumerate(TRIPLES)}
ALL_BLOCKS=tuple(sum(1<<x for x in t) for t in combinations(range(13),6))
BLOCK_TRIPLES={b:sum(1<<i for i,t in enumerate(TRIPLES) if b&t==t) for b in ALL_BLOCKS}
UNIVERSE=(1<<len(TRIPLES))-1

class Space:
    def __init__(self,p,r):
        self.vertices=tuple(x for x in range(13) if x not in (p,r))
        self.blocks=tuple(sum(1<<x for x in t) for t in combinations(self.vertices,6))
        self.points=tuple(tuple(i for i,x in enumerate(self.vertices) if b>>x&1) for b in self.blocks)
        self.pairs=tuple(sum(1<<x for x in t) for t in combinations(self.vertices,2))
        self.block_pairs=tuple(tuple(i for i,t in enumerate(self.pairs) if b&t==t) for b in self.blocks)
        self.coverage=tuple(BLOCK_TRIPLES[b] for b in self.blocks)
        self.point_inc=tuple(sum(1<<i for i,b in enumerate(self.blocks) if b>>x&1) for x in self.vertices)
        self.pair_inc=tuple(sum(1<<i for i,b in enumerate(self.blocks) if b&t==t) for t in self.pairs)
        self.triple_inc=tuple(sum(1<<i for i,b in enumerate(self.blocks) if b&t==t) for t in TRIPLES)
        self.point_triples=tuple(sum(1<<i for i,t in enumerate(TRIPLES) if t>>p&1) for p in self.vertices)
        self.all=(1<<len(self.blocks))-1

def solve(space,fixed,h,q,total_blocks=20,target_degrees=None,pair_bounds=None):
    k0=total_blocks-len(fixed)
    if target_degrees is None:target_degrees=[11 if x==h else 10 if x==q else 9 for x in range(13)]
    degree=[target_degrees[x]-sum(b>>x&1 for b in fixed) for x in space.vertices]
    cap=[(pair_bounds[t] if pair_bounds is not None else 20 if t==((1<<h)|(1<<q)) else 5)-sum(b&t==t for b in fixed) for t in space.pairs]
    covered=0
    for b in fixed:covered|=BLOCK_TRIPLES[b]
    uncovered=UNIVERSE&~covered
    nodes=0;chosen=[];witness=None;cutoffs=Counter()
    def visit(u,k,domain):
        nonlocal nodes,witness
        nodes+=1
        if any(d<0 or d>k for d in degree):cutoffs['degree']+=1;return False
        if not k:
            if u:return False
            if any(degree):raise ValueError('unexpected degree deficit at full size')
            witness=chosen.copy();return True
        for p,d in enumerate(degree):
            if d==0:domain &= ~space.point_inc[p]
            elif d==k:domain &= space.point_inc[p]
        # Every point needing only one further block must have all its
        # remaining triples in that same block.
        for p,d in enumerate(degree):
            if d!=1:continue
            required=u&space.point_triples[p]
            allowed=domain&space.point_inc[p]
            while required and allowed:
                bit=required&-required;required-=bit
                allowed &= space.triple_inc[bit.bit_length()-1]
            if not allowed:cutoffs['one_block_link']+=1;return False
            domain=(domain&~space.point_inc[p])|allowed
        if not domain:return False
        if domain.bit_count()<k:return False
        for p,d in enumerate(degree):
            if (domain&space.point_inc[p]).bit_count()<d:cutoffs['point_capacity']+=1;return False
        best=None;bits=u
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            options=domain&space.triple_inc[i]
            if not options:cutoffs['uncovered']+=1;return False
            if best is None or options.bit_count()<best.bit_count():best=options
            if best.bit_count()==1:break
        if best is None:
            # A permissive search may cover all triples before the prescribed
            # block count. Continue to enforce exact point degrees and count.
            best=domain
        options=[];bits=best
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            options.append((-(space.coverage[i]&u).bit_count(),i))
        options.sort()
        for _,i in options:
            domain &= ~(1<<i)
            if any(cap[t]<=0 for t in space.block_pairs[i]):continue
            future=domain
            for p in space.points[i]:degree[p]-=1
            for t in space.block_pairs[i]:
                cap[t]-=1
                if cap[t]==0:future &= ~space.pair_inc[t]
            chosen.append(i)
            found=visit(u&~space.coverage[i],k-1,future)
            chosen.pop()
            for t in space.block_pairs[i]:cap[t]+=1
            for p in space.points[i]:degree[p]+=1
            if found:return True
        return False
    domain=space.all
    fixed_set=set(fixed)
    for i,b in enumerate(space.blocks):
        if b in fixed_set:domain &= ~(1<<i)
    for t,c in enumerate(cap):
        if c<0:return dict(status='UNSAT',nodes=0,cutoffs={'initial_pair':1})
        if c==0:domain &= ~space.pair_inc[t]
    for p,d in enumerate(degree):
        if d!=2:continue
        required=uncovered&space.point_triples[p]
        candidates=domain&space.point_inc[p]
        supported=0;bits=candidates
        while bits:
            bit=bits&-bits;bits-=bit;i=bit.bit_length()-1
            missing=required&~space.coverage[i]
            allowed=candidates&~bit
            while missing and allowed:
                t=missing&-missing;missing-=t
                allowed &= space.triple_inc[t.bit_length()-1]
            for x in space.points[i]:
                if degree[x]==1:allowed &= ~space.point_inc[x]
            for t in space.block_pairs[i]:
                if cap[t]==1:allowed &= ~space.pair_inc[t]
            if allowed:supported |= bit|allowed
        if not supported:return dict(status='UNSAT',nodes=0,cutoffs={'two_block_link':1})
        domain=(domain&~space.point_inc[p])|supported
    found=visit(uncovered,k0,domain)
    result=dict(status='SAT' if found else 'UNSAT',nodes=nodes,cutoffs=dict(cutoffs))
    if found:result['witness']=[space.blocks[i] for i in witness]
    return result
