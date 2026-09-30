"""Alternate exact replay by the same author; no external reviewer verdict.

Different first-appearance normalization, full-period resource histograms,
non-CRT weight decoding, and literal progression-union pair capacities.
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from math import prod
from pathlib import Path
import random
from time import monotonic
import check
import kernel

BASE=Path(__file__).resolve().parent


def powers(n):
    result=[];p=2
    while p*p<=n:
        if n%p==0:
            q=1
            while n%p==0:n//=p;q*=p
            result.append((p,q))
        p+=1
    if n>1:result.append((n,n))
    return result


def normalize(previous):
    names={};answer=[]
    for m,a in previous:
        coordinates=[]
        for p,P in powers(m):
            power=1;encoded=0
            while power<P:
                original=a%power;labels=names.setdefault((p,power,original),{})
                digit=a//power%p
                if digit not in labels:labels[digit]=len(labels)
                encoded+=labels[digit]*power;power*=p
            coordinates.append((P,encoded))
        value=next(b for b in range(m) if all(b%P==v for P,v in coordinates))
        answer.append((m,value))
    return tuple(answer)


def reference_options(m,previous):
    for a in range(m):
        extended=previous+((m,a),)
        if normalize(extended)==extended:yield a


def children(m,A):
    return list(reference_options(m,tuple(A)))


def literal_bound(L,Q,U,remaining):
    # Explicit lift, with no gcd/lcm capacity formula or bit-sliced counts.
    points=[x for x in range(L) if U>>(x%Q)&1]
    capacity=L-len(points)
    for m in remaining:
        counts=[0]*m
        for x in points:counts[x%m]+=1
        capacity+=max(counts)
    return capacity


def literal_uniform(L,A):
    points=[x for x in range(L) if all(x%m!=a for m,a in A)]
    capacity=0
    for m in range(8,L+1):
        if L%m or m in dict(A):continue
        counts=[0]*m
        for x in points:counts[x%m]+=1
        capacity+=max(counts)
    return len(points),capacity


@lru_cache(None)
def literal_axis(L,P,mask):
    # Every membership predicate is an ordinary integer remainder.
    return sum(1<<x for x in range(L) if mask>>(x%P)&1)


def literal_decode(L,boxes):
    periods=[P for p,P in powers(L)]
    if prod(periods)!=L:raise ValueError('Incomplete factorization')
    W=[0]*L
    for box in boxes:
        if len(box)!=len(periods)+1 or type(box[-1]) is not int or box[-1]<=0:
            raise ValueError('Invalid weighted box')
        bits=(1<<L)-1
        for mask,P in zip(box[:-1],periods):
            if type(mask) is not int or not 0<mask<1<<P:raise ValueError('Invalid axis mask')
            bits&=literal_axis(L,P,mask)
        while bits:
            one=bits&-bits;x=one.bit_length()-1;bits^=one
            if W[x]:raise ValueError('Overlapping weighted boxes')
            W[x]=box[-1]
    return W


def literal_pairs(W,m,n):
    # Each class is its actual progression. Add the second progression's
    # weight only at points outside the first; no CRT intersection formula.
    left=[sum(W[x] for x in range(a,len(W),m)) for a in range(m)]
    right=[tuple((x,W[x]) for x in range(b,len(W),n) if W[x]) for b in range(n)]
    largest=0;digest=sha256()
    for a in range(m):
        for b in range(n):
            value=left[a]+sum(w for x,w in right[b] if x%m!=a)
            largest=max(largest,value);digest.update((str(value)+',').encode('ascii'))
    return largest,digest.hexdigest(),m*n


def literal_sieve():
    density=[];structural=[];retained=[]
    for L in range(10080,30240,8):
        # A full divisibility scan checks the complete finite LCM reduction.
        divisors=[m for m in range(1,L+1) if L%m==0]
        capacity=sum(L//m for m in divisors if m>=8)
        if capacity<L:density.append(L);continue
        prime_support={p for p,P in powers(L)}
        if prime_support.issubset({2,3,5}) and L%5400:structural.append(L);continue
        retained.append(L)
    return density,structural,retained


def controls():
    rng=random.Random(20260930);pair_cases=0;phase_tuples=0
    for L in (12,24,60):
        divisors=[m for m in range(2,L+1) if L%m==0]
        for sample in range(3):
            W=[rng.randrange(5) for x in range(L)]
            for i,m in enumerate(divisors):
                for n in divisors[i+1:]:
                    actual=literal_pairs(W,m,n);expected=check.pair_capacities(W,m,n)
                    if actual!=expected:raise ValueError('Small complete pair-capacity mismatch')
                    pair_cases+=1;phase_tuples+=m*n
    # Known smaller-minimum cover must survive both scalar capacity routines.
    witness=[(2,0),(3,0),(4,1),(6,1),(12,11)]
    if not all(any(x%m==a for m,a in witness) for x in range(12)):raise ValueError('Positive covering failed')
    ordinary=kernel.search_case(12,[2,3,4],minimum=2,prune=True)
    alternate=kernel.search_case(12,[2,3,4],minimum=2,prune=True,
                                 reference_bound=literal_bound,reference_options=reference_options)
    if ordinary!=alternate or ordinary['excludes']:raise ValueError('Known covering was falsely excluded')
    rejections=0
    for boxes in ([[[-1,1,1,1]]],[[[1,1,1,0]]]):
        # Flatten the one-box fixture; both decoders reject independently.
        for decoder in (check.decode,literal_decode):
            try:decoder(60,boxes[0])
            except ValueError:rejections+=1
            else:raise ValueError('Malformed box was accepted')
    cert=json.loads((BASE/'certificate.json').read_text())
    # Removing a required plan with an adjusted surviving list must not
    # certify the fixed theorem. Reject before any expensive replay.
    incomplete=json.loads(json.dumps(cert));removed=incomplete['plans'].pop(0)
    incomplete['remaining_LCMs']=sorted(incomplete['remaining_LCMs']+[removed['L']])
    try:check.prove(incomplete)
    except ValueError:rejections+=1
    else:raise ValueError('Incomplete exclusion list accepted')
    duplicate=json.loads(json.dumps(cert));duplicate['nodes'].append(duplicate['nodes'][0])
    try:check.prove(duplicate)
    except ValueError:rejections+=1
    else:raise ValueError('Duplicate proof record accepted')
    if literal_sieve()!=check.sieve():raise ValueError('Finite candidate sieve differs')
    return {'small_pair_cases':pair_cases,'small_pair_phase_tuples':phase_tuples,
            'positive_cover_checked':True,'malformed_or_incomplete_rejections':rejections,
            'all_2520_LCM_candidates_checked':True}


def main():
    start=monotonic();certificate=json.loads((BASE/'certificate.json').read_text())
    actual=check.prove(certificate,reference_bound=literal_bound,reference_options=reference_options,
        decoder=literal_decode,pair_counter=literal_pairs,uniform_counter=literal_uniform,
        child_options=children,sieve_fn=literal_sieve)
    if actual!=json.loads((BASE/'expected.json').read_text()):raise ValueError('Full alternate manifest differs')
    summary=controls()
    print(json.dumps({'agent':'six-covering-2','role':'researcher','full_alternate_replay':'PASS',
                      'completion_events_sha256':actual['completion_events_sha256'],
                      'pair_capacities_sha256':actual['pair_capacities_sha256'],'controls':summary},indent=2))
    print(f'Elapsed seconds: {monotonic()-start:.3f}')


if __name__=='__main__':main()
