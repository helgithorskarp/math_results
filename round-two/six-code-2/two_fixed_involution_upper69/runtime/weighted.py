from paths import INPUTS, WORK
"""Exact weighted coloring search with a positive witness on incompleteness."""
import time
from carrier import require


class Incomplete(RuntimeError):
    def __init__(self, best, weight, nodes):
        super().__init__('INCOMPLETE weighted clique guard')
        self.best, self.weight, self.nodes = best, weight, nodes


def maximum(adjacency, weights, seed=(), target=None, node_cap=3000000, seconds=30):
    n=len(weights)
    require(len(adjacency)==n and all(w in (1,2) for w in weights),'weighted graph domain')
    require(all(0<=a<1<<n and not a>>i&1 and all(bool(a>>j&1)==bool(adjacency[j]>>i&1)
            for j in range(n)) for i,a in enumerate(adjacency)),'undirected simple graph')
    require(len(seed)==len(set(seed)) and all(0<=i<n for i in seed) and all(
            adjacency[i]>>j&1 for k,i in enumerate(seed) for j in seed[k+1:]),'seed clique')
    require(0<=node_cap<=3000000 and 0<seconds<=30,'guard settings')
    best=tuple(seed); best_weight=sum(weights[i] for i in seed)
    nodes=0; started=time.monotonic()

    def coloring(pool):
        ordered,bounds=[],[]
        previous=0
        while pool:
            available=pool; largest=0
            while available:
                bit=available&-available; v=bit.bit_length()-1
                ordered.append(v); largest=max(largest,weights[v]);bounds.append(previous+largest)
                pool^=bit; available&=~bit&~adjacency[v]
            previous+=largest
        return ordered,bounds

    def visit(pool,chosen,value):
        nonlocal nodes,best,best_weight
        nodes+=1
        if value>best_weight:
            best,best_weight=tuple(chosen),value
        if nodes>node_cap or time.monotonic()-started>seconds:
            raise Incomplete(best,best_weight,nodes)
        if target is not None and best_weight>=target:
            return
        ordered,bounds=coloring(pool)
        for k in range(len(ordered)-1,-1,-1):
            if value+bounds[k]<=best_weight:
                return
            v=ordered[k]
            visit(pool&adjacency[v],chosen+(v,),value+weights[v])
            if target is not None and best_weight>=target:
                return
            pool&=~(1<<v)

    visit((1<<n)-1,(),0)
    return best_weight,tuple(sorted(best)),nodes,('FOUND_TARGET' if target is not None and
            best_weight>=target else 'COMPLETE_MAXIMUM')
