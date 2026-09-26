"""Exact local laws with an entirely empty transverse height plane.

Distributions are dicts from five selected-height masks to Fraction masses.
They are local distributions, never global point-set witnesses.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def subsets(mask, size):
    return tuple(sum(1 << z for z in zs)
                 for zs in combinations([z for z in range(5) if mask >> z & 1], size))


def uniform_fiber(size):
    masks = subsets(30, size)
    require(bool(masks), 'fiber size outside zero through four')
    return {mask: Fraction(1, len(masks)) for mask in masks}


def load_templates():
    data = json.loads((Path(__file__).resolve().parent/'small_templates.json').read_text())
    return {tuple(item['profile']): item['templates'] for item in data}


def ordinary_law(profile):
    """Line cap four: cover the four nonzero horizontal lines by holes.

Every selected set omits height zero. Arbitrary permutations of the four
nonzero heights preserve the two stated blocking properties here; they
are not asserted to preserve arbitrary affine line configurations.
"""
    require(len(profile) == 5 and all(type(v) is int and 0 <= v <= 4 for v in profile)
            and sum(profile) <= 16, 'bad ordinary profile')
    rows = []
    cursor = 0
    for v in profile:
        holes = {(cursor+j) % 4+1 for j in range(4-v)}
        cursor += 4-v
        rows.append(30-sum(1 << z for z in holes))
    require(cursor >= 4, 'the four horizontal lines are not covered')
    result = defaultdict(Fraction)
    for perm in permutations(range(1, 5)):
        image = tuple(sum(1 << perm[z-1] for z in range(1, 5) if mask >> z & 1)
                      for mask in rows)
        result[image] += Fraction(1, 24)
    return dict(result)


def small_top_law(profile, templates=None):
    """Line cap three, total ten: fourteen templates in seven profile types."""
    if templates is None:
        templates = load_templates()
    require(len(profile) == 5 and all(type(v) is int and 0 <= v <= 3 for v in profile)
            and sum(profile) == 10, 'bad top small profile')
    normalized, a, b = min((tuple(profile[(a*t+b) % 5] for t in range(5)), a, b)
                           for a in range(1, 5) for b in range(5))
    require(normalized in templates, 'missing affine profile representative')
    result = defaultdict(Fraction)
    for entry in templates[normalized]:
        rows = entry['rows']
        shifts = range(5) if entry['translate_rows'] else (0,)
        mass = Fraction(*entry['weight'])/(4*len(shifts))
        for shift, scale in product(shifts, range(1, 5)):
            image = [0]*5
            for t in range(5):
                mask = rows[(t+shift) % 5]
                image[(a*t+b) % 5] = sum(1 << ((scale*z) % 5)
                                        for z in range(5) if mask >> z & 1)
            result[tuple(image)] += mass
    return dict(result)


def small_law(profile, templates=None):
    """Uniformly delete inside fibers after padding to ten points."""
    require(len(profile) == 5 and all(type(v) is int and 0 <= v <= 3 for v in profile)
            and sum(profile) <= 10, 'bad small profile')
    padded = list(profile)
    needed = 10-sum(padded)
    for t in range(5):
        increment = min(needed, 3-padded[t])
        padded[t] += increment
        needed -= increment
    require(needed == 0, 'padding failed')
    result = defaultdict(Fraction)
    for rows, mass in small_top_law(tuple(padded), templates).items():
        choices = [subsets(mask, v) for mask, v in zip(rows, profile)]
        count = 1
        for domain in choices:
            count *= len(domain)
        for image in product(*choices):
            result[image] += mass/count
    return dict(result)


def quotient_lines():
    return tuple(tuple((b, t) for t in range(5)) for b in range(5)) + tuple(
        tuple((t, (a*t+b) % 5) for t in range(5))
        for a in range(5) for b in range(5))


def family71(weights):
    """The universal law is supported outside z=0; it cannot glue globally."""
    require(len(weights) == 25 and all(type(v) is int and 0 <= v <= 4 for v in weights)
            and sum(weights) == 71, 'bad 71-weight quotient')
    profiles = [tuple(weights[5*x+y] for x, y in line) for line in quotient_lines()]
    require(all(7 <= sum(profile) <= 16 for profile in profiles), 'bad quotient line sum')
    require(all(max(profile) <= 3 for profile in profiles if sum(profile) <= 10),
            'small-plane fiber implication failed')
    return [(line, small_law(profile) if sum(profile) <= 10 else ordinary_law(profile))
            for line, profile in zip(quotient_lines(), profiles)]
