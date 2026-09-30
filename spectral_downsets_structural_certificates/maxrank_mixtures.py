#!/usr/bin/env python3
"""Explicit partition mixtures; proofs and quantified scope in CLIQUE_CENTERS.md."""
from fractions import Fraction as F
import certificates as base
import friendship
import two_centers


def integer_at_least(value, minimum, name):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(name + " must be an integer >= " + str(minimum))


def partition_core(colors, s):
    integer_at_least(s, 1, "s")
    if any(not isinstance(c, int) or isinstance(c, bool) or not 0 <= c < s
           for c in colors):
        raise ValueError("Invalid partition color")
    return [[F(s * int(a == b) - 1) for b in colors] for a in colors]


def mix(core, colors, s, epsilon):
    return mix_cores(core, partition_core(colors,s), epsilon)


def mix_cores(core, part, epsilon):
    epsilon = F(epsilon)
    if not 0 < epsilon < 1 or len(part) != len(core):
        raise ValueError("Invalid mixture coefficient or dimensions")
    if any(len(row) != len(core) for row in core+part):
        raise ValueError("Nonsquare input core")
    return [[(1-epsilon)*a+epsilon*b for a,b in zip(row, other)]
            for row,other in zip(core,part)]


def repaired_core(core, colors, s):
    """Requires a centered H core with U>=I and a proper partition.

    Returns the mixture and epsilon. Those mathematical hypotheses must be
    established by the caller's proof; this function is not a PSD verifier.
    """
    n = len(core)+1
    beta = max(0, s*max(colors.count(c) for c in range(s))-n)
    epsilon = F(1, 2*(beta+1))
    return mix(core, colors, s, epsilon), epsilon


def two_center_colors(t):
    integer_at_least(t, 2, "t")
    a,b = 1 << t, 1 << (t+1)
    assignment = {a:t+1, b:t+1, a|b:t}
    for j in range(t):
        leaf = 1 << j
        assignment[a|leaf] = j
        assignment[b|leaf] = (j+1) % t
        assignment[leaf] = t
    return [assignment[a] for a in two_centers.family(t)[1:]]


def two_center_partition_average(t):
    """Average of the preceding proper partition under all leaf permutations.

    Distinct spoke leaves match colors with probability 1/(t-1); the other
    same-class relations do not depend on a permutation. No permutations
    are enumerated by this constructor.
    """
    integer_at_least(t,2,"t")
    a,b = 1 << t,1 << (t+1)
    edge = a|b
    members = two_centers.family(t)[1:]
    answer=[]
    for x in members:
        row=[]
        for y in members:
            if x==y:
                value=F(t+1)
            elif x & y:
                value=F(-1)
            elif (x in (a,b) and y in (a,b)) or (
                (x==edge or x.bit_count()==1 and x not in (a,b)) and
                (y==edge or y.bit_count()==1 and y not in (a,b))):
                value=F(t+1)
            elif x.bit_count()==y.bit_count()==2:
                value=F(3,t-1)
            else:
                value=F(-1)
            row.append(value)
        answer.append(row)
    return answer


def two_center_certificate(t, shift=0):
    integer_at_least(shift, 0, "shift")
    core = mix_cores(two_centers.core(t),two_center_partition_average(t),F(1,(t+1)**2))
    return two_centers.family(t, shift), base.lift(core, t+2), t+2


def friendship_colors(k):
    integer_at_least(k, 2, "k")
    center = 1 << (2*k)
    assignment = {center:2*k}
    for j in range(2*k):
        leaf = 1 << j
        assignment[center|leaf] = j
        assignment[leaf] = j ^ 1
    for i in range(k):
        edge = (1 << (2*i)) | (1 << (2*i+1))
        assignment[edge] = 2*k if i == 0 else (2*i+2) % (2*k)
    return [assignment[a] for a in friendship.family(k)[1:]]


def friendship_certificate(k, shift=0):
    integer_at_least(shift, 0, "shift")
    colors = friendship_colors(k)
    members,matrix,s = friendship.certificate(k)
    core = mix(base.extract_core(matrix,s), colors, s, F(1,2*(k+2)))
    return [a << shift for a in members], base.lift(core,s), s
