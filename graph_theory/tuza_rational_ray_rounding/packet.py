"""Construct finite typed packets and cyclic lifts; no solver dependency."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import lcm


def compile_packet(profile):
    capacities = {tuple(e): Fraction(1) for e in profile['edges']}
    capacities.update({(i, i): Fraction(1, 2) for i in profile['loops']})
    weights = {tuple(row['types']): Fraction(row['weight'])
               for row in profile['primal']}
    denominator = lcm(*(v.denominator for v in [*capacities.values(), *weights.values()]))
    loads = Counter()
    for triangle, value in weights.items():
        for edge in combinations(triangle, 2):
            loads[edge] += value
    types, components = [], []

    def append_component(roles):
        vertices = list(range(len(types), len(types) + len(roles)))
        types.extend(roles)
        components.append(vertices)

    for triangle, value in sorted(weights.items()):
        count = denominator * value
        if count.denominator != 1 or count < 0:
            raise ValueError('invalid triangle multiplicity')
        for _ in range(int(count)):
            append_component(triangle)
    for edge, capacity in sorted(capacities.items()):
        count = denominator * (capacity - loads[edge])
        if count.denominator != 1 or count < 0:
            raise ValueError('invalid spare-edge multiplicity')
        for _ in range(int(count)):
            append_component(edge)
    return {'denominator': denominator, 'types': types, 'components': components}


def latin_lift(packing, factor):
    if factor < 1:
        raise ValueError('factor must be positive')
    return [[a * factor + i, b * factor + j, c * factor + (i + j) % factor]
            for a, b, c in packing
            for i in range(factor) for j in range(factor)]


def label_substitute(packing, base_order, order, blocks):
    """Replace each ordered label block by a copy of the base packing."""
    return [[(v // base_order) * order + block[v % base_order] for v in triangle]
            for block in blocks for triangle in packing]
