#!/usr/bin/env python3
"""Standalone literal five-subset certificate check; no research-module imports."""
from pathlib import Path
from itertools import combinations
import argparse
import json


def check(data):
    words = data['words']
    if len(words)!=62 or len(set(words))!=62 or any(type(w) is not int or not 0<=w<1<<18 for w in words):
        raise ValueError('invalid62-word container')
    sets = tuple(frozenset(v for v in range(18) if w>>v&1) for w in words)
    if any(len(w)!=5 for w in sets) or any(len(a&b)>2 for a,b in combinations(sets,2)):
        raise ValueError('invalid five-subset packing')
    g = tuple(v^1 if v<16 else v for v in range(18))
    if tuple(data['involution'])!=g or {frozenset(g[v] for v in w) for w in sets}!=set(sets):
        raise ValueError('involution certificate fails')
    degrees = tuple(sum(v in w for w in sets) for v in range(18))
    pair = sum({16,17}<=w for w in sets)
    fixed = sum(frozenset(g[v] for v in w)==w for w in sets)
    if degrees[16:]!=(20,18) or pair!=4 or fixed!=6:
        raise ValueError('certificate does not match scoped theorem')
    return dict(status='VALID literal sharp witness',words=62,pair_multiplicity=pair,
                replications=degrees,fixed_words=fixed)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate',type=Path,nargs='?',default=Path(__file__).with_name('witness.json'))
    args=p.parse_args()
    print(json.dumps(check(json.loads(args.certificate.read_text())),sort_keys=True))
