"""Standalone literal witness checker, without search or census imports."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

def require(ok,why):
    if not ok:raise ValueError(why)

def check(data,size,multiplicity):
    masks=data['words'];g=data['involution'];u,v=data['centers']
    require(len(masks)==len(set(masks))==size and all(type(w) is int and 0<w<1<<18 and w.bit_count()==5 for w in masks),'literal distinct five-subsets')
    require(len(g)==18 and all(type(p) is int for p in g) and sorted(g)==list(range(18)) and all(g[g[p]]==p for p in range(18)) and sum(g[p]==p for p in range(18))==2,'involution cycle type')
    require(type(u) is int and type(v) is int and 0<=u<18 and 0<=v<18 and u!=v and g[u]==v,'exchanged centers')
    words=[frozenset(p for p in range(18) if w>>p&1) for w in masks]
    require(all(len(a&b)<=2 for a,b in combinations(words,2)),'literal packing')
    require({frozenset(g[p] for p in w) for w in words}==set(words),'involution closure')
    degrees=tuple(sum(p in w for w in words) for p in range(18))
    require(degrees[u]==degrees[v]==20 and sum({u,v}<=w for w in words)==multiplicity,'scoped saturated pair')
    if 'replications' in data:require(tuple(data['replications'])==degrees,'incorrect degree readout')
    return {'words':size,'literal_pairs':size*(size-1)//2,'pair_multiplicity':multiplicity,
            'degree_profile':sorted(Counter(degrees).items()),'fixed_words':sum(frozenset(g[p] for p in w)==w for w in words)}

def all_witnesses():
    base=Path(__file__).resolve().parent
    return {str(n):check(json.loads((base/('WITNESS%d.json'%n)).read_text()),n,m) for n,m in ((56,3),(58,4),(69,5))}

if __name__=='__main__':print(json.dumps({'status':'PASS_LITERAL56_58_69','witnesses':all_witnesses()},sort_keys=True))
