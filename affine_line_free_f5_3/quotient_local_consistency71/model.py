"""Construct planar sections with prescribed fiber sizes over F_5."""
from itertools import product
import json
from pathlib import Path


def load_templates():
    records = json.loads((Path(__file__).resolve().parent/'templates.json').read_text())
    return {(r['line_cap'], tuple(r['profile'])): tuple(r['rows']) for r in records}


TEMPLATES = load_templates()


def lift_profile(weights, line_cap=4):
    """Return five selected-height masks with exactly the given weights.

    For line_cap=4 the domain is 0<=w_i<=4, sum w_i<=16.
    For line_cap=3 the domain is 0<=w_i<=3, sum w_i<=10.
    The latter restriction is sufficient for every small plane at N=71.
    """
    if line_cap not in (3, 4):
        raise ValueError('line cap must be three or four')
    target = 10 if line_cap == 3 else 16
    if len(weights) != 5 or any(type(v) is not int or not 0 <= v <= line_cap
                                for v in weights) or sum(weights) > target:
        raise ValueError('inadmissible profile')
    padded = list(weights)
    needed = target-sum(padded)
    for t in range(5):
        increment = min(needed, line_cap-padded[t])
        padded[t] += increment
        needed -= increment
    if needed:
        raise ValueError('padding failed')
    normalized, a, b = min((tuple(padded[(a*t+b) % 5] for t in range(5)), a, b)
                           for a in range(1, 5) for b in range(5))
    rows = [0]*5
    for t, mask in enumerate(TEMPLATES[line_cap, normalized]):
        original = (a*t+b) % 5
        selected = [z for z in range(5) if mask >> z & 1]
        rows[original] = sum(1 << z for z in selected[:weights[original]])
    return tuple(rows)


def height_images(rows):
    """Uniform 100-element affine group (t,z)->(t,a*z+b*t+c)."""
    for a in range(1, 5):
        for b, c in product(range(5), repeat=2):
            yield tuple(sum(1 << ((a*z+b*t+c) % 5)
                            for z in range(5) if mask >> z & 1)
                        for t, mask in enumerate(rows))


def quotient_lines():
    """Ordered affine parameters: x=b, then y=a*x+b, with t=0,...,4."""
    return tuple(tuple((b, t) for t in range(5)) for b in range(5)) + tuple(
        tuple((t, (a*t+b) % 5) for t in range(5))
        for a in range(5) for b in range(5))


def local_family(weights):
    """Return one 100-term distribution for each projection plane.

    A family is pairwise consistent on full shared fibers. It is not a
    distribution on global lifts. This routine imposes no height gauge.
    """
    if len(weights) != 25 or any(type(v) is not int or not 0 <= v <= 4 for v in weights):
        raise ValueError('bad quotient weights')
    if sum(weights) != 71:
        raise ValueError('the universal theorem here is for total 71')
    family = []
    for line in quotient_lines():
        profile = tuple(weights[5*x+y] for x, y in line)
        size = sum(profile)
        if not 7 <= size <= 16:
            raise ValueError('bad quotient line weight')
        cap = 3 if size <= 10 else 4
        rows = lift_profile(profile, cap)
        family.append((line, tuple(height_images(rows))))
    return tuple(family)
