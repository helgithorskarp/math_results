"""Exact useful top-resource budgets; six-covering-3, researcher.

The universal claims are proved in proof.md. This module evaluates finite
formulas and realizes their maximizing block phases. It does not find a
covering, prove a full-period exclusion, or bound a literal class union.
"""
from functools import lru_cache
from itertools import product
from math import gcd, isqrt


def prime(p):
    return type(p) is int and p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))


def validate(W, p, c):
    if not prime(p) or type(c) is not int or c < 1 or len(W) != p**c:
        raise ValueError("Invalid prime, exponent or cofactor axis")
    b = len(W[0])
    if b < 1 or any(len(row) != b for row in W):
        raise ValueError("Invalid base axis")
    if any(type(w) is not int or w < 0 for row in W for w in row):
        raise ValueError("Nonnegative integer weights required")
    return b


def partitions(n):
    """Each partition once, by increasing first element of a block."""
    if n == 0:
        yield ()
        return
    for old in partitions(n - 1):
        for i in range(len(old)):
            yield old[:i] + (old[i] + (n - 1,),) + old[i + 1:]
        yield old + ((n - 1,),)


def useful(k):
    return k if k >= 2 else 0


def general_budget(W, p, c):
    """The finite F_c definition, with its literal maximizing witness.

    This reference enumeration is exponential, not an efficient general
    optimizer. Zero weight is allowed for the component identity.
    """
    b = validate(W, p, c)
    powers = tuple(p**j for j in range(c + 1))
    ps = tuple(partitions(c + 1))

    @lru_cache(None)
    def group_maximum(group, phases):
        if len(group) == 1:
            return 0, 0
        masses = [0] * b
        for z, row in enumerate(W):
            k = sum(z % powers[j] == phase for j, phase in zip(group, phases))
            if k >= 2:
                for t, weight in enumerate(row):
                    masses[t] += k * weight
        value = max(masses)
        return value, masses.index(value)

    best, witness = -1, None
    for phases in product(*(range(power) for power in powers)):
        for pi in ps:
            choices = [group_maximum(group, tuple(phases[j] for j in group)) for group in pi]
            value = sum(choice[0] for choice in choices)
            if value > best:
                best = value
                witness = {
                    "partition": [list(group) for group in pi],
                    "cofactor_phases": list(phases),
                    "group_maximizers": [choice[1] for choice in choices],
                }
    return best, witness


def cube_budget(W, p):
    """F_3 = max(K_3, 2 M_1 + 2 M_3), retaining a common t in K_3."""
    b = validate(W, p, 3)
    U1 = [[sum(W[z][t] for z in range(r, p**3, p)) for t in range(b)] for r in range(p)]
    U2 = [[sum(W[z][t] for z in range(u, p**3, p*p)) for t in range(b)] for u in range(p*p)]
    M1 = max(value for row in U1 for value in row)
    M3 = max(value for row in W for value in row)
    K, witness = -1, None
    for r in range(p):
        for u in range(p*p):
            a = 1 if u % p == r else 2
            for s in range(p**3):
                d = 1 if s % p == r or s % (p*p) == u else 2
                for t in range(b):
                    value = 2*U1[r][t] + a*U2[u][t] + d*W[s][t]
                    if value > K:
                        K, witness = value, [r, u, s, t]
    pair = 2*M1 + 2*M3
    return {
        "F3": max(K, pair), "K3": K, "pair_budget": pair,
        "M1": M1, "M3": M3, "K3_witness": witness,
    }


def radical(B):
    if type(B) is not int or B < 2:
        raise ValueError("B must be an integer at least two")
    answer, n, q = 1, B, 2
    while q*q <= n:
        if n % q == 0:
            answer *= q
            while n % q == 0:
                n //= q
        q += 1
    if n > 1:
        answer *= n
    return answer


def realize(B, p, c, W, witness):
    """Merge groups choosing equal t, then realize with actual CRT phases.

    This realizes the useful-charge maximum, not a covering completion.
    """
    b = validate(W, p, c)
    T = B // radical(B)
    if gcd(B, p) != 1 or T % b:
        raise ValueError("Coprimality and b|B/rad(B) required")
    pi = witness["partition"]
    phases = witness["cofactor_phases"]
    maxima = witness["group_maximizers"]
    flat = [j for group in pi for j in group]
    if sorted(flat) != list(range(c + 1)) or any(not group for group in pi):
        raise ValueError("Invalid top-resource partition")
    if len(phases) != c + 1 or any(type(r) is not int or not 0 <= r < p**j
                                  for j, r in enumerate(phases)):
        raise ValueError("Invalid cofactor phases")
    if len(maxima) != len(pi) or any(type(t) is not int or not 0 <= t < b for t in maxima):
        raise ValueError("Invalid block maxima")
    labels = {}
    merged = {}
    for group, t in zip(pi, maxima):
        merged.setdefault(t, []).extend(group)
        for j in group:
            labels[j] = t
    classes = []
    for j, r in enumerate(phases):
        q = labels[j]
        power = p**j
        a = q if j == 0 else q + B * ((r - q) * pow(B, -1, power) % power)
        classes.append([B*power, a])
    return {"N": B*p**c, "T": T, "classes": classes,
            "merged_groups": [{"label": t, "indices": sorted(js)}
                              for t, js in sorted(merged.items())]}
