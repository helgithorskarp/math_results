"""Positive actual-label/span DP, retaining the number of repeated labels."""
from functools import lru_cache
from math import comb


@lru_cache(None)
def extend(space, vector):
    result=space
    for x in range(space.bit_length()):
        if space >> x & 1:result |= 1 << (x^vector)
    return result


def marked(labels, rank, length, cap=3):
    states={(1,0,0):1}
    for vector in labels:
        new={}
        for (space,k,repeated),value in states.items():
            for t in range(min(cap,length-k)+1):
                key=(extend(space,vector) if t else space,k+t,repeated+int(t>=2))
                new[key]=new.get(key,0)+value*comb(k+t,t)
        states=new
    full=(1 << (2**rank))-1
    return [states.get((full,length,j),0) for j in range(length//2+1)]
