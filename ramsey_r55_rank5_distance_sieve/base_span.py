"""Independent positive counting by actual labels and their concrete span.

No Gaussian coefficients, Mobius function or span subtraction is used.
The state holds a subset of F2^r (the span) and all occupied word lengths.
"""
from functools import lru_cache
from math import comb


@lru_cache(None)
def extend(space, vector):
    result = space
    rest = space
    while rest:
        bit = rest & -rest
        rest -= bit
        result |= 1 << ((bit.bit_length()-1) ^ vector)
    return result


def span_counts(labels, rank, max_length, cap):
    labels = tuple(labels)
    if len(set(labels)) != len(labels) or any(type(x) is not int or not 0 <= x < 2**rank for x in labels):
        raise ValueError('invalid actual label set')
    if max_length < 0 or cap < 1:
        raise ValueError('invalid length or multiplicity cap')
    choose = [[comb(k+t, t) for t in range(min(cap,max_length-k)+1)]
              for k in range(max_length+1)]
    states = {1: [1] + [0]*max_length}
    for vector in labels:
        new = {space: counts[:] for space,counts in states.items()}
        for space,counts in states.items():
            destination = extend(space, vector)
            out = new.setdefault(destination, [0]*(max_length+1))
            for length,value in enumerate(counts):
                if not value:
                    continue
                for t in range(1, len(choose[length])):
                    out[length+t] += value*choose[length][t]
        states = new
    return states.get((1 << (2**rank))-1, [0]*(max_length+1))


def target_counts():
    """Compute every spanning-word value used by the target stages."""
    nonzero = {cap:span_counts(range(1,32),5,23,cap) for cap in (3,4,5,23)}
    affine = {cap:span_counts(range(16,32),5,23,cap) for cap in (3,4,5,23)}
    all_vectors = span_counts(range(32),5,23,23)
    return {'nonzero':nonzero,'affine':affine,'all_vectors':all_vectors}
