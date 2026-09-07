"""Exact probability of distance constraints for disjoint duplicate-row pairs."""
from collections import defaultdict
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb


def tail(n, threshold):
    return sum(comb(n,k) for k in range(max(0,threshold),n+1))


def signed_tail(n, degree, threshold):
    b=2*degree
    return sum((-1)**j*comb(b,j)*comb(n-b,k-j)
               for k in range(threshold,n+1) for j in range(b+1)
               if 0<=k-j<=n-b)


def transfer(side=20, threshold=8, pairs=4):
    """Expansion over a graph on the selected pairs; signed coefficients."""
    if not 0<=2*pairs<=side or not 0<=threshold<=side-2:
        raise ValueError('invalid transfer parameters')
    if pairs==0:
        return Fraction(1)
    edges=list(combinations(range(pairs),2))
    weights=[signed_tail(side-2,d,threshold) for d in range(pairs)]
    total=0
    for mask in range(1 << len(edges)):
        degrees=[0]*pairs
        for k,(a,b) in enumerate(edges):
            if mask >> k & 1:
                degrees[a]+=1;degrees[b]+=1
        term=1
        for degree in degrees:term*=weights[degree]
        total+=term
    return Fraction(total,2**((side-2)*pairs))


def grouped_transfer(side=20, threshold=8, pairs=10):
    """Exact degree-weighted graph sum with at most 2**pairs states."""
    if pairs==0:return Fraction(1),1
    weights=[signed_tail(side-2,d,threshold) for d in range(pairs)]
    @lru_cache(None)
    def visit(degrees):
        if not degrees:return 1
        center=degrees[0];groups=sorted(Counter(degrees[1:]).items())
        def choose(i,neighbors,following,mult):
            if i==len(groups):
                return mult*weights[center+neighbors]*visit(tuple(sorted(following)))
            d,c=groups[i]
            return sum(choose(i+1,neighbors+k,following+[d]*(c-k)+[d+1]*k,
                              mult*comb(c,k)) for k in range(c+1))
        return choose(0,0,[],1)
    value=visit((0,)*pairs)
    return Fraction(value,2**((side-2)*pairs)),visit.cache_info().currsize


def positive_transfer(side=20, threshold=8, pairs=4):
    """Independent integration over all actual 2x2 edge-block signatures."""
    if pairs==0:return Fraction(1)
    block=defaultdict(int)
    for bits in range(16):
        a,b,c,d=((bits >> k)&1 for k in range(4))
        block[(int(a!=c)+int(b!=d),int(a!=b)+int(c!=d))]+=1
    states={(0,)*pairs:1}
    for a,b in combinations(range(pairs),2):
        new=defaultdict(int)
        for degrees,count in states.items():
            for (x,y),mult in block.items():
                value=list(degrees);value[a]+=x;value[b]+=y
                new[tuple(value)]+=count*mult
        states=new
    unused=side-2*pairs
    total=0
    for degrees,count in states.items():
        term=count
        for d in degrees:term*=2**unused*tail(unused,threshold-d)
        total+=term
    touched=2*pairs*unused+4*comb(pairs,2)
    return Fraction(total,2**touched)


def grouped_positive_transfer(side=20, threshold=8, pairs=10):
    """Positive 2x2-block integration, grouped by partial distances."""
    unused=side-2*pairs
    if unused<0:raise ValueError('too many selected pairs')
    @lru_cache(None)
    def retire(current,odd,remaining):
        even=remaining-odd
        return 2**even*8**odd*2**unused*sum(
            comb(even,h)*tail(unused,threshold-current-odd-2*h)
            for h in range(even+1))
    @lru_cache(None)
    def visit(distances):
        if not distances:return 1
        center=distances[0];remaining=len(distances)-1
        groups=sorted(Counter(distances[1:]).items())
        destinations=defaultdict(int)
        def choose(i,odd,following,mult):
            if i==len(groups):
                destinations[(tuple(sorted(following)),odd)]+=mult
                return
            d,c=groups[i]
            for ones in range(c+1):
                for twos in range(c-ones+1):
                    choose(i+1,odd+ones,
                           following+[d]*(c-ones-twos)+[d+1]*ones+[d+2]*twos,
                           mult*comb(c,ones)*comb(c-ones,twos))
        choose(0,0,[],1)
        return sum(mult*retire(center,odd,remaining)*visit(following)
                   for (following,odd),mult in destinations.items())
    count=visit((0,)*pairs)
    touched=2*pairs*unused+4*comb(pairs,2)
    return Fraction(count,2**touched),visit.cache_info().currsize


if __name__=='__main__':
    import json
    rows=[]
    for p in range(11):
        a,states=grouped_transfer(pairs=p)
        b,positive_states=grouped_positive_transfer(pairs=p)
        if a!=b:raise ArithmeticError('independent transfer disagreement')
        rows.append({'pairs':p,'keep_fraction':[a.numerator,a.denominator],
                     'signed_states':states,'positive_states':positive_states})
    print(json.dumps(rows,indent=2,sort_keys=True))
