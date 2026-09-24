"""Independent proof search branching on complete remaining point stars."""
from itertools import combinations

class Space:
    def __init__(self,p,r):
        self.vertices=tuple(x for x in range(13) if x not in (p,r))
        self.triples=tuple(sum(1<<x for x in t) for t in combinations(range(13),3))
        self.pairs=tuple(sum(1<<x for x in t) for t in combinations(self.vertices,2))
        self.blocks=tuple(sum(1<<x for x in t) for t in combinations(self.vertices,6))
        self.member=tuple(tuple(j for j,x in enumerate(self.vertices) if b>>x&1) for b in self.blocks)
        self.pair_member=tuple(tuple(j for j,t in enumerate(self.pairs) if b&t==t) for b in self.blocks)
        self.cover=tuple(sum(1<<j for j,t in enumerate(self.triples) if b&t==t) for b in self.blocks)
        self.through=tuple(sum(1<<i for i,b in enumerate(self.blocks) if b>>p&1) for p in self.vertices)
        self.through_pair=tuple(sum(1<<i for i,b in enumerate(self.blocks) if b&t==t) for t in self.pairs)
        self.through_triple=tuple(sum(1<<i for i,b in enumerate(self.blocks) if b&t==t) for t in self.triples)
        self.star=tuple(sum(1<<j for j,t in enumerate(self.triples) if t>>p&1) for p in self.vertices)

def indices(bits):
    while bits:
        bit=bits&-bits;bits-=bit
        yield bit.bit_length()-1

def solve(space,fixed,h,q,total_blocks=20,target_degrees=None,pair_bounds=None):
    if target_degrees is None:target_degrees=[11 if p==h else 10 if p==q else 9 for p in range(13)]
    remain=[target_degrees[p]-sum(b>>p&1 for b in fixed) for p in space.vertices]
    caps=[(pair_bounds[t] if pair_bounds is not None else 20 if t==((1<<h)|(1<<q)) else 5)-sum(b&t==t for b in fixed) for t in space.pairs]
    missing=sum(1<<j for j,t in enumerate(space.triples) if not any(b&t==t for b in fixed))
    nodes=0;bundle_nodes=0;selected=[];witness=None

    def all_bundles(point,degree,need,domain):
        nonlocal bundle_nodes
        available=domain&space.through[point]
        if degree<=2:
            for i in indices(available):
                bundle_nodes+=1
                rest=need&~space.cover[i]
                if degree==1:
                    if not rest:yield (i,)
                    continue
                possible=available&~((1<<(i+1))-1)
                for t in indices(rest):possible &= space.through_triple[t]
                for x in space.member[i]:
                    if remain[x]==1:possible &= ~space.through[x]
                for t in space.pair_member[i]:
                    if caps[t]==1:possible &= ~space.through_pair[t]
                for j in indices(possible):yield (i,j)
            return
        def extend(u,left,choices,chosen):
            nonlocal bundle_nodes
            bundle_nodes+=1
            if not left:
                if not u:yield tuple(chosen)
                return
            if choices.bit_count()<left:return
            if u.bit_count()>10*left:return
            if left==1:
                possible=choices
                for t in indices(u):possible &= space.through_triple[t]
                for i in indices(possible):
                    if all(remain[p]>0 for p in space.member[i]) and all(caps[t]>0 for t in space.pair_member[i]):
                        yield tuple(chosen+[i])
                return
            if u:
                candidates=min((choices&space.through_triple[t] for t in indices(u)),key=int.bit_count)
            else:candidates=choices
            for i in indices(candidates):
                choices &= ~(1<<i)
                if any(remain[p]<=0 for p in space.member[i]) or any(caps[t]<=0 for t in space.pair_member[i]):continue
                future=choices
                for p in space.member[i]:
                    remain[p]-=1
                    if not remain[p]:future &= ~space.through[p]
                for t in space.pair_member[i]:
                    caps[t]-=1
                    if not caps[t]:future &= ~space.through_pair[t]
                yield from extend(u&~space.cover[i],left-1,future,chosen+[i])
                for t in space.pair_member[i]:caps[t]+=1
                for p in space.member[i]:remain[p]+=1
        # Materialize before yielding: recursive generation temporarily changes
        # margins, while the outer point search applies each finished bundle.
        for bundle in list(extend(need,degree,available,[])):yield bundle

    def visit(todo,left,domain):
        nonlocal nodes,witness
        nodes+=1
        if any(d<0 or d>left for d in remain):return False
        if not left:
            if todo or any(remain):return False
            witness=selected.copy();return True
        for p,d in enumerate(remain):
            if not d:domain &= ~space.through[p]
            if d==left:domain &= space.through[p]
        for t,c in enumerate(caps):
            if c<0:return False
            if not c:domain &= ~space.through_pair[t]
        if domain.bit_count()<left:return False
        active=[p for p,x in enumerate(space.vertices) if x not in (h,q) and remain[p]]
        if not active:return False
        degree=min(remain[p] for p in active)
        best=None;pivot=None
        for p in active:
            if remain[p]!=degree:continue
            need=todo&space.star[p]
            if need.bit_count()>10*degree:return False
            bundles=list(all_bundles(p,degree,need,domain))
            if not bundles:return False
            if best is None or len(bundles)<len(best):best=bundles;pivot=p
            if degree>2:break
        future=domain&~space.through[pivot]
        for bundle in best:
            covered=0
            for i in bundle:
                covered|=space.cover[i]
                for p in space.member[i]:remain[p]-=1
                for t in space.pair_member[i]:caps[t]-=1
            selected.extend(bundle)
            found=visit(todo&~covered,left-degree,future)
            del selected[-len(bundle):]
            for i in bundle:
                for t in space.pair_member[i]:caps[t]+=1
                for p in space.member[i]:remain[p]+=1
            if found:return True
        return False
    fixed_set=set(fixed)
    domain=sum(1<<i for i,b in enumerate(space.blocks) if b not in fixed_set)
    found=visit(missing,total_blocks-len(fixed),domain)
    out=dict(status='SAT' if found else 'UNSAT',point_states=nodes,bundle_states=bundle_nodes)
    if found:out['witness']=[space.blocks[i] for i in witness]
    return out
