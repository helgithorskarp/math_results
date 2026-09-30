"""Exact finite-period top-resource reduction and support projection.

six-covering-3, researcher. This is an application of the classical
Mirsky--Newman / primitive-period difference argument, not a claim to
have discovered that classical obstruction.

Let Q|N, Q<N, and let w on Z/N be nonnegative and Q-periodic, vanishing
on the placed congruences. The unplaced resource set R has at most one
class for each distinct modulus. If N is in R and lcm(Q,n)<N for every
other n in R, every covering completion satisfies

    sum_{n in R minus {N}} max_a sum_{x=a mod n} w(x) >= sum_x w(x).

Thus the singleton resource N may be omitted in the weighted capacity
bound. The actual N class is NOT deleted from a proposed covering.

Proof: set F=sum_{selected n<N} w*1_{a_n mod n} and h=F-w.
Every summand and w has period a proper divisor of N. Consequently
Delta h=0 for Delta=product_{p|N}(I-T_{N/p}).
If an N class is selected, h is nonnegative except possibly at its
single point a; otherwise h is nonnegative everywhere. The 2^omega(N)
subset shifts in Delta are distinct modulo N. Evaluating Delta h at
a shows that the nonnegative terms at positive-sign nonzero shifts
have sum at least -h(a). Hence sum h>=0, including when h(a)<0.
Therefore sum F>=sum w, and replacing selected footprints by their
individual maxima gives the displayed bound. No equality of capacities
or solver optimality is needed.

Distinct subset shifts: if S!=T, choose a prime p in their symmetric
difference. In their difference sum, the term +/-N/p is not divisible
by p^{v_p(N)}, while all other terms are. The difference is not 0 mod N.

A Q-periodic w vanishes on a class a mod m with m|N iff it is zero on
every base point y=a mod gcd(Q,m); this is the ordinary CRT compatibility
condition. Support markers do not consume modulus resources.
"""
from fractions import Fraction
from itertools import product
from math import gcd, lcm

def prime_divisors(n):
    if type(n) is not int or n < 2:
        raise ValueError('N must be an integer >=2')
    primes, trial = ([], 2)
    while trial * trial <= n:
        if n % trial == 0:
            primes.append(trial)
            while n % trial == 0:
                n //= trial
        trial += 1
    if n > 1:
        primes.append(n)
    return tuple(primes)

def signed_shifts(N):
    shifts = [(0, 1)]
    for p in prime_divisors(N):
        shifts += [((offset + N // p) % N, -sign) for offset, sign in shifts]
    if len({offset for offset, sign in shifts}) != len(shifts):
        raise ValueError('subset shifts unexpectedly collide')
    return tuple(shifts)

def unique_top(N, Q, resources):
    if type(Q) is not int or Q < 1 or N % Q or (Q >= N):
        return False
    if len(resources) != len(set(resources)):
        raise ValueError('resources must be distinct')
    if any((type(n) is not int or n <= 0 or N % n for n in resources)):
        raise ValueError('every resource must divide N')
    return tuple((n for n in resources if lcm(Q, n) == N)) == (N,)

def projected_markers(N, Q, actual_anchors):
    if Q < 1 or N % Q:
        raise ValueError('Q must divide N')
    markers = set()
    for m, a in actual_anchors:
        if m < 1 or N % m or (not 0 <= a < m):
            raise ValueError('invalid actual congruence')
        g = gcd(Q, m)
        markers.add((g, a % g))
    return tuple(sorted(markers))

def full_capacity(N, Q, vector, resources):
    """Literal full-N capacity; deliberately independent of gcd formula."""
    if N % Q or len(vector) != Q or any((type(w) is not int or w < 0 for w in vector)):
        raise ValueError('invalid periodic integer weights')
    maxima = {}
    for n in resources:
        if n < 1 or N % n:
            raise ValueError('invalid modulus')
        maxima[n] = max((sum((vector[x % Q] for x in range(a, N, n))) for a in range(n)))
    return (N // Q * sum(vector), maxima)

def base_capacity(Q, vector, resources):
    """Capacity in base units; each actual resource is charged separately."""
    if len(vector) != Q:
        raise ValueError('invalid vector length')
    answer = {}
    for n in resources:
        g = gcd(Q, n)
        M = max((sum((vector[x] for x in range(a, Q, g))) for a in range(g)))
        answer[n] = Fraction(g, n) * M
    return (sum(vector), answer)

def covers(N, anchors):
    return all((any((x % m == a for m, a in anchors)) for x in range(N)))

def controls():
    output = {'agent': 'six-covering-3', 'role': 'researcher'}
    shifts_checked, proper_functions = (0, 0)
    for N in (2, 3, 4, 6, 8, 12, 18, 20, 24, 30, 36, 60, 72):
        shifts = signed_shifts(N)
        shifts_checked += len(shifts)
        for d in range(1, N):
            if N % d:
                continue
            for a in range(d):
                if not all((sum((sign * int((x + offset) % d == a) for offset, sign in shifts)) == 0 for x in range(N))):
                    raise ValueError('Control failure in period.py at original line 129')
                proper_functions += 1
        for a in range(N):
            if not sum((sign * int((a + offset) % N == a) for offset, sign in shifts)) == 1:
                raise ValueError('Control failure in period.py at original line 133')
    output.update(small_subset_shifts=shifts_checked, proper_period_basis_functions=proper_functions)
    N, Q, anchors, resources, vector = (12, 2, ((2, 0),), (3, 4, 12), [0, 1])
    if not unique_top(N, Q, resources):
        raise ValueError('Control failure in period.py at original line 140')
    demand, maxima = full_capacity(N, Q, vector, resources)
    if not demand == sum(maxima.values()) == 6:
        raise ValueError('Control failure in period.py at original line 142')
    if not sum((maxima[n] for n in resources if n != N)) == 5:
        raise ValueError('Control failure in period.py at original line 143')
    if not Fraction(1, 2) + sum((Fraction(1, n) for n in resources)) > 1:
        raise ValueError('Control failure in period.py at original line 144')
    if not not any((covers(N, anchors + tuple(zip(resources, phases))) for phases in product(*(range(n) for n in resources)))):
        raise ValueError('Control failure in period.py at original line 145')
    output['residual_equality_fixture'] = {'N': N, 'Q': Q, 'placed': anchors, 'remaining': resources, 'demand': demand, 'ordinary_capacity': 6, 'reduced_capacity': 5, 'phase_assignments_checked': 3 * 4 * 12}
    anchors = ((2, 0), (4, 1))
    resources, phases, Q, vector = ((3, 6, 12), (0, 1, 11), 4, [0, 0, 0, 1])
    if not covers(12, anchors + tuple(zip(resources, phases))):
        raise ValueError('Control failure in period.py at original line 155')
    if not not unique_top(12, Q, resources):
        raise ValueError('Control failure in period.py at original line 156')
    demand, maxima = full_capacity(12, Q, vector, resources)
    if not demand == sum(maxima.values()) == 3:
        raise ValueError('Control failure in period.py at original line 158')
    if not sum((maxima[n] for n in resources if n != 12)) == 2:
        raise ValueError('Control failure in period.py at original line 159')
    output['positive_control_without_uniqueness'] = {'cover': anchors + tuple(zip(resources, phases)), 'Q': Q, 'demand': demand, 'ordinary_capacity': 3, 'invalid_reduced_capacity': 2}
    resources = (2, 3, 4, 6, 12)
    covers_checked, weight_checks = (0, 0)
    for phases in product(*(range(n) for n in resources)):
        anchors = tuple(zip(resources, phases))
        if not covers(12, anchors):
            continue
        covers_checked += 1
        for Q in (1, 2):
            if not unique_top(12, Q, resources):
                raise ValueError('Control failure in period.py at original line 174')
            for vector in product(range(3), repeat=Q):
                if not any(vector):
                    continue
                demand, maxima = full_capacity(12, Q, vector, resources)
                if not sum((v for n, v in maxima.items() if n != 12)) >= demand:
                    raise ValueError('Control failure in period.py at original line 179')
                weight_checks += 1
    output.update(positive_cover_assignments=covers_checked, positive_cover_weight_checks=weight_checks)
    N, Q = (43200, 720)
    resources = tuple((n for n in range(8, N + 1) if N % n == 0))
    if not unique_top(N, Q, resources):
        raise ValueError('Control failure in period.py at original line 187')
    if not not unique_top(N, 3600, resources):
        raise ValueError('Control failure in period.py at original line 188')
    shifts = signed_shifts(N)
    prefix = (0, 0, 0, 1, 1, 3, 3, 2, 7, 0)
    moduli = (8, 9, 10, 12, 15, 16, 18, 20, 24, 25)
    actual = tuple(zip(moduli, prefix))
    markers = projected_markers(N, Q, actual)
    for y in range(Q):
        possible = any((y % g == a for g, a in markers))
        literal = any((any((x % m == a for m, a in actual)) for x in range(y, N, Q)))
        if not possible == literal:
            raise ValueError('Control failure in period.py at original line 197')
    vector = [0 if any((y % g == a for g, a in markers)) else 1 + y % 7 for y in range(Q)]
    if not any(vector):
        raise ValueError('Control failure in period.py at original line 200')
    demand, maxima = full_capacity(N, Q, vector, resources)
    base_demand, capacities = base_capacity(Q, vector, resources)
    if not demand == N // Q * base_demand:
        raise ValueError('Control failure in period.py at original line 203')
    if not all((maxima[n] == N // Q * capacities[n] for n in resources)):
        raise ValueError('Control failure in period.py at original line 204')
    output['application_controls'] = {'N': N, 'Q': Q, 'eligible_divisors': len(resources), 'full_period_resources_at_Q720': [n for n in resources if lcm(Q, n) == N], 'full_period_resources_at_Q3600': [n for n in resources if lcm(3600, n) == N], 'literal_projection_base_points': Q, 'literal_N_capacity_checks': len(resources), 'subset_shifts': shifts}
    return output
