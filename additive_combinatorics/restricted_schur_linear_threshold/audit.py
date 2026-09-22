"""Definition-level forcing-certificate auditor, independent of the generator.

Only positive integer arithmetic and color consistency are used. There is no
case split, compression formula, generator import, solver, or floating point.
"""


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def check(k, ell, blue, sums, bound):
    demand(type(k) is int and type(ell) is int and k >= ell >= 2, 'parameters')
    demand(type(bound) is int and bound >= 2 * ell - 1, 'bound')
    blue = list(blue)
    demand(len(set(blue)) == len(blue), 'duplicate prefix value')
    demand(all(type(x) is int and 1 <= x <= 2 * ell - 1 for x in blue), 'prefix domain')
    colors = {x: int(x in blue) for x in range(1, 2 * ell)}
    for number, terms in enumerate(sums, 1):
        demand(isinstance(terms, (list, tuple)) and len(terms) == ell, 'distinct summand count')
        demand(all(isinstance(t, (list, tuple)) and len(t) == 2 for t in terms), 'term format')
        demand(all(type(x) is int and type(c) is int and 1 <= x <= bound and c > 0 for x, c in terms), 'term domain')
        values = [x for x, _ in terms]
        demand(len(set(values)) == ell, 'duplicate summand value')
        demand(sum(c for _, c in terms) == k, 'total multiplicity')
        demand(all(x in colors for x in values), 'unforced summand')
        color = colors[values[0]]
        demand(all(colors[x] == color for x in values), 'mixed summand colors')
        result = sum(x * c for x, c in terms)
        demand(max(values) < result <= bound, 'result domain')
        if result in colors:
            if colors[result] == color:
                return number
        else:
            colors[result] = 1 - color
    raise ValueError('certificate ends without contradiction')
