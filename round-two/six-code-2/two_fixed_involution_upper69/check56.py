"""Standalone literal checker; imports no carrier, generator or search code."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path


def check(data):
    words=data['words']; g=data['involution']; x,y=data['centers']
    if not isinstance(words,list) or len(words)!=56 or len(set(words))!=56 or any(
            type(w) is not int or not 0<=w<1<<18 or w.bit_count()!=5 for w in words):
        raise ValueError('56 distinct literal five-subsets required')
    if len(g)!=18 or any(type(v) is not int for v in g) or sorted(g)!=list(range(18)) or any(
            g[g[v]]!=v for v in range(18)) or sum(g[v]==v for v in range(18))!=2:
        raise ValueError('involution cycle type2^8*1^2 required')
    if type(x) is not int or type(y) is not int or not 0<=x<18 or not 0<=y<18 or x==y or g[x]!=y:
        raise ValueError('swapped centers required')
    sets=tuple(frozenset(v for v in range(18) if w>>v&1) for w in words)
    if any(len(a&b)>2 for a,b in combinations(sets,2)):
        raise ValueError('pairwise intersection above two')
    if {frozenset(g[v] for v in a) for a in sets}!=set(sets):
        raise ValueError('code not closed under involution')
    degrees=tuple(sum(v in a for a in sets) for v in range(18))
    if degrees[x]!=20 or degrees[y]!=20 or sum(x in a and y in a for a in sets)!=3:
        raise ValueError('saturated centers/multiplicity3 required')
    if 'replications' in data and tuple(data['replications'])!=degrees:
        raise ValueError('incorrect replication readout')
    return {'status':'VALID56_SCOPED_WITNESS','words':56,'literal_pairs':1540,
            'replications':degrees,'degree_profile':sorted(Counter(degrees).items()),
            'fixed_words':sum(frozenset(g[v] for v in a)==a for a in sets),'pair_multiplicity':3}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('witness',type=Path)
    args=parser.parse_args(); print(json.dumps(check(json.loads(args.witness.read_text())),sort_keys=True))
