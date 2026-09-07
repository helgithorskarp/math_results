"""Actual-span subtraction and per-letter integer polynomials; no moments import."""
from functools import lru_cache
from itertools import combinations, product
from collections import defaultdict
from math import comb
from independent_baseline import words, subspaces


@lru_cache(None)
def marked_span(left, r, cap, marked):
    """Span with marked independent vectors; all other labels differ from them and zero."""
    return words(left, 2**r-1-marked, cap)-sum(
        subspaces(r-marked, k-marked)*marked_span(left, k, cap, marked)
        for k in range(marked, r))


def row_event(m, r, cap, threshold, marked, zeros):
    out = 0
    for pops in product(range(threshold, cap+1), repeat=marked):
        if sum(pops)+zeros > m:
            continue
        left = m-zeros
        assignments = comb(m, zeros)
        for t in pops:
            assignments *= comb(left, t)
            left -= t
        out += assignments*marked_span(left, r, cap, marked)
    return out


@lru_cache(None)
def lattice(r):
    """All subspaces via every possible basis subset of size at most r."""
    found = set()
    for k in range(r+1):
        for basis in combinations(range(1, 2**r), k):
            values = set()
            for selection in product((0, 1), repeat=k):
                value = 0
                for use, x in zip(selection, basis):
                    if use:
                        value ^= x
                values.add(value)
            found.add(frozenset(values))
    return tuple(sorted(found, key=lambda x: (len(x), sorted(x))))


@lru_cache(None)
def polynomial(cells, n, cap, marked):
    """Insert each actual nonzero letter, recording length and every contact degree."""
    state = {(0,)+(0,)*marked: 1}
    for signature, multiplicity in enumerate(cells):
        for _ in range(multiplicity):
            next_state = defaultdict(int)
            for key, count in state.items():
                used, degrees = key[0], key[1:]
                for t in range(min(cap, n-used)+1):
                    nk = (used+t,)+tuple(d+t*((signature >> i) & 1) for i, d in enumerate(degrees))
                    next_state[nk] += count*comb(used+t, t)
            state = dict(next_state)
    return state


def column_event(n, r, cap, marked, zeros, bad):
    exact = {}
    for s in lattice(r):
        cells = tuple(sum(y != 0 and (y & (2**marked-1)) == t for y in s) for t in range(2**marked))
        state = polynomial(cells, n-zeros, cap, marked)
        contained = sum(value for key, value in state.items()
                        if key[0] == n-zeros and all(d in bad for d in key[1:]))
        exact[s] = contained-sum(value for sub, value in exact.items() if sub < s)
        if exact[s] < 0:
            raise ArithmeticError("negative actual-span count")
    return comb(n, zeros)*exact[frozenset(range(2**r))]
