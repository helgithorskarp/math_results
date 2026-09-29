"""Exact stabilizer orbits for a tuple of placed congruence classes.

An unvisited child and its entire subtree can be permuted freely. Visited
children are fixed individually. Coordinates are CRT prime-power residues,
with least significant digits first. See proof.md for the LP quotient.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from math import isqrt, prod


def divisors(L):
    result=set()
    for d in range(1,isqrt(L)+1):
        if L%d==0: result.update((d,L//d))
    return sorted(result)


def factor_levels(m):
    result=[]
    p=2
    while p*p<=m:
        if m%p==0:
            powers=[]; power=1
            while m%p==0:
                powers.append(power); power*=p; m//=p
            result.append((p,tuple(powers)))
        p+=1
    if m>1: result.append((m,(1,)))
    return tuple(result)


def orbit_data(L,anchors):
    if len({m for m,a in anchors})!=len(anchors): raise ValueError('Repeated modulus')
    if any(m<1 or L%m or not 0<=a<m for m,a in anchors): raise ValueError('Invalid anchor')
    used=defaultdict(set)
    for m,a in anchors:
        for p,powers in factor_levels(m):
            for power in powers: used[p,power,a%power].add(a//power%p)
    primes=[p for p,powers in factor_levels(L)]

    @lru_cache(None)
    def coordinate_table(p,exponent):
        table=[]
        for a in range(p**exponent):
            power=1
            for j in range(exponent):
                fixed=used[p,power,a%power]
                if a//power%p not in fixed:
                    first=min(c for c in range(p) if c not in fixed)
                    table.append(a%power+first*power)
                    break
                power*=p
            else: table.append(a)
        return tuple(table)

    @lru_cache(None)
    def phase_keys(m):
        exponents={p:len(powers) for p,powers in factor_levels(m)}
        periods=[p**exponents.get(p,0) for p in primes]
        tables=[coordinate_table(p,exponents.get(p,0)) for p in primes]
        return tuple(tuple(table[a%period] for table,period in zip(tables,periods)) for a in range(m))

    orbits={}
    for x,key in enumerate(phase_keys(L)):
        if all(x%m!=a for m,a in anchors): orbits.setdefault(key,[]).append(x)
    return list(orbits.values()),phase_keys


def quotient_rows(L,anchors,remaining):
    """Integer coefficients, row orbits, and original point orbits.

    A point orbit O projects onto one class orbit R; each individual class
    of R meets O in exactly |O|/|R| points. Rows with no residual point are
    omitted, because y_m>=0 implies their constraints.
    """
    if any(L%m for m in remaining): raise ValueError('Not a period')
    orbits,phase_keys=orbit_data(L,anchors)
    rows=[]
    for m in remaining:
        phases=phase_keys(m)
        sizes=Counter(phases)
        active={phases[orbit[0]%m] for orbit in orbits}
        for key in sorted(active):
            row={}
            for col,orbit in enumerate(orbits):
                if phases[orbit[0]%m]==key:
                    if len(orbit)%sizes[key]: raise RuntimeError('Nonintegral orbit fibre')
                    row[col]=len(orbit)//sizes[key]
            rows.append((m,key,row))
    return orbits,rows


def boxes_from_weights(L,anchors,weights):
    """Compress a point-orbit weight into explicit Cartesian axis masks."""
    periods=[p**len(powers) for p,powers in factor_levels(L)]
    orbits,_=orbit_data(L,anchors)
    result=[]
    for orbit in orbits:
        weight=weights.get(orbit[0],0)
        if any(weights.get(x,0)!=weight for x in orbit): raise ValueError('Not orbit-constant')
        if not weight: continue
        axes=[sorted({x%P for x in orbit}) for P in periods]
        if prod(len(axis) for axis in axes)!=len(orbit):
            raise RuntimeError('Not a Cartesian orbit')
        expected={tuple(x%P for P in periods) for x in orbit}
        if set(product(*axes))!=expected: raise RuntimeError('Cartesian expansion mismatch')
        result.append([sum(1<<a for a in axis) for axis in axes]+[weight])
    if sum(len(orbit)*weights.get(orbit[0],0) for orbit in orbits)!=sum(weights.values()):
        raise ValueError('Weight outside residual')
    return result
