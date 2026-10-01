"""Finite exact cover with full-footprint and optional contact exclusions.

UNKNOWN is represented only by an exception, never by a negative decision.
"""
class Incomplete(RuntimeError):
    pass

class Cover:
    def __init__(self,required,tiles,extra_conflict=None,node_limit=500000,audit=False,audit_extra=None):
        self.required=tuple(sorted(required));self.tiles=tuple(sorted(tiles))
        self.node_limit=node_limit;self.nodes=0
        hi={p:i for i,p in enumerate(self.required)}
        self.covers=[];self.at=[0]*len(hi)
        sets=[set(t) for t in self.tiles]
        for i,t in enumerate(self.tiles):
            mask=sum(1<<hi[p] for p in t if p in hi)
            assert mask,'Candidates must meet the required set'
            self.covers.append(mask)
            bits=mask
            while bits:
                bit=bits&-bits;bits^=bit
                self.at[bit.bit_length()-1]|=1<<i
        self.conflicts=[1<<i for i in range(len(sets))]
        for i,a in enumerate(sets):
            for j in range(i):
                if a&sets[j] or (extra_conflict is not None and extra_conflict(i,j)):
                    self.conflicts[i]|=1<<j;self.conflicts[j]|=1<<i
        self.full=(1<<len(hi))-1
        self.all=(1<<len(sets))-1
        self.failed=set()
        self.audit=None
        if audit:
            from audit import Audit
            self.audit=Audit(self,extra_conflict if audit_extra is None else audit_extra)

    def find(self,forced=None):
        def rec(available,remaining):
            self.nodes+=1
            if self.nodes>self.node_limit:raise Incomplete('Exact-cover node guard reached')
            if not remaining:return ()
            state=(available,remaining)
            if state in self.failed:return None
            bits=remaining;best=None;count=len(self.tiles)+1
            while bits:
                bit=bits&-bits;bits^=bit
                legal=self.at[bit.bit_length()-1]&available
                n=legal.bit_count()
                if n<count:best=legal;count=n
                if n<=1:break
            while best:
                bit=best&-best;best^=bit;i=bit.bit_length()-1
                ans=rec(available&~self.conflicts[i],remaining&~self.covers[i])
                if ans is not None:return (i,)+ans
            self.failed.add(state)
            return None
        root=(self.all,self.full) if forced is None else (self.all&~self.conflicts[forced],self.full&~self.covers[forced])
        result=rec(*root)
        if result is not None and forced is not None:result=(forced,)+result
        if self.audit is not None:
            if result is None:self.audit.certify(root)
            else:self.audit.witness(result,forced)
        return result

    def support(self):
        indices=set()
        for i in range(len(self.tiles)):
            if i in indices:continue
            found=self.find(i)
            if found is not None:indices.update(found)
        return {self.tiles[i] for i in indices}

    def solutions(self):
        def rec(available,remaining,chosen):
            self.nodes+=1
            if self.nodes>self.node_limit:raise Incomplete('Exact-cover enumeration guard reached')
            if not remaining:
                yield chosen;return
            bits=remaining;best=None;count=len(self.tiles)+1
            while bits:
                bit=bits&-bits;bits^=bit
                legal=self.at[bit.bit_length()-1]&available;n=legal.bit_count()
                if n<count:best=legal;count=n
                if n<=1:break
            while best:
                bit=best&-best;best^=bit;i=bit.bit_length()-1
                yield from rec(available&~self.conflicts[i],remaining&~self.covers[i],chosen+(i,))
        yield from rec(self.all,self.full,())
