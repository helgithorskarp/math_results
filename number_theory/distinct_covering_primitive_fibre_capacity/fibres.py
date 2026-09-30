"""A fibre version of the classical primitive-period obstruction.

six-covering-3, researcher. Written proof and exact controls, no solver.

Let N=B*p^2 with gcd(B,p)=1. Let b|B and suppose every nontop
resource n=m*d (m|B, d|p^2, m<B) has lcm(b,m)<B. A nonnegative
weight of period b*p^2 has coordinates w_z(t), t mod b, z mod p^2.
It vanishes on any placed classes. The three unplaced top-B resources
are B, B*p, B*p^2; at most one class of each may be used.

In each z fibre, the weight and every nontop weighted footprint have
proper period dividing B. If at most one top-B class is active in this
fibre, the signed-subset-shift argument of period.py gives
sum(nontop footprints)>=demand in the fibre. If at least two top-B
classes are active, use the ordinary nonnegative union bound instead.
Adjoin the three top-B classes if absent. This preserves coverage.
Since B is active in every z, the only useful top-B fibres are the
coset S={z:r mod p}, from the B*p class, together with the single
point s from the B*p^2 class.

Thus top-B mass may be bounded by

  sum_{z in S}(w_z(a)+w_z(c)) + w_s(e)
      + 1_{s not in S}w_s(a).

Its maximum J is at most 2*M_{bp}+2*M_{bp^2}, where M_g is the
maximum g-class weight on the base b*p^2. This replaces the ordinary
top-B charge M_b+M_{bp}+M_{bp^2}. Other actual resources are unchanged.
These are full-N capacities; multiply by (b*p^2)/N for base units.

At N43200, B1728, b144, p5:
Q3600: scaled coefficients at g144,720,3600 change by -5,+5,+5.
Q720: lift the weight five times to Q3600; the changes are -5,+6
at g144,720. The Q720 singleton-top omission remains a separate
valid bound; take whichever exact bound certifies a strict cut.

This is a scoped application/generalization of a classical period
argument. No historical-priority claim is made.
"""
from fractions import Fraction
from itertools import product
from math import gcd, lcm
from random import Random
from period import signed_shifts, covers, full_capacity

def proper_fibre_condition(B, b, resources, p):
    if B < 2 or b < 1 or B % b or (gcd(B, p) != 1):
        return False
    N = B * p * p
    if len(resources) != len(set(resources)) or any((N % n for n in resources)):
        raise ValueError('invalid finite resources')
    for n in resources:
        m = gcd(B, n)
        if m < B and lcm(b, m) == B:
            return False
    return b < B

def adjusted_actual_mass(B, p, Q, vector, classes):
    """Exact phase-dependent necessary budget, without maxima or gcd costs."""
    N = B * p * p
    resources = tuple((m for m, a in classes))
    b = gcd(B, Q)
    if not proper_fibre_condition(B, b, resources, p) or N % Q:
        raise ValueError('primitive fibre hypothesis fails')
    tops = tuple(((m, a) for m, a in classes if m % B == 0))
    others = tuple(((m, a) for m, a in classes if m % B != 0))
    useful = {z for z in range(p * p) if sum((int(z % (m // B) == a % (m // B)) for m, a in tops)) >= 2}
    ordinary = sum((vector[x % Q] for m, a in others for x in range(a, N, m)))
    useful_top = sum((vector[x % Q] for m, a in tops for x in range(a, N, m) if x % (p * p) in useful))
    return (sum(vector) * (N // Q), ordinary + useful_top)

def maxima_by_crt(b, p, Q, vector):
    """Physical full-N top charges from either declared weight period."""
    fine = b * p * p
    if fine % Q or Q not in (b * p, fine):
        raise ValueError('unexpected coarse/fine period')
    values = [vector[x % Q] for x in range(fine)]
    Mb = max((sum(values[a::b]) for a in range(b)))
    Mbp = max((sum(values[a::b * p]) for a in range(b * p)))
    Mfine = max(values)
    return (Mb, Mbp, Mfine)

def exact_J(b, p, Q, vector):
    """Exact maximum of the justified useful-top budget, not a cover test."""
    fine = b * p * p
    if fine % Q or Q not in (b * p, fine):
        raise ValueError('invalid period')
    W = [[0] * b for z in range(p * p)]
    for z in range(p * p):
        for t in range(b):
            x = next((x for x in range(t, fine, b) if x % (p * p) == z))
            W[z][t] = vector[x % Q]
    S = [[sum((W[z][t] for z in range(r, p * p, p))) for t in range(b)] for r in range(p)]
    M = [max(row) for row in S]
    u = [max(row) for row in W]
    best = 0
    for r in range(p):
        for s in range(p * p):
            if s % p == r:
                budget = 2 * M[r] + u[s]
            else:
                budget = M[r] + u[s] + max((a + c for a, c in zip(S[r], W[s])))
            best = max(best, budget)
    return best

def check_positive(B, b, p, Q, vector, classes):
    N = B * p * p
    if not covers(N, classes):
        raise ValueError('Control failure in fibres.py at original line 117')
    demand, adjusted = adjusted_actual_mass(B, p, Q, vector, classes)
    if not adjusted >= demand:
        raise ValueError('Control failure in fibres.py at original line 119')
    top = (B, B * p, N)
    all_resources = tuple((n for n, a in classes))
    full_demand, caps = full_capacity(N, Q, vector, all_resources)
    if not full_demand == demand:
        raise ValueError('Control failure in fibres.py at original line 123')
    Mb, Mbp, Mfine = maxima_by_crt(b, p, Q, vector)
    if not (caps[B], caps[B * p], caps[N]) == (Mb, Mbp, Mfine):
        raise ValueError('Control failure in fibres.py at original line 125')
    J = exact_J(b, p, Q, vector)
    if not J <= 2 * Mbp + 2 * Mfine:
        raise ValueError('Control failure in fibres.py at original line 127')
    total = sum((v for n, v in caps.items() if n not in top)) + J
    if not total >= demand:
        raise ValueError('Control failure in fibres.py at original line 129')
    return (J, total)

def controls():
    counts = {'agent': 'six-covering-3', 'role': 'researcher'}
    positive_checks, physical_phase_checks = (0, 0)
    B, b, p, N = (3, 1, 2, 12)
    resources = (2, 3, 4, 6, 12)
    for phases in product(*(range(n) for n in resources)):
        classes = tuple(zip(resources, phases))
        physical_phase_checks += 1
        if not covers(N, classes):
            continue
        for Q in (2, 4):
            for vector in product(range(3), repeat=Q):
                if not any(vector):
                    continue
                check_positive(B, b, p, Q, vector, classes)
                positive_checks += 1
    counts.update(raw_full_cover_phase_assignments=physical_phase_checks, exact_nonconstant_positive_checks=positive_checks)
    N, B, b, p = (300, 12, 2, 5)
    original = {2: 0, 3: 0, 4: 1, 6: 1, 12: 11}
    resources = tuple((n for n in range(2, N + 1) if N % n == 0))
    classes = tuple(((n, original.get(n, 1)) for n in resources))
    rng = Random(703)
    for Q in (10, 50):
        for i in range(12):
            vector = [rng.randrange(8) for _ in range(Q)]
            check_positive(B, b, p, Q, vector, classes)
            positive_checks += 1
    counts['literal_period300_cover_checks'] = 24
    N, B, b, p, Q = (300, 12, 12, 5, 300)
    classes = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11), (60, 0), (300, 0))
    if not covers(N, classes):
        raise ValueError('Control failure in fibres.py at original line 169')
    if not not proper_fibre_condition(B, b, tuple((n for n, a in classes)), p):
        raise ValueError('Control failure in fibres.py at original line 170')
    vector = [int(x % B == 11 and x % 25 == 1) for x in range(N)]
    ordinary_other = sum((vector[x] for n, a in classes if n % B for x in range(a, N, n)))
    useful_top = sum((vector[x] for n, a in classes if n % B == 0 for x in range(a, N, n) if sum((x % (m // B) == t % (m // B) for m, t in classes if m % B == 0)) >= 2))
    if not (sum(vector) == 1 and ordinary_other + useful_top == 0):
        raise ValueError('Control failure in fibres.py at original line 179')
    counts['hypothesis_failure_counterfixture'] = {'N': N, 'B': B, 'b': b, 'point_weight': 1, 'invalid_adjusted_mass': 0}
    N, B, b, p, scale = (43200, 1728, 144, 5, 60)
    resources = tuple((n for n in range(8, N + 1) if N % n == 0))
    if not proper_fibre_condition(B, b, resources, p):
        raise ValueError('Control failure in fibres.py at original line 187')
    applications = []
    for Q in (720, 3600):
        for i in range(5):
            vector = [rng.randrange(6) for _ in range(Q)]
            D, caps = full_capacity(N, Q, vector, resources)
            Mb, Mbp, Mfine = maxima_by_crt(b, p, Q, vector)
            if not (caps[B], caps[B * p], caps[N]) == (Mb, Mbp, Mfine):
                raise ValueError('Control failure in fibres.py at original line 194')
            J = exact_J(b, p, Q, vector)
            if not J <= 2 * Mbp + 2 * Mfine:
                raise ValueError('Control failure in fibres.py at original line 196')
            old = sum(caps.values())
            replacement = old - caps[B] - caps[B * p] - caps[N] + 2 * Mbp + 2 * Mfine
            base = Fraction(scale * Q, N) * old
            if Q == 720:
                M144 = max((sum(vector[a::144]) for a in range(144)))
                expected = base - 5 * M144 + 6 * max(vector)
            else:
                M144 = max((sum(vector[a::144]) for a in range(144)))
                M720 = max((sum(vector[a::720]) for a in range(720)))
                expected = base - 5 * M144 + 5 * M720 + 5 * max(vector)
            if not expected == Fraction(scale * Q, N) * replacement:
                raise ValueError('Control failure in fibres.py at original line 207')
            applications.append({'Q': Q, 'literal_resources': len(resources), 'ordinary_top_capacity': caps[B] + caps[B * p] + caps[N], 'exact_J': J, 'simple_top_bound': 2 * Mbp + 2 * Mfine})
    counts['literal_43200_models'] = applications
    counts['total_positive_cover_weight_checks'] = positive_checks
    return counts
