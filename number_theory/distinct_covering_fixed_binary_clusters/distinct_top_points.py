"""Exact controls for distinct top points, including fixed top phases.

Actual author: six-covering-2, researcher. Written proof is in
proof.md. Exhaustive budget evaluation deliberately
has a small complete phase-product cap; an oversized instance is refused.
No solver, covering exclusion, or historical-priority claim is implicit.
"""
from itertools import product
from math import gcd, prod


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def radical(n):
    r = 1
    for p in range(2, n + 1):
        if n % p == 0 and all(p % d for d in range(2, p)):
            r *= p
    return r


def prepare(B, C, b, known, u, v, minimum=2):
    if any(type(x) is not int for x in (B, C, b, minimum)):
        raise ValueError('Integer parameters')
    if min(B, C) < 2 or gcd(B, C) != 1 or B < minimum:
        raise ValueError('Coprime factorization and eligible top resources')
    N = B * C
    rho = radical(B)
    T = B // rho
    if b < 1 or T % b:
        raise ValueError('Block period')
    Q = b * C
    if len(u) != N or len(v) != Q:
        raise ValueError('Physical and periodic weight lengths')
    if any(type(x) is not int or x < 0 for x in u + v):
        raise ValueError('Nonnegative integer controls')
    A = dict(known)
    if len(A) != len(known):
        raise ValueError('Distinct known resources')
    for n, a in known:
        if type(n) is not int or type(a) is not int or n < minimum or N % n or not 0 <= a < n:
            raise ValueError('Known eligible classes')
        if any(u[x] for x in range(a, N, n)):
            raise ValueError('Unrestricted weight vanishes on all known classes')
    S = [B * d for d in divisors(C)]
    free = [n for n in S if n not in A]
    blocks = []
    for q in range(T):
        for z in range(C):
            x = q + B * (((z - q) * pow(B, -1, C)) % C)
            w = v[x % Q]
            if w:
                blocks.append((q, z, w))
    return {'B': B, 'C': C, 'b': b, 'N': N, 'Q': Q, 'T': T, 'rho': rho,
            'known': A, 'S': S, 'free': free, 'u': u, 'v': v,
            'blocks': blocks, 'has_u': bool(sum(u)), 'minimum': minimum}


def charge(state, phases):
    """CRT resource description; returns sharp and multiplicity charges."""
    if set(phases) != set(state['S']):
        raise ValueError('All top resources accounted')
    for n, a in phases.items():
        if type(a) is not int or not 0 <= a < n:
            raise ValueError('Actual phase range')
        if n in state['known'] and a != state['known'][n]:
            raise ValueError('A prescribed top phase must remain fixed')
    B, T = state['B'], state['T']
    top = [(a % B, n // B, a % (n // B)) for n, a in phases.items()]
    sharp = old = 0
    for q, z, w in state['blocks']:
        points = [alpha for alpha, d, r in top if alpha % T == q and z % d == r]
        r = len(set(points))
        k = len(points)
        if r >= 2:
            sharp += r * w
        if k >= 2:
            old += k * w
    if state['has_u']:
        ordinary = sum(sum(state['u'][phases[n]::n]) for n in state['free'])
        sharp += ordinary
        old += ordinary
    return sharp, old


def exact_budget(state, phase_cap=100_000):
    """Complete literal phase product, with no incomplete exclusion output."""
    count = prod(state['free'])
    if count > phase_cap:
        raise ValueError('Complete phase product exceeds control cap')
    best = old_best = -1
    best_phases = None
    fixed = {n: state['known'][n] for n in state['S'] if n in state['known']}
    for values in product(*(range(n) for n in state['free'])):
        phases = fixed | dict(zip(state['free'], values))
        s, o = charge(state, phases)
        if s > best:
            best = s
            best_phases = phases
        old_best = max(old_best, o)
    return {'sharp_budget': best, 'multiplicity_budget': old_best,
            'actual_tuples': count, 'attaining_phases': best_phases}
