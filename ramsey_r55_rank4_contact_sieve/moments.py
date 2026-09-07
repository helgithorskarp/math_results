"""Exact single and pair violation counts by subspace Mobius inversion."""
from functools import lru_cache
from itertools import product
from collections import Counter
from math import comb
from fractions import Fraction
import json
from baseline import bins, compute as baseline_count


@lru_cache(None)
def spaces(r):
    all_spaces = {frozenset([0])}
    layer = all_spaces.copy()
    for _ in range(r):
        new = set()
        for subspace in layer:
            for v in range(1, 2**r):
                if v not in subspace:
                    new.add(subspace | frozenset(x ^ v for x in subspace))
        all_spaces.update(new)
        layer = new
    return tuple(sorted(all_spaces, key=lambda s: (len(s), sorted(s))))


def mobius(r, s):
    codim = r-(len(s).bit_length()-1)
    return (-1)**codim * 2**comb(codim, 2)


def row_event(m, r, cap, threshold, marked, zeros):
    """Exactly zeros zeros, every marked independent type has threshold..cap copies."""
    fixed = [1 << i for i in range(marked)]
    out = 0
    for pops in product(range(threshold, cap+1), repeat=marked):
        if sum(pops)+zeros > m:
            continue
        choices = comb(m, zeros)
        left = m-zeros
        for t in pops:
            choices *= comb(left, t)
            left -= t
        spanning = sum(mobius(r, s)*bins(left, len(s)-1-marked, cap)
                       for s in spaces(r) if all(x in s for x in fixed))
        out += choices*spanning
    return out


@lru_cache(None)
def cells_count(cells, n, cap, marked, bad):
    """Sum multinomial assignments among contact cells; total n nonzero labels."""
    total = 0
    def visit(cell, remaining, weight, degrees):
        nonlocal total
        if cell == len(cells):
            if remaining == 0 and all(d in bad for d in degrees):
                total += weight
            return
        for t in range(min(remaining, cells[cell]*cap)+1):
            ways = bins(t, cells[cell], cap)
            if ways:
                visit(cell+1, remaining-t, weight*comb(remaining, t)*ways,
                      tuple(d+t*((cell >> i) & 1) for i, d in enumerate(degrees)))
    visit(0, n, 1, (0,)*marked)
    return total


def column_event(n, r, cap, marked, zeros, bad):
    hist = Counter()
    for s in spaces(r):
        cells = [0]*(2**marked)
        for y in s:
            if y:
                cells[y & (2**marked-1)] += 1
        hist[tuple(cells)] += mobius(r, s)
    return comb(n, zeros)*sum(coef*cells_count(cells, n-zeros, cap, marked, tuple(bad))
                              for cells, coef in hist.items() if coef)


def run():
    bad = tuple(range(10))+tuple(range(14, 24))
    rows = {str(l): [row_event(20, 4, 4, 3, l, z) for z in range(2)] for l in (1, 2)}
    columns = {str(l): [column_event(23, 4, 5, l, z, bad) for z in range(3)] for l in (1, 2)}
    flags = {l: rows[str(l)][0]*sum(columns[str(l)])+rows[str(l)][1]*columns[str(l)][0] for l in (1, 2)}
    first, rem1 = divmod(15*flags[1], 20160)
    second, rem2 = divmod(comb(15, 2)*flags[2], 20160)
    if rem1 or rem2:
        raise ArithmeticError("nonintegral factor quotient")
    old = baseline_count()
    overlap = old["stages"][-1]["complement_rank_three_overlap"]
    lower = first-second-overlap
    fraction = Fraction(lower, old["remaining"])
    if not 0 < lower < old["remaining"]:
        raise ArithmeticError("nonmaterial or impossible removal bound")
    return {"status": "EXACT_CONTACT_SIEVE_MOMENTS", "subspaces": len(spaces(4)),
            "rows": rows, "columns": columns, "first_moment": first,
            "second_binomial_moment": second, "old_complement_overlap": overlap,
            "baseline": old["remaining"], "removed_lower_bound": lower,
            "remaining_upper_bound": old["remaining"]-lower,
            "removed_fraction_lower_bound": [fraction.numerator, fraction.denominator],
            "internal_free_bits": 443}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
