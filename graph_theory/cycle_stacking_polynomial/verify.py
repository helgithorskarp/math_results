#!/usr/bin/env python3
"""Independent finite checks for the universal proof in PROOF.md."""
from __future__ import annotations
from dataclasses import asdict
from functools import lru_cache
from hashlib import sha256
from itertools import product
import argparse
import json
from pathlib import Path
from random import Random

from cycle_profiles import (Piece, all_maxima, analyze, candidate_points,
                            prefixes, verify_witness)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def compositions(mass, length):
    if length == 1:
        yield (mass,)
    else:
        for first in range(mass + 1):
            for tail in compositions(mass-first, length-1):
                yield (first,) + tail


@lru_cache(maxsize=None)
def raw_stackable(c):
    """Definition-level oracle: recurse over every legal first cycle move.

    This function does not use transfer messages, residues, cuts or profiles.
    """
    if sum(x > 0 for x in c) <= 1:
        return any(c)
    n = len(c)
    for i, pile in enumerate(c):
        if pile >= 2:
            for j in ((i-1) % n, (i+1) % n):
                child = list(c)
                child[i] -= 2
                child[j] += 1
                if raw_stackable(tuple(child)):
                    return True
    return False


def literal_scores(c):
    """Uncompressed signed-tree recurrence, independent of profile code."""
    n = len(c)
    def branch(values):
        message = 0
        nonempty = False
        for pile in values:
            nonempty |= pile != 0
            s = pile + message
            # Original net-balance formula, rather than normalized recurrence.
            message = 2*s - 3*max(1, -((-s)//2)) if nonempty else 0
        return message
    return tuple(c[t]+branch(c[:t])+branch(c[t+1:][::-1]) for t in range(n))


def literal_maxima(c):
    n = len(c)
    out = []
    for cut in range(n):
        maxima = [None] * (n+1)
        interior = tuple(c[(cut+i) % n] for i in range(1,n))
        for split in range(c[cut]+1):
            scores = literal_scores((split,) + interior + (c[cut]-split,))
            for t, value in enumerate(scores):
                if maxima[t] is None or value > maxima[t]:
                    maxima[t] = value
        out.append(maxima)
    return out


def run():
    digest = sha256()
    counts = {}
    def bind(label, data):
        digest.update(json.dumps([label, data], separators=(',',':')).encode()+b'\n')
    rng = Random(2026092607)

    # Arbitrary dyadic staircases, not only profiles realizable by pebbling.
    counts['floor_pair_cases'] = 0
    for p in (1,2,4,8,16):
        for q in (1,2,4,8,16):
            for _ in range(160):
                lo = rng.randrange(-40,40)
                hi = lo + rng.randrange(81)
                f = Piece(lo,hi,2**rng.randrange(6),rng.randrange(-60,60),p,rng.randrange(-9,10))
                g = Piece(lo,hi,2**rng.randrange(6),rng.randrange(-60,60),q,rng.randrange(-9,10))
                total = rng.randrange(-40,40)
                candidates = candidate_points(f,g,total,lo,hi)
                value = max(f.value(t)+g.value(total-t) for t in candidates)
                expected = max(f.value(t)+g.value(total-t) for t in range(lo,hi+1))
                require(value == expected, 'opposed-floor maximum mismatch')
                bind('floors',[p,q,lo,hi,value])
                counts['floor_pair_cases'] += 1

    counts['profile_entries'] = 0
    counts['profile_cases'] = 0
    for depth in range(1,31):
        for _ in range(15):
            residue = rng.randrange(3)
            lower = 1 if residue == 0 else 0
            upper = lower + 100
            additions = (0,) + tuple(rng.randrange(16) for _ in range(depth-1))
            profile, rout = prefixes(additions,residue,lower,upper)[-1]
            require(len(profile) <= depth+1, 'profile size bound')
            require([t for v in profile for t in range(v.lo,v.hi+1)] == list(range(lower,upper+1)), 'profile partition')
            values = []
            for v in profile:
                require(v.a > 0 and v.a & (v.a-1) == 0 and v.p > 0 and v.p & (v.p-1) == 0, 'non-dyadic coefficient')
                for t in range(v.lo,v.hi+1):
                    score = 3*t+residue
                    for c in additions:
                        s = score+c
                        score = 2*s-3*max(1,-((-s)//2))
                    require(score == 3*v.value(t)+rout, 'profile recurrence mismatch')
                    values.append(score)
                    counts['profile_entries'] += 1
            require(values == sorted(values), 'residue monotonicity')
            bind('profile',[depth,residue,additions,values])
            counts['profile_cases'] += 1

    # Compare every maximum, not just the final Boolean or aggregate count.
    counts['literal_configurations'] = 0
    counts['literal_cut_target_maxima'] = 0
    for n in range(3,10):
        for _ in range(100):
            c = tuple(rng.randrange(31) for _ in range(n))
            maxima, stats = all_maxima(c)
            observed = [[v.score for v in row] for row in maxima]
            expected = literal_maxima(c)
            require(observed == expected, f'literal maxima mismatch {c}')
            for row in maxima:
                for v in row:
                    interior = tuple(c[(v.cut+i)%n] for i in range(1,n))
                    require(literal_scores((v.split,)+interior+(c[v.cut]-v.split,))[v.target] == v.score, 'maximum attainment')
            bind('maxima',[c,observed])
            counts['literal_configurations'] += 1
            counts['literal_cut_target_maxima'] += n*(n+1)

    counts['raw_configurations'] = 0
    domain = [[3,8],[4,9],[5,10],[6,9],[7,8]]
    for n, mass_limit in domain:
        for mass in range(mass_limit+1):
            for c in compositions(mass,n):
                result = analyze(c)
                actual = raw_stackable(c)
                require(result['stackable'] == actual, f'raw move mismatch {c}')
                if actual:
                    require(verify_witness(c,result['witness']), 'positive witness rejection')
                bind('raw',[c,actual,result['maximum_split_score']])
                counts['raw_configurations'] += 1
        raw_stackable.cache_clear()

    # The universal stable obstruction and its sharp neighboring configuration.
    counts['stable_ray_cases'] = 0
    for k in list(range(3,26))+[32,48,64]:
        c = [0]*(2*k+1)
        c[0] = 5*2**(k-1)-6
        c[k] = c[k+2] = 1
        negative = analyze(c)
        require(not negative['stackable'], f'stable obstruction k={k}')
        c[0] += 1
        positive = analyze(c)
        require(positive['stackable'] and verify_witness(c,positive['witness']), 'stable conductor')
        bind('stable',[k,negative['maximum_split_score'],positive['maximum_split_score']])
        counts['stable_ray_cases'] += 2

    counts['large_integer_cases'] = 0
    counts['large_integer_attainments'] = 0
    for n in (3,5,9,17,33):
        for bits in (100,500,2000):
            c = tuple(rng.getrandbits(bits) if i % 3 == 0 else rng.randrange(2) for i in range(n))
            maxima, stats = all_maxima(c)
            require(stats['profile_pieces'] <= 3*n*(n+1)*(n+2), 'cubic profile bound')
            require(stats['piece_intersections'] <= 3*n*(n+1)**2, 'cubic intersection bound')
            require(stats['candidate_points'] <= 12*n*(n+1)**2, 'cubic candidate bound')
            for row in maxima:
                for v in row:
                    interior = tuple(c[(v.cut+i)%n] for i in range(1,n))
                    score = literal_scores((v.split,)+interior+(c[v.cut]-v.split,))[v.target]
                    require(score == v.score, 'large-integer attainment')
                    counts['large_integer_attainments'] += 1
            bind('large',[n,bits,[[v.score for v in row] for row in maxima],stats])
            counts['large_integer_cases'] += 1

    counts['rejected_inputs'] = 0
    for c in ([],[0,1],[1,-1,2],[True,1,2],[1.0,2,3]):
        try:
            analyze(c)
        except ValueError:
            counts['rejected_inputs'] += 1
        else:
            raise RuntimeError('malformed configuration accepted')
    c = [0,0,1,1,0,0,15]
    valid = analyze(c)['witness']
    require(verify_witness(c,valid), 'split-essential witness')
    for key, value in [('cut',-1),('target',8),('split',-1),('score',0),('score',valid['score']+1)]:
        changed = dict(valid)
        changed[key] = value
        require(not verify_witness(c,changed),'mutated witness accepted')
        counts['rejected_inputs'] += 1
    require(not verify_witness(c,{}),'empty witness accepted')
    counts['rejected_inputs'] += 1
    return dict(status='PASS',counts=counts,raw_domain=domain,entry_sha256=digest.hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=run()
    if args.check:
        expected=json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        require(result==expected,'expected-output mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
