"""Exact disjoint halo-cover support; arbitrary-precision integer masks."""
class Cover:
    def __init__(self,required,tiles):
        self.tiles=tuple(sorted(tiles));required=sorted(required)
        universe=sorted(set().union(*(set(t) for t in self.tiles))) if self.tiles else []
        index={p:i for i,p in enumerate(universe)};hi={p:i for i,p in enumerate(required)}
        self.masks=[sum(1<<index[p] for p in t) for t in self.tiles]
        self.covers=[sum(1<<hi[p] for p in t if p in hi) for t in self.tiles]
        self.at=[[] for p in required]
        for i,c in enumerate(self.covers):
            for j in range(len(required)):
                if (c>>j)&1:self.at[j].append(i)
        self.full=(1<<len(required))-1;self.nodes=0

    def find(self,forced=None):
        def rec(occupied,remaining):
            self.nodes+=1
            if not remaining:return ()
            best=None
            bits=remaining
            while bits:
                bit=bits&-bits;j=bit.bit_length()-1;bits^=bit
                legal=[i for i in self.at[j] if not occupied&self.masks[i]]
                if not legal:return None
                if best is None or len(legal)<len(best):best=legal
                if len(best)==1:break
            for i in best:
                result=rec(occupied|self.masks[i],remaining&~self.covers[i])
                if result is not None:return (i,)+result
            return None
        if forced is None:return rec(0,self.full)
        result=rec(self.masks[forced],self.full&~self.covers[forced])
        return None if result is None else (forced,)+result

    def support(self):
        used=set()
        for i in range(len(self.tiles)):
            if i in used:continue
            result=self.find(i)
            if result is not None:used.update(result)
        return {self.tiles[i] for i in used}
