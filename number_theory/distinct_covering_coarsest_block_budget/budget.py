"""Exact coarsest-top-resource upper budget, six-covering-3 researcher.

The universal necessary inequality is proved in proof.md. G is an upper
relaxation, not an attainable maximum or a covering construction.
"""
from itertools import product
from math import gcd, lcm, prod


def matrix(W, C):
    if type(C) is not int or C < 2 or len(W) != C:
        raise ValueError("An integer cofactor C>=2 and C weight rows are required")
    b = len(W[0])
    if b < 1 or any(len(row) != b for row in W):
        raise ValueError("A nonempty rectangular weight matrix is required")
    if any(type(w) is not int or w < 0 for row in W for w in row):
        raise ValueError("Nonnegative integer weights are required")
    return b


def radical(B):
    if type(B) is not int or B < 2:
        raise ValueError("B must be an integer at least two")
    result, remaining, p = 1, B, 2
    while p*p <= remaining:
        if remaining % p == 0:
            result *= p
            while remaining % p == 0:
                remaining //= p
        p += 1
    return result*remaining


def parameters(B, C, b):
    if type(C) is not int or C < 2 or type(b) is not int or b < 1:
        raise ValueError("Positive base period and integer cofactor C>=2 required")
    rho = radical(B)
    if gcd(B,C) != 1 or (B//rho) % b:
        raise ValueError("gcd(B,C)=1 and b|B/rad(B) required")
    return B*C


def coarsest_budget(W, C):
    """G_C=max_t sum_{d|C,d>1} max(M_d,2H_d(t)); zero weight allowed."""
    b = matrix(W,C)
    H = {}
    for d in range(2,C+1):
        if C % d == 0:
            H[d] = [max(sum(W[z][t] for z in range(a,C,d))
                        for a in range(d)) for t in range(b)]
    M = {d:max(values) for d,values in H.items()}
    totals = [sum(max(M[d],2*H[d][t]) for d in H) for t in range(b)]
    G = max(totals)
    return {"G":G,"maximizing_label":totals.index(G),
            "label_totals":totals,"H":H,"M":M,
            "doubled_independent_sum":2*sum(M.values())}


def decode_boxes(Q, axes, boxes):
    if (type(Q) is not int or Q < 1 or len(axes)!=3 or
            any(type(a) is not int or a<2 for a in axes) or prod(axes)!=Q or
            any(gcd(axes[i],axes[j])!=1 for i in range(3) for j in range(i))):
        raise ValueError("Three coprime coordinate axes with product Q required")
    vector = [0]*Q
    for box in boxes:
        if len(box)!=4 or any(type(v) is not int for v in box) or box[-1]<=0:
            raise ValueError("Malformed positive box")
        choices = []
        for axis,mask in zip(axes,box):
            if not 0<mask<1<<axis:
                raise ValueError("Invalid coordinate mask")
            choices.append([x for x in range(axis) if mask>>x & 1])
        for point in product(*choices):
            x = sum(a*(Q//axis)*pow(Q//axis,-1,axis)
                    for a,axis in zip(point,axes)) % Q
            if vector[x]:
                raise ValueError("Overlapping boxes")
            vector[x] = box[-1]
    if not any(vector):
        raise ValueError("Nonzero certificate weight required")
    return vector


def period_capacities(N, vector, resources):
    """Actual physical maxima from the elementary CRT lifting identity."""
    Q = len(vector)
    if type(N) is not int or N < 1 or not Q or N%Q:
        raise ValueError("Weight period must divide finite N")
    if any(type(w) is not int or w<0 for w in vector):
        raise ValueError("Nonnegative integer periodic weights required")
    if (len(resources)!=len(set(resources)) or
            any(type(n) is not int or n<2 or N%n for n in resources)):
        raise ValueError("Distinct resource divisors of N required")
    maxima = {}
    for g in {gcd(Q,n) for n in resources}:
        sums = [0]*g
        for x,w in enumerate(vector):
            sums[x%g] += w
        maxima[g] = max(sums)
    return {n:(N//lcm(Q,n))*maxima[gcd(Q,n)] for n in resources}
