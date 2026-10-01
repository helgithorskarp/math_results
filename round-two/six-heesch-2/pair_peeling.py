"""Symmetry-covariant pair-centered halo closure for finite upper bounds."""
from geometry import affine,inverse,halo,pose,contacts,matrices
from cover import Cover

class PairPeeling:
    def __init__(self,tile,node_limit=500000,audit=False):
        self.tile=tuple(sorted(tile));self.node_limit=node_limit;self.audit=audit
        self.raw=set(contacts(self.tile))
        self._poses={self.tile:(1,0,0,1,0,0)}
        self.stabilizers=[]
        for m in matrices():
            raw=affine(self.tile,m+(0,0));a,b=min(raw);x,y=min(self.tile)
            g=m+(x-a,y-b)
            if affine(self.tile,g)==self.tile:self.stabilizers.append(g)

    def check_domain(self,domain):
        assert domain<=self.raw
        for t in domain:
            assert affine(self.tile,inverse(pose(self.tile,t))) in domain,'Asymmetric contact domain'
            assert all(affine(t,g) in domain for g in self.stabilizers),'Stabilizer closure failed'

    def transported(self,t,domain):
        if t not in self._poses:self._poses[t]=pose(self.tile,t)
        g=self._poses[t]
        return {affine(u,g) for u in domain}

    def cover(self,fixed,domain):
        fixed=tuple(fixed);occupied=set().union(*(set(t) for t in fixed))
        need=halo(occupied)
        neighbors={t:self.transported(t,domain) for t in fixed}
        pool=set().union(*neighbors.values())
        pool={u for u in pool if occupied.isdisjoint(u) and set(u)&need}
        if domain==self.raw:
            # Completeness of E0 makes every disjoint contacting pair allowed.
            # Avoid rebuilding this vacuous restriction for every candidate.
            return Cover(need,pool,node_limit=self.node_limit,audit=self.audit)
        hs={t:halo(t) for t in fixed}
        pool={u for u in pool if all(not (set(u)&hs[t]) or u in neighbors[t] for t in fixed)}
        tiles=tuple(sorted(pool));sets=[set(t) for t in tiles]
        h=[halo(t) for t in tiles]
        inv=[inverse(pose(self.tile,t)) for t in tiles]
        def incompatible(i,j):
            return bool(sets[i]&h[j]) and (affine(tiles[i],inv[j]) not in domain or affine(tiles[j],inv[i]) not in domain)
        def audit_incompatible(i,j):
            # Direct cell-neighbor incidence, fresh isometries, and inverses;
            # does not use the search-side halo sets or precomputed frames.
            from geometry import DIRS
            if not any((x+a,y+b) in sets[j] for x,y in tiles[i] for a,b in DIRS):return False
            u=affine(tiles[i],inverse(pose(self.tile,tiles[j])))
            v=affine(tiles[j],inverse(pose(self.tile,tiles[i])))
            return u not in domain or v not in domain
        return Cover(need,tiles,incompatible,self.node_limit,audit=self.audit,audit_extra=audit_incompatible)

    def peel(self,domain):
        kept=set();evidence=[]
        for t in sorted(domain):
            c=self.cover((self.tile,t),domain)
            found=c.find()
            evidence.append({'pair':t,'possible':found is not None,'nodes':c.nodes,'pool':len(c.tiles)})
            if found is not None:kept.add(t)
        return kept,evidence

    def run(self,max_rounds=5,progress=None):
        domain=set(self.raw);rows=[]
        self.check_domain(domain)
        # Single-center eligibility can only prefilter pairs to be tested at
        # round 1. It MUST NOT restrict the candidate neighbors for that round.
        star=Cover(halo(self.tile),domain,node_limit=self.node_limit,audit=self.audit)
        first=star.find()
        rows.append({'round':0,'pairs':len(domain),'star':first is not None,'nodes':star.nodes})
        if progress is not None:progress(rows[-1])
        if first is None:return {'upper':0,'rows':rows,'domain':[]}
        tested=star.support()
        tested={t for t in tested if self.tile in self.transported(t,tested)}
        for r in range(1,max_rounds+1):
            if r==1:
                new=set();evidence=[]
                for t in sorted(tested):
                    c=self.cover((self.tile,t),domain);found=c.find()
                    evidence.append({'pair':t,'possible':found is not None,'nodes':c.nodes,'pool':len(c.tiles)})
                    if found is not None:new.add(t)
            else:new,evidence=self.peel(domain)
            domain=new
            self.check_domain(domain)
            star=self.cover((self.tile,),domain)
            found=star.find()
            rows.append({'round':r,'pairs':len(domain),'star':found is not None,'nodes':sum(v['nodes'] for v in evidence)+star.nodes,
                         'tested':len(evidence)})
            if progress is not None:progress(rows[-1])
            if found is None:return {'upper':r,'rows':rows,'domain':sorted(domain)}
            if r>1 and len(domain)==rows[-2]['pairs']:
                return {'upper':None,'stable':True,'rows':rows,'domain':sorted(domain)}
        return {'upper':None,'rows':rows,'domain':sorted(domain)}
